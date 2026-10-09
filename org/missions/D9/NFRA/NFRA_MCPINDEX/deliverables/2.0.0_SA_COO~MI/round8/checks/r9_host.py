"""r9_host.py -- runs ON the gateway host (shipped via SSM by r9.AC2.sh / r9.AC3.sh) under /opt/opal-gateway/.venv/bin/python.
Loads /opt/opal-gateway/.env the way systemd's EnvironmentFile does (KEY=VALUE per line, split at the first '='), NEVER
through a shell. Prints only dates, claims, dataset ids and need ids; no env value is printed.

FRESH lines (FWD-13): for 3 keys, the as-of the DEPLOYED discover states vs the served object's own vintage_field, read
independently here with a plain boto3 GetObject.
ROUTE lines (FWD-14, FWD-17): for Alyssa's 6 phrasings and 3 write asks, the deployed discover's first match (need id,
or dataset) and, for a need, its status / op_class / grant field.
"""
import json
import os
import re
import sys

ROOT = "/opt/opal-gateway"
with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v)
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import boto3  # noqa: E402
import yaml  # noqa: E402
from app.graphql_plumbing import catalog_gate as g  # noqa: E402
from app.integrations.opal_discover import integration as od  # noqa: E402

SEG = re.compile(r"\['([^']+)'\]|([^.\[\]]+)")
cat = yaml.safe_load(open(os.path.join(ROOT, "app/refs/DATA_CATALOG.yaml"), encoding="utf-8"))
rows = {str(r.get("key")): r for ch in cat["channels"].values() for r in (ch.get("artifacts") or []) if isinstance(r, dict)}
s3 = boto3.client("s3")
for key in ("json/benchmarks/model_portfolio_benchmarks.json", "platinum/mdpf/{scope}/aum-metrics.json",
            "platinum/mdpf/{scope}/aggregate-aua-timeseries.json"):
    real = key.replace("{scope}", "global")
    try:
        obj = json.loads(s3.get_object(Bucket=cat["bucket"], Key=real)["Body"].read())
        for q, p in SEG.findall(rows[key]["vintage_field"]):
            if q or p:
                obj = obj[q or p]
        served = str(obj)[:10]
    except Exception as exc:  # noqa: BLE001
        served = "UNREAD(%s)" % type(exc).__name__
    m = next((x for x in od.discover(key, g.OPAL_INTERNAL, exact=True).get("matches", [])
              if x.get("dataset") in (key, real)), {})
    lv = (m.get("freshness") or {}).get("latest_value") or {}
    print("FRESH %s stated=%s claim=%s served=%s" % (real, str(lv.get("value"))[:10], lv.get("claim"), served))
ASKS = ["account counts by partner", "cost basis", "statement", "stress test", "download the attachment", "S&P YTD",
        "save an attachment", "move mail", "send a Teams message"]
for i, ask in enumerate(ASKS, 28):
    ms = od.discover(ask, g.OPAL_INTERNAL).get("matches", [])
    first = ms[0] if ms else {}
    need = first.get("need") or {}
    print("ROUTE Q%d first=%s status=%s op_class=%s grant=%s" % (
        i, need.get("id") or first.get("dataset") or "NOT_CATALOGUED", need.get("status"), need.get("op_class"),
        (need.get("grant") or {}).get("allowed") if isinstance(need.get("grant"), dict) else need.get("grant")))
