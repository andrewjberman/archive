"""RIV-d-3 AC1 (LIVE) -- the peer-group map and the Bloomberg channel are served: G0 map_version 1 exists in the real bucket
with 13 rows and both home funds' source_policy home_producer (d-3 amendment 2, Andrew-direct "1b": RIVALS reads the Positioning
pull's landing for IDVZ/PFOE; never home_producer_pending); Bloomberg bronze holds >= 900 imported capture objects (503 IDVZ-group +
441 PFOE-group raws, each with a sidecar) under the builder prefix."""
import io
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

M1 = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~4/m1_home_producer.json"


def run(v):
    import boto3
    import pandas as pd

    root = c.setup_path()
    s3 = boto3.client("s3", region_name="us-east-1")
    g0 = c.address("rivalfunds", "etfs", "gold", "peer_group_map", "date=")[len("s3://opal-data-etfs/"):].rsplit("date=", 1)[0]
    keys = [o["Key"] for p in s3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-etfs", Prefix=g0)
            for o in p.get("Contents", []) if o["Key"].endswith(".parquet")]
    v.check(bool(keys), f"G0 objects under {g0}: {len(keys)}")
    if keys:
        df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket="opal-data-etfs", Key=sorted(keys)[-1])["Body"].read()))
        v.check(len(df) == 13, f"G0 rows {len(df)} == 13")
        m1 = json.loads((root / M1).read_text(encoding="utf-8"))
        print("m-1 verdicts (measurement on record, not the policy):", {f: m1["funds"][f]["verdict"] for f in ("IDVZ", "PFOE")})
        for fund in ("IDVZ", "PFOE"):
            want = "home_producer"  # amendment 2: Andrew-direct "1b" -- homes read the Positioning landing, whatever m-1 measured
            got = list(df[(df["fund_id"] == fund) & (df["role"] == "home")]["source_policy"])
            v.check(got and all(g == want for g in got), f"{fund} home source_policy {got} == {want} (m-1 verdict)")
    pre = c.address("bloomberg", "etfs", "bronze", "holdings", "date=")[len("s3://opal-data-etfs/"):].rsplit("date=", 1)[0]
    raws = sides = 0
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-etfs", Prefix=pre):
        for o in p.get("Contents", []):
            if o["Key"].endswith(".sidecar.json"):
                sides += 1
            else:
                raws += 1
    print(f"bloomberg bronze: {raws} raw, {sides} sidecars under {pre}")
    v.check(raws >= 900 and sides == raws, f">= 900 raws each with a sidecar ({raws}, {sides})")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
