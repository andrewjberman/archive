"""IRPT_ANLREQ round 57 (issuer 2.0.0_SA_COO~G2): the checks of the Opal-built report's price pages. Run from the worktree root.

    python ar_price_checks.py <cell> build|guard|regress     cell is 163, 164, 165 or 166
    python ar_price_checks.py calibrate                      the checker's own formulas against the shipped base elements (must read OK at base)
    python ar_price_checks.py baseline                       writes price_pages_base_status.json (the status of every element at the base)

Each run feeds the SHIPPED Opal producer the REAL overview map with the repository's own fixtures and a deterministic 10-year monthly
price history of its own (AAA 500, BBB 300, CCC 200 dollars; SPY the benchmark proxy, BIL the risk-free proxy), pricing off and on.
Prints one RESULT line: AR-PRICE-<cell>-OK / -FAIL (or -REGRESS-); rc 0 only on OK. ASCII only.
cell 163: eight price elements re-pointed to statistics the layout already has.   cell 164: the series forms (cumulative, drawdown,
annual returns, benchmark chart).   cell 165: the four text elements (two legends, two as-of lines).   cell 166: the per-holding price table.
"""
import json
import math
import subprocess
import sys

IR = "infra/aws/lambda/investor-reporting/"
TESTS = IR + "ycharts/research/tests"
MAP = "org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/maps/overview_map.json"
CHK = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/"
BASE_JSON = CHK + "price_pages_base_status.json"
AS_OF = "2026-10-14"
AMOUNTS = {"AAA": 500.0, "BBB": 300.0, "CCC": 200.0}
FACT = {"AAA": lambda k: 1.012 if k % 7 else 0.97, "BBB": lambda k: 1.008, "CCC": lambda k: 1.01 if k % 5 else 0.985,
        "SPY": lambda k: 1.009 if k % 6 else 0.98, "BIL": lambda k: 1.002}
LABEL = {"estate": "Opal data store", "yfinance": "Public market data", "ycharts": "Licensed market data"}  # AR-g-166 AMENDMENT 1: R8 forbids a vendor name on the page
TIER = {"AAA": "estate", "SPY": "estate", "BIL": "estate", "BBB": "yfinance", "CCC": "ycharts"}
IDS = {163: ["p2.e11", "p2.e14", "p2.e15", "p7.e04", "p7.e10", "p7.e11", "p7.e12", "p7.e13"],
       164: ["p2.e04", "p6.e21", "p2.e17", "p2.e18", "p7.e15"],
       165: ["p2.e03", "p6.e20", "p2.e07", "p2.e16"],
       166: []}
ROUND_IDS = IDS[163] + IDS[164] + IDS[165]
TABLE_ID = "opal.prices.holdings"  # the cell-166 element, appended after the last page like the classified elements
NINE = ["p2.e08", "p2.e13", "p6.e22", "p7.e02", "p7.e03", "p7.e05", "p7.e06", "p7.e07", "p7.e08"]
TEST_FILES = [TESTS + "/" + n for n in ("test_layout_overview.py", "test_opal_producer.py", "test_opal_producer_prices.py",
                                          "test_layout_own_series_columns.py", "test_opal_producer_page_wording.py",
                                          "test_opal_producer_benchmark.py")]
PIN_TEST = TESTS + "/test_layout_overview.py"  # AMENDMENT 1: line 754 pins the count of OWN_SERIES elements of the real map; a cell moves it by its delta
OWN = {163: (MAP, TESTS + "/test_price_pages_repoint.py", PIN_TEST),
       164: (IR + "ycharts/research/layout_overview.py", MAP, TESTS + "/test_price_pages_series.py", PIN_TEST),
       165: (IR + "ycharts/research/layout_overview.py", MAP, TESTS + "/test_price_pages_text.py", PIN_TEST),
       166: (IR + "ycharts/research/layout_overview.py", IR + "ycharts/research/opal_producer.py", TESTS + "/test_price_pages_table.py",
           TESTS + "/test_opal_producer.py")}
SLOT = {163: 301, 164: 302, 165: 302, 166: 303}
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/")


