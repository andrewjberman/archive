"""RIV-x-1 AC1 (RFW-D10): a full exit is priced from the PRIOR report's valuation and says so.

Pure, offline (`gold_trade_schedule.infer_trades` over a hand-built TXUE-like Bloomberg book; no sink, no S3).
One window 2026-09-29 -> 2026-09-30, flow factor 1.0 (the rest of the book is unchanged):
  - ZERO-LATER exit (the defect as served: TXUE "trim ATD_CN_Equity 138,182 -> 0", est. price and notional n/a):
    prior report qty 1000, market_value 50,000; the later report CARRIES the line at quantity 0, market_value 0
    -> one row, action `exit`, est_price == 50.0, est_notional == est_notional_base == -50,000,
    est_price_source == "prior_valuation";
  - ABSENT-LATER exit: prior report qty 1000, market_value 50,000; the line is absent from the later report
    -> the same values and est_price_source == "prior_valuation".
Interface: G5 gains the column `est_price_source` (in `gold_trade_schedule.SCHEMA` / `COLUMNS`). An exit (the line is
in the prior report with quantity > 0 and absent, or at quantity 0, in the later one) is action `exit` with
est_price = prior market_value / prior quantity and est_notional = est_notional_base = minus the prior market_value
(base currency, as today), est_price_source "prior_valuation". `est_price_band_reason` is not reused.
A 0 -> 0 row is not an exit (x-1 AC3)."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D0, D1 = "2026-09-29", "2026-09-30"
BOOK = {f"S{i} US Equity": (1000.0 + 10 * i, (1000.0 + 10 * i) * (10.0 + i)) for i in range(12)}


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


def near(x, y):
    return x is not None and x == x and abs(float(x) - y) < 1e-6


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds import gold_trade_schedule as g

    b0 = dict(BOOK, **{"ATD CN Equity": (1000.0, 50000.0), "GONE CN Equity": (1000.0, 50000.0)})
    b1 = dict(BOOK, **{"ATD CN Equity": (0.0, 0.0)})          # GONE CN Equity is absent from the later report
    t = g.infer_trades(pd.DataFrame(rows(D0, b0) + rows(D1, b1)))
    by = {str(r["security_key"]): r for r in t.to_dict("records")}
    print("est_price_source in COLUMNS:", "est_price_source" in g.COLUMNS)
    for k in ("ATD CN Equity", "GONE CN Equity"):
        r = by.get(k, {})
        print(f"  {k}: action {r.get('action')} est_price {r.get('est_price')} est_notional"
              f" {r.get('est_notional')} base {r.get('est_notional_base')}"
              f" source {r.get('est_price_source', '<no column>')}")
    z, a = by.get("ATD CN Equity", {}), by.get("GONE CN Equity", {})
    v.check(z.get("action") == "exit", "a line carried at quantity 0 in the later report is an exit (today: a trim)")
    v.check(near(z.get("est_price"), 50.0) and near(z.get("est_notional"), -50000.0)
            and near(z.get("est_notional_base"), -50000.0),
            "the zero-later exit is priced: est_price 50.0, est_notional = est_notional_base = -50,000 (today: n/a)")
    v.check(z.get("est_price_source") == "prior_valuation", "the zero-later exit's est_price_source is prior_valuation")
    v.check(a.get("action") == "exit" and near(a.get("est_price"), 50.0) and near(a.get("est_notional"), -50000.0)
            and near(a.get("est_notional_base"), -50000.0),
            "the absent-later exit: est_price 50.0, est_notional = est_notional_base = -50,000")
    v.check(a.get("est_price_source") == "prior_valuation",
            "the absent-later exit's est_price_source is prior_valuation")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
