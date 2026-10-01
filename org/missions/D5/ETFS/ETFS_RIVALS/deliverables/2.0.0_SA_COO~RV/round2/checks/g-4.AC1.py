"""RIV-g-4 AC1 -- over REAL data (the last 6 IDVZ-group captures + the real dividends import): no trade in G5 is on a cash
or currency line (a ' Curncy' security or an is_cash_line position); G6 flow_reconciliation holds one row per rival x window
with its columns; and cash-line movement was RECORDED, not discarded -- SCHY (CRO~Z: 59% of raw events on cash lines) has
a non-zero cash_line_delta_base in at least one window."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    files = c.idvz_captures(6)
    sink = c.tmpdir("rv_g52a_")
    res = c.run_idvz_chain(sink, files, "trades")
    print("trades:", str(res.get("trades"))[:300])
    t, _ = c.read_parquets(c.gold_dir(sink, "trade_schedule"))
    g6, n6 = c.read_parquets(c.gold_dir(sink, "flow_reconciliation"))
    v.check(len(t) > 0, f"G5 rows {len(t)}")
    sec = t["security_id"].astype(str) if "security_id" in t.columns else None
    v.check(sec is not None and not sec.str.endswith(" Curncy").any(), "no G5 trade on a ' Curncy' security")
    v.check(n6 >= 1 and len(g6) > 0, f"G6 objects {n6}, rows {len(g6)}")
    for col in ["fund_id", "window_end", "flow_factor_f", "cash_line_delta_base", "income_received_base", "fx_conversion_base",
                "corporate_action_count", "income_funded_trade_count", "unexplained_residual_base", "claim"]:
        v.check(col in g6.columns, f"G6 column {col}")
    if {"fund_id", "window_end"} <= set(g6.columns):
        per = g6.groupby("fund_id")["window_end"].nunique().to_dict()
        v.check(all(per.get(f, 0) >= 4 for f in c.IDVZ_GROUP[1:]), f"G6 windows per rival (>= 4 of 5 pairs) {per}")
    if "cash_line_delta_base" in g6.columns:
        schy = g6[g6["fund_id"] == "SCHY"]["cash_line_delta_base"].abs()
        v.check(len(schy) and float(schy.max()) > 0, f"SCHY cash-line movement recorded (max |delta| {float(schy.max()) if len(schy) else None})")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
