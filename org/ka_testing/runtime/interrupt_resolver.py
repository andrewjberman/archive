"""
Interrupt Resolution — Agent-first dispatch.

Replaces _stream_with_interrupts() terminal handler.
Implements INTERRUPT_RESOLUTION.md Phase 1.

Resolution chain (from DECISION_AUTHORITY.md):
    Worker encounters issue
        -> Coordinator (execution/passage authority)
        -> Architect (design authority, MUST resolve)
        -> Principal (optional, never blocking)

Standing policies allow known interrupt types to be resolved
without LLM calls (Principal pre-emptive directives).

Ontology source:
  DECISION_AUTHORITY.md — authority types and routing
  PRINCIPAL.md — BC2 (underdetermined selection)
  LAYER_PARTICIPATION.md — SPAN governance chain
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

from .state import AuditEntry


# ---------------------------------------------------------------------------
# Resolution record (telemetry)
# ---------------------------------------------------------------------------

@dataclass
class InterruptResolution:
    """Structured record of every interrupt resolution.

    Accumulates in ProjectState for learning loop telemetry.
    Maps to INTERRUPT_RESOLUTION.md Section 5.
    """
    interrupt_id: str
    authority_type: str
    sub_type: str
    resolver_identity: str       # Who resolved: identity or "PRINCIPAL"
    resolver_serial: str
    resolver_archetype: str      # coordinator, architect, or principal
    action: str                  # The resolution action taken
    rationale: str               # Why this resolution
    confidence: float            # 0.0-1.0 self-assessed
    ambiguity_flag: bool         # True if BC2 underdetermination
    escalated_from: str | None   # Prior resolver if escalated
    principal_override: bool     # True if Principal overrode
    timestamp: str = ""


# ---------------------------------------------------------------------------
# Resolution routing
# ---------------------------------------------------------------------------

# Authority type -> first resolver archetype
# From INTERRUPT_RESOLUTION.md Section 3: routing rules
RESOLUTION_ROUTING = {
    "validation":  "coordinator",   # Tier 1 failures -> Coordinator first
    "passage":     "coordinator",   # Hold decisions -> Coordinator
    "execution":   "coordinator",   # Feasibility/scope -> Coordinator
    "design":      "architect",     # Structural decisions -> Architect
}

# Confidence threshold below which coordinator escalates to architect
CONFIDENCE_THRESHOLD = 0.7


def resolve_interrupt(
    interrupt_data: dict[str, Any],
    state: dict[str, Any],
    *,
    confidence_threshold: float = CONFIDENCE_THRESHOLD,
    auto_approve_policies: list[dict] | None = None,
    ceiling_identity: str | None = None,
) -> dict[str, Any]:
    """Resolve an interrupt through the SPAN governance chain.

    Resolution chain (INTERRUPT_RESOLUTION.md Section 2):
        Worker encounters issue
            -> Coordinator (execution authority)
            -> Architect (design authority, MUST resolve)
            -> Ceiling agent (sponsor, if subordinate layer)
            -> Principal (optional, never blocking)

    In subordinate layers, the ceiling_identity limits escalation.
    The subordinate SPAN pair resolves locally. If neither can resolve,
    the interrupt escalates to the ceiling (sponsor), not to Principal.

    Args:
        interrupt_data: The interrupt envelope from interrupt().
        state: Current ProjectState dict.
        confidence_threshold: Below this, coordinator escalates.
        auto_approve_policies: Standing policies from Principal.
        ceiling_identity: If set, escalation stops at this agent
            instead of routing to Principal. Used in subordinate layers
            where the sponsor acts as Principal.

    Returns:
        Resolution dict suitable for Command(resume=resolution).
    """
    authority_type = interrupt_data.get("authority_type", "unknown")
    sub_type = interrupt_data.get("sub_type", "")

    interrupt_id = f"INT-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc).isoformat()

    # --- Check standing policies first ---
    policy_resolution = _check_standing_policies(
        authority_type, sub_type, interrupt_data.get("context", {}),
        policies=auto_approve_policies or [],
    )
    if policy_resolution is not None:
        _record_resolution(state, InterruptResolution(
            interrupt_id=interrupt_id,
            authority_type=authority_type,
            sub_type=sub_type,
            resolver_identity="POLICY",
            resolver_serial="standing_policy",
            resolver_archetype="principal",
            action=policy_resolution.get("action", "approve"),
            rationale=policy_resolution.get("rationale", "Standing policy"),
            confidence=1.0,
            ambiguity_flag=False,
            escalated_from=None,
            principal_override=False,
            timestamp=now,
        ))
        return policy_resolution

    # --- Route to first resolver ---
    first_resolver = RESOLUTION_ROUTING.get(authority_type, "coordinator")

    if first_resolver == "coordinator":
        resolution = _resolve_via_coordinator(
            interrupt_data, state, interrupt_id,
        )

        # Check confidence -> escalate to architect if low
        if (
            resolution.get("confidence", 1.0) < confidence_threshold
            or resolution.get("escalate", False)
        ):
            architect_resolution = _resolve_via_architect(
                interrupt_data, state, interrupt_id,
                prior_resolution=resolution,
            )
            return architect_resolution

        return resolution

    elif first_resolver == "architect":
        return _resolve_via_architect(
            interrupt_data, state, interrupt_id,
        )

    # Fallback: auto-approve with low confidence
    _record_resolution(state, InterruptResolution(
        interrupt_id=interrupt_id,
        authority_type=authority_type,
        sub_type=sub_type,
        resolver_identity="SYSTEM",
        resolver_serial="fallback",
        resolver_archetype="system",
        action="approve",
        rationale=f"No resolver for authority_type={authority_type}",
        confidence=0.3,
        ambiguity_flag=True,
        escalated_from=None,
        principal_override=False,
        timestamp=now,
    ))
    return _default_approval(authority_type, sub_type)


# ---------------------------------------------------------------------------
# Coordinator resolution
# ---------------------------------------------------------------------------

def _resolve_via_coordinator(
    interrupt_data: dict[str, Any],
    state: dict[str, Any],
    interrupt_id: str,
) -> dict[str, Any]:
    """Invoke the governing Coordinator to resolve an interrupt.

    Ontology source: DECISION_AUTHORITY.md — execution authority,
    passage authority. The Coordinator governs both.
    """
    from .config import load_agent_registry, resolve_agent, ARCHETYPE_MODELS

    registry = load_agent_registry()
    coordinator_identity = None
    coordinator_serial = ""
    for identity_key, rec in registry.items():
        if (rec.get("archetype") == "coordinator"
                and rec.get("placement_tier") == "exec"):
            coordinator_identity = identity_key
            coordinator_serial = rec.get("serial", "")
            break

    if not coordinator_identity:
        return {
            "confidence": 0.0,
            "escalate": True,
            "rationale": "No coordinator agent registered",
        }

    # Load coordinator prompt
    agent_prompt = ""
    try:
        agent_data = resolve_agent(coordinator_identity)
        agent_prompt = _load_agent_prompt(agent_data)
    except Exception:
        pass

    resolution_prompt = _build_resolution_prompt(
        role="coordinator",
        interrupt_data=interrupt_data,
        state=state,
        agent_prompt=agent_prompt,
    )

    # Invoke LLM (uses existing invoke_llm, no tools)
    from .llm import invoke_llm
    model = ARCHETYPE_MODELS.get("coordinator", "claude-sonnet-4-20250514")
    llm_response = invoke_llm(
        system=(
            "You are the Coordinator resolving an interrupt. "
            "Respond with a JSON object containing: action, rationale, "
            "confidence (0.0-1.0), escalate (boolean), and any fields "
            "required by the resolution schema. Be decisive."
        ),
        user=resolution_prompt,
        model=model,
    )

    resolution = _parse_resolution(
        llm_response,
        interrupt_data=interrupt_data,
    )

    now = datetime.now(timezone.utc).isoformat()
    _record_resolution(state, InterruptResolution(
        interrupt_id=interrupt_id,
        authority_type=interrupt_data.get("authority_type", ""),
        sub_type=interrupt_data.get("sub_type", ""),
        resolver_identity=coordinator_identity,
        resolver_serial=coordinator_serial,
        resolver_archetype="coordinator",
        action=resolution.get("action", "unknown"),
        rationale=resolution.get("rationale", ""),
        confidence=resolution.get("confidence", 0.5),
        ambiguity_flag=resolution.get("ambiguity_flag", False),
        escalated_from=None,
        principal_override=False,
        timestamp=now,
    ))

    return resolution


# ---------------------------------------------------------------------------
# Architect resolution
# ---------------------------------------------------------------------------

def _resolve_via_architect(
    interrupt_data: dict[str, Any],
    state: dict[str, Any],
    interrupt_id: str,
    prior_resolution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Invoke the governing Architect to resolve an interrupt.

    The Architect MUST resolve. If the choice space is genuinely
    underdetermined (BC2 from PRINCIPAL.md), the Architect:
    1. Makes the best available call given current evidence
    2. Logs ambiguity as first-class output
    3. Flags confidence: low, ambiguity_flag: true
    """
    from .config import load_agent_registry, resolve_agent, ARCHETYPE_MODELS

    registry = load_agent_registry()
    architect_identity = None
    architect_serial = ""
    for identity_key, rec in registry.items():
        if (rec.get("archetype") == "architect"
                and rec.get("placement_tier") == "exec"):
            architect_identity = identity_key
            architect_serial = rec.get("serial", "")
            break

    if not architect_identity:
        return _default_approval(
            interrupt_data.get("authority_type", ""),
            interrupt_data.get("sub_type", ""),
        )

    agent_prompt = ""
    try:
        agent_data = resolve_agent(architect_identity)
        agent_prompt = _load_agent_prompt(agent_data)
    except Exception:
        pass

    resolution_prompt = _build_resolution_prompt(
        role="architect",
        interrupt_data=interrupt_data,
        state=state,
        agent_prompt=agent_prompt,
        prior_resolution=prior_resolution,
    )

    from .llm import invoke_llm
    model = ARCHETYPE_MODELS.get("architect", "claude-sonnet-4-20250514")

    system_msg = (
        "You are the Architect resolving an interrupt that the Coordinator "
        "could not resolve with sufficient confidence. You MUST resolve it. "
        "If the choice is genuinely underdetermined, make your best call "
        "and set ambiguity_flag: true. "
        "Respond with a JSON object containing: action, rationale, "
        "confidence (0.0-1.0), ambiguity_flag (boolean)."
    )
    if prior_resolution:
        system_msg += (
            f"\n\nThe Coordinator's prior resolution was: "
            f"action={prior_resolution.get('action')}, "
            f"confidence={prior_resolution.get('confidence')}, "
            f"rationale={prior_resolution.get('rationale')}. "
            f"You may confirm, override, or revise."
        )

    llm_response = invoke_llm(
        system=system_msg,
        user=resolution_prompt,
        model=model,
    )

    resolution = _parse_resolution(
        llm_response,
        interrupt_data=interrupt_data,
    )

    # Architect MUST resolve — if confidence is still low, flag ambiguity
    if resolution.get("confidence", 0.5) < 0.5:
        resolution["ambiguity_flag"] = True

    now = datetime.now(timezone.utc).isoformat()
    escalated_from = None
    if prior_resolution:
        escalated_from = prior_resolution.get("resolver_identity", "")

    _record_resolution(state, InterruptResolution(
        interrupt_id=interrupt_id,
        authority_type=interrupt_data.get("authority_type", ""),
        sub_type=interrupt_data.get("sub_type", ""),
        resolver_identity=architect_identity,
        resolver_serial=architect_serial,
        resolver_archetype="architect",
        action=resolution.get("action", "unknown"),
        rationale=resolution.get("rationale", ""),
        confidence=resolution.get("confidence", 0.5),
        ambiguity_flag=resolution.get("ambiguity_flag", False),
        escalated_from=escalated_from,
        principal_override=False,
        timestamp=now,
    ))

    return resolution


