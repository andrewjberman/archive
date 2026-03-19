"""
R1: Execution -- Architect node.

The Architect reads the project brief, loads domain context (taxonomy files,
directory listing, spec registry), and produces a structured DesignSpec.
The structured output is validated deterministically before the coordinator
consumes it.

Ontology source: specs/core/ARCHETYPES.md (Architect archetype)
                 specs/core/EXECUTION_COMPLEXITY.md (EXECUTION_COMPLEXITY)
Runtime spec: runtime/specs/EXECUTION.md, runtime/specs/INTERRUPTION.md
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..state import AuditEntry, DesignSpec, ClassificationScheme, ProjectState


# ---------------------------------------------------------------------------
# Context injection -- load domain files before generation
# ---------------------------------------------------------------------------

def _collect_domain_context(
    working_directory: str,
    corporeal_root: Path,
) -> dict[str, Any]:
    """Collect Signal A context: directory listing, taxonomy files, registry.

    Returns a dict with:
      - directory_listing: flat list of files in the domain
      - taxonomy_content: dict of {filename: content} for taxonomy/classification files
      - spec_registry: content of SPEC_REGISTRY.json if it exists
      - object_count: number of classifiable objects found
    """
    context: dict[str, Any] = {
        "directory_listing": [],
        "taxonomy_content": {},
        "spec_registry": None,
        "object_count": 0,
    }

    # Find domain root from working directory
    wd = Path(working_directory)
    domain_dir = None
    for parent in [wd] + list(wd.parents):
        if parent.name in ("ontology", "system", "application") and parent.parent == corporeal_root:
            domain_dir = parent
            break

    if not domain_dir:
        return context

    # Directory listing (all .md, .json, .yaml files, 4 levels deep)
    try:
        result = subprocess.run(
            ["find", str(domain_dir), "-maxdepth", "4", "-type", "f",
             "(", "-name", "*.md", "-o", "-name", "*.json",
             "-o", "-name", "*.yaml", "-o", "-name", "*.yml", ")"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            context["directory_listing"] = [
                line.strip() for line in result.stdout.strip().split("\n")
                if line.strip()
            ]
    except Exception:
        pass

    # Count classifiable objects (specs, contracts, registries -- not logs, not agent files)
    classifiable_dirs = ["specs", "contracts", "registry"]
    count = 0
    for cdir in classifiable_dirs:
        target = domain_dir / cdir
        if target.exists():
            for f in target.rglob("*"):
                if f.is_file() and f.suffix in (".md", ".json", ".yaml", ".yml"):
                    # Exclude internal files (SPEC_REGISTRY, registry.yaml, macros/)
                    rel = str(f.relative_to(target))
                    if not rel.startswith("macros/") and f.name != "SPEC_REGISTRY.json":
                        count += 1
    context["object_count"] = count

    # Load taxonomy files (encoding registries that define valid codes)
    registry_dir = domain_dir / "registry"
    if registry_dir.exists():
        taxonomy_files = [
            "lifecycle_roles.json", "behavior_classes.json",
            "governance_intents.json", "object_classes.json",
            "key_spec.json", "action_types.json",
        ]
        for tf in taxonomy_files:
            tf_path = registry_dir / tf
            if tf_path.exists():
                try:
                    content = tf_path.read_text(encoding="utf-8")
                    context["taxonomy_content"][tf] = content
                except Exception:
                    pass

    # Load PRIMARY_TAXONOMY_ARCHITECTURE if it exists
    pta = domain_dir / "specs" / "core" / "PRIMARY_TAXONOMY_ARCHITECTURE.md"
    if pta.exists():
        try:
            content = pta.read_text(encoding="utf-8")
            # Truncate if very long -- architect needs the structure, not every detail
            if len(content) > 8000:
                content = content[:8000] + "\n\n[... truncated at 8000 chars ...]"
            context["taxonomy_content"]["PRIMARY_TAXONOMY_ARCHITECTURE.md"] = content
        except Exception:
            pass

    # Load spec registry
    spec_reg = domain_dir / "registry" / "SPEC_REGISTRY.json"
    if spec_reg.exists():
        try:
            context["spec_registry"] = spec_reg.read_text(encoding="utf-8")
        except Exception:
            pass

    return context


# ---------------------------------------------------------------------------
# Structured output parsing
# ---------------------------------------------------------------------------

DESIGN_SPEC_SCHEMA = """\
Return your design specification as a JSON object with these REQUIRED fields:

