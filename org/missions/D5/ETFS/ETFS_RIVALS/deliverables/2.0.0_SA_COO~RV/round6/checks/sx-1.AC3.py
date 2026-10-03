"""RIV-sx-1 AC3 (CONTROL): where every holding has a GICS sector, the sector ranks are exactly today's -- the change
touches only the "Unclassified" bucket.

Interface: `gold_holding_contribution.build(g1, g4, day, universe_entries)` and
`gold_buying_trend.build(g5, g6, g1, day, universe_entries)`, signatures unchanged.

Fixtures: round 5's rk-1 book (A, C Information Technology; B, D Energy; page day 2026-10-05; funds TXUE and SCHY)
and tb-1 trades (S1, S2 Information Technology; S3, S4 Energy, S4 in a REFUSED window; day 2026-10-02; fund TXUE),
unchanged. The expected rows are today's output on them (recorded at base 2026-10-02; equal to the rk-1 / tb-1
arithmetic):
  - holding_contribution, every fund x period: IT 0.12 (rank_best 1, rank_worst 2), Energy -0.035 (rank_best 2,
    rank_worst 1), n_ranked 2, n_missing 0; no Unclassified row;
  - buying_trend: IT into rank 1 (+800, bet, '+ + + 0 0 0 0 0 0 0', 3 windows); Energy away rank 1 (-300, bet,
    '0 - 0 - 0 0 0 0 0 0', 2 windows); no Unclassified row."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

IT, EN = "Information Technology", "Energy"
HC_DAY, BT_DAY = "2026-10-05", "2026-10-02"
HC_ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"},
              {"group_id": "IDVZ", "fund_id": "SCHY", "role": "index_control"}]
BT_ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}]
SECTOR = {"S1": IT, "S2": IT, "S3": EN, "S4": EN}
TRADES = [("S1", "entry", "2026-01-15", 100.0), ("S1", "add", "2026-02-13", 100.0), ("S1", "add", "2026-03-13", 100.0),
          ("S2", "add", "2026-03-13", 500.0), ("S3", "trim", "2026-02-13", 50.0), ("S3", "exit", "2026-04-15", 250.0),
          ("S4", "add", "2026-05-15", 1000.0)]
G6 = (("2026-01-15", None, None), ("2026-02-13", None, None), ("2026-03-13", None, None), ("2026-04-15", None, None),
      ("2026-05-15", "REFUSED", "flow_factor_out_of_band"))


def hc_fixtures():
    import pandas as pd
    book = [("A", "Alpha", 0.6, IT), ("B", "Beta", 0.4, EN), ("C", "Gamma", 0.1, IT), ("D", "Delta", 0.05, EN)]
    g1 = pd.DataFrame([{"fund_id": f, "fund_ticker": f, "report_date": "2026-09-30", "security_id": s,
                        "security_name": n, "weight": w, "gics_sector": sec, "is_cash_line": False,
                        "position_type": "equity"}
                       for f in ("TXUE", "SCHY") for s, n, w, sec in book])
    px = {"A": (100.0, 110.0, 121.0), "B": (50.0, 45.0, 45.0)}
    g4 = pd.DataFrame([{"security_id": s, "date": d, "px_close": p[i], "total_return_index": None,
                        "gics_sector": IT if s == "A" else EN}
                       for s, p in px.items() for i, d in enumerate(("2026-09-30", "2026-10-01", "2026-10-02"))]
                      + [{"security_id": "D", "date": d, "px_close": p, "total_return_index": None, "gics_sector": EN}
                         for d, p in (("2026-10-01", 20.0), ("2026-10-02", 22.0))])
    return g1, g4


def bt_fixtures():
    import pandas as pd
    g5 = pd.DataFrame([{"fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": s, "security_key": s, "action": a,
                        "window_end": pd.Timestamp(d).date(), "est_notional_base": n} for s, a, d, n in TRADES])
    g6 = pd.DataFrame([{"fund_id": "TXUE", "window_end": pd.Timestamp(d).date(), "status": st, "reason": rs}
                       for d, st, rs in G6])
    g1 = pd.DataFrame([{"fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": "2026-01-02", "security_id": s,
                        "security_name": s, "gics_sector": sec, "is_cash_line": False} for s, sec in SECTOR.items()])
    return g5, g6, g1


def _i(x):
    return None if x is None or x != x else int(x)


def run(v):
    c.setup_path()
    from rivalfunds import gold_buying_trend as bt
    from rivalfunds import gold_holding_contribution as hc

    out = hc.build(*hc_fixtures(), HC_DAY, HC_ENTRIES)
    sct = out[out.axis == "sector"]
    cols = ["fund_id", "period", "bucket", "contribution", "rank_best", "rank_worst", "n_ranked", "n_missing"]
    print(sct[cols].to_string(index=False))
    got = sorted((str(r.fund_id), str(r.period), str(r.bucket), round(float(r.contribution), 9), _i(r.rank_best),
                  _i(r.rank_worst), _i(r.n_ranked), _i(r.n_missing)) for r in sct.itertuples())
    want = sorted((f, p, b, cv, rb, rw, 2, 0) for f in ("TXUE", "SCHY") for p in ("MTD", "QTD", "YTD", "R30")
                  for b, cv, rb, rw in ((IT, 0.12, 1, 2), (EN, -0.035, 2, 1)))
    v.check(got == want,
            "holding_contribution sector rows equal today's: IT 0.12 (1/2), Energy -0.035 (2/1), n_ranked 2")

    out = bt.build(*bt_fixtures(), BT_DAY, BT_ENTRIES)
    sct = out[out.axis == "sector"]
    cols = ["bucket", "lean", "rank", "net_notional_base", "reading", "trend_mark", "n_windows"]
    print(sct[cols].to_string(index=False))
    got = sorted((str(r.bucket), str(r.lean), _i(r.rank), round(float(r.net_notional_base), 6), str(r.reading),
                  str(r.trend_mark), _i(r.n_windows)) for r in sct.itertuples())
    want = [(EN, "away", 1, -300.0, "bet", "0 - 0 - 0 0 0 0 0 0", 2),
            (IT, "into", 1, 800.0, "bet", "+ + + 0 0 0 0 0 0 0", 3)]
    v.check(got == want, "buying_trend sector rows equal today's: IT into rank 1 (+800), Energy away rank 1 (-300)")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
