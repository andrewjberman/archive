"""
Dispatch nodes — dependency-aware staged execution.

dispatch_planner: Topological sort of task order dependencies -> dispatch plan.
level_collector: Convergence barrier between dispatch levels.

These two nodes replace the flat Send()-all-workers fan-out with
staged execution that respects the dependency DAG.

Ontological grounding:
  ONT.CORE.ARTIFACT_DEPENDENCY — Artifact Dependency Topology (DAG invariant, convergence)
  ONT.CORE.ARCHETYPE — Coordinator's "in what order" responsibility
"""

from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any

from ..state import AuditEntry, Discovery, LevelOutcome, ProjectState


def dispatch_planner_node(state: ProjectState) -> dict[str, Any]:
    """Build a dispatch plan from the coordinator's task order dependencies.

    Pure function — no API call. Reads task_orders, extracts dependency
    edges, topological sorts into levels, validates structure (G5),
    checks activation scope (G1 initial pass).

    Output: dispatch_plan (list of levels, each level is a list of
    task order IDs), current_dispatch_level = 0.
    """
    task_orders = state.get("task_orders", [])
    project_id = state.get("project_id", "")
    now = datetime.now(timezone.utc).isoformat()

    if not task_orders:
        return {
            "dispatch_plan": [],
            "current_dispatch_level": 0,
            "current_phase": "review",
            "audit_trail": [AuditEntry(
                identity="SYSTEM", archetype="dispatch_planner",
                action="empty_dispatch", detail="No task orders to dispatch",
                timestamp=now,
            )],
        }

    # Build task order index
    to_index = {}
    for to in task_orders:
        to_index[to.id] = to

    # --- Build dependency DAG ---
    # Each task order's dependencies field contains IDs of tasks it depends on
    # Also infer dependencies from task ID references (e.g., "T001" in deps)
    adjacency = defaultdict(set)  # task_id -> set of task_ids it depends on
    all_ids = set(to_index.keys())

    for to in task_orders:
        deps = getattr(to, "dependencies", [])
        for dep in deps:
            # Normalize: deps might be full IDs ("PRJ-xxx-T001") or short ("T001")
            resolved = _resolve_dep(dep, all_ids, project_id)
            if resolved and resolved != to.id:
                adjacency[to.id].add(resolved)

    # --- Cycle detection (DAG Invariant 1) ---
    cycle = _detect_cycle(all_ids, adjacency)
    if cycle:
        return {
            "dispatch_plan": [],
            "current_dispatch_level": 0,
            "current_phase": "review",
            "error": f"Circular dependency detected in task orders: {' -> '.join(cycle)}",
            "audit_trail": [AuditEntry(
                identity="SYSTEM", archetype="dispatch_planner",
                action="cycle_detected",
                detail=f"Cycle: {' -> '.join(cycle)}",
                timestamp=now,
            )],
        }

    # --- Value chain floor: infer minimum ordering from archetypes ---
    # The value chain is an ontological invariant (ONT.CORE.VALUE_CHAIN):
    # supplier (L1) -> transformer (L2) -> compositor (L3) -> operator (L4)
    # If the coordinator declared no or insufficient dependency edges,
    # the planner infers edges from archetypes so downstream workers
    # never execute before upstream workers.
    # Declared edges are preserved — the floor only ADDS edges, never removes.
    inferred_count = _inject_value_chain_floor(to_index, adjacency)

    # Re-check for cycles after adding inferred edges
    if inferred_count > 0:
        cycle = _detect_cycle(all_ids, adjacency)
        if cycle:
            return {
                "dispatch_plan": [],
                "current_dispatch_level": 0,
                "current_phase": "review",
                "error": f"Circular dependency after value chain inference: {' -> '.join(cycle)}",
                "audit_trail": [AuditEntry(
                    identity="SYSTEM", archetype="dispatch_planner",
                    action="cycle_after_inference",
                    detail=f"Cycle: {' -> '.join(cycle)}",
                    timestamp=now,
                )],
            }

    # --- Topological sort into levels ---
    levels = _topological_levels(all_ids, adjacency)

    # Convert to list of lists of task order IDs
    dispatch_plan = [list(level) for level in levels]

    # --- Execution Gate: Resource grounding check ---
    # ARTIFACT_AND_CONTRACT_SPEC Section 4b: verify that referenced
    # resources exist before decomposing into work. A design that
    # references nonexistent modules wastes N workers' time.
    working_directory = state.get("working_directory", "")
    if working_directory:
        from pathlib import Path
        work_dir = Path(working_directory)
        missing_resources = []
        # All deliverable paths that will be CREATED (outputs)
        will_create = set()
        for to in task_orders:
            for d in to.deliverables:
                will_create.add(d.replace("\\", "/"))

        # Check context_refs (inputs) — do they exist or will they be created?
        for to in task_orders:
            for ref in getattr(to, "context_refs", []):
                ref_norm = ref.replace("\\", "/")
                ref_path = work_dir / ref
                if not ref_path.exists() and ref_norm not in will_create:
                    missing_resources.append({
                        "task_order_id": to.id,
                        "missing_resource": ref,
                        "type": "context_ref",
                    })

            # Also check if deliverable targets reference directories that don't exist
            for d in to.deliverables:
                d_path = work_dir / d
                parent = d_path.parent
                if not parent.exists() and str(parent) != str(work_dir):
                    try:
                        rel = str(parent.relative_to(work_dir))
                    except ValueError:
                        rel = str(parent)
                    missing_resources.append({
                        "task_order_id": to.id,
                        "missing_resource": rel,
                        "type": "parent_directory",
                    })

        if missing_resources:
            from langgraph.types import interrupt
            gate_decision = interrupt({
                "authority_type": "execution",
                "sub_type": "resource_grounding",
                "tier": 2,
                "holder": "coordinator",
                "message": (
                    f"Execution gate: {len(missing_resources)} referenced "
                    f"resource(s) not found in working directory."
                ),
                "resolution_options": ["proceed", "phase_prep", "fail"],
                "context": {
                    "missing_resources": missing_resources,
                    "working_directory": working_directory,
                    "dispatch_plan": dispatch_plan,
                },
            })

            gate_action = gate_decision.get("action", "proceed") if isinstance(gate_decision, dict) else "proceed"

            if gate_action == "fail":
                return {
                    "dispatch_plan": [],
                    "current_dispatch_level": 0,
                    "current_phase": "review",
                    "error": f"Execution gate FAIL: {len(missing_resources)} missing resources",
                    "audit_trail": [AuditEntry(
                        identity="SYSTEM", archetype="dispatch_planner",
                        action="execution_gate_fail",
                        detail=f"Missing: {[r['missing_resource'] for r in missing_resources]}",
                        timestamp=now,
                    )],
                }

            # phase_prep or proceed — continue with dispatch
            # (In Tier 2, phase_prep would create prerequisite task orders
            # and re-evaluate. In Tier 1, we proceed and let workers
            # create missing files as part of their task.)

    # --- G5: Structural validation of all task orders ---
    from ..boundary_validator import validate_task_order_boundary
    from ..state import Escalation

    structural_failures = []
    valid_ids = set()

    for to in task_orders:
        to_dict = {
            "objective": to.objective,
            "requirements": to.requirements,
            "acceptance_criteria": to.acceptance_criteria,
            "deliverables": to.deliverables,
            "archetype": to.archetype,
        }
        result = validate_task_order_boundary(to_dict)
        if not result.passed:
            structural_failures.append((to.id, result))
        else:
            valid_ids.add(to.id)

    # Remove structurally invalid task orders from the plan
    if structural_failures:
        dispatch_plan = [
            [tid for tid in level if tid in valid_ids]
            for level in dispatch_plan
        ]
        dispatch_plan = [level for level in dispatch_plan if level]  # remove empty levels

    # --- G1: Initial activation check for all agents ---
    from ..config import load_agent_registry
    registry = load_agent_registry()
    activation_issues = []

    for to in task_orders:
        if to.id not in valid_ids:
            continue
        identity = to.identity
        if identity == "NEW" or identity not in registry:
            activation_issues.append({
                "task_order_id": to.id,
                "identity": identity,
                "archetype": to.archetype,
                "reason": f"Agent '{identity}' not in registry. Activation required.",
            })

    # If activation issues exist, interrupt for Principal
    escalations = []
    if activation_issues:
        from langgraph.types import interrupt

        decision = interrupt({
            "authority_type": "execution",
            "sub_type": "activation_scope",
            "tier": 2,
            "holder": "coordinator",
            "message": f"{len(activation_issues)} agent(s) require Principal activation.",
            "resolution_options": ["approve", "reject"],
            "context": {
                "requires_principal": activation_issues,
                "dispatch_plan": dispatch_plan,
            },
        })

        # After resume: filter rejected
        approved = set(decision.get("approved_agents", []))
        if not approved and decision.get("rejected"):
            return {
                "dispatch_plan": [],
                "current_dispatch_level": 0,
                "current_phase": "review",
                "error": "All activations rejected by Principal.",
                "audit_trail": [AuditEntry(
                    identity="SYSTEM", archetype="dispatch_planner",
                    action="activations_rejected", detail="Principal rejected all",
                    timestamp=now,
                )],
            }

    declared_count = sum(len(deps) for deps in adjacency.values()) - inferred_count

    # --- Cross-project discovery loading (ONT.CORE.ARTIFACT v2) ---
    # Load discoveries from prior project runs in the same macro.
    # These are injected as cross_project scope discoveries so
    # level_dispatcher can match them against workers' task orders.
    cross_project_discoveries = _load_cross_project_discoveries(
        working_directory=working_directory,
        macro=state.get("macro", ""),
    )

    audit_detail = (
        f"{len(dispatch_plan)} levels, {sum(len(l) for l in dispatch_plan)} tasks. "
        f"Levels: {[len(l) for l in dispatch_plan]}. "
        f"Edges: {declared_count} declared, {inferred_count} inferred from value chain."
    )
    if cross_project_discoveries:
        audit_detail += f" Loaded {len(cross_project_discoveries)} cross-project discoveries."

    result = {
        "dispatch_plan": dispatch_plan,
        "current_dispatch_level": 0,
        "current_phase": "execution",
        "audit_trail": [AuditEntry(
            identity="SYSTEM", archetype="dispatch_planner",
            action="dispatch_plan_created",
            detail=audit_detail,
            timestamp=now,
        )],
    }

    # Seed the discovery accumulator with cross-project discoveries
    if cross_project_discoveries:
        result["discoveries"] = cross_project_discoveries

    return result


