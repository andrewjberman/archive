"""RIV-e-2 AC4 (issuer amendment A1, 2026-10-02): a dividend currency in Bloomberg MINOR units converts at its major
currency's rate divided by 100.

Source: the issuer's live DVD_CRNCY read at ~17:2xZ (6 securities): BATS LN -> "GBp" (pence), NPN SJ -> "ZAr" (rand
cents), SHEL LN -> "USD", TEVA IT -> "USD", ASML NA -> "EUR", 8306 JP -> "JPY". Bloomberg's minor-unit codes are GBp/GBX
(GBP / 100), ZAr/ZAc (ZAR / 100) and ILs/ILa (ILS / 100). As built, e-2 makes a G3 currency win, and "GBp" has no
"GBp Curncy" rate, so BATS-style pence dividends would read UNCONVERTED.

Fixture: test_g52's canonical-shape builder; rates from the funds' own `<CCY> Curncy` lines (JPY 0.0064, GBP 1.25,
ZAR 0.055, EUR 1.1). Positions: S1 JP 1000 sh, S2 LN 500 sh, S3 SJ 200 sh. Dividends per share: S1 2.0, S2 1.0, S3 300.0.
  (a) S2 paying "GBp" and S3 paying "ZAr" convert at GBP/100 and ZAR/100:
      income = 2*1000*0.0064 + 1*500*1.25/100 + 300*200*0.055/100 = 12.8 + 6.25 + 33.0 = 52.05;
  (b) "GBX" reads like "GBp" (12.8 + 6.25 + 33.0, with S3 at "ZAc");
  (c) CONTROL: S2 paying "USD" (SHEL LN) and S3 paying "JPY" convert at 1.0 and 0.0064 (12.8 + 500 + 384).
At e-2's first build (6ccc54f65e): (a) and (b) FAIL (the minor units read UNCONVERTED), (c) PASS.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import pandas as pd
    from rivalfunds import gold_trade_schedule as g
    from rivalfunds.tests.test_g52_trade_schedule_v2 import D2, D3, _canon, _g3

    b = {"S1 JP Equity": (1000.0, 10.0), "S2 LN Equity": (500.0, 20.0), "S3 SJ Equity": (200.0, 100.0)}
    cash = {"USD": (100.0, 0.0), "JPY": (1_000_000.0, 6400.0), "GBP": (1000.0, 1250.0), "ZAR": (10000.0, 550.0),
            "EUR": (1000.0, 1100.0)}
    canon = pd.DataFrame(_canon(D2, b, cash=cash) + _canon(D3, b, cash=cash))

    def income(ccy_ln, ccy_sj):
        acts = _g3(("S1 JP Equity", "cash_div", D3, 2.0), ("S2 LN Equity", "cash_div", D3, 1.0),
                   ("S3 SJ Equity", "cash_div", D3, 300.0))
        acts["currency"] = ["JPY", ccy_ln, ccy_sj]
        row = g.infer_recon(canon, acts).iloc[0]
        return float(row["income_received_base"]), row

    def near(x, y):
        return abs(x - y) < 1e-6 * max(1.0, abs(y))

    got, row = income("GBp", "ZAr")
    want = 2 * 1000 * 0.0064 + 1 * 500 * 1.25 / 100 + 300 * 200 * 0.055 / 100
    print(f"(a) GBp/ZAr: income_received_base {got:.4f} want {want:.4f}")
    v.check(near(got, want), "(a) GBp and ZAr dividends convert at GBP/100 and ZAR/100 (today: UNCONVERTED)")

    got, _ = income("GBX", "ZAc")
    print(f"(b) GBX/ZAc: income_received_base {got:.4f} want {want:.4f}")
    v.check(near(got, want), "(b) GBX and ZAc read as GBp and ZAr")

    got, _ = income("USD", "JPY")
    want_c = 2 * 1000 * 0.0064 + 1 * 500 * 1.0 + 300 * 200 * 0.0064
    print(f"(c) USD/JPY: income_received_base {got:.4f} want {want_c:.4f}")
    v.check(near(got, want_c), "(c) control: a major currency (SHEL LN paying USD; JPY) converts at its own rate")


failures = c.guarded("AC4", run)
print("AC4 RESULT: PASS 0 failures" if failures == 0 else f"AC4 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
