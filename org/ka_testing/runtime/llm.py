"""
LLM invocation layer.

Abstracts the actual LLM call so nodes don't couple to a specific
provider. Tier 1 uses the Anthropic Python SDK directly.

Execution trace: every tool-use invocation produces an ExecutionTrace
object stored at module level. The calling node can read it via
get_last_trace() after invoke_llm() returns. The trace contains:
- tool_calls: list of {name, inputs, output, success, iteration}
- token_usage: {input_tokens, output_tokens, total_tokens, by_iteration}
- iterations: number of LLM round-trips in the tool loop
- model: which model was used

This is the agent execution trace — a first-class artifact for
debugging, cost tracking, and learning loop telemetry.

Swap this module to change LLM providers without touching node logic.
"""

from __future__ import annotations

import os
import re
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Concurrency control — bounds parallel API calls within a dispatch level
# ---------------------------------------------------------------------------

_CONCURRENT_LIMIT = int(os.environ.get("HIERARCHY_CONCURRENT_CALLS", "2"))
_semaphore = threading.Semaphore(_CONCURRENT_LIMIT)

# Default iteration limit for the agentic tool loop.
# Tier-aware callers override this via invoke_llm(max_iterations=N).
# History: was 25 (original), reduced to 10 (rate limit fix, broke workers),
# now 20 (workers need 15-20 to read AND write).
DEFAULT_MAX_ITERATIONS = 20


# ---------------------------------------------------------------------------
# Execution trace — first-class artifact from tool-use invocations
# ---------------------------------------------------------------------------

@dataclass
class ToolCall:
    """Record of a single tool invocation."""
    iteration: int
    name: str
    inputs: dict[str, Any] = field(default_factory=dict)
    output: str = ""
    success: bool = True
    timestamp: str = ""


@dataclass
class ExecutionTrace:
    """Full trace of an LLM tool-use invocation.

    Produced by _invoke_with_tools, stored at module level,
    readable via get_last_trace(). Contains everything needed
    to replay, debug, or audit the agent's execution.
    """
    model: str = ""
    iterations: int = 0
    tool_calls: list[ToolCall] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    tokens_by_iteration: list[dict[str, int]] = field(default_factory=list)
    stop_reason: str = ""
    timestamp: str = ""

    @property
    def tool_call_count(self) -> int:
        return len(self.tool_calls)

    @property
    def failed_tool_calls(self) -> list[ToolCall]:
        return [tc for tc in self.tool_calls if not tc.success]

    def to_dict(self) -> dict[str, Any]:
        """Serialize for JSON storage / audit trail."""
        return {
            "model": self.model,
            "iterations": self.iterations,
            "tool_calls": [
                {
                    "iteration": tc.iteration,
                    "name": tc.name,
                    "inputs": {k: str(v)[:200] for k, v in tc.inputs.items()},
                    "output": tc.output[:500],
                    "success": tc.success,
                }
                for tc in self.tool_calls
            ],
            "token_usage": {
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "total_tokens": self.total_tokens,
            },
            "tokens_by_iteration": self.tokens_by_iteration,
            "stop_reason": self.stop_reason,
            "failed_tool_calls": len(self.failed_tool_calls),
        }


# ---------------------------------------------------------------------------
# KF gate v3 — Signal scanner and predicate evaluator
# (SYS.CORE.KF_GATED_EXEC_IMPL Sections 1-3)
# ---------------------------------------------------------------------------

# Unicode rightwards arrow U+2192. ASCII -> must NOT match (test_wrong_arrow).
_TRANSITION_PATTERN = re.compile(
    r'\[\[TRANSITION:\s*(\w+)\s*\u2192\s*(\w+)\s*\]\]'
)
_COMPLETE_PATTERN = re.compile(r'\[\[COMPLETE\]\]')
_CONSTRAINT_PATTERN = re.compile(
    r'\[\[ARCHETYPE_CONSTRAINT:\s*required=([^,\]]+),\s*request=([^\]]+)\]\]'
)


