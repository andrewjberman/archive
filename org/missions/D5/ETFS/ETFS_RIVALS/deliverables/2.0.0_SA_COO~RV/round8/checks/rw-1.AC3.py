"""RIV-rw-1 AC3 (RFW-U18, PARTIAL on rv-publish-1002r7): every account opens to its first TWO sentences. Measured: 21 of 22
PASS accounts open to 2, but BASG's direction verdict opens to 3. Its second sentence ends "...into CINTAS CORP." and the
splitter reads "corp" as an abbreviation (`render.py:1096` `_NOT_END`), so it does not end the sentence there.
Interface: `render._ai_card(ctx, f)`; the face lead `p.rf-lead` holds exactly the account's first two sentences. A
company suffix in capitals (CORP., INC., LTD.) followed by a capitalised sentence start ends the sentence. A mid-sentence
abbreviation followed by lower case ("Intuit Inc. reported ...") does not.
  - (a) "... trend. BASG added into CINTAS CORP. The year's strongest move ..." opens to the first two sentences only;
  - (b) control: "Intuit Inc. reported strong demand. It grew. A third." opens to "Intuit Inc. reported strong demand. It
        grew." (the mid-sentence "Inc." is not an end).
FAIL at base: (a); (b) PASSES."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _ui7 as u  # noqa: E402

A = ("The last thirty days mostly add to BASG's year-to-date trend. BASG added again in the recent window, including "
     "$1.3 million into CINTAS CORP. The year's strongest move away was also reinforced by recent trims.")
A_LEAD = ("The last thirty days mostly add to BASG's year-to-date trend. BASG added again in the recent window, including "
          "$1.3 million into CINTAS CORP.")
B = "Intuit Inc. reported strong demand. It grew. A third sentence follows."
B_LEAD = "Intuit Inc. reported strong demand. It grew."


def lead(render, fund, kind, text):
    acct = u.account(fund, kind, text)
    html = render._ai_card({"day": "2026-10-02", "a1": {"research_hypotheses": [acct]}}, {"fund": fund, "role": "rival"})
    leads = u.parse(html).cls("rf-lead")
    return u.text(leads[0]) if leads else ""


def run(v):
    c.setup_path()
    from rivalfunds import render

    a = lead(render, "BASG", "direction_verdict", A)
    b = lead(render, "TXUE", "activity_30d", B)
    print("lead A:", repr(a))
    print("lead B:", repr(b))
    v.check(a == u._norm(A_LEAD), "(a) a sentence ending in capitals 'CINTAS CORP.' ends the lead at two sentences")
    v.check(b == u._norm(B_LEAD), "(b) control: a mid-sentence 'Inc.' does not end a sentence")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
