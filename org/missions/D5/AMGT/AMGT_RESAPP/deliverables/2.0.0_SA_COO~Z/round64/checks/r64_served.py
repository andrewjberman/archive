"""AMGT_RESAPP round 64 -- the served reads of FWD-36/37/38, the cold read and the repairs (PRD v0.34/v0.35).

  --cell c9|c10|c11|c12|c13|c14|c15 --where local|deployed

c9  (FWD-36 chatter): collected/chatter takes ?days=30|90|365 (default 30); the response serves window_days, window_start,
    window_start_requested and window_end (a trading day, not stale); window_note when the store is shorter than asked; every row
    serves articles_total (int) plus tone and voters, each null only beside tone_reason; by_month stays on every row.
c10 (FWD-36 price, QUALIFIED WAIT v0.35): the price ranking takes ?days; 30 (and the default) serves rows at window_days 30; 90 and 365
    serve no rows and a reason containing "not produced yet". That answer is never read as the 90/365 path.
c11 (FWD-37): on BA, AMD, VLO the timeline route serves markers [{date, kind, label}]; every event has a coverage_event marker on its
    first_day labelled with its lead_headline; earnings_release is served as markers or, while no date is pulled, in
    marker_kinds_absent with the reason "no earnings dates are pulled yet".
c12 (FWD-38 a, b): on BA, AMD, VLO every article the day view shows inside the overlay feed's window is in the feed (by article_key);
    and every route that serves a display name serves the SAME one, not all-caps, with no share-class code.
c13 (FWD-38 c, d): every served places_moved names its axis and window (places_moved_axis, places_moved_window_days) on chatter rows;
    the overlay serves provenance.inputs naming filings, harvested_news and bloomberg, each with last_run or null beside a reason.
c14 (repairs): BP/_LN and NG/_LN classification resolves through the slash ticker or serves a TRUE reason (never "holds no
    classification"); ASML_NA's management reader text (source_item, pool_read.reason, fallback.label) carries no raw code
    (COMPANY_EXEC_OFFICERS, ABSENT, RESOLVED); 6501_JP / 2317_TT / ASML_NA management serves a source stamp
    (source_stamp from the body, or object_as_of from the key) distinct from the date-only as_of; the encoded key BP-SLASH-_LN_Equity
    reaches overlay, thesis, peers and coverage.
c16 (500 attribution, local): a planted fault on the overlay answers 500 and writes ONE structured AMGT_500 line
    {request_id, route, security_key, exception_class}; no alarm, no notification, no monitor.
c15 (cold read, deployed only): 3 COLD BA 2026-09-08 invokes, each under 5,000 ms with every headline (Init Duration proves cold),
    and the log tail carries AMGT_SEGMENT timing lines.
Verdict: R64 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import re
import sys

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
NAMES = ("BA_US_Equity", "AMD_US_Equity", "VLO_US_Equity")
RAW = re.compile(r"COMPANY_EXEC_OFFICERS|\bABSENT\b|\bRESOLVED\b")
SHARE_CLASS = re.compile(r"(\bClass [A-Z]\b|\bCl [A-Z]\b|[- ][A-Z]$|\b(ADR|GDR)\b)")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c9", "c10", "c11", "c12", "c13", "c14", "c15", "c16"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    from lib import trading_calendar as tc

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path, query=None):
            body, meta = cl._invoke(lam, path, query)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        from lib.research.api import scoped_amgt

        def call(path, query=None):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": query})
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

    today = datetime.datetime.now(datetime.timezone.utc).date()
    floor_end = tc.prev_trading_day(tc.prev_trading_day(tc.prev_trading_day(today)))

    if a.cell == "c9":
        for d in (None, 30, 90, 365):
            st, b = call(PREFIX + "/lead-panel/timeseries/collected/chatter", {"days": str(d)} if d else None)
            b = b or {}
            want = d or 30
            end = b.get("window_end")
            shape = (st == 200 and b.get("window_days") == want and b.get("window_start") and b.get("window_start_requested")
                     and end and tc.is_trading_day(end) and datetime.date.fromisoformat(end) >= floor_end)
            shorter = b.get("window_start") and b.get("window_start_requested") and b["window_start"] > b["window_start_requested"]
            note_ok = (not shorter) or bool(b.get("window_note"))
            rows = b.get("rows") or []
            bad = [r.get("security_key") for r in rows if not (isinstance(r.get("articles_total"), int) and "tone" in r and "voters" in r
                                                             and (r.get("tone") is not None or r.get("tone_reason"))
                                                             and "by_month" in r)]
            clause(f"C1 days={d or 'default'} serves its window and every row its counts, tone or reason, and by_month",
                   shape and note_ok and rows and not bad,
                   f"status {st} window_days {b.get('window_days')} start {b.get('window_start')} requested {b.get('window_start_requested')}"
                   f" end {end} note {bool(b.get('window_note'))} rows {len(rows)} bad {len(bad)}")
    elif a.cell == "c10":
        for d in (None, 30):
            st, b = call(PREFIX + "/lead-panel/rankings/breakout/price", {"days": str(d)} if d else None)
            rows = (b or {}).get("rows") or []
            clause(f"C1 price days={d or 'default'} serves rows at window_days 30", st == 200 and rows
                   and all(r.get("window_days") == 30 for r in rows), f"status {st} rows {len(rows)}")
        for d in (90, 365):
            st, b = call(PREFIX + "/lead-panel/rankings/breakout/price", {"days": str(d)})
            b = b or {}
            text = " ".join(str(b.get(k) or "") for k in ("window_reason", "ranking_reason", "reason"))
            clause(f"C2 price days={d} serves no rows and 'not produced yet'", st == 200 and not (b.get("rows") or [])
                   and "not produced yet" in text, f"status {st} rows {len(b.get('rows') or [])} reason {text[:90]!r}")
    elif a.cell == "c11":
        for key in NAMES:
            st, tl = call(f"{PREFIX}/security/{key}/timeline", {"from": "2026-09-01", "to": today.isoformat()})
            tl = tl or {}
            markers = tl.get("markers")
            events = tl.get("events") or []
            mk = markers if isinstance(markers, list) else []
            shape_bad = [m for m in mk if not (m.get("date") and m.get("kind") in ("coverage_event", "earnings_release") and "label" in m)]
            cov = {(m.get("date"), m.get("label")) for m in mk if m.get("kind") == "coverage_event"}
            missing = [e.get("first_day") for e in events if (e.get("first_day"), e.get("lead_headline")) not in cov]
            earn = [m for m in mk if m.get("kind") == "earnings_release"]
            absent = [x for x in (tl.get("marker_kinds_absent") or []) if x.get("kind") == "earnings_release"
                      and "no earnings dates are pulled yet" in str(x.get("reason"))]
            clause(f"C1 {key} serves markers for every event plus the earnings kind",
                   st == 200 and isinstance(markers, list) and not shape_bad and not missing and (earn or absent),
                   f"status {st} markers {len(mk) if isinstance(markers, list) else None} events {len(events)} missing {missing[:3]}"
                   f" earnings {len(earn)} absent-with-reason {bool(absent)}")
    elif a.cell == "c12":
        st_r, rk = call(PREFIX + "/lead-panel/rankings/breakout/price")
        st_c, ch = call(PREFIX + "/lead-panel/timeseries/collected/chatter")
        rk_rows = {r.get("security_key"): r for r in ((rk or {}).get("rows") or [])}
        ch_rows = {r.get("security_key"): r for r in ((ch or {}).get("rows") or [])}
        for key in NAMES:
            st, ov = call(f"{PREFIX}/security/{key}/overlay")
            ov = ov or {}
            feed = ov.get("feed") or {}
            win = feed.get("window") or {}
            fkeys = {i.get("article_key") for i in (feed.get("items") or []) if i.get("article_key")}
            st2, tl = call(f"{PREFIX}/security/{key}/timeline", {"from": win.get("start_date"), "to": win.get("end_date")})
            days = sorted({s.get("day") or s.get("date") for s in ((tl or {}).get("series") or [])
                           if (s.get("articles_total") or 0) > 0 and (s.get("day") or s.get("date"))})
            shown = set()
            for d in days:
                st3, dv = call(f"{PREFIX}/security/{key}/timeline/day/{d}")
                shown |= {x.get("article_key") for x in ((dv or {}).get("articles") or []) if x.get("article_key")}
            missing = sorted(shown - fkeys)
            clause(f"C1 {key} feed holds every day-view article in its window", win and shown and not missing,
                   f"window {win.get('start_date')}..{win.get('end_date')} days {len(days)} day-view {len(shown)} feed {len(fkeys)}"
                   f" missing {len(missing)}")
            st4, pe = call(f"{PREFIX}/security/{key}/peers")
            subj = (pe or {}).get("subject") or {}
            names = {"overlay": ov.get("display_name"), "ranking": (rk_rows.get(key) or {}).get("display_name"),
                     "chatter": (ch_rows.get(key) or {}).get("display_name"),
                     "peers": subj.get("display_name") or subj.get("name")}
            present = {k: v for k, v in names.items() if v}
            vals = set(present.values())
            one = vals and len(vals) == 1 and len(present) >= 3
            v = next(iter(vals)) if len(vals) == 1 else ""
            clean = bool(v) and v != v.upper() and not SHARE_CLASS.search(v)
            clause(f"C2 {key} serves one display name, cased, no share-class code", one and clean, f"names {present}")
    elif a.cell == "c13":
        st, ch = call(PREFIX + "/lead-panel/timeseries/collected/chatter")
        rows = (ch or {}).get("rows") or []
        moved = [r for r in rows if r.get("places_moved") is not None]
        unlabeled = [r.get("security_key") for r in moved if not (r.get("places_moved_axis") and r.get("places_moved_window_days"))]
        clause("C1 every chatter places_moved names its axis and window", moved and not unlabeled,
               f"{len(moved) - len(unlabeled)} of {len(moved)} labeled; e.g. {unlabeled[:3]}")
        for key in NAMES:
            st, ov = call(f"{PREFIX}/security/{key}/overlay")
            inputs = {i.get("input"): i for i in (((ov or {}).get("provenance") or {}).get("inputs") or [])}
            need = ("filings", "harvested_news", "bloomberg")
            bad = [n for n in need if n not in inputs or not (inputs[n].get("last_run") or inputs[n].get("reason"))]
            clause(f"C2 {key} overlay provenance names filings, harvested news and Bloomberg with a last run or reason",
                   not bad, f"inputs {sorted(inputs)} missing-or-bare {bad}")
    elif a.cell == "c14":
        st, rk = call(PREFIX + "/lead-panel/rankings/breakout/price")
        rows = {r.get("security_key"): r for r in ((rk or {}).get("rows") or [])}
        for key, sector in (("BP/_LN_Equity", "Energy"), ("NG/_LN_Equity", "Utilities")):
            r = rows.get(key) or {}
            c = r.get("classification") or {}
            reason = str(c.get("sector_reason") or r.get("sector_reason") or "")
            good = (c.get("sector") == sector and c.get("sector_source")) or (c.get("sector") is None and reason
                                                                            and "holds no classification" not in reason)
            clause(f"C1 {key} resolves its sector or serves a true reason", r and good,
                   f"sector {c.get('sector')!r} source {c.get('sector_source')!r} reason {reason[:80]!r}")
        st, th = call(PREFIX + "/security/ASML_NA_Equity/thesis")
        m = (th or {}).get("management") or {}
        texts = {"source_item": m.get("source_item"), "pool_read.reason": (m.get("pool_read") or {}).get("reason"),
                 "fallback.label": (m.get("fallback") or {}).get("label")}
        raw = {k: v for k, v in texts.items() if v and RAW.search(str(v))}
        clause("C2 ASML_NA management reader text carries no raw code", m and not raw, f"raw {raw}")
        for key in ("ASML_NA_Equity", "6501_JP_Equity", "2317_TT_Equity"):
            st, th = call(f"{PREFIX}/security/{key}/thesis")
            m = (th or {}).get("management") or {}
            stamp = m.get("source_stamp") or m.get("object_as_of")
            clause(f"C3 {key} management serves its source stamp", bool(stamp) and stamp != m.get("as_of"),
                   f"source_stamp {m.get('source_stamp')!r} object_as_of {m.get('object_as_of')!r} as_of {m.get('as_of')!r}")
        # analysis ruling 1: the route template accepts the encoded slash key
        for leaf in ("overlay", "thesis", "peers", "coverage"):
            st, b = call(f"{PREFIX}/security/BP-SLASH-_LN_Equity/{leaf}")
            clause(f"C4 the encoded key BP-SLASH-_LN_Equity reaches /{leaf}", st == 200 and (b or {}).get("security_key") == "BP/_LN_Equity",
                   f"status {st} security_key {(b or {}).get('security_key')!r}")
    elif a.cell == "c16":
        # analysis ruling 3: a planted fault answers 500 and writes ONE structured AMGT_500 line (no alarm, no notification)
        if a.where != "local":
            print("c16 plants a fault, so it is graded locally; the deployed census is the an-8 script")
            return 2
        import contextlib
        import io
        import logging

        from lib.research.api import scoped_amgt as sa

        def _boom(*_a, **_k):
            raise RuntimeError("planted fault r64")

        sa.read_security_overlay = _boom
        buf = io.StringIO()
        h = logging.StreamHandler(buf)
        logging.getLogger().addHandler(h)
        logging.getLogger().setLevel(logging.INFO)
        out = io.StringIO()
        status, escaped = None, None
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                r = sa.handler({"rawPath": PREFIX + "/security/BA_US_Equity/overlay",
                                "requestContext": {"http": {"method": "GET"}, "requestId": "r64-plant-1"},
                                "headers": {"x-firm-id": "opal"}, "queryStringParameters": None})
                status = r.get("statusCode")
            except Exception as err:  # noqa: BLE001 -- the base lets the fault escape; that is what this clause reads
                escaped = type(err).__name__
        lines = [ln for ln in (buf.getvalue() + out.getvalue()).splitlines() if "AMGT_500" in ln]
        rec = {}
        if len(lines) == 1:
            try:
                rec = json.loads(lines[0].split("AMGT_500", 1)[1].strip())
            except ValueError:
                rec = {}
        clause("C1 the planted fault answers 500 instead of escaping", status == 500 and escaped is None,
               f"status {status} escaped {escaped}")
        clause("C2 exactly one AMGT_500 line carries request id, route, key and exception class",
               len(lines) == 1 and rec.get("request_id") == "r64-plant-1" and "overlay" in str(rec.get("route"))
               and rec.get("security_key") == "BA_US_Equity" and rec.get("exception_class") == "RuntimeError",
               f"lines {len(lines)} record {json.dumps(rec)[:160]}")
    else:
        if a.where != "deployed":
            print("c15 is graded on the deployed function only")
            return 2
        import base64
        from concurrent.futures import ThreadPoolExecutor

        def one(_):
            ev = {"rawPath": PREFIX + "/security/BA_US_Equity/timeline/day/2026-09-08", "headers": {"x-firm-id": "opal"},
                  "requestContext": {"http": {"method": "GET"}}, "queryStringParameters": None}
            r = lam.invoke(FunctionName=cl.FUNCTION, Payload=json.dumps(ev).encode("utf-8"), LogType="Tail")
            raw = json.loads(r["Payload"].read())
            log = base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace")
            rep = next((ln for ln in log.splitlines() if ln.startswith("REPORT")), "")
            dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
            init = re.search(r"Init Duration: ([\d.]+) ms", rep)
            body = json.loads(raw.get("body") or "{}") if isinstance(raw, dict) else {}
            arts = body.get("articles") or []
            return {"status": raw.get("statusCode"), "duration_ms": float(dur.group(1)) if dur else None, "cold": init is not None,
                    "init_ms": float(init.group(1)) if init else None, "headlines": sum(1 for x in arts if x.get("headline")),
                    "articles": len(arts), "segments": [ln.strip() for ln in log.splitlines() if "AMGT_SEGMENT" in ln][:6]}

        with ThreadPoolExecutor(max_workers=3) as pool:
            runs = list(pool.map(one, range(3)))
        for i, r in enumerate(runs):
            print(f"   run {i + 1}: {r}")
        good = [r for r in runs if r["status"] == 200 and r["cold"] and r["duration_ms"] is not None and r["duration_ms"] < 5000
                and r["articles"] and r["headlines"] == r["articles"]]
        clause("C1 3 of 3 COLD BA Sept 8 invokes under 5 s with every headline", len(good) == 3, f"{len(good)} of 3")
        clause("C2 every run's log carries AMGT_SEGMENT timings", all(r["segments"] for r in runs),
               f"{sum(1 for r in runs if r['segments'])} of 3")
    print(f"R64 {a.cell.upper()} SERVED: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
