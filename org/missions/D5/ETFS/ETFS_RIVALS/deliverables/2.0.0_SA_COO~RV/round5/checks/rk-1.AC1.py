"""RIV-rk-1 AC1 (FWD-14 producer, amendment A1) -- holding contribution is the sum over the period's trading days of the prior
day's reported weight times the day's return, ranked per fund x period x axis; a holding with no price is kept as missing.

Pure, offline fixture (page day 2026-10-05, as-of T-1 2026-10-02 per CRO~RV CALL 3; one G1 report dated 2026-09-30; G4 prices on 2026-09-30, 10-01, 10-02):
  A weight 0.6, px 100 -> 110 -> 121 (returns +10%, +10%)  => MTD contribution 0.6*0.1 + 0.6*0.1 = 0.12
  B weight 0.4, px  50 ->  45 ->  45 (returns -10%, 0%)    => MTD contribution -0.04
  C weight 0.1, no G4 price at all                         => missing, kept, never ranked
  D weight 0.05, px only on 10-01 (20) and 10-02 (22)      => partial: 0.05*0.1 = 0.005, still ranked
  sectors: A and C Tech, B and D Energy => Tech 0.12, Energy -0.035
  - periods MTD, QTD, YTD and R30 all present; MTD security A = 0.12 and B = -0.04; A ranks best and B worst (rank 1 each);
  - C's MTD row exists with a null contribution, price_coverage missing, and n_missing = 1 on the MTD security rows;
  - sector rows Tech 0.12 and Energy -0.035;
  - the benchmark SCHY (index_control, same book) is measured by the same rule (its MTD A row also reads 0.12);
  - control: D is `partial` with contribution 0.005 and is ranked; the fund's first report (2026-09-30) is its YTD period_start."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-05"  # page day (Monday); CRO~RV CALL 3: periods run through prev_trading_day(DAY) = 2026-10-02
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}, {"group_id": "IDVZ", "fund_id": "SCHY", "role": "index_control"}]


def fixtures():
    import pandas as pd
    book = [("A", "Alpha", 0.6, "Information Technology"), ("B", "Beta", 0.4, "Energy"), ("C", "Gamma", 0.1, "Information Technology"),
            ("D", "Delta", 0.05, "Energy")]
    g1 = pd.DataFrame([{"fund_id": f, "fund_ticker": f, "report_date": "2026-09-30", "security_id": s, "security_name": n,
                        "weight": w, "gics_sector": sec, "is_cash_line": False, "position_type": "equity"}
                       for f in ("TXUE", "SCHY") for s, n, w, sec in book])
    px = {"A": (100.0, 110.0, 121.0), "B": (50.0, 45.0, 45.0)}
    g4 = pd.DataFrame([{"security_id": s, "date": d, "px_close": p[i], "total_return_index": None,
                        "gics_sector": "Information Technology" if s == "A" else "Energy"}
                       for s, p in px.items() for i, d in enumerate(("2026-09-30", "2026-10-01", "2026-10-02"))]
                      + [{"security_id": "D", "date": d, "px_close": p, "total_return_index": None, "gics_sector": "Energy"}
                         for d, p in (("2026-10-01", 20.0), ("2026-10-02", 22.0))])
    return g1, g4


def run(v):
    c.setup_path()
    from rivalfunds import gold_holding_contribution as hc

    g1, g4 = fixtures()
    out = hc.build(g1, g4, DAY, ENTRIES)
    print("columns:", list(out.columns))
    print("periods:", sorted(set(out["period"])))
    v.check(set(out["period"]) == {"MTD", "QTD", "YTD", "R30"}, "periods MTD, QTD, YTD and R30 are all present")

    def row(fund, period, axis, bucket):
        r = out[(out.fund_id == fund) & (out.period == period) & (out.axis == axis) & (out.bucket == bucket)]
        return r.iloc[0].to_dict() if len(r) == 1 else None

    a, b, cc = (row("TXUE", "MTD", "security", k) for k in ("A", "B", "C"))
    print("MTD A:", a and (a["contribution"], a["rank_best"], a["price_coverage"]))
    print("MTD B:", b and (b["contribution"], b["rank_worst"]))
    print("MTD C:", cc and (cc["contribution"], cc["price_coverage"], cc["n_missing"]))
    v.check(a is not None and b is not None and abs(a["contribution"] - 0.12) < 1e-9 and abs(b["contribution"] + 0.04) < 1e-9
            and a["rank_best"] == 1 and b["rank_worst"] == 1,
            "MTD: A contributes 0.12 and ranks best, B contributes -0.04 and ranks worst")
    v.check(cc is not None and (cc["contribution"] is None or cc["contribution"] != cc["contribution"])
            and cc["price_coverage"] == "missing" and int(cc["n_missing"]) == 1,
            "C has no price: its row is kept with a null contribution, coverage missing, n_missing 1")
    tech, en = row("TXUE", "MTD", "sector", "Information Technology"), row("TXUE", "MTD", "sector", "Energy")
    print("sectors:", tech and tech["contribution"], en and en["contribution"])
    v.check(tech is not None and en is not None and abs(tech["contribution"] - 0.12) < 1e-9 and abs(en["contribution"] + 0.035) < 1e-9,
            "sector rows: Information Technology 0.12, Energy -0.035")
    sa = row("SCHY", "MTD", "security", "A")
    v.check(sa is not None and abs(sa["contribution"] - 0.12) < 1e-9, "the benchmark SCHY is measured by the same rule")
    d, ya = row("TXUE", "MTD", "security", "D"), row("TXUE", "YTD", "security", "A")
    print("MTD D:", d and (d["contribution"], d["price_coverage"], d["rank_best"]), "| YTD period_start:", ya and str(ya["period_start"])[:10])
    v.check(d is not None and d["price_coverage"] == "partial" and abs(d["contribution"] - 0.005) < 1e-9 and d["rank_best"] == 2
            and ya is not None and str(ya["period_start"])[:10] == "2026-09-30",
            "control: D is partial (0.005, ranked 2nd best); YTD starts at the fund's first report, 2026-09-30")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
