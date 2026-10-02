"""RIV-sx-1 AC1 (RFW-U16, RFW-D06 producer half): holding_contribution never RANKS the no-sector bucket. Today a
security with no GICS sector lands in a sector row "Unclassified" that is ranked like a sector (GQGU YTD:
'1 Unclassified +3.83%').

Interface (prescribed): `gold_holding_contribution.build(g1, g4, day, universe_entries)` -- a sector-axis row with
bucket "Unclassified" keeps its contribution but has rank_best and rank_worst NULL, and is excluded from the sector
`n_ranked`; the real sectors rank 1..n among themselves.

Fixture (the round-5 rk-1 book, offline; page day 2026-10-05, as-of 2026-10-02; funds TXUE and SCHY, one G1 report
dated 2026-09-30), plus E: weight 0.5, no GICS sector in G1 or G4, px 10 -> 13 -> 13, so the Unclassified bucket is
the STRONGEST. Sectors (every period): Information Technology 0.12 (A; C unpriced), Energy -0.035 (B -0.04,
D 0.005), Unclassified 0.15.
  - every Unclassified sector row keeps contribution 0.15 and has rank_best and rank_worst NULL (today 1 and 3);
  - the real sectors rank among themselves: IT rank_best 1 / rank_worst 2, Energy rank_best 2 / rank_worst 1,
    n_ranked 2;
  - control: the security axis is untouched -- E is ranked there (rank_best 1 of 4 priced securities, MTD)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-05"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"},
           {"group_id": "IDVZ", "fund_id": "SCHY", "role": "index_control"}]
IT, EN, UN = "Information Technology", "Energy", "Unclassified"


def fixtures():
    import pandas as pd
    book = [("A", "Alpha", 0.6, IT), ("B", "Beta", 0.4, EN), ("C", "Gamma", 0.1, IT), ("D", "Delta", 0.05, EN),
            ("E", "Epsilon", 0.5, None)]
    g1 = pd.DataFrame([{"fund_id": f, "fund_ticker": f, "report_date": "2026-09-30", "security_id": s,
                        "security_name": n, "weight": w, "gics_sector": sec, "is_cash_line": False,
                        "position_type": "equity"}
                       for f in ("TXUE", "SCHY") for s, n, w, sec in book])
    px = {"A": ((100.0, 110.0, 121.0), IT), "B": ((50.0, 45.0, 45.0), EN), "E": ((10.0, 13.0, 13.0), None)}
    g4 = pd.DataFrame([{"security_id": s, "date": d, "px_close": p[i], "total_return_index": None, "gics_sector": sec}
                       for s, (p, sec) in px.items() for i, d in enumerate(("2026-09-30", "2026-10-01", "2026-10-02"))]
                      + [{"security_id": "D", "date": d, "px_close": p, "total_return_index": None, "gics_sector": EN}
                         for d, p in (("2026-10-01", 20.0), ("2026-10-02", 22.0))])
    return g1, g4


def null(x) -> bool:
    return x is None or x != x


def run(v):
    c.setup_path()
    from rivalfunds import gold_holding_contribution as hc

    g1, g4 = fixtures()
    out = hc.build(g1, g4, DAY, ENTRIES)
    sct = out[out.axis == "sector"]
    cols = ["fund_id", "period", "bucket", "contribution", "rank_best", "rank_worst", "n_ranked"]
    print(sct[cols].to_string(index=False))
    un = sct[sct.bucket == UN]
    v.check(len(un) == 8 and all(abs(float(x) - 0.15) < 1e-9 for x in un["contribution"])
            and all(null(x) for x in un["rank_best"]) and all(null(x) for x in un["rank_worst"]),
            "every Unclassified sector row (2 funds x 4 periods) keeps contribution 0.15 with rank_best and "
            "rank_worst NULL")
    real = sct[sct.bucket != UN]
    got = sorted((str(r.fund_id), str(r.period), str(r.bucket), None if null(r.rank_best) else int(r.rank_best),
                  None if null(r.rank_worst) else int(r.rank_worst), None if null(r.n_ranked) else int(r.n_ranked))
                 for r in real.itertuples())
    want = sorted((f, p, b, rb, rw, 2) for f in ("TXUE", "SCHY") for p in ("MTD", "QTD", "YTD", "R30")
                  for b, rb, rw in ((IT, 1, 2), (EN, 2, 1)))
    v.check(got == want, "real sectors rank among themselves: IT best 1 / worst 2, Energy best 2 / worst 1, n_ranked 2")
    e = out[(out.axis == "security") & (out.fund_id == "TXUE") & (out.period == "MTD") & (out.bucket == "E")]
    print("security E (TXUE MTD):", e[["contribution", "rank_best", "n_ranked"]].values.tolist())
    v.check(len(e) == 1 and not null(e.iloc[0]["rank_best"]) and int(e.iloc[0]["rank_best"]) == 1
            and int(e.iloc[0]["n_ranked"]) == 4,
            "control: the security axis is untouched -- E is ranked there (best 1 of 4)")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
