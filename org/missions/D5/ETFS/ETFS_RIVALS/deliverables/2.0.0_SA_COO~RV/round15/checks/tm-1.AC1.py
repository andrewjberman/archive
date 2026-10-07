"""RIV-tm-1 AC1 (PRD v0.18 FWD-22, C-TRADE-MARKER; ROUND15_CELLS_DRAFT.md rev 1.5): a fund's trades in a security as sized markers.

Measured (cell text): `trade_schedule` (G5) carries `action`, `window_start`, `window_end`, `window_trading_days`, `est_notional`;
no share-of-fund column for the trade itself. At the base there is no `rivalfunds/trade_markers.py`. G5 carries NO column that
marks a refused window: `gold_trade_schedule._pair_rows` returns no trade rows for one (the REFUSED status and reason are on
the G6 row), so in G5 a refused window IS an empty row set -- that is what arm (f) passes.

Interface (prescribed, verbatim from the cell): new `rivalfunds/trade_markers.py`. `markers(g5_rows, fund_mv_by_date: {date:
float}) -> [{"side", "start", "end", "span", "usd", "bps", "r", "n_trades"}]` per (fund, security): `side` = `buy` for entry /
add, `sell` for trim / exit; `usd` = abs(`est_notional`); `bps` = `usd / fund_mv_by_date[window_end] * 10000` (the fund's total
reported market value on the window end; absent -> `bps` None and `r` = R_MIN); `r` = the marker radius: `R_MIN` (3.0) at 20 bps
or less, `R_MAX` (12.0) at 500 bps or more, linear in bps between; `span` = `window_trading_days > 1`; trades of one side sharing
one window are ONE marker with `n_trades` counted and `usd` / `bps` summed. A REFUSED window yields no marker. `words(marker) ->
str` reads "Bought" / "Sold", the date or "between <start> and <end>", the dollar value, the basis points of the fund, and the
count.

Fixture: G5 row dicts (gold_trade_schedule.COLUMNS; dates as datetime.date, as a G5 parquet reads) of fund TXUE in AAA_US_Equity;
the fund's market value is 1,000,000.00 on every window end but 2026-09-16 (absent):
  W1 09-01..09-02 (1 trading day)  entry +1,000      -> buy,  10 bps,   r 3.0 (below the floor)
  W2 09-02..09-03 (1)              add   +2,000      -> buy,  20 bps,   r 3.0 (at the floor)
  W3 09-03..09-04 (1)              trim  -26,000     -> sell, 260 bps,  r 7.5 (the linear midpoint)
  W4 09-04..09-11 (4)              exit  -50,000     -> sell, 500 bps,  r 12.0 (at the ceiling), span
  W5 09-11..09-14 (1)              add   +100,000    -> buy,  1000 bps, r 12.0 (above the ceiling)
  W6 09-14..09-15 (1)              entry +3,000, add +5,000, trim -1,000 -> ONE buy (2 trades, 8,000, 80 bps, r 4.125) + ONE sell
  W7 09-15..09-16 (1)              add   +4,000, no fund value on 09-16 -> buy, bps None, r 3.0
  - (a) `trade_markers.markers` returns 8 markers, each with exactly the eight prescribed keys; entry / add read buy, trim /
    exit read sell (per window end);
  - (b) usd = abs(est_notional) and bps = usd / fund value * 10000 (10, 20, 260, 500, 1000 bps);
  - (c) the radius: R_MIN 3.0 and R_MAX 12.0 are the module's constants; <= 20 bps -> 3.0, >= 500 bps -> 12.0, 260 bps -> 7.5;
  - (d) a one-trading-day window is span False; the four-day window is span True and keeps start 09-04 and end 09-11;
  - (e) two buys sharing W6 are ONE marker (n_trades 2, usd 8,000, bps 80, r 4.125) and the sell of W6 is its own marker (n_trades 1);
    a window end with no fund value is bps None at r 3.0 with its usd kept;
  - (f) a refused window (no G5 rows) yields no marker: markers([], ...) == [];
  - (g) `words()`: the W3 sell reads "Sold", "$", 26,000 and 260 with "bps" or "basis points" and no "between"; the W4 sell reads
    "between"; the merged W6 buy reads "Bought" and its count 2;
  - (h) control: the fixture rows use only G5's own columns, the four actions and the planted arithmetic hold (26,000 over
    1,000,000 is 260 bps; the midpoint of 3.0 and 12.0 over 20..500 bps is 7.5 at 260).
FAIL at base: (a)-(g) FAIL (no rivalfunds.trade_markers); (h) PASSES."""
import datetime as dt
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