def levels(sym):
    """133 monthly points on the 14th, 2015-10-14 to 2026-10-14: [(date, level)], level 100 at the first."""
    out, v = [], 100.0
    for k in range(133):
        if k:
            v *= FACT[sym](k)
        total = 2015 * 12 + 9 + k
        out.append(("%04d-%02d-14" % (total // 12, total % 12 + 1), v))
    return out


def readers():
    tables = {t: {} for t in ("estate", "yfinance", "ycharts")}
    for sym, tier in TIER.items():
        tables[tier][sym] = levels(sym)

    def make(rows):
        def reader(symbol, start, end):
            return [r for r in rows.get(symbol, []) if start <= r[0] <= end]
        return reader
    return {tier: make(rows) for tier, rows in tables.items()}


def run(pricing, map_path=MAP):
    sys.path.insert(0, TESTS)
    sys.path.insert(0, "lib")
    import test_opal_producer as tp
    import test_opal_producer_prices as tpp
    mp = json.load(open(map_path, encoding="utf-8"))
    over = {"pricing": True, "as_of": AS_OF, "price_readers": readers()} if pricing else {}
    stores = tp.make_stores(map=mp, **over)
    rec = tpp.op.produce(tp.REQ, tp.FIRM, stores)
    sec = {}
    for s in stores["reports"].persisted[0]["report"]["sections"]:
        v = s.get("value")
        if isinstance(v, str):
            try:
                v = json.loads(v)
            except ValueError:
                pass
        sec[s["section_id"]] = {**s, "value": v}
    return rec, sec


def status_map(rec):
    return {e["id"]: [e["status"], e.get("reason")] for e in rec["elements"]}


def fin(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def close(a, b, rel=1e-7):
    return fin(a) and fin(b) and abs(a - b) <= rel * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------- the checker's own arithmetic (independent of the layout)
def portfolio_points():
    """Buy-and-hold [(date, level)] over the price window (as_of less 10 years .. as_of) from the common start."""
    start = "2016-10-14"
    rows = {s: [r for r in levels(s) if start <= r[0] <= AS_OF] for s in AMOUNTS}
    base = {s: rows[s][0][1] for s in AMOUNTS}
    n = len(rows["AAA"])
    return [(rows["AAA"][k][0], sum(AMOUNTS[s] * rows[s][k][1] / base[s] for s in AMOUNTS)) for k in range(n)]


def anchor(points, year):
    """The last level at or before 31 December of `year` (the layout's YTD convention), or None."""
    got = [v for d, v in points if d <= "%d-12-31" % year]
    return got[-1] if got else None


def annual_returns(points):
    last_year = int(points[-1][0][:4])
    out = {}
    for y in range(int(points[0][0][:4]), last_year):
        a0, a1 = anchor(points, y - 1), anchor(points, y)
        if a0 is not None and a1 is not None:
            out[str(y)] = (a1 / a0 - 1.0) * 100.0
    return out


def drawdown_path(points):
    peak, out = points[0][1], []
    for _, v in points:
        peak = max(peak, v)
        out.append((v / peak - 1.0) * 100.0)
    return out


# ---------------------------------------------------------------- the arms
def calibrate():
    """The checker's formulas against shipped base elements (pricing on): they must agree before any cell is graded."""
    fails = []
    rec, sec = run(True)
    pts = portfolio_points()
    ytd = (pts[-1][1] / anchor(pts, 2025) - 1.0) * 100.0
    if not close(sec["p2.e13"]["value"].get("Total return YTD"), ytd):
        fails.append("calibration: p2.e13 YTD %r is not the checker's %r" % (sec["p2.e13"]["value"].get("Total return YTD"), ytd))
    mdd = min(drawdown_path(pts))
    if not close(sec["p6.e22"]["value"].get("Max drawdown all"), mdd):
        fails.append("calibration: p6.e22 max drawdown all %r is not the checker's %r" % (sec["p6.e22"]["value"].get("Max drawdown all"), mdd))
    for i in NINE:
        if sec[i]["status"] != "VALUE":
            fails.append("calibration: base element %s is %s" % (i, sec[i]["status"]))
    return fails


def baseline():
    rec_on, sec_on = run(True)
    rec_off, _ = run(False)
    doc = {"on": status_map(rec_on), "off": status_map(rec_off), "nine": {i: sec_on[i]["value"] for i in NINE}}
    json.dump(doc, open(BASE_JSON, "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
    return doc


def arms_guard(cell):
    """Nothing outside the cell's own elements moves; pricing off still reads NOT_IN_THIS_VERSION for every price element."""
    fails = []
    base = json.load(open(BASE_JSON, encoding="utf-8"))
    rec_on, sec_on = run(True)
    rec_off, _ = run(False)
    on, off = status_map(rec_on), status_map(rec_off)
    for i, want in base["off"].items():
        if off.get(i) != want:
            fails.append("pricing OFF: %s reads %r, base %r" % (i, off.get(i), want))
    for i, got in off.items():
        if i not in base["off"] and got != ["NOT_AVAILABLE", "NOT_IN_THIS_VERSION"]:
            fails.append("pricing OFF: new element %s reads %r, want NOT_IN_THIS_VERSION" % (i, got))
    for i, want in base["on"].items():
        if i in ROUND_IDS:
            if on.get(i) != want and on.get(i, [None])[0] != "VALUE":
                fails.append("pricing ON: %s reads %r, base %r, and is not VALUE" % (i, on.get(i), want))
        elif on.get(i) != want:
            fails.append("pricing ON: %s reads %r, base %r" % (i, on.get(i), want))
    for i, want in base["nine"].items():
        if sec_on[i]["value"] != want:
            fails.append("the base VALUE of %s changed" % i)
    for i in IDS[cell]:
        if i not in base["on"]:
            fails.append("%s is not an element of the base map" % i)
    return fails


def _val(sec, i, fails):
    s = sec.get(i)
    if s is None or s["status"] != "VALUE":
        fails.append("%s is not VALUE (%s)" % (i, None if s is None else (s["status"], s.get("reason"))))
        return None
    return s["value"]


def arms_build_163():
    fails = []
    rec, sec = run(True)
    entry = {e["id"]: e for e in rec["elements"]}
    v = {i: _val(sec, i, fails) for i in IDS[163]}
    for i in IDS[163]:
        if i in entry and entry[i]["method"] != "OWN_SERIES":
            fails.append("%s method is %r, want OWN_SERIES" % (i, entry[i]["method"]))
    t13 = _val(sec, "p2.e13", fails) or {}
    if v["p2.e14"] is not None and not close(v["p2.e14"], t13.get("Total return YTD")):
        fails.append("p2.e14 (YTD) %r is not the YTD cell of p2.e13 %r" % (v["p2.e14"], t13.get("Total return YTD")))
    for i in ("p2.e11", "p2.e15"):
        if v[i] is not None and not fin(v[i]):
            fails.append("%s is not a finite number: %r" % (i, v[i]))
    ret_keys = ["Total return 1Y", "Total return 3Y", "Total return 5Y", "Total return 10Y"]
    sd_keys = ["Std dev 1Y", "Std dev 3Y", "Std dev 5Y", "Std dev 10Y"]
    if isinstance(v["p7.e10"], dict):
        if sorted(v["p7.e10"]) != sorted(ret_keys):
            fails.append("p7.e10 columns are %r, want %r" % (sorted(v["p7.e10"]), sorted(ret_keys)))
        for k in ret_keys:
            if not close(v["p7.e10"].get(k), t13.get(k)):
                fails.append("p7.e10 %s %r is not p2.e13's %r" % (k, v["p7.e10"].get(k), t13.get(k)))
        if v["p7.e11"] != [v["p7.e10"].get(k) for k in ret_keys]:
            fails.append("p7.e11 is not the bars of the p7.e10 row in order %r" % ret_keys)
    elif v["p7.e10"] is not None:
        fails.append("p7.e10 is not a table")
    if isinstance(v["p7.e04"], dict) and isinstance(v["p7.e13"], dict):
        if sorted(v["p7.e04"]) != sorted(sd_keys) or v["p7.e04"] != v["p7.e13"]:
            fails.append("p7.e04 and p7.e13 must be the same table with columns %r: %r vs %r" % (sd_keys, v["p7.e04"], v["p7.e13"]))
        if v["p7.e12"] != [v["p7.e13"].get(k) for k in sd_keys]:
            fails.append("p7.e12 is not the bars of the p7.e13 row in order %r" % sd_keys)
    else:
        fails.append("p7.e04 and p7.e13 must both be tables")
    return fails


def arms_build_164():
    fails = []
    rec, sec = run(True)
    pts = portfolio_points()
    v = {i: _val(sec, i, fails) for i in IDS[164]}
    cum = v["p2.e04"]
    if cum is not None:
        ok = isinstance(cum, list) and len(cum) == len(pts) and all(isinstance(p, list) and len(p) == 2 for p in cum)
        if not ok or not close(cum[-1][1] / cum[0][1], pts[-1][1] / pts[0][1]):
            fails.append("p2.e04 is not the buy-and-hold level path (want %d points ending at %.6f times the first)" % (
                len(pts), pts[-1][1] / pts[0][1]))
    dd = v["p6.e21"]
    if dd is not None:
        want = drawdown_path(pts)
        pcts = [p[1] for p in dd] if isinstance(dd, list) and dd and isinstance(dd[0], list) else dd
        if not (isinstance(pcts, list) and len(pcts) == len(want) and all(close(a, b) for a, b in zip(pcts, want))):
            fails.append("p6.e21 is not the percent-off-the-running-high path of the buy-and-hold level")
    want_y = annual_returns(pts)
    tab = v["p2.e18"]
    ytd = (pts[-1][1] / anchor(pts, int(pts[-1][0][:4]) - 1) - 1.0) * 100.0
    if isinstance(tab, dict):
        if sorted(tab) != sorted(list(want_y) + ["YTD"]):
            fails.append("p2.e18 columns are %r, want %r" % (sorted(tab), sorted(list(want_y) + ["YTD"])))
        for k, w in list(want_y.items()) + [("YTD", ytd)]:
            if not close(tab.get(k), w):
                fails.append("p2.e18 %s is %r, want %r" % (k, tab.get(k), w))
    elif tab is not None:
        fails.append("p2.e18 is not a table")
    bars = v["p2.e17"]
    if bars is not None and isinstance(tab, dict) and bars != [tab.get(k) for k in sorted(want_y)] + [tab.get("YTD")]:
        fails.append("p2.e17 is not the bars of the p2.e18 row: every calendar year in order, then YTD")
    bench = v["p7.e15"]
    spy = [r for r in levels("SPY") if "2016-10-14" <= r[0] <= AS_OF]
    if bench is not None:
        ok = isinstance(bench, list) and len(bench) == len(spy) and all(isinstance(p, list) and len(p) == 2 for p in bench)
        if not ok or not close(bench[-1][1] / bench[0][1], spy[-1][1] / spy[0][1]):
            fails.append("p7.e15 is not the benchmark (SPY) level path over the window (want %d points, last/first %.6f)" % (
                len(spy), spy[-1][1] / spy[0][1]))
    return fails


def arms_build_165():
    fails = []
    rec, sec = run(True)
    v = {i: _val(sec, i, fails) for i in IDS[165]}
    asof = "As of " + AS_OF
    legend = "Opal portfolio: buy-and-hold from the accepted amounts, priced to %s." % AS_OF
    for i in ("p2.e07", "p2.e16"):
        if v[i] is not None and v[i] != asof:
            fails.append("%s is %r, want %r" % (i, v[i], asof))
    for i in ("p2.e03", "p6.e20"):
        if v[i] is not None and v[i] != legend:
            fails.append("%s is %r, want %r" % (i, v[i], legend))
    return fails


def arms_build_166():
    fails = []
    rec, sec = run(True)
    row = _val(sec, TABLE_ID, fails)
    entry = {e["id"]: e for e in rec["elements"]}.get(TABLE_ID)
    if entry is not None and entry["inputs"] != ["prices"]:
        fails.append("%s inputs are %r, want ['prices']" % (TABLE_ID, entry["inputs"]))
    if row is not None:
        want = [{"Ticker": t, "Last price date": AS_OF, "Source": LABEL[TIER[t]]} for t in ("AAA", "BBB", "CCC")]
        if row != want:
            fails.append("%s is %r, want %r" % (TABLE_ID, row, want))
    return fails


BUILD = {163: arms_build_163, 164: arms_build_164, 165: arms_build_165, 166: arms_build_166}


def scope(cell):
    rc = subprocess.run(["git", "merge-base", "HEAD", "box/dell2"], capture_output=True)
    base = rc.stdout.decode().strip()
    if rc.returncode != 0 or not base:
        return ["no merge-base with box/dell2"]
    diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True)
    if diff.returncode != 0:
        return ["git diff rc=%d" % diff.returncode]
    own = set(OWN[cell]) | {"org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md"}
    for c in range(163, 167):
        if SLOT[c] == SLOT[cell]:
            own |= set(OWN[c])
    prefixes = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%d/" % SLOT[cell],) + ISSUER
    names = [n for n in diff.stdout.decode().splitlines() if n.strip()]
    stray = [n for n in names if n not in own and not n.startswith(prefixes) and "/task-orders/IRPT_ANLREQ.TO-AR-g-16" not in n]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


def regress(cell):
    fails = []
    for path in TEST_FILES:
        out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", path], capture_output=True, text=True)
        if out.returncode != 0:
            fails.append("%s: rc=%d %s" % (path.rsplit("/", 1)[-1], out.returncode, ((out.stdout or out.stderr).strip().splitlines() or [""])[-1]))
    return fails + scope(cell)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "calibrate":
        fails = calibrate()
        print("AR-PRICE-CALIBRATE-%s %s" % ("FAIL" if fails else "OK", "; ".join(fails) if fails else "the checker's formulas agree with the shipped base elements"))
        return 1 if fails else 0
    if mode == "baseline":
        doc = baseline()
        print("AR-PRICE-BASELINE-OK on=%d off=%d nine=%d" % (len(doc["on"]), len(doc["off"]), len(doc["nine"])))
        return 0
    if mode not in ("163", "164", "165", "166") or (sys.argv[2:3] or [""])[0] not in ("build", "guard", "regress"):
        print("AR-PRICE-FAIL usage: <163|164|165|166> build|guard|regress | calibrate | baseline")
        return 2
    cell, arm = int(mode), sys.argv[2]
    if arm == "regress":
        fails = regress(cell)
        print("AR-PRICE-%d-REGRESS-%s %s" % (cell, "FAIL" if fails else "OK", "; ".join(fails)))
    else:
        fails = BUILD[cell]() if arm == "build" else arms_guard(cell)
        print("AR-PRICE-%d-%s %s: %s" % (cell, "FAIL" if fails else "OK", arm, "; ".join(fails) if fails else "all arms"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
