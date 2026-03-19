"""
Session Logger -- writes SESSION_LOG_FORMAT.md compliant logs to agent folders.

Every node that executes produces a session log entry in the acting agent's
logs/ directory. The log format follows corporeal/system/SESSION_LOG_FORMAT.md:
  - YAML frontmatter (machine-parseable)
  - Archetype-specific body
  - Decisions, files modified, blockers, current state, next steps

This module is called after each node completes, receiving the node's
state update and the agent metadata.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_session_log(
    agent: dict[str, Any],
    node_name: str,
    state_update: dict[str, Any],
    project_id: str,
    full_state: dict[str, Any],
    corporeal_root: Path,
) -> Path | None:
    """Write a session log for a node execution.

    Args:
        agent: Agent record from AGENTS.json (must have domain_root, path, serial, etc.)
        node_name: Which graph node produced this (architect, coordinator, worker, reviewer)
        state_update: The partial state dict returned by the node
        project_id: Project identifier for frontmatter
        full_state: Full graph state at time of logging (for context)
        corporeal_root: Absolute path to corporeal/ root

    Returns:
        Path to the written log file, or None if logging failed.
    """
    agent_folder = corporeal_root / agent.get("domain_root", "") / agent.get("path", "")
    if not agent_folder.exists():
        return None

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    log_dir = agent_folder / "logs" / date_str
    log_dir.mkdir(parents=True, exist_ok=True)

    slug = _make_slug(node_name, project_id, full_state)
    log_path = log_dir / f"{slug}.md"

    serial = agent.get("serial", "UNKNOWN")
    identity = agent.get("identity", "UNKNOWN")
    archetype = agent.get("archetype", "unknown")
    placement_tier = agent.get("placement_tier", "unknown")
    domain = agent.get("domain", "unknown")

    # Determine task_order_ref
    task_order_ref = "null"
    if node_name == "worker":
        to = state_update.get("task_order") or full_state.get("task_order")
        if to and hasattr(to, "id"):
            task_order_ref = to.id

    # Build the log content
    content = _build_frontmatter(
        identity=identity,
        serial=serial,
        archetype=archetype,
        placement_tier=placement_tier,
        domain=domain,
        date=date_str,
        status="COMPLETE",
        project=project_id,
        task_order_ref=task_order_ref,
    )

    content += f"# {_title_for_node(node_name, full_state)} -- {serial}\n\n"
    content += f"**Date:** {date_str}\n"
    content += f"**Start:** {time_str}\n"
    content += f"**End:** {time_str}\n\n"

    # Objective
    content += "## Objective\n\n"
    content += _objective_for_node(node_name, full_state) + "\n\n"
    content += "---\n\n"

    # Body (archetype-specific)
    content += _body_for_node(node_name, archetype, placement_tier, state_update, full_state)

    # Decisions Made
    content += "## Decisions Made\n\n"
    content += "| Decision | Authority | Rationale |\n"
    content += "|----------|-----------|----------|\n"
    content += _decisions_for_node(node_name, state_update, full_state)
    content += "\n---\n\n"

    # Files Modified
    content += "## Files Modified\n\n"
    content += "| File | Change |\n"
    content += "|------|--------|\n"
    deliverables = state_update.get("deliverables", [])
    if deliverables:
        for d in deliverables:
            for fp in getattr(d, "file_paths", []):
                content += f"| `{fp}` | Created/modified by {node_name} |\n"
    else:
        content += "| (none) | Runtime node -- no direct file modifications |\n"
    content += "\n---\n\n"

    # Task Orders (if coordinator)
    task_orders = state_update.get("task_orders", [])
    if task_orders:
        content += "## Task Orders Issued / Updated\n\n"
        content += "| Task Order | Recipient | Status |\n"
        content += "|------------|-----------|--------|\n"
        for to in task_orders:
            content += f"| `{to.id}` | {to.identity} ({to.archetype}) | issued |\n"
        content += "\n---\n\n"

    # Blockers
    content += "## Blockers\n\n"
    escalations = state_update.get("escalations", [])
    if escalations:
        for e in escalations:
            content += f"- {e.reason} (authority: {e.authority_type})\n"
    else:
        content += "- NONE\n"
    content += "\n---\n\n"

    # Current State
    phase = full_state.get("current_phase", state_update.get("current_phase", "unknown"))
    error = state_update.get("error", "")
    content += "## Current State\n\n"
    content += f"**Status:** {phase.upper()}\n"
    if error:
        content += f"Error: {error}\n"
    content += _state_summary_for_node(node_name, state_update, full_state) + "\n\n"
    content += "---\n\n"

    # Next Steps
    content += "## Next Steps\n\n"
    content += _next_steps_for_node(node_name, full_state) + "\n"

    log_path.write_text(content, encoding="utf-8")
    return log_path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_frontmatter(**fields) -> str:
    lines = ["---"]
    for k, v in fields.items():
        lines.append(f"{k}: {v}")
    lines.append("---\n\n")
    return "\n".join(lines)


def _make_slug(node_name: str, project_id: str, state: dict) -> str:
    safe_pid = re.sub(r"[^a-zA-Z0-9-]", "", project_id)[:20]
    brief = state.get("project_brief", "")
    brief_slug = re.sub(r"[^a-z0-9]+", "-", brief.lower())[:30].strip("-")

    # Workers need task_order_id + serial to produce unique slugs.
    # Without this, all workers in the same project overwrite each other's logs.
    if node_name == "worker":
        task_order = state.get("task_order")
        to_id = ""
        if task_order:
            to_id = getattr(task_order, "id", "") if hasattr(task_order, "id") else str(task_order.get("id", ""))
        serial = state.get("serial", "")
        # Extract the short task ID (e.g., "T001" from "EXP-001-PSCFIX-T001")
        short_to = to_id.rsplit("-", 1)[-1] if to_id else ""
        safe_serial = re.sub(r"[^a-zA-Z0-9-]", "", serial)[:15]
        suffix = "-".join(filter(None, [short_to, safe_serial]))
        return f"{node_name}-{safe_pid}-{suffix}" if suffix else f"{node_name}-{safe_pid}-{brief_slug}"

    return f"{node_name}-{safe_pid}-{brief_slug}"


def _title_for_node(node_name: str, state: dict) -> str:
    brief = state.get("project_brief", "project")[:60]
    titles = {
        "architect": f"Design Spec for {brief}",
        "coordinator": f"Task Decomposition for {brief}",
        "worker": f"Task Execution for {brief}",
        "reviewer": f"Deliverable Review for {brief}",
    }
    return titles.get(node_name, f"{node_name.title()} Node Execution")


def _objective_for_node(node_name: str, state: dict) -> str:
    brief = state.get("project_brief", "")
    objectives = {
        "architect": f"Produce a design specification for the project brief: {brief}",
        "coordinator": "Decompose the approved design spec into concrete task orders for worker agents.",
        "worker": "Execute the assigned task order and produce deliverables.",
        "reviewer": "Validate all deliverables against acceptance criteria and produce evaluations.",
    }
    return objectives.get(node_name, "Execute graph node.")


def _body_for_node(
    node_name: str,
    archetype: str,
    placement_tier: str,
    state_update: dict,
    full_state: dict,
) -> str:
    """Build the archetype-specific body section."""

    # Exec-tier architects get Session Narrative
    if archetype == "architect" and placement_tier == "exec":
        spec = state_update.get("design_spec", "")
        if spec:
            return (
                "## Session Narrative\n\n"
                f"{spec}\n\n"
                "---\n\n"
            )

    # Coordinators get sweep-like results
    if node_name == "coordinator":
        task_orders = state_update.get("task_orders", [])
        result = "## Work Completed\n\n"
        result += f"### 1. Task Order Decomposition\n\n"
        result += f"Decomposed design spec into {len(task_orders)} task orders.\n\n"
        for to in task_orders:
            result += f"- **{to.id}** ({to.archetype}): {to.objective[:80]}\n"
        result += "\n---\n\n"
        return result

    # Workers get standard Work Completed
    if node_name == "worker":
        deliverables = state_update.get("deliverables", [])
        result = "## Work Completed\n\n"
        result += "### 1. Task Order Execution\n\n"
        for d in deliverables:
            result += f"Deliverable `{d.id}` produced for task `{d.task_order_id}`.\n"
            result += f"Content length: {len(d.content)} chars. "
            result += f"Files: {', '.join(d.file_paths) if d.file_paths else 'none'}.\n\n"
        result += "---\n\n"
        return result

    # Reviewer
    if node_name == "reviewer":
        evaluations = state_update.get("evaluations", [])
        result = "## Work Completed\n\n"
        result += "### 1. Deliverable Review\n\n"
        if evaluations:
            result += "| Deliverable | Verdict | Completeness | Correctness | Adherence | Scope |\n"
            result += "|-------------|---------|-------------|-------------|-----------|-------|\n"
            for ev in evaluations:
                result += f"| `{ev.deliverable_id}` | {ev.verdict} | {ev.completeness} | {ev.correctness} | {ev.adherence} | {ev.scope_discipline} |\n"
        result += "\n---\n\n"
        return result

    # Default
    return "## Work Completed\n\n### 1. Node Execution\n\nCompleted.\n\n---\n\n"


def _decisions_for_node(node_name: str, state_update: dict, full_state: dict) -> str:
    decisions = {
        "architect": "| Produced design spec | L2 | Architect synthesized brief into structured PRD |\n",
        "coordinator": "| Decomposed spec into task orders | L1 | Coordinator applied value chain mapping |\n",
        "reviewer": "| Evaluated deliverables | L1 | Reviewer applied acceptance criteria |\n",
    }
    return decisions.get(node_name, "| Executed task order | local | Worker followed task order requirements |\n")


def _state_summary_for_node(node_name: str, state_update: dict, full_state: dict) -> str:
    summaries = {
        "architect": "Design spec produced. Awaiting approval gate.",
        "coordinator": f"{len(state_update.get('task_orders', []))} task orders ready for dispatch.",
        "worker": f"{len(state_update.get('deliverables', []))} deliverables submitted for review.",
        "reviewer": f"{len(state_update.get('evaluations', []))} evaluations complete.",
    }
    return summaries.get(node_name, "Node execution complete.")


def _next_steps_for_node(node_name: str, full_state: dict) -> str:
    steps = {
        "architect": "1. **Approval gate** -- Principal reviews and approves/rejects design spec\n",
        "coordinator": "1. **Dispatch workers** -- Fan out task orders to archetype nodes\n",
        "worker": "1. **Submit to reviewer** -- Deliverables await quality evaluation\n",
        "reviewer": "1. **Complete or escalate** -- Pass to end or surface failures to Principal\n",
    }
    return steps.get(node_name, "1. **Continue** -- Next graph node\n")
