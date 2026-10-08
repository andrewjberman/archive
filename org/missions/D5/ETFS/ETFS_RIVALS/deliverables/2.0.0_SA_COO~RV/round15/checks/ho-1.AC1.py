"""RIV-ho-1 AC1 (PRD v0.19 C-HISTORY-OWED, FWD-24; issuer-written, 2.0.0_SA_COO~RV): THE HISTORY-OWED SET. A NEW module
`data/etfs/scripts/rivalfunds/history_owed.py` computes, from stored tables alone, every (security, trading day) of the last
`window_days` (default 365) that has no stored close:
  `history_owed.owed(s, day, window_days=365)` -> a pandas DataFrame, one row per owed unit, columns `security_id`,
  `security_bloomberg`, `date` (ISO string), `funds`; rows sorted by `date` descending, then `security_id`;
  `history_owed.summary(df)` -> {"securities", "units", "dates", "newest", "oldest"} (zeros and None for an empty frame).
A unit is owed when: the security is in the newest `security_universe` object at or before `day` and its `security_bloomberg` is
non-blank; `date` is a trading day (`lib.trading_calendar`) with `day - window_days <= date <= as_of(day)` (`as_of(day)` = the previous
trading day of `day`); the security's `last_seen` is on or after `day - window_days`; and `hc.g4_window` over the window returns no row for
(`security_id`, `date`) whose `px_close` is not null. READING OF THE CELL'S `first_seen` SENTENCE: "`first_seen - window_days <= date` is
NOT required" = `first_seen` is not a bound at all: a security whose `first_seen` is later than the window's early days is still owed those
early days (its whole window), and a security whose `last_seen` is inside the window is owed through `as_of(day)` even on days after its
`last_seen`. The set is defined by what the shared reader returns, not by what S3 holds: a close only in an UNTIMED object beside a
timed object of the same date (not read) leaves the unit owed. The function writes nothing; the module imports no vendor or network module.

Fixture (a `local:` sink; universe objects built with `gold_security_universe._bytes`; market objects with the producer's own schema,
`enrichment_bloomberg.MARKET_COLUMNS` / `_market_table`). `day` 2026-09-10, `window_days` 10 (lo 2026-08-31; as_of 2026-09-09; the
window holds the Labor Day holiday 2026-09-07 and the weekend 09-05/09-06): the trading days are 08-31, 09-01, 09-02, 09-03, 09-04, 09-08,
09-09 (7). The intended universe object is `date=2026-09-09` (the newest at or before `day`); an older one (`date=2026-09-01`, member
OLDONLY) and a newer-than-day one (`date=2026-09-11`, member NEWONLY) carry other members. Securities: NOCLOSE (no close anywhere),
PARTIAL (closes 09-02, 09-08), BLANKBB / NULLBB / WSBB (blank, null, whitespace Bloomberg key), STALE (last_seen 08-30, before lo),
EDGE (last_seen 08-31 = lo), INWIN (first_seen = last_seen = 09-03: owed the whole window), UNTONLY (close on 09-03 only in an untimed
object beside a timed one; timed closes on 09-01, 09-02, 09-04, 09-08, 09-09), NULLPX (a timed row with px_close null on 09-04; timed closes
on 09-01, 09-02, 09-03, 09-08, 09-09). 08-31 has no partition at all; every other trading day has one timed object (see `HELD`).

  - (a) NOCLOSE (Bloomberg key, no stored close) is owed on exactly the trading days of the window through as_of (count equals the trading
    calendar's 7; the weekend and the holiday are absent; the window's first day `lo` is included);
  - (b) PARTIAL (closes 09-02 and 09-08) is owed on exactly the other five trading days;
  - (c) BLANKBB, NULLBB, WSBB and STALE are never owed; EDGE (last_seen = lo) and INWIN (first_seen = last_seen = 09-03) are owed the whole
    window, including days after their last_seen and before their first_seen; the frame's `funds` is the universe's `funds`;
  - (d) the universe object used is the newest at or before `day`: OLDONLY and NEWONLY are never owed, the 09-09 members are; with the
    universe object dated exactly `day` it is used (a second small sink); and the default `window_days` (365) on a tiny universe owes
    exactly the calendar's trading days of [day - 365, as_of(day)] and equals the call with `window_days=365`;
  - (e) a close only in an UNTIMED object beside a timed one of the same date leaves the unit owed (UNTONLY on 09-03); a timed row with
    px_close null leaves it owed (NULLPX on 09-04); the same securities are not owed on their other (held) days;
  - (f) shape: a pandas DataFrame, columns exactly [security_id, security_bloomberg, date, funds], `date` an ISO string, sorted by date
    descending then security_id, no duplicate (security_id, date);
  - (g) `summary(df)` returns exactly the five keys with the right numbers (a hand-built frame and the fixture's), and zeros / None for an
    empty frame;
  - (h) the function writes nothing (the sink's file list, names and sizes, is identical before and after), the module source imports no
    vendor or network module (ast: no blpapi / blp* / bloomberg-named module, requests, urllib, urllib3, boto3, botocore, socket, http),
    and importing the module and calling `owed` adds no such module to `sys.modules`;
  - (i) CONTROL (PASSES at base): the fixture objects are on the sink (the 09-09 universe and the timed market objects, the untimed one);
    `gold_holding_contribution.g4_window` over [lo, as_of] returns the planted closes (PARTIAL 09-02 and 09-08, not the untimed UNTONLY
    09-03 close); `lib.trading_calendar` gives 7 trading days for the window and excludes 09-07; the 09-09 universe object reads back
    with its members.
Every build arm FAILS with a clear message when `rivalfunds.history_owed` or its `owed` / `summary` is missing.
FAIL at base 361b735308: (a), (b), (c), (d), (e), (f), (g), (h) FAIL (`rivalfunds.history_owed` does not exist: ImportError, reported as BUILD MISSING); (i) PASSES.
At base 361b735308: AC1 RESULT: FAIL 8: a, b, c, d, e, f, g, h (measured).
"""
import ast
import datetime as dt
import io
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY, WIN = "2026-09-10", 10
LO, ASOF = "2026-08-31", "2026-09-09"
TRADING = ["2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-08", "2026-09-09"]
COLS = ["security_id", "security_bloomberg", "date", "funds"]
SRC = "blp_client.reference_data"
NO, PA, IW, ED, ST = "NOCLOSE_US_Equity", "PARTIAL_US_Equity", "INWIN_US_Equity", "EDGE_US_Equity", "STALE_US_Equity"
UN, NP, BL, NL, WS = "UNTONLY_US_Equity", "NULLPX_US_Equity", "BLANKBB_US_Equity", "NULLBB_US_Equity", "WSBB_US_Equity"
OLD, NEW = "OLDONLY_US_Equity", "NEWONLY_US_Equity"
VENDOR = ("blpapi", "blp", "requests", "urllib", "urllib3", "boto3", "botocore", "socket", "http")


