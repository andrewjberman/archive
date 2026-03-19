"""
Classification Pipeline -- supplier-layer, KF_EXECUTION_MODES for structured codebases.

For codebases with known taxonomy and consistent directory structure.
Composes: Pe -> In -> Ev(rules) -> Ac(keys) -> Ac(registry) -> Ad(validate).
All D-mode when confidence is high. Ambiguous items forwarded to I-mode.

Archetype access: supplier workers only.

Usage:
    from pipelines.ingestion import run_classification_pipeline
    result = run_classification_pipeline(
        directory="/corporeal/ontology",
        taxonomy_dir="/corporeal/ontology/registry",
        key_spine="CORP-MAIN-CREATE-0001",
    )

Spec: ONT.CORE.KF_EXECUTION_MODES + ONT.CORE.HYBRID_CLASSIFICATION
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from ...modules.perceive.filesystem_scanner import FileMetadata, execute as pe_execute
from ...modules.interpret.content_fingerprinter import ContentFingerprint, execute as in_execute
from ...modules.evaluate.rule_classifier import Classification, execute as ev_execute
from ...modules.act.key_generator import KeyedObject, execute as ac_key_execute
from ...modules.act.registry_writer import execute as ac_write_execute
from ...modules.adapt.structural_validator import execute as ad_execute


def _load_taxonomy(taxonomy_dir: str) -> tuple[list[str], list[str], list[str]]:
    """Load taxonomy codes from registry JSON files."""
    td = Path(taxonomy_dir)
    lc, bc, gi = [], [], []
    for fname, key, target in [
        ("lifecycle_roles.json", "roles", "lc"),
        ("behavior_classes.json", "classes", "bc"),
        ("governance_intents.json", "intents", "gi"),
    ]:
        fp = td / fname
        if fp.exists():
            data = json.loads(fp.read_text())
            entries = data.get(key, [])
            codes = [e["code"] for e in entries if isinstance(e, dict) and "code" in e]
            if target == "lc":
                lc = codes
            elif target == "bc":
                bc = codes
            elif target == "gi":
                gi = codes
    return lc, bc, gi


def run_classification_pipeline(
    directory: str,
    taxonomy_dir: str = "",
    taxonomy_lifecycle: list[str] | None = None,
    taxonomy_behavior: list[str] | None = None,
    taxonomy_governance: list[str] | None = None,
    key_spine: str = "",
    key_format: str = "",
    expected_count: int = 0,
    output_dir: str = "",
    threshold: float = 0.75,
) -> dict[str, Any]:
    """Run the full Pe -> In -> Ev -> Ac -> Ad classification pipeline.

    All D-mode for confident objects. Returns ambiguous items for I-mode.
    """
    # Load taxonomy from directory if codes not provided directly
    if taxonomy_dir and not taxonomy_lifecycle:
        taxonomy_lifecycle, taxonomy_behavior, taxonomy_governance = _load_taxonomy(taxonomy_dir)

    lc = taxonomy_lifecycle or []
    bc = taxonomy_behavior or []
    gi = taxonomy_governance or []

    # --- Pe ---
    print("[Pe] Scanning filesystem...", file=sys.stderr)
    pe_result = pe_execute({}, {"directory": directory})
    pe_output: list[FileMetadata] = pe_result.data
    print(f"[Pe] Found {len(pe_output)} files", file=sys.stderr)

    # --- In ---
    print("[In] Fingerprinting content...", file=sys.stderr)
    in_result = in_execute({"pe_output": pe_output}, {})
    in_output: list[ContentFingerprint] = in_result.data
    print(f"[In] Fingerprinted {len(in_output)} files", file=sys.stderr)

    # --- Ev ---
    print(f"[Ev] Classifying (threshold={threshold})...", file=sys.stderr)
    ev_result = ev_execute(
        {"pe_output": pe_output, "in_output": in_output},
        {"taxonomy_lifecycle": lc, "taxonomy_behavior": bc,
         "taxonomy_governance": gi, "threshold": threshold},
    )
    confident: list[Classification] = ev_result.confident
    ambiguous: list[Classification] = ev_result.ambiguous
    print(f"[Ev] {len(confident)} confident ({ev_result.stats['confident_pct']}%), {len(ambiguous)} ambiguous", file=sys.stderr)

    # --- Ac: keys ---
    print(f"[Ac] Generating keys for {len(confident)} objects...", file=sys.stderr)
    ac_key_result = ac_key_execute(
        {"classifications": confident},
        {"key_spine": key_spine, "key_format": key_format},
    )
    keyed: list[KeyedObject] = ac_key_result.data
    print(f"[Ac] {len(keyed)} keys. Collisions: {ac_key_result.stats.get('collisions_resolved', 0)}", file=sys.stderr)

    # --- Ac: write ---
    out_dir = output_dir or str(Path(directory) / "classification_output")
    print(f"[Ac] Writing to {out_dir}...", file=sys.stderr)
    ac_write_result = ac_write_execute(
        {"keyed_objects": keyed},
        {"output_dir": out_dir, "key_spine": key_spine},
    )
    written = ac_write_result.data
    print(f"[Ac] Wrote {len(written)} artifacts", file=sys.stderr)

    # --- Ad: validate ---
    print("[Ad] Validating...", file=sys.stderr)
    ad_result = ad_execute(
        {"keyed_objects": keyed},
        {
            "expected_spine": key_spine,
            "expected_count": expected_count or len(pe_output),
            "taxonomy_lifecycle": lc, "taxonomy_behavior": bc, "taxonomy_governance": gi,
        },
    )
    all_passed = ad_result.stats.get("all_passed", False)
    print(f"[Ad] {'PASSED' if all_passed else 'FAILED'} ({ad_result.stats['passed']}/{ad_result.stats['total_checks']})", file=sys.stderr)
    if not all_passed:
        for v in ad_result.data:
            if not v.passed:
                print(f"  FAIL: {v.check} -- {v.detail}", file=sys.stderr)

    return {
        "keyed_objects": keyed,
        "ambiguous": ambiguous,
        "validation": ad_result.data,
        "artifacts_written": written,
        "stats": {
            "pe": pe_result.stats, "in": in_result.stats, "ev": ev_result.stats,
            "ac": ac_key_result.stats, "ad": ad_result.stats,
            "total_api_calls": 0,
            "ambiguous_for_llm": len(ambiguous),
        },
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Classification Pipeline")
    parser.add_argument("--directory", required=True)
    parser.add_argument("--taxonomy-dir", required=True)
    parser.add_argument("--key-spine", required=True)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--threshold", type=float, default=0.75)
    args = parser.parse_args()

    run_classification_pipeline(
        directory=args.directory,
        taxonomy_dir=args.taxonomy_dir,
        key_spine=args.key_spine,
        output_dir=args.output_dir,
        threshold=args.threshold,
    )


if __name__ == "__main__":
    main()
