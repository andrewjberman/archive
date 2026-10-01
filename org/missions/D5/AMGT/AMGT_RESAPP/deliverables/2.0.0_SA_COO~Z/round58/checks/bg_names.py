"""AMGT_RESAPP round 58 -- every covered row of the monthly chatter route carries a person-readable display_name.

CTO ruling msg 27675 (row Z-S331): 0 of 95 rows serve their security_key as display_name; the fallback is the plain ticker, never
the raw key.

  --where local                      calls lib.research.api.scoped_amgt.handler in this tree (live gold, read-only).
  --where deployed --pre <json>      invokes the DEPLOYED opal-amgt-scoped-api (capture_lib._invoke; a non-200 is a REFUSAL);
                                     C0 first: CodeSha256 AND LastModified moved off the printed pre values (round-55 ruling 2).
  --what pre --out <json>            records the deployed function's CodeSha256 / LastModified before a redeploy.

Clauses: C1 one row per covered name (fresh denominator); C2 0 rows whose display_name equals the security_key; C3 0 rows whose
display_name carries the key form (an `_Equity` suffix or `-SLASH-`); C4 every display_name non-empty; C5 the route still passes
round 56's af_1_route.py grader on the same body (the counts did not move).
Verdict: EVERY COVERED BUBBLE IS NAMED FOR A PERSON: YES|NO
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys

import boto3

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
AF1 = ROOT + "/2.0.0_SA_COO~Z/round56/checks/af_1_route.py"
PATH = "/api/scoped/amgt/lead-panel/timeseries/collected/chatter"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _config(cl):
    c = boto3.client("lambda", region_name=cl.REGION).get_function_configuration(FunctionName=cl.FUNCTION)
    return {"CodeSha256": c["CodeSha256"], "LastModified": c["LastModified"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", choices=("local", "deployed"))
    ap.add_argument("--what", choices=("pre",))
    ap.add_argument("--out")
    ap.add_argument("--pre")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.what == "pre":
        cl = _load("capture_lib", CAPTURE_LIB)
        now = _config(cl)
        json.dump(now, open(a.out, "w", encoding="utf-8"), indent=1)
        print(f"pre recorded: {now}")
        return 0
    af1 = _load("af_1_route", AF1)
    if a.where == "deployed":
        cl = _load("capture_lib", CAPTURE_LIB)
        pre = json.load(open(a.pre, encoding="utf-8"))
        now = _config(cl)
        clause("C0 the deployed code moved", now["CodeSha256"] != pre["CodeSha256"] and now["LastModified"] != pre["LastModified"],
               f"CodeSha256 {pre['CodeSha256']} -> {now['CodeSha256']}; LastModified {pre['LastModified']} -> {now['LastModified']}")
        lam = boto3.client("lambda", region_name=cl.REGION)
        body, meta = cl._invoke(lam, PATH)
        status = 200 if body is not None else meta.get("status")
    else:
        status, body = af1._live_body()
    if status != 200 or not isinstance(body, dict):
        clause("C1 route answered 200", False, f"status {status}")
        print("EVERY COVERED BUBBLE IS NAMED FOR A PERSON: NO")
        return 1
    from lib.research.coverage.covered_universe import covered_security_keys

    covered = covered_security_keys()
    rows = body.get("rows") or []
    print(f"denominator: {len(covered)} covered names (fresh read of research_dossier/); {len(rows)} rows served")
    clause("C1 one row per covered name", sorted(r.get("security_key") for r in rows) == covered, "")
    eq = [r["security_key"] for r in rows if (r.get("display_name") or "") == r.get("security_key")]
    clause("C2 0 rows serve the security_key as display_name", not eq, f"{len(eq)} of {len(rows)}: {eq[:5]}")
    kf = [(r["security_key"], r.get("display_name")) for r in rows
          if "_Equity" in str(r.get("display_name")) or "-SLASH-" in str(r.get("display_name"))]
    clause("C3 0 rows carry the key form", not kf, f"{len(kf)}: {kf[:4]}")
    empty = [r["security_key"] for r in rows if not str(r.get("display_name") or "").strip()]
    clause("C4 every display_name non-empty", not empty, f"{len(empty)}")
    af1._live_body = lambda: (200, body)
    sys.argv = ["af_1_route.py"]
    print("== C5: round 56's FWD-32 grader on the same body")
    clause("C5 the counts did not move", af1.main() == 0, "")
    verdict = all(ok)
    print(f"EVERY COVERED BUBBLE IS NAMED FOR A PERSON: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
