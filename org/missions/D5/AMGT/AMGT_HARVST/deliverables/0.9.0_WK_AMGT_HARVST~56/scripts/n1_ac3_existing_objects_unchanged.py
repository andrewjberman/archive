"""HVST-n-1 AC3: the change is going-forward only. Read the served bronze article objects'
metadata (S3 LIST + HEAD only, through a write-guarded client) THROUGH THE NEW STORE CODE
(`store.bronze_form_census`) and classify them; then cross-check every key against an independent
raw reading of its `received-form` label. The round-23 reading was 126 objects: 104
normalised_record, 16 as_received, 6 unlabelled.

PASS: the census reads the same 126 / 104 / 16 / 6, the new classification equals the raw label
reading for EVERY key (so no existing object is re-labelled), and the write guard counted zero
write calls.
"""

import json
from pathlib import Path
import sys


def _repo_root():
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "lib" / "opal_data_harvest" / "worker.py").exists():
            return parent
    raise SystemExit("ERROR: repo root not found above %s" % here)


ROOT = _repo_root()
sys.path.insert(0, str(ROOT))

import lib.research.harvest.store as store  # noqa: E402
from lib.opal_data_harvest.classify_unlabelled_bronze import build_guarded_client  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "n1_ac3_output.json"
SOURCES = ("seeking-alpha", "bloomberg", "barrons", "wsj", "ft")
ROUND23 = {"total": 126, "as_received": 16, "normalised_record": 104, "unlabelled": 6}


def main():
    client = build_guarded_client()
    per_source = {}
    all_keys = {}
    for source in SOURCES:
        census = store.bronze_form_census(source, "article", client=client)
        per_source[source] = {"total": census["total"], "counts": census["counts"]}
        all_keys.update(census["keys"])
        print("%-14s total=%-3d as_received=%-3d normalised_record=%-3d unlabelled=%-3d"
              % (source, census["total"], census["counts"]["as_received"],
                 census["counts"]["normalised_record"], census["counts"]["unlabelled"]))
    totals = {"total": len(all_keys)}
    for form in ("as_received", "normalised_record", "unlabelled"):
        totals[form] = sum(1 for f in all_keys.values() if f == form)
    print("NEW STORE CODE census over %d sources: total=%d as_received=%d normalised_record=%d unlabelled=%d"
          % (len(SOURCES), totals["total"], totals["as_received"], totals["normalised_record"], totals["unlabelled"]))

    # Independent reading: the raw `received-form` label on each key, no store code involved.
    mismatched, relabelled, lacking_hash = [], [], 0
    for key, form in all_keys.items():
        metadata = {k.lower(): v for k, v in (client.head_object(Bucket=store.HARVEST_BUCKET, Key=key)
                                              .get("Metadata") or {}).items()}
        label = metadata.get("received-form")
        expected = label if label in ("as_received", "normalised_record") else "unlabelled"
        if form != expected:
            mismatched.append(key)
        if form == "as_received" and label != "as_received":
            relabelled.append(key)
        if form == "as_received" and "received-sha256" not in metadata:
            lacking_hash += 1
    print("cross-check: %d of %d keys where the new classification differs from the raw label reading"
          % (len(mismatched), len(all_keys)))
    print("re-labelled as received bytes: %d of %d" % (len(relabelled), len(all_keys)))
    print("existing as_received objects carrying no received-sha256 (written before this change): %d of %d"
          % (lacking_hash, totals["as_received"]))
    print("write guard: %d write calls attempted" % client.write_calls)

    checks = {
        "total_matches_round23": totals["total"] == ROUND23["total"],
        "as_received_matches_round23": totals["as_received"] == ROUND23["as_received"],
        "normalised_record_matches_round23": totals["normalised_record"] == ROUND23["normalised_record"],
        "unlabelled_matches_round23": totals["unlabelled"] == ROUND23["unlabelled"],
        "classification_equals_raw_label_for_every_key": not mismatched,
        "no_object_relabelled_as_received": not relabelled,
        "zero_write_calls": client.write_calls == 0,
    }
    for name, ok in checks.items():
        print("%s: %s" % ("PASS" if ok else "FAIL", name))
    verdict = all(checks.values())
    print("%s (%d of %d objects classified as at the round-23 reading)"
          % ("PASS" if verdict else "FAIL", totals["total"], ROUND23["total"]))
    OUT.write_text(json.dumps({"per_source": per_source, "totals": totals, "round23": ROUND23,
                               "mismatched": mismatched, "relabelled": relabelled,
                               "as_received_lacking_received_sha256": lacking_hash,
                               "write_calls": client.write_calls, "checks": checks,
                               "verdict": "PASS" if verdict else "FAIL"}, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    return 0 if verdict else 1


if __name__ == "__main__":
    raise SystemExit(main())
