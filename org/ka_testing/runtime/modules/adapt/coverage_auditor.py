"""
Ad: Coverage Auditor (D-mode). Set difference: source vs output.

Finds: scanned but not classified, classified but not keyed,
keyed but not in registry.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any
from .. import ModuleOutput


def audit(source_paths: list[str], registry_paths: list[str]) -> dict[str, list[str]]:
    """Compare source file list against registry file list."""
    src = set(source_paths)
    reg = set(registry_paths)
    return {
        "missing_from_registry": sorted(src - reg),
        "in_registry_not_on_disk": sorted(reg - src),
        "covered": sorted(src & reg),
    }


def execute(inputs: dict, config: dict) -> ModuleOutput:
    gaps = audit(inputs.get("source_paths", []), inputs.get("registry_paths", []))
    missing = gaps["missing_from_registry"]
    phantom = gaps["in_registry_not_on_disk"]
    return ModuleOutput(
        data=gaps,
        confident=gaps["covered"],
        ambiguous=missing + phantom,
        mode="D", stage="Ad",
        stats={
            "source_count": len(inputs.get("source_paths", [])),
            "registry_count": len(inputs.get("registry_paths", [])),
            "missing": len(missing),
            "phantom": len(phantom),
            "coverage_pct": round(len(gaps["covered"]) / max(len(inputs.get("source_paths", [])), 1) * 100, 1),
        },
    )
