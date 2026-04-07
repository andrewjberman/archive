"""
The Graph — Tier 1 project execution event loop.

This is the main LangGraph StateGraph that wires architect -> coordinator
-> workers -> reviewer into an automated pipeline.

G1 resolution applied:
- Six generic archetype nodes (one per archetype, not per agent)
- Identity is in the Send() payload, not in graph topology
- Activation check runs in route_to_workers edge before fan-out
- Within-scope activation: Coordinator proceeds silently
- Cross-scope activation: interrupt() for Principal

Topology:

    START
      |
      v
    architect_scan             (deterministic structural inventory)
      |
      v
    architect_atomize         (containment tree + atomic units)
      |
      v
    architect_graph     (dependency graph + border registry)
      |
      v
    architect                  (produces design spec)
      |
      v
    approval_gate              (interrupt -- human approves or rejects)
      |
      v
    coordinator                (decomposes spec into task orders)
      |
      v
    task_order_gate            (HITL -- Principal approves task orders)
      |                        (approve/modify/reject/redecompose)
      v
    coordinator_recompose     (atom-wave projection + integration plan)
      |
      v
    dispatch_planner           (topological sort + value chain floor)
      |
      v  [Send] per level
    archetype_nodes            (supplier/transformer/compositor/operator)
      |
      v
    level_collector            (convergence barrier)
      |
      +---> more levels: loop back to dispatch
      |
      v
    deliverable_validator      (machine boundary contract gate)
      |                        (interrupt if failures: accept/rework/reject)
      v
    reviewer                   (Operator: binary acceptance test per deliverable)
      |
      v
    coordinator_integration    (Coordinator: recomposition + passage decision)
      |
      +---> [PASS/PARTIAL] END
      |
      +---> [FAIL] escalate    (passage denied -- interrupt for Principal)
      |             |
      |             v
      |            END
      |
      +---> [REDECOMPOSE] coordinator  (Tier 2: redecompose with narrower scope, max 2 attempts)

Usage:
    from graph import build_graph, run_project

    result = run_project(
        brief="Build the portfolio dashboard page",
        working_directory="/path/to/portal",
    )
"""

from __future__ import annotations

import json
import uuid
from typing import Any, Callable

from .state import ProjectState


def _wrap_node(
    node_fn: Callable,
    node_name: str,
    identity: str | None = None,
) -> Callable:
    """Wrap a graph node with event emission and session logging.

    Emits node.started before execution, node.completed after,
    and writes a session log to the agent's folder.
    """
    def wrapped(state):
        import time as _time
        from .events import emit, NODE_STARTED, NODE_COMPLETED, NODE_FAILED, SESSION_LOG_WRITTEN
        from .config import resolve_agent, CORPOREAL_ROOT

        # Resolve agent for this node
        resolved_agent = None
        resolved_identity = identity  # may be passed as provenance identity
        serial = ""
        archetype = ""

        # For workers, identity comes from the Send payload
        if not resolved_identity and isinstance(state, dict):
            resolved_identity = state.get("identity", "")

        # For architect/coordinator, resolve from project-scoped SPAN pair (canonical)
        # Falls back to macro-scoped SPAN pair (legacy DSSR pattern)
        if not resolved_identity and node_name in ("architect", "coordinator"):
            from .config import load_agent_registry
            target_archetype = node_name  # "architect" or "coordinator"
            registry = load_agent_registry()
            macro = state.get("macro", "") if isinstance(state, dict) else ""
            project = state.get("project", "") if isinstance(state, dict) else ""
            domain = state.get("domain", "") if isinstance(state, dict) else ""

            # First: try project-scoped resolution (scope_object == project code)
            if project:
                for identity_key, rec in registry.items():
                    if (rec.get("archetype") == target_archetype
                            and rec.get("placement_tier") == "span"
                            and rec.get("scope_object") == project
                            and rec.get("scope_type") == "project"
                            and (not domain or rec.get("domain") == domain)):
                        resolved_identity = identity_key
                        break

            # Fallback: macro-scoped resolution (legacy pattern)
            if not resolved_identity and macro:
                for identity_key, rec in registry.items():
                    if (rec.get("archetype") == target_archetype
                            and rec.get("placement_tier") == "span"
                            and rec.get("scope_object") == macro
                            and (not domain or rec.get("domain") == domain)):
                        resolved_identity = identity_key
                        break

        if resolved_identity and resolved_identity != "NEW":
            try:
                resolved_agent = resolve_agent(resolved_identity)
                serial = resolved_agent.get("serial", "")
                archetype = resolved_agent.get("archetype", "")
            except (ValueError, KeyError):
                pass

        emit(NODE_STARTED, identity=resolved_identity or "", serial=serial,
             archetype=archetype, node=node_name,
             phase=state.get("current_phase", "") if isinstance(state, dict) else "",
             detail={"summary": f"{node_name} starting"})

        wall_start = _time.monotonic()

        try:
            result = node_fn(state)
        except Exception as e:
            wall_elapsed = _time.monotonic() - wall_start
            emit(NODE_FAILED, identity=resolved_identity or "", serial=serial,
                 archetype=archetype, node=node_name,
                 detail={"error": str(e), "summary": f"FAILED: {e}",
                         "wall_time_s": round(wall_elapsed, 2)})
            raise

        wall_elapsed = _time.monotonic() - wall_start

        # Emit completion event with summary + execution telemetry
        detail = {
            "summary": f"{node_name} complete",
            "wall_time_s": round(wall_elapsed, 2),
        }
        if isinstance(result, dict):
            if "design_spec" in result:
                detail["spec_length"] = len(result["design_spec"])
            if "task_orders" in result:
                detail["task_count"] = len(result["task_orders"])
            if "evaluations" in result:
                verdicts = [e.verdict for e in result.get("evaluations", [])]
                detail["verdicts"] = verdicts
            if "deliverables" in result:
                detail["deliverable_count"] = len(result["deliverables"])

            # Extract execution trace from messages (all nodes now emit this)
            messages = result.get("messages", [])
            for msg in messages:
                if isinstance(msg, dict) and "execution_trace" in msg:
                    trace = msg["execution_trace"]
                    if trace:
                        token_usage = trace.get("token_usage", {})
                        detail["input_tokens"] = token_usage.get("input_tokens", 0)
                        detail["output_tokens"] = token_usage.get("output_tokens", 0)
                        detail["total_tokens"] = token_usage.get("total_tokens", 0)
                        detail["model"] = trace.get("model", "")
                        detail["llm_iterations"] = trace.get("iterations", 0)
                        detail["tool_calls"] = len(trace.get("tool_calls", []))
                        detail["failed_tool_calls"] = trace.get("failed_tool_calls", 0)
                        detail["stop_reason"] = trace.get("stop_reason", "")
                    break  # first message with trace is enough

        emit(NODE_COMPLETED, identity=resolved_identity or "", serial=serial,
             archetype=archetype, node=node_name,
             detail=detail)

        # Write session log
        if resolved_agent:
            from .session_logger import write_session_log
            project_id = ""
            full_state = state if isinstance(state, dict) else {}
            if isinstance(state, dict):
                project_id = state.get("project_id", "")

            log_path = write_session_log(
                agent=resolved_agent,
                node_name=node_name,
                state_update=result if isinstance(result, dict) else {},
                project_id=project_id,
                full_state=full_state,
                corporeal_root=CORPOREAL_ROOT,
            )
            if log_path:
                emit(SESSION_LOG_WRITTEN, identity=resolved_identity or "", serial=serial,
                     node=node_name,
                     detail={"log_path": str(log_path), "summary": f"-> {log_path.name}"})

        return result

    wrapped.__name__ = node_fn.__name__
    return wrapped