def bb(sid):
    return sid.replace("_", " ")


def urow(sid, bbk="same", first="2026-08-01", last="2026-09-08", funds="AAAA,BBBB"):
    return {"security_key": sid, "security_id": sid, "security_bloomberg": bb(sid) if bbk == "same" else bbk,
            "first_seen": dt.date.fromisoformat(first), "last_seen": dt.date.fromisoformat(last), "funds": funds, "n_report_dates": 3}


# the universe fixture: (rows of the intended 09-09 object, older 09-01 object, newer 09-11 object)
U_MAIN = [urow(NO, funds="AAAA,BBBB"), urow(PA, funds="CCCC"), urow(BL, bbk=""), urow(NL, bbk=None), urow(WS, bbk="   "),
          urow(ST, last="2026-08-30"), urow(ED, last="2026-08-31", funds="DDDD"), urow(IW, first="2026-09-03", last="2026-09-03", funds="EEEE"),
          urow(UN, funds="FFFF"), urow(NP, funds="GGGG")]
U_OLD = [urow(OLD, funds="OOOO")]
U_NEW = [urow(NEW, funds="NNNN")]
# closes held (per the shared reader): security -> the trading days with a timed, non-null close
HELD = {PA: {"2026-09-02", "2026-09-08"}}
# 08-31 has NO partition at all, so nothing is held there; 09-01 carries a timed object that holds UNTONLY / NULLPX closes
HELD[UN] = {"2026-09-01", "2026-09-02", "2026-09-04", "2026-09-08", "2026-09-09"}
HELD[NP] = {"2026-09-01", "2026-09-02", "2026-09-03", "2026-09-08", "2026-09-09"}


