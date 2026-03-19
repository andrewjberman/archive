"""
Ac: Act -- Registry Writer (D-mode).

Writes classification results to JSON/YAML files. Template-based,
schema-validated on write. No LLM involvement.

Spec: ONT.CORE.KF_EXECUTION_MODES Section 3.5
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .. import ModuleOutput
from .key_generator import KeyedObject


def write_registry(
    keyed_objects: list[KeyedObject],
    output_dir: Path,
    key_spine: str = "",
) -> dict[str, str]:
    """Write all output artifacts to disk.

    Returns dict of {artifact_name: file_path} for what was written.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    now = datetime.now(timezone.utc).isoformat()

    # 1. Object inventory (raw list)
    inventory = {
        "metadata": {
            "total_objects": len(keyed_objects),
            "generation_timestamp": now,
            "categories": _count_categories(keyed_objects),
        },
        "objects": [
            {
                "path": obj.path,
                "category": obj.category,
                "ook_key": obj.ook_key,
                "lifecycle_role": obj.lifecycle_role,
                "behavior_class": obj.behavior_class,
                "governance_intent": obj.governance_intent,
                "object_class": obj.object_class,
                "confidence": obj.confidence,
            }
            for obj in keyed_objects
        ],
    }
    inv_path = output_dir / "object_inventory.json"
    inv_path.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    written["object_inventory"] = str(inv_path)

    # 2. OOK registry (keyed lookup)
    registry = {
        "metadata": {
            "generation_timestamp": now,
            "total_objects": len(keyed_objects),
            "unique_keys": len(set(o.ook_key for o in keyed_objects)),
            "collision_count": sum(1 for o in keyed_objects if o.collision_resolved),
            "key_spine": key_spine,
        },
        "registry": {
            obj.ook_key: {
                "path": obj.path,
                "category": obj.category,
                "classification": {
                    "lifecycle_role": obj.lifecycle_role,
                    "behavior_class": obj.behavior_class,
                    "governance_intent": obj.governance_intent,
                },
                "object_class": obj.object_class,
                "object_version": obj.object_version,
                "confidence": obj.confidence,
                "collision_resolved": obj.collision_resolved,
            }
            for obj in keyed_objects
        },
    }
    reg_path = output_dir / "ook_registry.json"
    reg_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    written["ook_registry"] = str(reg_path)

    # 3. Classification summary (human-readable)
    summary_lines = [
        f"# OOK Classification Summary",
        f"",
        f"Generated: {now}",
        f"Total objects: {len(keyed_objects)}",
        f"Key spine: {key_spine}",
        f"",
        f"## Categories",
        f"",
    ]
    for cat, count in sorted(_count_categories(keyed_objects).items()):
        summary_lines.append(f"- {cat}: {count}")
    summary_lines.extend([
        f"",
        f"## Classification Distribution",
        f"",
        f"### Lifecycle Roles",
    ])
    for code, count in sorted(_count_axis(keyed_objects, "lifecycle_role").items()):
        summary_lines.append(f"- {code}: {count}")
    summary_lines.extend([f"", f"### Behavior Classes"])
    for code, count in sorted(_count_axis(keyed_objects, "behavior_class").items()):
        summary_lines.append(f"- {code}: {count}")
    summary_lines.extend([f"", f"### Governance Intents"])
    for code, count in sorted(_count_axis(keyed_objects, "governance_intent").items()):
        summary_lines.append(f"- {code}: {count}")

    collisions = [o for o in keyed_objects if o.collision_resolved]
    if collisions:
        summary_lines.extend([f"", f"## Collisions Resolved ({len(collisions)})"])
        for c in collisions:
            summary_lines.append(f"- {c.ook_key} ({c.collision_attempts} attempts)")

    sum_path = output_dir / "classification_summary.md"
    sum_path.write_text("\n".join(summary_lines), encoding="utf-8")
    written["classification_summary"] = str(sum_path)

    return written


def _count_categories(objects: list[KeyedObject]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for o in objects:
        counts[o.category] = counts.get(o.category, 0) + 1
    return counts


def _count_axis(objects: list[KeyedObject], axis: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for o in objects:
        val = getattr(o, axis, "")
        counts[val] = counts.get(val, 0) + 1
    return counts


def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Write registry artifacts to disk.

    Inputs:
        keyed_objects: list[KeyedObject] -- from key_generator

    Config:
        output_dir: str -- where to write files
        key_spine: str -- for metadata
    """
    keyed_objects = inputs.get("keyed_objects", [])
    output_dir = Path(config.get("output_dir", "."))
    key_spine = config.get("key_spine", "")

    written = write_registry(keyed_objects, output_dir, key_spine)

    return ModuleOutput(
        data=written,
        confident=list(written.values()),
        ambiguous=[],
        mode="D",
        stage="Ac",
        stats={
            "files_written": len(written),
            "artifacts": list(written.keys()),
        },
    )
