"""
G5: Boundary Contract Automation — Machine-checkable condition validators.

Implements the automatable conditions from BOUNDARY_CHECK_AUDIT.md.
Each validator is a pure function: artifact in, pass/fail out.

Three check types:
- field_present: required fields exist and are non-empty
- format_matches: artifact is valid structured data (JSON/XML/YAML)
- cross_reference_registries: referenced IDs exist in known registries

Condition maturity tiers (from EXP-001-PSCFIX postmortem analysis):
- tier 1 (runtime-guaranteed): fields the runtime always produces
  (artifact_id, identity, archetype, file_paths, status, produced_at)
- tier 2 (agent-declared): fields the worker prompt can reasonably supply
  (schema_version, component_count, source metadata)
- tier 3 (production): packaging/release metadata not yet in Tier 1
  (sha256, passage_authorization_id, validation_report, changelog)

The validator accepts a max_tier parameter. Conditions above max_tier
are recorded as skipped (not failed). This preserves the full ontological
contract shape while being honest about which checks are active at each
maturity level. We do not weaken contracts globally — we activate a
tier-appropriate subset intentionally.

Boundary violations produce escalations with:
    authority_type: validation
    sub_type: boundary_failure

Ontology source: contracts/boundaries/*.yaml (machine conditions)
                 contracts/BOUNDARY_CHECK_AUDIT.md (classification)
Runtime spec: runtime/specs/FLOW.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Validation result types
# ---------------------------------------------------------------------------

@dataclass
class ConditionResult:
    """Result of evaluating a single boundary condition."""
    condition_id: str          # e.g., "classified", "versioned"
    boundary: str              # e.g., "supplier_to_transformer"
    check_type: str            # field_present, format_matches, cross_reference
    passed: bool
    tier: int = 1              # Maturity tier: 1=runtime, 2=agent, 3=production
    skipped: bool = False      # True if condition was above active max_tier
    detail: str = ""           # Human-readable explanation
    fields_checked: list[str] = field(default_factory=list)
    fields_missing: list[str] = field(default_factory=list)


@dataclass
class BoundaryResult:
    """Aggregate result for all conditions on a single boundary crossing."""
    boundary: str
    producing_archetype: str
    consuming_archetype: str
    max_tier: int = 1          # Active tier ceiling for this validation run
    conditions: list[ConditionResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Pass/fail considers only active conditions (not skipped)."""
        active = [c for c in self.conditions if not c.skipped]
        return all(c.passed for c in active) if active else True

    @property
    def failures(self) -> list[ConditionResult]:
        """Only active (non-skipped) failures."""
        return [c for c in self.conditions if not c.passed and not c.skipped]

    @property
    def skipped_conditions(self) -> list[ConditionResult]:
        """Conditions above active tier — recorded but not enforced."""
        return [c for c in self.conditions if c.skipped]


# ---------------------------------------------------------------------------
# Boundary contract definitions (from YAML contracts, machine conditions only)
# ---------------------------------------------------------------------------

# Each boundary maps to a list of machine-checkable conditions.
# Agent-type conditions (semantic_coherence, etc.) are NOT here —
# those are evaluated by the reviewer LLM.

# Condition maturity tiers:
#   1 = runtime-guaranteed (fields the runtime always produces)
#   2 = agent-declared (fields a worker prompt can reasonably supply)
#   3 = production (packaging/release metadata, Tier 2+ runtime)
TIER_RUNTIME = 1
TIER_AGENT = 2
TIER_PRODUCTION = 3

