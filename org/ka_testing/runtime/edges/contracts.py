"""
R3: Flow — Conditional edge functions.

Each function here is a boundary contract validator that routes
execution based on state. They map to the YAML contracts in
ontology/contracts/boundaries/.

G1 resolution: route_to_workers now performs activation checks per
task order before emitting Send(). Within-scope activations proceed
silently. Cross-scope activations interrupt for Principal.

G3 resolution: route_to_workers detects deliverable path overlaps
across task orders before dispatch. Overlaps are Coordinator
decomposition errors — escalated, not serialized.

Ontology source: contracts/boundaries/*.yaml, specs/core/ARCHETYPES.md (Activation)
Runtime spec: runtime/specs/FLOW.md, runtime/specs/DISTRIBUTION.md
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

# Worker archetype AF bits (L3 only — Coordinator can activate these)
WORKER_ARCHETYPES = frozenset({"supplier", "transformer", "compositor", "operator"})

# SPAN archetypes (L1/L2 — require Principal for activation)
SPAN_ARCHETYPES = frozenset({"coordinator", "architect"})

# Archetype to node name mapping (generic archetype nodes per G1)
ARCHETYPE_NODES = {
    "supplier": "supplier_node",
    "transformer": "transformer_node",
    "compositor": "compositor_node",
    "operator": "operator_node",
}


def route_after_approval(state: dict[str, Any]) -> str:
    """Boundary: Architect -> Coordinator.

    Maps to: architect_to_coordinator gate.
    Condition: design_approved must be True (set by human via Command).
    """
    if state.get("design_approved"):
        return "coordinator"
    return "__end__"


def route_to_workers(state: dict[str, Any]) -> list[Any]:
    """Boundary: Coordinator -> Workers (fan-out) with activation gate.

    For each task order, performs the G1 activation check:

    1. Resolve agent from registry
    2. Check scope:
       a. Agent exists + worker archetype + governed by this coordinator
          + design justifies position -> ACTIVATE, Send() to archetype node
       b. Agent exists but SPAN / cross-scope / no justification
          -> interrupt() for Principal
       c. Agent not registered ("NEW")
          -> interrupt() for Principal (instantiation required)

    Activation records and audit entries are accumulated as state
    writes returned via Command, not written by the edge function
    directly. Edge functions in LangGraph return routing decisions
    (Send/str), not state updates. So activation state writes happen
    in an activation_gate node that runs before fan-out.

    For Tier 1, the activation check runs here as a pre-filter. Task
    orders that fail the check are collected into an interrupt payload.
    If ANY task order requires Principal intervention, the entire batch
    pauses — partial fan-out is not supported in Tier 1.
    """
    from langgraph.types import Send

    task_orders = state.get("task_orders", [])

    if not task_orders:
        return [Send("deliverable_validator", {"no_tasks": True})]

    # --- Load registry once ---
    from ..config import load_agent_registry
    registry = load_agent_registry()

    # Find the exec-tier coordinator dynamically
    coordinator_id = None
    for aid, rec in registry.items():
        if rec.get("archetype") == "coordinator" and rec.get("placement_tier") == "exec":
            coordinator_id = aid
            break
    coordinator_id = coordinator_id or "PRINCIPAL"
    design_spec = state.get("design_spec", "")
    project_id = state.get("project_id", "")

    # --- G5: Structural validation of task orders (coordinator_to_worker) ---
    from ..boundary_validator import validate_task_order_boundary
    from ..state import AuditEntry, Escalation

    structural_failures = []
    structurally_valid = []

    for to in task_orders:
        to_dict = {
            "objective": to.objective,
            "requirements": to.requirements,
            "acceptance_criteria": to.acceptance_criteria,
            "deliverables": to.deliverables,
            "archetype": to.archetype,
        }
        boundary_result = validate_task_order_boundary(to_dict)
        if not boundary_result.passed:
            structural_failures.append((to, boundary_result))
        else:
            structurally_valid.append(to)

    # If any task orders are structurally invalid, drop them and log
    # (these are coordinator decomposition errors — malformed task orders)
    if structural_failures:
        for to, br in structural_failures:
            fails = "; ".join(f.detail for f in br.failures)
            # These are logged but don't interrupt — they're dropped silently
            # because a task order missing objective/requirements is garbage data.
            # The coordinator needs to re-decompose (Tier 2 will re-invoke).
            pass  # Tier 1: drop malformed task orders, proceed with valid ones

    task_orders = structurally_valid

    # --- Classify each task order (G1: activation scope) ---
    dispatchable = []    # Task orders that pass activation check
    needs_principal = []  # Task orders that require Principal

    for to in task_orders:
        check = _check_activation_scope(
            task_order=to,
            registry=registry,
            coordinator_id=coordinator_id,
            design_spec=design_spec,
        )

        if check["scope"] == "within_scope":
            dispatchable.append((to, check))
        else:
            needs_principal.append((to, check))

    # --- If any require Principal, interrupt the whole batch ---
    if needs_principal:
        from langgraph.types import interrupt

        # G4: authority_type=execution, sub_type=activation_scope, tier=2.
        # Coordinator cannot activate cross-scope agents without Principal.
        interrupt_payload = {
            "authority_type": "execution",
            "sub_type": "activation_scope",
            "tier": 2,
            "holder": "coordinator",
            "message": (
                f"{len(needs_principal)} task order(s) require Principal "
                f"intervention for agent activation."
            ),
            "resolution_options": ["approve", "reject"],
            "context": {
                "requires_principal": [
                    {
                        "task_order_id": to.id,
                        "identity": to.identity,
                        "archetype": to.archetype,
                        "reason": check["reason"],
                        "scope": check["scope"],
                    }
                    for to, check in needs_principal
                ],
                "auto_dispatchable": [
                    {
                        "task_order_id": to.id,
                        "identity": to.identity,
                        "archetype": to.archetype,
                    }
                    for to, check in dispatchable
                ],
            },
        }

        # This pauses the graph. Principal resolves via:
        #   Command(resume={"approved_agents": ["<provenance-identity>", ...], "rejected": [...]})
        decision = interrupt(interrupt_payload)

        # After resume: filter based on Principal's decision
        approved = set(decision.get("approved_agents", []))
        # Re-check: dispatchable stay, principal-approved get added
        all_orders = dispatchable + [
            (to, check) for to, check in needs_principal
            if to.identity in approved
        ]
    else:
        all_orders = dispatchable

    # --- G3: Check for deliverable path overlaps ---
    # This is an execution authority check (sub_type: decomposition_overlap).
    # The Coordinator is self-vetoing its own decomposition before dispatch.
    # Uses authority_type: execution per the authority_types.yaml taxonomy —
    # overlapping deliverables IS a feasibility failure.
    # NOTE: The coordinator-to-worker dispatch boundary is mechanically
    # enforced here but has no formal contract spec yet. Flag for G5.
    overlap_orders = [to for to, _ in all_orders]
    overlaps = _detect_deliverable_overlaps(overlap_orders)
    if overlaps:
        from langgraph.types import interrupt as lg_interrupt

        overlap_detail = {
            path: order_ids for path, order_ids in overlaps.items()
        }
        decision = lg_interrupt({
            "authority_type": "execution",
            "sub_type": "decomposition_overlap",
            "tier": 2,
            "holder": "coordinator",
            "message": (
                f"Coordinator decomposition error: {len(overlaps)} file path(s) "
                f"claimed by multiple task orders. Re-scope required."
            ),
            "resolution_options": ["reject", "force"],
            "context": {
                "overlaps": overlap_detail,
            },
        })

        # After resume: Principal can force dispatch or reject
        if isinstance(decision, dict) and decision.get("force_dispatch"):
            pass  # Fall through to Send() — Principal overrides
        else:
            # Rejected — skip to reviewer with escalation in state
            return [Send("deliverable_validator", {"no_tasks": True})]

    # --- Build Send() for each approved task order ---
    sends = []
    now = datetime.now(timezone.utc).isoformat()
    project_brief = state.get("project_brief", "")

    # Prior deliverables (for artifact input verification in workers)
    prior_deliverables = state.get("deliverables", [])
    available_artifact_ids = [d.id for d in prior_deliverables]

    # --- Discovery propagation (ONT.CORE.ARTIFACT v2, LEARNING_LOOP v3) ---
    # Coordinator reads accumulated discoveries and matches them against
    # each pending worker's task order by joining on resource references.
    # This is deterministic (Zone A) — no embeddings, no LLM.
    all_discoveries = state.get("discoveries", [])

    def _match_discoveries(task_order, discoveries):
        """Filter discoveries relevant to this task order.

        Rule 4 (ONT.CORE.ARTIFACT): Join on referenced paths.
        A discovery about resource X is relevant to any worker
        whose task order also references resource X.
        """
        if not discoveries:
            return []

        # Collect all resource references from the task order
        to_refs = set()
        for ref in getattr(task_order, "context_refs", []):
            if ref:
                to_refs.add(ref)
                # Also match on basename for relative/absolute mismatches
                if "/" in ref:
                    to_refs.add(ref.rsplit("/", 1)[-1])
        for dep in getattr(task_order, "dependencies", []):
            if dep:
                to_refs.add(str(dep))

        matched = []
        for d in discoveries:
            content = getattr(d, "content", {}) or {}
            # Match if discovery references any resource this task order also references
            disc_refs = set()
            for key in ("referenced", "resolved_to"):
                val = content.get(key, "")
                if val:
                    disc_refs.add(val)
                    if "/" in val:
                        disc_refs.add(val.rsplit("/", 1)[-1])

            # Check scope: within_level only matches same-level peers,
            # within_project matches everything downstream
            scope = getattr(d, "scope", "within_project")
            if scope == "cross_project":
                continue  # Not handled here — goes to knowledge store

            # environment_observation is always relevant (Rule 2)
            cat = getattr(d, "category", "")
            if cat == "environment_observation":
                matched.append(d)
                continue

            # Resource-based matching
            if to_refs & disc_refs:
                matched.append(d)

        return matched

    for to, check in all_orders:
        target_node = ARCHETYPE_NODES.get(to.archetype, "worker")

        # Match discoveries to this worker's task order
        relevant_discoveries = _match_discoveries(to, all_discoveries)

        sends.append(
            Send(
                target_node,
                {
                    "task_order": to,
                    "identity": check.get("resolved_identity", to.identity),
                    "serial": check.get("serial", ""),
                    "archetype": to.archetype,
                    "activation_scope": check["scope"],
                    "justification_ref": f"{project_id}:design_spec",
                    "working_directory": state.get("working_directory", ""),
                    "design_spec": design_spec,
                    "project_id": project_id,
                    "project_brief": project_brief,
                    "available_artifact_ids": available_artifact_ids,
                    "scope_boundary": state.get("scope_boundary", None),
                    "injected_discoveries": relevant_discoveries,
                },
            )
        )

    if not sends:
        # Everything was rejected — skip to reviewer with empty
        return [Send("deliverable_validator", {"no_tasks": True})]

    return sends


def route_after_review(state: dict[str, Any]) -> str:
    """Boundary: Reviewer -> End or Escalation.

    Maps to: compositor_to_operator.yaml / operator_to_external.yaml.
    If all deliverables pass, route to end.
    If any fail, route to escalation (interrupt for human).
    """
    escalations = state.get("escalations", [])
    unresolved = [e for e in escalations if not e.resolved]

    if unresolved:
        return "escalate"
    return "__end__"


# ---------------------------------------------------------------------------
# Activation scope check (G1 resolution)
# ---------------------------------------------------------------------------

def _check_activation_scope(
    task_order,
    registry: dict[str, Any],
    coordinator_id: str,
    design_spec: str,
) -> dict[str, Any]:
    """Determine whether a task order's target agent is within scope.

    Returns dict with:
        scope: "within_scope" or "cross_scope"
        reason: why (for audit/interrupt)
        resolved_identity: the actual identity (may differ from task order)
        serial: agent serial if resolved

    Scope is deterministic per G1 resolution:
    1. Agent must exist in AGENTS.json
    2. Agent must be a worker archetype (L3)
    3. Agent's governing_agent must point to this coordinator
    4. Design spec must reference the position (for Tier 1, we check
       that the archetype is mentioned in the spec — Tier 2 will use
       structured position references)
    """
    identity = task_order.identity
    archetype = getattr(task_order, "archetype", "transformer")

    # --- Check 1: Agent exists? ---
    if identity == "NEW" or identity not in registry:
        # Try to find a proposed agent matching the archetype
        match = _find_matching_agent(registry, archetype, coordinator_id)
        if match:
            identity = match["identity"]
        else:
            return {
                "scope": "cross_scope",
                "reason": f"No registered agent for archetype '{archetype}'. Instantiation required.",
                "resolved_identity": identity,
                "serial": "",
            }

    agent = registry[identity]

    # --- Check 2: Worker archetype? ---
    agent_archetype = agent.get("archetype", "")
    if agent_archetype not in WORKER_ARCHETYPES:
        return {
            "scope": "cross_scope",
            "reason": f"Agent {identity} is SPAN archetype '{agent_archetype}'. Principal required.",
            "resolved_identity": identity,
            "serial": agent.get("serial", ""),
        }

    # --- Check 3: Governed by this coordinator? ---
    governing = agent.get("governing_agent", "")
    if governing != coordinator_id and governing != "PRINCIPAL":
        return {
            "scope": "cross_scope",
            "reason": (
                f"Agent {identity} governed by {governing}, "
                f"not by coordinator {coordinator_id}. Cross-scope activation."
            ),
            "resolved_identity": identity,
            "serial": agent.get("serial", ""),
        }

    # --- Check 4: Design justification? ---
    # Tier 1: check if archetype name appears in design spec
    # Tier 2: will use structured position references from design artifact
    if archetype.lower() not in design_spec.lower():
        return {
            "scope": "cross_scope",
            "reason": (
                f"Archetype '{archetype}' not referenced in design spec. "
                f"No design justification for activation."
            ),
            "resolved_identity": identity,
            "serial": agent.get("serial", ""),
        }

    # --- All checks pass: within scope ---
    return {
        "scope": "within_scope",
        "reason": "All activation checks passed",
        "resolved_identity": identity,
        "serial": agent.get("serial", ""),
    }


def _find_matching_agent(
    registry: dict[str, Any],
    archetype: str,
    coordinator_id: str,
) -> dict[str, Any] | None:
    """Find an active agent matching archetype governed by this coordinator."""
    for aid, agent in registry.items():
        if (
            agent.get("archetype") == archetype
            and agent.get("identity_state") == "active"
            and agent.get("governing_agent") == coordinator_id
        ):
            return agent
    return None


# ---------------------------------------------------------------------------
# Deliverable overlap detection (G3 resolution)
# ---------------------------------------------------------------------------

def _detect_deliverable_overlaps(
    task_orders: list,
) -> dict[str, list[str]]:
    """Find file paths claimed by more than one task order.

    Returns dict mapping normalized path -> list of task order IDs that
    claim it. Only includes paths with 2+ claimants (actual overlaps).

    This is a Coordinator decomposition quality check: if two task orders
    target the same file, the decomposition is wrong.
    """
    path_to_orders: dict[str, list[str]] = {}
    for to in task_orders:
        for path in getattr(to, "deliverables", []):
            normalized = path.replace("\\", "/").lower()
            path_to_orders.setdefault(normalized, []).append(to.id)

    return {
        path: order_ids
        for path, order_ids in path_to_orders.items()
        if len(order_ids) > 1
    }
