"""
R2: State — Value chain state schema for LangGraph.

This is the typed state that flows through the graph. Every node reads
from and writes partial updates to this shared state. Reducers control
merge semantics (append vs overwrite).

Ontology source: specs/core/VALUE_CHAIN.md
Runtime spec: runtime/specs/STATE.md
"""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from typing import Any, Literal

from typing_extensions import Annotated, TypedDict


# ---------------------------------------------------------------------------
# Artifact types per value chain layer
# ---------------------------------------------------------------------------

@dataclass
class ClassificationScheme:
    """Valid classification codes for an ingestion/cataloging project."""
    lifecycle_roles: list[str] = field(default_factory=list)      # e.g., ["SRC", "LOG", "CTL", "ASM", "DLV"]
    behavior_classes: list[str] = field(default_factory=list)      # e.g., ["DOC", "DEC", "MAP", "EXE", "PKG"]
    governance_intents: list[str] = field(default_factory=list)    # e.g., ["MOD", "POL", "REC", "INS", "REL"]
    object_class_pattern: str = ""                                  # e.g., "2-4 char abbreviation of object name"


@dataclass
class DesignSpec:
    """Structured architect output — typed contract between architect and coordinator.

    Replaces freeform text design_spec. Every field is validated deterministically
    before the coordinator consumes it. This eliminates the lossy compression of
    freeform text handoffs (architect writes prose → coordinator interprets prose).

    Ontology source: ONT.CORE.EXECUTION_COMPLEXITY Section 3 (Fix 2)
    """
    # --- Scope ---
    object_count: int = 0                                           # Expected number of objects to process
    object_categories: dict[str, int] = field(default_factory=dict) # {"core_specs": 18, "contracts": 14, ...}
    domain_root: str = ""                                           # Absolute path to domain being processed

    # --- Classification (for ingestion/cataloging projects) ---
    classification_scheme: ClassificationScheme | None = None       # Valid taxonomy codes
    key_spine: str = ""                                             # e.g., "CORP-MAIN-CREATE-0001"
    key_format: str = ""                                            # e.g., "ORG-MAC-PRJ-VER-BTS-KT-OTS-OTR-OTB-OTG-OC-OV"

    # --- Value chain ---
    value_chain_stages: list[str] = field(default_factory=list)     # e.g., ["supplier", "transformer", "compositor", "operator"]
    stage_descriptions: dict[str, str] = field(default_factory=dict) # {"supplier": "scan directory, produce inventory", ...}

    # --- Grading ---
    grading_rubric: dict[str, Any] = field(default_factory=dict)    # {"axis_a": {"weight": 60, ...}, ...}
    acceptance_criteria: list[str] = field(default_factory=list)     # Concrete, testable criteria

    # --- Context refs (files the coordinator and workers should read) ---
    taxonomy_files: list[str] = field(default_factory=list)          # Actual paths to taxonomy/classification specs
    reference_files: list[str] = field(default_factory=list)         # Other relevant files for context

    # --- Complexity classification (EXECUTION_COMPLEXITY) ---
    complexity_tier: str = "M"                                       # "S", "T", or "M"
    tier_rationale: str = ""                                         # Why this tier was selected

    # --- Raw narrative (preserved for human review) ---
    narrative: str = ""                                               # Freeform prose for human consumption


@dataclass
class TaskOrder:
    """Coordinator -> Worker assignment."""
    id: str
    identity: str
    archetype: str                    # Target archetype: supplier, transformer, compositor, operator
    objective: str
    requirements: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)  # Upstream deliverable IDs this task consumes
    context_refs: list[str] = field(default_factory=list)  # Files that exist NOW on disk (not upstream outputs)
    deliverable_schema: dict[str, Any] = field(default_factory=dict)  # JSON schema constraining worker output format
    split_justification: str = ""     # Why this task exists as a separate unit (not merged with adjacent)
    kf_budget: dict[str, int] = field(default_factory=dict)  # Legacy: explicit per-stage budgets (v1/v2). Ignored when read_ratio is set.
    read_ratio: float = 0.6  # KF gate v3 Layer 2: fraction of total_iterations for Pe+In read phase
    status: Literal[
        "pending", "in_progress", "complete", "blocked"
    ] = "pending"


@dataclass
class Deliverable:
    """Worker output artifact."""
    id: str
    task_order_id: str
    identity: str
    archetype: str
    content: str
    file_paths: list[str] = field(default_factory=list)
    status: Literal["draft", "submitted", "accepted", "rejected"] = "draft"