BOUNDARY_CONDITIONS: dict[str, list[dict[str, Any]]] = {
    "supplier_to_transformer": [
        {
            "id": "normalized_format",
            "check_type": "format_matches",
            "format": "json_or_xml",
            "description": "Supplier output is valid JSON or XML",
            "tier": TIER_RUNTIME,
        },
        {
            "id": "classified",
            "check_type": "field_present",
            "fields": ["source_type", "domain"],
            "description": "Intake record has classification metadata",
            "tier": TIER_AGENT,
        },
        {
            "id": "classified_full",
            "check_type": "field_present",
            "fields": ["source_type", "domain", "intake_date", "archetype_tag"],
            "description": "Intake record has full classification metadata",
            "tier": TIER_PRODUCTION,
        },
        {
            "id": "sourced",
            "check_type": "field_present",
            "fields": ["source_id", "source_name"],
            "description": "Intake record has provenance fields",
            "tier": TIER_AGENT,
        },
        {
            "id": "sourced_full",
            "check_type": "field_present",
            "fields": ["source_id", "source_name", "intake_method"],
            "description": "Intake record has full provenance fields",
            "tier": TIER_PRODUCTION,
        },
    ],
    "transformer_to_compositor": [
        {
            "id": "has_content",
            "check_type": "field_present",
            "fields": ["artifact_id", "archetype", "file_paths"],
            "description": "Transformer output has identity and deliverable paths",
            "tier": TIER_RUNTIME,
        },
        {
            "id": "versioned_basic",
            "check_type": "field_present",
            "fields": ["artifact_id", "produced_at"],
            "description": "Transformer output has basic version tracking",
            "tier": TIER_RUNTIME,
        },
        {
            "id": "structured",
            "check_type": "format_matches",
            "format": "json_or_xml",
            "description": "Transformer output is valid structured data with schema_version",
            "required_fields": ["schema_version"],
            "tier": TIER_AGENT,
        },
        {
            "id": "versioned_full",
            "check_type": "field_present",
            "fields": ["schema_version", "artifact_id", "produced_at"],
            "description": "Transformer output has full version tracking fields",
            "tier": TIER_AGENT,
        },
    ],
    "compositor_to_operator": [
        {
            "id": "identified",
            "check_type": "field_present",
            "fields": ["artifact_id", "produced_at"],
            "description": "Assembly has identity and timestamp",
            "tier": TIER_RUNTIME,
        },
        {
            "id": "versioned",
            "check_type": "field_present",
            "fields": ["assembly_version", "artifact_id", "produced_at", "component_count"],
            "description": "Assembly has version and component tracking",
            "tier": TIER_AGENT,
        },
        {
            "id": "testable",
            "check_type": "field_present",
            "fields": ["validation_hooks"],
            "description": "Assembly includes validation hook references",
            "tier": TIER_PRODUCTION,
        },
    ],
    "operator_to_external": [
        {
            "id": "identified",
            "check_type": "field_present",
            "fields": ["artifact_id", "produced_at", "status"],
            "description": "Release has identity, timestamp, and status",
            "tier": TIER_RUNTIME,
        },
        {
            "id": "has_deliverables",
            "check_type": "field_present",
            "fields": ["file_paths"],
            "description": "Release references deliverable files",
            "tier": TIER_RUNTIME,
        },
        {
            "id": "documented",
            "check_type": "field_present",
            "fields": ["release_version", "release_notes", "changelog", "produced_at"],
            "description": "Release has documentation fields",
            "tier": TIER_AGENT,
        },
        {
            "id": "validated",
            "check_type": "field_present",
            "fields": ["validation_report"],
            "description": "Release has validation report attached",
            "tier": TIER_PRODUCTION,
        },
        {
            "id": "hashed",
            "check_type": "field_present",
            "fields": ["sha256", "size_bytes"],
            "description": "Release has integrity hash and size",
            "tier": TIER_PRODUCTION,
        },
        {
            "id": "authorized",
            "check_type": "field_present",
            "fields": ["passage_authorization_id", "authorized_by", "authorized_at"],
            "description": "Release has passage authorization",
            "tier": TIER_PRODUCTION,
        },
    ],
    "external_to_supplier": [
        {
            "id": "attributable",
            "check_type": "field_present",
            "fields": ["source_id", "source_name"],
            "description": "External input has attribution metadata",
            "tier": TIER_AGENT,
        },
        {
            "id": "attributable_full",
            "check_type": "field_present",
            "fields": ["source_id", "source_name", "received_at"],
            "description": "External input has full attribution metadata",
            "tier": TIER_PRODUCTION,
        },
        {
            "id": "normalized_format",
            "check_type": "format_matches",
            "format": "json_or_xml",
            "description": "Supplier normalizes input to valid JSON or XML",
            "tier": TIER_RUNTIME,
        },
    ],
    "coordinator_to_worker": [
        {
            "id": "task_completeness",
            "check_type": "field_present",
            "fields": ["objective", "requirements", "acceptance_criteria", "deliverables"],
            "description": "Task order has all required planning fields",
            "tier": TIER_RUNTIME,
        },
        {
            "id": "archetype_specified",
            "check_type": "field_present",
            "fields": ["archetype"],
            "description": "Task order specifies target archetype",
            "tier": TIER_RUNTIME,
        },
    ],
    "architect_to_coordinator": [
        {
            "id": "resource_grounding",
            "check_type": "cross_reference",
            "registry": "agents",
            "ref_field": "identity",
            "description": "Referenced identities exist in AGENTS.json",
            "tier": TIER_RUNTIME,
        },
    ],
}

