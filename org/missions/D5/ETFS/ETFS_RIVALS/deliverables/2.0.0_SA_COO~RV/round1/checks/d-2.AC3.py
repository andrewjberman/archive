"""RIV-d-2 AC3 -- the backfill landed FROM AWS: BASG's issuer archive sits in the real issuer bronze prefix for the act
day, at least 300 raw objects whose sidecars say status OK and runtime etfs-rivalfunds-fetch-holdings-lambda (the
Lambda, not a laptop), and the silver/gold/state markers for the newest report exist."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

RECORD = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~5/d2_live.json"


def run(v):
    import boto3

    root = c.setup_path()
    rec = json.loads((root / RECORD).read_text(encoding="utf-8"))
    day, newest = rec["act_day"], rec["newest_basg_report_date"]
    s3 = boto3.client("s3", region_name="us-east-1")

    def keys(uri):
        b, k = uri[5:].split("/", 1)
        out = []
        for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=b, Prefix=k + "/"):
            out += [o["Key"] for o in pg.get("Contents", [])]
        return b, out

    b, bronze = keys(c.address("issuer-site", "etfs", "bronze", "holdings", f"date={day}"))
    raws = [k for k in bronze if k.rsplit("/", 1)[-1].startswith("basg-") and k.endswith(".txt")]
    sides = [k for k in bronze if k.endswith(".json")]
    ok = 0
    for k in sides:
        s = json.loads(s3.get_object(Bucket=b, Key=k)["Body"].read())
        ok += s.get("status") == "OK" and s.get("runtime") == "etfs-rivalfunds-fetch-holdings-lambda"
    v.check(len(raws) >= 300, f"{len(raws)} BASG raw objects in issuer bronze date={day} (>= 300)")
    v.check(ok >= 300, f"{ok} sidecars status OK written by the fetch Lambda (>= 300; {len(sides)} sidecars listed)")
    for label, uri in [("silver", c.address("issuer-site", "etfs", "silver", "holdings", f"date={newest}")),
                       ("canonical_shape", c.address("rivalfunds", "etfs", "gold", "canonical_shape", f"date={newest}")),
                       ("trade_schedule", c.address("rivalfunds", "etfs", "gold", "trade_schedule", f"date={newest}"))]:
        _, ks = keys(uri)
        v.check(any(k.endswith(".parquet") for k in ks), f"{label} parquet exists for the newest report {newest}")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