def scan_signals(text: str) -> dict:
    """Scan a model response for KF gate v3 transition signals.

    Returns a dict with keys:
      transition: tuple(from_stage, to_stage) or None
      complete:   bool
      constraint: dict(required, request) or None

    Only the first occurrence of each signal type is returned.

    Spec: SYS.CORE.KF_GATED_EXEC_IMPL Section 1
    """
    t = _TRANSITION_PATTERN.search(text)
    c = _COMPLETE_PATTERN.search(text)
    k = _CONSTRAINT_PATTERN.search(text)
    return {
        "transition": (t.group(1).strip(), t.group(2).strip()) if t else None,
        "complete": c is not None,
        "constraint": {
            "required": k.group(1).strip(),
            "request": k.group(2).strip(),
        } if k else None,
    }


_READ_PHASE_TOOLS = frozenset({"glob", "grep", "read_file", "run_command",
                                "list_dir", "grep_files"})


@dataclass
class StagePredicateResult:
    satisfied: bool
    reason: str  # empty string when satisfied


def evaluate_transition_predicate(
    from_stage: str,
    tool_call_history: list[dict],
    deliverable_paths: list[str],
    working_dir: str = ".",
) -> StagePredicateResult:
    """Evaluate whether a stage transition is permitted.

    Two governance boundaries enforced:
      In → Ac  at least one read tool called across Pe+In combined
      Ac → Ad  all declared deliverable paths exist on disk

    Pe → In is NOT enforced (model-reported subdivision, no governance value).
    Ad → done always permitted.

    Spec: SYS.CORE.KF_GATED_EXEC_IMPL Section 3
    """
    if from_stage == "Pe":
        return StagePredicateResult(satisfied=True, reason="")

    elif from_stage == "In":
        read_calls = [
            tc for tc in tool_call_history
            if tc.get("stage") in ("Pe", "In") and tc.get("name") in _READ_PHASE_TOOLS
        ]
        if not read_calls:
            return StagePredicateResult(
                satisfied=False,
                reason=(
                    "No read tools were called during the read phase (Pe + In). "
                    "At least one observation (glob, grep, read_file, or "
                    "run_command) is required before entering the write phase."
                ),
            )
        return StagePredicateResult(satisfied=True, reason="")

    elif from_stage == "Ac":
        if not deliverable_paths:
            return StagePredicateResult(satisfied=True, reason="")
        missing = [
            dp for dp in deliverable_paths
            if not (Path(working_dir) / dp).exists()
        ]
        if missing:
            return StagePredicateResult(
                satisfied=False,
                reason=(
                    f"Declared deliverables not yet written: {missing}. "
                    "Produce all deliverables before advancing to Adjudication."
                ),
            )
        return StagePredicateResult(satisfied=True, reason="")

    # Ad terminal, unknown stages: do not block
    return StagePredicateResult(satisfied=True, reason="")


# Module-level trace storage (last invocation)
_last_trace: ExecutionTrace | None = None


