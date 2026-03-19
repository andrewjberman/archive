"""
Ad: Adapt -- Differential Regression Testing (D-mode).

Compares current run output to the last known-good baseline and
classifies the delta. Catches regressions without understanding
content -- "did we get worse?" is cheaper than "is this correct?"

Zero API calls. Pure filesystem diff + classification rules.

Spec: ONT.CORE.KF_ACCELERATION Section 5.1
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from .. import ModuleOutput

BASELINE_DIR_NAME = ".baseline"


@dataclass
class DeltaEntry:
    """A single difference between baseline and current."""
    key: str                    # Object path or registry key
    delta_type: Literal["added", "removed", "mutated", "stable"]
    before: Any = None          # Value in baseline (None if added)
    after: Any = None           # Value in current (None if removed)
    detail: str = ""


@dataclass
class RegressionResult:
    """Overall regression assessment."""
    verdict: Literal["ACCEPT", "FLAG", "FAIL"]
    delta_class: Literal["ADDITION", "REMOVAL", "MUTATION", "STABLE", "REGRESSION"]
    total_baseline: int = 0
    total_current: int = 0
    added: int = 0
    removed: int = 0
    mutated: int = 0
    stable: int = 0
    deltas: list[DeltaEntry] = field(default_factory=list)
    detail: str = ""


def _load_json(path: Path) -> dict | list | None:
    """Safely load a JSON file."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _diff_registries(baseline: dict, current: dict) -> list[DeltaEntry]:
    """Diff two registry JSON structures (keyed by path or OOK key)."""
    deltas = []

    # Find the registry entries (look for "objects" or "registry" key)
    b_entries = {}
    c_entries = {}

    for data, target in [(baseline, b_entries), (current, c_entries)]:
        if isinstance(data, dict):
            # Try "registry" key (ook_registry.json)
            if "registry" in data and isinstance(data["registry"], dict):
                target.update(data["registry"])
            # Try "objects" key (object_inventory.json)
            elif "objects" in data and isinstance(data["objects"], list):
                for obj in data["objects"]:
                    key = obj.get("path", obj.get("ook_key", str(len(target))))
                    target[key] = obj
            else:
                target.update(data)

    all_keys = set(b_entries.keys()) | set(c_entries.keys())

    for key in sorted(all_keys):
        in_b = key in b_entries
        in_c = key in c_entries

        if in_b and not in_c:
            deltas.append(DeltaEntry(
                key=key, delta_type="removed",
                before=b_entries[key],
                detail="Present in baseline, missing in current",
            ))
        elif in_c and not in_b:
            deltas.append(DeltaEntry(
                key=key, delta_type="added",
                after=c_entries[key],
                detail="New in current run",
            ))
        elif in_b and in_c:
            b_val = b_entries[key]
            c_val = c_entries[key]
            # Compare classification fields if they exist
            b_class = _extract_classification(b_val)
            c_class = _extract_classification(c_val)
            if b_class and c_class and b_class != c_class:
                deltas.append(DeltaEntry(
                    key=key, delta_type="mutated",
                    before=b_class, after=c_class,
                    detail=f"Classification changed: {b_class} -> {c_class}",
                ))
            else:
                deltas.append(DeltaEntry(
                    key=key, delta_type="stable",
                ))

    return deltas


def _extract_classification(entry: Any) -> dict | None:
    """Extract classification fields from a registry entry."""
    if not isinstance(entry, dict):
        return None
    cl = entry.get("classification", {})
    if cl:
        return cl
    # Try flat fields
    lc = entry.get("lifecycle_role", "")
    bc = entry.get("behavior_class", "")
    gi = entry.get("governance_intent", "")
    if lc or bc or gi:
        return {"lifecycle_role": lc, "behavior_class": bc, "governance_intent": gi}
    return None