@dataclass
class Discovery:
    """Worker upstream output — incidental knowledge learned during execution.

    Discovery is NOT adaptation. Adaptation modifies the agent's own state
    for future cycles (self-directed). Discovery is emitted to the Coordinator
    for propagation to other agents (system-directed).

    Ontology source: ONT.CORE.ARTIFACT v2, Section 1 (The two output streams)
    Learning loop: LEARNING_LOOP v3, Tier 2 (Discovery Propagation)

    Discovery flows upstream (U) as PLK events to upstream.jsonl.
    The Coordinator reads the accumulator, matches discoveries against
    pending workers' task orders by joining on resource references,
    and injects relevant discoveries into worker context. Zone A.
    """
    agent_serial: str
    task_order_id: str
    kf_stage: Literal["Pe", "In", "Ev", "De", "Ac", "Ad"]
    scope: Literal["within_level", "within_project", "cross_project"]
    category: Literal[
        "resource_resolution",       # Pe: resource at different path than expected
        "resource_absence",          # Pe: referenced resource does not exist
        "structure_correction",      # In: input has different structure than expected
        "classification_decision",   # Ev: ambiguous classification resolved
        "environment_observation",   # Ac: execution environment differs from spec
        "process_correction",        # Ad: task order step unnecessary or missing
    ]
    content: dict[str, Any] = field(default_factory=dict)
    timestamp: str = ""


@dataclass
class ActivationRecord:
    """Records an agent activation event with traceability."""
    identity: str
    serial: str
    archetype: str
    activated_by: str               # Coordinator identity or "PRINCIPAL"
    justification_ref: str          # Design artifact ID / section that names this position
    scope_check: Literal[
        "within_scope", "cross_scope"
    ]
    timestamp: str = ""


@dataclass
class AuditEntry:
    """Append-only record of who did what."""
    identity: str
    archetype: str
    action: str
    detail: str = ""
    justification_ref: str = ""     # Design artifact / task order that justifies this action
    timestamp: str = ""             # ISO 8601, filled at write time


@dataclass
class Evaluation:
    """G6: Structured quality evaluation for the learning loop.

    Each deliverable receives a 4-dimension evaluation that feeds
    the learning loop's tier classification system.

    Dimensions score 0-3:
        0 = not addressed
        1 = attempted but deficient
        2 = adequate
        3 = exceeds expectations

    Learning loop tier (auto-classified):
        1 = instance repair (single deliverable fix)
        2 = pattern detection (repeated failures by archetype)
        3 = structural diagnosis (contract/topology change needed)
    """
    deliverable_id: str
    task_order_id: str
    identity: str
    archetype: str
    # 4 evaluation dimensions (0-3)
    completeness: int = 0       # Does it address all acceptance criteria?
    correctness: int = 0        # Is the artifact functionally correct?
    adherence: int = 0          # Does it follow the task order's requirements?
    scope_discipline: int = 0   # Did the worker stay within deliverable scope?
    # Verdict (backward compat with reviewer flow)
    verdict: Literal["PASS", "FAIL", "MISSING"] = "MISSING"
    reason: str = ""
    # Learning loop classification
    learning_tier: int = 1      # 1, 2, or 3
    tier_signal: str = ""       # What triggered the tier classification
    timestamp: str = ""


@dataclass
class LevelOutcome:
    """Convergence record for a dispatch level.

    Produced by level_collector after all workers in a level complete.
    Enables future convergence policies (quorum, timeout) and gives
    the reviewer visibility into level-by-level progression.
    """
    level: int
    completed: list[str] = field(default_factory=list)    # task order IDs that succeeded
    failed: list[str] = field(default_factory=list)       # task order IDs that failed
    artifacts_produced: list[str] = field(default_factory=list)  # deliverable IDs now available
    timestamp: str = ""


@dataclass
class ConditionCheck:
    """Single boundary condition check result."""
    condition_id: str              # e.g., "versioned", "structured", "hashed"
    check_type: str                # field_present, format_matches, cross_reference
    passed: bool
    tier: int = 1                  # 1=runtime, 2=agent, 3=production
    skipped: bool = False          # True if above active max_tier
    detail: str = ""               # Human-readable explanation
    expected: str = ""             # What the contract requires
    observed: str = ""             # What was actually found


@dataclass
class ValidationResult:
    """First-class artifact: per-deliverable boundary validation outcome.

    Produced by deliverable_validator_node. Survives in state for:
    - Reviewer: scope_discipline scoring adjustment
    - Knowledge engine: learning loop telemetry (which boundaries fail most)
    - Rework loops (Tier 2): which conditions to re-check after fix
    - Debugging: full trace of what was checked, what passed, what failed

    This is the machine-readable receipt for ONT.CORE.ARTIFACT rule 14:
    "deliver.sh validates before handoff."
    """
    deliverable_id: str
    task_order_id: str
    identity: str
    archetype: str                 # Producing archetype
    boundary: str                  # Which PLK boundary was checked
    passed: bool                   # Overall pass/fail
    conditions: list[ConditionCheck] = field(default_factory=list)
    failure_count: int = 0
    timestamp: str = ""