def build_graph(checkpointer: Any = None, registry_override: dict | None = None):
    """Construct and compile the project execution graph.

    Args:
        checkpointer: LangGraph checkpointer instance. If None, uses
            MemorySaver (in-memory, dev only). Pass SqliteSaver or
            PostgresSaver for persistence.
        registry_override: If provided, use this registry dict instead
            of loading from AGENTS_JSON. Used by build_subordinate_graph()
            for isolated compilation without global state mutation.

    Returns:
        Compiled StateGraph ready for invoke/stream.
    """
    from langgraph.graph import StateGraph, START, END
    from langgraph.types import interrupt, Command

    from .nodes import architect_node, architect_scan_node, architect_atomize_node, architect_graph_node, coordinator_node, coordinator_recompose_node, worker_node, reviewer_node
    from .nodes.dispatch import (
        dispatch_planner_node,
        level_collector_node,
        level_dispatcher,
        route_after_level,
        wave_gate_node,
        route_after_wave_gate,
    )
    from .nodes.deliverable_validator import deliverable_validator_node
    from .nodes.coordinator_integration import coordinator_integration_node
    from .nodes.task_order_gate import task_order_gate
    from .edges import route_after_approval
    from .archetype_enforcer import make_archetype_node

    # --- Approval gate node (deterministic validation) ---
    def approval_gate(state: ProjectState) -> dict[str, Any]:
        """Deterministic design spec validation gate.

        Replaces the LLM-based approval interrupt with a deterministic check.
        The architect node already ran validation and set design_approved.
        This node reads the result and routes accordingly.

        If validation failed (design_approved=False) and the structured spec
        is missing, the gate fires an interrupt for manual review as fallback.
        If validation passed, the gate proceeds directly to the coordinator.
        """
        approved = state.get("design_approved", False)
        structured = state.get("design_spec_structured", {})

        if approved and structured:
            # Deterministic validation passed -- proceed without interrupt
            return {
                "design_approved": True,
                "current_phase": "planning",
            }

        # Validation failed or no structured spec -- check if we should retry or escalate
        # Extract validation errors from the most recent audit entry
        errors = []
        for entry in reversed(state.get("audit_trail", [])):
            if hasattr(entry, "action") and entry.action == "design_spec_validation":
                errors = [entry.detail]
                break

        # Fire interrupt for manual review as fallback
        decision = interrupt({
            "authority_type": "design",
            "sub_type": "spec_approval",
            "tier": 3,
            "holder": "architect",
            "message": (
                f"Design spec validation FAILED. Errors: {'; '.join(errors)}. "
                f"Approve to proceed anyway, or reject to halt."
            ),
            "resolution_options": ["approve", "reject"],
            "context": {
                "design_spec": state.get("design_spec", ""),
                "validation_errors": errors,
                "structured_spec": structured,
            },
        })

        manual_approved = decision.get("approved", False) if isinstance(decision, dict) else bool(decision)

        return {
            "design_approved": manual_approved,
            "current_phase": "planning" if manual_approved else "complete",
            "error": "" if manual_approved else "Design spec rejected after validation failure.",
        }

    # --- Escalation node (human-in-the-loop for failures) ---
    def escalate_node(state: ProjectState) -> dict[str, Any]:
        """Interrupt for human to resolve review failures.

        G4: authority_type=validation, sub_type=review_failure, tier=1.
        Operator (reviewer) escalates failed deliverables. In Tier 1,
        falls through to Principal. Tier 2 will route to Coordinator first.
        """
        unresolved = [e for e in state.get("escalations", []) if not e.resolved]

        decision = interrupt({
            "authority_type": "validation",
            "sub_type": "review_failure",
            "tier": 1,
            "holder": "operator",
            "message": "Deliverables failed review. Resolve or accept.",
            "resolution_options": ["accept", "reject", "escalate"],
            "context": {
                "failures": [
                    {
                        "authority_type": e.authority_type,
                        "reason": e.reason,
                        "context": e.context,
                    }
                    for e in unresolved
                ],
            },
        })

        accepted = decision.get("accepted", False) if isinstance(decision, dict) else bool(decision)

        if accepted:
            for e in state.get("escalations", []):
                e.resolved = True
                e.resolution = "Accepted by principal"
            return {
                "current_phase": "complete",
                "escalations": [],
            }

        return {
            "current_phase": "complete",
            "error": decision.get("reason", "Rework requested"),
        }

    # --- Build the graph ---
    builder = StateGraph(ProjectState)

    # Planning pipeline: deterministic scan before architect
    builder.add_node("architect_scan", architect_scan_node)
    builder.add_node("architect_atomize", architect_atomize_node)
    builder.add_node("architect_graph", architect_graph_node)

    # SPAN nodes (one each — these are specific roles)
    builder.add_node("architect", _wrap_node(architect_node, "architect"))
    builder.add_node("approval_gate", approval_gate)
    builder.add_node("coordinator", _wrap_node(coordinator_node, "coordinator"))
    builder.add_node("task_order_gate", task_order_gate)
    builder.add_node("coordinator_recompose", coordinator_recompose_node)

    # --- cclass node: runs D-mode classification stages inline ---
    def cclass_node(state: ProjectState) -> dict[str, Any]:
        """Run D-mode classification pipeline (Pe+In+index).

        When the coordinator identifies work_type as "classification",
        this node runs the deterministic stages inline and returns
        structured file data. The LLM only handles taxonomy assignment.
        Ac and Ad stages run after LLM classification via finalize().
        """
        from datetime import datetime, timezone
        from .state import AuditEntry

        spec = state.get("design_spec_structured", {})
        working_dir = state.get("working_directory", "")

        try:
            from .modules.cclass import run as cclass_run
            result = cclass_run(
                directory=working_dir,
                key_spine=spec.get("key_spine", ""),
                build_index=True,
            )
            now = datetime.now(timezone.utc).isoformat()
            return {
                "audit_trail": [AuditEntry(
                    identity="SYSTEM", archetype="cclass",
                    action="dmode_classification",
                    detail=f"Pe+In: {result['file_count']} files, groups: {result['groups']}",
                    timestamp=now,
                )],
                "messages": [{
                    "role": "system",
                    "identity": "cclass",
                    "content": json.dumps({
                        "file_count": result["file_count"],
                        "groups": result["groups"],
                        "files": [
                            {"path": f.path, "filename": f.filename,
                             "extension": f.extension, "group": fp.group}
                            for f, fp in zip(result["files"], result["fingerprints"])
                        ],
                    }),
                    "timestamp": now,
                }],
            }
        except Exception as e:
            import sys
            print(f"WARN: cclass failed: {e}", file=sys.stderr)
            return {}

    # Dispatch nodes (dependency-aware staged execution)
    builder.add_node("cclass", cclass_node)
    builder.add_node("dispatch_planner", dispatch_planner_node)
    builder.add_node("wave_gate", wave_gate_node)
    builder.add_node("level_collector", level_collector_node)

    # Generic archetype worker nodes (G2 enforcer wrapping)
    builder.add_node("supplier_node", _wrap_node(make_archetype_node("supplier", worker_node), "worker"))
    builder.add_node("transformer_node", _wrap_node(make_archetype_node("transformer", worker_node), "worker"))
    builder.add_node("compositor_node", _wrap_node(make_archetype_node("compositor", worker_node), "worker"))
    builder.add_node("operator_node", _wrap_node(make_archetype_node("operator", worker_node), "worker"))

    # --- R7: Detect subordinate layers and wire as subgraph nodes ---
    # If any agent in the registry sponsors a subordinate layer
    # (has subordinate_span_architect/coordinator), replace its
    # archetype node with a subgraph that runs a full pipeline internally.
    try:
        from .composition import detect_subordinate_layers, build_subordinate_graph, make_subgraph_node
        from .config import load_agent_registry
        registry = load_agent_registry()
        # Convert registry to list format if needed
        reg_dict = {"agents": list(registry.values())} if isinstance(registry, dict) and "agents" not in registry else registry
        sponsors = detect_subordinate_layers(reg_dict)
        for sponsor in sponsors:
            sponsor_identity = sponsor.get("identity", "")
            sponsor_serial = sponsor.get("serial", "")
            try:
                sub_graph = build_subordinate_graph(sponsor)
                sub_node = make_subgraph_node(sub_graph, sponsor_identity, sponsor_serial)
                node_name = f"sub_{sponsor_serial.replace('.', '_')}"
                builder.add_node(node_name, _wrap_node(sub_node, "worker", identity=sponsor_identity))
                # Wire subordinate node to level_collector like other workers
                builder.add_edge(node_name, "level_collector")
            except Exception:
                pass  # Subordinate graph build failed — skip, use flat worker
    except ImportError:
        pass  # composition module not available
    builder.add_node("worker", _wrap_node(worker_node, "worker"))

    # Validation, integration, and review (separated concerns)
    #   deliverable_validator: contract compliance (machine-gated)
    #   coordinator_integration: recomposition check (Coordinator re-entry)
    #   reviewer: per-task quality evaluation (Operator)
    builder.add_node("deliverable_validator", deliverable_validator_node)
    builder.add_node("coordinator_integration", _wrap_node(coordinator_integration_node, "coordinator_integration"))
    builder.add_node("reviewer", _wrap_node(reviewer_node, "reviewer"))
    builder.add_node("escalate", escalate_node)

    # --- Edges ---

    # Phase 1: Design (scan -> atomize -> crystallize -> architect -> approval)
    def route_after_scan(state: dict[str, Any]) -> str:
        cache_status = state.get("planning_cache_status", {}) or {}
        if cache_status.get("planning_graph_cache_hit"):
            return "architect"
        return "architect_atomize"

    builder.add_edge(START, "architect_scan")
    builder.add_conditional_edges(
        "architect_scan",
        route_after_scan,
        {"architect_atomize": "architect_atomize", "architect": "architect"},
    )
    builder.add_edge("architect_atomize", "architect_graph")
    builder.add_edge("architect_graph", "architect")
    builder.add_edge("architect", "approval_gate")
    builder.add_conditional_edges(
        "approval_gate",
        route_after_approval,
        {"coordinator": "coordinator", "__end__": END},
    )

    # Phase 2: Planning -> cclass or dispatch
    def route_after_coordinator(state: dict[str, Any]) -> str:
        """Route based on complexity tier and work type.

        Tier S: deliverables already produced -> reviewer.
        Classification work: run cclass D-mode stages first -> then dispatch.
        Everything else: dispatch_planner directly.
        """
        phase = state.get("current_phase", "planning")
        if phase == "review":
            return "reviewer"

        # Check if coordinator specified classification work type
        spec = state.get("design_spec_structured", {})
        # Check messages for work_type from coordinator
        for msg in reversed(state.get("messages", [])):
            if isinstance(msg, dict) and msg.get("role") == "coordinator":
                content = msg.get("content", "")
                if '"work_type"' in content and '"classification"' in content:
                    return "cclass"
                break

        # Also check if this looks like classification from the spec
        if spec.get("key_spine") or spec.get("classification_scheme"):
            return "cclass"

        return "task_order_gate"

    builder.add_conditional_edges(
        "coordinator",
        route_after_coordinator,
        {"task_order_gate": "task_order_gate", "reviewer": "deliverable_validator",
         "cclass": "cclass"},
    )

    # Task order gate -> recomposition scaffold or redecompose
    def route_after_task_approval(state: dict[str, Any]) -> str:
        """Route based on HITL task order approval decision."""
        approved = state.get("task_orders_approved", False)
        phase = state.get("current_phase", "")
        error = state.get("error", "")

        if error or phase == "complete":
            return END  # Rejected
        if not approved:
            return "coordinator"  # Redecompose
        return "coordinator_recompose"  # Approved

    builder.add_conditional_edges(
        "task_order_gate",
        route_after_task_approval,
        {"coordinator_recompose": "coordinator_recompose", "coordinator": "coordinator", END: END},
    )

    # cclass -> recomposition scaffold -> dispatch_planner
    builder.add_edge("cclass", "coordinator_recompose")
    builder.add_edge("coordinator_recompose", "dispatch_planner")

    # Dispatch planner -> wave gate -> level_dispatcher
    builder.add_edge("dispatch_planner", "wave_gate")
    builder.add_conditional_edges(
        "wave_gate",
        route_after_wave_gate,
        {"dispatch": "level_dispatch", "__end__": END},
    )

    # All worker nodes -> level_collector (convergence barrier)
    builder.add_edge("supplier_node", "level_collector")
    builder.add_edge("transformer_node", "level_collector")
    builder.add_edge("compositor_node", "level_collector")
    builder.add_edge("operator_node", "level_collector")
    builder.add_edge("worker", "level_collector")

    # Level collector -> next level dispatch OR deliverable_validator
    builder.add_conditional_edges(
        "level_collector",
        route_after_level,
        {"wave_gate": "wave_gate", "reviewer": "deliverable_validator"},
    )

    # level_dispatch is a virtual node that re-dispatches via level_dispatcher
    # LangGraph needs a node to attach the conditional edge to
    builder.add_node("level_dispatch", lambda state: {})  # pass-through
    builder.add_conditional_edges("level_dispatch", level_dispatcher)

    # Phase 3: Validation → Acceptance → Passage (ONT.CORE.DECISION §Boundary Model)
    #   deliverable_validator: contract compliance (machine gate)
    #   reviewer (Operator): binary acceptance test per deliverable (ACCEPT/REJECT)
    #   coordinator_integration (Coordinator): recomposition + passage decision
    # The Operator validates first. The Coordinator decides passage second,
    # informed by the Operator's results.
    builder.add_edge("deliverable_validator", "reviewer")
    builder.add_edge("reviewer", "coordinator_integration")

    def route_after_integration(state: dict[str, Any]) -> str:
        """Route based on Coordinator passage decision.

        PASS    → END (passage authorized — project complete)
        PARTIAL → END with flags (passage authorized with caveats)
        FAIL    → escalate (passage denied — interrupt for Principal)
        REDECOMPOSE → coordinator (Tier 2: redecompose with narrower scope)
        """
        verdict = state.get("integration_verdict", "")
        if verdict == "FAIL":
            return "escalate"
        if verdict == "REDECOMPOSE":
            return "coordinator"
        return "__end__"

    builder.add_conditional_edges(
        "coordinator_integration",
        route_after_integration,
        {"__end__": END, "escalate": "escalate", "coordinator": "coordinator"},
    )
    builder.add_edge("escalate", END)

    # --- Compile ---
    if checkpointer is None:
        from langgraph.checkpoint.memory import MemorySaver
        checkpointer = MemorySaver()

    return builder.compile(checkpointer=checkpointer)


