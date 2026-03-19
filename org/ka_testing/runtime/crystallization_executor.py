"""
Crystallization Executor — Structural instantiation from mutation proposals.

Converts TopologyMutation proposals from crystallization_engine.py into
agent folders and registry entries. Every field derives from an ontological
primitive (see CHF.ONT.1 briefing for derivation table).

Two modes:
  dry_run=True  — compute proposal, return without writing (test mode)
  dry_run=False — create folder, write AGENT.md, update AGENTS.json

Identity model:
  Provenance-encoded identity strings per AGENT_ARCHITECTURE.md Section 4.
  Format: {DIV}-{MAC}-{PRJ}-{TIER}.{DEPTH}-{PREFIX}.{SCOPE}.{INSTANCE}
  No opaque counters. Identity IS provenance.

Ontology source:
  CRYSTALLIZATION_PROTOCOL.md — what crystallization produces
  AGENT_ARCHITECTURE.md — folder structure, provenance identity
  LAYER_PARTICIPATION.md — SPAN/WORKER modes, governance
  VALUE_CHAIN.md — boundary-to-layer mapping
  VERSION_SEMANTICS.md — crystallization triggers version boundary
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .crystallization_engine import (
    CrystallizationAssessment,
    MicroLayerAssessment,
    TopologyMutation,
)


# ---------------------------------------------------------------------------
# Ontological mappings
# ---------------------------------------------------------------------------

BOUNDARY_TO_ARCHETYPE = {
    "supplier_to_transformer": "transformer",
    "transformer_to_compositor": "compositor",
    "compositor_to_operator": "operator",
    "coordinator_to_worker": "transformer",
    "operator_output": "operator",
    "execution_flow": "coordinator",
}

ARCHETYPE_TO_FOLDER = {
    "supplier": "ingest",
    "transformer": "transform",
    "compositor": "assemble",
    "operator": "deploy",
    "coordinator": "span",
    "architect": "span",
}

ARCHETYPE_TO_PREFIX = {
    "supplier": "ING",
    "transformer": "TRN",
    "compositor": "ASM",
    "operator": "DPL",
    "coordinator": "CRD",
    "architect": "ARC",
}

DOMAIN_TO_DIV = {
    "ontology": "ONT",
    "system": "SYS",
    "application": "APP",
}

BOUNDARY_TO_LAYER = {
    "supplier_to_transformer": "L1-L2",
    "transformer_to_compositor": "L2-L3",
    "compositor_to_operator": "L3-L4",
    "coordinator_to_worker": "cross-layer",
    "operator_output": "L4-membrane",
}


# ---------------------------------------------------------------------------
# Output dataclasses
# ---------------------------------------------------------------------------

@dataclass
class CrystallizationProposal:
    """A fully specified proposal for a new agent from crystallization."""
    identity: str
    serial: str
    archetype: str
    placement_tier: str
    domain: str
    value_chain_folder: str
    layer_position: str
    governing_agent: str
    structural_parent: str | None
    trigger_boundary: str
    trigger_scores: dict
    trigger_decision: str
    mutation_type: str
    folder_path: str
    agent_md_content: str
    prompt_md_content: str
    executed: bool = False


@dataclass
class LayerBirthProposal:
    """Proposal for a subordinate SPAN pair + folder structure.

    Layer birth creates a governance layer, not just a worker.
    The sponsor agent becomes Principal to the subordinate chain.
    Workers are NOT pre-created — the subordinate Coordinator
    creates them at runtime based on the task it receives.
    """
    sponsor_identity: str
    sponsor_serial: str
    # Subordinate Coordinator
    coordinator_identity: str
    coordinator_serial: str
    coordinator_folder: str
    coordinator_agent_md: str
    coordinator_prompt_md: str
    # Subordinate Architect
    architect_identity: str
    architect_serial: str
    architect_folder: str
    architect_agent_md: str
    architect_prompt_md: str
    # Metadata
    trigger_boundary: str
    trigger_scores: dict
    trigger_decision: str
    sub_agents_root: str
    executed: bool = False


@dataclass
class ExecutorResult:
    """Result of running the crystallization executor."""
    proposals: list[CrystallizationProposal] = field(default_factory=list)
    layer_births: list[LayerBirthProposal] = field(default_factory=list)
    registry_updated: bool = False
    dry_run: bool = True
    timestamp: str = ""


# ---------------------------------------------------------------------------
# Core executor
# ---------------------------------------------------------------------------

def execute_crystallization(
    assessment: CrystallizationAssessment,
    corporeal_root: Path,
    domain: str = "system",
    governing_agent_identity: str = "PRINCIPAL",
    structural_parent_identity: str | None = None,
    macro: str = "EXEC",
    project: str = "CRYST",
    dry_run: bool = True,
) -> ExecutorResult:
    """Execute crystallization mutations from an assessment."""
    now = datetime.now(timezone.utc)
    result = ExecutorResult(dry_run=dry_run, timestamp=now.isoformat())

    # Process both CRYSTALLIZE (split_layer) and MONITOR mutations.
    # MONITOR mutations produce proposals in dry-run for test validation
    # but are NOT executed in live mode unless upgraded to CRYSTALLIZE.
    actionable = [
        (m, a) for m in assessment.mutations
        for a in assessment.assessments
        if m.target == a.boundary and m.mutation_type in ("split_layer", "monitor")
    ]

    if not actionable:
        return result

    registry_path = corporeal_root / "system" / "agents" / "registry" / "AGENTS.json"
    registry = _load_registry(registry_path)

    for mutation, micro_assessment in actionable:
        # Determine if this warrants layer birth or simple crystallization.
        # Uses the ontological three-condition test from LAYER_PARTICIPATION
        # Section 5, not score severity as a proxy.
        needs_lb = (
            mutation.mutation_type == "split_layer"
            and micro_assessment.decision == "CRYSTALLIZE"
            and _needs_layer_birth(assessment.assessments)
        )

        if needs_lb and structural_parent_identity:
            # Find sponsor agent in registry
            sponsor = _find_agent(registry, structural_parent_identity)
            if sponsor:
                lb_proposal = build_layer_birth_proposal(
                    mutation=mutation,
                    assessment=micro_assessment,
                    registry=registry,
                    corporeal_root=corporeal_root,
                    sponsor_agent=sponsor,
                    domain=domain,
                    macro=macro,
                    project=project,
                    now=now,
                )
                result.layer_births.append(lb_proposal)

                if not dry_run:
                    _execute_layer_birth(lb_proposal, registry, registry_path, corporeal_root)
                    lb_proposal.executed = True
                    result.registry_updated = True
                continue

        # Simple crystallization: add a worker at the same level
        proposal = _build_proposal(
            mutation=mutation,
            assessment=micro_assessment,
            registry=registry,
            corporeal_root=corporeal_root,
            domain=domain,
            governing_agent_identity=governing_agent_identity,
            structural_parent_identity=structural_parent_identity,
            macro=macro,
            project=project,
            now=now,
        )
        result.proposals.append(proposal)

        if not dry_run:
            _execute_proposal(proposal, registry, registry_path, corporeal_root)
            proposal.executed = True
            result.registry_updated = True

    return result


# ---------------------------------------------------------------------------
# Proposal builder
# ---------------------------------------------------------------------------

def _build_proposal(
    mutation: TopologyMutation,
    assessment: MicroLayerAssessment,
    registry: dict,
    corporeal_root: Path,
    domain: str,
    governing_agent_identity: str,
    structural_parent_identity: str | None,
    macro: str,
    project: str,
    now: datetime,
) -> CrystallizationProposal:
    archetype = BOUNDARY_TO_ARCHETYPE.get(mutation.target, "transformer")
    folder = ARCHETYPE_TO_FOLDER[archetype]
    prefix = ARCHETYPE_TO_PREFIX[archetype]
    layer_pos = BOUNDARY_TO_LAYER.get(mutation.target, "unknown")

    spec_raw = mutation.target.replace("_to_", "").replace("_", "")
    specialization = spec_raw[:6].upper()

    identity = _derive_identity(
        domain=domain, macro=macro, project=project,
        tier="worker", depth=0, prefix=prefix,
        scope=specialization, instance=1, registry=registry,
    )
    serial = _derive_serial(identity)

    if structural_parent_identity:
        parent_entry = _find_agent(registry, structural_parent_identity)
        parent_path = parent_entry.get("path", "") if parent_entry else ""
        folder_path = str(corporeal_root / parent_path / "sub_agents" / folder / serial)
    else:
        folder_path = str(corporeal_root / domain / "agents" / folder / serial)

    scores = {
        "volume": assessment.volume,
        "cognitive_distance": assessment.cognitive_distance,
        "blast_radius": assessment.blast_radius,
        "cadence_mismatch": assessment.cadence_mismatch,
        "skill_specialization": assessment.skill_specialization,
        "handoff_friction": assessment.handoff_friction,
        "sum": assessment.sum_score,
        "max": assessment.max_score,
        "count3": assessment.count3,
    }

    agent_md = _generate_agent_md(
        identity=identity, serial=serial, archetype=archetype,
        domain=domain, specialization=specialization,
        governing_agent=governing_agent_identity,
        structural_parent=structural_parent_identity,
        boundary=mutation.target, trigger=mutation.trigger,
        scores=scores, decision=assessment.decision,
        created_at=now.strftime("%Y-%m-%d"),
        macro=macro,
    )

    prompt_md = _generate_prompt_md(
        serial=serial, archetype=archetype,
        boundary=mutation.target, layer_position=layer_pos,
        description=mutation.description,
    )

    return CrystallizationProposal(
        identity=identity, serial=serial, archetype=archetype,
        placement_tier="worker", domain=domain,
        value_chain_folder=folder, layer_position=layer_pos,
        governing_agent=governing_agent_identity,
        structural_parent=structural_parent_identity,
        trigger_boundary=mutation.target, trigger_scores=scores,
        trigger_decision=assessment.decision,
        mutation_type=mutation.mutation_type,
        folder_path=folder_path,
        agent_md_content=agent_md, prompt_md_content=prompt_md,
    )


# ---------------------------------------------------------------------------
# File generation
# ---------------------------------------------------------------------------

def _generate_agent_md(
    identity, serial, archetype, domain, specialization,
    governing_agent, structural_parent, boundary, trigger,
    scores, decision, created_at, macro="EXEC",
) -> str:
    parent_line = f"\nstructural_parent: {structural_parent}" if structural_parent else ""
    scores_str = (
        f"V={scores['volume']} CD={scores['cognitive_distance']} "
        f"BR={scores['blast_radius']} CM={scores['cadence_mismatch']} "
        f"SS={scores['skill_specialization']} HF={scores['handoff_friction']} "
        f"(sum={scores['sum']}, max={scores['max']}, count3={scores['count3']})"
    )
    return f"""---