@dataclass
class ValidationOverride:
    """Records a Principal override of boundary validation failure.

    Overrides are exceptions, not normal flow. They must be expensive
    and visible — every override carries a structured record of what
    failed, who approved it, why, and what downstream risk it creates.
    This prevents the system from silently routing around its own rules.

    Consumed by:
    - Audit trail: permanent record of exception
    - Learning loop: override frequency signals contract miscalibration
    - Reviewer: downstream_risk_flag adjusts scope_discipline scoring
    - Knowledge engine: override patterns feed Tier 2/3 analysis
    """
    override_id: str                   # Unique ID: {project_id}-OVR-{seq}
    approver: str                      # Who approved: "PRINCIPAL" or identity
    deliverable_id: str                # Which deliverable was overridden
    task_order_id: str                 # Which task order it belongs to
    boundary: str                      # Which PLK boundary failed
    failed_conditions: list[str]       # condition_ids that failed
    failure_details: list[str]         # Human-readable failure descriptions
    rationale: str                     # Why the override was granted
    downstream_risk_flag: str          # "low", "medium", "high"
    timestamp: str = ""


@dataclass
class Escalation:
    """Interrupt payload — surfaces to human or governing agent."""
    identity: str
    authority_type: Literal[
        "archetype_constraint",  # Tier 0: system-enforced, sub-boundary (G2)
        "validation",            # Tier 1: boundary, operator-held
        "passage",               # Tier 2: boundary, coordinator-held
        "design",                # Tier 3: layer, architect-held
        "execution",             # Tier 2: layer, coordinator-held (veto)
    ]
    reason: str
    context: dict[str, Any] = field(default_factory=dict)
    resolved: bool = False
    resolution: str = ""


# ---------------------------------------------------------------------------
# Graph state schema
# ---------------------------------------------------------------------------

class ProjectState(TypedDict):
    """Top-level state for a project execution graph.

    Every field with Annotated[list, operator.add] uses append semantics:
    node returns {"field": [item]} and it extends, never overwrites.

    Fields without a reducer use last-write-wins (overwrite).
    """

    # --- Input (set once at graph entry) ---
    project_brief: str                # What the human wants built
    project_id: str                   # Unique run identifier
    working_directory: str            # Filesystem root for the project
    macro: str                        # 4-char macro code (e.g., MAIN, DSSR) — scopes agent resolution

    # --- Architect output (L1 design) ---
    design_spec: str                  # Freeform PRD (preserved for backward compat + human review)
    design_spec_structured: dict[str, Any]  # DesignSpec as dict (typed contract for coordinator)
    design_approved: bool             # Deterministic validation gate

    # --- Coordinator output (task decomposition) ---
    task_orders: Annotated[list[TaskOrder], operator.add]

    # --- Worker outputs (per-layer artifacts) ---
    deliverables: Annotated[list[Deliverable], operator.add]
    discoveries: Annotated[list[Discovery], operator.add]  # Upstream (U) knowledge — ONT.CORE.ARTIFACT v2

    # --- Cross-cutting ---
    activations: Annotated[list[ActivationRecord], operator.add]
    evaluations: Annotated[list[Evaluation], operator.add]  # G6: structured quality signals
    audit_trail: Annotated[list[AuditEntry], operator.add]
    escalations: Annotated[list[Escalation], operator.add]
    messages: Annotated[list[dict[str, Any]], operator.add]  # LLM message log

    # --- Boundary validation (deliverable_validator output) ---
    validation_results: Annotated[list[ValidationResult], operator.add]
    validation_overrides: Annotated[list[ValidationOverride], operator.add]

    # --- Interrupt resolution telemetry ---
    interrupt_resolutions: Annotated[list, operator.add]

    # --- Dispatch (dependency-aware staged execution) ---
    dispatch_plan: list[list[str]]  # [[task_order_ids level 0], [level 1], ...]
    current_dispatch_level: int     # which level we're executing
    level_outcomes: Annotated[list[LevelOutcome], operator.add]  # convergence records

    # --- Alignment (ONT.CORE.ALIGNMENT v1) ---
    alignment_assessment: dict[str, Any]  # AlignmentAssessment as dict, if alignment was run. Empty dict if skipped.

    # --- Flow control ---
    current_phase: Literal[
        "design", "planning", "execution", "review", "complete"
    ]
    error: str  # Non-empty if graph-level failure
