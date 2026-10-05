"""RIV-rn-1 AC1 (PRD v0.14 FWD-19/18; Andrew smoke S7/S8; AMENDED 2026-10-05 on Andrew-direct @575e7d7250 "there is no need for
MTD" and @a36e70f335 ideas 1-2): the period switch opens on the last 30 trading days, then a dividing line, then Quarter / Year to
date (no Month to date); each top pill carries its dates under it; and the same switch sits inside "What drove the return" and "Buying trend", where
choosing a period in any one place moves every one of them -- with no script on the page.
Measured: `render.PERIODS` = MTD, QTD, YTD; `PERIOD_ORDER` YTD first and selected (`render.py` ~:806-813); the switch lives only
at the top (`.rf-periods`); the trend card is year to date only.

Interface (prescribed): one radio group `name="rf-period"` with inputs `id="rf-period-R30|QTD|YTD"` (no MTD radio), R30 `checked`;
the top switch's labels read in order R30, then an element carrying `data-period-divider`, then QTD, YTD, and each top label
holds a `data-period-dates` element naming its first and last date; the rankings component
(`data-component="rankings"`) and each trend card (`data-trend-fund`) each hold a `<label for="rf-period-P">` for all four
periods (labels for the SAME radios, so any one moves all; R30, QTD, YTD); the page carries no `<script`.
Fixture: two funds (IDVZ home, TXUE rival); holding_contribution rows for R30, MTD, QTD, YTD; buying_trend rows carrying `period`
for the same four.
  - (a) the R30, QTD and YTD radios exist, there is no MTD radio, and R30 is the checked one;
  - (b) the top switch reads R30, a divider, then QTD, YTD, and every top label holds a data-period-dates line with two dates;
  - (c) the rankings component and every trend card each hold labels for R30, QTD and YTD, and the page has no script;
  - (d) control: the page still renders a rank panel per fund and period it has rows for (data-rank-fund / data-rank-period).
FAIL at base (CLOUD): (a), (b), (c) FAIL; (d) PASSES. FAIL at the rn-1 build (wk-ETFS_RIVALS-2 2ae50ff5ae): (a), (b) FAIL
(MTD still renders; no dates under the pills); (c), (d) PASS."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

PERIODS = ("R30", "MTD", "QTD", "YTD")  # the fixture still carries MTD rows: the producers keep writing them
SWITCH = ("R30", "QTD", "YTD")


def fixture():
    hc, bt = [], []
    for fund, role in (("IDVZ", "home"), ("TXUE", "rival")):
        for p in PERIODS:
            for r in u.hc_rows(fund, p, {"S1": 0.012, "S2": -0.004}, {"Energy": 0.01}):
                r["role"] = role
                hc.append(r)
            for r in u.bt_rows(fund):
                bt.append(dict(r, role=role, period=p))
    from rivalfunds.tests import test_crorv_layout as tl  # its holdings frame: the page needs one per updated fund
    funds = [u.fund_view("IDVZ", role="home"), u.fund_view("TXUE")]
    for f in funds:
        f["holdings"] = tl._HOLD.copy()
    return u.page_ctx(funds, a1={"holding_contribution": hc, "buying_trend": bt})


def run(v):
    c.setup_path()
    from rivalfunds import render

    html = render.render_page(fixture())
    root = u.parse(html)
    radios = {n.attrs.get("id"): n for n in root.iter() if n.tag == "input" and n.attrs.get("name") == "rf-period"}
    print("rf-period radios:", sorted(radios), "| checked:", [k for k, n in radios.items() if "checked" in n.attrs])
    v.check(all(f"rf-period-{p}" in radios for p in SWITCH) and "rf-period-MTD" not in radios
            and "checked" in radios.get("rf-period-R30", u.Node("x", {})).attrs
            and sum("checked" in n.attrs for n in radios.values()) == 1, "(a) R30, QTD, YTD radios, no MTD; R30 is the checked one")

    top = next((n for n in root.cls("rf-periods")), None)
    import re
    seq, dated = [], []
    if top is not None:
        for n in top.iter():
            if n.tag == "label" and str(n.attrs.get("for", "")).startswith("rf-period-"):
                seq.append(n.attrs["for"][len("rf-period-"):])
                d = [u.text(x) for x in n.iter() if "data-period-dates" in x.attrs]
                dated.append(bool(d) and len(re.findall(r"20\d\d-\d\d-\d\d|[A-Z][a-z]{2} \d{1,2}", d[0])) >= 2)
            elif "data-period-divider" in n.attrs:
                seq.append("|")
    print("top switch order:", seq, "| labels with two dates under them:", dated)
    v.check(seq == ["R30", "|", "QTD", "YTD"] and dated and all(dated),
            "(b) the top switch reads R30, a divider, then QTD, YTD; every pill carries its dates")

    def fors(node):
        return {str(n.attrs.get("for", ""))[len("rf-period-"):] for n in node.iter()
                if n.tag == "label" and str(n.attrs.get("for", "")).startswith("rf-period-")}

    ranks = [n for n in root.iter() if n.attrs.get("data-component") == "rankings"]
    trends = [n for n in root.iter() if "data-trend-fund" in n.attrs and "rf-card" in n.attrs.get("class", "")]
    print("rankings components:", len(ranks), [sorted(fors(n)) for n in ranks], "| trend cards:", len(trends),
          [sorted(fors(n)) for n in trends], "| <script:", "<script" in html.lower())
    v.check(bool(ranks) and bool(trends) and all(fors(n) >= set(SWITCH) and "MTD" not in fors(n) for n in ranks + trends)
            and "<script" not in html.lower(),
            "(c) the rankings component and every trend card hold labels for R30, QTD, YTD (no MTD); no script")

    panels = {(n.attrs.get("data-rank-fund"), n.attrs.get("data-rank-period")) for n in root.iter() if "data-rank-period" in n.attrs}
    shown = {p for _, p in panels}
    print("rank panels:", sorted(panels))
    v.check(all((f, p) in panels for f in ("IDVZ", "TXUE") for p in shown) and {"QTD", "YTD"} <= shown,
            "(d) control: a rank panel per fund for each period the page renders")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
