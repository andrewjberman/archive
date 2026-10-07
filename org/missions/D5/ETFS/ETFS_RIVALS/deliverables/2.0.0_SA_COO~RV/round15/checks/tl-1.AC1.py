"""RIV-tl-1 AC1 (PRD v0.18 FWD-22, F.7; row ETFS_RIVALS-Z-S56): the dialog's trade list never says "No trades in the last 365
days" about a window it has not read. The static page says the year's trades load with the chart; the page's one script
writes the list from the chart object's markers when the object loads.

Interface (prescribed, from the cell):
  - `render._trade_list([])` (no trade in the page context) returns the element `<p data-chart-trades>` holding STATIC
    exactly, and the words "No trades in the last 365 days" are no longer in any static markup the function returns;
  - the script exposes `window.rfChart.tradelines(markers)` -> an array of strings: no marker -> [NONE]; otherwise one
    `words(m)` line per marker, NEWEST first by `end` (ties by `start`, newest first), at most 20 lines, and when there are
    more a last line "and <N> earlier trades in the last 365 days." (N = the markers not listed; "trade" when N is 1);
  - when a chart object loads, the script replaces the frame's `[data-chart-trades]` element's content with those lines
    (the text `data-chart-trades` is in the script), for a holding with or without a stored currency.
Runs the script under node, as the package suite does (vm context with a stub document and window).
  - (a) `render._trade_list([])` holds STATIC inside a `data-chart-trades` element and does not hold NONE;
  - (b) tradelines([]) == [NONE];
  - (c) three markers given out of order come back newest first, each line equal to the script's own words(m);
  - (d) 25 markers give 21 lines: the 20 newest, then "and 5 earlier trades in the last 365 days."; 21 markers end "and 1
    earlier trade in the last 365 days.";
  - (e) the script reads `data-chart-trades`, and nc-1.AC1, md-1.AC1 and md-1.AC2 still end `PASS 0 failures`;
  - (f) control: node is on the PATH, the script exposes words() and it words a planted marker as expected, and
    `render._trade_list` with one context trade still lists that trade.
FAIL at base 07ff6ebe34: (a), (b), (c), (d), (e) FAIL (the static NONE sentence; no tradelines; the script does not read
data-chart-trades); (f) PASSES."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

STATIC = "The fund's trades over the last 365 days load with the chart."
NONE = "No trades in the last 365 days"
EARLIER = ("nc-1.AC1", "md-1.AC1", "md-1.AC2")
JS = r"""
const vm = require("vm");
const src = require("fs").readFileSync(process.argv[1], "utf8");
const ctx = {document: {addEventListener() {}}, window: {}};
vm.runInNewContext(src, ctx);
const r = ctx.window.rfChart || {};
const mk = (i, side) => ({side: side, start: "2026-01-" + String(i).padStart(2, "0"), end: "2026-01-" + String(i).padStart(2, "0"),
                          span: false, usd: 1000 * i, bps: i, r: 3, n_trades: 1});
const three = [mk(5, "buy"), mk(20, "sell"), mk(11, "buy")];
const many = []; for (let i = 1; i <= 25; i++) many.push(mk(i, i % 2 ? "buy" : "sell"));
const out = {has_words: typeof r.words === "function", has_tradelines: typeof r.tradelines === "function"};
if (out.has_words) { out.words_three = three.map(m => r.words(m)); out.words_many = many.map(m => r.words(m)); }
if (out.has_tradelines) {
  out.none = r.tradelines([]); out.three = r.tradelines(three); out.many = r.tradelines(many); out.twentyone = r.tradelines(many.slice(0, 21));
}
console.log(JSON.stringify(out));
"""


def node_run(script_text: str):
    node = shutil.which("node")
    if node is None:
        return None, "node is not on the PATH"
    with tempfile.TemporaryDirectory(prefix="rv_tl1_") as d:
        f = pathlib.Path(d) / "chart.js"
        f.write_text(script_text, encoding="utf-8")
        p = subprocess.run([node, "-e", JS, str(f)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        if p.returncode != 0:
            return None, f"node rc {p.returncode}: {(p.stderr or '').strip()[:300]}"
        try:
            return json.loads(p.stdout), None
        except Exception as e:  # noqa: BLE001 -- an unparseable run is a failed arm, not a crash
            return None, f"{type(e).__name__}: {e}"


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    try:
        empty = render._trade_list([])
    except Exception as e:  # noqa: BLE001
        empty = f"<error {type(e).__name__}: {e}>"
    print("_trade_list([]):", empty[:200])
    v.check("data-chart-trades" in empty and STATIC in empty and NONE not in empty,
            "(a) with no trade in the page context the static element holds the load-with-the-chart sentence and not the "
            "no-trades sentence")

    script = (getattr(render, "CHART_SCRIPT", "") or "").replace("@DAY@", "2026-10-02").replace("@FAIL@", getattr(render, "CHART_FAIL", "x"))
    out, err = node_run(script)
    out = out or {}
    print("node:", err or "ran", "| has words:", out.get("has_words"), "| has tradelines:", out.get("has_tradelines"))
    print("  tradelines([]):", out.get("none"))
    print("  tradelines(three):", out.get("three"))
    many = out.get("many") or []
    print("  tradelines(25): lines", len(many), "| first:", many[:1], "| last:", many[-1:])
    print("  tradelines(21) last:", (out.get("twentyone") or [])[-1:])

    v.check(out.get("none") == [NONE], "(b) no marker -> the one line 'No trades in the last 365 days'")
    w3 = out.get("words_three") or []
    v.check(len(w3) == 3 and out.get("three") == [w3[1], w3[2], w3[0]],
            "(c) three markers out of order come back newest first (01-20, 01-11, 01-05), each in the script's own words")
    wm = out.get("words_many") or []
    want = list(reversed(wm))[:20] + ["and 5 earlier trades in the last 365 days."] if len(wm) == 25 else None
    t21 = out.get("twentyone") or []
    v.check(want is not None and many == want and len(t21) == 21 and t21[-1] == "and 1 earlier trade in the last 365 days.",
            "(d) 25 markers -> the 20 newest then 'and 5 earlier trades in the last 365 days.'; 21 -> '... and 1 earlier trade ...'")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1500)
        last = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = last[-1].strip() if last else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    print("script reads data-chart-trades:", "data-chart-trades" in script)
    v.check("data-chart-trades" in script and all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(e) the script reads data-chart-trades, and nc-1.AC1, md-1.AC1 and md-1.AC2 still end PASS 0 failures")

    one = render._trade_list([{"action": "entry", "est_notional": 500.0, "window_start": "2026-10-01", "window_end": "2026-10-01",
                               "window_trading_days": 1}])
    print("_trade_list(one trade):", one[:160])
    v.check(shutil.which("node") is not None and out.get("has_words") is True and len(w3) == 3
            and w3[0] == "Bought on 2026-01-05: $5,000, 5 bps of the fund, 1 trade."
            and "data-chart-trades" in one and "Bought on 2026-10-01: $500, 1 trade." in one,
            "(f) control: node runs the script, its words() reads a planted marker as expected, and one context trade is still listed")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
