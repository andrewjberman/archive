"""RIV-h-5 AC1 (hop-9 ruling b) -- a window whose flow factor is implausible is REFUSED, never inferred; the thresholds live in
guardrails_config.json.

Pure, offline (the test_g2 fixture book):
  - config: `guardrails.load_config()` carries `flow_factor_band` ([0.5, 1.5]) and `max_zero_quantity_share` (0.20), PROVISIONAL;
  - f out of band: a book scaled x1.8 with one moved line -> the G6 row reads status REFUSED, reason flow_factor_out_of_band, and
    `infer_trades` returns 0 rows for that window;
  - zero-quantity share: 4 of 8 lines at quantity 0 on day 2 -> REFUSED, reason zero_quantity_share, 0 trades;
  - control: a book scaled x1.037 with one moved line is not refused and infers its 1 trade."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import gold_trade_schedule as g
    from rivalfunds import guardrails
    from rivalfunds.tests.test_g2_trade_schedule import BOOK, _cs, _scale

    cfg = guardrails.load_config()
    band, share = cfg.get("flow_factor_band", {}), cfg.get("max_zero_quantity_share", {})
    print("config:", band.get("value"), band.get("status"), share.get("value"), share.get("status"))
    v.check(list(band.get("value") or []) == [0.5, 1.5] and share.get("value") == 0.2
            and band.get("status") == share.get("status") == "PROVISIONAL",
            "guardrails_config carries flow_factor_band [0.5, 1.5] and max_zero_quantity_share 0.20, PROVISIONAL")

    def moved(book, k="S3", f=1.25):
        b = dict(book)
        q, p = b[k]
        b[k] = (q * f, p)
        return b

    def window(day2):
        df = _cs(("2026-09-28", BOOK), ("2026-09-29", day2))
        rec = g.infer_recon(df)
        st = rec["status"].astype(str).tolist() if "status" in rec.columns else ["<no status column>"]
        rs = rec["reason"].astype(str).tolist() if "reason" in rec.columns else ["<no reason column>"]
        return st, rs, len(g.infer_trades(df))

    st, rs, n = window(moved(_scale(BOOK, 1.8)))
    print("x1.8:", st, rs, "trades", n)
    v.check(st == ["REFUSED"] and rs == ["flow_factor_out_of_band"] and n == 0, "f=1.8 is REFUSED (flow_factor_out_of_band), 0 trades")
    zero = {k: ((0.0 if i < 4 else q), p) for i, (k, (q, p)) in enumerate(BOOK.items())}
    st, rs, n = window(zero)
    print("4/8 zero:", st, rs, "trades", n)
    v.check(st == ["REFUSED"] and rs == ["zero_quantity_share"] and n == 0, "a 50% zero-quantity window is REFUSED, 0 trades")
    st, rs, n = window(moved(_scale(BOOK, 1.037)))
    print("x1.037 control:", st, rs, "trades", n)
    v.check("REFUSED" not in st and n == 1, "control: f=1.037 with one move is not refused and infers 1 trade")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
