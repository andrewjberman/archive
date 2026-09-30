"""DSGN_AMGTV1 round-11 cut -- READ-ONLY captures of the deployed opal-amgt-scoped-api (issuer 2.0.0_SA_COO~D).

The /ledger, /versions and /compare routes (AMGT_RESAPP, served and mounted; the portal has no caller yet). Same capture_lib as
round 10 (same event shape, lambda:Invoke, GET routes only). One fixture per route per name in round11/fixtures/, each with a
`_capture_note`. Usage (repo root): python <this file>
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round11/fixtures"
NAMES = ["BA_US_Equity", "VLO_US_Equity", "IMB_LN_Equity", "AZN_LN_Equity"]
LEAVES = ["ledger", "versions", "compare"]


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
    total = 0
    for key in NAMES:
        for leaf in LEAVES:
            total += 1
            path = "%s/security/%s/%s" % (cl.ROUTE_PREFIX, key, leaf)
            obj, meta = cl._invoke(client, path)
            stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            if obj is None:
                print("MISS %s %s :: %s" % (leaf, key, json.dumps(meta)[:300]))
                continue
            doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "http": meta.get("status"),
                                     "captured_utc": stamp, "by": "2.0.0_SA_COO~D round-11 cut (read-only Lambda invoke)"},
                   "payload": obj}
            fn = os.path.join(OUT, "%s.%s.json" % (leaf, key))
            with open(fn, "w", encoding="utf-8", newline="\n") as f:
                json.dump(doc, f, indent=1, ensure_ascii=True)
                f.write("\n")
            ok += 1
            print("OK %s %s %s bytes" % (leaf, key, meta.get("bytes")))
    print("CAPTURED %d of %d" % (ok, total))
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