FUND, SEC, MV = "TXUE", "AAA_US_Equity", 1_000_000.0
KEYS = {"side", "start", "end", "span", "usd", "bps", "r", "n_trades"}
# (window_start, window_end, window_trading_days, action, est_notional)
TRADES = [("2026-09-01", "2026-09-02", 1, "entry", 1000.0), ("2026-09-02", "2026-09-03", 1, "add", 2000.0),
          ("2026-09-03", "2026-09-04", 1, "trim", -26000.0), ("2026-09-04", "2026-09-11", 4, "exit", -50000.0),
          ("2026-09-11", "2026-09-14", 1, "add", 100000.0), ("2026-09-14", "2026-09-15", 1, "entry", 3000.0),
          ("2026-09-14", "2026-09-15", 1, "add", 5000.0), ("2026-09-14", "2026-09-15", 1, "trim", -1000.0),
          ("2026-09-15", "2026-09-16", 1, "add", 4000.0)]
# (window end, side) -> (start, span, usd, bps, r, n_trades)
EXPECT = {("2026-09-02", "buy"): ("2026-09-01", False, 1000.0, 10.0, 3.0, 1),
          ("2026-09-03", "buy"): ("2026-09-02", False, 2000.0, 20.0, 3.0, 1),
          ("2026-09-04", "sell"): ("2026-09-03", False, 26000.0, 260.0, 7.5, 1),
          ("2026-09-11", "sell"): ("2026-09-04", True, 50000.0, 500.0, 12.0, 1),
          ("2026-09-14", "buy"): ("2026-09-11", False, 100000.0, 1000.0, 12.0, 1),
          ("2026-09-15", "buy"): ("2026-09-14", False, 8000.0, 80.0, 4.125, 2),
          ("2026-09-15", "sell"): ("2026-09-14", False, 1000.0, 10.0, 3.0, 1),
          ("2026-09-16", "buy"): ("2026-09-15", False, 4000.0, None, 3.0, 1)}


def _d(v) -> str:
    return str(v)[:10]


def g5_rows(columns):
    out = []
    for ws, we, n, action, usd in TRADES:
        buy = action in ("entry", "add")
        out.append({**{col: None for col in columns}, "fund_ticker": FUND, "fund_id": FUND, "security_key": SEC, "security_id": SEC,
                    "security_key_kind": "bloomberg", "key_resolved": True, "action": action,
                    "date": dt.date.fromisoformat(we), "window_start": dt.date.fromisoformat(ws),
                    "window_end": dt.date.fromisoformat(we), "window_trading_days": n, "window_widened": n > 1,
                    "shares_before": 0.0 if action == "entry" else 1000.0, "shares_after": 0.0 if action == "exit" else 1100.0,
                    "est_price": 100.0, "est_notional": usd, "est_notional_base": usd, "income_funded": False,
                    "confidence": "HIGH" if buy else "MEDIUM", "dataset_revision": "20260917T000000Z-aaaaaaaaaaaa"})
    return out


