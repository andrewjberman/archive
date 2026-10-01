"""AMGT_RESAPP round 56 -- AMGT-af-2: the served T-1 fallback, the breakout field, and percent units.

Live, read-only: calls lib.research.api.scoped_amgt.handler locally (API Gateway v2 events) on the
overlay route and the price rankings, with NO as_of (the portal sends none), and grades against an
oracle read HERE from the generation pointers and the raw DynamoDB items the producer wrote.

  --what fwd33   per-name overlay reads (price axes) serve the latest COMPLETE generation on or before
                 today, name the trading day served and the trading-day staleness; the rankings state
                 the same; the overlay's `breakout_price` is the BREAKOUT/PRICE row, never the trending row.
                 Verdict: THE PER-NAME READ SERVES THE LATEST TRADING DAY AND BREAKOUT READS BREAKOUT: YES|NO
  --what fwd34   every served price-movement figure is percent and says so in a `_pct` field: BREAKOUT/PRICE
                 `score` and `score_pct` = stored fraction x 100, `pct_jump_pct` = stored pct_jump x 100, no
                 unsuffixed `pct_jump`; TRENDING/PRICE `score` = `score_pct` = stored percent, `return_30d_pct`
                 on 30-day rows; the overlay's breakout row and the rank series agree.
                 Verdict: EVERY SERVED PRICE MOVEMENT IS PERCENT BY NAME: YES|NO
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys

TOL = 1e-6


def _call(path, query=None):
    from lib.research.api import scoped_amgt

    ev = {"rawPath": path, "requestContext": {"http": {"method": "GET"}},
          "headers": {"x-firm-id": "bd"}, "queryStringParameters": query}
    r = scoped_amgt.handler(ev)
    return r.get("statusCode"), json.loads(r.get("body") or "null")


def _latest(axis, today):
    from lib.research.api import scoped_amgt as s

    p = s.read_generation_pointer(axis, today)
    if p is not None and s._pointer_status(p) == s.RANKING_SERVED:
        return today, p
    return s._find_latest_served_pointer(axis, today)


def _raw(axis, date, pointer, ticker):
    from lib.research.api import scoped_amgt as s

    it = s._dynamodb().Table(s.METRICS_TABLE).get_item(
        Key={"axis_date": s.generation_key(axis, date, pointer["generation_id"]), "ticker": ticker}).get("Item")
    return s._plain(it) if it else None


def _close(a, b):
    try:
        return abs(float(a) - float(b)) <= TOL * max(1.0, abs(float(b)))
    except (TypeError, ValueError):
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("fwd33", "fwd34"), required=True)
    a = ap.parse_args()
    from lib import trading_calendar as tc
    from lib.research.api import scoped_amgt as s
    from lib.research.metrics import movement_gate as mg

    today = s._today()
    t1 = str(tc.prev_trading_day(datetime.datetime.now(datetime.timezone.utc)))[:10]
    bp_axis = mg.crossed_axis("BREAKOUT", "PRICE")
    tp_axis = mg.crossed_axis("TRENDING", "PRICE")
    bp_date, bp_ptr = _latest(bp_axis, today)
    tp_date, tp_ptr = _latest(tp_axis, today)
    print(f"oracle: today {today}; prev trading day {t1}; latest served {bp_axis} {bp_date}, {tp_axis} {tp_date}; "
          f"today has its own pointer: {s.read_generation_pointer(bp_axis, today) is not None}")
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    st_b, rk_b = _call(s.ROUTE_PREFIX + "/lead-panel/rankings/breakout/price")
    st_t, rk_t = _call(s.ROUTE_PREFIX + "/lead-panel/rankings/trending/price")
    rows_b = (rk_b or {}).get("rows") or []
    rows_t = (rk_t or {}).get("rows") or []
    if not rows_b:
        clause("C0 breakout price ranking has rows", False, f"status {st_b}")
        print("VERDICT UNREADABLE: NO")
        return 1
    ticker = rows_b[0]["ticker"]
    key = ticker.replace(" ", "_") + "_Equity"
    st_o, ov = _call(s.ROUTE_PREFIX + "/security/" + key + "/overlay")
    reads = {(e.get("movement"), e.get("subject")): e for e in (ov or {}).get("axis_reads") or []}
    print(f"name under test: {ticker} ({key}); overlay status {st_o}")

    if a.what == "fwd33":
        for (mv, axis, date) in (("BREAKOUT", bp_axis, bp_date), ("TRENDING", tp_axis, tp_date)):
            e = reads.get((mv, "PRICE")) or {}
            served = e.get("as_of_date") or e.get("served_as_of")
            clause(f"C1 overlay {mv}/PRICE served from the latest generation",
                   e.get("point_status") == s.RANKING_SERVED and e.get("row") and served == date,
                   f"point_status={e.get('point_status')} served={served} oracle={date}")
            stale = e.get("stale_trading_days")
            clause(f"C2 overlay {mv}/PRICE states trading-day staleness",
                   isinstance(stale, int) and stale >= 0 and ((stale == 0) == (served == t1)),
                   f"stale_trading_days={stale} served={served} t1={t1}")
        for name, rk, date in (("breakout", rk_b, bp_date), ("trending", rk_t, tp_date)):
            stale = (rk or {}).get("stale_trading_days")
            clause(f"C3 {name} price ranking serves {date} and states staleness",
                   (rk or {}).get("as_of_date") == date and isinstance(stale, int)
                   and ((stale == 0) == ((rk or {}).get("as_of_date") == t1)),
                   f"as_of_date={(rk or {}).get('as_of_date')} stale_trading_days={stale}")
        brk = (ov or {}).get("breakout_price")
        want = (reads.get(("BREAKOUT", "PRICE")) or {}).get("row")
        clause("C4 overlay breakout_price is the BREAKOUT/PRICE row",
               isinstance(brk, dict) and want is not None and brk == want
               and brk.get("movement_measure") == "PCT_JUMP_VS_TRAILING_BASELINE",
               f"breakout_price measure={(brk or {}).get('movement_measure')}")
        clause("C5 overlay price stays the TRENDING/PRICE row",
               (ov or {}).get("price") == (reads.get(("TRENDING", "PRICE")) or {}).get("row"), "")
        verdict = all(ok)
        print(f"THE PER-NAME READ SERVES THE LATEST TRADING DAY AND BREAKOUT READS BREAKOUT: {'YES' if verdict else 'NO'}")
        return 0 if verdict else 1

    raw_b = _raw(bp_axis, bp_date, bp_ptr, ticker)
    srv_b = rows_b[0]
    clause("C1 breakout example: score and score_pct = stored fraction x 100",
           raw_b and _close(srv_b.get("score"), float(raw_b["score"]) * 100) and _close(srv_b.get("score_pct"), float(raw_b["score"]) * 100),
           f"{ticker} stored {raw_b and raw_b.get('score')} served score={srv_b.get('score')} score_pct={srv_b.get('score_pct')}")
    clause("C2 breakout example: pct_jump_pct = stored pct_jump x 100, no unsuffixed pct_jump",
           raw_b and _close(srv_b.get("pct_jump_pct"), float(raw_b["pct_jump"]) * 100) and "pct_jump" not in srv_b,
           f"stored {raw_b and raw_b.get('pct_jump')} served pct_jump_pct={srv_b.get('pct_jump_pct')} has pct_jump={'pct_jump' in srv_b}")
    bad_b = [r.get("ticker") for r in rows_b if "pct_jump" in r or not _close(r.get("score_pct"), r.get("score"))
             or abs(float(r.get("score") or 0)) < 1e-12 and r.get("pct_jump_pct") not in (0, 0.0, None)]
    clause("C3 every breakout row: score_pct == score, no unsuffixed pct_jump", not bad_b, f"bad {len(bad_b)} of {len(rows_b)}")
    tt = rows_t[0] if rows_t else {}
    raw_t = _raw(tp_axis, tp_date, tp_ptr, tt.get("ticker")) if tt else None
    clause("C4 trending example: score = score_pct = stored percent; return_30d_pct on 30-day rows",
           raw_t and _close(tt.get("score"), raw_t["score"]) and _close(tt.get("score_pct"), raw_t["score"])
           and (int(raw_t.get("window_days") or 0) != 30 or _close(tt.get("return_30d_pct"), raw_t["score"])),
           f"{tt.get('ticker')} stored {raw_t and raw_t.get('score')} served score_pct={tt.get('score_pct')} return_30d_pct={tt.get('return_30d_pct')}")
    bad_t = [r.get("ticker") for r in rows_t if not _close(r.get("score_pct"), r.get("score"))
             or (int(r.get("window_days") or 0) == 30 and not _close(r.get("return_30d_pct"), r.get("score")))]
    clause("C5 every trending row: score_pct == score, return_30d_pct on 30-day rows", not bad_t, f"bad {len(bad_t)} of {len(rows_t)}")
    units = [(k, v) for r in rows_b + rows_t for k, v in r.items() if k.endswith("_unit") and str(v).lower() != "percent"]
    clause("C6 no unit field contradicts percent", not units, f"{units[:3]}")
    brk = (ov or {}).get("breakout_price") or {}
    clause("C7 overlay breakout_price carries the percent fields",
           raw_b is not None and _close(brk.get("score_pct"), float(raw_b["score"]) * 100) and "pct_jump" not in brk,
           f"overlay score_pct={brk.get('score_pct')}")
    st_s, ser = _call(s.ROUTE_PREFIX + "/lead-panel/timeseries/breakout/price", {"tickers": ticker})
    pts = [p for sr in (ser or {}).get("series") or [] if sr.get("ticker") == ticker for p in sr.get("points") or []]
    pt = [p for p in pts if p.get("as_of_date") == bp_date]
    clause("C8 breakout rank series point on the served day is percent (score_pct = score = stored x 100)",
           raw_b is not None and len(pt) == 1 and _close(pt[0].get("score"), float(raw_b["score"]) * 100)
           and _close(pt[0].get("score_pct"), float(raw_b["score"]) * 100),
           f"status {st_s} points {len(pts)} on {bp_date}: {pt[:1]}")
    verdict = all(ok)
    print(f"EVERY SERVED PRICE MOVEMENT IS PERCENT BY NAME: {'YES' if verdict else 'NO'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
