"""RIV-x-1 AC3 (RFW-D10, control; CRO CALL 12): a 0 -> 0 row is NOT an exit and no notional is invented for it.

Pure, offline (`gold_trade_schedule.infer_trades`; no sink, no S3). One window 2026-09-29 -> 2026-09-30, flow
factor 1.0, a 16-line book (so three zero lines stay under the max_zero_quantity_share refusal), in the SAME frame
as a priceable exit:
  - Z0: carried at quantity 0, market_value 0 on the prior report, absent from the later one -> today's row
    unchanged: action exit, shares 0 -> 0, est_price, est_notional and est_notional_base NULL, est_price_source
    (if present) not "prior_valuation";
  - Z1: quantity 0 but a stale market_value 1,234.50 on the prior report, absent later -> the same: NULL notional
    (the prior valuation is never read for a line that held no shares);
  - Z2: quantity 0 on both reports -> no row (as today).
Interface: the exit rule of x-1 AC1 applies only where the prior quantity is > 0."""
import datetime as dt
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D0, D1 = "2026-09-29", "2026-09-30"
BOOK = {f"S{i} US Equity": (1000.0 + 10 * i, (1000.0 + 10 * i) * (10.0 + i)) for i in range(16)}


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


def null(x):
    return x is None or x != x


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds import gold_trade_schedule as g

    b0 = dict(BOOK, **{"GONE CN Equity": (1000.0, 50000.0), "Z0 US Equity": (0.0, 0.0),
                       "Z1 US Equity": (0.0, 1234.5), "Z2 US Equity": (0.0, 0.0)})
    b1 = dict(BOOK, **{"Z2 US Equity": (0.0, 0.0)})
    df = pd.DataFrame(rows(D0, b0) + rows(D1, b1))
    rec = g.infer_recon(df)
    t = g.infer_trades(df)
    by = {str(r["security_key"]): r for r in t.to_dict("records")}
    print("window status:", rec["status"].tolist(), "| rows:", sorted((k, r["action"]) for k, r in by.items()))
    v.check(rec["status"].isna().all() and "GONE CN Equity" in by,
            "control: the window is inferred (not refused) and has its exit")
    for k in ("Z0 US Equity", "Z1 US Equity"):
        r = by.get(k, {})
        print(f"  {k}: action {r.get('action')} shares {r.get('shares_before')} -> {r.get('shares_after')}"
              f" est_price {r.get('est_price')} est_notional {r.get('est_notional')}"
              f" base {r.get('est_notional_base')} source {r.get('est_price_source', '<no column>')}")
        v.check(r.get("action") == "exit" and r.get("shares_before") == 0.0 and r.get("shares_after") == 0.0,
                f"{k}: the 0 -> 0 row is as today (action exit, shares 0 -> 0)")
        v.check(null(r.get("est_price")) and null(r.get("est_notional")) and null(r.get("est_notional_base"))
                and r.get("est_price_source") != "prior_valuation",
                f"{k}: no price or notional is invented for a line that held no shares")
    v.check("Z2 US Equity" not in by, "a line at quantity 0 on both reports yields no row")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
