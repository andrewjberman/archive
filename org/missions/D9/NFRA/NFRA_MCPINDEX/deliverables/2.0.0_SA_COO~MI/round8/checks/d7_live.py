"""d7_live.py -- MX-d-7 AC2 instrument (FWD-13): for three catalogued datasets, the as-of discover STATES equals the
as-of the served artifact CARRIES, read independently.

Discover runs from THIS worktree's code (app.integrations.opal_discover), opal-internal principal, exact key match, with
its own default S3 path. The independent read is a separate boto3 GetObject of the same key in this script, resolving the
catalog row's `vintage_field` path itself (a dotted path with ['...'] segments). The two are compared as strings.
Read-only: nothing is written, nothing leaves Opal's AWS. Prints one line per dataset and a total.
Usage: python d7_live.py <gateway_root>
"""
import json
import re
import sys

GW = sys.argv[1]
sys.path.insert(0, GW)
import boto3  # noqa: E402
import yaml  # noqa: E402

from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

KEYS = ["json/benchmarks/model_portfolio_benchmarks.json",
        "platinum/mdpf/{scope}/aum-metrics.json",
        "platinum/mdpf/{scope}/aggregate-aua-timeseries.json"]
SEG = re.compile(r"\['([^']+)'\]|([^.\[\]]+)")


def resolve(obj, path):
    for quoted, plain in SEG.findall(path):
        part = quoted or plain
        if not part:
            continue
        obj = obj[part]
    return obj


cat = yaml.safe_load(open(GW + "/app/refs/DATA_CATALOG.yaml", encoding="utf-8"))
bucket = cat["bucket"]
rows = {}
for ch in cat["channels"].values():
    for r in (ch.get("artifacts") or []):
        if isinstance(r, dict):
            rows[str(r.get("key"))] = r
s3 = boto3.client("s3")
ok = 0
for key in KEYS:
    row = rows.get(key)
    if row is None:
        print("%s: NO CATALOG ROW" % key)
        continue
    real_key = key.replace("{scope}", "global")
    try:
        body = json.loads(s3.get_object(Bucket=bucket, Key=real_key)["Body"].read())
        served = str(resolve(body, row["vintage_field"]))[:10]
    except Exception as exc:  # noqa: BLE001
        served = "UNREAD(%s)" % type(exc).__name__
    ans = od.discover(key, g.OPAL_INTERNAL, exact=True)
    m = next((x for x in ans.get("matches", []) if x.get("dataset") in (key, real_key)), None)
    lv = ((m or {}).get("freshness") or {}).get("latest_value") or {}
    stated = str(lv.get("value"))[:10] if lv.get("value") else "NONE"
    claim = lv.get("claim")
    equal = stated == served and claim == "measured"
    ok += 1 if equal else 0
    print("%s: field=%s stated=%s claim=%s served=%s %s" % (real_key, row["vintage_field"], stated, claim, served,
                                                            "EQUAL" if equal else "DIFFERENT"))
print("stated as-of equals served as-of (claim measured) for %d of %d datasets" % (ok, len(KEYS)))
sys.exit(0 if ok == len(KEYS) else 1)
