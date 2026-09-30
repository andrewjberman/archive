"""Round 26 AC (IB-pr-263, row S219) -- the two 49F twr_daily partitions that miss four declared columns carry them,
and their neighbours are untouched.

Usage: python p26_3_ac1_twr_daily_gap_filled.py <worktree root>
Reads the BEFORE record at <root>/org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/checks/r26/
twr_daily_partition_etags_BEFORE_20260930.json (bucket from lib.opal_naming at the cut), then:
  - for each gap partition (date=2024-07-08, date=2025-01-09): GetObject data.parquet, columns must include
    bmv, emv, cf_net, cf_gross AND every column the BEFORE shape had (account_id, business_date, r_net, r_gross, status,
    schema_version, ...), and the row count must be > 0;
  - for each neighbour partition: HeadObject ETag must EQUAL the BEFORE record (the fill touched nothing else).
Pass line: P26-3-AC1 PASS. Base (at the cut): FAIL -- both gap partitions lack the four columns (row S219's read).
"""
import io
import json
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
before_p = root / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/checks/r26/twr_daily_partition_etags_BEFORE_20260930.json"
NEEDED = {"bmv", "emv", "cf_net", "cf_gross"}
BASE_COLS = {"account_id", "business_date", "r_net", "r_gross", "status", "schema_version"}


def fail(msg):
    print("P26-3-AC1 FAIL: " + msg)
    sys.exit(1)


before = json.loads(before_p.read_text(encoding="utf-8"))
bucket = before["bucket"]
s3 = boto3.client("s3", region_name="us-east-1")

for d in before["gap_partitions"]:
    key = before["partitions"][d]["key"]
    try:
        body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    except Exception as exc:  # noqa: BLE001
        fail("GetObject %s: %s" % (key, str(exc)[:120]))
    tbl = pq.read_table(io.BytesIO(body))
    cols = set(tbl.column_names)
    missing = sorted((NEEDED | BASE_COLS) - cols)
    if missing:
        fail("date=%s missing columns %s (has %d columns, %d rows)" % (d, missing, len(cols), tbl.num_rows))
    if tbl.num_rows == 0:
        fail("date=%s has 0 rows" % d)
    print("  date=%s OK: %d rows, %d columns incl. %s" % (d, tbl.num_rows, len(cols), sorted(NEEDED)))

for d in before["neighbour_partitions"]:
    rec = before["partitions"][d]
    try:
        h = s3.head_object(Bucket=bucket, Key=rec["key"])
    except Exception as exc:  # noqa: BLE001
        fail("HeadObject %s: %s" % (rec["key"], str(exc)[:120]))
    if h["ETag"] != rec["etag"]:
        fail("neighbour date=%s CHANGED: etag %s != BEFORE %s" % (d, h["ETag"], rec["etag"]))
    print("  neighbour date=%s untouched (etag %s)" % (d, h["ETag"]))
print("P26-3-AC1 PASS")
