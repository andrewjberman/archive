"""AMGT_RESAPP round 60 -- the overlay a price bar opens shows the bar's own label (CTO round-59 analysis ruling 2).

  --where local                    lib.research.api.scoped_amgt.handler in this tree (live stores, read-only).
  --where deployed --pre <json>    the DEPLOYED opal-amgt-scoped-api; C0 first: CodeSha256 AND LastModified moved off the printed pre.
  --what pre --out <json>          records the deployed CodeSha256 / LastModified before the act.

The controls compare a field the act moves (round-59 ruling 1: never an HTTP status alone):
  C1 the TRENDING/PRICE ranking serves rows, every one keyed (round 59);
  C2 for EVERY ranked row, its overlay's top-level `display_name` is non-empty and equals the row's `display_name`
     (deployed base: the overlay carries no `display_name`);
  C3 AMD_US_Equity and TSM_US_Equity: overlay `name` is a company name (non-empty, not the ticker) equal to the row's display_name;
  C4 the shared identity block is unchanged in kind: AMD/TSM `identity.identity_status` MEASURED, no `display_name` inside it.
Verdict: EVERY BAR OPENS ONTO ITS OWN NAME: YES|NO
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys

import boto3

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"


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
    st, rk = call(PREFIX + "/lead-panel/rankings/trending/price")
    rows = (rk or {}).get("rows") or []
    clause("C1 the ranking serves keyed rows", st == 200 and rows and all(r.get("security_key") for r in rows),
           f"status {st} rows {len(rows)} keyed {sum(1 for r in rows if r.get('security_key'))}")
    bad, overlays = [], {}
    for r in rows:
        k = r.get("security_key")
        if not k:
            continue
        s2, ov = call(PREFIX + "/security/" + k + "/overlay")
        overlays[k] = ov or {}
        got = (ov or {}).get("display_name")
        if s2 != 200 or not got or got != r.get("display_name"):
            bad.append((k, got, r.get("display_name")))
    clause("C2 every overlay display_name equals its row's", rows and not bad, f"{len(bad)} of {len(rows)} differ: {bad[:4]}")
    byk = {r.get("security_key"): r for r in rows}
    named = []
    for k, t in (("AMD_US_Equity", "AMD US"), ("TSM_US_Equity", "TSM US")):
        ov = overlays.get(k) or {}
        nm = ov.get("name")
        named.append(bool(nm) and nm != t and nm == (byk.get(k) or {}).get("display_name"))
        print(f"   {k}: overlay name={nm!r} display_name={ov.get('display_name')!r} row display_name={(byk.get(k) or {}).get('display_name')!r}")
    clause("C3 AMD and TSM overlays carry the company name the bar shows", all(named) and len(named) == 2, "")
    idok = all((overlays.get(k) or {}).get("identity", {}).get("identity_status") == "MEASURED"
               and "display_name" not in ((overlays.get(k) or {}).get("identity") or {}) for k in ("AMD_US_Equity", "TSM_US_Equity"))
    clause("C4 the shared identity block is unchanged in kind", idok, "")
    verdict = all(ok)
    print(f"EVERY BAR OPENS ONTO ITS OWN NAME: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
