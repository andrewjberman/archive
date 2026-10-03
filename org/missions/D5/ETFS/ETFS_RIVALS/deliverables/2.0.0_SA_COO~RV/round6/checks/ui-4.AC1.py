"""RIV-ui-4 AC1 (RFW-U08, DESIGN.md C14 no block of system facts on the face): an AI account's face carries its prose and
'What would prove this wrong'. Cited rows, grade history, the demo-read note, the inputs and the run provenance open
from a closed 'Sources and checks' control.
INTERFACE: `render._ai_card(ctx, f)`. The audit material sits inside `<details data-sources>` elements (closed, summary
text "Sources and checks"): at most one per account, plus at most one for the card's run provenance.

Pure, offline fixture (`_ui.account`): TXUE, two PASS accounts. activity_30d cites two rows (holding_contribution
TXUE|R30|S1, trade_schedule TXUE|S1|2026-09-14), was written by a seat ad-hoc run (demo read) and records three input
vintages; direction_verdict was re-graded (grounding_check/4) over a superseded grade. Run runU8, model stub-model-x.
  - the card's face (closed <details> show only their summary) carries none of: "Cited rows", "TXUE|R30|S1",
    "Re-graded", "Superseded grade", "Demo read", "Inputs as of", "runU8", "stub-model-x";
  - every one of them is reachable inside a `data-sources` element;
  - every `data-sources` element is a closed <details> whose summary reads "Sources and checks", 1 to 3 of them;
  - control: the face keeps each account's first sentence and 'What would prove this wrong'."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui as u  # noqa: E402

AUDIT = (
    "Cited rows",
    "TXUE|R30|S1",
    "Re-graded",
    "Superseded grade",
    "Demo read",
    "Inputs as of",
    "runU8",
    "stub-model-x",
)
FIRST = ("TXUE added $23.0 million of Intuit Inc in the last 30 days.", "The fund is leaning into software.")


def run(v):
    c.setup_path()
    from rivalfunds import render

    a = u.account(
        "TXUE",
        "activity_30d",
        FIRST[0] + " The adds came in five windows. It kept trimming Arthur J Gallagher.",
        cited=[
            {"table": "holding_contribution", "key": "TXUE|R30|S1", "revision": "hc1", "value": 0.00340522},
            {"table": "trade_schedule", "key": "TXUE|S1|2026-09-14", "revision": "g5", "value": -2854200.0},
        ],
        observed=["TXUE added Intuit Inc in five windows."],
        inferred=["the manager may keep adding"],
        vintages={"fear_greed/fear_greed_index": "2026-10-01", "rsi/equities": "2026-10-01"},
        manifest={"run_path": "seat-adhoc", "seat": "2.0.0_SA_COO~RV", "run_at": "2026-10-02T01:00:00Z"},
        run_id="runU8",
    )
    b = u.account(
        "TXUE",
        "direction_verdict",
        FIRST[1] + " Its software weight rose from 8% to 11%.",
        manifest={
            "superseded": {
                "grounding": "FAIL",
                "reason": "an older grader missed a percent",
                "grader": "grounding_check/2",
            },
            "regraded_at": "2026-10-02T03:00:00Z",
            "grader": "grounding_check/4",
        },
        run_id="runU8",
    )
    html = render._ai_card(
        {"day": "2026-10-02", "a1": {"research_hypotheses": [a, b]}}, {"fund": "TXUE", "role": "rival"}
    )
    root = u.parse(html)
    fc = u.face(root)
    print("card face:", fc[:600])
    on_face = [x for x in AUDIT if x in fc]
    v.check(not on_face, f"no audit material on the account face (found {on_face})")
    src = root.all("data-sources")
    stext = " ".join(u.text(n) for n in src)
    unreach = [x for x in AUDIT if x not in stext]
    v.check(not unreach, f"all audit material is reachable inside data-sources (missing {unreach})")
    shape = [(n.tag, n.closed, u.face(n)) for n in src]
    print("data-sources elements (tag, closed, summary):", shape)
    v.check(
        1 <= len(src) <= 3
        and all(tag == "details" and closed and "Sources and checks" in s for tag, closed, s in shape),
        "the audit material opens from closed 'Sources and checks' controls (1 to 3)",
    )
    v.check(
        all(s in fc for s in FIRST) and "What would prove this wrong" in fc,
        "control: each account's first sentence and 'What would prove this wrong' stay on the face",
    )


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
