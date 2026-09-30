"""DSGN_AMGTV1 round-10 cut -- READ-ONLY captures of the deployed opal-amgt-scoped-api (issuer 2.0.0_SA_COO~D).

Uses AMGT_RESAPP's capture_lib (same event shape, same lambda:Invoke, GET routes only). Writes one fixture per route into
round10/fixtures/, each carrying a `_capture_note` (function, CodeSha256, path, http, captured_utc, by) beside the `payload`.
Usage (repo root): python <this file>
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round10/fixtures"
THESIS = ["IMB_LN_Equity", "AZN_LN_Equity", "6501_JP_Equity", "9433_JP_Equity", "8316_JP_Equity", "8035_JP_Equity",
          "8766_JP_Equity", "TSM_US_Equity"]
OVERLAY = ["IMB_LN_Equity", "AZN_LN_Equity", "6501_JP_Equity", "9433_JP_Equity", "8316_JP_Equity", "8035_JP_Equity",
           "8766_JP_Equity", "TSM_US_Equity"]


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    conf = client.get_function_configuration(FunctionName=cl.FUNCTION)
    sha = conf.get("CodeSha256")
    print("FUNCTION %s CodeSha256 %s LastModified %s" % (cl.FUNCTION, sha, conf.get("LastModified")))
    os.makedirs(OUT, exist_ok=True)
    ok = 0
    todo = [("thesisBundle", k, "/security/%s/thesis" % k) for k in THESIS] + [
        ("overlay", k, "/security/%s/overlay" % k) for k in OVERLAY]
    for kind, key, route in todo:
        path = cl.ROUTE_PREFIX + route
        obj, meta = cl._invoke(client, path)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        if obj is None:
            print("MISS %s %s :: %s" % (kind, key, json.dumps(meta)[:300]))
            continue
        doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "http": meta.get("status"),
                                 "captured_utc": stamp, "by": "2.0.0_SA_COO~D round-10 cut (read-only Lambda invoke)"},
               "payload": obj}
        fn = os.path.join(OUT, "%s.%s.json" % (kind, key))
        with open(fn, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1, ensure_ascii=True)
            f.write("\n")
        ok += 1
        print("OK %s %s %s bytes" % (kind, key, meta.get("bytes")))
    print("CAPTURED %d of %d" % (ok, len(todo)))
    return 0 if ok == len(todo) else 1


if __name__ == "__main__":
    sys.exit(main())
