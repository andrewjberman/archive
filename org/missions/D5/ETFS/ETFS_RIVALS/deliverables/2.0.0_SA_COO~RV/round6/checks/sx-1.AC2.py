"""RIV-sx-1 AC2 (RFW-U16, RFW-D06 producer half): buying_trend never RANKS the no-sector bucket. Today a trade in a
security no fund's file classifies feeds a sector line "Unclassified" that is ranked among the sectors leaned into or
away from (BASG's top trend sector away: 'No GICS sector in the source').

Interface (prescribed): `gold_buying_trend.build(g5, g6, g1, day, universe_entries)` -- a sector-axis "Unclassified"
row has rank NULL (or is absent from the ranked leans), and its notional is kept in a sector-axis "Unclassified" row
(rank NULL) the page can footnote; the real sectors rank among themselves.

Fixture (the round-5 tb-1 trades, offline; day 2026-10-02, fund TXUE), plus S5: add +2000 in the window ending
2026-06-15, and no GICS sector for S5 in any fund's G1 file. Sector nets: Unclassified into +2000 (largest),
Information Technology into +800, Energy away -300.
  - a sector-axis Unclassified row carries net_notional_base +2000, and every sector-axis Unclassified row has rank
    NULL (today: into rank 1);
  - the real sectors rank among themselves: IT into rank 1, Energy away rank 1, and no other real sector line;
  - control: the security axis is untouched -- S5 is ranked there (into rank 1, net +2000)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-02"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}]
SECTOR = {"S1": "Information Technology", "S2": "Information Technology", "S3": "Energy", "S4": "Energy", "S5": None}
TRADES = [("S1", "entry", "2026-01-15", 100.0), ("S1", "add", "2026-02-13", 100.0), ("S1", "add", "2026-03-13", 100.0),
          ("S2", "add", "2026-03-13", 500.0), ("S3", "trim", "2026-02-13", 50.0), ("S3", "exit", "2026-04-15", 250.0),
          ("S4", "add", "2026-05-15", 1000.0), ("S5", "add", "2026-06-15", 2000.0)]
G6 = (("2026-01-15", None, None), ("2026-02-13", None, None), ("2026-03-13", None, None), ("2026-04-15", None, None),
      ("2026-05-15", "REFUSED", "flow_factor_out_of_band"), ("2026-06-15", None, None))


def fixtures():
    import pandas as pd
    g5 = pd.DataFrame([{"fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": s, "security_key": s, "action": a,
                        "window_end": pd.Timestamp(d).date(), "est_notional_base": n} for s, a, d, n in TRADES])
    g6 = pd.DataFrame([{"fund_id": "TXUE", "window_end": pd.Timestamp(d).date(), "status": st, "reason": rs}
                       for d, st, rs in G6])
    g1 = pd.DataFrame([{"fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": "2026-01-02", "security_id": s,
                        "security_name": s, "gics_sector": sec, "is_cash_line": False} for s, sec in SECTOR.items()])
    return g5, g6, g1


def null(x) -> bool:
    return x is None or x != x


def run(v):
    c.setup_path()
    from rivalfunds import gold_buying_trend as bt

    g5, g6, g1 = fixtures()
    out = bt.build(g5, g6, g1, DAY, ENTRIES)
    sct = out[out.axis == "sector"]
    print(sct[["bucket", "lean", "rank", "net_notional_base"]].to_string(index=False))
    un = sct[sct.bucket == "Unclassified"]
    v.check(len(un) >= 1 and any(abs(float(x) - 2000.0) < 1e-9 for x in un["net_notional_base"])
            and all(null(x) for x in un["rank"]),
            "the Unclassified sector line keeps net +2000 in a sector row whose rank is NULL")
    real = sct[sct.bucket != "Unclassified"]
    got = sorted((str(r.bucket), str(r.lean), None if null(r.rank) else int(r.rank),
                  round(float(r.net_notional_base), 6)) for r in real.itertuples())
    v.check(got == [("Energy", "away", 1, -300.0), ("Information Technology", "into", 1, 800.0)],
            "real sectors rank among themselves: IT into rank 1 (+800), Energy away rank 1 (-300)")
    s5 = out[(out.axis == "security") & (out.bucket == "S5")]
    print("security S5:", s5[["lean", "rank", "net_notional_base"]].values.tolist())
    v.check(len(s5) == 1 and str(s5.iloc[0]["lean"]) == "into" and not null(s5.iloc[0]["rank"])
            and int(s5.iloc[0]["rank"]) == 1 and abs(float(s5.iloc[0]["net_notional_base"]) - 2000.0) < 1e-9,
            "control: the security axis is untouched -- S5 is ranked there (into rank 1, +2000)")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
