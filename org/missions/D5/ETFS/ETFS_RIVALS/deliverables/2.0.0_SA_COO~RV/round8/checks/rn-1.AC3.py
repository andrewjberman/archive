"""RIV-rn-1 AC3 (Andrew-direct 2026-10-05 @a36e70f335, idea 4 of the pitch, agreed): a period that covers fewer than 5 trading
days says so and greys. Measured: the as-of 2026-10-01 is the first day of Q4, so QTD is ONE trading day for every fund, and
Andrew read the switch as "not doing much".

Interface (prescribed): when a period's holding_contribution rows carry `n_days_period` < 5, every switch label for that period
(top switch and inside the components) carries `data-period-short` and reads its length (e.g. "QTD · 1 day" or "QTD, 1
trading day"); a period of 5 or more trading days carries no `data-period-short`.
Fixture: as rn-1.AC2 (IDVZ home, TXUE rival); QTD rows with n_days_period 1 (2026-10-01 to 2026-10-01); R30 30, YTD 188.
  - (a) every label for rf-period-QTD carries data-period-short and its text names "1" and "day";
  - (b) control: no label for rf-period-R30 or rf-period-YTD carries data-period-short.
FAIL at base and at the rn-1 build: (a) FAILS; (b) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

DAYS = {"R30": 30, "MTD": 1, "QTD": 1, "YTD": 188}
START = {"R30": "2026-08-20", "MTD": "2026-10-01", "QTD": "2026-10-01", "YTD": "2026-01-02"}


def fixture():
    from rivalfunds.tests import test_crorv_layout as tl
    hc, bt = [], []
    for fund, role in (("IDVZ", "home"), ("TXUE", "rival")):
        for p in DAYS:
            for r in u.hc_rows(fund, p, {"S1": 0.012, "S2": -0.004}, {"Energy": 0.01}, end="2026-10-01"):
                r.update(role=role, period_start=START[p], period_nominal_start=START[p], period_clipped=False,
                         n_days_period=DAYS[p], n_days_priced=DAYS[p])
                hc.append(r)
            for r in u.bt_rows(fund):
                bt.append(dict(r, role=role, period=p, window_start=START[p], n_trading_days=DAYS[p]))
    funds = [u.fund_view("IDVZ", role="home"), u.fund_view("TXUE")]
    for f in funds:
        f["holdings"] = tl._HOLD.copy()
    return u.page_ctx(funds, a1={"holding_contribution": hc, "buying_trend": bt})


def run(v):
    c.setup_path()
    from rivalfunds import render

    root = u.parse(render.render_page(fixture()))
    labels = {}
    for n in root.iter():
        if n.tag == "label" and str(n.attrs.get("for", "")).startswith("rf-period-"):
            labels.setdefault(n.attrs["for"][len("rf-period-"):], []).append(n)
    q = labels.get("QTD", [])
    print("QTD labels:", len(q), [(u.text(n), "data-period-short" in n.attrs) for n in q[:3]])
    v.check(bool(q) and all("data-period-short" in n.attrs and "1" in u.text(n) and "day" in u.text(n).lower() for n in q),
            "(a) every QTD label is marked short and names its 1 trading day")
    others = [n for p in ("R30", "YTD") for n in labels.get(p, [])]
    print("R30/YTD labels:", len(others), "| marked short:", sum("data-period-short" in n.attrs for n in others))
    v.check(bool(others) and not any("data-period-short" in n.attrs for n in others),
            "(b) control: no R30 or YTD label is marked short")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
