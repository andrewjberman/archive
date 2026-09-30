"""AMGT_RESAPP round 52, AMGT-ab-1 -- a READ-ONLY preview of ASML's D-1 rebuild (CTO round-51 analysis item 1).
Builds the drafting document in memory from the STORED newest analysis object with the committed producer
(`drafting_build.build_drafting_document`, the same transform `--rebuild-pool` runs) and compares it with the stored
`drafting/v1/ASML_NA_Equity.json`: prints every top-level key whose value differs, the sentence counts per section before and after,
and the thesis_driver points with their spans before and after. Writes nothing.
PASS (the preview's own claim) when the rebuilt driver carries >= 2 points with a span; the served proof is
`round51/checks/zz_8_served.py --what chart` (the route), never this in-memory build.
usage: python <this>   (from the repo root; S3 read-only)"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402

KEY = "ASML_NA_Equity"


def spans(driver):
    pts = (driver or {}).get("points") or []
    return len(pts), sum(1 for p in pts if isinstance(p, dict) and p.get("span"))


def main():
    cl = boto3.client("s3", region_name="us-east-1")
    akey = db._newest_analysis_key(cl, KEY)
    analysis = db._get_json_object(cl, akey)
    rebuilt = db.build_drafting_document(analysis)
    stored = db._get_json_object(cl, db._drafting_pool_key(KEY))
    print("analysis %s; drafting %s" % (akey, db._drafting_pool_key(KEY)))
    keys = sorted(set(rebuilt) | set(stored))
    moved = [k for k in keys if json.dumps(rebuilt.get(k), sort_keys=True) != json.dumps(stored.get(k), sort_keys=True)]
    print("top-level keys %d; differing %d: %s" % (len(keys), len(moved), moved))
    for label, doc in (("stored", stored), ("rebuilt", rebuilt)):
        counts = {s.get("section"): len(s.get("sentences") or []) for s in doc.get("sections") or []}
        n, sp = spans(doc.get("thesis_driver"))
        print("%-8s sections %s; thesis_driver points %d, with span %d" % (label, counts, n, sp))
    n, sp = spans(rebuilt.get("thesis_driver"))
    ok = sp >= 2
    print("THE REBUILT D-1 DOCUMENT CARRIES THE SPANNED DRIVER: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