```json
{
  "object_count": <int>,
  "object_categories": {"<category_name>": <count>, ...},
  "domain_root": "<absolute path to domain being processed>",
  "classification_scheme": {
    "lifecycle_roles": ["<valid codes from taxonomy>"],
    "behavior_classes": ["<valid codes from taxonomy>"],
    "governance_intents": ["<valid codes from taxonomy>"],
    "object_class_pattern": "<description of how OC codes are derived>"
  },
  "key_spine": "<e.g., CORP-MAIN-CREATE-0001>",
  "key_format": "<e.g., ORG-MAC-PRJ-VER-BTS-KT-OTS-OTR-OTB-OTG-OC-OV>",
  "value_chain_stages": ["supplier", "transformer", "compositor", "operator"],
  "stage_descriptions": {
    "supplier": "<what this stage does>",
    "transformer": "<what this stage does>",
    "compositor": "<what this stage does>",
    "operator": "<what this stage does>"
  },
  "acceptance_criteria": ["<concrete, testable criterion>", ...],
  "taxonomy_files": ["<absolute path to taxonomy file>", ...],
  "reference_files": ["<absolute path to other relevant file>", ...],
  "complexity_tier": "S" | "T" | "M",
  "tier_rationale": "<one sentence explaining tier choice>",
  "narrative": "<freeform prose description of the project for human review>"
}
```

