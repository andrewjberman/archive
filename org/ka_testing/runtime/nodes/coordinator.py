"""
R1: Execution + R5: Distribution -- Coordinator node.

The Coordinator reads the structured DesignSpec and decomposes it into
task orders. Tier-aware: Tier S produces deliverables directly (no workers),
Tier T collapses the value chain, Tier M uses the full pipeline.

Ontology source: specs/core/ARCHETYPES.md (Coordinator archetype)
                 specs/core/DECISION_AUTHORITY.md (execution authority)
                 specs/core/EXECUTION_COMPLEXITY.md (EXECUTION_COMPLEXITY tiers)
Runtime spec: runtime/specs/EXECUTION.md, runtime/specs/DISTRIBUTION.md
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from ..state import AuditEntry, Deliverable, TaskOrder, ProjectState


# ---------------------------------------------------------------------------
# Tier S: Single-shot -- coordinator produces deliverables directly
# ---------------------------------------------------------------------------

def _tier_s_prompt(spec: dict, working_dir: str, corporeal_root: str) -> str:
    """Build the Tier S prompt: coordinator produces all deliverables inline."""
    cs = spec.get("classification_scheme", {})

    return (
        f"## Project: Single-Shot Execution (Tier S)\n\n"
        f"You have been given a structured design spec. This project is classified\n"
        f"as Tier S (single-shot) because all context is available to produce the\n"
        f"deliverables directly. No workers will be dispatched.\n\n"
        f"## Design Spec\n\n"
        f"- Object count: {spec.get('object_count', 0)}\n"
        f"- Categories: {json.dumps(spec.get('object_categories', {}))}\n"
        f"- Domain root: {spec.get('domain_root', '')}\n"
        f"- Key spine: {spec.get('key_spine', '')}\n"
        f"- Key format: {spec.get('key_format', '')}\n\n"
        f"## Classification Scheme (MANDATORY -- use ONLY these codes)\n\n"
        f"- Lifecycle roles: {cs.get('lifecycle_roles', [])}\n"
        f"- Behavior classes: {cs.get('behavior_classes', [])}\n"
        f"- Governance intents: {cs.get('governance_intents', [])}\n"
        f"- Object class pattern: {cs.get('object_class_pattern', '')}\n\n"
        f"## Acceptance Criteria\n\n"
        + "\n".join(f"- {c}" for c in spec.get("acceptance_criteria", []))
        + f"\n\n"
        f"## Taxonomy Files (for reference)\n\n"
        + "\n".join(f"- {f}" for f in spec.get("taxonomy_files", []))
        + f"\n\n"
        f"## Working Directory: {working_dir}\n"
        f"## Corporeal Root: {corporeal_root}\n\n"
        f"## Instructions\n\n"
        f"Produce ALL deliverables as a JSON array of objects:\n\n"
        f"```json\n"
        f"[\n"
        f'  {{"path": "relative/to/working_dir/file.json", "content": "..."}},\n'
        f"  ...\n"
        f"]\n"
        f"```\n\n"
        f"CRITICAL RULES:\n"
        f"- Classification codes MUST come from the scheme above. Do NOT invent codes.\n"
        f"- Key spine MUST be exactly: {spec.get('key_spine', '')}\n"
        f"- Produce a complete inventory + OOK registry + validation report.\n"
        f"- If you realize you need information you don't have, return:\n"
        f'  {{"reclassify": "T", "reason": "..."}}\n\n'
        f"Wrap the JSON in ```json``` fences."
    )


def _handle_tier_s(
    state: ProjectState,
    spec: dict,
    identity: str,
    system_prompt: str,
    corporeal_root: str,
) -> dict[str, Any]:
    """Execute Tier S: coordinator produces deliverables directly."""
    from ..llm import invoke_llm
    from ..config import ARCHETYPE_MODELS

    prompt = _tier_s_prompt(spec, state["working_directory"], corporeal_root)

    response = invoke_llm(
        system=system_prompt,
        user=prompt,
        model=ARCHETYPE_MODELS["coordinator"],
        tools=[],
    )

    now = datetime.now(timezone.utc).isoformat()

    from ..llm import get_last_trace
    trace = get_last_trace()
    trace_dict = trace.to_dict() if trace else {}

    # Check for reclassification
    if '"reclassify"' in response:
        match = re.search(r'"reclassify"\s*:\s*"([TM])"', response)
        if match:
            new_tier = match.group(1)
            return {
                "current_phase": "planning",
                "audit_trail": [AuditEntry(
                    identity=identity, archetype="coordinator",
                    action="tier_reclassify",
                    detail=f"Reclassified from S to {new_tier}",
                    timestamp=now,
                )],
                "messages": [{"role": "coordinator", "identity": identity,
                             "content": response, "timestamp": now,
                             "execution_trace": trace_dict}],
                # Signal to re-enter coordinator with new tier
                "design_spec_structured": {**spec, "complexity_tier": new_tier},
            }

    # Parse deliverables and write to disk
    deliverables = _parse_tier_s_deliverables(response, state["project_id"], identity)
    _write_tier_s_files(deliverables, state["working_directory"])

    return {
        "deliverables": deliverables,
        "task_orders": [],  # No task orders in Tier S
        "current_phase": "review",  # Skip dispatch, go straight to reviewer
        "audit_trail": [AuditEntry(
            identity=identity, archetype="coordinator",
            action="tier_s_direct_production",
            detail=f"Tier S: produced {len(deliverables)} deliverables directly (0 workers)",
            timestamp=now,
        )],
        "messages": [{"role": "coordinator", "identity": identity,
                     "content": response, "timestamp": now,
                     "execution_trace": trace_dict}],
    }


def _write_tier_s_files(deliverables: list[Deliverable], working_dir: str) -> None:
    """Write Tier S deliverables to disk.

    Workers normally write files via tool calls. Tier S has no workers,
    so the coordinator writes inline content to the declared paths.
    """
    from pathlib import Path
    import sys

    wd = Path(working_dir)
    for d in deliverables:
        for fp in d.file_paths:
            target = wd / fp
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                target.write_text(d.content, encoding="utf-8")
                print(f"  [TIER S] Wrote: {target}", file=sys.stderr)
            except Exception as e:
                print(f"  [TIER S] WARN: Could not write {target}: {e}", file=sys.stderr)


def _parse_tier_s_deliverables(
    response: str,
    project_id: str,
    identity: str,
) -> list[Deliverable]:
    """Parse deliverables from Tier S coordinator response."""
    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if not match:
        return []

    try:
        raw = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []

    if not isinstance(raw, list):
        return []

    deliverables = []
    for i, item in enumerate(raw, 1):
        if not isinstance(item, dict) or "path" not in item:
            continue
        deliverables.append(Deliverable(
            id=f"{project_id}-S{i:03d}",
            task_order_id=f"{project_id}-TIER_S",
            identity=identity,
            archetype="coordinator",
            content=item.get("content", ""),
            file_paths=[item["path"]],
            status="submitted",
        ))

    return deliverables


# ---------------------------------------------------------------------------
# Tier T/M: Decompose into task orders
# ---------------------------------------------------------------------------

def _format_alignment_for_decomposition(assessment) -> str:
    """Format an AlignmentAssessment as enrichment text for the decomposition prompt.

    Injects resolved interface contracts, dependency graph, and gap list
    into the Coordinator's task order production context. This replaces
    PRD assumptions with ground-truth from Phase 2/3.
    """
    from ..alignment import AlignmentAssessment

    parts = ["## Alignment Assessment (from Worker state reports)\n"]

    if assessment.interfaces:
        parts.append("### Resolved Interfaces\n")
        for iface in assessment.interfaces:
            status_label = iface.status.upper()
            parts.append(
                f"- **{iface.producer}** -> **{iface.consumer}**: {status_label}\n"
                f"  Producer shape: {iface.producer_shape}\n"
                f"  Consumer shape: {iface.consumer_shape}\n"
            )
            if iface.resolution:
                parts.append(f"  RESOLVED: {iface.resolution}\n")
        parts.append("")

    if assessment.gaps:
        parts.append("### Gaps (PRD requirements nobody currently produces)\n")
        for gap in assessment.gaps:
            parts.append(f"- {gap}")
        parts.append("")

    if assessment.dependency_graph:
        parts.append("### Dependency Graph (from actual state, not PRD assumptions)\n")
        for dep in assessment.dependency_graph:
            parts.append(
                f"- {dep.producer} produces [{dep.artifact}] "
                f"-> consumed by {dep.consumer} "
                f"(required before: {dep.required_before})"
            )
        parts.append("")

    if assessment.conflicts:
        parts.append("### Resolved Conflicts\n")
        for conflict in assessment.conflicts:
            if conflict.resolution:
                parts.append(
                    f"- [{conflict.type}] {conflict.description}\n"
                    f"  DECISION: {conflict.resolution}"
                )
        parts.append("")

    parts.append(
        "IMPORTANT: Use the resolved interfaces above (not PRD assumptions) "
        "when writing interface contracts in task orders. Each task order "
        "should embed the specific field names, types, and paths from the "
        "alignment assessment.\n\n"
        "IMPORTANT: For each deliverable, classify as 'create' (file does not "
        "exist) or 'mutate' (file exists and needs targeted edits). Workers "
        "MUST use edit_file for mutations, not write_file. For mutations, "
        "specify exactly what to change (add lines, remove lines, replace "
        "specific sections). The state reports tell you what files exist.\n"
    )

    return "\n".join(parts)


def _build_decomposition_prompt(
    state: ProjectState,
    spec: dict,
    available_agents: list[dict],
    corporeal_root: str,
    fs_listing: str,
    alignment_context: str = "",
) -> str:
    """Build the coordinator prompt for Tier T and M decomposition."""
    cs = spec.get("classification_scheme", {})
    tier = spec.get("complexity_tier", "M")

    # Tier-specific instructions
    if tier == "T":
        tier_instructions = (
            "## Complexity: Tier T (Tool-Assisted)\n\n"
            "IMPORTANT: Minimize the number of workers. Maximum 3 workers.\n"
            "Collapse adjacent value chain stages into a single worker when the\n"
            "downstream stage's only input is the upstream stage's output.\n"
            "Prefer 1-2 workers over 3-4. Each worker gets max 20 tool iterations.\n\n"
            "For each worker, declare which value chain stages it covers:\n"
            '  "stages": ["supplier", "transformer"]  // collapsed\n\n'
        )
    else:
        tier_instructions = (
            "## Complexity: Tier M (Multi-Phase)\n\n"
            "Full value chain decomposition. Use as many workers as needed.\n"
            "Each worker gets max 25 tool iterations.\n\n"
        )

    # Build classification constraints from structured spec
    classification_block = ""
    if cs:
        classification_block = (
            f"## Classification Scheme (workers MUST use ONLY these codes)\n\n"
            f"- Lifecycle roles: {cs.get('lifecycle_roles', [])}\n"
            f"- Behavior classes: {cs.get('behavior_classes', [])}\n"
            f"- Governance intents: {cs.get('governance_intents', [])}\n"
            f"- Key spine: {spec.get('key_spine', '')} (EXACT -- do not substitute)\n"
            f"- Key format: {spec.get('key_format', '')}\n\n"
            f"Include these constraints in EVERY worker's requirements.\n"
            f"Workers that classify objects MUST use only codes from this list.\n\n"
        )

    # Structured spec summary (coordinator reads typed fields, not prose)
    spec_summary = (
        f"## Structured Design Spec\n\n"
        f"- Object count: {spec.get('object_count', 0)}\n"
        f"- Categories: {json.dumps(spec.get('object_categories', {}))}\n"
        f"- Domain root: {spec.get('domain_root', '')}\n"
        f"- Value chain stages: {spec.get('value_chain_stages', [])}\n"
        f"- Stage descriptions: {json.dumps(spec.get('stage_descriptions', {}), indent=2)}\n\n"
        f"## Acceptance Criteria\n\n"
        + "\n".join(f"- {c}" for c in spec.get("acceptance_criteria", []))
        + "\n\n"
    )

    # Narrative (freeform, for additional context)
    narrative = spec.get("narrative", "")
    narrative_block = f"## Design Narrative\n\n{narrative}\n\n" if narrative else ""

    # Alignment context (Phase 3 output, if alignment was run)
    alignment_block = f"\n{alignment_context}\n" if alignment_context else ""

    return (
        tier_instructions
        + spec_summary
        + classification_block
        + narrative_block
        + alignment_block
        + f"## Working Directory\n\n{state['working_directory']}\n\n"
        + f"## Corporeal Root\n\n{corporeal_root}\n\n"
        + (f"## Filesystem (actual files on disk)\n\n```\n{fs_listing}\n```\n\n"
           f"IMPORTANT: Only reference files from this listing in context_refs.\n"
           f"Do NOT invent file paths.\n\n"
           if fs_listing else "")
        + f"## Available Worker Agents\n\n"
        f"```json\n{json.dumps(available_agents, indent=2)}\n```\n\n"
        f"## Value Chain Ordering\n\n"
        f"  Supplier (L1: ingest) -> Transformer (L2: restructure/analyze) -> "
        f"Compositor (L3: assemble/integrate) -> Operator (L4: deploy/validate)\n\n"
        f"## Your Task\n\n"
        f"Decompose into concrete task orders. MINIMIZE the number of tasks.\n\n"
        f"### Minimum Viable Decomposition Rule\n"
        f"Each task split MUST be justified. If the input to task N+1 is exactly\n"
        f"the output of task N with no additional context needed, they MUST be one task.\n"
        f"For cataloging/classification projects: ingest+classify can be one task,\n"
        f"assemble+validate can be one task. Do NOT create 5 tasks when 2-3 suffice.\n\n"
        f"### For each task, provide:\n"
        f"1. **identity**: specific agent (by identity) or 'NEW'\n"
        f"2. **objective**: clear objective\n"
        f"3. **requirements**: specific requirements. INCLUDE classification constraints\n"
        f"   for any task that classifies objects.\n"
        f"4. **acceptance_criteria**: testable criteria\n"
        f"5. **deliverables**: array of objects, each with:\n"
        f"   - **path**: file path RELATIVE to the working directory\n"
        f"   - **action**: 'create' or 'mutate'\n"
        f"     - create: file does not exist yet. Worker uses write_file.\n"
        f"     - mutate: file already exists. Worker uses edit_file or apply_patch.\n"
        f"       For mutate, include **edit_instructions**: exactly what to change\n"
        f"       (which lines to add, remove, or replace). Do NOT tell the Worker\n"
        f"       to rewrite the entire file.\n"
        f"   This distinction is CRITICAL. write_file on an existing file destroys\n"
        f"   its content. Workers MUST use edit_file for existing files.\n"
        f"6. **dependencies**: task IDs this task depends on (T001, T002, etc)\n"
        f"7. **context_refs**: ABSOLUTE filesystem paths to files that EXIST NOW on disk.\n"
        f"   These are INPUT files the worker should read.\n"
        f"   context_refs and deliverables are DIFFERENT things:\n"
        f"   - context_refs = files that already exist (from the filesystem listing above)\n"
        f"   - deliverables = files the worker will CREATE or MUTATE\n"
        f"   - upstream outputs = go in the 'dependencies' array, NOT in context_refs\n"
        f"   Example: if T001 produces 'inventory.json' and T002 needs it,\n"
        f"   T002 lists T001 in dependencies, NOT 'inventory.json' in context_refs.\n"
        f"8. **deliverable_schema**: JSON schema constraining the output format.\n"
        f"   Derive enum constraints from the classification_scheme above.\n"
        f"   Example for a classifier task:\n"
        f"   {{"
        f'     "type": "object",'
        f'     "properties": {{'
        f'       "lifecycle_role": {{"type": "string", "enum": {json.dumps(cs.get("lifecycle_roles", []))}}},'
        f'       "behavior_class": {{"type": "string", "enum": {json.dumps(cs.get("behavior_classes", []))}}},'
        f'       "governance_intent": {{"type": "string", "enum": {json.dumps(cs.get("governance_intents", []))}}}'
        f"     }}"
        f"   }}\n"
        f"9. **split_justification**: one sentence explaining why this is a separate task\n"
        f"   (not merged with an adjacent task in the value chain)\n"
        f"10. **kf_budget**: iteration budget per Knowledge Function stage:\n"
        f"   {{\"Pe\": N, \"In\": N, \"Ac\": N, \"Ad\": N}}\n"
        f"   Pe = reading/discovering files. In = interpreting specific content.\n"
        f"   Ac = writing deliverables (MUST have budget >= 2). Ad = self-validating output.\n"
        f"   The worker's tools change per stage. In Ac, read tools are REMOVED.\n"
        f"   The worker MUST produce output during Ac — it cannot defer writing.\n"
        f"   If omitted, defaults are applied based on archetype.\n\n"
        f"Return as a JSON array with fields: identity, archetype, objective, "
        f"requirements (array), acceptance_criteria (array), deliverables (array), "
        f"dependencies (array), context_refs (array), deliverable_schema (object), "
        f"split_justification (string), kf_budget (object, optional)\n\n"
        f"Wrap the JSON in ```json``` fences."
    )


def _get_fs_listing(corporeal_root: str, working_dir: str) -> str:
    """Get filesystem listing for the domain root."""
    import subprocess
    from pathlib import Path

    try:
        wd = Path(working_dir)
        corp = Path(corporeal_root)
        domain_dir = None
        for parent in [wd] + list(wd.parents):
            if parent.name in ("ontology", "system", "application") and parent.parent == corp:
                domain_dir = str(parent)
                break
        if domain_dir:
            result = subprocess.run(
                ["find", domain_dir, "-maxdepth", "3", "-type", "f",
                 "(", "-name", "*.md", "-o", "-name", "*.json",
                 "-o", "-name", "*.yaml", ")"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                return result.stdout.strip()
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Main coordinator node
# ---------------------------------------------------------------------------

def coordinator_node(state: ProjectState) -> dict[str, Any]:
    """Coordinator: tier-aware decomposition.

    Reads design_spec_structured (typed contract from architect).
    Routes by complexity_tier:
      - Tier S: produce deliverables directly, skip workers
      - Tier T: collapsed value chain, max 3 workers
      - Tier M: full value chain decomposition
    """
    from ..llm import invoke_llm
    from ..config import (
        resolve_agent,
        load_agent_prompt,
        load_agent_registry,
        ARCHETYPE_MODELS,
        CORPOREAL_ROOT,
    )

    # --- Resolve identity ---
    registry = load_agent_registry()
    identity = None
    macro = state.get("macro", "")
    domain = state.get("domain", "")

    if not macro:
        raise ValueError("No macro specified in state.")

    for aid, rec in registry.items():
        if (rec.get("archetype") == "coordinator"
                and rec.get("placement_tier") == "span"
                and rec.get("scope_object") == macro
                and (not domain or rec.get("domain") == domain)):
            identity = aid
            break

    if not identity:
        raise ValueError(f"No span-tier coordinator for macro '{macro}'.")

    agent = resolve_agent(identity)
    system_prompt = load_agent_prompt(agent)
    corporeal_root_str = str(CORPOREAL_ROOT)

    # --- Read structured spec ---
    spec = state.get("design_spec_structured", {})
    tier = spec.get("complexity_tier", "M") if spec else "M"

    # --- Tier S: direct production ---
    if tier == "S" and spec:
        return _handle_tier_s(state, spec, identity, system_prompt, corporeal_root_str)

    # --- Tier T/M: decompose into task orders ---
    available_agents = []
    for aid, rec in registry.items():
        if rec.get("placement_tier") == "worker":
            available_agents.append({
                "identity": aid,
                "serial": rec.get("serial"),
                "archetype": rec.get("archetype"),
                "specialization": rec.get("specialization", ""),
                "mandate": rec.get("mandate", ""),
                "identity_state": rec.get("identity_state"),
            })

    # --- Alignment pass (ONT.CORE.ALIGNMENT v1) ---
    # Conditionally collect Worker state reports and synthesize alignment
    # assessment before producing task orders. Internal to Coordinator node.
    alignment_assessment_dict: dict = {}
    alignment_context = ""
    try:
        from ..alignment import alignment_pass, assessment_to_dict

        prd_section = spec.get("narrative", "") if spec else state.get("design_spec", "")
        assessment = alignment_pass(
            spec=spec or {},
            prd_section=prd_section,
            worker_roster=available_agents,
            coordinator_identity=identity,
            coordinator_prompt=system_prompt,
            working_directory=state.get("working_directory", ""),
        )

        if assessment is not None:
            alignment_assessment_dict = assessment_to_dict(assessment)
            # Build alignment context to enrich the decomposition prompt
            alignment_context = _format_alignment_for_decomposition(assessment)
    except Exception as e:
        # Alignment failure is non-fatal -- fall back to PRD-only task orders
        import sys
        print(f"  [ALIGNMENT] WARN: alignment_pass failed: {e}", file=sys.stderr)

    fs_listing = _get_fs_listing(corporeal_root_str, state.get("working_directory", ""))

    # Build prompt from structured spec (not freeform text)
    if spec:
        user_prompt = _build_decomposition_prompt(
            state, spec, available_agents, corporeal_root_str, fs_listing,
            alignment_context=alignment_context,
        )
    else:
        # Fallback: use freeform design_spec (backward compat)
        user_prompt = _build_fallback_prompt(
            state, available_agents, corporeal_root_str, fs_listing,
        )

    response = invoke_llm(
        system=system_prompt,
        user=user_prompt,
        model=ARCHETYPE_MODELS["coordinator"],
        tools=[],
    )

    task_orders = _parse_task_orders(response, state["project_id"])

    now = datetime.now(timezone.utc).isoformat()
    from ..llm import get_last_trace
    trace = get_last_trace()
    trace_dict = trace.to_dict() if trace else {}

    result = {
        "task_orders": task_orders,
        "current_phase": "planning",
        "audit_trail": [AuditEntry(
            identity=identity, archetype="coordinator",
            action="decompose_design",
            detail=f"Tier {tier}: produced {len(task_orders)} task orders"
                   + (f" (alignment: {len(alignment_assessment_dict.get('interfaces', []))} interfaces analyzed)"
                      if alignment_assessment_dict else " (no alignment)"),
            timestamp=now,
        )],
        "messages": [{"role": "coordinator", "identity": identity,
                     "content": response, "timestamp": now,
                     "execution_trace": trace_dict}],
    }

    if alignment_assessment_dict:
        result["alignment_assessment"] = alignment_assessment_dict

    return result


# ---------------------------------------------------------------------------
# Fallback prompt (backward compat -- no structured spec)
# ---------------------------------------------------------------------------

def _build_fallback_prompt(
    state: ProjectState,
    available_agents: list[dict],
    corporeal_root: str,
    fs_listing: str,
) -> str:
    """Build coordinator prompt from freeform design_spec (old path)."""
    return (
        f"## Approved Design Spec\n\n{state['design_spec']}\n\n"
        f"## Working Directory\n\n{state['working_directory']}\n\n"
        f"## Corporeal Root\n\n{corporeal_root}\n\n"
        + (f"## Filesystem\n\n```\n{fs_listing}\n```\n\n" if fs_listing else "")
        + f"## Available Worker Agents\n\n"
        f"```json\n{json.dumps(available_agents, indent=2)}\n```\n\n"
        f"## Your Task\n\n"
        f"Decompose this design spec into concrete task orders.\n"
        f"Return as a JSON array with fields: identity, archetype, objective, "
        f"requirements (array), acceptance_criteria (array), deliverables (array), "
        f"dependencies (array), context_refs (array)\n\n"
        f"Wrap the JSON in ```json``` fences."
    )


# ---------------------------------------------------------------------------
# Task order parsing (shared by Tier T and M)
# ---------------------------------------------------------------------------

def _parse_task_orders(response: str, project_id: str) -> list[TaskOrder]:
    """Extract structured task orders from coordinator LLM response."""
    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if not match:
        return [TaskOrder(
            id=f"{project_id}-T001", identity="NEW", archetype="transformer",
            objective="Execute the full design spec (coordinator parse failed)",
            requirements=["See design spec"],
            acceptance_criteria=["Design spec requirements met"],
        )]

    try:
        raw_tasks = json.loads(match.group(1))
    except json.JSONDecodeError:
        return [TaskOrder(
            id=f"{project_id}-T001", identity="NEW",
            objective="Execute the full design spec (JSON parse failed)",
            requirements=["See design spec"],
            acceptance_criteria=["Design spec requirements met"],
        )]

    task_orders = []
    for i, raw in enumerate(raw_tasks, 1):
        task_orders.append(TaskOrder(
            id=f"{project_id}-T{i:03d}",
            identity=raw.get("identity", "NEW"),
            archetype=raw.get("archetype", "transformer"),
            objective=raw.get("objective", ""),
            requirements=raw.get("requirements", []),
            acceptance_criteria=raw.get("acceptance_criteria", []),
            deliverables=raw.get("deliverables", []),
            dependencies=raw.get("dependencies", []),
            context_refs=raw.get("context_refs", []),
            deliverable_schema=raw.get("deliverable_schema", {}),
            split_justification=raw.get("split_justification", ""),
            kf_budget=raw.get("kf_budget", {}),
        ))

    return task_orders
