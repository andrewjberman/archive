"""AMGT_RESAPP round 61 -- a company name on every row of the price ranking and the chatter set
(DSGN_AMGTV1 round-21 analysis @e14de1769c section 3B cell B1, FWD-2).

  --where local                    lib.research.api.scoped_amgt.handler in this tree (live stores, read-only).
  --where local --mutant           the same, with the model-block name step removed (must FAIL: the instrument discriminates).
  --where deployed --pre <json>    the DEPLOYED opal-amgt-scoped-api; C0 first: CodeSha256 AND LastModified moved off the printed pre.
  --what pre --out <json>          records the deployed CodeSha256 / LastModified before the act.

Clauses (each reads a field the act moves, never an HTTP status alone):
  C1 TRENDING/PRICE and BREAKOUT/PRICE: rows served, 0 rows without `name`, and no `name` equal to its ticker root;
  C2 positive control on one of the 24 the base leaves unnamed: RMS_FP_Equity's ranked `name` is a company name;
  C3 the chatter set: 0 rows whose `name_source` is `ticker`; BABA, COST, KPN and NOVN carry a name, not their ticker;
  C4 the overlay RMS_FP_Equity opens serves the row's `display_name`.
Verdict: EVERY PRICE BAR AND BUBBLE CARRIES A COMPANY NAME: YES|NO
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
BUBBLES = ("BABA_US_Equity", "COST_US_Equity", "KPN_NA_Equity", "NOVN_SW_Equity")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _config(cl):
    c = boto3.client("lambda", region_name=cl.REGION).get_function_configuration(FunctionName=cl.FUNCTION)
    return {"CodeSha256": c["CodeSha256"], "LastModified": c["LastModified"]}


def _root(ticker):
    return str(ticker or "").strip().split(" ")[0].upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", choices=("local", "deployed"))
    ap.add_argument("--what", choices=("pre",))
    ap.add_argument("--out")
    ap.add_argument("--pre")
    ap.add_argument("--mutant", action="store_true")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.what == "pre":
        now = _config(_load("capture_lib", CAPTURE_LIB))
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

        if a.mutant:
            scoped_amgt._model_block_name = lambda key: None
            print("MUTANT: the model-block name step returns None (the base's behaviour)")

        def call(path):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "bd"}, "queryStringParameters": None})
            return r.get("statusCode"), json.loads(r.get("body") or "null")

    trending = []
    for kind in ("trending/price", "breakout/price"):
        st, body = call(PREFIX + "/lead-panel/rankings/" + kind)
        rows = (body or {}).get("rows") or []
        unnamed = [r.get("security_key") for r in rows if not r.get("name")]
        ticker_named = [r.get("security_key") for r in rows if r.get("name") and str(r["name"]).strip().upper() == _root(r.get("ticker"))]
        clause(f"C1 {kind} names every row", st == 200 and rows and not unnamed and not ticker_named,
               f"status {st} rows {len(rows)} unnamed {len(unnamed)} {unnamed[:6]} ticker-as-name {len(ticker_named)}")
        if kind == "trending/price":
            trending = rows
    rms = next((r for r in trending if r.get("security_key") == "RMS_FP_Equity"), {})
    clause("C2 positive control RMS_FP_Equity is named", bool(rms.get("name")) and _root(rms.get("ticker")) != str(rms.get("name")).upper(),
           f"name={rms.get('name')!r} name_source={rms.get('name_source')!r}")
    st, body = call(PREFIX + "/lead-panel/timeseries/collected/chatter")
    crows = (body or {}).get("rows") or []
    by_key = {r.get("security_key"): r for r in crows}
    ticker_rows = [(r.get("security_key"), r.get("display_name")) for r in crows if r.get("name_source") == "ticker"]
    bubbles = {k: ((by_key.get(k) or {}).get("display_name"), (by_key.get(k) or {}).get("name_source")) for k in BUBBLES}
    clause("C3 the chatter set names every row", st == 200 and crows and not ticker_rows
           and all(v[0] and v[1] != "ticker" for v in bubbles.values()),
           f"status {st} rows {len(crows)} ticker-named {len(ticker_rows)} {ticker_rows[:6]}; bubbles {bubbles}")
    st, ov = call(PREFIX + "/security/RMS_FP_Equity/overlay")
    clause("C4 the overlay serves the row's display_name", st == 200 and (ov or {}).get("display_name") == rms.get("display_name") and rms.get("display_name"),
           f"overlay {((ov or {}).get('display_name'))!r} row {rms.get('display_name')!r}")
    verdict = all(ok)
    print(f"EVERY PRICE BAR AND BUBBLE CARRIES A COMPANY NAME: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
