"""RIV-tb-1 AC1 (FWD-15 producer, amendment A1) -- the year-to-date buying trend ranks what each fund leaned into and away from,
reads each line as a tilt or a bet, marks the trend by month in ASCII, and excludes a REFUSED window.

Pure, offline fixture (day 2026-10-02, fund TXUE; signed notional = +|est_notional_base| for entry/add, -|.| for trim/exit):
  S1 Tech   : entry 01-15 +100, add 02-13 +100, add 03-13 +100  -> net +300, largest window 1/3       -> tilt
  S2 Tech   : add 03-13 +500                                     -> net +500, one window                -> bet
  S3 Energy : trim 02-13 -50, exit 04-15 -250                    -> net -300, largest window 250/300    -> bet, leaned AWAY
  S4 Energy : add 05-15 +1000 in a window G6 marks REFUSED       -> excluded, counted in n_refused_windows
  - into: S2 rank 1, S1 rank 2; away: S3 rank 1; S4 has no row;
  - readings: S1 tilt, S2 bet, S3 bet; S1's trend_mark is "+ + + 0 0 0 0 0 0 0" (Jan..Oct) and every mark is ASCII;
  - sector rows: Information Technology into +800; Energy away -300; n_refused_windows 1;
  - control: n_trading_days equals the calendar's year-to-date trading days through 2026-10-02."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-10-02"
ENTRIES = [{"group_id": "IDVZ", "fund_id": "TXUE", "role": "rival"}]
SECTOR = {"S1": "Information Technology", "S2": "Information Technology", "S3": "Energy", "S4": "Energy"}
TRADES = [("S1", "entry", "2026-01-15", 100.0), ("S1", "add", "2026-02-13", 100.0), ("S1", "add", "2026-03-13", 100.0),
          ("S2", "add", "2026-03-13", 500.0), ("S3", "trim", "2026-02-13", 50.0), ("S3", "exit", "2026-04-15", 250.0),
          ("S4", "add", "2026-05-15", 1000.0)]


def fixtures():
    import pandas as pd
    g5 = pd.DataFrame([{"fund_id": "TXUE", "fund_ticker": "TXUE", "security_id": s, "security_key": s, "action": a,
                        "window_end": pd.Timestamp(d).date(), "est_notional_base": n} for s, a, d, n in TRADES])
    g6 = pd.DataFrame([{"fund_id": "TXUE", "window_end": pd.Timestamp(d).date(), "status": st, "reason": rs}
                       for d, st, rs in (("2026-01-15", None, None), ("2026-02-13", None, None), ("2026-03-13", None, None),
                                         ("2026-04-15", None, None), ("2026-05-15", "REFUSED", "flow_factor_out_of_band"))])
    g1 = pd.DataFrame([{"fund_id": "TXUE", "fund_ticker": "TXUE", "report_date": "2026-01-02", "security_id": s,
                        "security_name": s, "gics_sector": sec, "is_cash_line": False} for s, sec in SECTOR.items()])
    return g5, g6, g1


def run(v):
    c.setup_path()
    from lib import trading_calendar as tc
    from rivalfunds import gold_buying_trend as bt

    g5, g6, g1 = fixtures()
    out = bt.build(g5, g6, g1, DAY, ENTRIES)
    print("columns:", list(out.columns))
    sec = out[out.axis == "security"]

    def r(bucket):
        x = sec[sec.bucket == bucket]
        return x.iloc[0].to_dict() if len(x) == 1 else None

    s1, s2, s3, s4 = (r(k) for k in ("S1", "S2", "S3", "S4"))
    for k, x in (("S1", s1), ("S2", s2), ("S3", s3)):
        print(k, x and (x["lean"], x["rank"], x["net_notional_base"], x["reading"], x["trend_mark"]))
    v.check(s2 is not None and s1 is not None and s3 is not None and s4 is None
            and (s2["lean"], s2["rank"]) == ("into", 1) and (s1["lean"], s1["rank"]) == ("into", 2) and (s3["lean"], s3["rank"]) == ("away", 1),
            "into: S2 rank 1, S1 rank 2; away: S3 rank 1; the refused window's S4 has no row")
    v.check(s1 is not None and s2 is not None and s3 is not None and (s1["reading"], s2["reading"], s3["reading"]) == ("tilt", "bet", "bet")
            and s1["trend_mark"] == "+ + + 0 0 0 0 0 0 0" and all(ord(ch) < 128 for t in out["trend_mark"] for ch in str(t)),
            "readings S1 tilt, S2 bet, S3 bet; S1 marked '+ + + 0 0 0 0 0 0 0'; every mark ASCII")
    st = out[out.axis == "sector"]
    tech = st[st.bucket == "Information Technology"]
    en = st[st.bucket == "Energy"]
    print("sectors:", tech[["lean", "net_notional_base"]].values.tolist(), en[["lean", "net_notional_base"]].values.tolist(),
          "| refused:", sorted(set(out["n_refused_windows"])))
    v.check(len(tech) == 1 and tech.iloc[0]["lean"] == "into" and abs(tech.iloc[0]["net_notional_base"] - 800) < 1e-9
            and len(en) == 1 and en.iloc[0]["lean"] == "away" and abs(en.iloc[0]["net_notional_base"] + 300) < 1e-9
            and set(out["n_refused_windows"]) == {1},
            "sectors: IT into +800, Energy away -300; n_refused_windows 1")
    want = len(tc.trading_days_ytd(DAY))
    print("n_trading_days:", sorted(set(out["n_trading_days"])), "calendar YTD:", want)
    v.check(set(out["n_trading_days"]) == {want}, "control: n_trading_days equals the calendar's YTD trading days")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