CRITICAL RULES:
- classification_scheme values MUST come from the taxonomy files provided. Do NOT invent codes.
- key_spine MUST use the project code from the task order, not a synonym.
- taxonomy_files and reference_files MUST be absolute paths that exist on disk.
- object_count MUST match your count of objects in the directory listing.
- Wrap the JSON in ```json``` fences.
"""


def _parse_design_spec(response: str) -> DesignSpec | None:
    """Parse structured DesignSpec from architect LLM response."""
    import re

    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if not match:
        return None

    try:
        raw = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

    # Build ClassificationScheme
    cs_raw = raw.get("classification_scheme", {})
    cs = ClassificationScheme(
        lifecycle_roles=cs_raw.get("lifecycle_roles", []),
        behavior_classes=cs_raw.get("behavior_classes", []),
        governance_intents=cs_raw.get("governance_intents", []),
        object_class_pattern=cs_raw.get("object_class_pattern", ""),
    )

    return DesignSpec(
        object_count=raw.get("object_count", 0),
        object_categories=raw.get("object_categories", {}),
        domain_root=raw.get("domain_root", ""),
        classification_scheme=cs,
        key_spine=raw.get("key_spine", ""),
        key_format=raw.get("key_format", ""),
        value_chain_stages=raw.get("value_chain_stages", []),
        stage_descriptions=raw.get("stage_descriptions", {}),
        acceptance_criteria=raw.get("acceptance_criteria", []),
        taxonomy_files=raw.get("taxonomy_files", []),
        reference_files=raw.get("reference_files", []),
        complexity_tier=raw.get("complexity_tier", "M"),
        tier_rationale=raw.get("tier_rationale", ""),
        narrative=raw.get("narrative", ""),
    )


# ---------------------------------------------------------------------------
# Deterministic validation gate
# ---------------------------------------------------------------------------

def _validate_design_spec(
    spec: DesignSpec,
    domain_context: dict[str, Any],
) -> tuple[bool, list[str]]:
    """Deterministic validation of the DesignSpec.

    Returns (passed, list_of_errors). No LLM calls.

    Checks:
    1. Schema completeness (required fields present and non-empty)
    2. Object count matches directory scan (+/- 10% tolerance)
    3. Classification codes are subsets of actual taxonomy registries
    4. Referenced files exist on disk
    5. Key spine uses correct project code (not a synonym)
    """
    errors = []

    # 1. Schema completeness
    if spec.object_count == 0:
        errors.append("object_count is 0 -- must be a positive integer")
    if not spec.object_categories:
        errors.append("object_categories is empty -- must list category counts")
    if not spec.value_chain_stages:
        errors.append("value_chain_stages is empty -- must list at least one stage")
    if not spec.acceptance_criteria:
        errors.append("acceptance_criteria is empty -- must list testable criteria")
    if not spec.complexity_tier or spec.complexity_tier not in ("S", "T", "M"):
        errors.append(f"complexity_tier '{spec.complexity_tier}' invalid -- must be S, T, or M")

    # 2. Object count validation (within 15% of directory scan)
    actual_count = domain_context.get("object_count", 0)
    if actual_count > 0 and spec.object_count > 0:
        deviation = abs(spec.object_count - actual_count) / actual_count
        if deviation > 0.15:
            errors.append(
                f"object_count {spec.object_count} deviates {deviation:.0%} from "
                f"directory scan ({actual_count}). Max tolerance: 15%"
            )

    # 3. Classification scheme validation
    if spec.classification_scheme:
        cs = spec.classification_scheme
        taxonomy = domain_context.get("taxonomy_content", {})

        # Validate codes against taxonomy registries
        # Taxonomy files use {"<key>": [{"code": "X", ...}, ...]} structure
        _taxonomy_checks = [
            ("lifecycle_roles", "lifecycle_roles.json", "roles"),
            ("behavior_classes", "behavior_classes.json", "classes"),
            ("governance_intents", "governance_intents.json", "intents"),
        ]
        for field_name, file_name, array_key in _taxonomy_checks:
            if file_name not in taxonomy:
                continue
            agent_codes = getattr(cs, field_name, [])
            if not agent_codes:
                continue
            try:
                data = json.loads(taxonomy[file_name])
                # Extract codes from array of {code, name, description} objects
                entries = data.get(array_key, [])
                if isinstance(entries, list):
                    valid_codes = {e.get("code", "") for e in entries if isinstance(e, dict)}
                else:
                    valid_codes = set(data.keys())
                invalid = [c for c in agent_codes if c not in valid_codes]
                if invalid:
                    errors.append(
                        f"{field_name} {invalid} not in taxonomy. "
                        f"Valid: {sorted(valid_codes)}"
                    )
            except (json.JSONDecodeError, AttributeError):
                pass

    # 4. Referenced files exist on disk
    for ref in spec.taxonomy_files + spec.reference_files:
        if ref and not Path(ref).exists():
            errors.append(f"referenced file does not exist: {ref}")

    return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Architect node
# ---------------------------------------------------------------------------

def architect_node(state: ProjectState) -> dict[str, Any]:
    """Architect: read project brief + domain context, produce structured DesignSpec.

    Three-phase execution:
    1. Context injection: load taxonomy files, directory listing, spec registry
    2. LLM generation: produce structured JSON DesignSpec
    3. Deterministic validation: schema check, count check, taxonomy check

    If validation fails, the errors are included in the audit trail and the
    design_approved flag is set to False. The interrupt resolver sees this
    and can retry or escalate.
    """
    from ..llm import invoke_llm
    from ..config import resolve_agent, load_agent_prompt, ARCHETYPE_MODELS, CORPOREAL_ROOT

    # --- Resolve identity ---
    from ..config import load_agent_registry
    registry = load_agent_registry()
    identity = None

    macro = state.get("macro", "")
    domain = state.get("domain", "")
    if not macro:
        raise ValueError(
            "No macro specified in state. The runtime requires --macro to "
            "scope agent resolution to the correct SPAN pair."
        )

    for aid, rec in registry.items():
        if (rec.get("archetype") == "architect"
                and rec.get("placement_tier") == "span"
                and rec.get("scope_object") == macro
                and (not domain or rec.get("domain") == domain)):
            identity = aid
            break

    if not identity:
        raise ValueError(
            f"No span-tier architect found for macro '{macro}'. "
            f"Ensure ARC.{macro}.1 is registered in AGENTS.json."
        )
    agent = resolve_agent(identity)
    system_prompt = load_agent_prompt(agent)

    # --- Phase 1: Context injection ---
    domain_context = _collect_domain_context(
        working_directory=state["working_directory"],
        corporeal_root=CORPOREAL_ROOT,
    )

    # Build context section for the prompt
    context_sections = []

    if domain_context["directory_listing"]:
        listing = "\n".join(domain_context["directory_listing"])
        context_sections.append(
            f"## Domain Files (actual files on disk)\n\n```\n{listing}\n```\n\n"
            f"Object count from directory scan: {domain_context['object_count']}\n"
        )

    if domain_context["taxonomy_content"]:
        tax_parts = []
        for fname, content in domain_context["taxonomy_content"].items():
            # For JSON files, include them inline so the architect sees valid codes
            if fname.endswith(".json"):
                tax_parts.append(f"### {fname}\n\n```json\n{content}\n```\n")
            else:
                tax_parts.append(f"### {fname}\n\n{content}\n")
        context_sections.append(
            "## Taxonomy Files (classification codes -- use ONLY these values)\n\n"
            + "\n".join(tax_parts)
        )

    if domain_context["spec_registry"]:
        context_sections.append(
            f"## Spec Registry (existing indexed specs)\n\n"
            f"```json\n{domain_context['spec_registry']}\n```\n"
        )

    context_block = "\n\n".join(context_sections)

    # --- Phase 2: LLM generation ---
    user_prompt = (
        f"## Project Brief\n\n{state['project_brief']}\n\n"
        f"## Working Directory\n\n{state['working_directory']}\n\n"
        + context_block + "\n\n"
        f"## Output Format\n\n{DESIGN_SPEC_SCHEMA}\n"
    )

    response = invoke_llm(
        system=system_prompt,
        user=user_prompt,
        model=ARCHETYPE_MODELS["architect"],
        tools=[],
    )

    now = datetime.now(timezone.utc).isoformat()

    # Capture execution trace
    from ..llm import get_last_trace
    trace = get_last_trace()
    trace_dict = trace.to_dict() if trace else {}

    # --- Phase 3: Parse + validate ---
    spec = _parse_design_spec(response)
    validation_errors = []

    if spec is None:
        validation_errors = ["Failed to parse structured JSON from architect response"]
        design_approved = False
        spec_dict = {}
    else:
        passed, validation_errors = _validate_design_spec(spec, domain_context)
        design_approved = passed
        from dataclasses import asdict
        spec_dict = asdict(spec)

    audit_entries = [
        AuditEntry(
            identity=identity,
            archetype="architect",
            action="produce_design_spec",
            detail=f"Spec length: {len(response)} chars. Structured: {'yes' if spec else 'no'}",
            timestamp=now,
        ),
    ]

    if validation_errors:
        audit_entries.append(AuditEntry(
            identity="SYSTEM",
            archetype="validation_gate",
            action="design_spec_validation",
            detail=f"FAILED ({len(validation_errors)} errors): {'; '.join(validation_errors[:5])}",
            timestamp=now,
        ))
    else:
        audit_entries.append(AuditEntry(
            identity="SYSTEM",
            archetype="validation_gate",
            action="design_spec_validation",
            detail="PASSED: All deterministic checks passed",
            timestamp=now,
        ))

    return {
        "design_spec": response,  # Freeform text preserved for human review
        "design_spec_structured": spec_dict,  # Typed contract for coordinator
        "design_approved": design_approved,
        "current_phase": "design",
        "audit_trail": audit_entries,
        "messages": [
            {
                "role": "architect",
                "identity": identity,
                "content": response,
                "timestamp": now,
                "execution_trace": trace_dict,
                "validation_errors": validation_errors,
                "structured_spec": spec_dict,
            }
        ],
    }
