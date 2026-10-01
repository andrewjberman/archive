"""RIV-h-5 AC2 (hop-9 ruling b, the seam against REAL G1) -- the CTO's named implausible windows are REFUSED with 0 trades.

READ-ONLY S3: for INEQ 2025-08-29 and TXUE 2025-04-14, the served G1 rows of the window (own prior report date -> the date) feed the
merged `infer_recon` / `infer_trades` locally.
  - each named window's G6 row reads status REFUSED and the window infers 0 trades;
  - control: INEQ's PREVIOUS window (ending on its prior report date) is not refused (the rule does not refuse everything)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

NAMED = [("INEQ", "2025-08-29"), ("TXUE", "2025-04-14")]


def run(v):
    c.setup_path()
    from rivalfunds import gold_trade_schedule as g

    def window(fund, end):
        prior = c.served_prior_date(fund, end)
        df = c.served_g1_fund(fund, [prior, end]) if prior else None
        if df is None or not len(df):
            return prior, None, None, None
        rec = g.infer_recon(df)
        st = rec["status"].astype(str).tolist() if "status" in rec.columns else ["<no status column>"]
        f = rec["flow_factor_f"].round(3).tolist() if "flow_factor_f" in rec.columns else None
        return prior, st, f, len(g.infer_trades(df))

    for fund, end in NAMED:
        prior, st, f, n = window(fund, end)
        print(f"{fund} {prior} -> {end}: status {st}, f {f}, trades {n}")
        v.check(st == ["REFUSED"] and n == 0, f"{fund} {end} is REFUSED with 0 trades")
    prior = c.served_prior_date("INEQ", "2025-08-29")
    p2, st, f, n = window("INEQ", prior) if prior else (None, None, None, None)
    print(f"control INEQ {p2} -> {prior}: status {st}, f {f}, trades {n}")
    v.check(st is not None and "REFUSED" not in st, "control: INEQ's previous window is not refused")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