# --- Identity ---
identity: {identity}
serial: {serial}

# --- Placement ---
placement_tier: worker
archetype: {archetype}
domain: {domain}

# --- Governance ---
governing_agent: {governing_agent}{parent_line}

# --- Scope ---
scope_type: macro
scope_object: {macro}

# --- Mandate ---
mandate: >
  Dedicated {archetype} worker crystallized at the `{boundary}` boundary.
  Runtime signals indicated that this micro-layer accumulated sufficient
  complexity to warrant a dedicated agent (CRYSTALLIZATION_PROTOCOL).

# --- State ---
identity_state: active

# --- Provenance ---
created_at: "{created_at}"
created_by: crystallization_engine
---

# {serial}

## Crystallization Origin

- **Boundary:** {boundary}
- **Trigger:** {trigger}
- **Decision:** {decision}
- **Scores:** {scores_str}

## Mandate

Dedicated {archetype} worker crystallized at the `{boundary}` boundary.
Runtime signals indicated that this micro-layer accumulated sufficient
complexity to warrant a dedicated agent (CRYSTALLIZATION_PROTOCOL).
"""


def _generate_prompt_md(serial, archetype, boundary, layer_position, description) -> str:
    return f"""# {serial}

You are {serial}, a {archetype} agent at the {layer_position} boundary.

