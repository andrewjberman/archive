"""RIV-d-3 AC2 (LIVE) -- the served page is grouped and the coverage is real: the newest platinum page (written by
rivalfunds-publish-page-lambda) carries data-group="IDVZ" and data-group="PFOE"; G2 in the real bucket, for the imported
IDVZ-group window, reads per fund a count of status new within 2% of CRO~Z's census (SCHY 501, INEQ 498, CGIC 496, BIDD 464,
TXUE 417 dated days)."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

CENSUS = {"SCHY": 501, "INEQ": 498, "CGIC": 496, "BIDD": 464, "TXUE": 417}


def run(v):
    import boto3
    import pandas as pd

    c.setup_path()
    s3 = boto3.client("s3", region_name="us-east-1")
    pre = c.address("rivalfunds", "etfs", "platinum", "page", "date=")[len("s3://opal-data-etfs/"):].rsplit("date=", 1)[0]
    idx = sorted(o["Key"] for p in s3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-etfs", Prefix=pre)
                 for o in p.get("Contents", []) if o["Key"].endswith("/index.html") and "/revisions/" not in o["Key"])
    v.check(bool(idx), f"served pages {len(idx)}")
    if idx:
        obj = s3.get_object(Bucket="opal-data-etfs", Key=idx[-1])
        html = obj["Body"].read().decode("utf-8")
        v.check('data-group="IDVZ"' in html and 'data-group="PFOE"' in html, f"{idx[-1]} is grouped (IDVZ and PFOE)")
    g2 = c.address("rivalfunds", "etfs", "gold", "holdings_coverage", "date=")[len("s3://opal-data-etfs/"):].rsplit("date=", 1)[0]
    keys = [o["Key"] for p in s3.get_paginator("list_objects_v2").paginate(Bucket="opal-data-etfs", Prefix=g2)
            for o in p.get("Contents", []) if o["Key"].endswith(".parquet")]
    v.check(bool(keys), f"G2 objects {len(keys)}")
    if keys:
        df = pd.concat([pd.read_parquet(io.BytesIO(s3.get_object(Bucket="opal-data-etfs", Key=k)["Body"].read())) for k in keys],
                       ignore_index=True)
        df = df[(df["selected"] == True) & (df["expected_date"].astype(str).str[:10] <= "2026-09-29")]  # noqa: E712
        for f, n in CENSUS.items():
            got = int(((df["fund_id"] == f) & (df["status"] == "new")).sum())
            v.check(abs(got - n) <= max(2, int(0.02 * n)), f"{f}: {got} new days vs census {n}")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
