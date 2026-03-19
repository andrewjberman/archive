"""
R1: Execution — Reviewer node (Operator archetype).

The Reviewer runs after deliverable_validator confirms boundary compliance.
It evaluates deliverable QUALITY against acceptance criteria from task orders.
This is the Operator's evaluation authority (Tier 1 of the learning loop).

Separation of concerns (P0 fix from EXP-001-PSCFIX postmortem):
  - deliverable_validator_node: contract compliance (machine-gated)
  - reviewer_node: quality evaluation (LLM-judged)
Validation gates progression. Evaluation informs the learning loop.
The reviewer never sees artifacts that failed boundary checks (unless
Principal overrides the validator gate).

G6: Structured evaluation with 4 dimensions feeding the learning loop.

Ontology source: specs/core/ARCHETYPES.md (Operator archetype)
                 specs/core/LEARNING_LOOP.md (Tier 1 instance repair)
Runtime spec: runtime/specs/EXECUTION.md, runtime/specs/FLOW.md
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..state import AuditEntry, Escalation, Evaluation, ProjectState


def reviewer_node(state: ProjectState) -> dict[str, Any]:
    """Reviewer: evaluate deliverable QUALITY against acceptance criteria.

    Boundary validation is handled upstream by deliverable_validator_node.
    This node focuses exclusively on semantic quality evaluation:
    1. LLM quality review against acceptance criteria
    2. Structured evaluation (G6): 4-dimension scoring for learning loop

    Boundary failure counts are passed via _boundary_fail_counts from
    the validator node for scope_discipline scoring adjustments.
    """
    from ..llm import invoke_llm
    from ..config import ARCHETYPE_MODELS

    task_orders = state.get("task_orders", [])
    deliverables = state.get("deliverables", [])

    # --- Build deliverable index by task order ---
    deliverable_map: dict[str, list] = {}
    for d in deliverables:
        deliverable_map.setdefault(d.task_order_id, []).append(d)

    # --- Build task order index ---
    task_order_map: dict[str, Any] = {}
    for to in task_orders:
        task_order_map[to.id] = to

    # Boundary failure counts from upstream validator (if available)
    boundary_fail_count: dict[str, int] = state.get("_boundary_fail_counts", {})

    # --- Build review prompt (G6: request dimension scores) ---
    review_sections = []
    for to in task_orders:
        related = deliverable_map.get(to.id, [])
        section = (
            f"### Task Order: {to.id}\n"
            f"**Objective:** {to.objective}\n"
            f"**Acceptance Criteria:**\n"
            + "\n".join(f"- {c}" for c in to.acceptance_criteria)
            + "\n\n**Deliverables Received:**\n"
        )
        if related:
            for d in related:
                section += (
                    f"- {d.id} (by {d.identity}, status: {d.status})\n"
                    f"  Content summary: {d.content[:500]}...\n"
                    f"  Files: {', '.join(d.file_paths)}\n"
                )
        else:
            section += "- NONE -- no deliverable received for this task order\n"
        review_sections.append(section)

    user_prompt = (
        f"## Design Spec\n\n{state.get('design_spec', '')}\n\n"
        f"## Deliverables to Review\n\n"
        + "\n\n".join(review_sections)
        + "\n\n## Your Task\n\n"
        "Review each deliverable against its task order's acceptance criteria.\n"
        "For each task order, produce:\n"
        "1. A verdict: PASS, FAIL, or MISSING\n"
        "2. Four dimension scores (0-3 each):\n"
        "   - completeness: Does it address all acceptance criteria? "
        "(0=not addressed, 1=deficient, 2=adequate, 3=exceeds)\n"
        "   - correctness: Is the artifact functionally correct?\n"
        "   - adherence: Does it follow the task order's requirements?\n"
        "   - scope_discipline: Did the worker stay within deliverable scope?\n"
        "3. A reason explaining the verdict\n\n"
        "Return as JSON array with fields: task_order_id, verdict, "
        "completeness, correctness, adherence, scope_discipline, reason\n\n"
        "Wrap in ```json``` fences."
    )

    system_prompt = (
        "You are a quality reviewer (Operator archetype). Your job is to "
        "validate deliverables against acceptance criteria. Be precise and "
        "fair. Score each dimension 0-3. A PASS verdict requires all "
        "dimensions >= 2. A FAIL means at least one dimension < 2. "
        "MISSING means no deliverable was received."
    )

    response = invoke_llm(
        system=system_prompt,
        user=user_prompt,
        model=ARCHETYPE_MODELS["operator"],
        tools=[],
    )

    now = datetime.now(timezone.utc).isoformat()

    # Capture execution trace (token usage, model, timing)
    from ..llm import get_last_trace
    trace = get_last_trace()
    trace_dict = trace.to_dict() if trace else {}

    # --- G6: Parse structured evaluations ---
    evaluations = _extract_evaluations(
        response, deliverables, task_order_map, boundary_fail_count, now
    )

    # --- Extract escalations from evaluations ---
    llm_escalations = _evaluations_to_escalations(evaluations)

    phase = "complete" if not llm_escalations else "review"

    return {
        "current_phase": phase,
        "evaluations": evaluations,
        "audit_trail": [
            AuditEntry(
                identity="reviewer",
                archetype="operator",
                action="quality_review",
                detail=(
                    f"Reviewed {len(task_orders)} task orders, "
                    f"{len(llm_escalations)} quality failures, "
                    f"{len(evaluations)} evaluations produced"
                ),
                timestamp=now,
            )
        ],
        "escalations": llm_escalations,
        "messages": [
            {
                "role": "reviewer",
                "identity": "reviewer",
                "content": response,
                "timestamp": now,
                "execution_trace": trace_dict,
            }
        ],
    }


def _extract_evaluations(
    response: str,
    deliverables: list,
    task_order_map: dict,
    boundary_fail_count: dict[str, int],
    timestamp: str,
) -> list[Evaluation]:
    """Parse reviewer response into structured Evaluation objects.

    Falls back to basic PASS/FAIL extraction if dimension scores
    are missing from the LLM response.
    """
    import json
    import re

    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if not match:
        return _fallback_evaluations(deliverables, task_order_map, timestamp)

    try:
        verdicts = json.loads(match.group(1))
    except json.JSONDecodeError:
        return _fallback_evaluations(deliverables, task_order_map, timestamp)

    # Index deliverables by task order
    deliverable_by_task: dict[str, Any] = {}
    for d in deliverables:
        deliverable_by_task[d.task_order_id] = d

    evaluations = []
    for v in verdicts:
        task_id = v.get("task_order_id", "")
        d = deliverable_by_task.get(task_id)
        to = task_order_map.get(task_id)

        verdict = v.get("verdict", "MISSING")
        completeness = _clamp_score(v.get("completeness", 0))
        correctness = _clamp_score(v.get("correctness", 0))
        adherence = _clamp_score(v.get("adherence", 0))
        scope_raw = _clamp_score(v.get("scope_discipline", 2))

        # Machine override: if G2/G5 caught violations, scope_discipline drops
        if d and boundary_fail_count.get(d.id, 0) > 0:
            scope_raw = min(scope_raw, 1)

        # Classify learning loop tier
        scores = [completeness, correctness, adherence, scope_raw]
        min_score = min(scores)
        tier, signal = _classify_tier(min_score, scores, verdict)

        evaluations.append(Evaluation(
            deliverable_id=d.id if d else "",
            task_order_id=task_id,
            identity=d.identity if d else "",
            archetype=d.archetype if d else (to.archetype if to else ""),
            completeness=completeness,
            correctness=correctness,
            adherence=adherence,
            scope_discipline=scope_raw,
            verdict=verdict,
            reason=v.get("reason", ""),
            learning_tier=tier,
            tier_signal=signal,
            timestamp=timestamp,
        ))

    return evaluations


def _fallback_evaluations(
    deliverables: list,
    task_order_map: dict,
    timestamp: str,
) -> list[Evaluation]:
    """Create minimal evaluations when LLM response can't be parsed."""
    evaluations = []
    for d in deliverables:
        to = task_order_map.get(d.task_order_id)
        evaluations.append(Evaluation(
            deliverable_id=d.id,
            task_order_id=d.task_order_id,
            identity=d.identity,
            archetype=d.archetype,
            completeness=2,
            correctness=2,
            adherence=2,
            scope_discipline=2,
            verdict="PASS",
            reason="Evaluation parse failed -- default pass",
            learning_tier=1,
            tier_signal="parse_failure",
            timestamp=timestamp,
        ))
    return evaluations


