"""AMGT_RESAPP round 57 -- the scoped-API redeploy's served read (FWD-32, FWD-33, FWD-34 on the DEPLOYED function).

CTO round-55 analysis @5a3c8e4462 ruling 2: a served-read criterion compares a field every write moves, with the pre-act value printed
beside it. Here that field is the function's CodeSha256 and LastModified (`--pre <json>` from `--what pre`).

  --what pre  --out <json>     records the live CodeSha256 / LastModified / Version before the act.
  --what post --pre <json>     C0: CodeSha256 AND LastModified both moved off the printed pre values; then runs the round-56 graders
                               (af_1_route.py, af_2_serve.py fwd33 + fwd34) with their call swapped from the LOCAL handler to an
                               invoke of the DEPLOYED `opal-amgt-scoped-api` (capture_lib._invoke; a non-200 is a REFUSAL).
  --what text --pre <json>     C0 as above; then round 56's served-text check (af_7_text.py) against the DEPLOYED function.
Verdict: THE DEPLOYED FUNCTION SERVES THE FRIDAY FEED: YES|NO  (text: ... SERVES EVERY REASON IN PLAIN WORDS)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys

import boto3

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
R56 = ROOT + "/2.0.0_SA_COO~Z/round56/checks/"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _config(cl):
    c = boto3.client("lambda", region_name=cl.REGION).get_function_configuration(FunctionName=cl.FUNCTION)
    return {"CodeSha256": c["CodeSha256"], "LastModified": c["LastModified"], "Version": c.get("Version")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("pre", "post", "text"), required=True)
    ap.add_argument("--out")
    ap.add_argument("--pre")
    a = ap.parse_args()
    cl = _load("capture_lib", CAPTURE_LIB)
    now = _config(cl)
    if a.what == "pre":
        json.dump(now, open(a.out, "w", encoding="utf-8"), indent=1)
        print(f"pre recorded: {now}")
        return 0
    pre = json.load(open(a.pre, encoding="utf-8"))
    moved = now["CodeSha256"] != pre["CodeSha256"] and now["LastModified"] != pre["LastModified"]
    print(f"{'PASS' if moved else 'FAIL'} C0 the deployed code moved -- CodeSha256 {pre['CodeSha256']} -> {now['CodeSha256']}; "
          f"LastModified {pre['LastModified']} -> {now['LastModified']}")
    lam = boto3.client("lambda", region_name=cl.REGION)

    def deployed(path, query=None):
        body, meta = cl._invoke(lam, path, query)
        if body is None:
            print(f"REFUSED: deployed read failed: {json.dumps(meta)[:300]}")
            return meta.get("status"), {"refused": True}
        return 200, body

    if a.what == "text":
        a7 = _load("af_7_text", R56 + "af_7_text.py")
        a7._call = deployed
        sys.argv = ["af_7_text.py"]
        print("== SERVED TEXT (deployed)")
        ok = a7.main() == 0
        verdict = moved and ok
        print(f"THE DEPLOYED FUNCTION SERVES EVERY REASON IN PLAIN WORDS: {'YES' if verdict else 'NO'}")
        return 0 if verdict else 1
    results = []
    a1 = _load("af_1_route", R56 + "af_1_route.py")
    a1._live_body = lambda: deployed(a1.PATH)
    sys.argv = ["af_1_route.py"]
    print("== FWD-32 (deployed)")
    results.append(a1.main() == 0)
    a2 = _load("af_2_serve", R56 + "af_2_serve.py")
    a2._call = deployed
    for w in ("fwd33", "fwd34"):
        print(f"== {w.upper()} (deployed)")
        sys.argv = ["af_2_serve.py", "--what", w]
        results.append(a2.main() == 0)
    verdict = moved and all(results)
    print(f"THE DEPLOYED FUNCTION SERVES THE FRIDAY FEED: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