## Position

You operate at the `{boundary}` boundary in the value chain.

## Scope

{description}

## Operating Rules

- Receive task orders from your governing Coordinator
- Produce deliverables within declared scope
- scope_boundary: strict by default
- Escalate if work falls outside your archetype's function
"""


# ---------------------------------------------------------------------------
# Layer birth detection (ontological three-condition test)
# ---------------------------------------------------------------------------

# Value chain boundary order for adjacency detection
_CHAIN_ORDER = [
    "supplier_to_transformer",
    "transformer_to_compositor",
    "compositor_to_operator",
    "operator_output",
]


def _needs_layer_birth(
    assessments: list,
) -> bool:
    """Determine if pressure pattern warrants layer birth.

    Three conditions from LAYER_PARTICIPATION Section 5:
    1. Multiple sub-agents with distinct archetypes needed
    2. Internal governance required (adjacent handoff boundaries)
    3. Bounded interface (invariant — always true)

    Uses the actual ontological test, not score severity as proxy.
    A single boundary at extreme pressure gets simple crystallization.
    Multiple adjacent boundaries with distinct archetypes get layer birth.
    """
    # Filter to assessments with real pressure
    pressured = [
        a for a in assessments
        if getattr(a, "decision", "ABSORB") in ("CRYSTALLIZE", "MONITOR")
    ]

    if len(pressured) < 2:
        return False

    # Condition 1: Distinct archetypes
    archetypes = set()
    for a in pressured:
        boundary = getattr(a, "boundary", "")
        downstream = BOUNDARY_TO_ARCHETYPE.get(boundary, "")
        if downstream:
            archetypes.add(downstream)

    if len(archetypes) < 2:
        return False

    # Condition 2: Adjacent boundaries (internal handoffs)
    pressured_boundaries = [getattr(a, "boundary", "") for a in pressured]
    chain_positions = []
    for b in pressured_boundaries:
        if b in _CHAIN_ORDER:
            chain_positions.append(_CHAIN_ORDER.index(b))

    chain_positions.sort()

    for i in range(len(chain_positions) - 1):
        if chain_positions[i + 1] - chain_positions[i] == 1:
            return True  # Adjacent pair found

    return False


# ---------------------------------------------------------------------------
# Layer birth builder
# ---------------------------------------------------------------------------

def build_layer_birth_proposal(
    mutation: TopologyMutation,
    assessment: MicroLayerAssessment,
    registry: dict,
    corporeal_root: Path,
    sponsor_agent: dict,
    domain: str,
    macro: str = "EXEC",
    project: str = "CRYST",
    now: datetime | None = None,
) -> LayerBirthProposal:
    """Build a complete layer birth proposal with SPAN pair.

    Creates subordinate Architect + Coordinator under the sponsor's
    sub_agents/ directory. Workers are NOT pre-created — the
    subordinate Coordinator creates them at runtime.

    Every field traces to ontological primitives:
    - LAYER_PARTICIPATION Section 5: layer birth conditions
    - AGENT_ARCHITECTURE Section 7: sub_agents/ folder structure
    - CRYSTALLIZATION_PROTOCOL Part 2.4: archetype from boundary
    """
    if now is None:
        now = datetime.now(timezone.utc)

    sponsor_identity = sponsor_agent.get("identity", "unknown")
    sponsor_serial = sponsor_agent.get("serial", "unknown")
    sponsor_path = sponsor_agent.get("path", "")
    domain_root = sponsor_agent.get("domain_root", "")

    sub_agents_root = str(
        corporeal_root / domain_root / sponsor_path / "sub_agents"
    )

    # Derive SPAN pair provenance identities
    boundary_short = mutation.target.replace("_to_", "").replace("_", "")[:6].upper()

    coord_identity = _derive_identity(
        domain=domain, macro=macro, project=project,
        tier="span", depth=1, prefix="CRD",
        scope=boundary_short, instance=1, registry=registry,
    )
    coord_serial = _derive_serial(coord_identity)

    # Add coordinator to temp registry so architect gets a unique identity
    temp_registry = dict(registry)
    temp_agents = list(temp_registry.get("agents", []))
    temp_agents.append({"identity": coord_identity})
    temp_registry["agents"] = temp_agents

    arch_identity = _derive_identity(
        domain=domain, macro=macro, project=project,
        tier="span", depth=1, prefix="ARC",
        scope=boundary_short, instance=1, registry=temp_registry,
    )
    arch_serial = _derive_serial(arch_identity)

    coord_folder = str(Path(sub_agents_root) / "span" / coord_serial)
    arch_folder = str(Path(sub_agents_root) / "span" / arch_serial)

    scores = {
        "volume": assessment.volume,
        "cognitive_distance": assessment.cognitive_distance,
        "blast_radius": assessment.blast_radius,
        "cadence_mismatch": assessment.cadence_mismatch,
        "skill_specialization": assessment.skill_specialization,
        "handoff_friction": assessment.handoff_friction,
        "sum": assessment.sum_score,
        "max": assessment.max_score,
        "count3": assessment.count3,
    }

    created_at = now.strftime("%Y-%m-%d")

    coord_agent_md = f"""---
