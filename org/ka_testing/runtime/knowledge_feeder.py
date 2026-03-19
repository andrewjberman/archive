"""
G7: Knowledge Feeding — Runtime state to knowledge engine bridge.

Extracts knowledge events from completed ProjectState and formats them
for ingestion by the knowledge engine. Each event is typed per the 7
knowledge types from 004_KNOWLEDGE_ENGINE_EVOLUTION.md and tagged with
calibration metadata per CALIBRATION_SPEC.md.

Integration:
    from knowledge_feeder import extract_knowledge_events
    events = extract_knowledge_events(final_state)
    # events is a list of dicts compatible with index.json schema

Ontology source: LEARNING_LOOP.md (three tiers)
                 EMBEDDING_CLASSIFICATION_SPEC.md (two-layer architecture)
                 CALIBRATION_SPEC.md (zone/authority tagging)
                 004_KNOWLEDGE_ENGINE_EVOLUTION.md (7 knowledge types)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# Knowledge event types (from 004_KNOWLEDGE_ENGINE_EVOLUTION.md)
# ---------------------------------------------------------------------------

KNOWLEDGE_TYPES = {
    "decision",          # Decomposition choices, archetype assignment
    "outcome",           # Quality assessment, evaluation scores
    "lesson",            # Pattern generalization (Tier 2+, not produced in Tier 1)
    "failure",           # Archetype violations, boundary failures
    "data_lineage",      # Action sequence, agent chain
    "artifact_registry", # What was produced, by whom, which contract
    "escalation",        # Authority type, tier, resolution
}

# ---------------------------------------------------------------------------
# Calibration zones (from CALIBRATION_SPEC.md)
# ---------------------------------------------------------------------------

ZONE_MAP = {
    # Zone A: agent-exclusive operations
    "execute_task_order": "A",
    "decompose_design": "A",
    "produce_design_spec": "A",
    "validate_deliverables": "A",
    "archetype_violation_pre": "A",
    "archetype_violation_post": "A",
    "boundary_validation_failure": "A",
    # Zone B: human-exclusive decisions
    "design_approved": "B",
    "escalation_resolved": "B",
    # Zone C: handoff transitions
    "activation_required": "C",
    "activation_approved": "C",
    "deliverable_overlap": "C",
}


def extract_knowledge_events(
    state: dict[str, Any],
    project_id: str = "",
) -> list[dict[str, Any]]:
    """Extract knowledge events from completed ProjectState.

    Produces entries compatible with the knowledge engine's index.json
    schema, including the calibration extension from CALIBRATION_SPEC.md.

    Args:
        state: The final ProjectState dict after graph completion.
        project_id: Override project ID (defaults to state's project_id).

    Returns:
        List of knowledge event dicts ready for index.json ingestion.
    """
    project_id = project_id or state.get("project_id", "unknown")
    now = datetime.now(timezone.utc).isoformat()
    events: list[dict[str, Any]] = []

    # --- DECISION events: task order decomposition ---
    events.extend(_extract_decisions(state, project_id, now))

    # --- ARTIFACT_REGISTRY events: deliverables ---
    events.extend(_extract_artifacts(state, project_id, now))

    # --- OUTCOME events: evaluations ---
    events.extend(_extract_outcomes(state, project_id, now))

    # --- FAILURE events: violations and boundary failures ---
    events.extend(_extract_failures(state, project_id, now))

    # --- ESCALATION events: typed interrupts ---
    events.extend(_extract_escalations(state, project_id, now))

    # --- DATA_LINEAGE events: audit trail ---
    events.extend(_extract_lineage(state, project_id, now))

    return events


# ---------------------------------------------------------------------------
# Per-type extractors
# ---------------------------------------------------------------------------

def _extract_decisions(state: dict, project_id: str, now: str) -> list[dict]:
    """Extract DECISION events from task orders."""
    events = []
    for i, to in enumerate(state.get("task_orders", [])):
        text = (
            f"Coordinator decomposed design into task: {to.objective}. "
            f"Assigned to archetype '{to.archetype}', agent '{to.identity}'. "
            f"Deliverables: {', '.join(to.deliverables)}. "
            f"Dependencies: {', '.join(to.dependencies) if to.dependencies else 'none'}."
        )
        events.append(_make_entry(
            source_path=f"runtime:{project_id}:decision:{i}",
            heading=f"DECISION: {to.objective[:80]}",
            agent="coordinator",
            text=text,
            knowledge_type="decision",
            project=project_id,
            archetype="coordinator",
            zone="A",
            authority="agent",
            confidence=1.0,
            now=now,
        ))
    return events


def _extract_artifacts(state: dict, project_id: str, now: str) -> list[dict]:
    """Extract ARTIFACT_REGISTRY events from deliverables."""
    events = []
    for i, d in enumerate(state.get("deliverables", [])):
        text = (
            f"Agent '{d.identity}' ({d.archetype}) produced deliverable {d.id} "
            f"for task {d.task_order_id}. "
            f"Files: {', '.join(d.file_paths)}. "
            f"Status: {d.status}."
        )
        events.append(_make_entry(
            source_path=f"runtime:{project_id}:artifact:{i}",
            heading=f"ARTIFACT: {d.id} by {d.identity}",
            agent=d.identity,
            text=text,
            knowledge_type="artifact_registry",
            project=project_id,
            archetype=d.archetype,
            zone="A",
            authority="agent",
            confidence=1.0,
            now=now,
        ))
    return events


def _extract_outcomes(state: dict, project_id: str, now: str) -> list[dict]:
    """Extract OUTCOME events from evaluations (G6)."""
    events = []
    for i, ev in enumerate(state.get("evaluations", [])):
        text = (
            f"Evaluation of {ev.deliverable_id} ({ev.archetype}): "
            f"verdict={ev.verdict}. "
            f"Scores: completeness={ev.completeness}, correctness={ev.correctness}, "
            f"adherence={ev.adherence}, scope_discipline={ev.scope_discipline}. "
            f"Learning tier={ev.learning_tier} ({ev.tier_signal}). "
            f"Reason: {ev.reason}"
        )
        events.append(_make_entry(
            source_path=f"runtime:{project_id}:outcome:{i}",
            heading=f"OUTCOME: {ev.deliverable_id} {ev.verdict}",
            agent="reviewer",
            text=text,
            knowledge_type="outcome",
            project=project_id,
            archetype=ev.archetype,
            zone="A",
            authority="agent",
            confidence=0.7,  # LLM-generated scores are approximate
            now=now,
        ))
    return events


def _extract_failures(state: dict, project_id: str, now: str) -> list[dict]:
    """Extract FAILURE events from escalations with specific sub_types."""
    events = []
    for i, esc in enumerate(state.get("escalations", [])):
        sub_type = esc.context.get("sub_type", "")
        check = esc.context.get("check", "")

        # Only extract archetype violations and boundary failures as FAILURE
        if esc.authority_type == "archetype_constraint" or sub_type == "boundary_failure":
            if esc.authority_type == "archetype_constraint":
                failure_mode = "archetype_routing_error"
                zone = "A"
                confidence = 1.0
            else:
                failure_mode = "boundary_structural_deficiency"
                zone = "A"
                confidence = 1.0

            text = (
                f"FAILURE ({failure_mode}): {esc.reason}. "
                f"Authority type: {esc.authority_type}. "
                f"Agent: {esc.identity}. "
                f"Context: {esc.context}"
            )
            events.append(_make_entry(
                source_path=f"runtime:{project_id}:failure:{i}",
                heading=f"FAILURE: {failure_mode} ({esc.identity})",
                agent=esc.identity,
                text=text,
                knowledge_type="failure",
                project=project_id,
                archetype=esc.context.get("archetype", ""),
                zone=zone,
                authority="agent",
                confidence=confidence,
                now=now,
            ))
    return events


def _extract_escalations(state: dict, project_id: str, now: str) -> list[dict]:
    """Extract ESCALATION events from non-failure escalations."""
    events = []
    for i, esc in enumerate(state.get("escalations", [])):
        sub_type = esc.context.get("sub_type", "")

        # Skip failures (handled by _extract_failures) and boundary failures
        if esc.authority_type == "archetype_constraint":
            continue
        if sub_type == "boundary_failure":
            continue

        text = (
            f"Escalation ({esc.authority_type}): {esc.reason}. "
            f"Agent: {esc.identity}. "
            f"Resolved: {esc.resolved}. "
            f"Resolution: {esc.resolution or 'pending'}"
        )

        # Determine zone from context
        zone = "C" if not esc.resolved else "B"

        events.append(_make_entry(
            source_path=f"runtime:{project_id}:escalation:{i}",
            heading=f"ESCALATION: {esc.authority_type}/{sub_type}",
            agent=esc.identity,
            text=text,
            knowledge_type="escalation",
            project=project_id,
            archetype="",
            zone=zone,
            authority="handoff" if not esc.resolved else "principal",
            confidence=1.0,
            now=now,
        ))
    return events


def _extract_lineage(state: dict, project_id: str, now: str) -> list[dict]:
    """Extract DATA_LINEAGE events from the audit trail."""
    events = []

    # Build a condensed lineage from the full audit trail
    trail = state.get("audit_trail", [])
    if not trail:
        return events

    # Group by archetype to show the execution flow
    flow_steps = []
    for entry in trail:
        flow_steps.append(
            f"[{entry.archetype}] {entry.identity}: {entry.action} -- {entry.detail}"
        )

    text = (
        f"Project {project_id} execution lineage ({len(trail)} steps):\n"
        + "\n".join(flow_steps)
    )

    events.append(_make_entry(
        source_path=f"runtime:{project_id}:lineage:0",
        heading=f"LINEAGE: {project_id} ({len(trail)} steps)",
        agent="system",
        text=text,
        knowledge_type="data_lineage",
        project=project_id,
        archetype="",
        zone="A",
        authority="agent",
        confidence=1.0,
        now=now,
    ))

    return events


# ---------------------------------------------------------------------------
# Entry builder
# ---------------------------------------------------------------------------

def _make_entry(
    source_path: str,
    heading: str,
    agent: str,
    text: str,
    knowledge_type: str,
    project: str,
    archetype: str,
    zone: str,
    authority: str,
    confidence: float,
    now: str,
) -> dict[str, Any]:
    """Build an index.json-compatible knowledge entry.

    Schema follows EMBEDDING_CLASSIFICATION_SPEC.md (base fields) +
    CALIBRATION_SPEC.md (calibration extension) +
    004_KNOWLEDGE_ENGINE_EVOLUTION.md (knowledge_type field).
    """
    return {
        # Base fields (existing index.json schema)
        "source_type": "runtime_state",
        "source_path": source_path,
        "heading": heading,
        "agent": agent,
        "date": now[:10],
        "text_preview": text[:200],
        "ingested_at": now,
        # Knowledge type extension (004_KNOWLEDGE_ENGINE_EVOLUTION)
        "knowledge_type": knowledge_type,
        "project": project,
        "archetype": archetype,
        # Calibration extension (CALIBRATION_SPEC)
        "calibration": {
            "zone": zone,
            "authority": authority,
            "confidence": confidence,
        },
        # Full text for embedding (not stored in index, used by embed())
        "_embed_text": text,
    }


# ---------------------------------------------------------------------------
# Summary for human consumption
# ---------------------------------------------------------------------------

def summarize_knowledge_events(events: list[dict[str, Any]]) -> str:
    """Produce a human-readable summary of extracted knowledge events."""
    by_type: dict[str, int] = {}
    for e in events:
        kt = e.get("knowledge_type", "unknown")
        by_type[kt] = by_type.get(kt, 0) + 1

    lines = [f"Knowledge events extracted: {len(events)}"]
    for kt, count in sorted(by_type.items()):
        lines.append(f"  {kt}: {count}")

    # Zone distribution
    zones: dict[str, int] = {}
    for e in events:
        z = e.get("calibration", {}).get("zone", "?")
        zones[z] = zones.get(z, 0) + 1
    lines.append(f"Zone distribution: {zones}")

    return "\n".join(lines)
