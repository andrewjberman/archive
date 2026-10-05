"""RIV-rn-1 AC2 (PRD v0.14 FWD-14/15; Andrew smoke S3: "if it is not year to date, we should not be saying year to date"):
every rank panel and every trend panel states its period, its first and last trading day and its trading-day count up front,
and a window clipped to the fund's first report never reads "Year to date".
Measured: IDVZ's served rank panel reads "Year to date (2026), 2026-08-21 to 2026-10-01" (`render.py` ~:873) although the fund's
history starts 2026-08-21; the trend card's eyebrow reads "Buying trend, year to date" for every fund (~:1057).

Interface (prescribed): each rank panel (`data-rank-period="P"`) and each per-period trend panel (`data-trend-period="P"`,
inside the trend card) carries one element `data-period-window` whose text names the period's label, its first and last
date and "trading days" (e.g. "Last 30 trading days, 2026-08-20 to 2026-10-01, 30 trading days"). R30's label is "Last 30
trading days". When the holding_contribution rows carry `period_clipped` True, that panel's label reads "Data available
since <period_start>" (AMENDED on Andrew-direct 2026-10-05: "Instead of just saying 'Since X', I'd say 'Data available since
X'") and never "Year to date" / "Quarter to date".
Fixture: as rn-1.AC1, with IDVZ's YTD rows clipped (period_start 2026-08-21, period_nominal_start 2026-01-01,
period_clipped True); TXUE's YTD unclipped (period_start 2026-01-02).
  - (a) every rank panel holds a data-period-window naming its two dates and "trading days";
  - (b) IDVZ's YTD rank panel reads "Data available since 2026-08-21" and nowhere "Year to date"; R30 reads "Last 30 trading days";
  - (c) every trend card holds a data-trend-period panel per period, each with a data-period-window;
  - (d) control: TXUE's YTD rank panel still reads "Year to date".
FAIL at base (CLOUD): (a), (b), (c) FAIL; (d) PASSES. At the rn-1 build: (b) FAILS (it reads "Since first report").
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

PERIODS = ("R30", "MTD", "QTD", "YTD")
START = {"R30": "2026-08-20", "MTD": "2026-10-01", "QTD": "2026-10-01", "YTD": "2026-01-02"}


def fixture():
    hc, bt = [], []
    for fund, role in (("IDVZ", "home"), ("TXUE", "rival")):
        for p in PERIODS:
            clipped = fund == "IDVZ" and p == "YTD"
            for r in u.hc_rows(fund, p, {"S1": 0.012, "S2": -0.004}, {"Energy": 0.01}, end="2026-10-01"):
                r.update(role=role, period_start="2026-08-21" if clipped else START[p],
                         period_nominal_start="2026-01-01" if p == "YTD" else START[p], period_clipped=clipped)
                hc.append(r)
            for r in u.bt_rows(fund):
                bt.append(dict(r, role=role, period=p, window_start=START[p]))
    from rivalfunds.tests import test_crorv_layout as tl  # its holdings frame: the page needs one per updated fund
    funds = [u.fund_view("IDVZ", role="home"), u.fund_view("TXUE")]
    for f in funds:
        f["holdings"] = tl._HOLD.copy()
    return u.page_ctx(funds, a1={"holding_contribution": hc, "buying_trend": bt})


def run(v):
    c.setup_path()
    from rivalfunds import render

    root = u.parse(render.render_page(fixture()))
    panels = {(n.attrs.get("data-rank-fund"), n.attrs.get("data-rank-period")): n for n in root.iter()
              if "data-rank-period" in n.attrs}

    def window(node):
        w = [n for n in node.iter() if "data-period-window" in n.attrs]
        return u.text(w[0]) if w else ""

    bad = []
    for (f, p), n in sorted(panels.items()):
        w = window(n)
        if not (w and "2026-10-01" in w and "trading days" in w and any(d in w for d in ("2026-08-21", START.get(p, "?")))):
            bad.append((f, p, w))
    print("rank panels:", len(panels), "| without a full window line:", bad[:4])
    v.check(bool(panels) and not bad, "(a) every rank panel states its period, its two dates and its trading days")

    idvz = u.text(panels.get(("IDVZ", "YTD"), u.Node("x", {})))
    r30 = [window(n) for (f, p), n in panels.items() if p == "R30"]
    print("IDVZ YTD window:", window(panels.get(("IDVZ", "YTD"), u.Node("x", {}))), "| R30 windows:", r30[:2])
    v.check("Data available since 2026-08-21" in idvz and "Year to date" not in idvz and r30
            and all("Last 30 trading days" in w for w in r30),
            "(b) IDVZ's clipped YTD reads 'Data available since 2026-08-21', never 'Year to date'; R30 reads 'Last 30 trading days'")

    cards = [n for n in root.iter() if "data-trend-fund" in n.attrs and "rf-card" in n.attrs.get("class", "")]
    ok_cards = []
    for card in cards:
        tp = {n.attrs.get("data-trend-period"): n for n in card.iter() if "data-trend-period" in n.attrs}
        ok_cards.append(set(tp) >= {"R30", "QTD", "YTD"} and all(window(tp[p]) for p in ("R30", "QTD", "YTD")))
    print("trend cards:", len(cards), "| each with four windowed period panels:", ok_cards)
    v.check(bool(cards) and all(ok_cards), "(c) every trend card holds a windowed panel per period")

    txue = u.text(panels.get(("TXUE", "YTD"), u.Node("x", {})))
    v.check("Year to date" in txue, "(d) control: TXUE's unclipped YTD still reads 'Year to date'")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
