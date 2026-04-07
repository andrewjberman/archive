"""
Ac: Act -- OOK Key Generator (D-mode).

Deterministic key generation from classification + spine template.
No LLM needed. Collision detection via hash set + suffix increment.

Spec: ONT.CORE.KF_EXECUTION_MODES Section 3.5
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .. import ModuleOutput, Classification


@dataclass
class KeyedObject:
    """Object with OOK key assigned."""
    path: str
    category: str
    ook_key: str
    lifecycle_role: str
    behavior_class: str
    governance_intent: str
    object_class: str           # 4-char abbreviation
    object_version: str         # e.g., "0001"
    confidence: float
    collision_resolved: bool = False
    collision_attempts: int = 0


def _derive_object_class(filename: str, category: str) -> str:
    """Derive a 4-character object class code from the filename.

    Takes first 2 chars of category prefix + first 2 chars of filename.
    E.g., core_spec + ARCHETYPES.md -> CSAR
    """
    # Category prefix (2 chars)
    prefix_map = {
        "core_spec": "CS",
        "derived_spec": "DS",
        "meta_spec": "MS",
        "archetype_contract": "AC",
        "boundary_contract": "BC",
        "gate_contract": "GC",
        "encoding_registry": "ER",
        "domain_index": "DI",
    }
    prefix = prefix_map.get(category, "XX")

    # Filename suffix (2 chars from cleaned name)
    name = filename.split(".")[0].upper()
    # Remove common prefixes/suffixes
    for remove in ("_SPEC", "_PROTOCOL", "_ARCHITECTURE"):
        name = name.replace(remove, "")
    suffix = name[:2] if len(name) >= 2 else name.ljust(2, "X")

    return prefix + suffix


def generate_keys(
    classifications: list[Classification],
    key_spine: str,
    key_format: str = "",
    timestamp: str = "",
) -> list[KeyedObject]:
    """Generate OOK keys for all classified objects.

    Args:
        classifications: Ev-stage output (confident + resolved ambiguous)
        key_spine: e.g., "CORP-MAIN-CREATE-0001"
        key_format: e.g., "ORG-MAC-PRJ-VER-BTS-KT-OTS-OTR-OTB-OTG-OC-OV"
        timestamp: ISO timestamp for BTS/OTS segments (auto-generated if empty)

    Returns:
        List of KeyedObject with unique OOK keys.
    """
    if not timestamp:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    used_keys: set[str] = set()
    results: list[KeyedObject] = []

    for cl in classifications:
        oc = _derive_object_class(cl.metadata.filename if cl.metadata else "", cl.category)
        version = "0001"

        # Build key
        key = (
            f"{key_spine}-{timestamp}-O-{timestamp}-"
            f"{cl.lifecycle_role.code}-{cl.behavior_class.code}-"
            f"{cl.governance_intent.code}-{oc}-{version}"
        )

        # Collision detection + resolution
        collision = False
        attempts = 0
        while key in used_keys:
            collision = True
            attempts += 1
            # Modify OC with numeric suffix
            if attempts == 1:
                oc = oc[:3] + str(attempts)
            else:
                oc = oc[:2] + str(attempts).zfill(2)
            key = (
                f"{key_spine}-{timestamp}-O-{timestamp}-"
                f"{cl.lifecycle_role.code}-{cl.behavior_class.code}-"
                f"{cl.governance_intent.code}-{oc}-{version}"
            )
            if attempts > 20:
                break

        used_keys.add(key)

        results.append(KeyedObject(
            path=cl.path,
            category=cl.category,
            ook_key=key,
            lifecycle_role=cl.lifecycle_role.code,
            behavior_class=cl.behavior_class.code,
            governance_intent=cl.governance_intent.code,
            object_class=oc,
            object_version=version,
            confidence=cl.confidence,
            collision_resolved=collision,
            collision_attempts=attempts,
        ))

    return results


def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Generate OOK keys for all classified objects.

    Inputs:
        classifications: list[Classification] -- from Ev (confident) + De (resolved)

    Config:
        key_spine: str -- e.g., "CORP-MAIN-CREATE-0001"
        key_format: str -- optional format description
    """
    classifications = inputs.get("classifications", [])
    key_spine = config.get("key_spine", "CORP-UNKNOWN-0001")

    keyed = generate_keys(
        classifications,
        key_spine=key_spine,
        key_format=config.get("key_format", ""),
    )

    collisions = sum(1 for k in keyed if k.collision_resolved)

    return ModuleOutput(
        data=keyed,
        confident=keyed,
        ambiguous=[],
        mode="D",
        stage="Ac",
        stats={
            "total_keyed": len(keyed),
            "collisions_resolved": collisions,
            "unique_keys": len(set(k.ook_key for k in keyed)),
        },
    )