def get_last_trace() -> ExecutionTrace | None:
    """Get the execution trace from the most recent invoke_llm call.

    Returns None if the last call was a simple (non-tool) invocation.
    """
    return _last_trace


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _ensure_api_key():
    """Load .env from repo root if ANTHROPIC_API_KEY not set."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return
    search = Path(__file__).resolve().parent
    for _ in range(10):
        env_path = search / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())
            return
        search = search.parent


def invoke_llm(
    system: str,
    user: str,
    model: str | None = None,
    tools: list[Any] | None = None,
    max_tokens: int = 8192,
    max_iterations: int | None = None,
) -> str:
    """Call an LLM and return the text response.

    For Tier 1 this uses the Anthropic SDK. Tool use (agentic loop)
    is handled by _invoke_with_tools for workers.

    After this call returns, get_last_trace() provides the full
    execution trace (tool calls, token usage, iterations) for
    tool-use invocations. Returns None for simple invocations.

    Args:
        system: System prompt.
        user: User message content.
        model: Model ID (defaults to config.DEFAULT_MODEL).
        tools: Tool definitions. If non-empty, uses agentic tool loop.
        max_tokens: Max response tokens.
        max_iterations: Max tool-use loop iterations. If None, uses
            DEFAULT_MAX_ITERATIONS (20). Callers should set this based
            on complexity tier: Tier T = 20, Tier M = 25.

    Returns:
        The assistant's text response.
    """
    global _last_trace
    from .config import DEFAULT_MODEL

    model = model or DEFAULT_MODEL

    with _semaphore:
        if tools:
            iterations = max_iterations if max_iterations is not None else DEFAULT_MAX_ITERATIONS
            text, trace = _invoke_with_tools(system, user, model, tools, max_tokens, iterations)
            _last_trace = trace
            return text
        _last_trace = None
        return _invoke_simple(system, user, model, max_tokens)


def invoke_llm_staged(
    system: str,
    user: str,
    stages: list[dict],
    model: str | None = None,
    max_tokens: int = 8192,
    hook_registry: Any = None,
) -> str:
    """KF-Gated tool loop: run multiple stages with different tool sets.

    Each stage has:
      - name: KF stage name ("Pe", "In", "Ac", "Ad")
      - tools: tool definitions available in this stage
      - budget: max iterations for this stage
      - transition_msg: message injected when entering this stage

    Conversation history carries across stages. The tool set changes
    at each gate boundary. This is the mechanism that prevents
    infinite-reading: Ac stage has no read tools.

    Args:
        hook_registry: Optional HookRegistry for PreToolUse/PostToolUse
            callbacks. Hooks can block tool calls (PreToolUse) or modify
            output (PostToolUse) in real time during execution.

    ONT.CORE.KF_GATED_EXECUTION Section 2.

    Returns the combined text response.
    """
    global _last_trace
    from .config import DEFAULT_MODEL

    model = model or DEFAULT_MODEL

    with _semaphore:
        text, trace = _invoke_staged(system, user, model, stages, max_tokens, hook_registry)
        _last_trace = trace
        return text


def _invoke_staged(
    system: str,
    user: str,
    model: str,
    stages: list[dict],
    max_tokens: int,
    hook_registry: Any = None,
) -> tuple[str, ExecutionTrace]:
    """Multi-stage tool loop with per-stage tool scoping.

    Carries message history across stages. Tool set changes at
    each stage boundary. Injects a transition message so the LLM
    knows its available tools have changed.
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic package not installed.")

    _ensure_api_key()
    client = anthropic.Anthropic()

    messages = [{"role": "user", "content": user}]
    all_text: list[str] = []
    global_iteration = 0
    # All tool calls across all stages — needed for In→Ac predicate (Pe+In combined)
    all_tool_history: list[dict] = []

    trace = ExecutionTrace(
        model=model,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    def _emit_iter(iteration, iter_input, iter_output, tool_names, stop_reason, stage_name):
        try:
            from .events import get_event_bus, LLM_ITERATION
            bus = get_event_bus()
            if bus:
                bus.emit(LLM_ITERATION, detail={
                    "iteration": iteration + 1,
                    "max_iterations": sum(s.get("budget", 0) for s in stages),
                    "stage": stage_name,
                    "input_tokens": iter_input,
                    "output_tokens": iter_output,
                    "cumulative_input": trace.input_tokens,
                    "cumulative_output": trace.output_tokens,
                    "tool_calls": len(tool_names),
                    "tool_names": tool_names,
                    "stop_reason": stop_reason,
                })
        except Exception:
            pass

    def _emit_tool(iteration, name, path, success, stage_name):
        try:
            from .events import get_event_bus, LLM_TOOL_CALL
            bus = get_event_bus()
            if bus:
                bus.emit(LLM_TOOL_CALL, detail={
                    "iteration": iteration + 1,
                    "stage": stage_name,
                    "tool_name": name,
                    "tool_path": path,
                    "success": success,
                })
        except Exception:
            pass

    for stage in stages:
        stage_name = stage.get("name", "?")
        stage_tools = stage.get("tools", [])
        stage_budget = stage.get("budget", 0)
        transition_msg = stage.get("transition_msg", "")
        stage_deliverables = stage.get("deliverables", [])
        stage_working_dir = stage.get("working_dir", ".")
        predicate_enabled = stage.get("predicate_enabled", True)
        # current_sub_stage tracks Pe→In model-reported subdivision within the
        # read phase. Predicate check uses this, not the stage dict name.
        current_sub_stage = stage_name

        if stage_budget <= 0:
            continue

        anthropic_tools = _convert_tools(stage_tools)

        # Inject stage transition message (except for the first stage)
        if transition_msg:
            messages.append({"role": "user", "content": transition_msg})

        for stage_iter in range(stage_budget):
            response = _call_with_retry(
                client, model=model, max_tokens=max_tokens,
                system=system, messages=messages,
                tools=anthropic_tools if anthropic_tools else None,
            )

            usage = getattr(response, "usage", None)
            iter_input = getattr(usage, "input_tokens", 0) if usage else 0
            iter_output = getattr(usage, "output_tokens", 0) if usage else 0
            trace.input_tokens += iter_input
            trace.output_tokens += iter_output
            trace.total_tokens += iter_input + iter_output
            trace.tokens_by_iteration.append({
                "iteration": global_iteration,
                "stage": stage_name,
                "input_tokens": iter_input,
                "output_tokens": iter_output,
            })

            assistant_content = response.content
            messages.append({"role": "assistant", "content": assistant_content})

            tool_calls = [b for b in assistant_content if b.type == "tool_use"]
            text_blocks = [b for b in assistant_content if b.type == "text"]

            for tb in text_blocks:
                all_text.append(tb.text)

            global_iteration += 1
            trace.iterations = global_iteration
            trace.stop_reason = getattr(response, "stop_reason", "")

            # --- KF gate v3: scan response for governance signals ---
            iter_text = "\n".join(b.text for b in text_blocks)
            signals = scan_signals(iter_text)

            # Track Pe→In sub-stage transition (informational — no tool set change)
            if (signals.get("transition") == ("Pe", "In")
                    and current_sub_stage == "Pe"
                    and stage_name == "Pe"):
                current_sub_stage = "In"
                try:
                    from .events import get_event_bus, KF_TRANSITION
                    bus = get_event_bus()
                    if bus:
                        bus.emit(KF_TRANSITION, detail={
                            "from_stage": "Pe", "to_stage": "In",
                            "trigger": "explicit_signal",
                            "iteration": global_iteration,
                        })
                except Exception:
                    pass

            if not tool_calls:
                _emit_iter(global_iteration - 1, iter_input, iter_output, [], trace.stop_reason, stage_name)

                # [[COMPLETE]] always exits
                if signals.get("complete"):
                    break

                # [[ARCHETYPE_CONSTRAINT]] — emit event, inject ack, continue
                constraint = signals.get("constraint")
                if constraint:
                    try:
                        from .events import get_event_bus, ARCHETYPE_CONSTRAINT
                        bus = get_event_bus()
                        if bus:
                            bus.emit(ARCHETYPE_CONSTRAINT, detail={
                                "stage": current_sub_stage,
                                "required_tool": constraint["required"],
                                "request_type": constraint["request"],
                                "iteration": global_iteration,
                            })
                    except Exception:
                        pass
                    messages.append({"role": "user", "content": (
                        f"Constraint noted. Required tool: {constraint['required']}. "
                        f"Request type: {constraint['request']}. "
                        f"Coordinator has been notified. Continue with available tools."
                    )})
                    continue  # Not a stage exit — worker continues

                # Predicate check before accepting voluntary transition
                if not predicate_enabled:
                    break  # Ratio-only variant: voluntary transition always accepted

                pred = evaluate_transition_predicate(
                    from_stage=current_sub_stage,
                    tool_call_history=all_tool_history,
                    deliverable_paths=stage_deliverables,
                    working_dir=stage_working_dir,
                )
                if not pred.satisfied:
                    messages.append({"role": "user", "content": (
                        f"TRANSITION DENIED: {pred.reason}\n"
                        f"Continue in {current_sub_stage} stage."
                    )})
                    try:
                        from .events import get_event_bus, KF_TRANSITION_DENIED
                        bus = get_event_bus()
                        if bus:
                            bus.emit(KF_TRANSITION_DENIED, detail={
                                "stage": current_sub_stage,
                                "reason": pred.reason,
                                "iteration": global_iteration,
                            })
                    except Exception:
                        pass
                    continue  # Stay in stage

                # Predicate satisfied — voluntary transition accepted
                try:
                    from .events import get_event_bus, KF_TRANSITION
                    bus = get_event_bus()
                    if bus:
                        bus.emit(KF_TRANSITION, detail={
                            "from_stage": current_sub_stage,
                            "to_stage": "next",
                            "trigger": "voluntary",
                            "iteration": global_iteration,
                        })
                except Exception:
                    pass
                break  # Exit stage loop

            tool_results = []
            tool_names = []
            hook_ctx = {"stage": stage_name, "iteration": global_iteration}
            for tc in tool_calls:
                now = datetime.now(timezone.utc).isoformat()
                _path = str(tc.input.get("file_path", tc.input.get("pattern", tc.input.get("command", ""))))[:60]

                # --- PreToolUse hook ---
                effective_input = dict(tc.input)
                if hook_registry and hasattr(hook_registry, "run_pre"):
                    pre_result = hook_registry.run_pre(tc.name, tc.input, hook_ctx)
                    if pre_result.blocked:
                        result = f"BLOCKED by hook: {pre_result.message}"
                        success = False
                        trace.tool_calls.append(ToolCall(
                            iteration=global_iteration - 1, name=tc.name,
                            inputs=tc.input, output=result[:2000],
                            success=False, timestamp=now,
                        ))
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tc.id,
                            "content": result,
                        })
                        tool_names.append(tc.name)
                        _emit_tool(global_iteration - 1, tc.name, _path, False, stage_name)
                        continue
                    if pre_result.modified_input is not None:
                        effective_input = pre_result.modified_input

                # --- Execute tool ---
                result = _execute_tool(tc.name, effective_input, stage_tools)
                success = not str(result).startswith("ERROR:") and not str(result).startswith("BLOCKED")

                # --- PostToolUse hook ---
                if hook_registry and hasattr(hook_registry, "run_post"):
                    post_result = hook_registry.run_post(tc.name, effective_input, result, hook_ctx)
                    if post_result.modified_output is not None:
                        result = post_result.modified_output

                trace.tool_calls.append(ToolCall(
                    iteration=global_iteration - 1,
                    name=tc.name,
                    inputs=effective_input,
                    output=str(result)[:2000],
                    success=success,
                    timestamp=now,
                ))
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tc.id,
                    "content": str(result),
                })
                tool_names.append(tc.name)
                all_tool_history.append({
                    "name": tc.name, "stage": current_sub_stage, "success": success,
                })
                _emit_tool(global_iteration - 1, tc.name, _path, success, stage_name)

            _emit_iter(global_iteration - 1, iter_input, iter_output, tool_names, trace.stop_reason, stage_name)
            messages.append({"role": "user", "content": tool_results})

    return "\n".join(all_text), trace


