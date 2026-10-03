"""RIV-ui-3 AC1 (RFW-U05, chart not glyphs): each trend row's month trend is a small inline SVG, not ASCII marks, and the
card carries no glyph legend.
INTERFACE: `render._trend_card(ctx, f)`. Each row of a trend table carries ONE `<svg data-trend-spark ...>` drawn from
the row's `trend_mark`; the mark string itself is not printed.

Pure, offline fixture (`_ui.bt_rows`): TXUE, two security lines and two sector lines, marks such as "0 0 0 0 + + + + +
0" and ". . . . . . . 0 - 0".
  - one `svg[data-trend-spark]` per trend row (4), each inside its row (<tr>);
  - the card text outside the svgs (an svg <title> is a tooltip) carries no run of five or more space-separated glyphs
    (+ - 0 .) and none of the mark strings;
  - the card text carries no glyph legend ("+ bought", "- sold", "0 no trade");
  - control: the four lines' names (Intuit Inc, Arthur J Gallagher, Energy, Industrials) still render.
Left to the judgment grade: month ticks, and 0 overlap with the adjacent table at 1280-1920 px."""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import render

    rows = u.bt_rows()
    html = render._trend_card({"day": "2026-10-02", "a1": {"buying_trend": rows}}, {"fund": "TXUE", "role": "rival"})
    root = u.parse(html)
    t = u.text(root)
    print("card text:", t[:500])
    sparks = [n for n in root.all("data-trend-spark") if n.tag == "svg"]
    in_rows = [n for n in sparks if u.inside(n, lambda x: x.tag == "tr")]
    print("sparks:", len(sparks), "| inside a row:", len(in_rows))
    v.check(
        len(sparks) == len(rows) == len(in_rows),
        f"one svg[data-trend-spark] per trend row ({len(sparks)} of {len(rows)})",
    )
    printed = u.text(root, skip=lambda n: n.tag == "svg")  # an svg <title> is a tooltip, not printed text
    glyphs = re.findall(r"(?:[+\-0.] ){4,}[+\-0.](?![\w.])", printed)
    marks = [r["trend_mark"] for r in rows if r["trend_mark"] in printed]
    v.check(not glyphs and not marks, f"no ASCII month marks in the card text (found {glyphs[:3] or marks[:3]})")
    legend = [p for p in ("+ bought", "- sold", "0 no trade") if p in t]
    v.check(not legend, f"no glyph legend sentence (found {legend})")
    names = ("Intuit Inc", "Arthur J Gallagher", "Energy", "Industrials")
    v.check(all(n in t for n in names), "control: the four trend lines still render by name")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
