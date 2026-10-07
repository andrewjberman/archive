"""RIV-pl-1 AC1 (PRD v0.18 FWD-22, FWD-23; 3.0.0_SA_CVO~RV ADJUDICATION_v20 row ETFS_RIVALS-Z-C-S60): the month strip shows
every month of its window, and the dialog's trade list is headed by the window it covers.

Interface (prescribed, from the cell):
  - `render._month_chart(mark, end)` draws EVERY token of the mark, at most 13. When the first and the last cell are the
    same calendar month (a 13-token mark: the 365-day window's first and last month), those two cells carry the month and a
    two-digit year, `data-m="Oct 25"` and `data-m="Oct 26"`; every other cell carries the bare month as before. A mark of 12
    tokens or fewer is drawn exactly as round 19 drew it. `render._month_words(mark, end)` names the same months the same way.
  - `render._trade_list(trades)` puts, immediately before the `[data-chart-trades]` element, the caption element
    `<p data-chart-trades-head>` holding exactly HEAD, whether or not the page context holds a trade.
  - (a) the 13-token mark with end 2026-10-06 draws 13 cells: "Oct 25", Nov, Dec, Jan .. Sep, "Oct 26", with the classes of
    all 13 tokens;
  - (b) a 12-token mark with end 2026-10-06 draws 12 cells labelled Nov .. Oct with no year;
  - (c) `_month_words` on a 13-token mark whose first and last tokens are trades names "Oct 25" first and "Oct 26" last;
  - (d) `_trade_list([])` and `_trade_list([one trade])` each hold the caption element with HEAD, before the trades element;
  - (e) ml-1.AC1, tl-1.AC1, md-1.AC1, md-1.AC2 and pd-2.AC1 still end `PASS 0 failures` (each run as its own process);
  - (f) control: a 2-token mark draws Sep and Oct, and with no trade the trades element still holds the static sentence.
FAIL at base 6bee8e3a91 or later: (a), (c), (d) FAIL (12 cells, no year; no caption); (b), (e), (f) PASS."""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
END = "2026-10-06"
M13 = "+ - 0 . + - 0 . + - 0 . +"
M12 = "- 0 . + - 0 . + - 0 . +"
CLS = {"+": "u", "-": "d", "0": "f", ".": "n"}
HEAD = "Trades in the last 365 days"
STATIC = "The fund's trades over the last 365 days load with the chart."
EARLIER = ("ml-1.AC1", "tl-1.AC1", "md-1.AC1", "md-1.AC2", "pd-2.AC1")
ONE = {"action": "entry", "est_notional": 500.0, "window_start": "2026-10-01", "window_end": "2026-10-01", "window_trading_days": 1}


def cells(html: str):
    """[(class letter, label)] per cell; the label is the data-m value, quoted or not."""
    out = []
    for tag in re.findall(r"<i\b[^>]*>", html or ""):
        k = re.search(r'\bclass="?([a-z])"?', tag)
        m = re.search(r'\bdata-m=(?:"([^"]*)"|([A-Za-z]{3})\b)', tag)
        out.append((k.group(1) if k else None, (m.group(1) or m.group(2)) if m else None))
    return out


def call(fn, *a):
    try:
        return fn(*a), None
    except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
        return None, f"{type(e).__name__}: {e}"


def head_before_trades(html: str) -> bool:
    m = re.search(r"<p\b[^>]*\bdata-chart-trades-head\b[^>]*>([^<]*)</p>\s*<(?:p|ul)\b[^>]*\bdata-chart-trades\b", html or "")
    return bool(m) and m.group(1).strip() == HEAD


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    h13, e13 = call(render._month_chart, M13, END)
    got13 = cells(h13 or "")
    labels13 = ["Oct 25"] + MON[10:] + MON[:9] + ["Oct 26"]
    print("13 tokens ->", e13 or got13)
    v.check(got13 == [(CLS[t], lab) for t, lab in zip(M13.split(), labels13)],
            "(a) a 13-token mark draws 13 cells, the two Octobers carrying their year, with the classes of all 13 tokens")

    h12, e12 = call(render._month_chart, M12, END)
    print("12 tokens ->", e12 or cells(h12 or ""))
    v.check(cells(h12 or "") == [(CLS[t], lab) for t, lab in zip(M12.split(), MON[10:] + MON[:10])],
            "(b) a 12-token mark draws Nov .. Oct with no year, as round 19 drew it")

    w13, ew = call(render._month_words, M13, END)
    print("13-token words:", ew or repr(w13))
    v.check(isinstance(w13, str) and w13.startswith("Oct 25 ") and "Oct 26 " in w13 and w13.rfind("Oct 26 ") > w13.find("Oct 25 "),
            "(c) the hover words name 'Oct 25' first and 'Oct 26' last on a 13-token mark")

    e0, _ = call(render._trade_list, [])
    e1, _ = call(render._trade_list, [ONE])
    print("_trade_list([]):", (e0 or "")[:170])
    print("_trade_list([one]):", (e1 or "")[:170])
    v.check(head_before_trades(e0 or "") and head_before_trades(e1 or ""),
            "(d) the caption element holding 'Trades in the last 365 days' sits before the trades element, with or without a context trade")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1700)
        last = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = last[-1].strip() if last else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    v.check(all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(e) ml-1.AC1, tl-1.AC1, md-1.AC1, md-1.AC2 and pd-2.AC1 still end PASS 0 failures")

    h2, _ = call(render._month_chart, "- +", END)
    print("2 tokens ->", cells(h2 or ""), "| static sentence in the empty list:", STATIC in (e0 or ""))
    v.check(cells(h2 or "") == [("d", "Sep"), ("u", "Oct")] and STATIC in (e0 or "") and "data-chart-trades" in (e0 or ""),
            "(f) control: a 2-token mark draws Sep and Oct, and with no trade the trades element holds the static sentence")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