def mrow(eb, sec, date, px=None):
    r = {col: None for col in eb.MARKET_COLUMNS}
    r.update(security_id=sec, security_bloomberg=bb(sec), date=dt.date.fromisoformat(date), px_close=px, currency="USD", source=SRC,
             as_of=dt.date.fromisoformat(date), as_of_source="pull", producer_version=eb.GOLD_VERSION, input_manifest="{}",
             claim="MEASURED", produced_at=f"{date}T01:00:00Z")
    return r


def put_market(eb, s, date, name, rows):
    rev = name[len("market-"):-len(".parquet")]
    uri = eb.market_target_uri(date, rev)
    s.put(uri, eb._parquet_bytes(eb._market_table([dict(r, revision=rev) for r in rows])), "application/octet-stream")
    return uri


def put_universe(s, date, rows, rev="20260909T120000Z-aaaaaaaaaaaa"):
    import pandas as pd

    from rivalfunds import gold_security_universe as gsu
    from rivalfunds import homes
    cols = [f.name for f in gsu.SCHEMA][:11]
    uri = homes.address("rivalfunds", "etfs", "gold", gsu.TABLE, f"date={date}", f"universe-{rev}.parquet")
    s.put(uri, gsu._bytes(pd.DataFrame(rows, columns=cols)), "application/octet-stream")
    return uri


def new_sink(tag):
    from rivalfunds import sinks
    d = c.tmpdir(f"rv_ho1_{tag}_")
    return d, sinks.get_sink(f"local:{d}")


def build_fixture(tag, universe=True):
    """The main fixture on a fresh sink. Returns (dir, sink, {name: uri})."""
    from rivalfunds import enrichment_bloomberg as eb
    d, s = new_sink(tag)
    uris = {}
    if universe:
        uris["u_main"] = put_universe(s, "2026-09-09", U_MAIN)
        uris["u_old"] = put_universe(s, "2026-09-01", U_OLD, "20260901T120000Z-bbbbbbbbbbbb")
        uris["u_new"] = put_universe(s, "2026-09-11", U_NEW, "20260911T120000Z-cccccccccccc")
    for i, day in enumerate(TRADING[1:]):  # 08-31 has no partition
        rows = [mrow(eb, "FILLER_US_Equity", day, px=1.0)]
        for sec in (PA, UN, NP):
            if day in HELD[sec]:
                rows.append(mrow(eb, sec, day, px=10.0 + i))
        if day == "2026-09-04":
            rows.append(mrow(eb, NP, day, px=None))  # a timed row with a null close
        uris[f"t_{day}"] = put_market(eb, s, day, f"market-{day.replace('-', '')}T101500Z-aaaaaaaaaaaa.parquet", rows)
    # UNTONLY's 09-03 close sits only in an UNTIMED object beside the timed one (not read by the shared reader)
    uris["untimed_0903"] = put_market(eb, s, "2026-09-03", "market-20260903-53bc393958bd.parquet", [mrow(eb, UN, "2026-09-03", px=99.0)])
    return d, s, uris


def listing(d):
    out = []
    for root, _dirs, files in os.walk(d):
        for f in files:
            p = os.path.join(root, f)
            out.append((os.path.relpath(p, d).replace("\\", "/"), os.path.getsize(p)))
    return sorted(out)


def pairs(df, sec=None):
    return {(r["security_id"], str(r["date"])) for r in df.to_dict("records") if sec is None or r["security_id"] == sec}


def import_ho():
    """(module or None, message). A missing module / function is a clear failure message, never a crash."""
    try:
        from rivalfunds import history_owed as ho
    except Exception as e:  # noqa: BLE001
        return None, f"rivalfunds.history_owed cannot be imported ({type(e).__name__}: {e})"
    miss = [n for n in ("owed", "summary") if not callable(getattr(ho, n, None))]
    if miss:
        return None, f"rivalfunds.history_owed has no callable {', '.join(miss)}"
    return ho, ""