# ---------------------------------------------------------------------------
# Support functions
# ---------------------------------------------------------------------------

def _check_standing_policies(
    authority_type: str,
    sub_type: str,
    context: dict,
    policies: list[dict],
) -> dict | None:
    """Check if a standing policy resolves this interrupt.

    Standing policies are Principal pre-emptive directives that
    let the system resolve known interrupt types without LLM calls.
    """
    for policy in policies:
        if (policy.get("authority_type") == authority_type
                and policy.get("sub_type") == sub_type):
            return {
                "action": policy.get("action", "approve"),
                "rationale": policy.get("rationale", "Standing policy"),
                "confidence": 1.0,
                **_action_to_decision(
                    policy.get("action", "approve"),
                    authority_type, sub_type, context,
                ),
            }
    return None


def _default_approval(authority_type: str, sub_type: str) -> dict:
    """Produce a default approval resolution. Used only as fallback."""
    defaults = {
        ("design", "spec_approval"): {"approved": True},
        ("execution", "activation_scope"): {"approved_agents": []},
        ("execution", "decomposition_overlap"): {"force_dispatch": True},
        ("execution", "resource_grounding"): {"action": "proceed"},
        ("validation", "boundary_failure"): {
            "action": "accept",
            "rationale": "No resolver available — auto-accepting",
            "risk": "high",
        },
        ("validation", "review_failure"): {"accepted": True},
    }
    base = defaults.get((authority_type, sub_type), {"approved": True})
    base["confidence"] = 0.3
    base["ambiguity_flag"] = True
    return base