def level_collector_node(state: ProjectState) -> dict[str, Any]:
    """Convergence barrier — runs after all workers in a level complete.

    Produces a LevelOutcome convergence record, increments the dispatch
    level, and signals whether to continue or route to reviewer.

    Refinement 2: carries level outcome for learning loop visibility.
    """
    now = datetime.now(timezone.utc).isoformat()
    current_level = state.get("current_dispatch_level", 0)
    dispatch_plan = state.get("dispatch_plan", [])

    # Determine which task orders were in the current level
    level_task_ids = set()
    if current_level < len(dispatch_plan):
        level_task_ids = set(dispatch_plan[current_level])

    # Check which deliverables were produced for this level's tasks
    deliverables = state.get("deliverables", [])
    completed = []
    failed = []
    artifacts = []

    for tid in level_task_ids:
        matching = [d for d in deliverables if d.task_order_id == tid]
        if matching:
            completed.append(tid)
            artifacts.extend(d.id for d in matching)
        else:
            failed.append(tid)

    outcome = LevelOutcome(
        level=current_level,
        completed=completed,
        failed=failed,
        artifacts_produced=artifacts,
        timestamp=now,
    )

    next_level = current_level + 1

    # --- Persist discoveries to upstream.jsonl (ONT.CORE.ARTIFACT v2) ---
    # After each level converges, write NEW discoveries from this level
    # to the event log for cross-level and cross-project retrieval.
    # This is the Coordinator's Tier 2 responsibility (LEARNING_LOOP v3).
    #
    # Only write discoveries from workers in THIS level to avoid
    # duplicate writes (upstream.jsonl uses append mode).
    all_discoveries = state.get("discoveries", [])
    level_discoveries = [
        d for d in all_discoveries
        if getattr(d, "task_order_id", "") in level_task_ids
    ]
    discovery_count = 0
    if level_discoveries:
        from ..events import get_event_bus
        bus = get_event_bus()
        if bus:
            discovery_count = bus.write_discoveries(level_discoveries)

    detail_msg = (
        f"Level {current_level}: {len(completed)} completed, "
        f"{len(failed)} failed, {len(artifacts)} artifacts."
    )
    if discovery_count:
        detail_msg += f" {discovery_count} discoveries persisted to upstream.jsonl."
    if next_level < len(dispatch_plan):
        detail_msg += " More levels remain."
    else:
        detail_msg += " All levels done."

    return {
        "current_dispatch_level": next_level,
        "level_outcomes": [outcome],
        "audit_trail": [AuditEntry(
            identity="SYSTEM", archetype="level_collector",
            action="level_converged",
            detail=detail_msg,
            timestamp=now,
        )],
    }


