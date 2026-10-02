"""AMGT_RESAPP round 63 -- the served reads of cells 1-5 (CTO round-62 analysis final addendum @0ce76710dc).

  --cell c1|c2|c3|c4|c5 --where local|deployed [--pool <dir>]

c1 (track C step 2): BA_US_Equity /timeline/day/2026-09-08 serves 5 of 5 headlines with NO headline_reason. Under --where local the
   silver reader is planted to RAISE, so a YES proves the route reads no silver at request time (headlines come from gold).
c2 (FWD-7): ASML_NA_Equity's management is SERVED with roster_source BLOOMBERG_FALLBACK and officer_count > 0 (as 6861_JP is today);
   6501_JP_Equity and 2317_TT_Equity each have a management object: SERVED with officers, or ABSENT with a reason that is not the
   "no M-1 management object has landed" fallback. --pool <dir> (local only) points the pool reader at a directory holding the
   PLANNED objects (management/v1/<key>/<as_of>.json), so the produced objects are graded through read_management itself.
c3 (FWD-2): every collected-chatter row carries `ticker`, `classification` and `places_moved` keys beside `display_name`; `ticker`
   is non-empty on every row.
c4: every peers absent-column entry for BA_US_Equity and VLO_US_Equity carries a non-empty `reason_class`.
c5 (Z-S332): a fabricated key's overlay answers 404 (base 200), and BA_US_Equity's overlay still answers 200.
Verdict: R63 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
NO_OBJECT = "no M-1 management object has landed"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c1", "c2", "c3", "c4", "c5"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    ap.add_argument("--pool")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path):
            body, meta = cl._invoke(lam, path)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        if a.pool:
            os.environ["AMGT_POOL_ROOT"] = os.path.abspath(a.pool)
        from lib.research.api import scoped_amgt

        if a.cell == "c1":
            def _no_silver(keys):
                raise AssertionError("silver read at request time")

            scoped_amgt._timeline_silver_articles = _no_silver

        def call(path):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": None})
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

    if a.cell == "c1" and a.where == "deployed":
        import base64
        import re
        from concurrent.futures import ThreadPoolExecutor

        def one(_):
            ev = {"rawPath": PREFIX + "/security/BA_US_Equity/timeline/day/2026-09-08", "headers": {"x-firm-id": "opal"},
                  "requestContext": {"http": {"method": "GET"}}, "queryStringParameters": None}
            r = lam.invoke(FunctionName=cl.FUNCTION, Payload=json.dumps(ev).encode("utf-8"), LogType="Tail")
            raw = json.loads(r["Payload"].read())
            rep = next((ln for ln in base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace").splitlines()
                        if ln.startswith("REPORT")), "")
            dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
            init = re.search(r"Init Duration: ([\d.]+) ms", rep)
            body = json.loads(raw.get("body") or "{}") if isinstance(raw, dict) else {}
            arts = body.get("articles") or []
            return {"status": raw.get("statusCode"), "duration_ms": float(dur.group(1)) if dur else None,
                    "cold": init is not None, "headlines": sum(1 for x in arts if x.get("headline")), "articles": len(arts),
                    "reason": bool(body.get("headline_reason"))}

        with ThreadPoolExecutor(max_workers=3) as pool:
            runs = list(pool.map(one, range(3)))
        for i, r in enumerate(runs):
            print(f"   run {i + 1}: {r}")
        good = [r for r in runs if r["status"] == 200 and r["cold"] and r["duration_ms"] is not None and r["duration_ms"] < 5000
                and r["articles"] and r["headlines"] == r["articles"] and not r["reason"]]
        clause("C1 3 of 3 COLD BA Sept 8 invokes under 5 s with every headline and no reason", len(good) == 3, f"{len(good)} of 3")
    elif a.cell == "c1":
        st, b = call(PREFIX + "/security/BA_US_Equity/timeline/day/2026-09-08")
        arts = (b or {}).get("articles") or []
        clause("C1 BA Sept 8 serves every headline from gold, no reason", st == 200 and arts and all(x.get("headline") for x in arts)
               and not (b or {}).get("headline_reason"), f"status {st} articles {len(arts)} with headline {sum(1 for x in arts if x.get('headline'))} reason {bool((b or {}).get('headline_reason'))}")
    elif a.cell == "c2":
        if a.where == "local" and a.pool:
            from lib.research.api import scoped_amgt

            def mg_of(key):
                return scoped_amgt.read_management(key, scoped_amgt.resolve_identity(key))
        else:
            def mg_of(key):
                st, b = call(f"{PREFIX}/security/{key}/thesis")
                return (b or {}).get("management") or {}
        asml = mg_of("ASML_NA_Equity")
        clause("C1 ASML_NA falls back to the Bloomberg officer list", asml.get("management_status") == "SERVED"
               and asml.get("roster_source") == "BLOOMBERG_FALLBACK" and (asml.get("officer_count") or 0) > 0,
               f"status {asml.get('management_status')} source {asml.get('roster_source')} officers {asml.get('officer_count')}")
        for key in ("6501_JP_Equity", "2317_TT_Equity"):
            mg = mg_of(key)
            served = mg.get("management_status") == "SERVED" and (mg.get("officer_count") or 0) > 0
            reasoned = mg.get("management_status") != "SERVED" and mg.get("reason") and NO_OBJECT not in str(mg.get("reason"))
            clause(f"C2 {key} has a management object (officers, or a stated reason)", served or reasoned,
                   f"status {mg.get('management_status')} officers {mg.get('officer_count')} reason {str(mg.get('reason'))[:80]!r}")
    elif a.cell == "c3":
        st, b = call(PREFIX + "/lead-panel/timeseries/collected/chatter")
        rows = (b or {}).get("rows") or []
        keyed = [r for r in rows if all(k in r for k in ("ticker", "classification", "places_moved"))]
        ticked = [r for r in rows if r.get("ticker")]
        clause("C1 every chatter row carries ticker, classification and places_moved", rows and len(keyed) == len(rows), f"{len(keyed)} of {len(rows)}")
        clause("C2 every chatter row's ticker is non-empty", rows and len(ticked) == len(rows), f"{len(ticked)} of {len(rows)}")
    elif a.cell == "c4":
        for key in ("BA_US_Equity", "VLO_US_Equity"):
            st, b = call(f"{PREFIX}/security/{key}/peers")
            absent = ((b or {}).get("csc_columns") or {}).get("absent") or []
            classed = [e for e in absent if e.get("reason_class")]
            clause(f"C1 {key} every absent column carries a reason_class", absent and len(classed) == len(absent),
                   f"{len(classed)} of {len(absent)}; classes {sorted({e.get('reason_class') for e in classed})}")
    else:
        st, _b = call(PREFIX + "/security/ZZZZ_XX_Equity/overlay")
        clause("C1 a fabricated key's overlay answers 404", st == 404, f"status {st}")
        st2, _b2 = call(PREFIX + "/security/BA_US_Equity/overlay")
        clause("C2 a covered key's overlay still answers 200", st2 == 200, f"status {st2}")
    print(f"R63 {a.cell.upper()} SERVED: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
