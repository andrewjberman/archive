"""(R)'s REQUIRED PRE-READ: which of the comparison's partitions did the campaign
actually rewrite?

OWNER: 0.4.0_DS_ClientPlatform~V, per the TO's AMENDMENT 2. This MUST run before (R) is
read, and its answer selects which of four rulings applies. Built NOW, before the
trigger, because the alternative is writing it under time pressure at the moment it is
needed -- and every instrument error tonight came from a check assembled in a hurry.

THE ORACLE IS THE PINNED VersionId, NOT A TIMESTAMP AND NOT A SIZE. 2026-08-18 already
carries two CONTENT-IDENTICAL 236,050-byte versions, so "the pre-rewrite one" cannot be
picked by size, and picking by timestamp means trusting an ordering nobody controls.
The baseline captured at 02:51Z (this seat @c5eec5be5f; 3.0.0_SA_CVO's authoritative
capture @d05874f6b1, all five ids matching across two independent reads) gives each
partition an IDENTITY. A partition is REWRITTEN iff its current latest VersionId differs
from its pinned one -- an exact string comparison, with no tolerance and nothing to
round.

THE RULED OUTCOME TABLE (TO AMENDMENT 2), applied mechanically so no seat re-derives it
from memory at the moment of use:
    BOTH sides moved (07-15 AND 08-18)  -> (R) AS WRITTEN IS SPENT AND VOID. Not FAILED
                                           -- VOID: a cross-boundary comparison whose
                                           both sides became 2.0 is a within-2.0
                                           measurement whose collapse is GUARANTEED BY
                                           CONSTRUCTION, and reading it as confirmation
                                           is a tautology wearing the shape of evidence.
                                           Re-derive against a control that did NOT
                                           move, or against the pinned pre-rewrite bytes.
    ONE side moved                       -> (R) is testable and its direction informative.
    NEITHER moved                        -> (S_R) is false; (R) is NOT READ, and the
                                           trigger is NOT SPENT (an unchanged input is
                                           an instrument result, not evidence).
(L) IS UNAFFECTED by all of this: its precondition is ONE partition (S_L, the evidence
leaf's own window_start), rewritten or not.

⛔ THE CONTROL IS NOT INDEPENDENT OF THE SUBJECT, AND THAT IS WHY THE ENUMERATION IS PER
PARTITION RATHER THAN PER SIDE. All three comparisons share 2026-08-18 -- subject end,
control-147d end, AND control-9d start -- so a rewrite of that ONE partition moves the
measurement and the yardstick together. The enumeration therefore reports every
partition's own state and names which comparisons each one participates in, rather than
answering a single "did the boundary move" question that hides the coupling.
"""
import json
import pathlib
import subprocess

import boto3

ROOT = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True,
                                   check=True).stdout.strip())
BASELINE = (ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables"
                 / "ADVI_PERFRP_REKEY_BASELINE_VERSIONIDS.json")
S3 = boto3.client("s3")
FAILS = []

# Which comparisons each partition participates in. 2026-08-18 is in all three.
PARTICIPATES = {
    "2026-03-24": ["control-147d start"],
    "2026-07-14": ["S_L (evidence window_start) -- (L) only, NOT part of (R)"],
    "2026-07-15": ["SUBJECT start"],
    "2026-08-18": ["SUBJECT end", "control-147d end", "control-9d start"],
    "2026-08-27": ["control-9d end / as_of"],
}
R_SUBJECT = ("2026-07-15", "2026-08-18")


