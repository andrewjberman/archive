"""
G8: Crystallization Engine — Structural diagnosis from runtime signals.

Detects crystallization pressure from G7 knowledge events and proposes
topology mutations per CRYSTALLIZATION_PROTOCOL.md and LEARNING_LOOP.md.

Tier 1 limitation: single-project signals only. Cross-project pattern
detection (Tier 2/3) requires R4 persistence and knowledge engine
aggregation. The Tier 1 engine produces automated proxy scores on the
6 crystallization dimensions from observable runtime signals.

Integration:
    from crystallization_engine import assess_crystallization
    assessment = assess_crystallization(knowledge_events, state)
    # assessment contains dimension scores, decision, and mutation proposals

Ontology source: CRYSTALLIZATION_PROTOCOL.md (6 dimensions, decision function)
                 LEARNING_LOOP.md (Tier 3 structural diagnosis)
                 FRACTAL_LAYERS.md (micro-layer crystallization)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Crystallization dimensions (from CRYSTALLIZATION_PROTOCOL.md)
# ---------------------------------------------------------------------------

DIMENSION_NAMES = [
    "volume",              # Capacity consumed by micro-layer
    "cognitive_distance",  # How different the reasoning mode is
    "blast_radius",        # Impact scope asymmetry on failure
    "cadence_mismatch",    # Timing/trigger differences
    "skill_specialization",# Would you hire a different person?
    "handoff_friction",    # Rework/errors at the boundary
]


@dataclass
class CrystallizationSignal:
    """A single structural pressure signal detected from runtime events."""
    boundary: str            # e.g. "coordinator_to_worker", "transformer_to_compositor"
    archetype: str           # The archetype under pressure
    dimension: str           # Which of the 6 dimensions
    score: int               # 1-5 proxy score
    evidence: str            # What runtime signal produced this score
    source_event_type: str   # G7 knowledge type that sourced this


@dataclass
class MicroLayerAssessment:
    """Assessment of a single micro-layer's crystallization pressure."""
    boundary: str
    archetype: str
    volume: int = 1
    cognitive_distance: int = 1
    blast_radius: int = 1
    cadence_mismatch: int = 1
    skill_specialization: int = 1
    handoff_friction: int = 1
    signals: list[CrystallizationSignal] = field(default_factory=list)

    @property
    def scores(self) -> list[int]:
        return [
            self.volume, self.cognitive_distance, self.blast_radius,
            self.cadence_mismatch, self.skill_specialization, self.handoff_friction,
        ]

    @property
    def sum_score(self) -> int:
        return sum(self.scores)

    @property
    def max_score(self) -> int:
        return max(self.scores)

    @property
    def count3(self) -> int:
        """Number of dimensions scoring >= 3."""
        return sum(1 for s in self.scores if s >= 3)

    @property
    def decision(self) -> str:
        """Apply crystallization function from CRYSTALLIZATION_PROTOCOL.md."""
        if self.max_score >= 5:
            return "CRYSTALLIZE"
        if self.sum_score >= 20:
            return "CRYSTALLIZE"
        if self.count3 >= 4:
            return "CRYSTALLIZE"
        if self.max_score >= 4:
            return "MONITOR"
        if self.sum_score >= 15:
            return "MONITOR"
        if self.count3 >= 2:
            return "MONITOR"
        return "ABSORB"


@dataclass
class TopologyMutation:
    """A proposed change to the graph topology."""
    mutation_type: str       # "add_node", "remove_node", "add_edge", "split_layer"
    target: str              # What to mutate (archetype, boundary, node)
    description: str         # Human-readable explanation
    trigger: str             # What crystallization decision triggered this
    authority_required: str  # "architect" (Tier 3 only)


@dataclass
class CrystallizationAssessment:
    """Complete crystallization assessment for a project run."""
    project_id: str
    assessments: list[MicroLayerAssessment] = field(default_factory=list)
    mutations: list[TopologyMutation] = field(default_factory=list)
    tier: int = 1  # Always 1 for single-project

    @property
    def has_structural_signals(self) -> bool:
        return any(a.decision != "ABSORB" for a in self.assessments)


# ---------------------------------------------------------------------------
# Signal extraction from G7 knowledge events
# ---------------------------------------------------------------------------

