"""
R1: Execution — Worker node.

Workers receive a task order via Send() and execute it. Each worker
gets its own state slice containing the task order + relevant context.
Workers have tool access (read, write, edit, glob, grep, bash) to
actually modify files in the working directory.

This is the node that replaces manually starting a Claude session
for each agent.

Ontology source: specs/core/ARCHETYPES.md (Worker archetypes)
Runtime spec: runtime/specs/EXECUTION.md
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from ..state import AuditEntry, Deliverable, Discovery, Escalation, ProjectState

# Re-export so sandbox stub swap works:
#   from system.os.runtime.worker import evaluate_transition_predicate
from ..llm import evaluate_transition_predicate  # noqa: F401


def worker_node(state: dict[str, Any]) -> dict[str, Any]:
    """Worker: execute a single task order.

    This node receives state from Send() — it gets the task order
    and a slice of the project state, NOT the full ProjectState.
    The worker makes an LLM call with tool access to actually modify
    files, then reports its deliverables back.

    The worker's output merges back into the parent graph's state
    via reducers (operator.add on lists).
    """
    from ..llm import invoke_llm
    from ..config import resolve_agent, load_agent_prompt, ARCHETYPE_MODELS
    from ..tools import get_worker_tools

    task_order = state["task_order"]
    working_directory = state.get("working_directory", "")
    design_spec = state.get("design_spec", "")

    # --- Artifact input verification ---
    # If the task order declares inputs (upstream deliverable IDs it consumes),
    # verify they exist in the available artifacts from prior dispatch levels.
    # Missing inputs = upstream work didn't complete. Fail fast instead of
    # producing semantically wrong output against stale/missing data.
    declared_inputs = getattr(task_order, "inputs", [])
    available = set(state.get("available_artifact_ids", []))
    if declared_inputs:
        missing = [i for i in declared_inputs if i not in available]
        if missing:
            now_fail = datetime.now(timezone.utc).isoformat()
            return {
                "deliverables": [],
                "audit_trail": [
                    AuditEntry(
                        identity=state.get("identity", task_order.identity),
                        archetype=getattr(task_order, "archetype", "transformer"),
                        action="input_artifact_missing",
                        detail=(
                            f"Task {task_order.id}: declared inputs {missing} "
                            f"not in available artifacts. Failing fast."
                        ),
                        timestamp=now_fail,
                    )
                ],
            }

    # --- PRE-FLIGHT GATES (EXECINT Section 8.1) ---
    # Three deterministic checks before the LLM call. No tokens consumed
    # if a pre-flight gate fails.

    # PRE-FLIGHT 1: Resource existence check
    # Verify files referenced in context_refs actually exist.
    # Try: absolute, relative to working_directory, relative to CORPOREAL_ROOT.
    # Skip refs that match deliverable paths from declared dependencies —
    # those don't exist yet but will after the upstream worker completes.
    # The dispatch planner guarantees dependency ordering.
    from pathlib import Path as _Path
    import os as _os
    _corporeal_root = _os.environ.get("CORPOREAL_ROOT", "")
    _working_dir = _Path(working_directory) if working_directory else _Path(".")

    # Collect deliverable paths from declared dependency task orders
    _upstream_deliverables = set()
    for _dep_id in task_order.dependencies:
        for _to in state.get("task_orders", []):
            if hasattr(_to, "id") and _to.id == _dep_id:
                _upstream_deliverables.update(getattr(_to, "deliverables", []))

    missing_resources = []
    for ref in getattr(task_order, "context_refs", []):
        if not ref:
            continue
        # Skip refs that are outputs of upstream dependency tasks
        if ref in _upstream_deliverables:
            continue
        # Try absolute path (also resolves .. components)
        ref_path = _Path(ref)
        if ref_path.exists():
            continue
        # Try resolved absolute path (handles .. traversal)
        try:
            if ref_path.resolve().exists():
                continue
        except (OSError, ValueError):
            pass
        # Try relative to working directory (also resolve ..)
        wd_ref = _working_dir / ref
        if wd_ref.exists():
            continue
        try:
            if wd_ref.resolve().exists():
                continue
        except (OSError, ValueError):
            pass
        # Try relative to CORPOREAL_ROOT
        if _corporeal_root:
            cr_ref = _Path(_corporeal_root) / ref
            if cr_ref.exists():
                continue
            try:
                if cr_ref.resolve().exists():
                    continue
            except (OSError, ValueError):
                pass
        missing_resources.append(ref)
    if missing_resources:
        # Soft gate: warn but proceed. Workers have tools (glob, grep, read)
        # to discover files at runtime. Blocking on hallucinated coordinator
        # paths wastes the entire dispatch cycle. The worker LLM can adapt.
        import sys
        print(
            f"WARN: Pre-flight 1 (soft): Task {task_order.id}: "
            f"context_refs not found: {missing_resources}. Proceeding anyway.",
            file=sys.stderr,
        )

    # PRE-FLIGHT 2: Specification completeness check
    # Detect obviously incomplete requirements (TODO, TBD, placeholder)
    import re as _re
    ambiguous_reqs = []
    for i, req in enumerate(task_order.requirements):
        if _re.search(r'\b(TODO|TBD|PLACEHOLDER|\.\.\.)\b', req, _re.IGNORECASE):
            ambiguous_reqs.append(f"requirement[{i}]: {req[:80]}")
    if ambiguous_reqs:
        now_pf2 = datetime.now(timezone.utc).isoformat()
        return {
            "deliverables": [],
            "audit_trail": [
                AuditEntry(
                    identity=state.get("identity", task_order.identity),
                    archetype=getattr(task_order, "archetype", "transformer"),
                    action="preflight_spec_ambiguous",
                    detail=(
                        f"Task {task_order.id}: ambiguous requirements: "
                        f"{ambiguous_reqs}. Pre-flight 2 failed."
                    ),
                    timestamp=now_pf2,
                )
            ],
            "escalations": [
                Escalation(
                    identity=state.get("identity", task_order.identity),
                    authority_type="execution",
                    reason=f"AMBIGUOUS: Incomplete requirements: {ambiguous_reqs}",
                    context={
                        "ambiguities": ambiguous_reqs,
                        "preflight_gate": 2,
                        "interrupt_type": "AMBIGUOUS",
                        "task_order_id": task_order.id,
                    },
                )
            ],
        }

    # PRE-FLIGHT 3: Upstream dependency check
    # Verify all declared dependencies are satisfied
    dep_failures = []
    for dep in task_order.dependencies:
        dep_str = str(dep)
        if "status" in dep_str and "complete" not in dep_str.lower():
            if "pending" in dep_str.lower() or "blocked" in dep_str.lower():
                dep_failures.append(dep_str[:80])
    if dep_failures:
        now_pf3 = datetime.now(timezone.utc).isoformat()
        return {
            "deliverables": [],
            "audit_trail": [
                AuditEntry(
                    identity=state.get("identity", task_order.identity),
                    archetype=getattr(task_order, "archetype", "transformer"),
                    action="preflight_upstream_blocked",
                    detail=(
                        f"Task {task_order.id}: upstream dependencies not met: "
                        f"{dep_failures}. Pre-flight 3 failed."
                    ),
                    timestamp=now_pf3,
                )
            ],
            "escalations": [
                Escalation(
                    identity=state.get("identity", task_order.identity),
                    authority_type="execution",
                    reason=f"BLOCKED: Upstream dependencies not complete: {dep_failures}",
                    context={
                        "blocked_on": dep_failures,
                        "resource_type": "upstream_deliverable",
                        "preflight_gate": 3,
                        "interrupt_type": "BLOCKED",
                        "task_order_id": task_order.id,
                    },
                )
            ],
        }

    # --- Resolve identity (G1: identity injected via Send payload) ---
    # The edge function (route_to_workers) resolves identity and puts
    # identity, serial, archetype in the Send payload. We read from
    # payload first, fall back to task_order fields.
    identity = state.get("identity", task_order.identity)
    serial = state.get("serial", "")
    archetype = state.get("archetype", getattr(task_order, "archetype", "transformer"))

    try:
        agent = resolve_agent(identity)
        system_prompt = load_agent_prompt(agent)
        archetype = agent.get("archetype", archetype)
    except (ValueError, KeyError):
        # NEW agent or unregistered — use generic worker prompt
        system_prompt = (
            "You are a worker agent. Execute your task order precisely. "
            "Write code, modify files, and produce the deliverables specified. "
            "Be thorough but stay within scope. Do not modify files outside "
            "your task order's deliverables list unless absolutely necessary."
        )

    # --- Build context from references ---
    _tier = state.get("complexity_tier", "M")
    context_text = _load_context_refs(task_order.context_refs, complexity_tier=_tier)

    # --- Build worker prompt ---
    user_prompt = (
        f"## Task Order: {task_order.id}\n\n"
        f"**Objective:** {task_order.objective}\n\n"
        f"**Requirements:**\n"
        + "\n".join(f"- {r}" for r in task_order.requirements)
        + "\n\n"
        f"**Acceptance Criteria:**\n"
        + "\n".join(f"- {c}" for c in task_order.acceptance_criteria)
        + "\n\n"
        f"**Expected Deliverables:**\n"
        + "\n".join(f"- {d}" for d in task_order.deliverables)
        + "\n\n"
        f"**Dependencies:**\n"
        + "\n".join(f"- {dep}" for dep in task_order.dependencies)
        + "\n\n"
        f"**Required Inputs (upstream artifacts):**\n"
        + ("\n".join(f"- {inp}" for inp in declared_inputs) if declared_inputs else "- (none declared)")
        + "\n\n"
    )

    # Inject deliverable schema if present -- constrains worker output format
    _schema = getattr(task_order, "deliverable_schema", {})
    if _schema:
        user_prompt += (
            f"## Deliverable Schema (MANDATORY)\n\n"
            f"Your output files MUST conform to this schema. Do NOT invent values\n"
            f"outside the enums defined here. Validation will reject non-conforming output.\n\n"
            f"```json\n{json.dumps(_schema, indent=2)}\n```\n\n"
        )

    user_prompt += (
        f"## Design Spec (for reference)\n\n{design_spec}\n\n"
        f"## Working Directory\n\n{working_directory}\n\n"
    )

    if context_text:
        user_prompt += f"## Context References\n\n{context_text}\n\n"

    # --- Inject discoveries from peer/upstream workers (ONT.CORE.ARTIFACT v2) ---
    # These are facts learned by other workers in this project run.
    # They prevent you from re-deriving what has already been discovered.
    injected = state.get("injected_discoveries", [])
    if injected:
        user_prompt += "## Prior Discoveries (from peer workers)\n\n"
        user_prompt += (
            "Other workers in this project have already discovered the following. "
            "Use these facts directly — do not re-derive them.\n\n"
        )
        for disc in injected:
            content = getattr(disc, "content", {}) or {}
            cat = getattr(disc, "category", "unknown")
            agent = getattr(disc, "agent_serial", "unknown")
            if cat == "resource_resolution":
                user_prompt += (
                    f"- **Path correction** ({agent}): "
                    f"`{content.get('referenced', '?')}` is actually at "
                    f"`{content.get('resolved_to', '?')}`\n"
                )
            elif cat == "resource_absence":
                user_prompt += (
                    f"- **Missing resource** ({agent}): "
                    f"`{content.get('referenced', '?')}` does not exist\n"
                )
            elif cat == "structure_correction":
                user_prompt += (
                    f"- **Structure note** ({agent}): "
                    f"{content.get('note', '?')}\n"
                )
            elif cat == "environment_observation":
                user_prompt += (
                    f"- **Environment** ({agent}): "
                    f"{content.get('note', '?')}\n"
                )
            else:
                note = content.get("note", str(content))
                user_prompt += f"- **{cat}** ({agent}): {note}\n"
        user_prompt += "\n"

    user_prompt += (
        "## Instructions\n\n"
        "Execute this task order by using your tools. You MUST use tools to "
        "accomplish the work — do not just describe what you would do.\n\n"
        "Your execution follows Knowledge Function stages. Your available tools "
        "will CHANGE between stages. You will be notified when a stage transition "
        "occurs. In the ACTION stage, read tools are removed — you must write "
        "your deliverables from what you already know.\n\n"
        "The deliverables are FILESYSTEM CHANGES, not text descriptions. "
        "If you do not call write_file or edit_file, your task order is not complete."
    )

    # --- KF-Gated tool loop (ONT.CORE.KF_GATED_EXECUTION v3) ---
    # Two phases: read (Pe+In combined) and write (Ac+Ad combined).
    # Phase budgets driven by read_ratio (Layer 2). Tool sets enforced per phase.
    from ..archetype_enforcer import scope_tools_for_archetype
    from ..tools import scope_tools_for_stage, resolve_read_ratio
    scope_boundary = state.get("scope_boundary", None)
    allowed_paths = task_order.deliverables if scope_boundary == "strict" else None

    _READ_CAP = {"S": 10000, "T": 30000, "M": 0}
    _max_read = _READ_CAP.get(_tier, 0)
    all_tools = get_worker_tools(working_directory, allowed_paths=allowed_paths, max_read_chars=_max_read)
    all_tools = scope_tools_for_archetype(all_tools, archetype)

    _TIER_ITERATIONS = {"S": 10, "T": 20, "M": 25}
    _max_iter = _TIER_ITERATIONS.get(_tier, 20)
    _read_ratio = getattr(task_order, "read_ratio", 0.6)
    read_ceiling, write_budget = resolve_read_ratio(_read_ratio, _max_iter)

    deliverables_list = "\n".join(f"- {d}" for d in task_order.deliverables) if task_order.deliverables else "(none declared)"

    # Build 2-phase staged invocation
    stages = []
    if read_ceiling > 0:
        stages.append({
            "name": "Pe",
            "tools": scope_tools_for_stage("Pe", all_tools),
            "budget": read_ceiling,
            "transition_msg": "",
            "predicate_stage": "Pe",
            "deliverables": task_order.deliverables,
            "working_dir": working_directory,
        })
    if write_budget > 0:
        stages.append({
            "name": "Ac",
            "tools": scope_tools_for_stage("Ac", all_tools),
            "budget": write_budget,
            "transition_msg": (
                "STAGE TRANSITION: You are now in the ACTION stage.\n"
                "glob and grep removed. Available tools: "
                "write_file, edit_file, apply_patch, read_file (your own output only).\n\n"
                "TIP: Use apply_patch for modifying existing files (unified diff format).\n"
                "It is much more token-efficient than write_file for edits.\n"
                "Use write_file only for creating new files from scratch.\n\n"
                f"Declared deliverables:\n{deliverables_list}\n\n"
                "Signal completion with [[COMPLETE]] or [[TRANSITION: Ac\u2192Ad]] "
                "once all deliverables are written."
            ),
            "predicate_stage": "Ac",
            "deliverables": task_order.deliverables,
            "working_dir": working_directory,
        })

    # --- Build hook registry for this worker ---
    from ..hooks import HookRegistry, HookMatcher, make_schema_validation_hook, make_audit_hook
    _hooks = HookRegistry()

    # Real-time schema validation on writes (catches violations during Ac, not after)
    _schema = getattr(task_order, "deliverable_schema", {})
    if _schema and task_order.deliverables:
        _hooks.register("PreToolUse", HookMatcher(
            "write_file|edit_file",
            [make_schema_validation_hook(_schema, task_order.deliverables)],
        ))

    # Audit trail hook (logs every tool call to event bus)
    _hooks.register("PostToolUse", HookMatcher(
        "*",
        [make_audit_hook(identity, task_order.id)],
    ))

    from ..llm import invoke_llm_staged
    response = invoke_llm_staged(
        system=system_prompt,
        user=user_prompt,
        stages=stages,
        model=ARCHETYPE_MODELS.get(archetype, ARCHETYPE_MODELS["transformer"]),
        hook_registry=_hooks,
    )

    now = datetime.now(timezone.utc).isoformat()

    # --- Capture execution trace (tool calls + token usage) ---
    from ..llm import get_last_trace
    trace = get_last_trace()
    trace_summary = ""
    trace_dict = {}
    if trace:
        trace_dict = trace.to_dict()
        failed = len(trace.failed_tool_calls)
        trace_summary = (
            f"iterations={trace.iterations}, "
            f"tool_calls={trace.tool_call_count} ({failed} failed), "
            f"tokens={trace.total_tokens} "
            f"(in={trace.input_tokens}, out={trace.output_tokens})"
        )

    # --- Post-generation schema validation (EXECUTION_COMPLEXITY briefing item 1) ---
    schema_violations = []
    _schema = getattr(task_order, "deliverable_schema", {})
    if _schema and task_order.deliverables:
        schema_violations = _validate_deliverable_schema(
            task_order.deliverables, _schema, _working_dir,
        )
        if schema_violations:
            import sys
            print(
                f"  [SCHEMA] Task {task_order.id}: {len(schema_violations)} violation(s). "
                f"Retrying once.",
                file=sys.stderr,
            )
            # Retry: inject violations into message history and call LLM once more
            retry_prompt = (
                f"Your output has schema violations. Fix them and rewrite the affected files.\n\n"
                f"Violations:\n"
                + "\n".join(f"- {v}" for v in schema_violations[:10])
                + f"\n\nThe deliverable schema requires:\n"
                f"```json\n{json.dumps(_schema, indent=2)}\n```\n\n"
                f"Use edit_file or write_file to correct the files. Do NOT invent values "
                f"outside the schema enums."
            )
            _retry_response = invoke_llm(
                system=system_prompt,
                user=retry_prompt,
                model=ARCHETYPE_MODELS.get(archetype, ARCHETYPE_MODELS["transformer"]),
                tools=tools,
            )
            # Re-validate after retry
            schema_violations = _validate_deliverable_schema(
                task_order.deliverables, _schema, _working_dir,
            )
            if schema_violations:
                print(
                    f"  [SCHEMA] Task {task_order.id}: still {len(schema_violations)} "
                    f"violation(s) after retry.",
                    file=sys.stderr,
                )
            else:
                print(
                    f"  [SCHEMA] Task {task_order.id}: violations fixed on retry.",
                    file=sys.stderr,
                )
            # Update trace with retry
            trace2 = get_last_trace()
            if trace2:
                trace_dict = trace2.to_dict()
                trace_summary += f" +retry(tokens={trace2.total_tokens})"

    # --- Package deliverable ---
    deliverable = Deliverable(
        id=f"{task_order.id}-D001",
        task_order_id=task_order.id,
        identity=identity,
        archetype=archetype,
        content=response,
        file_paths=task_order.deliverables,
        status="submitted",
    )

    audit_entries = [
        AuditEntry(
            identity=identity,
            archetype=archetype,
            action="execute_task_order",
            detail=f"Task {task_order.id}: {task_order.objective[:80]}",
            timestamp=now,
        ),
        AuditEntry(
            identity=identity,
            archetype=archetype,
            action="execution_trace",
            detail=trace_summary or "no trace (simple invocation)",
            timestamp=now,
        ),
    ]
    if schema_violations:
        audit_entries.append(AuditEntry(
            identity=identity,
            archetype=archetype,
            action="schema_violations",
            detail=f"{len(schema_violations)} violations after retry: {'; '.join(schema_violations[:5])}",
            timestamp=now,
        ))

    # --- Extract discoveries (ONT.CORE.ARTIFACT v2: upstream output) ---
    # Discoveries are deterministic extractions from execution, not LLM inferences.
    # They flow upstream to the Coordinator for propagation to peer/downstream workers.
    worker_discoveries = []

    # Pe-stage: resource resolution discoveries from pre-flight soft gate
    if missing_resources:
        for ref in missing_resources:
            # Check if the worker actually found/used the resource at a different path
            # by scanning tool call results for file reads that resolved the reference
            resolved_path = None
            if trace:
                for tc in getattr(trace, "tool_calls", []):
                    tc_path = str(getattr(tc, "path", ""))
                    ref_basename = ref.rsplit("/", 1)[-1] if "/" in ref else ref
                    if ref_basename and ref_basename in tc_path and getattr(tc, "success", False):
                        resolved_path = tc_path
                        break
            if resolved_path:
                worker_discoveries.append(Discovery(
                    agent_serial=serial or identity,
                    task_order_id=task_order.id,
                    kf_stage="Pe",
                    scope="within_project",
                    category="resource_resolution",
                    content={
                        "referenced": ref,
                        "resolved_to": resolved_path,
                        "note": "Pre-flight ref not found; worker resolved via tools",
                    },
                    timestamp=now,
                ))
            else:
                worker_discoveries.append(Discovery(
                    agent_serial=serial or identity,
                    task_order_id=task_order.id,
                    kf_stage="Pe",
                    scope="within_project",
                    category="resource_absence",
                    content={
                        "referenced": ref,
                        "note": "Resource not found by pre-flight or during execution",
                    },
                    timestamp=now,
                ))

    # In-stage: schema violations are structure corrections
    if schema_violations:
        worker_discoveries.append(Discovery(
            agent_serial=serial or identity,
            task_order_id=task_order.id,
            kf_stage="In",
            scope="within_level",
            category="structure_correction",
            content={
                "violations": schema_violations[:10],
                "note": "Output schema mismatch detected and corrected" if not schema_violations else "Output schema mismatch persists after retry",
            },
            timestamp=now,
        ))

    return {
        "deliverables": [deliverable],
        "discoveries": worker_discoveries,
        "audit_trail": audit_entries,
        "messages": [
            {
                "role": "worker",
                "identity": identity,
                "task_order_id": task_order.id,
                "content": response,
                "timestamp": now,
                "execution_trace": trace_dict,
                "schema_violations": schema_violations,
            }
        ],
    }


def _validate_deliverable_schema(
    deliverable_paths: list[str],
    schema: dict,
    working_dir: _Path,
) -> list[str]:
    """Validate worker output files against the deliverable_schema.

    Checks JSON/YAML files on disk against enum constraints in the schema.
    Returns a list of violation strings. Empty list = all valid.
    """
    import yaml as _yaml
    violations = []

    # Extract enum constraints from schema properties
    props = schema.get("properties", {})
    enums = {}
    for field_name, field_spec in props.items():
        if "enum" in field_spec:
            enums[field_name] = set(field_spec["enum"])

    if not enums:
        return []  # No enum constraints to validate

    for dp in deliverable_paths:
        fp = working_dir / dp
        if not fp.exists():
            continue
        if fp.suffix not in (".json", ".yaml", ".yml"):
            continue

        try:
            content = fp.read_text(encoding="utf-8")
            if fp.suffix == ".json":
                data = json.loads(content)
            else:
                data = _yaml.safe_load(content)
        except Exception:
            continue

        # Validate: walk the data looking for enum-constrained fields
        _check_enums(data, enums, str(dp), violations)

    return violations


def _check_enums(
    data: Any,
    enums: dict[str, set],
    path_context: str,
    violations: list[str],
) -> None:
    """Recursively check enum constraints in a data structure."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in enums and isinstance(value, str):
                if value not in enums[key]:
                    violations.append(
                        f"{path_context}: field '{key}' has value '{value}' "
                        f"not in enum {sorted(enums[key])}"
                    )
            elif isinstance(value, (dict, list)):
                _check_enums(value, enums, path_context, violations)
    elif isinstance(data, list):
        for item in data:
            _check_enums(item, enums, path_context, violations)


