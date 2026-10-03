"""AMGT_RESAPP round 66 -- the CTO's round-65 analysis @2de1ef2251, rulings 2 and 3.

  --cell c18|c19|c22 --where local|deployed

c18 (FWD-39, PRD v0.37): on BA, AMD, VLO the timeline route (2026-09-01..today) serves `word_cloud` = {terms: [{term, count}],
    reason}. C1 per name: 1 to WORD_CLOUD_MAX_TERMS (40) terms, each a str with an int count > 0, ordered by count descending, none in
    the DECLARED stop list (scoped_amgt.WORD_CLOUD_STOP_WORDS, source printed from WORD_CLOUD_STOP_WORDS_SOURCE) and none a word of
    the company's served display_name. C2: BA over a window with no headlines (2025-06-01..2025-06-30, before the store floor)
    serves terms [] with a non-empty reason. The stop list and the name words are read from the LOCAL tree (row Z-S342), so a
    deployed run is graded from a checkout at the build commit.
c19 (ruling 2): every tone_reason the collected/chatter route serves (default, 30, 90, 365 days) cites no terms card: it contains
    none of 'terms', 'HARVST', 'held'.
c22 (FWD-36 price 90/365, ADDENDUM 1 @1162e9be0e): on trending/price and breakout/price, ?days=90 and ?days=365 each serve rows
    from a real 90/365 generation: status 200, at least one row, ranks 1..n in order, a numeric score on every row, window_days equal
    to the request, a window_end date; where window_end is earlier than the last trading day a window_note names that end date
    (the interim branch: never graded as the T-1 path); and no "not produced yet" reason.
Verdict: R66 <CELL> SERVED: YES|NO.
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
BANNED = ("terms", "harvst", "held")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c18", "c19", "c22"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    from lib.research.api import scoped_amgt

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path, query=None):
            body, meta = cl._invoke(lam, path, query)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        def call(path, query=None):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": query})
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

    today = datetime.datetime.now(datetime.timezone.utc).date()
    if a.cell == "c18":
        stop = {str(w).lower() for w in (getattr(scoped_amgt, "WORD_CLOUD_STOP_WORDS", ()) or ())}
        cap = getattr(scoped_amgt, "WORD_CLOUD_MAX_TERMS", 40)
        print(f"   declared stop words: {len(stop)}; source: {getattr(scoped_amgt, 'WORD_CLOUD_STOP_WORDS_SOURCE', 'NOT DECLARED')}; cap {cap}")
        for key in NAMES:
            st_o, ov = call(f"{PREFIX}/security/{key}/overlay")
            name_words = {w for w in re.findall(r"[a-z0-9']+", str((ov or {}).get("display_name") or "").lower())}
            st, tl = call(f"{PREFIX}/security/{key}/timeline", {"from": "2026-09-01", "to": today.isoformat()})
            wc = (tl or {}).get("word_cloud")
            terms = (wc or {}).get("terms") if isinstance(wc, dict) else None
            terms = terms if isinstance(terms, list) else []
            bad_shape = [t for t in terms if not (isinstance(t, dict) and isinstance(t.get("term"), str)
                                                  and isinstance(t.get("count"), int) and t["count"] > 0)]
            counts = [t.get("count") for t in terms if isinstance(t, dict)]
            ordered = counts == sorted(counts, reverse=True)
            in_stop = [t["term"] for t in terms if isinstance(t, dict) and str(t.get("term")).lower() in stop]
            in_name = [t["term"] for t in terms if isinstance(t, dict) and str(t.get("term")).lower() in name_words]
            clause(f"C1 {key} serves 1..{cap} terms, counted, ordered, no stop word, no name word",
                   st == 200 and isinstance(wc, dict) and 0 < len(terms) <= cap and not bad_shape and ordered
                   and not in_stop and not in_name and bool(stop),
                   f"status {st} terms {len(terms)} top {[(t.get('term'), t.get('count')) for t in terms[:5]]} "
                   f"bad {len(bad_shape)} ordered {ordered} stop-hits {in_stop[:3]} name-hits {in_name[:3]}")
        st, tl = call(f"{PREFIX}/security/BA_US_Equity/timeline", {"from": "2025-06-01", "to": "2025-06-30"})
        wc = (tl or {}).get("word_cloud")
        clause("C2 BA with no headlines in the window serves an empty list with a reason",
               st == 200 and isinstance(wc, dict) and wc.get("terms") == [] and bool(str(wc.get("reason") or "").strip()),
               f"status {st} word_cloud {json.dumps(wc)[:160] if wc is not None else None}")
    elif a.cell == "c22":
        from lib import trading_calendar as tc

        last = tc.prev_trading_day(today).isoformat()
        for mv in ("trending", "breakout"):
            for d in (90, 365):
                st, b = call(f"{PREFIX}/lead-panel/rankings/{mv}/price", {"days": str(d)})
                b = b or {}
                rows = b.get("rows") or []
                ranks = [r.get("rank") for r in rows]
                scores_ok = all(isinstance(r.get("score"), (int, float)) for r in rows)
                end = str(b.get("window_end") or "")
                note = str(b.get("window_note") or "")
                text = " ".join(str(b.get(k) or "") for k in ("ranking_reason", "window_reason"))
                note_ok = (end == last) or (bool(end) and end in note)
                clause(f"C1 {mv} price days={d} serves a real {d}-day ranking with its end date",
                       st == 200 and rows and ranks == list(range(1, len(rows) + 1)) and scores_ok
                       and b.get("window_days") == d and bool(end) and note_ok and "not produced yet" not in text,
                       f"status {st} rows {len(rows)} window_days {b.get('window_days')} window_end {end or None} last {last} "
                       f"note {note[:80]!r} reason {text.strip()[:60]!r}")
    else:
        for d in (None, 30, 90, 365):
            st, b = call(PREFIX + "/lead-panel/timeseries/collected/chatter", {"days": str(d)} if d else None)
            reasons = sorted({str(r.get("tone_reason")) for r in ((b or {}).get("rows") or []) if r.get("tone_reason")})
            hits = [x for x in reasons if any(w in x.lower() for w in BANNED)]
            clause(f"C1 chatter days={d} serves tone_reason with no terms-card wording",
                   st == 200 and reasons and not hits, f"status {st} reasons {reasons[:2]}")
    print(f"R66 {a.cell.upper()} SERVED: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
