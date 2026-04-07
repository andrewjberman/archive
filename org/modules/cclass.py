"""
cclass — Classification pipeline entry point.

Runs Pe -> In -> Ac -> Ad stages deterministically.
Taxonomy classification itself is LLM work (dispatched separately).
This module handles everything around it.

Usage:
    from modules.cclass import run
    result = run("/path/to/directory", key_spine="CORP-MAIN-CREATE-0001")

CLI:
    python -m system.os.runtime.modules.cclass --directory ontology --key-spine CORP-MAIN-CREATE-0001
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .perceive.filesystem_scanner import execute as scan_files
from .perceive.corpus_indexer import CorpusIndex
from .interpret.content_fingerprinter import execute as fingerprint
from .act.key_generator import execute as generate_keys
from .act.registry_writer import execute as write_registry
from .adapt.structural_validator import execute as validate
from .adapt.coverage_auditor import execute as audit_coverage
from .adapt.differential_regression import execute as diff_regress


def run(
    directory: str,
    key_spine: str = "",
    output_dir: str = "",
    taxonomy_lifecycle: list[str] | None = None,
    taxonomy_behavior: list[str] | None = None,
    taxonomy_governance: list[str] | None = None,
    expected_count: int = 0,
    build_index: bool = True,
) -> dict[str, Any]:
    """Run the classification pipeline.

    D-mode stages run here. Taxonomy classification (Ev/De) is NOT
    included — that's LLM work handled by the runtime's worker nodes.

    This function:
      1. Scans files (Pe)
      2. Fingerprints content (In)
      3. Builds corpus index (Pe)
      4. Returns structured data for the LLM classifier to consume

    If classifications are provided (post-LLM), also:
      5. Generates OOK keys (Ac)
      6. Writes registry artifacts (Ac)
      7. Validates output (Ad)
      8. Checks coverage (Ad)
      9. Runs regression diff (Ad)
    """
    out = Path(output_dir) if output_dir else Path(directory) / "cclass_output"

    # --- Pe: Scan ---
    print("[Pe] Scanning...", file=sys.stderr)
    pe = scan_files({}, {"directory": directory})
    files = pe.data
    print(f"[Pe] {len(files)} files", file=sys.stderr)

    # --- Pe: Index ---
    idx_stats = {}
    if build_index:
        print("[Pe] Indexing corpus...", file=sys.stderr)
        idx = CorpusIndex(directory)
        idx_stats = idx.build()
        # If index has 0 docs but files exist, force rebuild (cross-platform index)
        if idx_stats.get("status") == "already_indexed" and idx.file_count() == 0 and len(files) > 0:
            idx_stats = idx.reindex()
        print(f"[Pe] Index: {idx_stats.get('indexed', 0)} files", file=sys.stderr)

    # --- In: Fingerprint ---
    print("[In] Fingerprinting...", file=sys.stderr)
    fp = fingerprint({"pe_output": files}, {})
    fingerprints = fp.data
    print(f"[In] Groups: {fp.stats.get('by_group', {})}", file=sys.stderr)

    return {
        "files": files,
        "fingerprints": fingerprints,
        "file_count": len(files),
        "groups": fp.stats.get("by_group", {}),
        "index_stats": idx_stats if build_index else None,
        "output_dir": str(out),
        "key_spine": key_spine,
        "taxonomy": {
            "lifecycle": taxonomy_lifecycle or [],
            "behavior": taxonomy_behavior or [],
            "governance": taxonomy_governance or [],
        },
    }


def finalize(
    pre_result: dict[str, Any],
    classifications: list[dict[str, Any]],
) -> dict[str, Any]:
    """Run post-classification stages (Ac + Ad).

    Call this after the LLM has classified the objects.
    `classifications` is a list of dicts with at minimum:
      {path, lifecycle_role, behavior_class, governance_intent}
    """
    from . import Classification, AxisResult

    out = Path(pre_result["output_dir"])
    key_spine = pre_result.get("key_spine", "")
    taxonomy = pre_result.get("taxonomy", {})

    # Convert raw dicts to Classification objects for key_generator
    classified = []
    for c in classifications:
        # key_generator reads cl.metadata.filename for OC derivation
        class _Meta:
            def __init__(self, fn): self.filename = fn
        meta = _Meta(Path(c["path"]).name)

        cl = Classification(
            path=c["path"],
            category=c.get("category", ""),
            lifecycle_role=AxisResult(c.get("lifecycle_role", ""), 1.0),
            behavior_class=AxisResult(c.get("behavior_class", ""), 1.0),
            governance_intent=AxisResult(c.get("governance_intent", ""), 1.0),
            confidence=1.0,
            confident=True,
            metadata=meta,
        )
        classified.append(cl)

    # --- Ac: Generate keys ---
    print(f"[Ac] Generating keys for {len(classified)} objects...", file=sys.stderr)
    keys = generate_keys({"classifications": classified}, {"key_spine": key_spine})
    keyed = keys.data
    print(f"[Ac] {len(keyed)} keys. Collisions: {keys.stats.get('collisions_resolved', 0)}", file=sys.stderr)

    # --- Ac: Write registry ---
    print(f"[Ac] Writing to {out}...", file=sys.stderr)
    written = write_registry(
        {"keyed_objects": keyed},
        {"output_dir": str(out), "key_spine": key_spine},
    )
    print(f"[Ac] Wrote: {list(written.data.keys())}", file=sys.stderr)

    # --- Ad: Validate ---
    print("[Ad] Validating...", file=sys.stderr)
    val = validate(
        {"keyed_objects": keyed},
        {
            "expected_spine": key_spine,
            "expected_count": pre_result.get("file_count", 0),
            "taxonomy_lifecycle": taxonomy.get("lifecycle", []),
            "taxonomy_behavior": taxonomy.get("behavior", []),
            "taxonomy_governance": taxonomy.get("governance", []),
        },
    )
    passed = val.stats.get("all_passed", False)
    print(f"[Ad] Validation: {'PASS' if passed else 'FAIL'} ({val.stats['passed']}/{val.stats['total_checks']})", file=sys.stderr)

    # --- Ad: Coverage ---
    source_paths = [f.path for f in pre_result["files"]]
    registry_paths = [k.path for k in keyed]
    cov = audit_coverage(
        {"source_paths": source_paths, "registry_paths": registry_paths}, {},
    )
    print(f"[Ad] Coverage: {cov.stats['coverage_pct']}%", file=sys.stderr)

    # --- Ad: Regression ---
    diff = diff_regress({}, {"output_dir": str(out), "update_on_pass": passed})
    print(f"[Ad] Regression: {diff.stats['verdict']} ({diff.stats['detail']})", file=sys.stderr)

    return {
        "keyed_objects": keyed,
        "artifacts": written.data,
        "validation": val.stats,
        "coverage": cov.stats,
        "regression": diff.stats,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="cclass: classification pipeline")
    parser.add_argument("--directory", required=True)
    parser.add_argument("--key-spine", default="")
    parser.add_argument("--output-dir", default="")
    args = parser.parse_args()

    result = run(args.directory, key_spine=args.key_spine, output_dir=args.output_dir)

    print(f"\nPre-classification complete.", file=sys.stderr)
    print(f"  Files: {result['file_count']}", file=sys.stderr)
    print(f"  Groups: {result['groups']}", file=sys.stderr)
    print(f"  Ready for LLM classification (Ev/De stage).", file=sys.stderr)


if __name__ == "__main__":
    main()