def run_project(
    brief: str,
    working_directory: str,
    project_id: str | None = None,
    checkpointer: Any = None,
    quiet: bool = False,
    interactive: bool = False,
    auto_approve_policies: list[dict] | None = None,
    event_log_dir: str | None = None,
    macro: str = "",
    project: str = "",
) -> dict[str, Any]:
    """Run a complete project through the graph.

    This is the main entry point. It:
    1. Initializes the event bus for real-time visibility
    2. Builds the graph
    3. Creates initial state from the brief
    4. Streams execution, handling interrupts
    5. Writes session logs for every node execution
    6. Extracts knowledge events (G7) and crystallization signals (G8)

    Args:
        brief: What the human wants built (natural language).
        working_directory: Filesystem path for the project.
        project_id: Unique run ID. Auto-generated if not provided.
        checkpointer: LangGraph checkpointer. None = MemorySaver.
        quiet: Suppress console event output.
        interactive: If True, use terminal input() for interrupts (Tier 1
            debug mode). If False, use agent-first resolution via
            interrupt_resolver.py (production mode).
        auto_approve_policies: Standing policies for agent-resolved mode.
            Each policy is a dict with authority_type, sub_type, action,
            rationale. Matching interrupts are resolved without LLM calls.
        event_log_dir: Directory for JSONL event logs. If provided, events
            are written here (e.g., project events folder). If None, defaults
            to system/runtime/event_logs/.

    Returns:
        Final graph state after completion.
    """
    from pathlib import Path
    from langgraph.types import Command
    from .config import CORPOREAL_ROOT
    from .events import init_event_bus, emit, PROJECT_STARTED, PROJECT_COMPLETED, PROJECT_FAILED
    from .planning import load_planning_state_seed

    graph = build_graph(checkpointer=checkpointer)
    project_id = project_id or f"PRJ-{uuid.uuid4().hex[:8]}"

    # --- Initialize event bus ---
    log_dir = Path(event_log_dir) if event_log_dir else CORPOREAL_ROOT / "system" / "runtime" / "event_logs"
    bus = init_event_bus(
        project_id=project_id,
        log_dir=log_dir,
        console=True,
        quiet=quiet,
    )

    config = {"configurable": {"thread_id": project_id}}

    # --- Checkpoint working_directory migration ---
    # When resuming from a checkpoint, the stored working_directory may be
    # stale (e.g., /corporeal from a pre-worktree run). The caller (run.py)
    # always passes the correct current worktree path. Force-update the
    # checkpoint so downstream nodes use the right cwd.
    try:
        _existing = graph.get_state(config)
        if _existing and _existing.values and _existing.values.get("working_directory"):
            _stored_wd = _existing.values["working_directory"]
            if _stored_wd != working_directory:
                import sys as _sys
                print(
                    f"[WORKTREE] Migrating checkpoint working_directory: "
                    f"{_stored_wd} -> {working_directory}",
                    file=_sys.stderr,
                )
                graph.update_state(config, {"working_directory": working_directory})
    except Exception:
        pass  # No checkpoint yet — first run

    # --- Derive domain from working_directory path ---
    _domain = ""
    _wd = Path(working_directory)
    for _parent in [_wd] + list(_wd.parents):
        if _parent.name in ("ontology", "system", "application") and _parent.parent == CORPOREAL_ROOT:
            _domain = _parent.name
            break

    cached_planning_seed = load_planning_state_seed(CORPOREAL_ROOT, working_directory)

    initial_state = {
        "project_brief": brief,
        "project_id": project_id,
        "working_directory": working_directory,
        "macro": macro,
        "project": project,
        "domain": _domain,
        "design_spec": "",
        "design_spec_structured": {},
        "design_approved": False,
        "task_orders": [],
        "deliverables": [],
        "discoveries": [],
        "activations": [],
        "evaluations": [],
        "audit_trail": [],
        "escalations": [],
        "messages": [],
        "validation_results": [],
        "validation_overrides": [],
        "interrupt_resolutions": [],
        # Planning pipeline (R0)
        "structural_inventory": {},
        "structural_inventory_receipt": {},
        "planning_cache_status": {},
        "nesting_tree": {},
        "atomic_units": [],
        "process_inventory": [],
        "governance_hierarchy": {},
        "dependency_graph": {},
        "border_registry": {},
        "execution_order_projection": {},
        "integration_plan": {},
        "planning_graph_receipt": {},
        "critical_path": [],
        "wave_preconditions": {},
        "condition_checks": [],
        "dispatch_plan": [],
        "current_dispatch_level": 0,
        "level_outcomes": [],
        "integration_verdict": "",
        "integration_hollow_passes": [],
        "decomposition_attempts": 1,
        "current_phase": "design",
        "error": "",
    }
    initial_state.update({
        key: value for key, value in cached_planning_seed.items()
        if key in initial_state and key not in {"project_brief", "project_id", "working_directory", "macro", "project", "domain"}
    })

    emit(PROJECT_STARTED, phase="design", detail={
        "brief": brief[:200],
        "working_directory": working_directory,
        "summary": f"Starting project: {brief[:60]}",
    })

    if interactive:
        result = _stream_with_interrupts(graph, initial_state, config)
    else:
        from .interrupt_resolver import stream_with_agent_resolution
        result = stream_with_agent_resolution(
            graph, initial_state, config,
            auto_approve_policies=auto_approve_policies or [],
        )

    # --- G7: Extract knowledge events from completed state ---
    from .knowledge_feeder import extract_knowledge_events, summarize_knowledge_events
    knowledge_events = extract_knowledge_events(result, project_id=project_id)

    # --- G8: Crystallization assessment from knowledge events ---
    from .crystallization_engine import assess_crystallization, summarize_crystallization
    crystallization = assess_crystallization(knowledge_events, result, project_id=project_id)

    # --- G8b: Crystallization executor (dry run for proposals) ---
    if crystallization.has_structural_signals:
        from .crystallization_executor import execute_crystallization
        from dataclasses import asdict
        executor_result = execute_crystallization(
            assessment=crystallization,
            corporeal_root=CORPOREAL_ROOT,
            domain="system",
            dry_run=True,
        )
        result["_crystallization_proposals"] = [
            asdict(p) for p in executor_result.proposals
        ]
    else:
        result["_crystallization_proposals"] = []

    # --- Final status ---
    final_phase = result.get("current_phase", "unknown")
    error = result.get("error", "")

    if error:
        emit(PROJECT_FAILED, phase=final_phase, detail={
            "error": error,
            "summary": f"FAILED: {error[:80]}",
        })
        result["_run_status"] = "failed"
    else:
        emit(PROJECT_COMPLETED, phase=final_phase, detail={
            "deliverables": len(result.get("deliverables", [])),
            "activations": len(result.get("activations", [])),
            "escalations": len(result.get("escalations", [])),
            "knowledge_events": len(knowledge_events),
            "summary": summarize_knowledge_events(knowledge_events),
        })
        result["_run_status"] = "completed"

    result["_knowledge_events"] = knowledge_events
    result["_crystallization"] = crystallization
    result["_event_count"] = bus.event_count

    return result


