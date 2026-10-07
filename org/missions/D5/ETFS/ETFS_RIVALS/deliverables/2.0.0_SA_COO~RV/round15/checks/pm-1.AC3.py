"""RIV-pm-1 AC3 (PRD v0.18 FWD-22, C-TRADE-MARKER): the chart object's markers are honest -- no marker for a trade of zero
dollars, and the markers run through the PAGE day.

Interface (prescribed, from the cell):
  - `trade_markers.markers(trades, fund_mv_by_date)` skips a trade whose `est_notional` is zero (0.0 or -0.0) as it already
    skips a null one;
  - in `publish_page` the G5 trades handed to `trade_markers.markers` include a trade whose `window_end` equals the page
    day (today the read stops at the as-of day, the previous trading day, so such a trade is in gold buying_trend's strip and
    not in the chart object). Prices (`points`, `ranges`) and `asof` still end at the as-of day.

Fixture: (a) rows in the style of tests/test_r15tm1_trade_markers.py -- three trades in one window ending 2026-09-02:
an add of 500.0, a trim of 0.0 and a trim of -0.0. (b)-(e) co-1.AC1's own fixture (`fixture()` and `publish()` of
round15/checks/co-1.AC1.py, loaded without its verdict): page day 2026-09-30, as-of day 2026-09-29, funds TXUE and BASG.
That fixture's reports are 2026-09-25, 09-28 and 09-29, so gold_trade_schedule writes G5 for windows ending 09-28 and 09-29
and NONE ending on the page day. This check therefore plants ONE G5 object under `date=2026-09-30` BEFORE publish: TXUE's own
S05 row of the 09-29 object (same schema, same file name) with action `add`, est_notional 1,234.5, window 2026-09-29 ..
2026-09-30.
  - (a) markers of the three trades is ONE marker: side buy, usd 500.0, n_trades 1 (no sell marker of zero dollars);
  - (b) TXUE's chart object lists, for S05, a buy marker whose `end` is "2026-09-30" and whose usd is 1,234.5;
  - (c) TXUE's and BASG's objects still carry `asof` "2026-09-29", ranges counted from it, no point dated after it, and
    S05 still carries its sell marker ending 2026-09-29;
  - (d) co-1.AC1, co-1.AC2 and tl-1.AC1 still end `PASS 0 failures` (each run as its own process from the worktree root);
  - (e) control: the G5 in the sink holds the planted page-day trade (TXUE, S05, add, 1,234.5, ending 2026-09-30), the page
    publishes on the fixture (OK or PARTIAL), S05 is in TXUE's object with its 09-29 sell, and `markers` keeps the 500.0 buy
    and skips a null est_notional. (Measured and printed, not asserted, because the build changes them: today the object has
    no marker ending on the page day, and `markers` returns a zero-dollar sell.)
Not graded here: the marker's `bps` on the page day (the fund's G1 total for a day after the as-of day may not be read), and
what the script draws for a marker dated after `asof`.
FAIL at base b1a4837abe: (a), (b) FAIL (a sell marker of usd 0.0 with n_trades 2; no marker ending 2026-09-30); (c), (d), (e) PASS."""
import datetime as dt
import io
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

DAY, ASOF, PREV = "2026-09-30", "2026-09-29", "2026-09-29"
RANGES = {"R30": "2026-08-30", "R90": "2026-07-01", "R365": "2025-09-29"}
FUNDS = ("TXUE", "BASG")
FUND, SEC, USD = "TXUE", "S05", 1234.5
EARLIER = ("co-1.AC1", "co-1.AC2", "tl-1.AC1")


