"""RIV-x-1 AC2 (RFW-D10, control): a non-exit row keeps today's implied price; only exits move.

Pure, offline (`gold_trade_schedule.infer_trades`, the x-1 AC1 book; no sink, no S3). One window
2026-09-29 -> 2026-09-30, flow factor 1.0, in the SAME frame as a zero-later exit (so the exit rule runs beside them):
  - a partial TRIM (prior qty 2000, mv 40,000 = 20.00; later qty 1500, mv 33,000 = 22.00) keeps the LATER report's
    implied price: action trim, est_price 22.0, est_notional = est_notional_base = -11,000, est_price_band_reason
    "bloomberg-band-enrichment", confidence CLEAN, shares 2000 -> 1500, discretionary -500;
  - an ADD (prior qty 3000, mv 30,000 = 10.00; later qty 3600, mv 39,600 = 11.00): est_price 11.0,
    est_notional 6,600, the same reason and confidence.
Every value above is the base output for that row (measured at the round-6 base before the cell). The prior price
differs from the later one on both rows, so an implementation that prices every sell (or every row) from the prior
valuation fails here.
Interface: unchanged for non-exit rows; the new `est_price_source` column (x-1 AC1) is not graded on them."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D0, D1 = "2026-09-29", "2026-09-30"
BOOK = {f"S{i} US Equity": (1000.0 + 10 * i, (1000.0 + 10 * i) * (10.0 + i)) for i in range(12)}
REASON = "bloomberg-band-enrichment"
BASE_ROWS = {   # the base output of the two rows (gold_trade_schedule at the round-6 base)
    "TRM US Equity": {"action": "trim", "shares_before": 2000.0, "shares_after": 1500.0,
                      "discretionary_shares": -500.0, "est_price": 22.0, "est_notional": -11000.0,
                      "est_notional_base": -11000.0, "est_price_band_reason": REASON, "confidence": "CLEAN"},
    "ADD US Equity": {"action": "add", "shares_before": 3000.0, "shares_after": 3600.0,
                      "discretionary_shares": 600.0, "est_price": 11.0, "est_notional": 6600.0,
                      "est_notional_base": 6600.0, "est_price_band_reason": REASON, "confidence": "CLEAN"},
}


def rows(date, book):
    """book: {bloomberg id: (quantity, market_value)} -> canonical_shape-like Bloomberg rows (TXUE) + one cash line."""
    d = dt.date.fromisoformat(date)
    base = {"fund_ticker": "TXUE", "report_date": d, "dataset_revision": "r1", "source_used": "bloomberg",
            "security_id": None, "resolution_status": "UNRESOLVED", "weight": 0.01}
    out = [dict(base, position_type="cash", security_bloomberg="USD Curncy", raw_identifier="USD Curncy",
                quantity=1000.0, market_value=1000.0)]
    for k, (q, mv) in book.items():
        out.append(dict(base, position_type="long", security_bloomberg=k, raw_identifier=k, quantity=float(q),
                        market_value=float(mv)))
    return out


def same(x, y):
    if isinstance(y, float):
        return x is not None and x == x and abs(float(x) - y) < 1e-6
    return x == y


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds import gold_trade_schedule as g

    b0 = dict(BOOK, **{"ATD CN Equity": (1000.0, 50000.0), "TRM US Equity": (2000.0, 40000.0),
                       "ADD US Equity": (3000.0, 30000.0)})
    b1 = dict(BOOK, **{"ATD CN Equity": (0.0, 0.0), "TRM US Equity": (1500.0, 33000.0),
                       "ADD US Equity": (3600.0, 39600.0)})
    t = g.infer_trades(pd.DataFrame(rows(D0, b0) + rows(D1, b1)))
    by = {str(r["security_key"]): r for r in t.to_dict("records")}
    print("rows:", sorted((k, r["action"]) for k, r in by.items()))
    for key, want in BASE_ROWS.items():
        got = by.get(key, {})
        diff = {f: (got.get(f), w) for f, w in want.items() if not same(got.get(f), w)}
        print(f"  {key}: differs from base on {diff or 'nothing'}")
        v.check(bool(got) and not diff, f"control: the {want['action']} row of {key} is identical to the base output")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
