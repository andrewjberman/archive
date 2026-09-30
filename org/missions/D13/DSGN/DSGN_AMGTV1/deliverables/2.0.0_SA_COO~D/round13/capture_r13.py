"""DSGN_AMGTV1 round-13 cut -- READ-ONLY captures of the deployed opal-amgt-scoped-api (issuer 2.0.0_SA_COO~D).

Same capture_lib as rounds 10-12 (lambda:Invoke, GET routes only). Two families, each fixture with a `_capture_note`:
  - the per-name /thesis bundles the no-dossier reader is graded on (6501 JP has no dossier; BA, IMB, VLO, 992 HK have one or not);
  - every route the portal's ui-contract fixture set keys, captured LIVE so AV-l-1 can refresh that set from the served shapes,
    plus the Model tab's /versions, /compare, /ledger and the /timeline the old set never fed.
Usage (repo root): python <this file>
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = "org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round13/fixtures"

# (fixture file name, path under the route prefix, query)
PLAN = [
    ("thesisBundle.6501_JP_Equity.json", "/security/6501_JP_Equity/thesis", None),
    ("thesisBundle.BA_US_Equity.json", "/security/BA_US_Equity/thesis", None),
    ("thesisBundle.IMB_LN_Equity.json", "/security/IMB_LN_Equity/thesis", None),
    ("thesisBundle.VLO_US_Equity.json", "/security/VLO_US_Equity/thesis", None),
    ("thesisBundle.992_HK_Equity.json", "/security/992_HK_Equity/thesis", None),
    ("overlay.BA_US_Equity.json", "/security/BA_US_Equity/overlay", None),
    ("overlay.6501_JP_Equity.json", "/security/6501_JP_Equity/overlay", None),
    ("peers.BA_US_Equity.json", "/security/BA_US_Equity/peers", None),
    ("versions.BA_US_Equity.json", "/security/BA_US_Equity/versions", None),
    ("ledger.BA_US_Equity.json", "/security/BA_US_Equity/ledger", None),
    ("timeline.BA_US_Equity.json", "/security/BA_US_Equity/timeline", None),
    ("watchlist.json", "/watchlist", None),
    ("rankings.trending.chatter.json", "/lead-panel/rankings/trending/chatter", None),
    ("timeseries.trending.chatter.json", "/lead-panel/timeseries/trending/chatter", None),
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

    def grab(name, sub, query):
        path = cl.ROUTE_PREFIX + sub
        obj, meta = cl._invoke(client, path, query)
        if obj is None:
            print("MISS %s :: %s" % (name, json.dumps(meta)[:300]))
            return None
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "query": query,
                                 "http": meta.get("status"), "captured_utc": stamp,
                                 "by": "2.0.0_SA_COO~D round-13 cut (read-only Lambda invoke)"},
               "payload": obj}
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1, ensure_ascii=True)
            f.write("\n")
        print("OK %s %s bytes" % (name, meta.get("bytes")))
        return obj

    ok = 0
    for name, sub, query in PLAN:
        if grab(name, sub, query) is not None:
            ok += 1
    with open(os.path.join(OUT, "versions.BA_US_Equity.json"), encoding="utf-8") as f:
        stamps = [v["stamp"] for v in json.load(f)["payload"]["versions"]]
    if grab("compare.BA_US_Equity.oldest-latest.json", "/security/BA_US_Equity/compare", {"from": stamps[0], "to": stamps[-1]}) is not None:
        ok += 1
    total = len(PLAN) + 1
    print("CAPTURED %d of %d" % (ok, total))
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