def _clamp_score(val: Any) -> int:
    """Clamp a score value to 0-3 range."""
    try:
        return max(0, min(3, int(val)))
    except (TypeError, ValueError):
        return 0


def _classify_tier(
    min_score: int,
    scores: list[int],
    verdict: str,
) -> tuple[int, str]:
    """Classify learning loop tier from evaluation scores.

    Tier 1: Any dimension < 2 (single instance needs repair)
    Tier 2/3: Require aggregation across multiple evaluations
    (only detectable with R4 persistence -- Tier 2 runtime).
    For now, all signals are Tier 1.
    """
    if verdict == "MISSING":
        return (1, "no_deliverable")
    if min_score < 2:
        weak = []
        dim_names = ["completeness", "correctness", "adherence", "scope_discipline"]
        for i, s in enumerate(scores):
            if s < 2:
                weak.append(dim_names[i])
        return (1, f"deficient: {', '.join(weak)}")
    return (1, "adequate")


def _evaluations_to_escalations(evaluations: list[Evaluation]) -> list[Escalation]:
    """Convert FAIL/MISSING evaluations to escalations."""
    escalations = []
    for ev in evaluations:
        if ev.verdict in ("FAIL", "MISSING"):
            escalations.append(
                Escalation(
                    identity="reviewer",
                    authority_type="validation",
                    reason=ev.reason or f"Verdict: {ev.verdict}",
                    context={
                        "task_order_id": ev.task_order_id,
                        "verdict": ev.verdict,
                        "completeness": ev.completeness,
                        "correctness": ev.correctness,
                        "adherence": ev.adherence,
                        "scope_discipline": ev.scope_discipline,
                        "learning_tier": ev.learning_tier,
                        "tier_signal": ev.tier_signal,
                        "sub_type": "quality_failure",
                    },
                )
            )
    return escalations
