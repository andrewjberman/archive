"""DSGN_AMGTV1 round-30 cut (issuer 2.0.0_SA_COO~D) -- READ-ONLY capture of the served rolling windows (RESAPP FWD-36).

Same capture_lib as rounds 10-13 and 29 (lambda:Invoke of the deployed opal-amgt-scoped-api, GET routes only, no write call of any
kind). Captures, for days in 30 / 90 / 365, the collected-chatter route and the trending price ranking, so round 30's FWD-26 checks
read the served window shape (window start, "since <date>", the price "not produced yet" reason) instead of guessing it.
Usage (repo root): python <this file>
Writes: windows.<route>.<days>.json beside this file, each with a `_capture_note`.
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = os.path.dirname(os.path.abspath(__file__))
ROUTES = {"chatter": "/lead-panel/timeseries/collected/chatter", "price": "/lead-panel/rankings/trending/price"}


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    conf = client.get_function_configuration(FunctionName=cl.FUNCTION)
    sha = conf.get("CodeSha256")
    print("FUNCTION %s CodeSha256 %s LastModified %s" % (cl.FUNCTION, sha, conf.get("LastModified")))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rc = 0
    for name, sub in ROUTES.items():
        for days in (30, 90, 365):
            path = cl.ROUTE_PREFIX + sub
            obj, meta = cl._invoke(client, path, {"days": str(days)})
            fn = "windows.%s.%d.json" % (name, days)
            if obj is None:
                print("MISS %s :: %s" % (fn, json.dumps(meta)[:300]))
                rc = 1
                continue
            doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "query": {"days": str(days)},
                                     "http": meta.get("status"), "captured_utc": stamp,
                                     "by": "2.0.0_SA_COO~D round-30 cut, FWD-26 checks (read-only Lambda invoke)"},
                   "payload": obj}
            with open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n") as f:
                json.dump(doc, f, indent=1, ensure_ascii=True)
                f.write("\n")
            rows = obj.get("rows") or []
            keys = sorted(k for k in obj.keys() if k != "rows")
            print("OK %s http %s, %d rows, top-level keys %s" % (fn, meta.get("status"), len(rows), keys))
            if rows:
                print("   row keys: %s" % sorted(rows[0].keys()))
    return rc


if __name__ == "__main__":
    sys.exit(main())
