"""RIV-sx-1 AC4 (CRO GICS census Fix 1, CRO~RV CALL 9 (b)): the RANKINGS producer applies the cross-fund GICS fallback
the trend already applies -- a security with no GICS sector of its own takes the sector another fund's file states for
it. Source: docs/briefs/rivalfunds-gics-census-20261002.md section 3 Fix 1 (308f982bb8; 220 lines joinable, INEQ ~0% ->
99% classified); org/tier1_exec/4.0.0_SA_CRO/deliverables/ETFS_RIVALS_RULINGS_20261002.md CALL 9 (b). Today
holding_contribution reads the fund's own G1 sector (newest report, then older ones), then G4, else "Unclassified"
(`gold_holding_contribution.py:190`, `:209`, decided at `:346`), so X below sits in Unclassified.

Precedence mirrored from `gold_buying_trend.py` `_sector_src` (:90-97, history built by `_sectors` :61-83): the fund's
OWN G1 sector first ("own"); else the security's GICS sector in ANY fund's G1 file, date-sorted, as of the date
("other_fund"); else "Unclassified". The trend never reads G4, so it fixes no order between G4 and the other-fund file:
this fixture gives X, Y and Z no G4 row at all, and the check holds whichever of the two a fix puts first.

Interface: `gold_holding_contribution.build(g1, g4, day, universe_entries)`, signature unchanged.

Fixture (offline; page day 2026-10-05, as-of 2026-10-02; G4 empty). Fund TXUE (A) reports on 2026-09-30, 10-01 and
10-02, quantity 100 each, priced from its own valuation (holding_implied, CALL 1):
  X: weight 0.4, no gics_sector in TXUE's file, market value 1000 -> 1100 -> 1100   -> contribution 0.04;
  Y: weight 0.2, no gics_sector in ANY file,     market value 1000 -> 1000 -> 1050   -> contribution 0.01;
  Z: weight 0.3, gics_sector Energy in TXUE's file, market value 1000 -> 1020 -> 1020 -> contribution 0.006.
Fund BIDD (B) reports once (2026-09-30): X with gics_sector Financials, Z with gics_sector Utilities.
  - (a) TXUE's sector axis carries X's 0.04 under "Financials" in every period (MTD, QTD, YTD, R30);
  - (b) Y stays Unclassified: TXUE's Unclassified row carries Y's 0.01 in every period, plus X's 0.04 only in a period
    where (a) has not moved X (so X is never counted twice);
  - (c) control, own file wins: TXUE's Energy row carries Z's 0.006 and TXUE has no Utilities row.
FAIL at base: (a) FAILs (no Financials row; X sits in Unclassified, which reads 0.05); (b) and (c) PASS. Ranks are not
graded here (sx-1.AC1-3 grade them; Unclassified rank NULL is compatible with every limb)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-05"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"},
           {"group_id": "IDVZ", "fund_id": "BIDD", "role": "rival"}]
FIN, EN, UT, UN = "Financials", "Energy", "Utilities", "Unclassified"
PERIODS = ("MTD", "QTD", "YTD", "R30")
CX, CY, CZ = 0.04, 0.01, 0.006
# security: (name, weight, TXUE's own gics_sector, market values on 09-30 / 10-01 / 10-02)
BOOK_A = {"X": ("Xeno", 0.4, None, (1000.0, 1100.0, 1100.0)), "Y": ("Ypsilon", 0.2, None, (1000.0, 1000.0, 1050.0)),
          "Z": ("Zeta", 0.3, EN, (1000.0, 1020.0, 1020.0))}
BOOK_B = {"X": ("Xeno", 0.5, FIN), "Z": ("Zeta", 0.5, UT)}
DATES = ("2026-09-30", "2026-10-01", "2026-10-02")


def fixtures():
    import pandas as pd
    base = {"is_cash_line": False, "position_type": "equity", "asset_class": "Equity", "quantity": 100.0}
    g1 = [dict(base, fund_id="TXUE", fund_ticker="TXUE", report_date=d, security_id=s, security_name=n, weight=w,
               gics_sector=sec, market_value=mv[i])
          for i, d in enumerate(DATES) for s, (n, w, sec, mv) in BOOK_A.items()]
    g1 += [dict(base, fund_id="BIDD", fund_ticker="BIDD", report_date=DATES[0], security_id=s, security_name=n,
                weight=w, gics_sector=sec, market_value=500.0) for s, (n, w, sec) in BOOK_B.items()]
    g4 = pd.DataFrame(columns=["security_id", "date", "px_close", "total_return_index", "gics_sector"])
    return pd.DataFrame(g1), g4


def null(x) -> bool:
    return x is None or x != x


def near(x, want) -> bool:
    return not null(x) and abs(float(x) - want) < 1e-9


def run(v):
    c.setup_path()
    from rivalfunds import gold_holding_contribution as hc

    g1, g4 = fixtures()
    out = hc.build(g1, g4, DAY, ENTRIES)
    sec = out[(out.axis == "security") & (out.fund_id == "TXUE") & (out.period == "MTD")]
    print("security axis (TXUE MTD):", sorted((str(r.bucket), None if null(r.contribution) else round(
        float(r.contribution), 9), str(r.price_source)) for r in sec.itertuples()))
    sct = out[(out.axis == "sector") & (out.fund_id == "TXUE")]
    print(sct[["fund_id", "period", "bucket", "contribution", "price_coverage"]].to_string(index=False))

    def contrib(period, bucket):
        x = sct[(sct.period == period) & (sct.bucket == bucket)]
        return x.iloc[0]["contribution"] if len(x) == 1 else None

    moved = {p: near(contrib(p, FIN), CX) for p in PERIODS}
    v.check(all(moved.values()),
            "(a) TXUE carries X's 0.04 under Financials (the sector BIDD's file states) in every period")
    v.check(all(near(contrib(p, UN), CY + (0.0 if moved[p] else CX)) for p in PERIODS),
            "(b) Y stays Unclassified: TXUE's Unclassified row carries Y's 0.01 in every period (plus X's 0.04 only "
            "where X has not moved)")
    v.check(all(near(contrib(p, EN), CZ) for p in PERIODS) and not (sct.bucket == UT).any(),
            "(c) control, own file wins: TXUE's Energy row carries Z's 0.006 and TXUE has no Utilities row")


failures = c.guarded("AC4", run)
print("AC4 RESULT: PASS 0 failures" if failures == 0 else f"AC4 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