def _action_to_decision(
    action: str,
    authority_type: str,
    sub_type: str,
    context: dict,
) -> dict:
    """Convert an action string to the decision format expected
    by each interrupt's resume handler."""
    if authority_type == "design" and sub_type == "spec_approval":
        return {"approved": action in ("approve", "accept")}

    if authority_type == "execution" and sub_type == "activation_scope":
        if action in ("approve", "accept"):
            agents = [
                r.get("identity", "")
                for r in context.get("requires_principal", [])
            ]
            return {"approved_agents": agents}
        return {"approved_agents": [], "rejected": True}

    if authority_type == "execution" and sub_type == "decomposition_overlap":
        return {"force_dispatch": action in ("approve", "force", "accept")}

    if authority_type == "execution" and sub_type == "resource_grounding":
        # Map resolver actions to gate outcomes
        if action in ("proceed", "approve", "accept"):
            return {"action": "proceed"}
        elif action == "phase_prep":
            return {"action": "phase_prep"}
        else:
            return {"action": "fail"}

    if authority_type == "validation" and sub_type == "boundary_failure":
        return {"action": action}

    if authority_type == "validation" and sub_type == "review_failure":
        return {"accepted": action in ("approve", "accept")}

    # Worker asking PRINCIPAL a clarifying question (AskUserQuestion tool)
    if authority_type == "execution" and sub_type == "worker_question":
        return {"answer": action}

    return {"approved": action in ("approve", "accept")}


