"""RIV-as-1 AC1 (row Z-W1-S48; ROUND_ANALYSIS.round13.md ruling 4 @8e9364a2d5): the audit page has its own loud size rule -- over
its cap it publishes the newest trades that fit, states the cut and the count left out, and never lets the gateway refuse it.

Measured 2026-10-07: the served audit.html is 1,381,244 B against the gateway's 2,097,152 B read cap (34.1% under); the trade log
grows every day; publish_page checks only index.html against MAX_PAGE_BYTES and writes audit.html unconditionally.

Interface (prescribed):
  - `render.AUDIT_SOFT_CAP` (bytes, default 1_950_000, as DIALOG_SOFT_CAP); `render.render_audit_page(ctx)` returns a document of at
    most AUDIT_SOFT_CAP bytes when a cut can achieve it: trade trace panels are dropped OLDEST first (by window end) until it fits,
    and the page then carries one element `data-audit-cut="<count left out>"` whose text states the number of trades left out and
    the oldest window end still shown; with nothing cut the attribute is absent;
  - `publish_page`: the manifest carries `audit_trades_left_out` (0 when none), and when it is > 0 the stage prints a line
    starting `FAIL: audit page over cap` (the day still publishes).
Fixture: round 8's fc-1 fixture with TXUE given three one-trade windows ending 2026-09-28, 2026-09-29, 2026-09-30.
  - (a) with AUDIT_SOFT_CAP set to (full audit bytes - 1): the page is at most the cap, shows fewer than 3 trace panels and at
    least 1, carries data-audit-cut equal to the number dropped, and the newest window (2026-09-30) is still shown;
  - (b) control: at the default cap all 3 trace panels are present and data-audit-cut is absent.
FAIL at base: (a) FAILS (no cut, no attribute); (b) PASSES."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

ENDS = ("2026-09-28", "2026-09-29", "2026-09-30")


def fixture():
    import _ui7 as u
    ctx = c.load_fc1().fixture()
    wins = [u.window(e, e, [u.trade(e, e, name="Apple Inc", key="AAPL_US_Equity")]) for e in ENDS]
    for g in ctx["groups"]:
        g["funds"] = [u.fund_view("TXUE", windows=wins) if f["fund"] == "TXUE" else f for f in g["funds"]]
        for f in g["funds"]:
            if "holdings" not in f:
                from rivalfunds.tests import test_crorv_layout as tl
                f["holdings"] = tl._HOLD.copy()
    ctx["n_updated"] = sum(1 for g in ctx["groups"] for f in g["funds"] if f["status"] == "updated")
    return ctx


def traces(html):
    return html.count('<details class="trace"')


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    full = render.render_audit_page(fixture())
    n_full, b_full = traces(full), len(full.encode("utf-8"))
    print("full audit page:", b_full, "B |", n_full, "trace panels | data-audit-cut present:", "data-audit-cut" in full)
    v.check(n_full == 3 and "data-audit-cut" not in full, "(b) control: at the default cap all 3 trades show and nothing is cut")

    had = hasattr(render, "AUDIT_SOFT_CAP")
    old = getattr(render, "AUDIT_SOFT_CAP", None)
    render.AUDIT_SOFT_CAP = b_full - 1
    try:
        cut = render.render_audit_page(fixture())
    finally:
        if had:
            render.AUDIT_SOFT_CAP = old
        else:
            del render.AUDIT_SOFT_CAP
    n_cut, b_cut = traces(cut), len(cut.encode("utf-8"))
    m = re.search(r'data-audit-cut="(\d+)"', cut)
    left = int(m.group(1)) if m else None
    print("cut audit page:", b_cut, "B |", n_cut, "trace panels | data-audit-cut:", left, "| newest window shown:", ENDS[-1] in cut)
    v.check(b_cut <= b_full - 1 and 1 <= n_cut < 3 and left == 3 - n_cut and ENDS[-1] in cut,
            "(a) over the cap the newest trades that fit are shown, and the page states how many were left out")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
