"""RIV-fc-1 AC1 (PRD v0.16 FWD-21 @646ce7f4b8; Andrew-direct 2026-10-05 ~03:3xZ: "anytime a stock/ticker is mentioned, it should
be clickable to the modal, and we should be able to see backfill on it"): every security named on the page opens ONE modal for
that security, page-wide, and the modal says so when its history is not yet backfilled.
Measured at the rn-1 build: only the YTD rankings and the trend open a holding dialog (`render._name_button`, one dialog per
fund x holding, `_holding_dialogs`); the trade log, the other periods' rankings and the AI text name securities as plain text;
the page is 1.89 MB of a 2.10 MB gateway cap, so one dialog per fund x security cannot simply be added everywhere.

Interface (prescribed; issuer ruling at the cut: ONE dialog per security page-wide, keyed by its security key, reused by
every mention, so the page grows by one dialog per distinct security and never per mention):
  - every security mention in the rankings tables, the trend tables, the trade log and the AI text is a
    `<button ... data-sec="<security key>" popovertarget="<id>">`;
  - each popovertarget resolves to exactly one element `id="<id>"` carrying `data-sec-dialog="<security key>"`; no two
    elements share a `data-sec-dialog` key;
  - a security with no history rows in the page context reads "History not yet backfilled" in its dialog, which carries
    `data-history="none"`; the page carries no `<script`.
Fixture: IDVZ (home) and TXUE (rival); Apple Inc (AAPL_US_Equity) and Microsoft Corp (MSFT_US_Equity) in the rankings
(R30, QTD, YTD) and the trend of both funds; one TXUE trade in Apple; one TXUE AI account naming AAPL_US_Equity; no history rows.
  - (a) Apple is a data-sec button in each surface (rankings, trend, trade log, AI text), each resolving to Apple's dialog;
  - (b) every data-sec button resolves, at least one dialog exists, and no data-sec-dialog key repeats;
  - (c) Apple's dialog carries data-history="none" and reads "History not yet backfilled";
  - (d) control: the page has no script and still renders a rank panel per fund for R30, QTD and YTD.
FAIL at the rn-1 build: (a), (b), (c) FAIL; (d) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

PERIODS = ("R30", "QTD", "YTD")
SECS = {"AAPL_US_Equity": "Apple Inc", "MSFT_US_Equity": "Microsoft Corp"}


def fixture():
    from rivalfunds.tests import test_crorv_layout as tl
    hc, bt = [], []
    for fund, role in (("IDVZ", "home"), ("TXUE", "rival")):
        for p in PERIODS:
            for r in u.hc_rows(fund, p, {"AAPL_US_Equity": 0.012, "MSFT_US_Equity": -0.004}, {"Energy": 0.01}, end="2026-10-01"):
                if r["axis"] == "security":
                    r["security_name"] = SECS[r["bucket"]]
                r.update(role=role, n_days_period=20)
                hc.append(r)
            for r in u.bt_rows(fund):
                if r["axis"] == "security":
                    k = "AAPL_US_Equity" if r["bucket"] == "S1" else "MSFT_US_Equity"
                    r = dict(r, bucket=k, security_name=SECS[k])
                bt.append(dict(r, role=role, period=p))
    funds = [u.fund_view("IDVZ", role="home"),
             u.fund_view("TXUE", windows=[u.window("2026-09-30", "2026-10-01",
                                                   [u.trade("2026-09-30", "2026-10-01", name="Apple Inc", key="AAPL_US_Equity")])])]
    for f in funds:
        f["holdings"] = tl._HOLD.copy()
    acct = u.account("TXUE", "activity_30d", "TXUE added AAPL_US_Equity over the last 30 trading days.")
    return u.page_ctx(funds, a1={"holding_contribution": hc, "buying_trend": bt, "research_hypotheses": [acct]})


def run(v):
    c.setup_path()
    from rivalfunds import render

    html = render.render_page(fixture())
    root = u.parse(html)
    nodes = list(root.iter())
    ids = {n.attrs.get("id"): n for n in nodes if n.attrs.get("id")}
    dialogs = [n for n in nodes if "data-sec-dialog" in n.attrs]
    buttons = [n for n in nodes if n.tag == "button" and "data-sec" in n.attrs]

    def resolves(b):
        t = ids.get(b.attrs.get("popovertarget"))
        return t is not None and t.attrs.get("data-sec-dialog") == b.attrs.get("data-sec")

    def apple_in(pred):
        hosts = [n for n in nodes if pred(n)]
        return any(b.attrs.get("data-sec") == "AAPL_US_Equity" and resolves(b) for h in hosts for b in h.iter()
                   if b.tag == "button" and "data-sec" in b.attrs)

    surfaces = {
        "rankings": apple_in(lambda n: n.attrs.get("data-component") == "rankings"),
        "trend": apple_in(lambda n: "data-trend-fund" in n.attrs and "rf-card" in n.attrs.get("class", "")),
        "trade log": apple_in(lambda n: "data-trades" in n.attrs),
        "AI text": apple_in(lambda n: "data-ai-fund" in n.attrs),
    }
    print("Apple opens its dialog from:", surfaces, "| data-sec buttons:", len(buttons), "| dialogs:", len(dialogs))
    v.check(all(surfaces.values()), "(a) Apple is a data-sec button resolving to its dialog in rankings, trend, trade log and AI text")

    keys = [d.attrs["data-sec-dialog"] for d in dialogs]
    v.check(bool(dialogs) and bool(buttons) and all(resolves(b) for b in buttons) and len(keys) == len(set(keys)),
            f"(b) every data-sec button resolves; one dialog per security ({len(set(keys))} keys, {len(keys)} dialogs)")

    apple = next((d for d in dialogs if d.attrs.get("data-sec-dialog") == "AAPL_US_Equity"), None)
    print("Apple dialog data-history:", None if apple is None else apple.attrs.get("data-history"))
    v.check(apple is not None and apple.attrs.get("data-history") == "none" and "History not yet backfilled" in u.text(apple),
            "(c) Apple's dialog says its history is not yet backfilled")

    panels = {(n.attrs.get("data-rank-fund"), n.attrs.get("data-rank-period")) for n in nodes if "data-rank-period" in n.attrs}
    v.check("<script" not in html.lower() and all((f, p) in panels for f in ("IDVZ", "TXUE") for p in PERIODS),
            "(d) control: no script; a rank panel per fund for R30, QTD, YTD")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