def run_project_stream(
    brief: str,
    working_directory: str,
    project_id: str | None = None,
    checkpointer: Any = None,
    auto_approve_policies: list[dict] | None = None,
    event_log_dir: str | None = None,
    macro: str = "",
    project: str = "",
):
    """Streaming entry point — yields events as they happen.

    Same as run_project() but returns a generator that yields event dicts
    in real time. Consumers can iterate with:

        for event in run_project_stream(brief="...", ...):
            print(event["event_type"], event.get("detail", {}))

    This is the Claude Agent SDK pattern: async for message in query().
    No polling. No JSONL scraping. Events stream directly to the consumer.

    The generator yields every event the bus emits (node.started,
    node.completed, llm.iteration, llm.tool_call, interrupt.fired, etc.)
    and finally yields a {"event_type": "project.result", "result": state}
    event with the final state.
    """
    import queue
    import threading
    from pathlib import Path
    from .config import CORPOREAL_ROOT
    from .events import init_event_bus, emit, PROJECT_STARTED
    from .planning import load_planning_state_seed

    project_id = project_id or f"PRJ-{uuid.uuid4().hex[:8]}"

    # Event queue — bus subscriber pushes events, generator pops them
    event_queue: queue.Queue = queue.Queue()

    def _queue_subscriber(event: dict[str, Any]):
        event_queue.put(event)

    # Initialize event bus with the queue subscriber
    log_dir = Path(event_log_dir) if event_log_dir else CORPOREAL_ROOT / "system" / "runtime" / "event_logs"
    bus = init_event_bus(
        project_id=project_id,
        log_dir=log_dir,
        console=False,  # Consumer handles display
        quiet=True,
    )
    bus.subscribe(_queue_subscriber)

    # Derive domain
    _wd = Path(working_directory)
    _domain = ""
    for _parent in [_wd] + list(_wd.parents):
        if _parent.name in ("ontology", "system", "application") and _parent.parent == CORPOREAL_ROOT:
            _domain = _parent.name
            break

    cached_planning_seed = load_planning_state_seed(CORPOREAL_ROOT, working_directory)

    initial_state = {
        "project_brief": brief,
        "project_id": project_id,
        "working_directory": working_directory,
        "macro": macro,
        "project": project,
        "domain": _domain,
        "design_spec": "",
        "design_spec_structured": {},
        "design_approved": False,
        "task_orders": [],
        "deliverables": [],
        "discoveries": [],
        "activations": [],
        "evaluations": [],
        "audit_trail": [],
        "escalations": [],
        "messages": [],
        "validation_results": [],
        "validation_overrides": [],
        "interrupt_resolutions": [],
        # Planning pipeline (R0)
        "structural_inventory": {},
        "structural_inventory_receipt": {},
        "planning_cache_status": {},
        "nesting_tree": {},
        "atomic_units": [],
        "process_inventory": [],
        "governance_hierarchy": {},
        "dependency_graph": {},
        "border_registry": {},
        "execution_order_projection": {},
        "integration_plan": {},
        "planning_graph_receipt": {},
        "critical_path": [],
        "wave_preconditions": {},
        "condition_checks": [],
        "dispatch_plan": [],
        "current_dispatch_level": 0,
        "level_outcomes": [],
        "integration_verdict": "",
        "integration_hollow_passes": [],
        "decomposition_attempts": 1,
        "current_phase": "design",
        "error": "",
    }
    initial_state.update({
        key: value for key, value in cached_planning_seed.items()
        if key in initial_state and key not in {"project_brief", "project_id", "working_directory", "macro", "project", "domain"}
    })

    # Run the graph in a background thread
    final_result = {}
    run_error = []

    def _run():
        nonlocal final_result
        try:
            graph = build_graph(checkpointer=checkpointer)
            config = {"configurable": {"thread_id": project_id}}

            # Checkpoint working_directory migration (same as run_project)
            try:
                _existing = graph.get_state(config)
                if _existing and _existing.values and _existing.values.get("working_directory"):
                    _stored_wd = _existing.values["working_directory"]
                    if _stored_wd != working_directory:
                        import sys as _sys
                        print(
                            f"[WORKTREE] Migrating checkpoint working_directory: "
                            f"{_stored_wd} -> {working_directory}",
                            file=_sys.stderr,
                        )
                        graph.update_state(config, {"working_directory": working_directory})
            except Exception:
                pass

            from .interrupt_resolver import stream_with_agent_resolution
            final_result = stream_with_agent_resolution(
                graph, initial_state, config,
                auto_approve_policies=auto_approve_policies or [],
            )
        except Exception as e:
            run_error.append(e)
        finally:
            # Signal end of stream
            event_queue.put(None)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    # Yield events as they arrive
    while True:
        event = event_queue.get()
        if event is None:
            break
        yield event

    thread.join(timeout=5)

    if run_error:
        yield {
            "event_type": "project.error",
            "error": str(run_error[0]),
            "detail": {"error": str(run_error[0]), "summary": f"FATAL: {run_error[0]}"},
        }

    # Final result event
    yield {
        "event_type": "project.result",
        "result": final_result,
        "detail": {
            "deliverables": len(final_result.get("deliverables", [])),
            "error": final_result.get("error", ""),
            "summary": "Project complete" if not final_result.get("error") else f"Failed: {final_result['error'][:80]}",
        },
    }