def _near(a, b) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) < 1e-6


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import gold_trade_schedule as g5

    rows = g5_rows(g5.COLUMNS)
    mv = {dt.date.fromisoformat(we): MV for _, we, _, _, _ in TRADES if we != "2026-09-16"}
    try:
        from rivalfunds import trade_markers as tm
        why = None
    except ImportError as e:
        tm, why = None, f"{type(e).__name__}: {e}"
    print("rivalfunds.trade_markers:", "imported" if tm else f"ABSENT ({why})")

    got, none_got, err = [], None, None
    if tm is not None and hasattr(tm, "markers"):
        try:
            got = list(tm.markers([dict(r) for r in rows], dict(mv)) or [])
            none_got = tm.markers([], dict(mv))
        except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
            err = f"{type(e).__name__}: {e}"
    got = [m for m in got if isinstance(m, dict)]
    by = {(_d(m.get("end")), m.get("side")): m for m in got}
    print("markers() error:", err, "| markers returned:", len(got))
    for k in sorted(by):
        m = by[k]
        print("  ", k, "start", _d(m.get("start")), "span", m.get("span"), "usd", m.get("usd"), "bps", m.get("bps"), "r", m.get("r"),
              "n_trades", m.get("n_trades"))

    def field(k, name):
        return by.get(k, {}).get(name)

    v.check(len(got) == 8 and set(by) == set(EXPECT) and all(set(m) == KEYS for m in got),
            f"(a) 8 markers with exactly the eight prescribed keys; entry / add read buy, trim / exit read sell ({len(got)} markers)")
    priced = [k for k in EXPECT if EXPECT[k][3] is not None and k[0] != "2026-09-15"]
    v.check(bool(by) and all(_near(field(k, "usd"), EXPECT[k][2]) and _near(field(k, "bps"), EXPECT[k][3]) for k in priced),
            "(b) usd = abs(est_notional); bps = usd / the fund's value on the window end * 10000 (10, 20, 260, 500, 1000)")
    r_min, r_max = getattr(tm, "R_MIN", None), getattr(tm, "R_MAX", None)
    print("R_MIN:", r_min, "| R_MAX:", r_max)
    v.check(r_min == 3.0 and r_max == 12.0 and bool(by) and all(_near(field(k, "r"), EXPECT[k][4]) for k in priced),
            "(c) the radius is R_MIN 3.0 at 20 bps or less, R_MAX 12.0 at 500 bps or more, 7.5 at 260 bps")
    one_day = [k for k in EXPECT if k != ("2026-09-11", "sell")]
    v.check(bool(by) and all(field(k, "span") is False and _d(field(k, "start")) == EXPECT[k][0] for k in one_day)
            and field(("2026-09-11", "sell"), "span") is True and _d(field(("2026-09-11", "sell"), "start")) == "2026-09-04",
            "(d) a one-trading-day window is span False; the four-day window is span True with start 09-04 and end 09-11 kept")
    w6b, w6s, w7 = ("2026-09-15", "buy"), ("2026-09-15", "sell"), ("2026-09-16", "buy")
    v.check(bool(by) and field(w6b, "n_trades") == 2 and _near(field(w6b, "usd"), 8000.0) and _near(field(w6b, "bps"), 80.0)
            and _near(field(w6b, "r"), 4.125) and field(w6s, "n_trades") == 1 and _near(field(w6s, "usd"), 1000.0)
            and w7 in by and field(w7, "bps") is None and _near(field(w7, "r"), 3.0) and _near(field(w7, "usd"), 4000.0),
            "(e) two buys sharing one window are ONE marker (2 trades, 8,000, 80 bps, r 4.125), the window's sell is its own; "
            "no fund value on the window end -> bps None at r 3.0")
    print("markers([], ...) ->", none_got)
    v.check(tm is not None and err is None and none_got is not None and list(none_got) == [],
            "(f) a refused window (no G5 rows) yields no marker")

    words = {}
    if tm is not None and hasattr(tm, "words"):
        for k in (("2026-09-04", "sell"), ("2026-09-11", "sell"), w6b):
            try:
                words[k] = tm.words(by[k]) if k in by else None
            except Exception as e:  # noqa: BLE001
                words[k] = None
                print("words() error:", type(e).__name__, e)
    for k, w in words.items():
        print("  words", k, "->", repr(w))
    w3, w4, wb = (words.get(k) or "" for k in (("2026-09-04", "sell"), ("2026-09-11", "sell"), w6b))
    digits = re.sub(r"[,\s]", "", w3)
    v.check("Sold" in w3 and "$" in w3 and "26000" in digits and "260" in w3 and ("bps" in w3 or "basis points" in w3)
            and "between" not in w3 and "Sold" in w4 and "between" in w4 and "Bought" in wb and bool(re.search(r"(?<![\d,.$-])2(?![\d,.-])|two", wb)),
            "(g) words(): a one-day sell reads Sold, $26,000 and 260 bps with no 'between'; the span reads 'between'; the merged "
            "buy reads Bought and its count 2")

    actions = {r["action"] for r in rows}
    src = (c.ROOT / "data" / "etfs" / "scripts" / "rivalfunds" / "gold_trade_schedule.py").read_text(encoding="utf-8")
    named = {a: f'"{a}"' in src for a in sorted(actions)}
    mid_r = 3.0 + (260.0 - 20.0) / (500.0 - 20.0) * (12.0 - 3.0)
    print("fixture rows:", len(rows), "| actions:", sorted(actions), "| named in gold_trade_schedule.py:", named,
          "| 26,000 / 1,000,000 * 10000 =", 26000.0 / MV * 10000, "| r at 260 bps =", mid_r)
    v.check(len(rows) == 9 and all(set(r) == set(g5.COLUMNS) for r in rows) and actions == {"entry", "add", "trim", "exit"}
            and all(named.values()) and all(col in g5.COLUMNS for col in ("action", "window_start", "window_end",
                                                                         "window_trading_days", "est_notional"))
            and 26000.0 / MV * 10000 == 260.0 and mid_r == 7.5 and dt.date(2026, 9, 16) not in mv and len(mv) == 6,
            "(h) control: the fixture rows are G5's own columns and four actions, and the planted arithmetic holds")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