def load_co1():
    """co-1.AC1's module with its fixture and publish only (its own verdict never runs)."""
    p = HERE / "co-1.AC1.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]
    mod = type(sys)("co1_ac1_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def _row(action, usd, ws="2026-09-01", we="2026-09-02", n=1):
    return {"action": action, "est_notional": usd, "window_start": dt.date.fromisoformat(ws), "window_end": dt.date.fromisoformat(we),
            "window_trading_days": n}


def _markers(tm, rows, mv):
    try:
        out = tm.markers(rows, mv)
        return [m for m in out if isinstance(m, dict)], None
    except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
        return [], f"{type(e).__name__}: {e}"


def plant(s):
    """Write ONE G5 object for the page day: TXUE's S05 row of the 09-29 object, turned into an add ending on the page day.
    Returns (uri | None, error words | None)."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import homes

    try:
        src = next(u for u in s.list(homes.trade_schedule(PREV)) if u.endswith(".parquet"))
        table = pq.read_table(io.BytesIO(s.get(src)))
        df = table.to_pandas()
        row = df[(df["fund_ticker"] == FUND) & (df["security_key"] == SEC)].head(1).copy()
        if len(row) != 1:
            return None, f"the fixture's G5 for {PREV} holds no {FUND} {SEC} row"
        row["action"], row["est_notional"], row["est_notional_base"] = "add", USD, USD
        for col, val in (("date", DAY), ("window_start", PREV), ("window_end", DAY)):
            row[col] = [dt.date.fromisoformat(val)]
        buf = io.BytesIO()
        pq.write_table(pa.Table.from_pandas(row, preserve_index=False, schema=table.schema), buf)
        uri = src.replace(f"date={PREV}", f"date={DAY}")
        if uri == src:
            return None, f"could not derive the page-day address from {src}"
        s.put(uri, buf.getvalue())
        return uri, None
    except Exception as e:  # noqa: BLE001 -- a fixture that cannot be planted fails the control arm, not the process
        return None, f"{type(e).__name__}: {e}"


def g5_page_day(s):
    """[(fund, security, action, est_notional, window_end)] of every G5 row in the sink whose window ends on the page day."""
    import pyarrow.parquet as pq

    from rivalfunds import homes

    out = []
    for u in s.list(homes.trade_schedule("")):
        if not u.endswith(".parquet"):
            continue
        df = pq.read_table(io.BytesIO(s.get(u))).to_pandas()
        out += [(str(x.fund_ticker), str(x.security_key), str(x.action), round(float(x.est_notional), 2), str(x.window_end)[:10])
                for x in df.itertuples() if str(x.window_end)[:10] == DAY]
    return out


def _json(s, uri):
    try:
        return json.loads(s.get(uri).decode("utf-8")) if s.exists(uri) else None
    except Exception as e:  # noqa: BLE001 -- an unreadable object is a failed arm, not a crash
        print("unreadable", uri, type(e).__name__, e)
        return None


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import homes
    from rivalfunds import trade_markers as tm

    mv = {dt.date(2026, 9, 2): 1_000_000.0}
    three, e3 = _markers(tm, [_row("add", 500.0), _row("trim", 0.0), _row("trim", -0.0)], mv)
    got3 = [(m.get("side"), m.get("usd"), m.get("n_trades")) for m in three]
    print("markers(add 500.0, trim 0.0, trim -0.0) ->", e3 or got3)
    v.check(got3 == [("buy", 500.0, 1)], "(a) a trade of zero dollars (0.0 or -0.0) makes no marker: only the 500.0 buy comes back")

    co1 = load_co1()
    spec, s = co1.fixture()
    made = g5_page_day(s)
    uri, perr = plant(s)
    held = g5_page_day(s)
    print("fixture G5 rows ending on the page day before the plant:", made, "| planted:", perr or uri.rsplit("/", 2)[-2])
    print("G5 rows ending on the page day in the sink:", held)
    try:
        r, _out = co1.publish(spec)
    except Exception as e:  # noqa: BLE001 -- a publish that raises on the page-day G5 is a failed arm, not a crash
        r = {"status": f"<error {type(e).__name__}: {e}>"}
    objs = {f: _json(s, homes.page(DAY, f"charts/{f}.json")) for f in FUNDS}
    objs = {f: (o if isinstance(o, dict) else {}) for f, o in objs.items()}
    secs = {f: (objs[f].get("securities") if isinstance(objs[f].get("securities"), dict) else {}) for f in FUNDS}
    marks = [m for m in (secs[FUND].get(SEC) or {}).get("markers") or [] if isinstance(m, dict)]
    print("publish:", r.get("status"), f"| {FUND} {SEC} markers:", [(m.get("side"), m.get("start"), m.get("end"), m.get("usd"), m.get("bps"))
                                                                 for m in marks])
    on_day = [m for m in marks if str(m.get("end"))[:10] == DAY]
    v.check(len(on_day) == 1 and on_day[0].get("side") == "buy" and isinstance(on_day[0].get("usd"), (int, float))
            and abs(on_day[0]["usd"] - USD) < 0.01,
            f"(b) {FUND}'s chart object lists for {SEC} the buy marker of 1,234.5 whose end is the page day {DAY}")

    last = {f: max((str(p[0]) for x in secs[f].values() if isinstance(x, dict) for p in x.get("points") or []), default=None)
            for f in FUNDS}
    prev_sell = [m for m in marks if m.get("side") == "sell" and str(m.get("end"))[:10] == PREV]
    print("asof:", {f: objs[f].get("asof") for f in FUNDS}, "| ranges:", {f: objs[f].get("ranges") for f in FUNDS},
          "| last point date:", last, f"| {SEC} sells ending {PREV}:", len(prev_sell))
    v.check(all(objs[f].get("asof") == ASOF and objs[f].get("ranges") == RANGES and last[f] == ASOF for f in FUNDS)
            and len(prev_sell) == 1,
            "(c) both objects keep asof 2026-09-29, ranges counted from it and no point after it, and S05 keeps its 09-29 sell")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1500)
        res = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = res[-1].strip() if res else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    v.check(all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(d) co-1.AC1, co-1.AC2 and tl-1.AC1 still end PASS 0 failures")

    kept, ek = _markers(tm, [_row("add", 500.0), _row("trim", None), _row("trim", float("nan"))], mv)
    zero_sells = [m for m in three if m.get("side") == "sell"]
    print("control: markers(add 500.0, trim None, trim nan) ->", ek or [(m.get("side"), m.get("usd"), m.get("n_trades")) for m in kept])
    print("  base readings (printed, not asserted): zero-dollar sell markers returned today:",
          [(m.get("usd"), m.get("n_trades")) for m in zero_sells], "| markers ending on the page day in the object today:", len(on_day))
    v.check(made == [] and perr is None and held == [(FUND, SEC, "add", USD, DAY)] and r.get("status") in ("OK", "PARTIAL")
            and SEC in secs[FUND] and len(prev_sell) == 1
            and [(m.get("side"), m.get("usd"), m.get("n_trades")) for m in kept] == [("buy", 500.0, 1)],
            "(e) control: the sink's G5 holds the one planted page-day trade, the page publishes, S05 is in TXUE's object with "
            "its 09-29 sell, and markers keeps the 500.0 buy and skips a null est_notional")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
