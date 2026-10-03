"""RIV-ui-3 AC2 (RFW-U06, format:money -- one money format): net notional, and the gross under it when the line churned,
read in $ millions with one decimal and a sign on the net ('+$23.0m'), never to the dollar ('+22,973,442').
INTERFACE: `render._trend_card(ctx, f)` (the net cell and the "of ... traded" note `_of_gross` writes).

Pure, offline fixture (`_ui.bt_rows`): Intuit Inc net +22,973,442 of 50,000,000 traded; Arthur J Gallagher net
-1,340,000; sectors Energy net +30,000,000 and Industrials -2,000,000 (a U+2212 minus is read as '-').
  - the card text carries "+$23.0m", "-$1.3m", "+$30.0m" and "-$2.0m";
  - the churn note reads "$50.0m" (gross 50,000,000 is at least twice the net);
  - no figure on the card is printed to the dollar: no number with two or more thousands groups (d,ddd,ddd);
  - control: the window counts (5, 1, 4, 1) still render in the Windows column.
Left to the judgment grade: holding names wrap to at most 2 lines."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def _has(t, s):
    """`s` in `t`, tolerating whitespace between the sign, '$', the figure and 'm'."""
    return bool(re.search(r"\s*".join(re.escape(ch) for ch in s), t))


def run(v):
    c.setup_path()
    from rivalfunds import render

    html = render._trend_card(
        {"day": "2026-10-02", "a1": {"buying_trend": u.bt_rows()}}, {"fund": "TXUE", "role": "rival"}
    )
    root = u.parse(html)
    t = u.text(root)
    print("card text:", t[:600])
    want = ("+$23.0m", "-$1.3m", "+$30.0m", "-$2.0m")
    miss = [w for w in want if not _has(t, w)]
    v.check(not miss, f"net notional reads in $ millions, one decimal, signed (missing {miss})")
    v.check(_has(t, "$50.0m"), "the churn note reads the gross in $ millions ('$50.0m')")
    raw = re.findall(r"\d{1,3}(?:,\d{3}){2,}", t)
    v.check(not raw, f"no figure printed to the dollar (found {raw})")
    win = []
    for tr in root.tags("tr"):
        tds = [x for x in tr.children if isinstance(x, u.Node) and x.tag == "td"]
        if len(tds) >= 4:
            win.append(u.text(tds[3]))
    print("windows column:", win)
    v.check(win == ["5", "1", "4", "1"], "control: the Windows column still carries the window counts")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
