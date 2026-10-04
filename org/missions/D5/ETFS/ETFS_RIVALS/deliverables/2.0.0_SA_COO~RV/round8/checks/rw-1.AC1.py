"""RIV-rw-1 AC1 (RFW-U07, PARTIAL on rv-publish-1002r7): the buying-trend card's caption carries the dates and trading days
only. Measured: all 13 served trend cards still carry 'The net amount the manager bought (+) or sold (-), in $ millions.
Click a holding for its month-by-month record; hover a Tilt or Bet tag for what it means.' (`render.py:1031-1032`).
Interface: `render._trend_card(ctx, f)`. The trend's `p.rf-caption` (the one without `data-unclassified-share`) reads the
window dates and trading days (plus a refused-window note when one exists) and nothing else. The money unit still shows in
the card (a column heading or a title carries "$ millions" or "$m"). The Tilt/Bet pills keep their title tooltips.
  - (a) the caption holds the dates and "trading days", and no "$ millions" / "Click" / "hover" sentence;
  - (b) the unit is still on the card outside the caption ("$ millions" or "$m" in a heading, cell or title);
  - (c) control: every Tilt/Bet pill carries a title.
FAIL at base: (a) and (b) (today the unit sits only in the caption, so moving it is part of the build); (c) PASSES."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import render

    rows = u.bt_rows("TXUE")
    html = render._trend_card({"day": "2026-10-02", "a1": {"buying_trend": rows}}, {"fund": "TXUE", "role": "rival"})
    root = u.parse(html)
    caps = [n for n in root.cls("rf-caption") if "data-unclassified-share" not in n.attrs]
    cap = u.text(caps[0]) if caps else ""
    print("caption:", repr(cap))
    r0 = rows[0]
    dates = [str(r0.get("window_start"))[:10], str(r0.get("window_end"))[:10]]
    v.check(bool(caps) and all(d in cap for d in dates) and "trading days" in cap
            and not re.search(r"\$ ?millions|click|hover", cap, re.I),
            "(a) the trend caption reads the dates and trading days only")
    outside = u.text(root, skip=lambda n: n in caps)
    titles = " ".join(n.attrs.get("title", "") for n in root.all("title"))
    v.check(re.search(r"\$ ?millions|\$m\b", outside + " " + titles, re.I) is not None,
            "(b) the money unit is still on the card, outside the caption")
    pills = [n for n in root.iter() if re.fullmatch(r"(Tilt|Bet)(, \d+ trades?)?", u.text(n) or "") and n.tag in ("span", "b")]
    v.check(bool(pills) and all(p.attrs.get("title") for p in pills),
            f"(c) control: every Tilt/Bet pill carries a title ({len(pills)} pills)")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