def guard(v, label, desc, fn):
    try:
        ok = fn()
    except Exception as e:  # noqa: BLE001
        print(f"  ({label}) raised {type(e).__name__}: {e}")
        ok = False
    v.check(bool(ok), f"({label}) {desc}")


def run(v):
    c.setup_path()
    c.offline_guards()
    import pandas as pd
    import pyarrow.parquet as pq

    from lib import trading_calendar as tc
    S0 = set(sys.modules)
    ho, why = import_ho()
    S1 = set(sys.modules)
    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import homes

    def need():
        if ho is None:
            print(f"  BUILD MISSING: {why}")
            return False
        return True

    cache = {}

    def main_frame():
        if "df" not in cache:
            _d, s, _u = build_fixture("main")
            cache["df"] = ho.owed(s, DAY, window_days=WIN)
        return cache["df"]

    def secs_owed(df, sid):
        return sorted(x[1] for x in pairs(df, sid))

    # ---- (a) ---------------------------------------------------------------------------------------------------------
    def arm_a():
        if not need():
            return False
        got = secs_owed(main_frame(), NO)
        print(f"  {NO} owed {got} | trading calendar {TRADING}")
        return got == TRADING and len(got) == len(tc.trading_days_between(LO, ASOF)) and "2026-09-07" not in got \
            and "2026-09-05" not in got and "2026-09-10" not in got and LO in got

    guard(v, "a", "a Bloomberg-keyed security with no stored close is owed on every trading day of the window through as_of(day) (7; the weekend "
                  "and Labor Day absent; lo included; `day` itself absent)", arm_a)

    # ---- (b) ---------------------------------------------------------------------------------------------------------
    def arm_b():
        if not need():
            return False
        got = secs_owed(main_frame(), PA)
        want = sorted(set(TRADING) - HELD[PA])
        print(f"  {PA} owed {got} | want {want}")
        return got == want and len(got) == 5

    guard(v, "b", "a security with stored closes on 09-02 and 09-08 is owed exactly on the other five trading days", arm_b)

    # ---- (c) ---------------------------------------------------------------------------------------------------------
    def arm_c():
        if not need():
            return False
        df = main_frame()
        never = {x: secs_owed(df, x) for x in (BL, NL, WS, ST)}
        edge, inwin = secs_owed(df, ED), secs_owed(df, IW)
        funds = {r["security_id"]: r["funds"] for r in df.to_dict("records")}
        print(f"  never owed {never} | EDGE {edge} | INWIN {inwin} | funds {({k: funds.get(k) for k in (NO, PA, ED, IW)})}")
        return (all(x == [] for x in never.values()) and edge == TRADING and inwin == TRADING
                and funds.get(NO) == "AAAA,BBBB" and funds.get(PA) == "CCCC" and funds.get(ED) == "DDDD" and funds.get(IW) == "EEEE")

    guard(v, "c", "blank / null / whitespace Bloomberg keys and a last_seen before lo are never owed; last_seen = lo and first_seen = last_seen "
                  "= 09-03 are owed the whole window (days after last_seen, days before first_seen); `funds` is the universe's", arm_c)

    # ---- (d) ---------------------------------------------------------------------------------------------------------
    def arm_d():
        if not need():
            return False
        df = main_frame()
        ids = {r["security_id"] for r in df.to_dict("records")}
        print(f"  securities owed {sorted(ids)}")
        ok = OLD not in ids and NEW not in ids and NO in ids
        # the universe object dated exactly `day` is used (at or before)
        _dd, s2 = new_sink("d_at")
        put_universe(s2, "2026-09-01", U_OLD, "20260901T120000Z-bbbbbbbbbbbb")
        put_universe(s2, DAY, [urow(NEW, funds="TTTT")], "20260910T120000Z-dddddddddddd")
        got2 = ho.owed(s2, DAY, window_days=WIN)
        ids2 = {r["security_id"] for r in got2.to_dict("records")}
        print(f"  universe dated exactly day -> securities owed {sorted(ids2)}")
        ok = ok and ids2 == {NEW} and secs_owed(got2, NEW) == TRADING
        # the default window (365) on a tiny universe
        _d3, s3 = new_sink("d_365")
        put_universe(s3, "2026-09-09", [urow(NO, first="2025-01-01", last="2026-09-08")])
        full = ho.owed(s3, DAY)
        want = [x.isoformat() for x in tc.trading_days_between(dt.date.fromisoformat(DAY) - dt.timedelta(days=365), ASOF)]
        got3 = sorted(x[1] for x in pairs(full))
        same = ho.owed(s3, DAY, 365)
        print(f"  default window: {len(got3)} units, calendar {len(want)} trading days ({want[0]}..{want[-1]})")
        return ok and got3 == sorted(want) and len(want) > 200 and pairs(same) == pairs(full)

    guard(v, "d", "the universe object is the newest at or before `day` (older and newer-than-day members never owed; one dated exactly `day` "
                  "is used); the default window_days (365) owes exactly the calendar's trading days of [day-365, as_of(day)]", arm_d)

    # ---- (e) ---------------------------------------------------------------------------------------------------------
    def arm_e():
        if not need():
            return False
        df = main_frame()
        un, np_ = secs_owed(df, UN), secs_owed(df, NP)
        want_un, want_np = sorted(set(TRADING) - HELD[UN]), sorted(set(TRADING) - HELD[NP])
        print(f"  {UN} owed {un} (want {want_un}) | {NP} owed {np_} (want {want_np})")
        return un == want_un and np_ == want_np and "2026-09-03" in un and "2026-09-04" in np_

    guard(v, "e", "a close only in an untimed object beside a timed one (UNTONLY, 09-03) leaves the unit owed; a timed row with px_close null "
                  "(NULLPX, 09-04) leaves it owed; their other held days are not owed", arm_e)

    # ---- (f) ---------------------------------------------------------------------------------------------------------
    def arm_f():
        if not need():
            return False
        df = main_frame()
        if not isinstance(df, pd.DataFrame):
            print(f"  not a DataFrame: {type(df).__name__}")
            return False
        recs = df.to_dict("records")
        keys = [(r["security_id"], r["date"]) for r in recs]
        want_order = sorted(sorted(keys, key=lambda k: k[0]), key=lambda k: k[1], reverse=True)  # date desc, then security_id asc (stable)
        str_dates = all(isinstance(r["date"], str) and len(r["date"]) == 10 and r["date"][4] == "-" for r in recs)
        print(f"  columns {list(df.columns)} | rows {len(df)} | dup keys {len(keys) - len(set(keys))} | "
              f"ISO-string dates {str_dates}")
        return (list(df.columns) == COLS and str_dates and keys == want_order and len(keys) == len(set(keys)))

    guard(v, "f", "a DataFrame with columns [security_id, security_bloomberg, date, funds], ISO-string dates, sorted by date descending then "
                  "security_id, no duplicate (security_id, date)", arm_f)

    # ---- (g) ---------------------------------------------------------------------------------------------------------
    def arm_g():
        if not need():
            return False
        keys5 = {"securities", "units", "dates", "newest", "oldest"}
        hand = pd.DataFrame({"security_id": ["A", "A", "B"], "security_bloomberg": ["A", "A", "B"],
                             "date": ["2026-09-09", "2026-09-08", "2026-09-09"], "funds": ["X", "X", "Y"]})
        s_hand = ho.summary(hand)
        df = main_frame()
        s_main = ho.summary(df)
        s_empty = ho.summary(pd.DataFrame(columns=COLS))
        print(f"  hand {s_hand} | fixture {s_main} | empty {s_empty}")
        want_main = {"securities": len({r["security_id"] for r in df.to_dict("records")}), "units": len(df),
                     "dates": len({r["date"] for r in df.to_dict("records")}), "newest": max(r["date"] for r in df.to_dict("records")), "oldest": min(r["date"] for r in df.to_dict("records"))}
        ok_hand = s_hand == {"securities": 2, "units": 3, "dates": 2, "newest": "2026-09-09", "oldest": "2026-09-08"}
        ok_empty = isinstance(s_empty, dict) and set(s_empty) == keys5 and s_empty["securities"] == 0 and s_empty["units"] == 0 \
            and s_empty["dates"] == 0 and s_empty["newest"] is None and s_empty["oldest"] is None
        return isinstance(s_hand, dict) and set(s_hand) == keys5 and ok_hand and s_main == want_main and ok_empty

    guard(v, "g", "summary(df) returns exactly {securities, units, dates, newest, oldest} with the right numbers (hand frame and fixture) and "
                  "zeros / None for an empty frame", arm_g)

    # ---- (h) ---------------------------------------------------------------------------------------------------------
    def arm_h():
        if not need():
            return False
        d, s, _u = build_fixture("h")
        before = listing(d)
        S2 = set(sys.modules)
        ho.owed(s, DAY, window_days=WIN)
        S3 = set(sys.modules)
        after = listing(d)
        added = sorted(m for m in (S1 - S0) | (S3 - S2) if m.split(".")[0].lower() in VENDOR or "bloomberg" in m.lower()
                       or m.lower().startswith("blp"))
        src = pathlib.Path(ho.__file__).read_text(encoding="utf-8")
        bad = []
        for n in ast.walk(ast.parse(src)):
            names = [a.name for a in n.names] if isinstance(n, ast.Import) else \
                ([(n.module or "")] + [(n.module or "") + "." + a.name for a in n.names]) if isinstance(n, ast.ImportFrom) else []
            for nm in names:
                top = nm.split(".")[0].lower()
                if top in VENDOR or "bloomberg" in nm.lower() or "blp" in nm.lower():
                    bad.append(nm)
        print(f"  sink files before {len(before)} / after {len(after)} identical {before == after} | vendor modules added {added} | "
              f"vendor imports in source {sorted(set(bad))}")
        return before == after and len(before) > 0 and not added and not bad

    guard(v, "h", "the function writes nothing (sink file list identical), the module source imports no vendor / network / bloomberg module, "
                  "and importing it and calling owed adds none to sys.modules", arm_h)

    # ---- (i) control -------------------------------------------------------------------------------------------------
    def arm_i():
        d, s, uris = build_fixture("i")
        listed = [u for u in s.list(hc.g4_prefix()) if u.endswith(".parquet")]
        ulisted = [u for u in s.list(homes.address("rivalfunds", "etfs", "gold", "security_universe", "date=")) if u.endswith(".parquet")]
        g, _objs = hc.g4_window(s, LO, ASOF, columns=["security_id", "date", "px_close"])
        px = {(r["security_id"], str(r["date"])[:10]): r["px_close"] for r in g.to_dict("records")}
        days = [x.isoformat() for x in tc.trading_days_between(LO, ASOF)]
        mem = {r["security_id"] for r in pq.read_table(io.BytesIO(s.get(uris["u_main"]))).to_pandas().to_dict("records")}
        print(f"  market objects {len(listed)} (6 timed days + 1 untimed = 7) | universe objects {len(ulisted)} (3) | calendar days {days}")
        print(f"  g4_window: PARTIAL 09-02 {px.get((PA, '2026-09-02'))}, 09-08 {px.get((PA, '2026-09-08'))}; UNTONLY 09-03 {px.get((UN, '2026-09-03'))}")
        return (len(listed) == 7 and len(ulisted) == 3 and days == TRADING and "2026-09-07" not in days
                and px.get((PA, "2026-09-02")) is not None and px.get((PA, "2026-09-08")) is not None
                and (px.get((UN, "2026-09-03")) is None or px.get((UN, "2026-09-03")) != px.get((UN, "2026-09-03"))
                     or px.get((UN, "2026-09-03")) != 99.0)
                and mem == {r["security_id"] for r in U_MAIN})

    guard(v, "i", "control: the fixture objects are on the sink (7 market, 3 universe); g4_window returns the planted timed closes and not the "
                  "untimed 99.0; the trading calendar gives the 7 days and excludes 09-07; the 09-09 universe object reads back with its "
                  "members", arm_i)


v = c.Verdict("AC1")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- a dead fixture is a failed check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = [m.split(")")[0].lstrip("(") for m in v.fails]
print("AC1 RESULT: PASS 0 failures" if not v.fails else f"AC1 RESULT: FAIL {len(v.fails)}: {', '.join(labels)}")
sys.exit(0 if not v.fails else 1)
