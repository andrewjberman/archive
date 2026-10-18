"""AMGT_HARVST HVST-cg-2, issuer's own C-6 / read-back check (2.0.0_SA_COO~W1). READ ONLY.

Lists every part under amgt/harvest/silver/research-report/, applies the gateway's rule (the part whose KEY sorts
highest wins per (security_key, report_id); infra/aws/ec2/opal-gateway/app/harvest_research.py::_research_reports),
drops the misfiled reports as the gateway does, and prints:
  - the number of parts and of the new parts (run_stamp of 2026-10-18),
  - the kept rows, how many carry fund_relation, and the count per relation,
  - for each kept NEW row, whether every column other than fund_relation and record_hash equals the row it supersedes
    (the highest key below it among the rows of the same report).
Run from the repo root:  python -u <this file>
"""
import io
import json
import sys

import pyarrow.parquet as pq

sys.path.insert(0, ".")
from lib.research.corpus import typed                      # noqa: E402
from lib.research.harvest import store                     # noqa: E402

PREFIX = store.table_prefix(typed.SOURCE, "silver", typed.TABLE)
BUCKET = store.HARVEST_BUCKET
client = store._default_client()
gets = 0
nbytes = 0

keys = []
for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
    gets += 1
    for obj in page.get("Contents", []) or []:
        if obj["Key"].endswith(".parquet"):
            keys.append(obj["Key"])
keys.sort()

excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
by_report = {}
for key in keys:
    raw = client.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    gets += 1
    nbytes += len(raw)
    for row in pq.read_table(io.BytesIO(raw)).to_pylist():
        rk = (row.get("security_key"), row.get("report_id"))
        if rk in excluded:
            continue
        by_report.setdefault(rk, []).append((key, row))

new_parts = [k for k in keys if "part-20261018" in k]
counts = {}
kept = 0
with_rel = 0
new_rows = 0
mismatch = 0
detail = []
for rk, rows in sorted(by_report.items(), key=lambda kv: str(kv[0])):
    rows.sort(key=lambda kr: kr[0])
    key, row = rows[-1]
    kept += 1
    rel = row.get("fund_relation")
    if rel is not None:
        with_rel += 1
        counts[rel] = counts.get(rel, 0) + 1
    if "part-20261018" in key:
        new_rows += 1
        if len(rows) < 2:
            mismatch += 1
            detail.append("NO_PREDECESSOR %s %s" % rk)
            continue
        prev = rows[-2][1]
        ignore = {"fund_relation", "record_hash"}
        diff = sorted(c for c in set(row) | set(prev) if c not in ignore and row.get(c) != prev.get(c))
        if diff:
            mismatch += 1
            detail.append("DIFF %s %s columns=%s" % (rk[0], rk[1], ",".join(diff)))

print("# PARTS total=%d new=%d %s" % (len(keys), len(new_parts), json.dumps(new_parts)))
print("# RELATIONS %s" % json.dumps(counts, sort_keys=True))
for d in detail[:20]:
    print(d)
print("VERIFY reports=%d with_fund_relation=%d from_new_parts=%d predecessor_mismatch=%d gets=%d bytes=%d"
      % (kept, with_rel, new_rows, mismatch, gets, nbytes))
