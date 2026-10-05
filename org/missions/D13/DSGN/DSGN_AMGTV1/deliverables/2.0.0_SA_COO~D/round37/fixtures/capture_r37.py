"""DSGN_AMGTV1 round-37 cut (issuer 2.0.0_SA_COO~D) -- READ-ONLY capture of today's served data for the round-37 repair check.

Same capture_lib as rounds 10-13, 29, 31 and 35 (lambda:Invoke of the deployed opal-amgt-scoped-api, GET routes only, no write call
of any kind). Captures:
  - the collected-chatter route /lead-panel/timeseries/collected/chatter at days 30, 90, 365 (FWD-21: the collage the 365D edge
    labels collide on);
  - for MSFT_US_Equity and AMD_US_Equity: /security/<key>/peers (FWD-8: the per-peer price currency), /overlay and /thesis
    (FWD-10: the date an absent posture carries).
Usage (repo root): python <this file>
Writes: chatter.<days>.json and <route>.<key>.json beside this file, each {_capture_note, payload}.
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = os.path.dirname(os.path.abspath(__file__))
KEYS = ["MSFT_US_Equity", "AMD_US_Equity"]
SEC_ROUTES = ["peers", "overlay", "thesis"]


def _write(fn, cl, sha, stamp, path, query, meta, obj, why):
    doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "query": query,
                             "http": meta.get("status"), "captured_utc": stamp,
                             "by": "2.0.0_SA_COO~D round-37 cut, %s (read-only Lambda invoke)" % why},
           "payload": obj}
    with open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=1, ensure_ascii=True)
        f.write("\n")


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
    for days in (30, 90, 365):
        path = cl.ROUTE_PREFIX + "/lead-panel/timeseries/collected/chatter"
        query = {"days": str(days)}
        obj, meta = cl._invoke(client, path, query)
        fn = "chatter.%d.json" % days
        if obj is None:
            print("MISS %s :: %s" % (fn, json.dumps(meta)[:300]))
            rc = 1
            continue
        _write(fn, cl, sha, stamp, path, query, meta, obj, "FWD-21 collage edge labels")
        rows = obj.get("rows") or []
        print("OK %s http %s, %d rows, top-level keys %s" % (fn, meta.get("status"), len(rows),
                                                            sorted(k for k in obj.keys() if k != "rows")))
    for key in KEYS:
        for route in SEC_ROUTES:
            path = "%s/security/%s/%s" % (cl.ROUTE_PREFIX, key, route)
            obj, meta = cl._invoke(client, path, {})
            fn = "%s.%s.json" % (route, key)
            if obj is None:
                print("MISS %s :: %s" % (fn, json.dumps(meta)[:300]))
                rc = 1
                continue
            _write(fn, cl, sha, stamp, path, {}, meta, obj, "FWD-8 peers currency / FWD-10 no-call date")
            keys = sorted(obj.keys()) if isinstance(obj, dict) else type(obj).__name__
            print("OK %s http %s, top-level keys %s" % (fn, meta.get("status"), keys))
    return rc


if __name__ == "__main__":
    sys.exit(main())