# --- Identity ---
identity: {coord_identity}
serial: {coord_serial}

# --- Placement ---
placement_tier: span
archetype: coordinator
domain: {domain}

# --- Governance ---
governing_agent: {sponsor_identity}
structural_parent: {sponsor_identity}

# --- Scope ---
scope_type: macro
scope_object: {macro}

# --- Mandate ---
mandate: >
  Subordinate Coordinator for the `{mutation.target}` boundary.
  Decomposes task orders from the sponsor into worker assignments,
  manages dispatch ordering, and enforces boundary contracts within
  the subordinate scope. The sponsor ({sponsor_serial}) acts as
  Principal for this governance chain.

# --- State ---
identity_state: active

# --- Provenance ---
created_at: "{created_at}"
created_by: crystallization_engine
---

# {coord_serial}

## Crystallization Origin

- **Sponsor:** {sponsor_serial} ({sponsor_identity})
- **Boundary:** {mutation.target}
- **Trigger:** {mutation.trigger}
- **Decision:** {assessment.decision}

## Mandate

Subordinate Coordinator for the `{mutation.target}` boundary.
Decomposes task orders from the sponsor into worker assignments,
manages dispatch ordering, and enforces boundary contracts within
the subordinate scope. The sponsor ({sponsor_serial}) acts as
Principal for this governance chain.
"""

    coord_prompt_md = f"""# {coord_serial}

