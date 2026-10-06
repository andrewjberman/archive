"""FWD-8 + FWD-27 re-grade census (2.0.0_SA_COO~D, CTO msg 29878) on the deployed opal-amgt-scoped-api: every covered name's
/peers members (ticker shape, ticker_reason, resolved key, all-caps names) and /thesis Model vendor line, plus the Lead Panel price
ranking's names. Read-only Lambda invokes. Writes one JSON report to argv[1]."""
import concurrent.futures as cf
import json
import re
import sys
from collections import Counter

import boto3

sys.path.insert(0, r"C:\Users\Opal Bloomberg\Desktop\ajb_workspace")
from lib.research.coverage import covered_universe  # noqa: E402

lam = boto3.client("lambda", region_name="us-east-1")
CAPS = re.compile(r"^[A-Z0-9 .,&'/()-]{5,}$")


def call(path, query=""):
    ev = {"version": "2.0", "rawPath": path, "rawQueryString": query, "headers": {"x-firm-id": "opal-capital"},
          "queryStringParameters": dict(p.split("=", 1) for p in query.split("&") if "=" in p) or None,
          "requestContext": {"http": {"method": "GET", "path": path}, "requestId": "coo-d-regrade"}, "isBase64Encoded": False}
    out = json.loads(lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(ev).encode())["Payload"].read())
    body = json.loads(out.get("body") or "{}")
    return out.get("statusCode"), (body.get("data", body) if isinstance(body, dict) else body)


def caps(s):
    return bool(s) and bool(CAPS.match(str(s))) and any(ch.isalpha() for ch in str(s))


def per_name(key):
    st, peers = call(f"/api/scoped/amgt/security/{key}/peers")
    members = (peers or {}).get("members") or [] if st == 200 else []
    rows = []
    for m in members:
        t = str(m.get("ticker") or "")
        rows.append({"name": m.get("name"), "display_name": m.get("display_name"), "ticker": t,
                     "numeric": t.isdigit(), "ticker_reason": m.get("ticker_reason"), "security_key": m.get("security_key"),
                     "caps_name": caps(m.get("display_name") or m.get("name"))})
    st2, thesis = call(f"/api/scoped/amgt/security/{key}/thesis")
    blob = json.dumps(thesis) if st2 == 200 else ""
    vendor_line = "Company short name:" in blob
    return key, {"peers_status": st, "members": rows, "thesis_status": st2, "model_vendor_line": vendor_line}


keys = sorted(covered_universe.covered_security_keys())
res = {}
with cf.ThreadPoolExecutor(8) as ex:
    for k, v in ex.map(per_name, keys):
        res[k] = v

st, rank = call("/api/scoped/amgt/lead-panel/rankings/trending/price")
rank_rows = []
if st == 200:
    for r in (rank.get("rows") or rank.get("rankings") or rank.get("items") or []):
        nm = r.get("display_name") or r.get("name")
        rank_rows.append({"ticker": r.get("ticker"), "display_name": r.get("display_name"), "name": r.get("name"), "caps": caps(nm)})

mem = [m for v in res.values() for m in v["members"]]
numeric = [m for m in mem if m["numeric"]]
report = {
    "covered_names": len(keys),
    "peers_200": sum(v["peers_status"] == 200 for v in res.values()),
    "members_total": len(mem),
    "numeric_ticker_members": len(numeric),
    "numeric_with_reason": sum(bool(m["ticker_reason"]) for m in numeric),
    "numeric_with_resolved_key": sum(bool(m["security_key"]) for m in numeric),
    "numeric_neither": sum(not m["ticker_reason"] and not m["security_key"] for m in numeric),
    "distinct_numeric_tickers": len({m["ticker"] for m in numeric}),
    "caps_peer_names": sorted({m["display_name"] or m["name"] for m in mem if m["caps_name"]}),
    "thesis_200": sum(v["thesis_status"] == 200 for v in res.values()),
    "names_with_model_vendor_line": sorted(k for k, v in res.items() if v["model_vendor_line"]),
    "price_rank_status": st,
    "price_rank_rows": len(rank_rows),
    "price_rank_caps_names": sorted({r["display_name"] or r["name"] for r in rank_rows if r["caps"]}),
    "price_rank_keys_seen": sorted(Counter(k for r in (rank.get("rows") or [])[:1] for k in r).keys()) if st == 200 and isinstance(rank, dict) else [],
}
json.dump({"report": report, "per_name": res, "price_rank": rank_rows}, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 12 else f"{len(v)} items") for k, v in report.items()}))
