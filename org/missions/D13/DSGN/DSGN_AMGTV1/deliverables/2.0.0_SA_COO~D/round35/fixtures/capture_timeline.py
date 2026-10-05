"""DSGN_AMGTV1 round-35 cut (issuer 2.0.0_SA_COO~D) -- READ-ONLY capture of the served timeline range payload (RESAPP FWD-39).

Same capture_lib as rounds 10-13, 29 and 31 (lambda:Invoke of the deployed opal-amgt-scoped-api, GET routes only, no write call of
any kind). Captures `/security/<key>/timeline` for BA, VLO and AMD (the walk's three names) and for every other key in KEYS, so the
round-35 word-cloud checks read the served `word_cloud` block ({terms: [{term, count}], window: {from, to}, reason}) instead of
guessing it. A key whose served `terms` list is empty is the designed-empty-state control.
Usage (repo root): python <this file> [EXTRA_KEY ...]
Writes: timeline.<key>.json beside this file, each with a `_capture_note`.
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = os.path.dirname(os.path.abspath(__file__))
KEYS = ["BA_US_Equity", "VLO_US_Equity", "AMD_US_Equity", "MSFT_US_Equity", "ASML_NA_Equity", "ROG_SW_Equity"]


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
    for key in KEYS + sys.argv[1:]:
        path = "%s/security/%s/timeline" % (cl.ROUTE_PREFIX, key)
        obj, meta = cl._invoke(client, path, {})
        fn = "timeline.%s.json" % key
        if obj is None:
            print("MISS %s :: %s" % (fn, json.dumps(meta)[:300]))
            rc = 1
            continue
        doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "query": {},
                                 "http": meta.get("status"), "captured_utc": stamp,
                                 "by": "2.0.0_SA_COO~D round-35 cut, FWD-5 word cloud (read-only Lambda invoke)"},
               "payload": obj}
        with open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1, ensure_ascii=True)
            f.write("\n")
        wc = obj.get("word_cloud") if isinstance(obj, dict) else None
        if isinstance(wc, dict):
            terms = wc.get("terms") or []
            print("OK %s http %s, word_cloud %d terms, window %s, reason %r, top %s" % (
                fn, meta.get("status"), len(terms), wc.get("window"), wc.get("reason"), terms[:3]))
        else:
            print("OK %s http %s, NO word_cloud key; top-level keys %s" % (
                fn, meta.get("status"), sorted(obj.keys()) if isinstance(obj, dict) else type(obj).__name__))
    return rc


if __name__ == "__main__":
    sys.exit(main())