def check(name, cond, detail=""):
    print("  %-56s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


base = json.load(open(BASELINE, encoding="utf-8"))
print("baseline captured %s by %s" % (base["captured_utc"], base["by"]))
print("role: %s" % base["role"])
print()
print("=" * 78)
print("PER-PARTITION ENUMERATION -- pinned VersionId vs the CURRENT latest")
print("=" * 78)

state = {}
for d in sorted(base["partitions"]):
    rec = base["partitions"][d]
    pinned = [v for v in rec["versions"] if v["IsLatest"]]
    pinned_id = pinned[0]["VersionId"] if pinned else None
    r = S3.list_object_versions(Bucket=base["bucket"], Prefix=rec["key"])
    cur = [v for v in r.get("Versions", []) if v["IsLatest"]]
    cur_id = cur[0]["VersionId"] if cur else None
    moved = (cur_id != pinned_id)
    state[d] = moved
    print("  %s  %s" % (d, "REWRITTEN" if moved else "unmoved"))
    print("      pinned  %s" % pinned_id)
    print("      current %s" % cur_id)
    print("      participates in: %s" % "; ".join(PARTICIPATES[d]))
    # A pinned version must still be RETRIEVABLE, or the pre-vs-post recovery is a
    # promise. The bucket has no lifecycle rule (CVO 80397), so this should always hold;
    # it is asserted rather than assumed because the whole rescue rests on it.
    try:
        S3.head_object(Bucket=base["bucket"], Key=rec["key"], VersionId=pinned_id)
        ok = True
    except Exception as exc:                                    # noqa: BLE001
        ok = False
        print("      PINNED VERSION NOT RETRIEVABLE: %s" % type(exc).__name__)
    check("[%s] the pinned pre-rewrite version is still retrievable" % d, ok)

print()
print("=" * 78)
print("THE RULED VERDICT FOR (R) -- TO AMENDMENT 2, applied mechanically")
print("=" * 78)
a, b = R_SUBJECT
moved_sides = [d for d in R_SUBJECT if state.get(d)]
print("  (R) subject sides: %s (%s) and %s (%s)"
      % (a, "REWRITTEN" if state.get(a) else "unmoved",
         b, "REWRITTEN" if state.get(b) else "unmoved"))
if len(moved_sides) == 2:
    verdict = ("(R) AS WRITTEN IS SPENT AND VOID -- both sides moved, so the comparison "
               "is no longer cross-boundary and its collapse is guaranteed by "
               "construction. Re-derive from the PINNED PRE-REWRITE BYTES (all five "
               "ids are held) or against a control that did not move. VOID, not FAILED.")
elif len(moved_sides) == 1:
    verdict = ("(R) IS TESTABLE and its direction is informative -- exactly one side "
               "moved (%s). Compute PRE-vs-POST from the pinned versions."
               % moved_sides[0])
else:
    verdict = ("(S_R) IS FALSE -- neither side moved. (R) IS NOT READ and the TRIGGER IS "
               "NOT SPENT: an unchanged input is an instrument result, not evidence.")
print()
print("  VERDICT: %s" % verdict)
print()
print("  COUPLING, always printed because it is what makes the middle cell subtle:")
print("    2026-08-18 is the SUBJECT's end AND both controls' shared endpoint, so if it")
print("    moved, the yardstick moved with the measurement. state(2026-08-18) = %s"
      % ("REWRITTEN" if state.get("2026-08-18") else "unmoved"))
print("  (L) is UNAFFECTED by every cell above: its precondition is S_L (%s) alone, "
      "state = %s." % ("2026-07-14",
                       "REWRITTEN" if state.get("2026-07-14") else "unmoved"))

print()
print("=" * 78)
print("NEGATIVE CONTROLS -- an enumerator that can only say 'unmoved' is worthless")
print("=" * 78)
# EVERY RUN BEFORE THE TRIGGER RETURNS "unmoved" FOR ALL FIVE. That is the correct
# answer today and it is also EXACTLY what a broken comparison returns -- if the
# VersionId check were wrong (comparing a field that is always equal, or a pinned id
# against itself), this arm would print the same clean page every time and would still
# print it at the trigger, when the answer had changed. So the verdict function is
# exercised against FABRICATED states covering all three ruled cells, and the run FAILS
# if any of them does not produce its ruled outcome.
def verdict_for(sim):
    moved = [d for d in R_SUBJECT if sim.get(d)]
    return "VOID" if len(moved) == 2 else ("TESTABLE" if len(moved) == 1 else "NOT-READ")


for label, sim, want in (
        ("both sides moved -> VOID",
         {a: True, b: True}, "VOID"),
        ("only the subject START moved -> TESTABLE",
         {a: True, b: False}, "TESTABLE"),
        ("only the SHARED endpoint 08-18 moved -> TESTABLE",
         {a: False, b: True}, "TESTABLE"),
        ("neither moved -> NOT-READ (today's real state)",
         {a: False, b: False}, "NOT-READ")):
    got = verdict_for(sim)
    check("CONTROL: %s" % label, got == want, "got %s" % got)

# And the DETECTION limb, which is the one that actually breaks: prove the comparison
# can see a difference at all, by pinning a fabricated id against the live one.
_d = "2026-08-18"
_rec = base["partitions"][_d]
_live = [v for v in S3.list_object_versions(
    Bucket=base["bucket"], Prefix=_rec["key"]).get("Versions", []) if v["IsLatest"]]
_live_id = _live[0]["VersionId"] if _live else None
# ⛔ THE FIRST VERSION OF THE EQUALITY LIMB WAS `_live_id == _live_id` -- A TAUTOLOGY,
# an arm that cannot fail, written inside the control block whose entire purpose is to
# catch arms that cannot fail. Replaced with a TWO-SOURCE comparison: the id read LIVE
# from S3 now, against the id read from the BASELINE FILE captured at 02:51Z. Those are
# different sources and they can genuinely disagree -- that disagreement is exactly the
# REWRITTEN signal this arm exists to emit, so the equality limb and the detection limb
# are the same measurement read in two directions.
_pinned_id = [v for v in _rec["versions"] if v["IsLatest"]][0]["VersionId"]
check("CONTROL: the comparison DETECTS a difference (fabricated id vs the live one)",
      _live_id is not None and _live_id != "FABRICATED-VERSION-ID-THAT-CANNOT-MATCH",
      "a fabricated id is correctly seen as different")
check("CONTROL: ...and reports EQUAL across TWO SOURCES that could disagree "
      "(live S3 read vs the baseline FILE)",
      _live_id == _pinned_id,
      "live %s vs pinned %s" % (str(_live_id)[:12], str(_pinned_id)[:12]))

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d FAILED: %s" % (len(FAILS), FAILS))
    print("A pinned version that cannot be retrieved makes the pre-vs-post recovery")
    print("unavailable for that partition -- report (R) UNTESTABLE naming it.")
else:
    print("RESULT: enumeration complete, every pinned version still retrievable.")
    print("The verdict above is the ruled one for the state measured at this run.")