def _extract_signals(
    knowledge_events: list[dict[str, Any]],
    state: dict[str, Any],
) -> list[CrystallizationSignal]:
    """Extract crystallization pressure signals from knowledge events.

    Maps runtime signals to the 6 crystallization dimensions using
    automated proxy scoring. These are approximations -- the real
    informed assessment requires human input (CRYSTALLIZATION_PROTOCOL
    Part 2).
    """
    signals: list[CrystallizationSignal] = []

    # --- FAILURE events -> handoff_friction, blast_radius ---
    failures = [e for e in knowledge_events if e.get("knowledge_type") == "failure"]
    failure_by_archetype: dict[str, list] = {}
    for f in failures:
        arch = f.get("archetype", "unknown")
        failure_by_archetype.setdefault(arch, []).append(f)

    for arch, arch_failures in failure_by_archetype.items():
        count = len(arch_failures)

        # Boundary failures from G5 may have empty archetype in the
        # knowledge event. Infer from boundary name in the failure text.
        resolved_arch = arch
        if not arch:
            for f in arch_failures:
                text = f.get("_embed_text", "")
                for candidate in ("supplier", "transformer", "compositor", "operator"):
                    if candidate in text.lower():
                        resolved_arch = candidate
                        break
                if resolved_arch:
                    break

        # handoff_friction: failures at boundaries indicate interface problems
        # 1 failure = score 2, 2-3 = score 3, 4+ = score 4
        friction_score = min(5, 1 + count)
        signals.append(CrystallizationSignal(
            boundary=_infer_boundary(resolved_arch),
            archetype=resolved_arch,
            dimension="handoff_friction",
            score=friction_score,
            evidence=f"{count} failure event(s) for archetype '{resolved_arch or 'unknown'}'",
            source_event_type="failure",
        ))

        # blast_radius: archetype routing errors vs boundary failures
        routing_errors = [
            f for f in arch_failures
            if "routing_error" in f.get("heading", "")
        ]
        if routing_errors:
            signals.append(CrystallizationSignal(
                boundary=_infer_boundary(arch),
                archetype=arch,
                dimension="blast_radius",
                score=min(5, 2 + len(routing_errors)),
                evidence=f"{len(routing_errors)} archetype routing error(s) -- wrong archetype assigned",
                source_event_type="failure",
            ))

    # --- OUTCOME events -> volume, cognitive_distance ---
    outcomes = [e for e in knowledge_events if e.get("knowledge_type") == "outcome"]
    for o in outcomes:
        text = o.get("_embed_text", "")
        # scope_discipline failures indicate the worker went outside their lane
        # -> cognitive_distance signal (work requires different reasoning)
        if "scope_discipline" in text and ("=0" in text or "=1" in text):
            signals.append(CrystallizationSignal(
                boundary=_infer_boundary(o.get("archetype", "")),
                archetype=o.get("archetype", ""),
                dimension="cognitive_distance",
                score=3,
                evidence="Low scope_discipline score -- worker operated outside primary archetype function",
                source_event_type="outcome",
            ))

    # --- ESCALATION events -> skill_specialization ---
    escalations = [e for e in knowledge_events if e.get("knowledge_type") == "escalation"]
    if escalations:
        # Escalations that couldn't be resolved at the current tier
        # indicate the worker lacks the skill to handle the boundary
        unresolved = [e for e in escalations if "pending" in e.get("_embed_text", "").lower()]
        if unresolved:
            for esc in unresolved:
                signals.append(CrystallizationSignal(
                    boundary="escalation_boundary",
                    archetype=esc.get("archetype", ""),
                    dimension="skill_specialization",
                    score=3,
                    evidence="Unresolved escalation -- current tier lacks authority/skill",
                    source_event_type="escalation",
                ))

    # --- DECISION events -> volume (task order count per archetype) ---
    decisions = [e for e in knowledge_events if e.get("knowledge_type") == "decision"]
    archetype_task_count: dict[str, int] = {}
    for d in decisions:
        text = d.get("_embed_text", "")
        # Extract archetype from the decision text
        for arch in ("supplier", "transformer", "compositor", "operator"):
            if f"archetype '{arch}'" in text:
                archetype_task_count[arch] = archetype_task_count.get(arch, 0) + 1

    for arch, count in archetype_task_count.items():
        if count >= 2:
            # Task volume for a single archetype -> volume pressure
            # 2 = score 3, 3 = score 4, 4+ = score 5
            signals.append(CrystallizationSignal(
                boundary=_infer_boundary(arch),
                archetype=arch,
                dimension="volume",
                score=min(5, 1 + count),
                evidence=f"{count} task orders assigned to archetype '{arch}' in single run",
                source_event_type="decision",
            ))

    # --- DELIVERABLE events -> cognitive_distance (layer mismatch) ---
    # Detect when an archetype produces deliverables in a different
    # value chain layer than its primary position. A compositor modifying
    # pipeline/ files is a direct measurement of cognitive distance.
    # (CRYSTALLIZATION_PROTOCOL Part 2.4: archetype matches micro-layer function)
    deliverables = state.get("deliverables", [])
    for d in deliverables:
        archetype = getattr(d, "archetype", "") if hasattr(d, "archetype") else ""
        file_paths = getattr(d, "file_paths", []) if hasattr(d, "file_paths") else []

        layer_mismatch = False
        mismatch_detail = ""
        for fp in file_paths:
            fp_lower = fp.replace("\\", "/").lower()
            if archetype == "compositor" and ("pipeline/" in fp_lower or "transform" in fp_lower):
                layer_mismatch = True
                mismatch_detail = f"compositor modifying pipeline-layer file: {fp}"
            elif archetype == "transformer" and ("consumer/" in fp_lower or "renderer" in fp_lower or "assemble" in fp_lower):
                layer_mismatch = True
                mismatch_detail = f"transformer modifying compositor-layer file: {fp}"
            elif archetype == "operator" and ("pipeline/" in fp_lower or "consumer/" in fp_lower):
                layer_mismatch = True
                mismatch_detail = f"operator modifying upstream-layer file: {fp}"

        if layer_mismatch:
            signals.append(CrystallizationSignal(
                boundary=_infer_boundary(archetype),
                archetype=archetype,
                dimension="cognitive_distance",
                score=4,  # High: archetype working in wrong layer
                evidence=mismatch_detail,
                source_event_type="deliverable",
            ))

    # --- DATA_LINEAGE events -> cadence_mismatch ---
    lineage = [e for e in knowledge_events if e.get("knowledge_type") == "data_lineage"]
    for lin in lineage:
        text = lin.get("_embed_text", "")
        # If the audit trail shows interleaved archetype transitions
        # (supplier -> operator -> supplier -> transformer), that's
        # a cadence mismatch signal
        steps = text.split("\n")
        if len(steps) > 2:
            archetypes_seen = []
            for step in steps:
                if step.startswith("["):
                    arch = step.split("]")[0].lstrip("[")
                    archetypes_seen.append(arch)
            # Count archetype transitions (context switches)
            transitions = sum(
                1 for i in range(1, len(archetypes_seen))
                if archetypes_seen[i] != archetypes_seen[i-1]
            )
            if transitions > len(set(archetypes_seen)) * 2:
                signals.append(CrystallizationSignal(
                    boundary="execution_flow",
                    archetype="coordinator",
                    dimension="cadence_mismatch",
                    score=min(5, 2 + (transitions // 3)),
                    evidence=f"{transitions} archetype transitions in lineage -- high context switching",
                    source_event_type="data_lineage",
                ))

    return signals


def _infer_boundary(archetype: str) -> str:
    """Infer the PLK boundary from archetype."""
    boundary_map = {
        "supplier": "supplier_to_transformer",
        "transformer": "transformer_to_compositor",
        "compositor": "compositor_to_operator",
        "operator": "operator_output",
        "coordinator": "coordinator_to_worker",
        "architect": "architect_to_coordinator",
    }
    return boundary_map.get(archetype, f"{archetype}_boundary")


# ---------------------------------------------------------------------------
# Assessment builder
# ---------------------------------------------------------------------------

def _build_assessments(
    signals: list[CrystallizationSignal],
) -> list[MicroLayerAssessment]:
    """Aggregate signals into per-boundary micro-layer assessments."""
    # Group signals by (boundary, archetype)
    grouped: dict[tuple[str, str], list[CrystallizationSignal]] = {}
    for s in signals:
        key = (s.boundary, s.archetype)
        grouped.setdefault(key, []).append(s)

    assessments = []
    for (boundary, archetype), boundary_signals in grouped.items():
        assessment = MicroLayerAssessment(
            boundary=boundary,
            archetype=archetype,
            signals=boundary_signals,
        )

        # Apply highest signal score per dimension
        for s in boundary_signals:
            current = getattr(assessment, s.dimension, 1)
            if s.score > current:
                setattr(assessment, s.dimension, s.score)

        assessments.append(assessment)

    return assessments


# ---------------------------------------------------------------------------
# Mutation proposals
# ---------------------------------------------------------------------------

def _propose_mutations(
    assessments: list[MicroLayerAssessment],
) -> list[TopologyMutation]:
    """Generate topology mutation proposals from assessments."""
    mutations = []

    for a in assessments:
        if a.decision == "CRYSTALLIZE":
            mutations.append(TopologyMutation(
                mutation_type="split_layer",
                target=a.boundary,
                description=(
                    f"Micro-layer at {a.boundary} ({a.archetype}) has crystallized. "
                    f"Scores: V={a.volume} CD={a.cognitive_distance} BR={a.blast_radius} "
                    f"CM={a.cadence_mismatch} SS={a.skill_specialization} HF={a.handoff_friction}. "
                    f"Decision: {a.decision} (sum={a.sum_score}, max={a.max_score}, "
                    f"count3={a.count3}). "
                    f"Propose dedicated worker at this boundary."
                ),
                trigger=f"crystallization:{a.boundary}",
                authority_required="architect",
            ))
        elif a.decision == "MONITOR":
            mutations.append(TopologyMutation(
                mutation_type="monitor",
                target=a.boundary,
                description=(
                    f"Micro-layer at {a.boundary} ({a.archetype}) shows pressure. "
                    f"Scores: V={a.volume} CD={a.cognitive_distance} BR={a.blast_radius} "
                    f"CM={a.cadence_mismatch} SS={a.skill_specialization} HF={a.handoff_friction}. "
                    f"Decision: {a.decision} (sum={a.sum_score}, max={a.max_score}, "
                    f"count3={a.count3}). "
                    f"Formalize handoff interface; re-assess next cycle."
                ),
                trigger=f"pressure:{a.boundary}",
                authority_required="architect",
            ))

    return mutations


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def assess_crystallization(
    knowledge_events: list[dict[str, Any]],
    state: dict[str, Any],
    project_id: str = "",
) -> CrystallizationAssessment:
    """Run crystallization assessment on G7 knowledge events.

    Tier 1 implementation: single-project automated proxy scoring.
    Produces MicroLayerAssessments with the 6 crystallization dimensions
    and TopologyMutation proposals for any CRYSTALLIZE or MONITOR decisions.

    Args:
        knowledge_events: G7 knowledge events from extract_knowledge_events().
        state: Final ProjectState dict.
        project_id: Project identifier.

    Returns:
        CrystallizationAssessment with dimension scores and mutation proposals.
    """
    project_id = project_id or state.get("project_id", "unknown")

    # Step 1: Extract structural pressure signals from knowledge events
    signals = _extract_signals(knowledge_events, state)

    # Step 2: Aggregate into per-boundary assessments
    assessments = _build_assessments(signals)

    # Step 3: Generate mutation proposals for CRYSTALLIZE/MONITOR decisions
    mutations = _propose_mutations(assessments)

    return CrystallizationAssessment(
        project_id=project_id,
        assessments=assessments,
        mutations=mutations,
        tier=1,
    )


def summarize_crystallization(assessment: CrystallizationAssessment) -> str:
    """Produce a human-readable summary of crystallization assessment."""
    lines = [f"Crystallization assessment (Tier {assessment.tier}):"]
    lines.append(f"  Micro-layers assessed: {len(assessment.assessments)}")

    by_decision: dict[str, int] = {}
    for a in assessment.assessments:
        by_decision[a.decision] = by_decision.get(a.decision, 0) + 1

    for decision, count in sorted(by_decision.items()):
        lines.append(f"  {decision}: {count}")

    if assessment.mutations:
        lines.append(f"  Mutation proposals: {len(assessment.mutations)}")
        for m in assessment.mutations:
            lines.append(f"    [{m.mutation_type}] {m.target}: {m.description[:100]}...")

    if not assessment.has_structural_signals:
        lines.append("  No structural pressure detected -- topology stable")

    return "\n".join(lines)