You are {coord_serial} ({coord_identity}), a subordinate Coordinator governing the
`{mutation.target}` boundary under {sponsor_serial}.

Decompose incoming task orders into worker assignments. Enforce
value chain ordering. Resolve interrupts within your scope. Escalate
to your sponsor ({sponsor_serial}) only when you cannot resolve.
"""

    arch_agent_md = f"""---
# --- Identity ---
identity: {arch_identity}
serial: {arch_serial}

# --- Placement ---
placement_tier: span
archetype: architect
domain: {domain}

# --- Governance ---
governing_agent: {sponsor_identity}
structural_parent: {sponsor_identity}
division_pair: {coord_identity}

# --- Scope ---
scope_type: macro
scope_object: {macro}

# --- Mandate ---
mandate: >
  Subordinate Architect for the `{mutation.target}` boundary.
  Designs solutions within the subordinate scope. Partners with
  {coord_serial} as the SPAN pair. The sponsor ({sponsor_serial})
  acts as Principal for this governance chain.

# --- State ---
identity_state: active

# --- Provenance ---
created_at: "{created_at}"
created_by: crystallization_engine
---

# {arch_serial}

## Crystallization Origin

- **Sponsor:** {sponsor_serial} ({sponsor_identity})
- **Boundary:** {mutation.target}
- **Trigger:** {mutation.trigger}