# Map producing -> consuming archetype to boundary name
ARCHETYPE_BOUNDARY_MAP = {
    ("supplier", "transformer"): "supplier_to_transformer",
    ("transformer", "compositor"): "transformer_to_compositor",
    ("compositor", "operator"): "compositor_to_operator",
    ("operator", "external"): "operator_to_external",
    ("external", "supplier"): "external_to_supplier",
    ("coordinator", "supplier"): "coordinator_to_worker",
    ("coordinator", "transformer"): "coordinator_to_worker",
    ("coordinator", "compositor"): "coordinator_to_worker",
    ("coordinator", "operator"): "coordinator_to_worker",
}


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------

def check_field_present(
    artifact: dict[str, Any],
    fields: list[str],
) -> tuple[bool, list[str]]:
    """Check that all required fields exist and are non-empty.

    Returns (passed, missing_fields).
    """
    missing = []
    for f in fields:
        val = artifact.get(f)
        if val is None or val == "" or val == []:
            missing.append(f)
    return (len(missing) == 0, missing)


def check_format_matches(
    artifact: dict[str, Any],
    format_spec: str,
    required_fields: list[str] | None = None,
) -> tuple[bool, str]:
    """Check that artifact content is valid structured data.

    For Tier 1, this checks that the artifact is a non-empty dict
    (already parsed). Tier 2 will add schema validation against
    JSON Schema / XML Schema definitions.

    Returns (passed, detail).
    """
    if not isinstance(artifact, dict):
        return (False, f"Expected dict, got {type(artifact).__name__}")
    if not artifact:
        return (False, "Artifact is empty")

    if required_fields:
        missing = [f for f in required_fields if f not in artifact]
        if missing:
            return (False, f"Missing required structural fields: {missing}")

    return (True, "Valid structured artifact")


def check_cross_reference(
    artifact: dict[str, Any],
    registry: str,
    ref_field: str,
) -> tuple[bool, str]:
    """Check that a referenced ID exists in a known registry.

    For Tier 1, this checks AGENTS.json. Tier 2 will add
    ARTIFACTS.json and other registries.

    Returns (passed, detail).
    """
    ref_value = artifact.get(ref_field)
    if not ref_value:
        return (True, f"No {ref_field} to validate")  # Absent ref is not a violation

    if registry == "agents":
        from .config import load_agent_registry
        reg = load_agent_registry()
        if ref_value in reg or ref_value == "NEW":
            return (True, f"Agent {ref_value} exists in registry")
        return (False, f"Agent {ref_value} not found in AGENTS.json")

    return (True, f"Registry '{registry}' not yet implemented")


# ---------------------------------------------------------------------------
# Main validation entry point
# ---------------------------------------------------------------------------