# ---------------------------------------------------------------------------
# Edge functions for dispatch
# ---------------------------------------------------------------------------

def level_dispatcher(state: dict[str, Any]) -> list[Any]:
    """Conditional edge: Send() workers for the current dispatch level.

    Refinement 3: G3 overlap detection is per-level (same-level workers
    might collide, cross-level workers can't since they're sequential).
    G1 re-verify agent state at dispatch time.
    """
    from langgraph.types import Send

    dispatch_plan = state.get("dispatch_plan", [])
    current_level = state.get("current_dispatch_level", 0)

    if current_level >= len(dispatch_plan):
        # All levels done -> deliverable_validator
        return [Send("deliverable_validator", {"dispatch_complete": True})]

    level_task_ids = dispatch_plan[current_level]
    if not level_task_ids:
        return [Send("deliverable_validator", {"dispatch_complete": True})]

    # Build task order index from state
    task_orders = state.get("task_orders", [])
    to_index = {to.id: to for to in task_orders}

    level_tasks = [to_index[tid] for tid in level_task_ids if tid in to_index]

    if not level_tasks:
        return [Send("deliverable_validator", {"dispatch_complete": True})]

    # --- G3: Per-level overlap detection ---
    overlaps = _detect_level_overlaps(level_tasks)
    if overlaps:
        from langgraph.types import interrupt as lg_interrupt
        decision = lg_interrupt({
            "authority_type": "execution",
            "sub_type": "decomposition_overlap",
            "tier": 2,
            "holder": "coordinator",
            "message": f"Level {current_level}: {len(overlaps)} overlapping deliverable path(s).",
            "resolution_options": ["reject", "force"],
            "context": {"overlaps": overlaps, "level": current_level},
        })
        if isinstance(decision, dict) and not decision.get("force_dispatch"):
            return [Send("deliverable_validator", {"dispatch_complete": True})]

    # --- G1: Re-verify agent state at dispatch time ---
    from ..config import load_agent_registry
    registry = load_agent_registry()

    # Archetype to node mapping
    ARCHETYPE_NODES = {
        "supplier": "supplier_node",
        "transformer": "transformer_node",
        "compositor": "compositor_node",
        "operator": "operator_node",
    }

    sends = []
    design_spec = state.get("design_spec", "")
    project_id = state.get("project_id", "")
    project_brief = state.get("project_brief", "")

    # Collect deliverable IDs from all prior levels for artifact verification.
    # Workers can check that their declared inputs exist before executing.
    prior_deliverables = state.get("deliverables", [])
    available_artifact_ids = {d.id for d in prior_deliverables}

    # --- Discovery propagation (ONT.CORE.ARTIFACT v2, LEARNING_LOOP v3) ---
    # Coordinator reads accumulated discoveries from prior levels and matches
    # them against each pending worker's task order by resource references.
    # This is Tier 2 process refinement: inject what earlier workers learned.
    all_discoveries = state.get("discoveries", [])

    for to in level_tasks:
        target_node = ARCHETYPE_NODES.get(to.archetype, "worker")

        # Resolve agent (may be NEW — already approved by planner)
        resolved_id = to.identity
        serial = ""
        if resolved_id != "NEW" and resolved_id in registry:
            agent = registry[resolved_id]
            serial = agent.get("serial", "")
            # G1 re-verify: check agent is still active
            if agent.get("identity_state") != "active":
                continue  # Skip inactive agents

        # Match discoveries to this worker's task order (Rule 4: deterministic join)
        relevant_discoveries = _match_discoveries(to, all_discoveries)

        sends.append(Send(target_node, {
            "task_order": to,
            "identity": resolved_id,
            "serial": serial,
            "archetype": to.archetype,
            "activation_scope": "within_scope",
            "justification_ref": f"{project_id}:design_spec",
            "working_directory": state.get("working_directory", ""),
            "design_spec": design_spec,
            # Session log slug fix: workers need these for _make_slug()
            "project_id": project_id,
            "project_brief": project_brief,
            # Artifact verification: IDs available from completed prior levels
            "available_artifact_ids": list(available_artifact_ids),
            # Scope containment: propagate from project config
            "scope_boundary": state.get("scope_boundary", None),
            # Tier-aware context loading (EXECUTION_COMPLEXITY)
            "complexity_tier": state.get("design_spec_structured", {}).get("complexity_tier", "M"),
            # Task orders for upstream artifact exemption in pre-flight
            "task_orders": task_orders,
            # Discovery propagation (ONT.CORE.ARTIFACT v2)
            "injected_discoveries": relevant_discoveries,
        }))

    if not sends:
        return [Send("deliverable_validator", {"dispatch_complete": True})]

    return sends