def _build_resolution_prompt(
    role: str,
    interrupt_data: dict[str, Any],
    state: dict[str, Any],
    agent_prompt: str = "",
    prior_resolution: dict | None = None,
) -> str:
    """Build the prompt for the resolver agent's LLM call."""
    authority_type = interrupt_data.get("authority_type", "")
    sub_type = interrupt_data.get("sub_type", "")
    context = interrupt_data.get("context", {})
    options = interrupt_data.get("resolution_options", [])
    schema = interrupt_data.get("resolution_schema", {})

    parts = []

    if agent_prompt:
        parts.append(f"<agent_context>\n{agent_prompt}\n</agent_context>\n")

    parts.append(f"## Interrupt to Resolve\n")
    parts.append(f"**Authority type:** {authority_type}")
    parts.append(f"**Sub-type:** {sub_type}")
    parts.append(f"**Message:** {interrupt_data.get('message', '')}\n")

    parts.append(f"**Context:**\n```json\n{json.dumps(context, indent=2, default=str)}\n```\n")
    parts.append(f"**Resolution options:** {options}")

    if schema:
        parts.append(f"**Resolution schema:** {json.dumps(schema, indent=2)}")

    parts.append(f"\n**Project state:**\n{_summarize_state(state)}\n")

    if prior_resolution:
        parts.append(
            f"\n**Prior coordinator resolution (escalated to you):**\n"
            f"  Action: {prior_resolution.get('action')}\n"
            f"  Rationale: {prior_resolution.get('rationale')}\n"
            f"  Confidence: {prior_resolution.get('confidence')}\n"
        )

    parts.append(
        "\nRespond with a JSON object (wrapped in ```json``` fences)."
    )

    return "\n".join(parts)


def _parse_resolution(
    llm_response: str,
    interrupt_data: dict[str, Any],
) -> dict:
    """Parse the resolver agent's LLM response into a structured resolution."""
    authority_type = interrupt_data.get("authority_type", "")
    sub_type = interrupt_data.get("sub_type", "")
    context = interrupt_data.get("context", {})

    # Try to extract JSON from the response
    json_match = re.search(r'```json\s*(.*?)\s*```', llm_response, re.DOTALL)
    if not json_match:
        json_match = re.search(r'\{[^{}]*\}', llm_response, re.DOTALL)

    if json_match:
        try:
            text = json_match.group(1) if '```' in json_match.group() else json_match.group()
            parsed = json.loads(text)
            action = parsed.get("action", "approve")
            decision = _action_to_decision(action, authority_type, sub_type, context)
            parsed.update(decision)
            return parsed
        except json.JSONDecodeError:
            pass

    # Fallback: approve with low confidence
    result = _default_approval(authority_type, sub_type)
    result["rationale"] = f"Could not parse LLM response: {llm_response[:200]}"
    result["confidence"] = 0.3
    return result


def _load_agent_prompt(agent_data: dict) -> str:
    """Load the agent's prompt.md file content."""
    from pathlib import Path
    from .config import CORPOREAL_ROOT

    agent_path = agent_data.get("path", "")
    domain_root = agent_data.get("domain_root", "")
    if not agent_path:
        return ""

    prompt_path = CORPOREAL_ROOT / domain_root / agent_path / "prompt.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return ""


