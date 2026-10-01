"""RIV-d-3 AC3 (LIVE) -- the served trade schedule is income-clean: in the real bucket G5 has trades for every IDVZ rival, none
on a ' Curncy' security, and G6 flow_reconciliation records a non-zero cash-line movement for SCHY; the vehicle gate is on
exactly as the pair names (RIVALFUNDS_BBG_LEG=1 in the vehicle's environment is the one enabling line recorded in d3_live.json)."""
import io
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

REC = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~5/d3_live.json"


def load(s3, table):
    import pandas as pd

    pre = c.address("rivalfunds", "etfs", "gold", table, "date=")[len("s3://opal-data-etfs/"):].rsplit("date=", 1)[0]
    keys = [o["Key"] for p in s3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-etfs", Prefix=pre)
            for o in p.get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return pd.DataFrame()
    return pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket="opal-data-etfs", Key=k)["Body"].read())) for k in keys],
                     ignore_index=True)


def run(v):
    import boto3

    root = c.setup_path()
    s3 = boto3.client("s3", region_name="us-east-1")
    t = load(s3, "trade_schedule")
    v.check(len(t) > 0, f"G5 rows {len(t)}")
    if len(t):
        have = set(t["fund_id"])
        v.check(set(c.IDVZ_GROUP[1:]) <= have, f"trades for every IDVZ rival ({sorted(set(c.IDVZ_GROUP[1:]) - have)} missing)")
        v.check(not t["security_id"].astype(str).str.endswith(" Curncy").any(), "no G5 trade on a ' Curncy' security")
    g6 = load(s3, "flow_reconciliation")
    schy = g6[g6["fund_id"] == "SCHY"]["cash_line_delta_base"].abs() if len(g6) else []
    v.check(len(schy) and float(schy.max()) > 0, "SCHY cash-line movement recorded in G6")
    rec = json.loads((root / REC).read_text(encoding="utf-8"))
    v.check(rec.get("vehicle_enable_line") == "RIVALFUNDS_BBG_LEG=1", f"enable line recorded {rec.get('vehicle_enable_line')}")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
