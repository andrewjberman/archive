"""RIV-rw-1 AC2 (RFW-U12, PARTIAL on rv-publish-1002r7): every run of consecutive 0-trade windows collapses into ONE line,
including windows that carry a money-market (cash_equiv) or zero-share (no_move) note. Each note is kept inside the run.
Measured: 4 runs (12 windows: IDVZ 4, WCMG 4, TSEL 2, PCLG 2) still render one heading per window. `_empty_window`
(`render.py:311-313`) excludes a window carrying either note from the collapse.
Interface: `render._trades(f, wmax)`. A run of 0-trade windows (not refused) is ONE `details[data-empty-run=<n>]`, and
each window's note text appears inside it. A window with trades keeps its own heading.
Fixture (one fund TXUE, windows newest first):
  W1 2026-09-29..09-30 has a trade;
  W2..W4 have 0 trades, each with cash_equiv=1;
  W5 has 0 trades and no note.
  - (a) W2..W5 collapse into ONE run: data-empty-run="4", and there is no 'Window ...' heading for W2..W5;
  - (b) the three money-market notes survive inside the run (the text "money-market" appears in it);
  - (c) control: W1 keeps its heading and its trade row.
FAIL at base: (a) and (b) (W2..W4 each get a heading; W5 is a run of 1); (c) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

WIN = [("2026-09-29", "2026-09-30"), ("2026-09-26", "2026-09-29"), ("2026-09-25", "2026-09-26"),
       ("2026-09-24", "2026-09-25"), ("2026-09-23", "2026-09-24")]


def run(v):
    c.setup_path()
    from rivalfunds import render

    ws = [u.window(*WIN[0], trades=[u.trade(*WIN[0])])]
    for i in (1, 2, 3):
        w = u.window(*WIN[i])
        w["cash_equiv"] = 1
        ws.append(w)
    ws.append(u.window(*WIN[4]))
    f = u.fund_view("TXUE", windows=ws)
    root = u.parse(render._trades(f, 0.1))
    runs = root.all("data-empty-run")
    heads = [u.text(h) for h in root.tags("h4") if u.text(h).startswith("Window")]
    print("empty runs:", [(r.attrs.get("data-empty-run"), u.text(r)[:120]) for r in runs])
    print("window headings:", heads)
    v.check(len(runs) == 1 and runs[0].attrs.get("data-empty-run") == "4" and len(heads) == 1,
            "(a) W2..W5 collapse into ONE run of 4, and only W1 keeps a heading")
    v.check(len(runs) == 1 and u.text(runs[0]).lower().count("money-market") >= 3,
            "(b) the three money-market notes survive inside the run")
    v.check(any(WIN[0][0] in h and "1 trade" in h for h in heads) and len(root.all("data-income-funded")) == 1,
            "(c) control: W1 keeps its heading and its one trade row")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