def route_after_level(state: dict[str, Any]) -> str:
    """After level_collector: dispatch next level or go to reviewer."""
    dispatch_plan = state.get("dispatch_plan", [])
    current_level = state.get("current_dispatch_level", 0)

    if current_level >= len(dispatch_plan):
        return "reviewer"
    return "level_dispatch"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resolve_dep(dep: str, all_ids: set[str], project_id: str) -> str | None:
    """Resolve a dependency reference to a task order ID."""
    if dep in all_ids:
        return dep
    # Try prefixing with project ID (e.g., "T001" -> "PRJ-xxx-T001")
    candidate = f"{project_id}-{dep}"
    if candidate in all_ids:
        return candidate
    # Try matching suffix
    for tid in all_ids:
        if tid.endswith(f"-{dep}"):
            return tid
    return None


def _detect_cycle(nodes: set[str], adjacency: dict[str, set[str]]) -> list[str] | None:
    """Detect cycles in the dependency graph. Returns cycle path or None."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}
    path = []

    def dfs(node):
        color[node] = GRAY
        path.append(node)
        for dep in adjacency.get(node, set()):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                idx = path.index(dep)
                return path[idx:] + [dep]
            if color[dep] == WHITE:
                result = dfs(dep)
                if result:
                    return result
        path.pop()
        color[node] = BLACK
        return None

    for node in nodes:
        if color[node] == WHITE:
            result = dfs(node)
            if result:
                return result
    return None


def _topological_levels(nodes: set[str], adjacency: dict[str, set[str]]) -> list[set[str]]:
    """Kahn's algorithm variant that produces levels (parallel groups).

    Level 0 = nodes with no dependencies (in-degree 0).
    Level 1 = nodes whose dependencies are all in level 0.
    And so on.
    """
    in_degree = {n: 0 for n in nodes}
    reverse = defaultdict(set)  # node -> set of nodes that depend on it

    for node, deps in adjacency.items():
        for dep in deps:
            if dep in nodes:
                in_degree[node] = in_degree.get(node, 0) + 1
                reverse[dep].add(node)

    # Also count nodes not in adjacency
    for n in nodes:
        if n not in in_degree:
            in_degree[n] = 0

    levels = []
    remaining = set(nodes)

    while remaining:
        # Find all nodes with in-degree 0 among remaining
        level = {n for n in remaining if in_degree.get(n, 0) == 0}
        if not level:
            # Shouldn't happen if cycle detection ran first
            # Put everything remaining in one level as fallback
            level = remaining.copy()

        levels.append(level)
        remaining -= level

        # Reduce in-degree for dependents
        for node in level:
            for dependent in reverse.get(node, set()):
                if dependent in remaining:
                    in_degree[dependent] = max(0, in_degree[dependent] - 1)

    return levels


# Value chain ordering: supplier -> transformer -> compositor -> operator
# This is ONT.CORE.VALUE_CHAIN — an ontological invariant, not a heuristic.
VALUE_CHAIN_ORDER = {
    "supplier": 0,
    "transformer": 1,
    "compositor": 2,
    "operator": 3,
}


def _inject_value_chain_floor(
    to_index: dict[str, Any],
    adjacency: dict[str, set[str]],
) -> int:
    """Inject minimum ordering edges from the value chain.

    For every pair of task orders where the consumer's archetype is
    downstream of the producer's archetype in the value chain, add a
    dependency edge from consumer -> producer (consumer depends on producer).

    Same-archetype tasks get no inferred edge (parallel within level).
    Tasks already connected by declared edges are not re-added.

    Returns the number of inferred edges added.
    """
    # Group task order IDs by their value chain level
    by_chain_level: dict[int, list[str]] = defaultdict(list)
    for tid, to in to_index.items():
        archetype = getattr(to, "archetype", "transformer")
        chain_level = VALUE_CHAIN_ORDER.get(archetype, 1)
        by_chain_level[chain_level].append(tid)

    # For each pair of adjacent chain levels, add edges:
    # every task at level N+1 depends on every task at level N
    sorted_levels = sorted(by_chain_level.keys())
    inferred = 0

    for i in range(len(sorted_levels) - 1):
        upstream_level = sorted_levels[i]
        downstream_level = sorted_levels[i + 1]

        upstream_ids = by_chain_level[upstream_level]
        downstream_ids = by_chain_level[downstream_level]

        for down_id in downstream_ids:
            for up_id in upstream_ids:
                if up_id not in adjacency.get(down_id, set()):
                    adjacency[down_id].add(up_id)
                    inferred += 1

    return inferred


def _detect_level_overlaps(task_orders: list) -> dict[str, list[str]]:
    """G3: Detect file path overlaps within a single dispatch level."""
    path_to_orders: dict[str, list[str]] = {}
    for to in task_orders:
        for path in getattr(to, "deliverables", []):
            normalized = path.replace("\\", "/").lower()
            path_to_orders.setdefault(normalized, []).append(to.id)
    return {p: ids for p, ids in path_to_orders.items() if len(ids) > 1}


# ---------------------------------------------------------------------------
# Discovery propagation (ONT.CORE.ARTIFACT v2, LEARNING_LOOP v3)
# ---------------------------------------------------------------------------

def _match_discoveries(task_order, discoveries: list) -> list:
    """Filter discoveries relevant to a task order.

    Rule 4 (ONT.CORE.ARTIFACT v2): Join on referenced paths.
    A discovery about resource X is relevant to any worker
    whose task order also references resource X.

    This is deterministic (Zone A from CONTEXT_SEEDING) —
    no embeddings, no LLM inference.
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

        # Skip cross_project — handled separately via knowledge store
        scope = getattr(d, "scope", "within_project")
        if scope == "cross_project":
            continue

        # environment_observation is always relevant (Rule 2)
        cat = getattr(d, "category", "")
        if cat == "environment_observation":
            matched.append(d)
            continue

        # Resource-based matching
        disc_refs = set()
        for key in ("referenced", "resolved_to"):
            val = content.get(key, "")
            if val:
                disc_refs.add(val)
                if "/" in val:
                    disc_refs.add(val.rsplit("/", 1)[-1])

        if to_refs & disc_refs:
            matched.append(d)

    return matched


