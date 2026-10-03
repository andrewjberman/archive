"""DSGN_AMGTV1 round-29 cut, AV-zg-3 (cell-slug leadprice) -- READ-ONLY capture of the served Trending x Price ranking.

Same capture_lib as rounds 10-13 (lambda:Invoke of the deployed opal-amgt-scoped-api, GET route only, no write call of any
kind). Why: the portal fixture uiContractFixtures.json at base dcdc89b1 carries the round-7 32-row price set (9 gainers), so it
cannot show a face that keeps 10 gainers and 10 losers at rest with names left over; the live route served 94 rows on
2026-10-02 (served-reread-20261002/read-20261002T184239Z price_rows 94).
Usage (repo root): python <this file>
Writes: rankings.trending.price.live.json beside this file, with a `_capture_note`.
"""
import datetime
import importlib.util
import json
import os
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
OUT = os.path.dirname(os.path.abspath(__file__))
NAME = "rankings.trending.price.live.json"
SUB = "/lead-panel/rankings/trending/price"


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    conf = client.get_function_configuration(FunctionName=cl.FUNCTION)
    sha = conf.get("CodeSha256")
    print("FUNCTION %s CodeSha256 %s LastModified %s" % (cl.FUNCTION, sha, conf.get("LastModified")))
    path = cl.ROUTE_PREFIX + SUB
    obj, meta = cl._invoke(client, path, None)
    if obj is None:
        print("MISS %s :: %s" % (NAME, json.dumps(meta)[:300]))
        return 1
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    doc = {"_capture_note": {"function": cl.FUNCTION, "code_sha256": sha, "path": path, "query": None,
                             "http": meta.get("status"), "captured_utc": stamp,
                             "by": "2.0.0_SA_COO~D round-29 cut, AV-zg-3 checks (read-only Lambda invoke)"},
           "payload": obj}
    with open(os.path.join(OUT, NAME), "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=1, ensure_ascii=True)
        f.write("\n")
    rows = obj.get("rows") or []
    print("OK %s %s bytes, %d rows, as_of_date %s, generation %s" % (NAME, meta.get("bytes"), len(rows), obj.get("as_of_date"), obj.get("generation_id")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
