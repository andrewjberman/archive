"""
R7: Composition — Subgraph layer birth.

Enables fractal nesting: a worker node can be replaced by a full
value chain subgraph (architect → coordinator → workers → reviewer).
The parent graph doesn't know or care — same interface, deeper structure.

Interface contract: task order in, deliverable out.
State isolation: subordinate has own ProjectState.
Interrupt ceiling: subordinate SPAN pair resolves locally, sponsor is ceiling.

Ontology source:
  LAYER_PARTICIPATION.md Section 5 — layer birth, Interface Fixation
  FRACTAL_LAYERS.md — same topology at every depth
  CRYSTALLIZATION_PROTOCOL.md — what triggers layer birth
"""

from __future__ import annotations

from typing import Any, Callable

from .state import (
    AuditEntry, Deliverable, ProjectState,
)


def build_subordinate_graph(
    sponsor_agent: dict[str, Any],
    subordinate_registry_path: str | None = None,
    checkpointer: Any = None,
):
    """Build a subordinate graph for layer birth.

    Same topology as the parent graph:
        architect → coordinator → dispatch → workers → validator → reviewer

    Scoped to the subordinate layer:
    - Agents from subordinate registry (under sub_agents/)
    - Interrupt resolver uses sponsor as ceiling
    - Checkpointer is namespaced

    Args:
        sponsor_agent: The agent record that sponsors this layer.
        subordinate_registry_path: Path to subordinate AGENTS.json.
            If None, uses the sponsor's sub_agents/registry/.
        checkpointer: Checkpointer instance. None = MemorySaver.

    Returns:
        Compiled StateGraph with subordinate topology.
    """
    from pathlib import Path
    from .config import CORPOREAL_ROOT

    # Resolve subordinate registry
    if subordinate_registry_path:
        registry_path = Path(subordinate_registry_path)
    else:
        sponsor_path = sponsor_agent.get("path", "")
        domain_root = sponsor_agent.get("domain_root", "")
        registry_path = (
            CORPOREAL_ROOT / domain_root / sponsor_path
            / "sub_agents" / "registry" / "AGENTS.json"
        )

    # Load subordinate registry
    import json
    sub_registry = {}
    if registry_path.exists():
        sub_registry = json.loads(registry_path.read_text(encoding="utf-8"))

    # Build the graph with registry override — no global state mutation.
    # Thread-safe: each subordinate compilation is isolated.
    from .graph import build_graph as _build_parent_graph

    if checkpointer is None:
        from langgraph.checkpoint.memory import MemorySaver
        checkpointer = MemorySaver()

    graph = _build_parent_graph(
        checkpointer=checkpointer,
        registry_override=sub_registry,
    )

    return graph