def _invoke_simple(system: str, user: str, model: str, max_tokens: int) -> str:
    """Single-turn LLM call, no tools."""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "anthropic package not installed. "
            "Run: pip install anthropic"
        )

    _ensure_api_key()
    client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

    response = _call_with_retry(
        client, model=model, max_tokens=max_tokens,
        system=system, messages=[{"role": "user", "content": user}],
    )

    # Extract text from response
    text_parts = []
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)

    return "\n".join(text_parts)


def _call_with_retry(client, *, model, max_tokens, system, messages,
                     tools=None, max_retries=5):
    """Call Anthropic API with exponential backoff on rate limit errors.

    Respects retry-after headers from the API when available.
    """
    import time as _time
    import sys

    kwargs = dict(model=model, max_tokens=max_tokens, system=system, messages=messages)
    if tools:
        kwargs["tools"] = tools

    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                # Try to extract retry-after from the exception
                retry_after = None
                if hasattr(e, "response") and hasattr(e.response, "headers"):
                    retry_after = e.response.headers.get("retry-after")
                    if retry_after:
                        try:
                            retry_after = float(retry_after)
                        except (ValueError, TypeError):
                            retry_after = None

                wait = retry_after if retry_after else min(2 ** attempt * 15, 120)
                print(f"  [RATE LIMIT] Attempt {attempt+1}/{max_retries}, "
                      f"waiting {wait:.0f}s"
                      f"{' (retry-after)' if retry_after else ''}...",
                      file=sys.stderr)
                _time.sleep(wait)
            else:
                raise
    # Final attempt without catch
    return client.messages.create(**kwargs)


