"""RIV-ui-5 AC2 (RFW-U12, DESIGN.md C14 details/summary): consecutive empty trade windows collapse into ONE line ('6
windows, no trades'); the G6 exclusions show once per fund as totals, the per-window detail on demand.
INTERFACE: `render._trades(f, wmax)`. A run of consecutive windows with no trade is ONE element carrying
`data-empty-run="<n>"` whose text states n windows; per-window G6 lines and empty-window notes are off the face (inside
a closed <details> if kept); the per-fund totals line and the `data-excluded-*` attributes stay as today.

Pure, offline fixture (`_ui.fund_view`): TXUE with nine windows, newest first: 2 empty, 1 with one trade (Apple Inc), 6
empty; each window's G6 row excludes 2 cash lines (fund total 18).
  - the empty runs read data-empty-run 2 then 6, and the 6-run's text says "6 windows";
  - the trades block's face carries no "No trades inferred in this window" and no "Excluded before inference", and "cash
    line" at most once (the fund totals; today 10 times);
  - control: Apple Inc's trade shows on the face with its one trace panel, and data-excluded-cash="18"."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402

DAYS = (
    "2026-09-17",
    "2026-09-18",
    "2026-09-21",
    "2026-09-22",
    "2026-09-23",
    "2026-09-24",
    "2026-09-25",
    "2026-09-28",
    "2026-09-29",
    "2026-09-30",
)


def run(v):
    c.setup_path()
    from rivalfunds import render

    pairs = list(zip(DAYS[:-1], DAYS[1:]))[::-1]  # newest first, as publish_page orders them
    wins = [u.window(a, b, [u.trade(a, b)] if i == 2 else []) for i, (a, b) in enumerate(pairs)]
    html = render._trades(u.fund_view("TXUE", windows=wins), 0.02)
    root = u.parse(html)
    runs = [(n.attrs["data-empty-run"], u.text(n)) for n in root.all("data-empty-run")]
    print("empty runs:", runs)
    v.check(
        [r for r, _ in runs] == ["2", "6"] and "6 windows" in runs[1][1],
        "consecutive empty windows collapse into one line per run (2, then 6: '6 windows')",
    )
    fc = u.face(root)
    print("trades face:", fc[:500])
    n_none = fc.count("No trades inferred in this window")
    n_g6 = fc.count("Excluded before inference")
    n_cash = fc.count("cash line")
    v.check(
        n_none == 0 and n_g6 == 0 and n_cash <= 1,
        f"no per-window empty or G6 line on the face; cash lines stated once ({n_none}, {n_g6}, {n_cash})",
    )
    v.check(
        "Apple Inc" in fc and len(root.cls("trace")) == 1 and bool(root.all("data-excluded-cash", "18")),
        "control: the trade window shows its trade and trace panel; the fund total stays 18",
    )


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
