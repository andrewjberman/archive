"""RIV-ui-4 AC3 (RFW-U10 + RFW-D09 render half, DESIGN.md C14 status leads): an account's grade is a badge at its top,
before its prose. A Grounding FAIL account is collapsed by default, its reason on the summary line; a PASS account is
not.
INTERFACE: `render._ai_card(ctx, f)`. Each account keeps `data-ai-kind="<kind>"` and carries ONE badge element
`data-grade="PASS|FAIL"` placed before its text. A FAIL account's prose sits inside a closed <details> whose <summary>
carries the grounding reason.

Pure, offline fixture (`_ui.account`): TXUE, activity_30d FAIL (reason "'$1.6 million, $1.3 million' not in any cited
row", the IDVZ walker case) and direction_verdict PASS.
  - each account carries exactly one data-grade badge: activity_30d FAIL, direction_verdict PASS;
  - in each account the badge comes before the account's first sentence;
  - the FAIL account's first sentence is NOT on the card face, and the face carries its reason ("$1.6 million");
  - control: the PASS account's first sentence is on the card face."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402

FAIL_FIRST = "TXUE bought $1.6 million of Intuit Inc and $1.3 million of Adobe Inc this month."
PASS_FIRST = "The fund is leaning into software."
REASON = "'$1.6 million, $1.3 million' not in any cited row"


def run(v):
    c.setup_path()
    from rivalfunds import render

    fa = u.account(
        "TXUE", "activity_30d", FAIL_FIRST + " The adds came in two windows.", grounding="FAIL", reason=REASON
    )
    pa = u.account("TXUE", "direction_verdict", PASS_FIRST + " Its software weight rose from 8% to 11%.")
    html = render._ai_card(
        {"day": "2026-10-02", "a1": {"research_hypotheses": [fa, pa]}}, {"fund": "TXUE", "role": "rival"}
    )
    root = u.parse(html)
    grades, order = {}, {}
    for kind, first in (("activity_30d", FAIL_FIRST), ("direction_verdict", PASS_FIRST)):
        acc = root.all("data-ai-kind", kind)
        badges = acc[0].all("data-grade") if len(acc) == 1 else []
        grades[kind] = [b.attrs["data-grade"] for b in badges]
        pos = html.find(first[:30], acc[0].start) if len(acc) == 1 else -1
        order[kind] = len(badges) == 1 and 0 <= badges[0].start < pos
    print("grades:", grades, "| badge before prose:", order)
    v.check(
        grades == {"activity_30d": ["FAIL"], "direction_verdict": ["PASS"]},
        "each account carries one data-grade badge (activity_30d FAIL, direction_verdict PASS)",
    )
    v.check(all(order.values()), "in each account the grade badge comes before the prose")
    fc = u.face(root)
    print("card face:", fc[:500])
    v.check(
        FAIL_FIRST not in fc and "$1.6 million" in fc,
        "the FAIL account is collapsed by default, its reason on the face (summary line)",
    )
    v.check(PASS_FIRST in fc, "control: the PASS account's first sentence is on the face")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
