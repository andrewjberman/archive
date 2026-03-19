"""
Ad: Adapt -- Structural Validator (D-mode, 100% coverage).

Deterministic validation of classification output against ground truth.
Catches: path existence, taxonomy enum compliance, key spine match,
object count match, key uniqueness, format compliance.

Zero API calls. Pure filesystem checks and string comparisons.

Spec: ONT.CORE.KF_EXECUTION_MODES Section 3.6
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .. import ModuleOutput
from ..act.key_generator import KeyedObject


@dataclass
class ValidationResult:
    """Result of structural validation."""
    check: str
    passed: bool
    detail: str = ""
    affected_objects: list[str] = field(default_factory=list)


def validate_structural(
    keyed_objects: list[KeyedObject],
    expected_spine: str,
    expected_count: int,
    valid_lifecycle: list[str],
    valid_behavior: list[str],
    valid_governance: list[str],
    count_tolerance: float = 0.15,
) -> list[ValidationResult]:
    """Run all structural validation checks.

    Returns list of ValidationResult. All must pass for the batch
    to be accepted.
    """
    results = []

    # 1. Path existence
    missing = [o.path for o in keyed_objects if not Path(o.path).exists()]
    results.append(ValidationResult(
        check="path_existence",
        passed=len(missing) == 0,
        detail=f"{len(missing)} paths do not exist" if missing else "All paths exist",
        affected_objects=missing[:10],
    ))

    # 2. Taxonomy enum compliance
    lc_invalid = [
        o.path for o in keyed_objects
        if valid_lifecycle and o.lifecycle_role not in valid_lifecycle
    ]
    results.append(ValidationResult(
        check="lifecycle_role_enum",
        passed=len(lc_invalid) == 0,
        detail=f"{len(lc_invalid)} invalid lifecycle roles" if lc_invalid else "All valid",
        affected_objects=lc_invalid[:10],
    ))

    bc_invalid = [
        o.path for o in keyed_objects
        if valid_behavior and o.behavior_class not in valid_behavior
    ]
    results.append(ValidationResult(
        check="behavior_class_enum",
        passed=len(bc_invalid) == 0,
        detail=f"{len(bc_invalid)} invalid behavior classes" if bc_invalid else "All valid",
        affected_objects=bc_invalid[:10],
    ))

    gi_invalid = [
        o.path for o in keyed_objects
        if valid_governance and o.governance_intent not in valid_governance
    ]
    results.append(ValidationResult(
        check="governance_intent_enum",
        passed=len(gi_invalid) == 0,
        detail=f"{len(gi_invalid)} invalid governance intents" if gi_invalid else "All valid",
        affected_objects=gi_invalid[:10],
    ))

    # 3. Key spine match
    spine_mismatch = [
        o.path for o in keyed_objects
        if expected_spine and not o.ook_key.startswith(expected_spine)
    ]
    results.append(ValidationResult(
        check="key_spine_match",
        passed=len(spine_mismatch) == 0,
        detail=f"{len(spine_mismatch)} keys do not start with '{expected_spine}'" if spine_mismatch else "All keys match spine",
        affected_objects=spine_mismatch[:10],
    ))

    # 4. Object count
    actual = len(keyed_objects)
    if expected_count > 0:
        deviation = abs(actual - expected_count) / expected_count
        passed = deviation <= count_tolerance
        results.append(ValidationResult(
            check="object_count",
            passed=passed,
            detail=f"Expected {expected_count}, got {actual} (deviation: {deviation:.1%}, tolerance: {count_tolerance:.0%})",
        ))

    # 5. Key uniqueness
    keys = [o.ook_key for o in keyed_objects]
    duplicates = [k for k in keys if keys.count(k) > 1]
    unique_dupes = list(set(duplicates))
    results.append(ValidationResult(
        check="key_uniqueness",
        passed=len(unique_dupes) == 0,
        detail=f"{len(unique_dupes)} duplicate keys" if unique_dupes else "All keys unique",
        affected_objects=unique_dupes[:10],
    ))

    # 6. Format compliance (key segment count)
    # Expected: SPINE-BTS-KT-OTS-OTR-OTB-OTG-OC-OV
    # Spine itself has segments, so total varies. Check minimum segment count.
    spine_segments = len(expected_spine.split("-")) if expected_spine else 0
    expected_total = spine_segments + 8  # BTS, KT, OTS, OTR, OTB, OTG, OC, OV
    format_bad = [
        o.path for o in keyed_objects
        if len(o.ook_key.split("-")) < expected_total - 1  # allow 1 segment tolerance
    ]
    results.append(ValidationResult(
        check="format_compliance",
        passed=len(format_bad) == 0,
        detail=f"{len(format_bad)} keys have wrong segment count" if format_bad else "All keys format-compliant",
        affected_objects=format_bad[:10],
    ))

    return results


def execute(inputs: dict, config: dict) -> ModuleOutput:
    """Run structural validation on keyed objects.

    Inputs:
        keyed_objects: list[KeyedObject]

    Config:
        expected_spine: str
        expected_count: int
        taxonomy_lifecycle: list[str]
        taxonomy_behavior: list[str]
        taxonomy_governance: list[str]
        count_tolerance: float (default 0.15)
    """
    keyed_objects = inputs.get("keyed_objects", [])

    results = validate_structural(
        keyed_objects,
        expected_spine=config.get("expected_spine", ""),
        expected_count=config.get("expected_count", 0),
        valid_lifecycle=config.get("taxonomy_lifecycle", []),
        valid_behavior=config.get("taxonomy_behavior", []),
        valid_governance=config.get("taxonomy_governance", []),
        count_tolerance=config.get("count_tolerance", 0.15),
    )

    passed = all(r.passed for r in results)
    failed = [r for r in results if not r.passed]

    return ModuleOutput(
        data=results,
        confident=[r for r in results if r.passed],
        ambiguous=[r for r in results if not r.passed],
        mode="D",
        stage="Ad",
        stats={
            "total_checks": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "all_passed": passed,
            "failed_checks": [r.check for r in failed],
        },
    )