def _stream_with_interrupts(graph, initial_state, config) -> dict:
    """Stream graph execution, prompting user at interrupt points.

    G4: Dispatches on authority_type from the standardized interrupt
    envelope. Each authority type has a specific handler that presents
    the right context and collects a resolution matching that type's
    schema.

    In Tier 1, all interrupts route to Principal (human). Tier 2 will
    add agent-level handlers where Operator/Coordinator/Architect
    resolve interrupts within their authority before escalating.
    """
    from langgraph.types import Command

    current_input = initial_state

    while True:
        last_state = None
        interrupted = False

        for event in graph.stream(current_input, config, stream_mode="values"):
            last_state = event

            if isinstance(event, dict) and event.get("__interrupt__"):
                interrupted = True
                break

        if not interrupted:
            return last_state or {}

        state_snapshot = graph.get_state(config)
        if not state_snapshot.tasks:
            return last_state or {}

        for task in state_snapshot.tasks:
            if hasattr(task, "interrupts") and task.interrupts:
                interrupt_data = task.interrupts[0].value

                authority = interrupt_data.get("authority_type", "unknown")
                sub_type = interrupt_data.get("sub_type", "")
                tier = interrupt_data.get("tier", "?")
                holder = interrupt_data.get("holder", "unknown")
                ctx = interrupt_data.get("context", {})

                # Emit interrupt event
                from .events import emit, INTERRUPT_FIRED, INTERRUPT_RESUMED
                emit(INTERRUPT_FIRED, node=holder, detail={
                    "authority_type": authority,
                    "sub_type": sub_type,
                    "tier": tier,
                    "message": interrupt_data.get("message", ""),
                    "summary": f"{authority}/{sub_type}",
                })

                print(f"\n--- INTERRUPT [{authority}/{sub_type}] tier={tier} holder={holder} ---")
                print(f"Message: {interrupt_data.get('message', '')}")
                print(f"Options: {interrupt_data.get('resolution_options', [])}")

                # --- Design authority (Tier 3) ---
                if authority == "design" and sub_type == "spec_approval":
                    print(f"\n{'_'*40}")
                    print("DESIGN SPEC:")
                    print(ctx.get("design_spec", "")[:2000])
                    print(f"{'_'*40}")
                    answer = input("\nApprove this design? [y/n]: ").strip().lower()
                    decision = {"approved": answer in ("y", "yes")}

                # --- Execution authority (Tier 2) ---
                elif authority == "execution" and sub_type == "activation_scope":
                    print("\nREQUIRES PRINCIPAL:")
                    for r in ctx.get("requires_principal", []):
                        print(f"  - {r.get('task_order_id')}: {r.get('reason')}")
                    if ctx.get("auto_dispatchable"):
                        print("AUTO-DISPATCHABLE (within scope):")
                        for a in ctx["auto_dispatchable"]:
                            print(f"  - {a.get('task_order_id')}: {a.get('identity')}")
                    answer = input("\nApprove all? [y/n]: ").strip().lower()
                    if answer in ("y", "yes"):
                        approved = [
                            r["identity"]
                            for r in ctx.get("requires_principal", [])
                        ]
                        decision = {"approved_agents": approved}
                    else:
                        decision = {"approved_agents": [], "rejected": True}

                elif authority == "execution" and sub_type == "decomposition_overlap":
                    print("\nOVERLAPPING DELIVERABLES:")
                    for path, orders in ctx.get("overlaps", {}).items():
                        print(f"  '{path}' claimed by: {', '.join(orders)}")
                    answer = input("\nForce dispatch anyway? [y/n]: ").strip().lower()
                    if answer in ("y", "yes"):
                        decision = {"force_dispatch": True}
                    else:
                        decision = {"rejected": True}

                # --- Validation authority: boundary failures ---
                elif authority == "validation" and sub_type == "boundary_failure":
                    print(f"\nBOUNDARY VALIDATION FAILURES ({ctx.get('fail_count', '?')}):")
                    for f in ctx.get("failures", []):
                        print(f"  {f.get('deliverable_id', '?')} at {f.get('boundary', '?')}:")
                        for c in f.get("failures", []):
                            print(f"    - [{c.get('condition_id')}] {c.get('detail', '')}")
                    print("\nOptions: accept (override), rework, reject")
                    answer = input("Action [accept/rework/reject]: ").strip().lower()
                    if answer == "accept":
                        rationale = input("Rationale (required): ").strip()
                        risk = input("Downstream risk [low/medium/high]: ").strip().lower()
                        if risk not in ("low", "medium", "high"):
                            risk = "medium"
                        decision = {
                            "action": "accept",
                            "rationale": rationale or "No rationale provided",
                            "risk": risk,
                        }
                    elif answer == "rework":
                        decision = {"action": "rework"}
                    else:
                        decision = {"action": "reject"}

                # --- Validation authority: review quality failures ---
                elif authority == "validation" and sub_type == "review_failure":
                    print("\nQUALITY FAILURES:")
                    for f in ctx.get("failures", []):
                        print(f"  - {f.get('reason', 'unknown')}")
                    answer = input("\nAccept deliverables as-is? [y/n]: ").strip().lower()
                    decision = {"accepted": answer in ("y", "yes")}

                # --- Worker question (AskUserQuestion tool) ---
                elif authority == "execution" and sub_type == "worker_question":
                    print(f"\nWORKER QUESTION:")
                    print(f"  {ctx.get('question', interrupt_data.get('message', ''))}")
                    if ctx.get("why"):
                        print(f"  Context: {ctx['why']}")
                    opts = ctx.get("options", [])
                    if opts:
                        print(f"  Options:")
                        for i, opt in enumerate(opts, 1):
                            print(f"    {i}. {opt}")
                    answer = input("\nYour answer: ").strip()
                    # If they entered a number, map to option
                    if opts and answer.isdigit():
                        idx = int(answer) - 1
                        if 0 <= idx < len(opts):
                            answer = opts[idx]
                    decision = {"answer": answer}

                # --- Fallback for unrecognized authority types ---
                else:
                    print(f"\nUnrecognized authority: {authority}/{sub_type}")
                    answer = input("Resume value (JSON or text): ").strip()
                    try:
                        import json
                        decision = json.loads(answer)
                    except (json.JSONDecodeError, ValueError):
                        decision = answer

                emit(INTERRUPT_RESUMED, node=holder, detail={
                    "authority_type": authority,
                    "sub_type": sub_type,
                    "decision": str(decision)[:200],
                    "summary": f"resumed: {authority}/{sub_type}",
                })

                current_input = Command(resume=decision)
                break
        else:
            return last_state or {}
