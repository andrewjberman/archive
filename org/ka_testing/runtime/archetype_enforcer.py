"""
G2: Archetype Enforcement — Pre/post validation wrapper.

Wraps each generic archetype node with I/O validation and tool scoping
derived from ARCHETYPES.md access gating table.

Authority type: archetype_constraint (sub-boundary, system-enforced, Tier 0).
Distinct from boundary validation (Tier 1) — archetype violations are routing
errors, not quality failures. See authority_types.yaml.

Ontology source: specs/core/ARCHETYPES.md (Access Gating, Behavioral Contracts)
                 specs/core/ARCHETYPE_REGISTRY.yaml (canonical identifiers)
                 contracts/authority_types.yaml (archetype_constraint type)
Runtime spec: runtime/specs/EXECUTION.md
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from .state import AuditEntry, Escalation


# ---------------------------------------------------------------------------
# Per-archetype contracts (from ARCHETYPES.md access gating table)
# ---------------------------------------------------------------------------

# Per-archetype contracts derived from ARCHETYPE_REGISTRY.yaml.
# Identifiers are strings (append-only registry), not bit positions.
# write_layers align with ARCHETYPE_REGISTRY.yaml write_layers field.
ARCHETYPE_CONTRACTS = {
    "supplier": {
        "consumes": {"src/"},           # Can read own src/
        "produces": {"src/"},           # Writes to src/
        "forbidden_writes": {"log/", "asm/", "dlv/", "ctl/"},
        "otr_layer": "src",
        "canonical_actions": ["create", "verify"],
    },
    "transformer": {
        "consumes": {"src/", "log/"},   # Reads src/ (upstream) + own log/
        "produces": {"log/"},           # Writes to log/
        "forbidden_writes": {"asm/", "dlv/", "ctl/"},
        "otr_layer": "log",
        "canonical_actions": ["modify", "verify"],
    },
    "compositor": {
        "consumes": {"src/", "log/", "asm/"},  # Reads src/ + log/ + own asm/
        "produces": {"asm/"},           # Writes to asm/
        "forbidden_writes": {"dlv/", "ctl/"},
        "otr_layer": "asm",
        "canonical_actions": ["create", "modify", "verify"],
    },
    "operator": {
        "consumes": {"asm/", "dlv/"},   # Reads asm/ (upstream) + own dlv/
        "produces": {"dlv/"},           # Writes to dlv/
        "forbidden_writes": {"src/", "log/", "ctl/"},
        "otr_layer": "dlv",
        "canonical_actions": ["modify", "verify", "complete"],
    },
}


def make_archetype_node(archetype: str, base_fn: Callable) -> Callable:
    """Wrap a worker node function with archetype enforcement.

    Pre-validation: checks input state is consumable by this archetype.
    Post-validation: checks output contains only artifacts this archetype
    can produce. Violations become escalations, not silent corrections.

    Args:
        archetype: One of supplier, transformer, compositor, operator.
        base_fn: The base worker_node function to wrap.

    Returns:
        Wrapped function with same signature as base_fn.
    """
    contract = ARCHETYPE_CONTRACTS.get(archetype)
    if not contract:
        # Unknown archetype — pass through without enforcement
        return base_fn

    def enforced_node(state: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        identity = state.get("identity", "unknown")
        task_order = state.get("task_order")
        task_id = task_order.id if task_order else "unknown"

        # --- Pre-validation: check deliverable paths are in scope ---
        if task_order and hasattr(task_order, "deliverables"):
            pre_violations = _check_path_scope(
                paths=task_order.deliverables,
                allowed_writes=contract["produces"],
                forbidden_writes=contract["forbidden_writes"],
                archetype=archetype,
            )
            if pre_violations:
                return {
                    "escalations": [
                        Escalation(
                            identity=identity,
                            authority_type="archetype_constraint",
                            reason=(
                                f"Archetype enforcement: {archetype} task order "
                                f"{task_id} targets forbidden paths"
                            ),
                            context={
                                "violations": pre_violations,
                                "archetype": archetype,
                                "task_order_id": task_id,
                                "check": "pre_validation",
                            },
                        )
                    ],
                    "audit_trail": [
                        AuditEntry(
                            identity=identity,
                            archetype=archetype,
                            action="archetype_violation_pre",
                            detail=f"Forbidden paths in task order: {pre_violations}",
                            timestamp=now,
                        )
                    ],
                }

        # --- Execute the base node ---
        result = base_fn(state)

        # --- Post-validation: check output deliverable paths ---
        deliverables = result.get("deliverables", [])
        for d in deliverables:
            post_violations = _check_path_scope(
                paths=d.file_paths if hasattr(d, "file_paths") else [],
                allowed_writes=contract["produces"],
                forbidden_writes=contract["forbidden_writes"],
                archetype=archetype,
            )
            if post_violations:
                # Don't suppress the deliverable — flag it with escalation
                if "escalations" not in result:
                    result["escalations"] = []
                result["escalations"].append(
                    Escalation(
                        identity=identity,
                        authority_type="archetype_constraint",
                        reason=(
                            f"Archetype enforcement: {archetype} produced "
                            f"artifacts in forbidden paths"
                        ),
                        context={
                            "violations": post_violations,
                            "archetype": archetype,
                            "deliverable_id": d.id if hasattr(d, "id") else "unknown",
                            "check": "post_validation",
                        },
                    )
                )
                if "audit_trail" not in result:
                    result["audit_trail"] = []
                result["audit_trail"].append(
                    AuditEntry(
                        identity=identity,
                        archetype=archetype,
                        action="archetype_violation_post",
                        detail=f"Deliverable wrote to forbidden paths: {post_violations}",
                        timestamp=now,
                    )
                )

        return result

    # Preserve function name for LangGraph node naming
    enforced_node.__name__ = f"{archetype}_enforced"
    return enforced_node


def _check_path_scope(
    paths: list[str],
    allowed_writes: set[str],
    forbidden_writes: set[str],
    archetype: str,
) -> list[str]:
    """Check if any paths fall in forbidden OTR layers.

    Returns list of violation descriptions (empty if all clear).
    """
    violations = []
    for path in paths:
        normalized = path.replace("\\", "/").lower()
        for forbidden in forbidden_writes:
            if f"/{forbidden}" in normalized or normalized.startswith(forbidden):
                violations.append(
                    f"Path '{path}' is in '{forbidden}' "
                    f"(forbidden for {archetype})"
                )
    return violations


def scope_tools_for_archetype(
    tools: list[dict[str, Any]],
    archetype: str,
) -> list[dict[str, Any]]:
    """Filter/modify tool definitions based on archetype access gating.

    For write tools (write_file, edit_file), wraps the handler to
    reject writes to forbidden paths. Read tools are unrestricted
    within the adjacent-read rule (enforced at a higher level).
    """
    contract = ARCHETYPE_CONTRACTS.get(archetype)
    if not contract:
        return tools

    forbidden = contract["forbidden_writes"]
    scoped_tools = []

    for tool in tools:
        if tool["name"] in ("write_file", "edit_file", "apply_patch"):
            # Wrap handler to enforce write scope
            original_handler = tool["handler"]
            scoped_tools.append({
                **tool,
                "handler": _make_scoped_write_handler(
                    original_handler, forbidden, archetype
                ),
            })
        else:
            scoped_tools.append(tool)

    return scoped_tools


def _make_scoped_write_handler(
    original_handler: Callable,
    forbidden: set[str],
    archetype: str,
) -> Callable:
    """Create a write handler that rejects forbidden paths."""
    def scoped_handler(**kwargs):
        file_path = kwargs.get("file_path", "")
        normalized = file_path.replace("\\", "/").lower()
        for f in forbidden:
            if f"/{f}" in normalized or normalized.startswith(f):
                return (
                    f"BLOCKED: {archetype} archetype cannot write to "
                    f"'{f}' paths. This is an access gating violation. "
                    f"Escalate to coordinator if you believe this task "
                    f"requires cross-layer access."
                )
        return original_handler(**kwargs)

    return scoped_handler