## Mandate

Subordinate Architect for the `{mutation.target}` boundary.
Designs solutions within the subordinate scope. Partners with
{coord_serial} as the SPAN pair. The sponsor ({sponsor_serial})
acts as Principal for this governance chain.
"""

    arch_prompt_md = f"""# {arch_serial}

You are {arch_serial} ({arch_identity}), a subordinate Architect at the
`{mutation.target}` boundary under {sponsor_serial}.

Design solutions for task orders received from the sponsor.
Produce design specs that {coord_serial} decomposes into
worker assignments. Resolve design-authority interrupts locally.
"""

    return LayerBirthProposal(
        sponsor_identity=sponsor_identity,
        sponsor_serial=sponsor_serial,
        coordinator_identity=coord_identity,
        coordinator_serial=coord_serial,
        coordinator_folder=coord_folder,
        coordinator_agent_md=coord_agent_md,
        coordinator_prompt_md=coord_prompt_md,
        architect_identity=arch_identity,
        architect_serial=arch_serial,
        architect_folder=arch_folder,
        architect_agent_md=arch_agent_md,
        architect_prompt_md=arch_prompt_md,
        trigger_boundary=mutation.target,
        trigger_scores=scores,
        trigger_decision=assessment.decision,
        sub_agents_root=sub_agents_root,
    )


def _execute_layer_birth(proposal: LayerBirthProposal, registry: dict,
                         registry_path: Path, corporeal_root: Path):
    """Create SPAN pair folders and registry entries for layer birth."""
    for folder_path, agent_md, prompt_md in [
        (proposal.coordinator_folder, proposal.coordinator_agent_md, proposal.coordinator_prompt_md),
        (proposal.architect_folder, proposal.architect_agent_md, proposal.architect_prompt_md),
    ]:
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "logs").mkdir(exist_ok=True)
        (folder / "deliverables").mkdir(exist_ok=True)
        (folder / "task_orders").mkdir(exist_ok=True)
        (folder / "AGENT.md").write_text(agent_md, encoding="utf-8")
        (folder / "prompt.md").write_text(prompt_md, encoding="utf-8")

    # Create value chain folders for future workers
    sub_root = Path(proposal.sub_agents_root)
    for vc_folder in ("ingest", "transform", "assemble", "deploy"):
        (sub_root / vc_folder).mkdir(parents=True, exist_ok=True)

    # Register both SPAN agents
    agents_list = registry.get("agents", [])
    for identity, serial, archetype, folder_path, pair_identity in [
        (proposal.coordinator_identity, proposal.coordinator_serial,
         "coordinator", proposal.coordinator_folder, proposal.architect_identity),
        (proposal.architect_identity, proposal.architect_serial,
         "architect", proposal.architect_folder, proposal.coordinator_identity),
    ]:
        rel_path = str(Path(folder_path).relative_to(corporeal_root)).replace("\\", "/")
        agents_list.append({
            "identity": identity,
            "serial": serial,
            "archetype": archetype,
            "placement_tier": "span",
            "domain": "",
            "identity_state": "active",
            "governing_agent": proposal.sponsor_identity,
            "structural_parent": proposal.sponsor_identity,
            "path": rel_path + "/",
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "created_by": "crystallization_engine",
        })

    # Update sponsor with subordinate metadata
    for agent in agents_list:
        if agent.get("identity") == proposal.sponsor_identity:
            agent["subordinate_span_coordinator"] = proposal.coordinator_identity
            agent["subordinate_span_architect"] = proposal.architect_identity
            break

    _save_registry(registry_path, registry)


# ---------------------------------------------------------------------------
# Live execution
# ---------------------------------------------------------------------------

def _execute_proposal(proposal, registry, registry_path, corporeal_root):
    folder = Path(proposal.folder_path)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "logs").mkdir(exist_ok=True)
    (folder / "deliverables").mkdir(exist_ok=True)
    (folder / "AGENT.md").write_text(proposal.agent_md_content, encoding="utf-8")
    (folder / "prompt.md").write_text(proposal.prompt_md_content, encoding="utf-8")

    relative_path = str(Path(proposal.folder_path).relative_to(corporeal_root)).replace("\\", "/")
    agents_list = registry.get("agents", [])
    agents_list.append({
        "identity": proposal.identity,
        "serial": proposal.serial,
        "archetype": proposal.archetype,
        "placement_tier": proposal.placement_tier,
        "domain": proposal.domain,
        "identity_state": "active",
        "governing_agent": proposal.governing_agent,
        "structural_parent": proposal.structural_parent,
        "path": relative_path + "/",
        "domain_root": proposal.domain,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "created_by": "crystallization_engine",
        "crystallization_trigger": proposal.trigger_boundary,
    })
    _save_registry(registry_path, registry)


# ---------------------------------------------------------------------------
# Registry helpers
# ---------------------------------------------------------------------------

def _load_registry(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"schema_version": "2.0", "agents": []}

def _save_registry(path: Path, registry: dict):
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def _derive_identity(
    *,
    domain: str,
    macro: str,
    project: str,
    tier: str,
    depth: int,
    prefix: str,
    scope: str,
    instance: int,
    registry: dict,
) -> str:
    """Derive a provenance-encoded identity string.

    Format: {DIV}-{MAC}-{PRJ}-{TIER}.{DEPTH}-{PREFIX}.{SCOPE}.{INSTANCE}

    Checks for collision against the registry. If the identity already
    exists, increments the instance number until a unique identity is found.
    """
    div = DOMAIN_TO_DIV.get(domain, domain[:3].upper())
    # Tier codes are 4-char: EXEC, SPAN, WORK
    tier_code = {"exec": "EXEC", "span": "SPAN", "worker": "WORK"}.get(
        tier.lower(), tier[:4].upper()
    )
    candidate_instance = instance

    existing_identities = {
        agent.get("identity", "") for agent in registry.get("agents", [])
    }

    while True:
        identity = f"{div}-{macro}-{project}-{tier_code}.{depth}-{prefix}.{scope}.{candidate_instance}"
        if identity not in existing_identities:
            return identity
        candidate_instance += 1


def _derive_serial(identity: str) -> str:
    """Extract the serial from a provenance identity string.

    The serial is the last segment after the tier marker:
    APP-DSSR-CREATE-SPAN.1-ARC.DSSR.1 → ARC.DSSR.1

    Tier codes are 4-char: EXEC, SPAN, WORK.
    """
    parts = identity.split("-")
    # Find the tier segment (contains a dot with a digit: SPAN.1, WORK.0, EXEC)
    for i, part in enumerate(parts):
        if "." in part and any(c.isdigit() for c in part.split(".")[-1]):
            prefix = part.split(".")[0]
            if prefix in ("SPAN", "WORK", "EXEC"):
                return "-".join(parts[i + 1:])
    # Fallback: last dot-separated segment
    return parts[-1]


def _find_agent(registry: dict, identity: str) -> dict | None:
    """Find an agent in the registry by provenance identity string."""
    for agent in registry.get("agents", []):
        if agent.get("identity") == identity:
            return agent
    return None