def _summarize_state(state: dict) -> str:
    """Produce a concise summary of project state for the resolver."""
    lines = []
    lines.append(f"Project: {state.get('project_id', 'unknown')}")
    lines.append(f"Phase: {state.get('current_phase', 'unknown')}")
    lines.append(f"Task orders: {len(state.get('task_orders', []))}")
    lines.append(f"Deliverables: {len(state.get('deliverables', []))}")
    lines.append(f"Escalations: {len(state.get('escalations', []))}")

    plan = state.get("dispatch_plan", [])
    if plan:
        lines.append(f"Dispatch plan: {[len(level) for level in plan]}")

    return "\n".join(lines)


def _record_resolution(state: dict, resolution: InterruptResolution):
    """Append an InterruptResolution to state for telemetry."""
    if "interrupt_resolutions" not in state:
        state["interrupt_resolutions"] = []
    state["interrupt_resolutions"].append(resolution)


# ---------------------------------------------------------------------------
# Graph integration: the production execution loop
# ---------------------------------------------------------------------------

def stream_with_agent_resolution(
    graph,
    initial_state: dict,
    config: dict,
    *,
    auto_approve_policies: list[dict] | None = None,
    confidence_threshold: float = CONFIDENCE_THRESHOLD,
    ceiling_identity: str | None = None,
) -> dict:
    """Stream graph execution with agent-first interrupt resolution.

    Replaces _stream_with_interrupts(). No input(). No blocking.

    The loop:
    1. Stream graph until completion or interrupt
    2. On interrupt: resolve via SPAN governance chain
    3. Resume with resolution via Command(resume=decision)
    4. Repeat until graph completes

    In subordinate layers, ceiling_identity limits escalation — the
    subordinate SPAN pair resolves locally, and the sponsor is the
    ceiling (not Principal).

    InterruptResolution records are accumulated and attached to the
    final result as 'interrupt_resolutions' for telemetry.
    """
    from langgraph.types import Command
    from .events import emit, INTERRUPT_FIRED, INTERRUPT_RESUMED

    current_input = initial_state
    max_iterations = 20
    all_resolutions: list[InterruptResolution] = []

    for _ in range(max_iterations):
        last_state = None
        interrupted = False

        for event in graph.stream(current_input, config, stream_mode="values"):
            last_state = event
            if isinstance(event, dict) and event.get("__interrupt__"):
                interrupted = True
                break

        if not interrupted:
            result = last_state or {}
            result["interrupt_resolutions"] = all_resolutions
            return result

        state_snapshot = graph.get_state(config)
        if not state_snapshot.tasks:
            result = last_state or {}
            result["interrupt_resolutions"] = all_resolutions
            return result

        for task in state_snapshot.tasks:
            if hasattr(task, "interrupts") and task.interrupts:
                interrupt_data = task.interrupts[0].value

                authority = interrupt_data.get("authority_type", "unknown")
                sub_type = interrupt_data.get("sub_type", "")

                emit(INTERRUPT_FIRED, node=interrupt_data.get("holder", ""),
                     detail={
                         "authority_type": authority,
                         "sub_type": sub_type,
                         "tier": interrupt_data.get("tier", "?"),
                         "summary": f"{authority}/{sub_type}",
                     })

                # --- Agent-first resolution ---
                # Use a temporary state dict to capture resolutions
                temp_state = {"interrupt_resolutions": []}
                resolution = resolve_interrupt(
                    interrupt_data,
                    temp_state,
                    confidence_threshold=confidence_threshold,
                    auto_approve_policies=auto_approve_policies,
                    ceiling_identity=ceiling_identity,
                )

                # Collect resolutions from the temp state
                for r in temp_state.get("interrupt_resolutions", []):
                    all_resolutions.append(r)

                emit(INTERRUPT_RESUMED, node=interrupt_data.get("holder", ""),
                     detail={
                         "authority_type": authority,
                         "sub_type": sub_type,
                         "resolver": resolution.get("resolver_serial", "agent"),
                         "action": resolution.get("action", "unknown"),
                         "confidence": resolution.get("confidence", 0),
                         "summary": f"resolved: {authority}/{sub_type} "
                                    f"-> {resolution.get('action', '?')}",
                     })

                current_input = Command(resume=resolution)
                break
        else:
            result = last_state or {}
            result["interrupt_resolutions"] = all_resolutions
            return result

    import sys
    print("WARNING: Hit max iterations in agent resolution loop", file=sys.stderr)
    result = last_state or {}
    result["interrupt_resolutions"] = all_resolutions
    return result
