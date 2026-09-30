"""DSGN_AMGTV1 round-12 cut -- READ-ONLY captures of the deployed opal-amgt-scoped-api (issuer 2.0.0_SA_COO~D).

Same capture_lib as rounds 10-11 (lambda:Invoke, GET routes only). One fixture per route per name in round12/fixtures/, each
with a `_capture_note`. Usage (repo root): python <this file>
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round12/fixtures"

# (fixture file name, route leaf under /security/<key>/, key, query)
PLAN = [
    ("versions.BA_US_Equity.json", "versions", "BA_US_Equity", None),
    ("versions.VLO_US_Equity.json", "versions", "VLO_US_Equity", None),
    ("versions.IMB_LN_Equity.json", "versions", "IMB_LN_Equity", None),
    ("versions.AZN_LN_Equity.json", "versions", "AZN_LN_Equity", None),
    ("thesisBundle.BA_US_Equity.json", "thesis", "BA_US_Equity", None),
    ("overlay.BA_US_Equity.json", "overlay", "BA_US_Equity", None),
    ("thesisBundle.IMB_LN_Equity.json", "thesis", "IMB_LN_Equity", None),
    ("timeline.992_HK_Equity.json", "timeline", "992_HK_Equity", None),
    ("timelineDay.992_HK_Equity.2026-08-13.json", "timeline/day/2026-08-13", "992_HK_Equity", None),
    ("timeline.6501_JP_Equity.json", "timeline", "6501_JP_Equity", None),
    ("timeline.BA_US_Equity.json", "timeline", "BA_US_Equity", None),
    ("timelineDay.BA_US_Equity.2026-09-08.json", "timeline/day/2026-09-08", "BA_US_Equity", None),
]


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    conf = client.get_function_configuration(FunctionName=cl.FUNCTION)
    sha = conf.get("CodeSha256")
    print("FUNCTION %s CodeSha256 %s LastModified %s" % (cl.FUNCTION, sha, conf.get("LastModified")))
    os.makedirs(OUT, exist_ok=True)
    plan = list(PLAN)
    ok = 0
    # the compare runs after versions so it spans the oldest and newest stamps served NOW
    vpath = os.path.join(OUT, "versions.BA_US_Equity.json")
    for name, leaf, key, query in plan:
        path = "%s/security/%s/%s" % (cl.ROUTE_PREFIX, key, leaf)
        obj, meta = cl._invoke(client, path, query)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        if obj is None:
            print("MISS %s :: %s" % (name, json.dumps(meta)[:300]))
            continue
        doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "query": query,
                                 "http": meta.get("status"), "captured_utc": stamp,
                                 "by": "2.0.0_SA_COO~D round-12 cut (read-only Lambda invoke)"},
               "payload": obj}
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1, ensure_ascii=True)
            f.write("\n")
        ok += 1
        print("OK %s %s bytes" % (name, meta.get("bytes")))
    total = len(plan) + 1
    with open(vpath, encoding="utf-8") as f:
        stamps = [v["stamp"] for v in json.load(f)["payload"]["versions"]]
    query = {"from": stamps[0], "to": stamps[-1]}
    path = "%s/security/BA_US_Equity/compare" % cl.ROUTE_PREFIX
    obj, meta = cl._invoke(client, path, query)
    if obj is None:
        print("MISS compare :: %s" % json.dumps(meta)[:300])
    else:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "query": query,
                                 "http": meta.get("status"), "captured_utc": stamp,
                                 "by": "2.0.0_SA_COO~D round-12 cut (read-only Lambda invoke)"},
               "payload": obj}
        with open(os.path.join(OUT, "compare.BA_US_Equity.oldest-latest.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1, ensure_ascii=True)
            f.write("\n")
        ok += 1
        print("OK compare %s -> %s" % (stamps[0], stamps[-1]))
    print("CAPTURED %d of %d" % (ok, total))
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