def make_subgraph_node(
    subordinate_graph,
    sponsor_identity: str,
    sponsor_serial: str = "",
) -> Callable:
    """Wrap a subordinate graph as a node in the parent graph.

    Interface contract (LAYER_PARTICIPATION Step 5 — Interface Fixation):
    - Receives: Send payload with task_order, working_directory, etc.
    - Returns: deliverables, audit_trail, messages
    - Parent doesn't know a full pipeline ran internally

    The subordinate graph runs its own:
    - Architect (produces design spec from task order objective)
    - Coordinator (decomposes into subordinate task orders)
    - Workers (execute subordinate tasks)
    - Validator + Reviewer (validate subordinate output)

    All internally. The parent sees one deliverable.
    """

    def subgraph_node(state: dict[str, Any]) -> dict[str, Any]:
        from datetime import datetime, timezone
        from .interrupt_resolver import stream_with_agent_resolution

        task_order = state["task_order"]
        now = datetime.now(timezone.utc).isoformat()

        # Convert Send payload to subordinate ProjectState
        subordinate_input = {
            "project_brief": task_order.objective,
            "project_id": f"{state.get('project_id', 'sub')}_{task_order.id}",
            "working_directory": state.get("working_directory", ""),
            "design_spec": "",
            "design_approved": False,
            "task_orders": [],
            "deliverables": [],
            "activations": [],
            "evaluations": [],
            "audit_trail": [],
            "escalations": [],
            "messages": [],
            "validation_results": [],
            "validation_overrides": [],
            "interrupt_resolutions": [],
            "dispatch_plan": [],
            "current_dispatch_level": 0,
            "level_outcomes": [],
            "current_phase": "design",
            "error": "",
            "scope_boundary": state.get("scope_boundary"),
        }

        config = {
            "configurable": {
                "thread_id": f"{task_order.id}_subordinate",
            }
        }

        # Run subordinate graph with sponsor as interrupt ceiling
        try:
            result = stream_with_agent_resolution(
                subordinate_graph,
                subordinate_input,
                config,
                auto_approve_policies=[],
                confidence_threshold=0.7,
                ceiling_identity=sponsor_identity,
            )
        except Exception as e:
            return {
                "deliverables": [],
                "audit_trail": [AuditEntry(
                    identity=sponsor_identity,
                    archetype="compositor",
                    action="subordinate_failed",
                    detail=f"Subordinate graph failed: {e}",
                    timestamp=now,
                )],
            }

        # Extract deliverables from subordinate result
        sub_deliverables = result.get("deliverables", [])
        sub_audit = result.get("audit_trail", [])
        sub_messages = result.get("messages", [])

        # Re-tag deliverables with parent task order ID
        tagged_deliverables = []
        for i, d in enumerate(sub_deliverables):
            tagged = Deliverable(
                id=f"{task_order.id}-D{i+1:03d}",
                task_order_id=task_order.id,
                identity=d.identity if hasattr(d, "identity") else sponsor_identity,
                archetype=d.archetype if hasattr(d, "archetype") else "compositor",
                content=d.content if hasattr(d, "content") else "",
                file_paths=d.file_paths if hasattr(d, "file_paths") else [],
                status="submitted",
            )
            tagged_deliverables.append(tagged)

        # If subordinate produced no deliverables, create a summary
        if not tagged_deliverables:
            tagged_deliverables = [Deliverable(
                id=f"{task_order.id}-D001",
                task_order_id=task_order.id,
                identity=sponsor_identity,
                archetype=state.get("archetype", "compositor"),
                content=f"Subordinate pipeline completed. {len(sub_audit)} audit entries.",
                file_paths=task_order.deliverables,
                status="submitted",
            )]

        # Prefix subordinate audit entries
        prefixed_audit = [
            AuditEntry(
                identity=a.identity if hasattr(a, "identity") else "",
                archetype=a.archetype if hasattr(a, "archetype") else "",
                action=f"sub:{a.action}" if hasattr(a, "action") else "sub:unknown",
                detail=a.detail if hasattr(a, "detail") else "",
                timestamp=a.timestamp if hasattr(a, "timestamp") else now,
            )
            for a in sub_audit
            if hasattr(a, "action")
        ]

        # Add summary entry
        prefixed_audit.append(AuditEntry(
            identity=sponsor_identity,
            archetype="compositor",
            action="subordinate_complete",
            detail=(
                f"Subordinate pipeline for {task_order.id}: "
                f"{len(sub_deliverables)} deliverables, "
                f"{len(sub_audit)} audit entries, "
                f"error={'yes: ' + result.get('error', '')[:50] if result.get('error') else 'none'}"
            ),
            timestamp=now,
        ))

        return {
            "deliverables": tagged_deliverables,
            "audit_trail": prefixed_audit,
            "messages": sub_messages,
        }

    subgraph_node.__name__ = f"subordinate_{sponsor_serial or sponsor_identity}"
    return subgraph_node


def detect_subordinate_layers(
    registry: dict[str, Any],
) -> list[dict[str, Any]]:
    """Detect agents in the registry that sponsor subordinate layers.

    A sponsor is identified by having:
    - subordinate_span_architect field set
    - subordinate_span_coordinator field set

    Returns list of sponsor agent records.
    """
    sponsors = []
    agents = registry.get("agents", [])

    # Handle both list and dict registry formats
    if isinstance(agents, list):
        agent_list = agents
    elif isinstance(agents, dict):
        agent_list = list(agents.values())
    else:
        return []

    for agent in agent_list:
        if (agent.get("subordinate_span_architect")
                and agent.get("subordinate_span_coordinator")):
            sponsors.append(agent)

    return sponsors
