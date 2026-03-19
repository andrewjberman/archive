"""
Deliverable Validator — Machine-enforced boundary contract gate.

Runs AFTER all workers in the final dispatch level complete and BEFORE
the reviewer. Validates deliverables against PLK boundary contracts
(ONT.CORE.ARTIFACT rule 14: deliver.sh validates before handoff).

This node separates two concerns:
  - Validation (contract compliance): machine-checkable, gates progression
  - Evaluation (quality review): LLM-judged, informational for learning loop

If any deliverable fails boundary validation, the node interrupts for
rework routing. The reviewer never sees invalid artifacts.

Ontology source: contracts/boundaries/*.yaml (machine conditions)
                 specs/core/ARTIFACT_AND_CONTRACT_SPEC.md (rule 14)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..state import (
    AuditEntry, ConditionCheck, Escalation, ProjectState,
    ValidationOverride, ValidationResult,
)


def deliverable_validator_node(state: ProjectState) -> dict[str, Any]:
    """Validate all deliverables against PLK boundary contracts.

    Two outcomes:
      PASS: All deliverables meet boundary conditions -> proceed to reviewer.
      FAIL: One or more deliverables fail -> interrupt for rework decision.

    The interrupt gives the Principal (Tier 1) or Coordinator (Tier 2)
    three options:
      - rework: return failed task orders to workers (Tier 2)
      - accept: override and proceed to reviewer despite failures
      - reject: end the project with validation failure
    """
    from ..boundary_validator import validate_deliverable_boundary

    deliverables = state.get("deliverables", [])
    now = datetime.now(timezone.utc).isoformat()

    if not deliverables:
        return {
            "current_phase": "review",
            "audit_trail": [AuditEntry(
                identity="SYSTEM", archetype="deliverable_validator",
                action="no_deliverables",
                detail="No deliverables to validate. Proceeding to reviewer.",
                timestamp=now,
            )],
        }

    # --- Run boundary checks on every deliverable ---
    # Build first-class ValidationResult objects for full telemetry
    validation_results: list[ValidationResult] = []
    all_failures: list[dict[str, Any]] = []
    pass_count = 0
    fail_count = 0
    audit_entries: list[AuditEntry] = []
    boundary_fail_counts: dict[str, int] = {}

    for d in deliverables:
        metadata = {
            "artifact_id": d.id,
            "produced_at": now,
            "identity": d.identity,
            "archetype": d.archetype,
            "file_paths": d.file_paths,
            "status": d.status,
        }
        result = validate_deliverable_boundary(metadata, d.archetype, max_tier=1)

        if result:
            # Build structured condition checks for telemetry
            condition_checks = [
                ConditionCheck(
                    condition_id=c.condition_id,
                    check_type=c.check_type,
                    passed=c.passed,
                    tier=c.tier,
                    skipped=c.skipped,
                    detail=c.detail,
                    expected=", ".join(c.fields_checked) if c.fields_checked else c.condition_id,
                    observed=(
                        f"skipped (tier {c.tier})" if c.skipped
                        else ", ".join(c.fields_missing) + " missing" if c.fields_missing
                        else ("present" if c.passed else "failed")
                    ),
                )
                for c in result.conditions
            ]

            vr = ValidationResult(
                deliverable_id=d.id,
                task_order_id=d.task_order_id,
                identity=d.identity,
                archetype=d.archetype,
                boundary=result.boundary,
                passed=result.passed,
                conditions=condition_checks,
                failure_count=len(result.failures),
                timestamp=now,
            )
            validation_results.append(vr)

            if not result.passed:
                fail_count += 1
                boundary_fail_counts[d.id] = len(result.failures)
                failure_detail = {
                    "deliverable_id": d.id,
                    "task_order_id": d.task_order_id,
                    "identity": d.identity,
                    "archetype": d.archetype,
                    "boundary": result.boundary,
                    "failures": [
                        {
                            "condition_id": f.condition_id,
                            "check_type": f.check_type,
                            "detail": f.detail,
                        }
                        for f in result.failures
                    ],
                }
                all_failures.append(failure_detail)
                audit_entries.append(AuditEntry(
                    identity=d.identity,
                    archetype=d.archetype,
                    action="boundary_validation_failure",
                    detail=(
                        f"Deliverable {d.id} failed {len(result.failures)} "
                        f"boundary condition(s) at {result.boundary}"
                    ),
                    timestamp=now,
                ))
            else:
                pass_count += 1
        else:
            # No boundary contract applies (e.g., coordinator archetype)
            pass_count += 1

    # Summary audit entry
    audit_entries.append(AuditEntry(
        identity="SYSTEM", archetype="deliverable_validator",
        action="boundary_validation_complete",
        detail=(
            f"{pass_count} passed, {fail_count} failed "
            f"out of {len(deliverables)} deliverables. "
            f"{len(validation_results)} validation results produced."
        ),
        timestamp=now,
    ))

    # --- Gate decision ---
    if not all_failures:
        # All deliverables pass boundary checks -> proceed to reviewer
        return {
            "current_phase": "review",
            "validation_results": validation_results,
            "audit_trail": audit_entries,
            "_boundary_fail_counts": boundary_fail_counts,
        }

    # --- Failures exist: interrupt for rework decision ---
    from langgraph.types import interrupt

    project_id = state.get("project_id", "unknown")

    decision = interrupt({
        "authority_type": "validation",
        "sub_type": "boundary_failure",
        "tier": 1,
        "holder": "operator",
        "message": (
            f"{fail_count} deliverable(s) failed boundary validation. "
            f"Rework, accept (requires rationale), or reject."
        ),
        "resolution_options": ["accept", "rework", "reject"],
        "resolution_schema": {
            "accept": {
                "rationale": "string (required) — why this override is justified",
                "risk": "low | medium | high — downstream risk assessment",
            },
        },
        "context": {
            "failures": all_failures,
            "pass_count": pass_count,
            "fail_count": fail_count,
        },
    })

    resolution = decision if isinstance(decision, dict) else {"action": str(decision)}
    action = resolution.get("action", resolution.get("accepted", ""))

    # Handle "accept" (override) — proceed to reviewer despite failures.
    # Overrides are exceptions, not normal flow. Every override produces a
    # structured ValidationOverride record that makes the exception expensive
    # and visible. This prevents the system from silently routing around rules.
    if action in ("accept", True, "true") or resolution.get("accepted"):
        override_ts = datetime.now(timezone.utc).isoformat()
        rationale = resolution.get("rationale", "No rationale provided")
        risk = resolution.get("risk", "medium")

        overrides = []
        for i, f in enumerate(all_failures):
            ovr = ValidationOverride(
                override_id=f"{project_id}-OVR-{i + 1:03d}",
                approver="PRINCIPAL",
                deliverable_id=f["deliverable_id"],
                task_order_id=f["task_order_id"],
                boundary=f["boundary"],
                failed_conditions=[c["condition_id"] for c in f["failures"]],
                failure_details=[c["detail"] for c in f["failures"]],
                rationale=rationale,
                downstream_risk_flag=risk,
                timestamp=override_ts,
            )
            overrides.append(ovr)

        audit_entries.append(AuditEntry(
            identity="PRINCIPAL", archetype="deliverable_validator",
            action="boundary_override",
            detail=(
                f"Principal overrode {len(overrides)} boundary failure(s). "
                f"Risk: {risk}. Rationale: {rationale[:100]}"
            ),
            timestamp=override_ts,
        ))

        # Convert failures to resolved escalations so reviewer has visibility
        escalations = [
            Escalation(
                identity=f["identity"],
                authority_type="validation",
                reason=(
                    f"Boundary failure at {f['boundary']}: "
                    + "; ".join(c["detail"] for c in f["failures"])
                ),
                context={
                    "deliverable_id": f["deliverable_id"],
                    "sub_type": "boundary_failure_override",
                    "override_id": overrides[i].override_id,
                },
                resolved=True,
                resolution=f"Override {overrides[i].override_id}: {rationale[:80]}",
            )
            for i, f in enumerate(all_failures)
        ]
        return {
            "current_phase": "review",
            "validation_results": validation_results,
            "validation_overrides": overrides,
            "audit_trail": audit_entries,
            "escalations": escalations,
            "_boundary_fail_counts": boundary_fail_counts,
        }

    # Handle "reject" — end the project
    if action == "reject":
        return {
            "current_phase": "complete",
            "validation_results": validation_results,
            "error": f"Project rejected: {fail_count} deliverables failed boundary validation.",
            "audit_trail": audit_entries,
        }

    # Handle "rework" — in Tier 1, this is equivalent to reject since
    # we don't yet have the rework loop. Log it and proceed to reviewer
    # with escalations so failures are visible.
    # Tier 2 will route failed task orders back to workers.
    escalations = [
        Escalation(
            identity=f["identity"],
            authority_type="validation",
            reason=(
                f"Boundary failure at {f['boundary']}: "
                + "; ".join(c["detail"] for c in f["failures"])
            ),
            context={
                "deliverable_id": f["deliverable_id"],
                "sub_type": "boundary_failure",
            },
        )
        for f in all_failures
    ]
    audit_entries.append(AuditEntry(
        identity="PRINCIPAL", archetype="deliverable_validator",
        action="rework_requested",
        detail=f"Rework requested for {fail_count} deliverables. Tier 1: routing to reviewer with escalations.",
        timestamp=datetime.now(timezone.utc).isoformat(),
    ))
    return {
        "current_phase": "review",
        "validation_results": validation_results,
        "audit_trail": audit_entries,
        "escalations": escalations,
        "_boundary_fail_counts": boundary_fail_counts,
    }
