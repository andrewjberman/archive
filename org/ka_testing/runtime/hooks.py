"""
Hooks — lifecycle callbacks for tool execution.

Modeled after the Claude Agent SDK hook system. Hooks let the Coordinator
inject per-task-order validation, logging, or transformation without
modifying worker code.

Hook points:
  - PreToolUse: runs BEFORE a tool is executed. Can block, modify input, or allow.
  - PostToolUse: runs AFTER a tool is executed. Can modify output, log, or trigger side effects.
  - StageTransition: runs when the KF stage changes. Can inject context or modify budgets.

Hooks are registered per-worker (via the Send() payload) or globally
(via the event bus). Worker-level hooks override global hooks for the
same matcher.

Usage:
    hooks = HookRegistry()
    hooks.register("PreToolUse", HookMatcher("write_file", validate_schema))
    hooks.register("PostToolUse", HookMatcher("*", log_all_tool_calls))

    # In the tool loop:
    result = hooks.run_pre("write_file", tool_input)
    if result.blocked:
        return result.message
    output = execute_tool(...)
    hooks.run_post("write_file", tool_input, output)
"""

from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class HookResult:
    """Result from a hook execution.

    blocked: If True, the tool call is prevented.
    message: Explanation (shown to LLM if blocked, logged otherwise).
    modified_input: If set, replaces the original tool input.
    modified_output: If set, replaces the original tool output.
    metadata: Arbitrary data for downstream consumers (audit trail, telemetry).
    """
    blocked: bool = False
    message: str = ""
    modified_input: dict[str, Any] | None = None
    modified_output: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HookMatcher:
    """Associates a pattern with one or more hook callbacks.

    pattern: Tool name pattern. Supports:
      - Exact match: "write_file"
      - Pipe-separated: "write_file|edit_file|apply_patch"
      - Wildcard: "*" (matches all tools)
      - Glob: "write_*"

    hooks: List of callables. Each receives (tool_name, tool_input, context)
      and returns a HookResult. For PostToolUse, also receives tool_output.
    """
    pattern: str
    hooks: list[Callable] = field(default_factory=list)

    def matches(self, tool_name: str) -> bool:
        """Check if this matcher applies to the given tool name."""
        if self.pattern == "*":
            return True
        if "|" in self.pattern:
            return tool_name in self.pattern.split("|")
        if "*" in self.pattern or "?" in self.pattern:
            return fnmatch.fnmatch(tool_name, self.pattern)
        return tool_name == self.pattern


