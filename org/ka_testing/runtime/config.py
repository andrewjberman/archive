"""
Runtime configuration — LLM provider, checkpointer, agent registry.

This module wires the LangGraph graph to external dependencies:
- Which LLM to call at each node
- Where to persist checkpoints
- How to resolve agent identities from the registry
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

# Corporeal root — everything is relative to this
# Detection: walk up from this file until we find a directory named "corporeal"
# that contains system/, ontology/, and application/ subdirectories.
def _detect_corporeal_root() -> Path:
    """Detect corporeal/ root by walking up from this file."""
    search = Path(__file__).resolve().parent
    for _ in range(10):
        # Check if we ARE inside corporeal/ by looking for the sibling domains
        candidate = search
        while candidate.name and candidate.name != "corporeal":
            candidate = candidate.parent
        if (
            candidate.name == "corporeal"
            and (candidate / "system").is_dir()
            and (candidate / "ontology").is_dir()
        ):
            return candidate
        search = search.parent
    raise RuntimeError(
        "Could not detect corporeal/ root. Set CORPOREAL_ROOT env var."
    )


# KA Testing: hardcode corporeal root since this copy lives outside corporeal/
_KA_FALLBACK = Path(__file__).resolve().parent.parent.parent.parent / "vectordb" / "corporeal"
CORPOREAL_ROOT = Path(os.environ.get("CORPOREAL_ROOT", "")) if os.environ.get("CORPOREAL_ROOT") else (_KA_FALLBACK if _KA_FALLBACK.is_dir() else _detect_corporeal_root())

AGENTS_JSON = CORPOREAL_ROOT / "system" / "agents" / "registry" / "AGENTS.json"
CONTRACTS_DIR = CORPOREAL_ROOT / "ontology" / "contracts" / "boundaries"
TOOLS_DIR = CORPOREAL_ROOT / "system" / "os" / "cli"


# ---------------------------------------------------------------------------
# LLM provider selection
# ---------------------------------------------------------------------------

# HIERARCHY_LLM_PROVIDER: "anthropic" (default) or "openai"
# Controls which LLM backend is used for all invoke_llm() calls.
LLM_PROVIDER = os.environ.get("HIERARCHY_LLM_PROVIDER", "anthropic")

# ---------------------------------------------------------------------------
# LLM configuration
# ---------------------------------------------------------------------------

# Default model for all nodes. Override per-archetype if needed.
if LLM_PROVIDER == "openai":
    DEFAULT_MODEL = os.environ.get("HIERARCHY_MODEL", "gpt-4o")
else:
    DEFAULT_MODEL = os.environ.get("HIERARCHY_MODEL", "claude-sonnet-4-20250514")

# Archetype-specific overrides (optional).
# Reasoning-heavy archetypes (architect, coordinator) may want a stronger model.
ARCHETYPE_MODELS: dict[str, str] = {
    "architect": os.environ.get("HIERARCHY_ARCHITECT_MODEL", DEFAULT_MODEL),
    "coordinator": os.environ.get("HIERARCHY_COORDINATOR_MODEL", DEFAULT_MODEL),
    "transformer": DEFAULT_MODEL,
    "compositor": DEFAULT_MODEL,
    "supplier": DEFAULT_MODEL,
    "operator": DEFAULT_MODEL,
}


# ---------------------------------------------------------------------------
# Agent registry loader
# ---------------------------------------------------------------------------

def load_agent_registry() -> dict[str, Any]:
    """Load AGENTS.json and index by identity (provenance-encoded).

    Identity format: {DIV}-{MAC}-{PRJ}-{TIER}.{DEPTH}-{PREFIX}.{SCOPE}.{INSTANCE}
    Example: APP-DSSR-CREATE-SPAN.1-ARC.DSSR.1

    For exec agents (no macro/project): {DIV}-EXEC-{PREFIX}.{SCOPE}.{INSTANCE}
    Example: SYS-EXEC-CHF.SYS.1
    """
    with open(AGENTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {agent["identity"]: agent for agent in data["agents"]}


def resolve_agent(identity: str) -> dict[str, Any]:
    """Resolve a single agent record by provenance identity string."""
    registry = load_agent_registry()
    if identity not in registry:
        raise ValueError(f"Agent {identity} not found in registry")
    return registry[identity]


def load_agent_prompt(agent: dict[str, Any]) -> str:
    """Load an agent's system prompt from its folder.

    Resolution chain:
    1. {CORPOREAL_ROOT}/{domain_root}/{path}/prompt.md  (canonical)
    2. {CORPOREAL_ROOT}/{domain_root}/prompt.md          (legacy fallback)
    3. agent["mandate"] field                            (last resort)

    AGENTS.json provides:
      domain_root: "ontology" | "system" | "application"
      path: "agents/exec/CHF.ONT.1/"  (relative to domain root)
    """
    domain_root = agent.get("domain_root", "")
    agent_path = agent.get("path", "")

    # Canonical: domain_root/path/prompt.md
    if agent_path:
        prompt_path = CORPOREAL_ROOT / domain_root / agent_path / "prompt.md"
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")

    # Legacy fallback: domain_root/prompt.md
    fallback_path = CORPOREAL_ROOT / domain_root / "prompt.md"
    if fallback_path.exists():
        return fallback_path.read_text(encoding="utf-8")

    return agent.get("mandate", "You are an agent. Follow your task order.")


def resolve_agent_folder(agent: dict[str, Any]) -> Path:
    """Return the absolute path to an agent's folder.

    Used by session_logger to write logs to the correct location.
    """
    domain_root = agent.get("domain_root", "")
    agent_path = agent.get("path", "")
    return CORPOREAL_ROOT / domain_root / agent_path


def resolve_agent_by_serial(serial: str) -> dict[str, Any]:
    """Resolve a single agent record by serial (human-readable ID)."""
    registry = load_agent_registry()
    for agent in registry.values():
        if agent.get("serial") == serial:
            return agent
    raise ValueError(f"Agent with serial '{serial}' not found in registry")


# ---------------------------------------------------------------------------
# Boundary contract loader
# ---------------------------------------------------------------------------

def load_boundary_contracts() -> dict[str, dict[str, Any]]:
    """Load all boundary contract YAML files.

    Returns dict keyed by contract name (filename stem).
    Deferred: requires PyYAML. For Tier 1, contracts are loaded as
    raw text and validated structurally later.
    """
    contracts = {}
    if CONTRACTS_DIR.exists():
        for f in CONTRACTS_DIR.glob("*.yaml"):
            contracts[f.stem] = {"path": str(f), "raw": f.read_text(encoding="utf-8")}
    return contracts
