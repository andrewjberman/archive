"""RIV-rn-1 AC1 (PRD v0.14 FWD-19/18; Andrew smoke S7/S8): the period switch opens on the last 30 trading days, then a dividing
line, then Month / Quarter / Year to date; and the same switch sits inside "What drove the return" and "Buying trend", where
choosing a period in any one place moves every one of them -- with no script on the page.
Measured: `render.PERIODS` = MTD, QTD, YTD; `PERIOD_ORDER` YTD first and selected (`render.py` ~:806-813); the switch lives only
at the top (`.rf-periods`); the trend card is year to date only.

Interface (prescribed): one radio group `name="rf-period"` with inputs `id="rf-period-R30|MTD|QTD|YTD"`, R30 `checked`; the top
switch's labels read in order R30, then an element carrying `data-period-divider`, then MTD, QTD, YTD; the rankings component
(`data-component="rankings"`) and each trend card (`data-trend-fund`) each hold a `<label for="rf-period-P">` for all four
periods (labels for the SAME radios, so any one moves all); the page carries no `<script`.
Fixture: two funds (IDVZ home, TXUE rival); holding_contribution rows for R30, MTD, QTD, YTD; buying_trend rows carrying `period`
for the same four.
  - (a) the four radios exist and R30 is the checked one;
  - (b) the top switch reads R30, a divider, then MTD, QTD, YTD;
  - (c) the rankings component and every trend card each hold labels for all four periods, and the page has no script;
  - (d) control: the page still renders a rank panel per fund and period it has rows for (data-rank-fund / data-rank-period).
FAIL at base: (a), (b), (c) FAIL; (d) PASSES for MTD/QTD/YTD (it reads the periods the page renders)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

PERIODS = ("R30", "MTD", "QTD", "YTD")


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
    v.check(all(f"rf-period-{p}" in radios for p in PERIODS) and "checked" in radios.get("rf-period-R30", u.Node("x", {})).attrs
            and sum("checked" in n.attrs for n in radios.values()) == 1, "(a) four period radios; R30 is the checked one")

    top = next((n for n in root.cls("rf-periods")), None)
    seq = []
    if top is not None:
        for n in top.iter():
            if n.tag == "label" and str(n.attrs.get("for", "")).startswith("rf-period-"):
                seq.append(n.attrs["for"][len("rf-period-"):])
            elif "data-period-divider" in n.attrs:
                seq.append("|")
    print("top switch order:", seq)
    v.check(seq == ["R30", "|", "MTD", "QTD", "YTD"], "(b) the top switch reads R30, a divider, then MTD, QTD, YTD")

    def fors(node):
        return {str(n.attrs.get("for", ""))[len("rf-period-"):] for n in node.iter()
                if n.tag == "label" and str(n.attrs.get("for", "")).startswith("rf-period-")}

    ranks = [n for n in root.iter() if n.attrs.get("data-component") == "rankings"]
    trends = [n for n in root.iter() if "data-trend-fund" in n.attrs and "rf-card" in n.attrs.get("class", "")]
    print("rankings components:", len(ranks), [sorted(fors(n)) for n in ranks], "| trend cards:", len(trends),
          [sorted(fors(n)) for n in trends], "| <script:", "<script" in html.lower())
    v.check(bool(ranks) and bool(trends) and all(fors(n) >= set(PERIODS) for n in ranks + trends)
            and "<script" not in html.lower(),
            "(c) the rankings component and every trend card hold labels for all four periods; no script")

    panels = {(n.attrs.get("data-rank-fund"), n.attrs.get("data-rank-period")) for n in root.iter() if "data-rank-period" in n.attrs}
    shown = {p for _, p in panels}
    print("rank panels:", sorted(panels))
    v.check(all((f, p) in panels for f in ("IDVZ", "TXUE") for p in shown) and {"MTD", "QTD", "YTD"} <= shown,
            "(d) control: a rank panel per fund for each period the page renders")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