def _invoke_with_tools(
    system: str,
    user: str,
    model: str,
    tools: list[Any],
    max_tokens: int,
    max_iterations: int = 20,
) -> tuple[str, ExecutionTrace]:
    """Agentic tool-use loop with execution trace capture.

    Keeps calling until no more tool_use blocks. Every tool call,
    its inputs, outputs, and success status are recorded in the
    ExecutionTrace. Token usage is accumulated across iterations.

    Args:
        max_iterations: Safety limit on tool-use loop iterations.
            Tier T = 20, Tier M = 25. Prevents unbounded API calls.

    Returns (text_response, execution_trace).
    """
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "anthropic package not installed. "
            "Run: pip install anthropic"
        )

    _ensure_api_key()
    client = anthropic.Anthropic()

    # Convert our tool definitions to Anthropic format
    anthropic_tools = _convert_tools(tools)

    messages = [{"role": "user", "content": user}]
    all_text: list[str] = []

    # Initialize trace
    trace = ExecutionTrace(
        model=model,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    # --- Per-iteration telemetry (emit events if bus available) ---
    def _emit_iter(iteration, iter_input, iter_output, tool_names, stop_reason):
        try:
            from .events import get_event_bus, LLM_ITERATION
            bus = get_event_bus()
            if bus:
                bus.emit(LLM_ITERATION, detail={
                    "iteration": iteration + 1,
                    "max_iterations": max_iterations,
                    "input_tokens": iter_input,
                    "output_tokens": iter_output,
                    "cumulative_input": trace.input_tokens,
                    "cumulative_output": trace.output_tokens,
                    "tool_calls": len(tool_names),
                    "tool_names": tool_names,
                    "stop_reason": stop_reason,
                })
        except Exception:
            pass

    def _emit_tool(iteration, name, path, success):
        try:
            from .events import get_event_bus, LLM_TOOL_CALL
            bus = get_event_bus()
            if bus:
                bus.emit(LLM_TOOL_CALL, detail={
                    "iteration": iteration + 1,
                    "tool_name": name,
                    "tool_path": path,
                    "success": success,
                })
        except Exception:
            pass

    # Agentic loop: call LLM, execute tools, feed results back
    for iteration in range(max_iterations):
        response = _call_with_retry(
            client, model=model, max_tokens=max_tokens,
            system=system, messages=messages,
            tools=anthropic_tools if anthropic_tools else None,
        )

        # Track token usage
        usage = getattr(response, "usage", None)
        iter_input = getattr(usage, "input_tokens", 0) if usage else 0
        iter_output = getattr(usage, "output_tokens", 0) if usage else 0
        trace.input_tokens += iter_input
        trace.output_tokens += iter_output
        trace.total_tokens += iter_input + iter_output
        trace.tokens_by_iteration.append({
            "iteration": iteration,
            "input_tokens": iter_input,
            "output_tokens": iter_output,
        })

        # Collect text and tool_use blocks
        assistant_content = response.content
        messages.append({"role": "assistant", "content": assistant_content})

        tool_calls = [b for b in assistant_content if b.type == "tool_use"]
        text_blocks = [b for b in assistant_content if b.type == "text"]

        for tb in text_blocks:
            all_text.append(tb.text)

        trace.iterations = iteration + 1
        trace.stop_reason = getattr(response, "stop_reason", "")

        if not tool_calls:
            # No more tool calls — agent is done
            _emit_iter(iteration, iter_input, iter_output, [], trace.stop_reason)
            break

        # Execute each tool call and build tool_result messages
        tool_results = []
        tool_names = []
        for tc in tool_calls:
            now = datetime.now(timezone.utc).isoformat()
            result = _execute_tool(tc.name, tc.input, tools)
            success = not str(result).startswith("ERROR:")

            _path = str(tc.input.get("file_path", tc.input.get("pattern", tc.input.get("command", ""))))[:60]

            trace.tool_calls.append(ToolCall(
                iteration=iteration,
                name=tc.name,
                inputs=tc.input,
                output=str(result)[:2000],
                success=success,
                timestamp=now,
            ))

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": str(result),
            })

            tool_names.append(tc.name)
            _emit_tool(iteration, tc.name, _path, success)

        _emit_iter(iteration, iter_input, iter_output, tool_names, trace.stop_reason)
        messages.append({"role": "user", "content": tool_results})

    return "\n".join(all_text), trace


def _convert_tools(tools: list[Any]) -> list[dict]:
    """Convert tool definitions to Anthropic API format.

    Tools are dicts with: name, description, input_schema (JSON Schema).
    """
    converted = []
    for tool in tools:
        if isinstance(tool, dict):
            converted.append({
                "name": tool["name"],
                "description": tool.get("description", ""),
                "input_schema": tool.get("input_schema", {"type": "object", "properties": {}}),
            })
    return converted


def _execute_tool(name: str, inputs: dict, tools: list[Any]) -> str:
    """Execute a tool by name. Dispatches to the tool's handler function."""
    for tool in tools:
        if isinstance(tool, dict) and tool["name"] == name:
            handler = tool.get("handler")
            if handler and callable(handler):
                try:
                    return handler(**inputs)
                except Exception as e:
                    return f"ERROR: Tool {name} failed: {e}"
    return f"ERROR: Tool {name} not found"
