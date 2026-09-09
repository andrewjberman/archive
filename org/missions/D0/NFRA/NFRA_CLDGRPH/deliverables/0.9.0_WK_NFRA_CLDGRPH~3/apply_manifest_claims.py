#!/usr/bin/env python3
"""CG-s-19 deliverable 4 -- put the S53 CLAIM FIELDS on the STAYING stores'
manifests in the MAIN WORKSPACE. Run once; idempotent; prints the file before
and after; opens no store with any engine and changes no store's bytes.

TWO ARTIFACTS, TWO DIFFERENT ACTS:

  kuzu_db._build_manifest.json  -- EDIT IN PLACE. Two keys ADDED, nothing else
      touched (the script asserts the pre-existing key/value set is identical
      after the write). edge_count_claim=merge_attempts because kuzu_load.py
      stamps `len(edges) - skipped`, an upper bound on edges actually present;
      artifact_claim=historical because the CVO's P7 row classes this store
      HISTORICAL (Jun-12 scratch, 1,166 nodes).

  kuzu_ac7.db._build_manifest.json -- CREATED. The store has NO builder
      manifest and its builder (NFRA_GLOBGRPH.ITEM-3, June 2026) left no
      record, so this file is a CLAIM CARD, not a build stamp, and every
      rendered field says so. A manifest that says it does not know is the
      honest one -- but note that creating ANY manifest beside a manifest-less
      DB silences _provenance.format_provenance_header's `!! UNKNOWN VINTAGE`
      banner (_provenance.py, the `m is None` branch), which is why every value
      here is the word UNKNOWN and why the effect is filed as a surprise row.

USAGE: python apply_manifest_claims.py [--check]
       --check reports the state and writes nothing.
"""
from __future__ import annotations

import json
import os
import sys

W = r"C:\Users\AndrewBerman\Desktop\ajb_workspace\infra\aws\globgrph"
KUZU_DB_MANIFEST = os.path.join(W, "kuzu_db._build_manifest.json")
AC7_MANIFEST = os.path.join(W, "kuzu_ac7.db._build_manifest.json")

AC7_CARD = {
    "schema_version": 1,
    "source_kind": "UNKNOWN (claim card written by CG-s-19, NOT a build stamp)",
    "source": ("unknown (no builder manifest; NFRA_GLOBGRPH.ITEM-3, June 2026 --"
               " the builder was kuzu_ac_traversals.py's ancestor and left no"
               " provenance record)"),
    "built_at": "UNKNOWN (no build record; the file's mtime is 2026-06-12 10:57 local)",
    "artifact_claim": "historical",
    "edge_count_claim": "unknown",
    "claim_note": ("node_count and edge_count are ABSENT ON PURPOSE: no count of"
                   " this store exists that was not produced by opening it, and"
                   " kuzu.Database CREATES an absent store on open, so CG-s-19"
                   " takes counts from manifests only. edge_count_claim=unknown"
                   " is a THIRD value beside the merge_attempts/edges pair the"
                   " task order names -- an artifact with no edge_count field"
                   " can honestly claim neither."),
    "written_by": "0.9.0_WK_NFRA_CLDGRPH~3 (NFRA_CLDGRPH.TO-CG-E-3, cell CG-s-19)",
}


def show(path: str, label: str) -> None:
    print("--- %s: %s ---" % (label, path))
    if not os.path.exists(path):
        print("  (absent)")
        return
    with open(path, encoding="utf-8") as fh:
        print("".join("  " + ln for ln in fh.readlines()))


def main() -> int:
    check = "--check" in sys.argv[1:]
    show(KUZU_DB_MANIFEST, "BEFORE")
    show(AC7_MANIFEST, "BEFORE")

    with open(KUZU_DB_MANIFEST, encoding="utf-8") as fh:
        before = json.load(fh)
    after = dict(before)
    after["edge_count_claim"] = "merge_attempts"
    after["artifact_claim"] = "historical"
    untouched_before = {k: v for k, v in before.items()
                        if k not in ("edge_count_claim", "artifact_claim")}
    untouched_after = {k: v for k, v in after.items()
                       if k not in ("edge_count_claim", "artifact_claim")}
    assert untouched_before == untouched_after, "a pre-existing key changed"
    if not check:
        tmp = KUZU_DB_MANIFEST + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(after, fh, indent=2, sort_keys=True)
        os.replace(tmp, KUZU_DB_MANIFEST)
        if not os.path.exists(AC7_MANIFEST):
            tmp2 = AC7_MANIFEST + ".tmp"
            with open(tmp2, "w", encoding="utf-8") as fh:
                json.dump(AC7_CARD, fh, indent=2, sort_keys=True)
            os.replace(tmp2, AC7_MANIFEST)

    show(KUZU_DB_MANIFEST, "AFTER")
    show(AC7_MANIFEST, "AFTER")
    print("PRE_EXISTING_KEYS_UNCHANGED=%d of %d" %
          (len(untouched_before), len(before)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
