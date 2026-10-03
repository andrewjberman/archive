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
c7 (R1, DSGN Z-C-S36): no ranked-in-both price bar serves the false "not ranked" reason; places_moved = prior rank - rank.
c8 (R2, DSGN Z-C-S37): an equity's classification.sector = sub_asset_class when GICS-11 (sector_source named), else null + reason.
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
    ap.add_argument("--cell", choices=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), required=True)
    ap.add_argument("--plan", help="c6: the frozen peers_slash_plan.json (am-8 AMENDMENT 1)")
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

        def call(path, query=None):
            body, meta = cl._invoke(lam, path, query)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        if a.pool:
            os.environ["AMGT_POOL_ROOT"] = os.path.abspath(a.pool)
        from lib.research.api import scoped_amgt

        if a.cell == "c1":
            def _no_silver(keys):
                raise AssertionError("silver read at request time")

            scoped_amgt._timeline_silver_articles = _no_silver

        def call(path, query=None):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": query})
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
        # AMENDMENT 1 (CTO msg 28553, DSGN FWD-24): the overlay's breakout_price row serves places_moved from the rankings row
        st, rk = call(PREFIX + "/lead-panel/rankings/breakout/price")
        vrow = next((r for r in ((rk or {}).get("rows") or []) if r.get("security_key") == "VLO_US_Equity"), {})
        st, ov = call(PREFIX + "/security/VLO_US_Equity/overlay")
        bp = (ov or {}).get("breakout_price") or {}
        clause("C3 VLO's overlay breakout_price.places_moved equals its rankings row", "places_moved" in bp
               and bp.get("places_moved") == vrow.get("places_moved") and vrow.get("places_moved") is not None,
               f"overlay {bp.get('places_moved')!r} ranking {vrow.get('places_moved')!r}")
        st, ov2 = call(PREFIX + "/security/ROG_SW_Equity/overlay")
        bp2 = (ov2 or {}).get("breakout_price") or {}
        reason = bp2.get("places_moved_reason") or (ov2 or {}).get("places_moved_reason")
        clause("C4 an unranked name (ROG_SW_Equity) serves the reason instead", bp2.get("places_moved") is None and bool(reason),
               f"places_moved {bp2.get('places_moved')!r} reason {str(reason)[:80]!r}")
    elif a.cell == "c4":
        for key in ("BA_US_Equity", "VLO_US_Equity"):
            st, b = call(f"{PREFIX}/security/{key}/peers")
            absent = ((b or {}).get("csc_columns") or {}).get("absent") or []
            classed = [e for e in absent if e.get("reason_class")]
            clause(f"C1 {key} every absent column carries a reason_class", absent and len(classed) == len(absent),
                   f"{len(classed)} of {len(absent)}; classes {sorted({e.get('reason_class') for e in classed})}")
    elif a.cell == "c6":
        # am-8 AMENDMENT 1 / am-7 AMENDMENT 1: every served_field_changes entry of the frozen plan reads its `after` on /peers
        import re as _re

        plan = json.load(open(a.plan, encoding="utf-8"))
        tok = _re.compile(r"(?:^|\.)([A-Za-z0-9_]+)|\[(\d+)\]")  # a bare first segment, then .key or [i]
        bad, n = [], 0
        for e in plan.get("entries") or []:
            st, body = call(f"{PREFIX}/security/{e['security_key']}/peers")
            for ch in e.get("served_field_changes") or []:
                n += 1
                node = body
                try:
                    for k, i in tok.findall(ch["json_path"]):
                        node = node[k] if k else node[int(i)]
                except (KeyError, IndexError, TypeError):
                    node = "<unlocatable>"
                if node != ch.get("after"):
                    bad.append((e["security_key"], ch["json_path"]))
        clause("C1 every planned peers field serves its after value", n > 0 and not bad, f"{n - len(bad)} of {n}; differing {bad[:4]}")
    elif a.cell == "c7":
        # R1 (DSGN Z-C-S36): no ranked-in-both name serves "not ranked in the previous generation"; moved = prior rank - rank
        import re as _re

        st, cur = call(PREFIX + "/lead-panel/rankings/breakout/price")
        rows = (cur or {}).get("rows") or []
        dates = {m.group(1) for r in rows for m in [_re.search(r"previous generation \((\d{4}-\d{2}-\d{2})\)", str(r.get("places_moved_reason")))] if m}
        prior_date = sorted(dates)[0] if dates else None
        prior_rows = []
        if prior_date is None:
            # no reason names the prior date: read the generation before the served one through the route's own as_of walk
            served = (cur or {}).get("as_of_date")
            import datetime as _dt
            if served:
                prior_date = (_dt.date.fromisoformat(served) - _dt.timedelta(days=1)).isoformat()
        if prior_date:
            st2, pr = call(PREFIX + "/lead-panel/rankings/breakout/price", {"as_of": prior_date})
            prior_rows = (pr or {}).get("rows") or []
            prior_date = (pr or {}).get("as_of_date") or prior_date
        prior_rank = {}
        for r in prior_rows:
            for k in (r.get("security_key"), r.get("ticker")):
                if k and r.get("rank") is not None:
                    prior_rank[k] = r["rank"]
        false_reason, wrong_math, moved_ok, new_ok = [], [], 0, 0
        for r in rows:
            pr_rank = prior_rank.get(r.get("security_key")) or prior_rank.get(r.get("ticker"))
            if r.get("places_moved") is None:
                if pr_rank is not None and "previous generation" in str(r.get("places_moved_reason")):
                    false_reason.append(r.get("ticker"))
                else:
                    new_ok += 1
            elif pr_rank is not None and r.get("rank") is not None:
                if r["places_moved"] == int(pr_rank) - int(r["rank"]):
                    moved_ok += 1
                else:
                    wrong_math.append(r.get("ticker"))
        clause("C1 0 ranked-in-both bars serve the false 'not ranked' reason", rows and prior_rows and not false_reason,
               f"{len(false_reason)} false of {len(rows)} bars (prior {prior_date}, {len(prior_rows)} rows); e.g. {false_reason[:5]}")
        clause("C2 every served places_moved equals prior rank minus rank", rows and not wrong_math,
               f"{moved_ok} correct, {len(wrong_math)} wrong, {new_ok} truly new with a reason")
    elif a.cell == "c8":
        # R2 (DSGN Z-C-S37): an equity's sector = sub_asset_class when GICS-11, source named; else null with a reason
        gics = {"Communication Services", "Consumer Discretionary", "Consumer Staples", "Energy", "Financials", "Health Care",
                "Industrials", "Information Technology", "Materials", "Real Estate", "Utilities"}
        st, cur = call(PREFIX + "/lead-panel/rankings/breakout/price")
        rows = (cur or {}).get("rows") or []
        bad, served, reasoned = [], 0, 0
        for r in rows:
            c = r.get("classification") or {}
            want = c.get("sub_asset_class") if c.get("asset_class") == "equity" and c.get("sub_asset_class") in gics else None
            if want is not None:
                if c.get("sector") == want and c.get("sector_source") == "opal_classification.sub_asset_class":
                    served += 1
                else:
                    bad.append(r.get("ticker"))
            elif c.get("sector") is None and (c.get("sector_reason") or r.get("sector_reason")):
                reasoned += 1
            else:
                bad.append(r.get("ticker"))
        amd = next((r for r in rows if r.get("security_key") == "AMD_US_Equity"), {})
        ac = amd.get("classification") or {}
        clause("C1 AMD serves Information Technology from sub_asset_class", ac.get("sector") == "Information Technology"
               and ac.get("sector_source") == "opal_classification.sub_asset_class", f"sector {ac.get('sector')!r} source {ac.get('sector_source')!r}")
        clause("C2 every bar serves a GICS sector with its source, or null with a reason", rows and not bad,
               f"{served} served, {reasoned} null with a reason, {len(bad)} wrong of {len(rows)}; e.g. {bad[:5]}")
    else:
        st, _b = call(PREFIX + "/security/ZZZZ_XX_Equity/overlay")
        clause("C1 a fabricated key's overlay answers 404", st == 404, f"status {st}")
        st2, _b2 = call(PREFIX + "/security/BA_US_Equity/overlay")
        clause("C2 a covered key's overlay still answers 200", st2 == 200, f"status {st2}")
    print(f"R63 {a.cell.upper()} SERVED: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
