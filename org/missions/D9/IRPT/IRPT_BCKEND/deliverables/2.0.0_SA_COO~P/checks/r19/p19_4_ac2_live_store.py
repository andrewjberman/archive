"""IB-pr-194 AC2 -- the seam probe against the REAL retained store, read-only: the reopen predicate flags exactly
the two NEW-01 reports and no other.

Usage: python p19_4_ac2_live_store.py <worktree root>
Reads DynamoDB irpt-requests (tenant 49financial, REPORT# rows) and each row's S3 blob by version id, then applies
retained.implausible_engine_series(report) from the worktree's retained.py. No write.
Measured by the COO at the cut (2026-09-28 ~22:2xZ): 23 retained 49F PERFORMANCE reports, all OPAL_ENGINE; exactly
2 carry a daily_cumulative_series value <= -1.0 -- revisions 790fe675 (1Y) and 74fb35a4 (YTD), both the NEW-01
account; 0 near-misses.
Pass: the predicate exists, flags exactly {790fe675, 74fb35a4}, and passes the other rows.
"""
import json
import sys
from pathlib import Path

import boto3
from boto3.dynamodb.conditions import Key

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _engine_path import install  # noqa: E402

root, package = install(sys.argv[1] if len(sys.argv) > 1 else ".")
sys.path.insert(0, str(package.parent / "reports"))
import retained  # noqa: E402

EXPECTED = {"790fe675", "74fb35a4"}


def query_all(table):
    items, kw = [], dict(KeyConditionExpression=Key("tenant").eq("49financial") & Key("request_revision").begins_with("REPORT#"))
    while True:
        result = table.query(**kw)
        items += result["Items"]
        if "LastEvaluatedKey" not in result:
            return items
        kw["ExclusiveStartKey"] = result["LastEvaluatedKey"]


ok = True
pred = getattr(retained, "implausible_engine_series", None)
if not callable(pred):
    print("FAIL: retained.implausible_engine_series is not defined")
    ok = False
else:
    table = boto3.resource("dynamodb").Table("irpt-requests")
    s3 = boto3.client("s3")
    items = query_all(table)
    flagged, passed = set(), 0
    for it in items:
        blob = it["blob"]
        record = json.loads(s3.get_object(Bucket=blob["bucket"], Key=blob["key"], VersionId=blob["version_id"])["Body"].read())
        revision = (it.get("ref") or {}).get("revision", "")[:8]
        if pred(record.get("report") or {}):
            flagged.add(revision)
        else:
            passed += 1
    print("retained 49F reports read: %d | flagged: %s | passed: %d" % (len(items), sorted(flagged), passed))
    if flagged != EXPECTED:
        print("FAIL: flagged %s, expected exactly %s" % (sorted(flagged), sorted(EXPECTED)))
        ok = False
if ok:
    print("P19-4-AC2 PASS")
else:
    print("P19-4-AC2 FAIL")
sys.exit(0 if ok else 1)