def _load_context_refs(refs: list[str], complexity_tier: str = "M") -> str:
    """Load context reference files, tier-aware.

    Tier S: No loading (coordinator handles everything).
    Tier T: Metadata only (first 5 lines + size). Workers read on demand.
    Tier M: Full content up to budget (30K chars total).
    """
    from pathlib import Path
    import os

    if complexity_tier == "S":
        return ""

    corporeal_root = os.environ.get("CORPOREAL_ROOT", "")
    parts = []
    total_chars = 0
    budget = 30000 if complexity_tier == "M" else 5000  # Tier T gets smaller budget

    for ref in refs:
        p = Path(ref)
        candidates = [p]
        if corporeal_root:
            candidates.append(Path(corporeal_root) / ref)
        for candidate in candidates:
            try:
                resolved = candidate.resolve()
            except (OSError, ValueError):
                resolved = candidate
            if resolved.exists() and resolved.is_file():
                try:
                    content = resolved.read_text(encoding="utf-8")
                    if complexity_tier == "T":
                        # Metadata only: first 5 lines + size
                        lines = content.split("\n")[:5]
                        preview = "\n".join(lines)
                        size = len(content)
                        parts.append(
                            f"### {resolved.name} ({size} chars)\n\n"
                            f"{preview}\n[...use read_file for full content]\n"
                        )
                        total_chars += len(preview) + 100
                    else:
                        # Tier M: full content up to budget
                        if total_chars + len(content) > budget:
                            remaining = budget - total_chars
                            if remaining > 500:
                                parts.append(
                                    f"### {resolved.name}\n\n"
                                    f"{content[:remaining]}\n"
                                    f"[...truncated, use read_file for full content]\n"
                                )
                                total_chars = budget
                            break
                        parts.append(f"### {resolved.name}\n\n{content}\n")
                        total_chars += len(content)
                except Exception:
                    parts.append(f"### {resolved.name}\n\n[Could not read file]\n")
                break

    return "\n".join(parts)
