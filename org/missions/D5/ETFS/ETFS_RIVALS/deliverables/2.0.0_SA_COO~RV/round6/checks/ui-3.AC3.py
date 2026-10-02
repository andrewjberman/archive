"""RIV-ui-3 AC3 (RFW-U07, DESIGN.md C14 helpText tooltip): the BET/TILT definition sits behind the reading pill's
tooltip, not as a sentence in every trend block; the block caption keeps the dates and the trading days.
INTERFACE: `render._trend_card(ctx, f)`. Each reading pill keeps class `rf-tag` and carries `title="<definition>"`; a
bet pill's title defines a BET, a tilt pill's title defines a TILT, each naming "window".

Pure, offline fixture (`_ui.bt_rows`): two tilt lines and two bet lines.
  - the card text (attributes excluded) carries no definition: none of "BET is", "TILT is", "carrying at least half",
    "built across windows";
  - every `rf-tag` pill (4) carries a non-empty title naming its own reading (bet/tilt) and "window";
  - control: the caption (`rf-caption`) still reads "2026-01-02 to 2026-10-02" and "189 trading days"."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import render

    html = render._trend_card(
        {"day": "2026-10-02", "a1": {"buying_trend": u.bt_rows()}}, {"fund": "TXUE", "role": "rival"}
    )
    root = u.parse(html)
    t = u.text(root)
    found = [p for p in ("BET is", "TILT is", "carrying at least half", "built across windows") if p in t]
    print("definition phrases in the card text:", found)
    v.check(not found, "the BET/TILT definition is not printed in the trend block")
    pills = root.cls("rf-tag")
    got = [(u.text(p).lower(), p.attrs.get("title", "")) for p in pills]
    print("pills (text, title):", got)
    ok = len(pills) == 4 and all(
        word in ("bet", "tilt") and title.strip() and word in title.lower() and "window" in title.lower()
        for word, title in got
    )
    v.check(ok, "each reading pill carries its own definition as its title tooltip")
    cap = root.cls("rf-caption")
    ct = u.text(cap[0]) if cap else ""
    print("caption:", ct)
    v.check(
        "2026-01-02 to 2026-10-02" in ct and "189 trading days" in ct,
        "control: the caption keeps the date span and the trading days",
    )


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
