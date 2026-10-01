"""AMGT_RESAPP round 59 -- every price-ranking row can open a name and shows a name (CTO round-58 analysis ruling 1).

  --where local                    lib.research.api.scoped_amgt.handler in this tree (live stores, read-only).
  --where deployed --pre <json>    the DEPLOYED opal-amgt-scoped-api (capture_lib._invoke; a non-200 is a REFUSAL); C0 first:
                                   CodeSha256 AND LastModified moved off the printed pre values (round-55 ruling 2).
  --what pre --out <json>          records the deployed CodeSha256 / LastModified before the act.

Per axis (TRENDING/PRICE, BREAKOUT/PRICE), printed with the counts beside:
  C1 the ranking serves rows (SERVED); C2 0 rows without `security_key` (deployed base: 62 of 94);
  C3 0 rows without `display_name` (base: no such field; 58 rows without `name`); C4 0 rows whose display_name is a raw key;
  C5 every `security_key` is a covered name (fresh research_dossier read); C6 every row still serves `score_pct` (FWD-34 kept).
Verdict: EVERY PRICE BAR OPENS AND NAMES A COVERED SECURITY: YES|NO
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys

import boto3

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt/lead-panel/rankings/"


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
    if a.where == "deployed":
        cl = _load("capture_lib", CAPTURE_LIB)
        pre = json.load(open(a.pre, encoding="utf-8"))
        now = _config(cl)
        clause("C0 the deployed code moved", now["CodeSha256"] != pre["CodeSha256"] and now["LastModified"] != pre["LastModified"],
               f"CodeSha256 {pre['CodeSha256']} -> {now['CodeSha256']}; LastModified {pre['LastModified']} -> {now['LastModified']}")
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path):
            body, meta = cl._invoke(lam, path)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        from lib.research.api import scoped_amgt

        def call(path):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "bd"}, "queryStringParameters": None})
            return r.get("statusCode"), json.loads(r.get("body") or "null")
    from lib.research.coverage.covered_universe import covered_security_keys

    covered = set(covered_security_keys())
    print(f"denominator: {len(covered)} covered names (fresh read of research_dossier/)")
    for mv in ("trending", "breakout"):
        st, body = call(PREFIX + mv + "/price")
        rows = (body or {}).get("rows") or []
        tag = mv.upper()
        clause(f"C1 {tag} serves rows", st == 200 and (body or {}).get("ranking_status") == "SERVED" and rows,
               f"status {st} ranking_status {(body or {}).get('ranking_status')} rows {len(rows)} as_of {(body or {}).get('as_of_date')}")
        nokey = [r.get("ticker") for r in rows if not r.get("security_key")]
        clause(f"C2 {tag} 0 rows without security_key", not nokey, f"{len(nokey)} of {len(rows)}: {nokey[:6]}")
        noname = [r.get("ticker") for r in rows if not str(r.get("display_name") or "").strip()]
        clause(f"C3 {tag} 0 rows without display_name", not noname,
               f"{len(noname)} of {len(rows)} (rows without `name`: {sum(1 for r in rows if not r.get('name'))})")
        raw = [r.get("ticker") for r in rows if r.get("display_name") and (r.get("display_name") == r.get("security_key")
               or "_Equity" in str(r.get("display_name")))]
        clause(f"C4 {tag} 0 raw-key labels", not raw, f"{len(raw)}")
        foreign = [r.get("security_key") for r in rows if r.get("security_key") and r.get("security_key") not in covered]
        clause(f"C5 {tag} every key is a covered name", not foreign, f"{len(foreign)}: {foreign[:4]}")
        nopct = [r.get("ticker") for r in rows if r.get("score_pct") is None]
        clause(f"C6 {tag} every row still serves score_pct", not nopct, f"{len(nopct)}")
    verdict = all(ok)
    print(f"EVERY PRICE BAR OPENS AND NAMES A COVERED SECURITY: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