def run_differential(
    current_dir: Path,
    artifact_name: str = "ook_registry.json",
) -> RegressionResult:
    """Compare current output to baseline.

    Args:
        current_dir: Directory containing current run's artifacts
        artifact_name: Which artifact to diff (default: ook_registry.json)

    Returns:
        RegressionResult with verdict and delta details.
    """
    baseline_dir = current_dir / BASELINE_DIR_NAME
    current_file = current_dir / artifact_name
    baseline_file = baseline_dir / artifact_name

    # No baseline = first run
    if not baseline_dir.exists() or not baseline_file.exists():
        return RegressionResult(
            verdict="ACCEPT",
            delta_class="ADDITION",
            detail="No baseline found -- first run. All entries are new.",
        )

    if not current_file.exists():
        return RegressionResult(
            verdict="FAIL",
            delta_class="REGRESSION",
            detail=f"Current artifact {artifact_name} does not exist but baseline does.",
        )

    baseline_data = _load_json(baseline_file)
    current_data = _load_json(current_file)

    if baseline_data is None or current_data is None:
        return RegressionResult(
            verdict="FLAG",
            delta_class="MUTATION",
            detail="Could not parse baseline or current artifact as JSON.",
        )

    deltas = _diff_registries(baseline_data, current_data)

    added = sum(1 for d in deltas if d.delta_type == "added")
    removed = sum(1 for d in deltas if d.delta_type == "removed")
    mutated = sum(1 for d in deltas if d.delta_type == "mutated")
    stable = sum(1 for d in deltas if d.delta_type == "stable")
    total_b = removed + mutated + stable
    total_c = added + mutated + stable

    # Classify the delta
    if removed == 0 and mutated == 0:
        delta_class = "ADDITION" if added > 0 else "STABLE"
        verdict = "ACCEPT"
    elif removed > 5 or (total_b > 0 and removed / total_b > 0.10):
        delta_class = "REGRESSION"
        verdict = "FAIL"
    elif removed > 0:
        delta_class = "REMOVAL"
        verdict = "FLAG"
    elif mutated > 0:
        delta_class = "MUTATION"
        verdict = "FLAG"
    else:
        delta_class = "STABLE"
        verdict = "ACCEPT"

    return RegressionResult(
        verdict=verdict,
        delta_class=delta_class,
        total_baseline=total_b,
        total_current=total_c,
        added=added,
        removed=removed,
        mutated=mutated,
        stable=stable,
        deltas=[d for d in deltas if d.delta_type != "stable"],  # Only report changes
        detail=f"+{added} -{removed} ~{mutated} ={stable}",
    )


def update_baseline(current_dir: Path, artifact_names: list[str] | None = None) -> None:
    """Copy current artifacts to baseline after a successful run."""
    baseline_dir = current_dir / BASELINE_DIR_NAME
    baseline_dir.mkdir(parents=True, exist_ok=True)

    if artifact_names is None:
        artifact_names = ["ook_registry.json", "object_inventory.json", "classification_summary.md"]

    for name in artifact_names:
        src = current_dir / name
        dst = baseline_dir / name
        if src.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Run differential regression testing.

    Config:
        output_dir: str -- directory with current run artifacts
        artifact_name: str -- which artifact to diff (default: ook_registry.json)
        update_on_pass: bool -- update baseline if verdict is ACCEPT (default: True)
    """
    output_dir = Path(config.get("output_dir", "."))
    artifact = config.get("artifact_name", "ook_registry.json")
    update_on_pass = config.get("update_on_pass", True)

    result = run_differential(output_dir, artifact)

    if result.verdict == "ACCEPT" and update_on_pass:
        update_baseline(output_dir)

    return ModuleOutput(
        data=result,
        confident=[result] if result.verdict == "ACCEPT" else [],
        ambiguous=[result] if result.verdict != "ACCEPT" else [],
        mode="D",
        stage="Ad",
        stats={
            "verdict": result.verdict,
            "delta_class": result.delta_class,
            "added": result.added,
            "removed": result.removed,
            "mutated": result.mutated,
            "stable": result.stable,
            "detail": result.detail,
        },
    )
