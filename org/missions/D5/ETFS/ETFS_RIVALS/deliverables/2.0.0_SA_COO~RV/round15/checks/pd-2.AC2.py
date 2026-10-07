"""RIV-pd-2 AC2 (PRD v0.18 FWD-23): the security dialog speaks the three periods -- its contribution rows are the last 30 / 90 /
365 days, its buying line is the R365 trend row -- and a period that ranks nothing for a fund still greys and says why.

Measured today: `_sec_fund_section` lists R30, QTD, YTD; `_sec_dialogs` prefers the YTD trend row (:1776) and the sentence says
"this year" (:1750); a fund with no R90 rows has no R90 label to grey because there is no R90 switch.

Interface (prescribed, verbatim): `PERIOD_LABEL = {"R30": "Last 30 days", "R90": "Last 90 days", "R365": "Last 365 days"}`. The
dialog keys cover R30 and R365; the security dialog's trend row prefers R365. A period that ranks nothing for the fund greys
and says why (unchanged rule). Rows of MTD / QTD / YTD in the context are ignored, not an error.
Fixture: round 8's fc-1 page with rows for R30, R90, R365, MTD, QTD, YTD. Apple's contribution is +1.20% (R30), +2.10% (R90),
+3.40% (R365), +9.90% (MTD, QTD, YTD). TXUE's Apple trend row is net BOUGHT in every period except R365, where it is net SOLD
($5.0m away). IDVZ has no R90 holding_contribution rows.
  - (a) TXUE's section of Apple's dialog reads "Last 30 days +1.20%", "Last 90 days +2.10%", "Last 365 days +3.40%" and never
        +9.90%;
  - (b) TXUE's section of Apple's dialog reads "net sold" (the R365 trend row) and not "net bought";
  - (c) the top switch's R90 label carries the "(nothing ranked)" state for IDVZ (`data-state-fund="IDVZ"`) and not for TXUE;
  - (d) control: Apple's dialog exists with one section per fund, and TXUE's section shows +1.20% and a net figure.
FAIL at base: (a), (b), (c) FAIL (QTD / YTD rows at +9.90%, the YTD trend row "net bought", no R90 label); (d) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

SIX = ("R30", "R90", "R365", "MTD", "QTD", "YTD")
VALUE = {"R30": 0.012, "R90": 0.021, "R365": 0.034, "MTD": 0.099, "QTD": 0.099, "YTD": 0.099}
APPLE = "AAPL_US_Equity"


def fixture():
    ctx = c.load_fc1().fixture()
    a1 = ctx["a1"]
    hc0 = [r for r in a1["holding_contribution"] if r.get("period") == "R30"]
    bt0 = [r for r in a1["buying_trend"] if r.get("period") == "R30"]
    hc, bt = [], []
    for p in SIX:
        for r in hc0:
            if p == "R90" and r["fund_id"] == "IDVZ":
                continue
            r = dict(r, period=p)
            if r.get("bucket") == APPLE:
                r["contribution"] = VALUE[p]
            hc.append(r)
        for r in bt0:
            r = dict(r, period=p)
            if p == "R365" and r["fund_id"] == "TXUE" and r.get("bucket") == APPLE:
                r.update(lean="away", net_notional_base=-5000000.0, gross_notional_base=5000000.0, n_windows=1, rank=2,
                         reading="bet")
            bt.append(r)
    a1["holding_contribution"], a1["buying_trend"] = hc, bt
    return ctx


def run(v):
    c.setup_path()
    c.offline_guards()
    import _ui7 as u

    from rivalfunds import render

    html = render.render_page(fixture())
    root = u.parse(html)
    nodes = list(root.iter())
    dlg = next((n for n in nodes if n.attrs.get("data-sec-dialog") == APPLE), None)
    secs = {} if dlg is None else {n.attrs["data-fund"]: u.text(n) for n in dlg.iter() if n.tag == "section" and "data-fund" in n.attrs}
    tx = secs.get("TXUE", "")
    print("Apple dialog sections:", sorted(secs), "| TXUE section text:", tx)

    v.check(all(w in tx for w in ("Last 30 days +1.20%", "Last 90 days +2.10%", "Last 365 days +3.40%")) and "+9.90%" not in tx,
            "(a) the dialog lists the last 30 / 90 / 365 days and no MTD / QTD / YTD row")
    v.check("net sold" in tx and "net bought" not in tx, "(b) the dialog's buying line is the R365 trend row")

    ctl = root.cls("rf-controls")
    states = {}
    for n in (ctl[0].iter() if ctl else ()):
        if n.tag == "label" and (n.attrs.get("for") or "").startswith("rf-period-"):
            states[n.attrs["for"][len("rf-period-"):]] = sorted(s.attrs.get("data-state-fund") for s in n.iter()
                                                                if "data-state-fund" in s.attrs)
    print("top switch 'nothing ranked' states by period:", states)
    v.check(states.get("R90") == ["IDVZ"] and "(nothing ranked)" in u.text(ctl[0]) if ctl else False,
            "(c) a period that ranks nothing for a fund greys and says why (R90 for IDVZ only)")

    v.check(dlg is not None and sorted(secs) == ["IDVZ", "TXUE"] and "+1.20%" in tx and " net " in tx,
            "(d) control: Apple's dialog has a section per fund with its R30 figure and its buying line")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