def validate_boundary(
    artifact: dict[str, Any],
    boundary: str,
    max_tier: int = TIER_RUNTIME,
) -> BoundaryResult:
    """Run machine-checkable conditions for a boundary crossing.

    Conditions are tiered by maturity level. Conditions at or below
    max_tier are enforced (pass/fail). Conditions above max_tier are
    recorded as skipped — visible in telemetry but not gating.

    Args:
        artifact: The artifact dict being validated.
        boundary: Boundary name (e.g., "supplier_to_transformer").
        max_tier: Highest tier to enforce. 1=runtime, 2=agent, 3=production.

    Returns:
        BoundaryResult with per-condition pass/fail/skip.
    """
    conditions = BOUNDARY_CONDITIONS.get(boundary, [])
    parts = boundary.split("_to_")
    producing = parts[0] if len(parts) == 2 else "unknown"
    consuming = parts[1] if len(parts) == 2 else "unknown"

    result = BoundaryResult(
        boundary=boundary,
        producing_archetype=producing,
        consuming_archetype=consuming,
        max_tier=max_tier,
    )

    for cond in conditions:
        cond_id = cond["id"]
        check_type = cond["check_type"]
        cond_tier = cond.get("tier", TIER_RUNTIME)

        # Conditions above active tier are recorded but not enforced
        if cond_tier > max_tier:
            result.conditions.append(ConditionResult(
                condition_id=cond_id,
                boundary=boundary,
                check_type=check_type,
                passed=False,
                tier=cond_tier,
                skipped=True,
                detail=f"Skipped: tier {cond_tier} > active tier {max_tier}",
                fields_checked=cond.get("fields", []),
            ))
            continue

        if check_type == "field_present":
            passed, missing = check_field_present(artifact, cond["fields"])
            result.conditions.append(ConditionResult(
                condition_id=cond_id,
                boundary=boundary,
                check_type=check_type,
                passed=passed,
                tier=cond_tier,
                detail=cond["description"] if passed else f"Missing: {missing}",
                fields_checked=cond["fields"],
                fields_missing=missing,
            ))

        elif check_type == "format_matches":
            required = cond.get("required_fields", [])
            passed, detail = check_format_matches(artifact, cond["format"], required)
            result.conditions.append(ConditionResult(
                condition_id=cond_id,
                boundary=boundary,
                check_type=check_type,
                passed=passed,
                tier=cond_tier,
                detail=detail,
            ))

        elif check_type == "cross_reference":
            passed, detail = check_cross_reference(
                artifact, cond["registry"], cond["ref_field"]
            )
            result.conditions.append(ConditionResult(
                condition_id=cond_id,
                boundary=boundary,
                check_type=check_type,
                passed=passed,
                tier=cond_tier,
                detail=detail,
            ))

    return result


def validate_deliverable_boundary(
    deliverable_metadata: dict[str, Any],
    producing_archetype: str,
    consuming_archetype: str = "",
    max_tier: int = TIER_RUNTIME,
) -> BoundaryResult | None:
    """Validate a deliverable against the appropriate PLK boundary.

    Determines which boundary contract applies based on producing
    and consuming archetypes, then runs conditions up to max_tier.

    If no consuming archetype is specified, infers from the OTR
    flow direction (supplier->transformer->compositor->operator).

    Returns BoundaryResult or None if no boundary contract applies.
    """
    # Infer consuming archetype from flow direction if not specified
    if not consuming_archetype:
        flow_map = {
            "supplier": "transformer",
            "transformer": "compositor",
            "compositor": "operator",
            "operator": "external",
        }
        consuming_archetype = flow_map.get(producing_archetype, "")

    boundary = ARCHETYPE_BOUNDARY_MAP.get(
        (producing_archetype, consuming_archetype)
    )
    if not boundary:
        return None

    return validate_boundary(deliverable_metadata, boundary, max_tier=max_tier)


def validate_task_order_boundary(
    task_order_dict: dict[str, Any],
    max_tier: int = TIER_RUNTIME,
) -> BoundaryResult:
    """Validate a task order against the coordinator_to_worker contract.

    Runs the task_completeness and archetype_specified conditions.
    G1 (activation_scope) and G3 (deliverable_uniqueness) are handled
    separately in route_to_workers — this covers the structural checks.
    """
    return validate_boundary(task_order_dict, "coordinator_to_worker", max_tier=max_tier)