class HookRegistry:
    """Registry for tool lifecycle hooks.

    Hooks are organized by hook point (PreToolUse, PostToolUse, StageTransition).
    Multiple matchers can exist per hook point. They execute in registration order.
    First blocking result wins (short-circuit).
    """

    def __init__(self):
        self._hooks: dict[str, list[HookMatcher]] = {
            "PreToolUse": [],
            "PostToolUse": [],
            "StageTransition": [],
        }

    def register(self, hook_point: str, matcher: HookMatcher):
        """Register a hook matcher for a hook point."""
        if hook_point not in self._hooks:
            raise ValueError(f"Unknown hook point: {hook_point}. Valid: {list(self._hooks.keys())}")
        self._hooks[hook_point].append(matcher)

    def run_pre(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> HookResult:
        """Run PreToolUse hooks. Returns combined result.

        If any hook blocks, returns immediately with that result.
        If any hook modifies input, the modification carries forward.
        """
        ctx = context or {}
        current_input = dict(tool_input)

        for matcher in self._hooks["PreToolUse"]:
            if not matcher.matches(tool_name):
                continue
            for hook_fn in matcher.hooks:
                try:
                    result = hook_fn(tool_name, current_input, ctx)
                    if not isinstance(result, HookResult):
                        continue
                    if result.blocked:
                        return result
                    if result.modified_input is not None:
                        current_input = result.modified_input
                except Exception as e:
                    # Hooks must not crash the runtime
                    _emit_hook_error("PreToolUse", tool_name, e)

        return HookResult(modified_input=current_input if current_input != tool_input else None)

    def run_post(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
        tool_output: str,
        context: dict[str, Any] | None = None,
    ) -> HookResult:
        """Run PostToolUse hooks. Returns combined result.

        PostToolUse hooks cannot block (tool already executed).
        They can modify output or log.
        """
        ctx = context or {}
        current_output = tool_output

        for matcher in self._hooks["PostToolUse"]:
            if not matcher.matches(tool_name):
                continue
            for hook_fn in matcher.hooks:
                try:
                    result = hook_fn(tool_name, tool_input, current_output, ctx)
                    if not isinstance(result, HookResult):
                        continue
                    if result.modified_output is not None:
                        current_output = result.modified_output
                except Exception as e:
                    _emit_hook_error("PostToolUse", tool_name, e)

        return HookResult(modified_output=current_output if current_output != tool_output else None)

    def run_stage_transition(
        self,
        from_stage: str,
        to_stage: str,
        context: dict[str, Any] | None = None,
    ) -> HookResult:
        """Run StageTransition hooks when KF stage changes."""
        ctx = context or {}
        for matcher in self._hooks["StageTransition"]:
            if not matcher.matches(f"{from_stage}->{to_stage}"):
                continue
            for hook_fn in matcher.hooks:
                try:
                    result = hook_fn(from_stage, to_stage, ctx)
                    if isinstance(result, HookResult) and result.blocked:
                        return result
                except Exception as e:
                    _emit_hook_error("StageTransition", f"{from_stage}->{to_stage}", e)

        return HookResult()

    @property
    def has_hooks(self) -> bool:
        return any(matchers for matchers in self._hooks.values())


def _emit_hook_error(hook_point: str, tool_name: str, error: Exception):
    """Emit a hook error event (non-fatal)."""
    try:
        from .events import get_event_bus
        bus = get_event_bus()
        if bus:
            bus.emit("hook.error", detail={
                "hook_point": hook_point,
                "tool_name": tool_name,
                "error": str(error),
                "summary": f"Hook error: {hook_point}/{tool_name}: {error}",
            })
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Built-in hooks (registered by worker_node based on task order)
# ---------------------------------------------------------------------------

def make_schema_validation_hook(deliverable_schema: dict, deliverable_paths: list[str]) -> Callable:
    """Create a PreToolUse hook that validates write_file content against schema.

    Runs before write_file/apply_patch. Checks if the content being written
    to a deliverable path conforms to the deliverable_schema enum constraints.
    If violations found, blocks the write and returns the errors.

    This is real-time schema enforcement — catches violations DURING Ac stage
    instead of after all iterations complete.
    """
    import json

    def _hook(tool_name: str, tool_input: dict[str, Any], context: dict) -> HookResult:
        if tool_name not in ("write_file", "edit_file"):
            return HookResult()

        file_path = tool_input.get("file_path", "")
        # Only validate deliverable paths
        normalized = file_path.replace("\\", "/")
        is_deliverable = any(
            normalized.endswith(d.replace("\\", "/"))
            for d in deliverable_paths
        )
        if not is_deliverable:
            return HookResult()

        content = tool_input.get("content", "")
        if not content:
            return HookResult()

        # Try to parse as JSON and validate enums
        props = deliverable_schema.get("properties", {})
        enums = {k: set(v["enum"]) for k, v in props.items() if "enum" in v}
        if not enums:
            return HookResult()

        try:
            data = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            return HookResult()  # Not JSON — can't validate, let it through

        violations = []
        _check_enums_recursive(data, enums, file_path, violations)

        if violations:
            return HookResult(
                blocked=True,
                message=(
                    f"SCHEMA VIOLATION in {file_path}: {len(violations)} error(s).\n"
                    + "\n".join(f"  - {v}" for v in violations[:10])
                    + "\n\nFix the values and try again. Valid codes are in the "
                    "Deliverable Schema section of your task order."
                ),
                metadata={"violations": violations},
            )

        return HookResult()

    return _hook


def _check_enums_recursive(data: Any, enums: dict[str, set], path: str, violations: list):
    """Recursively check enum constraints."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in enums and isinstance(value, str) and value not in enums[key]:
                violations.append(
                    f"field '{key}' = '{value}' not in {sorted(enums[key])}"
                )
            elif isinstance(value, (dict, list)):
                _check_enums_recursive(value, enums, path, violations)
    elif isinstance(data, list):
        for item in data:
            _check_enums_recursive(item, enums, path, violations)


def make_audit_hook(identity: str, task_order_id: str) -> Callable:
    """Create a PostToolUse hook that emits audit events for every tool call."""
    def _hook(tool_name: str, tool_input: dict, tool_output: str, context: dict) -> HookResult:
        try:
            from .events import get_event_bus
            bus = get_event_bus()
            if bus:
                file_path = tool_input.get("file_path", tool_input.get("command", ""))
                success = not tool_output.startswith("ERROR:") and not tool_output.startswith("SCOPE VIOLATION")
                bus.emit("hook.audit", identity=identity, detail={
                    "tool_name": tool_name,
                    "file_path": str(file_path)[:100],
                    "task_order_id": task_order_id,
                    "success": success,
                    "output_length": len(tool_output),
                    "summary": f"audit: {tool_name}({str(file_path)[:40]})",
                })
        except Exception:
            pass
        return HookResult()

    return _hook
