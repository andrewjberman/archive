"""FWD-4 re-grade census (2.0.0_SA_COO~D, CTO msg 29800): every covered name's deployed /overlay header -- the seven key
figures, each a value, a reasoned null ("Bloomberg returned no value" = accounted for; "not in the latest stored pull" = our gap),
or silent. Read-only Lambda invokes of the deployed opal-amgt-scoped-api. Writes one JSON report."""
import concurrent.futures as cf
import json
import sys
from collections import Counter
import boto3
sys.path.insert(0, r"C:\Users\Opal Bloomberg\Desktop\ajb_workspace")
from lib.research.coverage import covered_universe

SEVEN = [("price", ["PX_LAST"]), ("market cap", ["CUR_MKT_CAP"]), ("enterprise value", ["CURR_ENTP_VAL"]),
         ("net debt", ["NET_DEBT"]), ("beta", ["EQY_BETA"]), ("average volume", ["VOLUME_AVG_30D"]),
         ("short interest", ["SHORT_INT_RATIO", "SI_PERCENT_EQUITY_FLOAT"])]
lam = boto3.client("lambda", region_name="us-east-1")
keys = sorted(covered_universe.covered_security_keys())

def read(key):
    p = f"/api/scoped/amgt/security/{key}/overlay"
    ev = {"version": "2.0", "rawPath": p, "rawQueryString": "", "headers": {"x-firm-id": "opal-capital"},
          "requestContext": {"http": {"method": "GET", "path": p}, "requestId": f"coo-d-fwd4-{key}"}, "isBase64Encoded": False}
    r = lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(ev).encode())
    out = json.loads(r["Payload"].read())
    if out.get("statusCode") != 200:
        return key, {"status": out.get("statusCode"), "figures": None}
    b = json.loads(out["body"])
    b = b.get("data", b)
    hf = b.get("header_figures") or []
    row = {}
    for label, mns in SEVEN:
        ents = [f for f in hf if f.get("mnemonic") in mns]
        val = next((f for f in ents if f.get("value") is not None), None)
        if val:
            row[label] = {"state": "VALUE"}
            continue
        reason = next((str(f.get("reason")).strip() for f in ents if str(f.get("reason") or "").strip()), None)
        if not reason:
            row[label] = {"state": "SILENT"}
        elif reason.startswith("Bloomberg returned no value"):
            row[label] = {"state": "VENDOR_EMPTY", "reason": reason}
        elif "not in the latest stored pull" in reason:
            row[label] = {"state": "NOT_IN_PULL", "reason": reason}
        else:
            row[label] = {"state": "OTHER_REASON", "reason": reason}
    return key, {"status": 200, "figures": row}

res = {}
with cf.ThreadPoolExecutor(8) as ex:
    for k, v in ex.map(read, keys):
        res[k] = v
tally = Counter(s["state"] for v in res.values() if v["figures"] for s in v["figures"].values())
not_ok = sorted(k for k, v in res.items() if v["status"] != 200)
gap = {k: sorted(fig for fig, s in v["figures"].items() if s["state"] == "NOT_IN_PULL") for k, v in res.items() if v["figures"]}
gap = {k: v for k, v in gap.items() if v}
silent = {k: sorted(fig for fig, s in v["figures"].items() if s["state"] == "SILENT") for k, v in res.items() if v["figures"]}
silent = {k: v for k, v in silent.items() if v}
complete = sorted(k for k, v in res.items() if v["figures"] and all(s["state"] == "VALUE" for s in v["figures"].values()))
report = {"covered_names": len(keys), "read_200": len(keys) - len(not_ok), "non_200": not_ok, "cell_tally": dict(tally),
          "names_all_seven_values": len(complete), "names_with_not_in_pull": len(gap), "not_in_pull_by_name": gap,
          "names_with_silent": len(silent), "silent_by_name": silent,
          "not_in_pull_by_figure": dict(Counter(fig for v in gap.values() for fig in v))}
json.dump({"report": report, "per_name": res}, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
print(json.dumps({k: report[k] for k in ("covered_names", "read_200", "non_200", "cell_tally", "names_all_seven_values",
                                          "names_with_not_in_pull", "not_in_pull_by_figure", "names_with_silent")}))
