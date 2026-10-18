"""HVST-cg-2 step 3 (C-6): READ ONLY. Apply the gateway's newest-part rule (the part whose object KEY sorts highest, per
(security_key, report_id), the two misfiled KMB reports excluded) to the bucket and print, for all reports, that the newest row
carries fund_relation, which part it came from, the per-relation counts against the census line, and the six PROOF-NAMES.
Run from the pinned worktree: python -u cg2_after.py. ASCII only.
"""
from __future__ import annotations

import io
import os
import sys
from collections import Counter, defaultdict

WT = r"C:\tmp\cg2-build"
sys.path.insert(0, WT)
os.chdir(WT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.corpus import fund_relation  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

CENSUS = {"holding": 121, "candidate": 14, "initiate": 2, "interest": 2, "template": 1, "unclassified": 0, "none": 213}
PROOF = ("ADBE_US_Equity", "SNPS_US_Equity", "MNST_US_Equity", "ML_FP_Equity", "CLX_US_Equity", "UNH_US_Equity")
EXPECT_PROOF = "ADBE_US_Equity=candidate SNPS_US_Equity=candidate MNST_US_Equity=candidate ML_FP_Equity=template CLX_US_Equity=candidate UNH_US_Equity=holding"
NEW_STAMPS = ("20261018T010034Z", "20261018T010056Z", "20261018T010114Z")


def main():
    client = store._default_client()
    prefix = store.table_prefix(typed.SOURCE, "silver", typed.TABLE)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        keys.extend(o["Key"] for o in (page.get("Contents", []) or []) if o["Key"].endswith(".parquet"))
    keys.sort()
    newest = {}
    rows_read = 0
    for key in keys:
        part_rows = pq.read_table(io.BytesIO(client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read())).to_pylist()
        rows_read += len(part_rows)
        print("# PART %s rows=%d" % (key, len(part_rows)))
        for row in part_rows:
            ident = (row.get("security_key"), row.get("report_id"))
            prev = newest.get(ident)
            if prev is None or key > prev[0]:
                newest[ident] = (key, row)
    excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
    kept = [(i, newest[i]) for i in sorted(newest, key=lambda x: (str(x[0]), str(x[1]))) if i not in excluded]
    print("# DENOMINATOR parts=%d rows_read=%d distinct_reports=%d kept=%d excluded_misfiled=%d" % (
        len(keys), rows_read, len(newest), len(kept), len(newest) - len(kept)))
    stored = Counter()
    from_new = 0
    missing = 0
    recompute_mismatch = 0
    by_security = defaultdict(set)
    for (sk, _rid), (part, row) in kept:
        rel = row.get("fund_relation")
        if rel is None:
            missing += 1
            continue
        stored[rel] += 1
        if any(("part-" + s) in part for s in NEW_STAMPS):
            from_new += 1
        if rel != fund_relation.classify(row.get("fund"), row.get("fund_evidence")):
            recompute_mismatch += 1
        if row.get("fund") is not None:
            by_security[sk].add(rel)
    print("NEWEST-CARRIES-FUND-RELATION kept=%d with_value=%d missing=%d from_the_three_new_parts=%d recompute_mismatch=%d" % (
        len(kept), len(kept) - missing, missing, from_new, recompute_mismatch))
    line = " ".join("%s=%d" % (k, stored.get(k, 0)) for k in CENSUS)
    want = " ".join("%s=%d" % (k, v) for k, v in CENSUS.items())
    print("COUNTS %s" % line)
    print("CENSUS %s" % want)
    proof = " ".join("%s=%s" % (sk, "+".join(sorted(by_security.get(sk, ()))) or "none") for sk in PROOF)
    print("PROOF-NAMES " + proof)
    ok = (len(kept) == 353 and missing == 0 and from_new == 353 and recompute_mismatch == 0 and line == want and proof == EXPECT_PROOF)
    print("NEWEST_PER_REPORT_EQUALS_CENSUS=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