def _load_cross_project_discoveries(working_directory: str, macro: str) -> list:
    """Load discoveries from prior project runs in the same macro.

    Reads upstream.jsonl files from previous runs' event directories.
    Returns Discovery objects with scope='cross_project' for injection
    into the current run's workers.

    This is Signal B (CONTEXT_SEEDING) — cross-project knowledge
    propagation via the discovery stream.
    """
    import json as _json
    from pathlib import Path as _Path

    if not working_directory:
        return []

    work_dir = _Path(working_directory)

    # Look for upstream.jsonl in sibling version directories
    # Pattern: {MAC}/projects/{PRJ}/v{VER}/events/flows/upstream.jsonl
    # We want to read from PRIOR versions, not the current one.
    discoveries = []

    # Walk up to find the macro's projects directory
    # The working_directory is typically the project version dir
    events_flows = work_dir / "events" / "flows" / "upstream.jsonl"
    if events_flows.exists():
        # This is the CURRENT run's upstream.jsonl — skip it
        pass

    # Check sibling version directories
    projects_dir = work_dir.parent  # e.g., {MAC}/projects/{PRJ}/
    if projects_dir.exists():
        for version_dir in sorted(projects_dir.iterdir()):
            if version_dir == work_dir:
                continue  # Skip current version
            if not version_dir.is_dir():
                continue
            prior_upstream = version_dir / "events" / "flows" / "upstream.jsonl"
            if prior_upstream.exists():
                try:
                    with open(prior_upstream, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                record = _json.loads(line)
                                if record.get("type") == "discovery":
                                    discoveries.append(Discovery(
                                        agent_serial=record.get("agent_serial", ""),
                                        task_order_id=record.get("task_order", ""),
                                        kf_stage=record.get("kf_stage", "Pe"),
                                        scope="cross_project",
                                        category=record.get("category", ""),
                                        content=record.get("content", {}),
                                        timestamp=record.get("timestamp", ""),
                                    ))
                            except (_json.JSONDecodeError, TypeError):
                                continue
                except OSError:
                    continue

    return discoveries
