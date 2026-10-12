"""DB-b-157: amend TIMING_CLASSES_PROPOSAL.json to the ruled class set (CTO msg 5955). Text-level edits, no recompute."""
import json
import re
import sys
from pathlib import Path

p = Path(sys.argv[1])
b = p.read_bytes()
t = b.decode("utf-8")


def sub(old, new, count=1):
    global t
    assert t.count(old) == count, (old[:60], t.count(old))
    t = t.replace(old, new)


sub('"TIMING_MID", "TIMING_END", "TIMING_NOT_DETERMINED"]', '"TIMING_MID", "TIMING_NOT_DETERMINED"]', 2)
# value_meaning line
t, n = re.subn(r'    "TIMING_END": "exactly one admitted timing closes and it is END[^\n]*\n', "", t)
assert n == 1
sub('"TIMING_MID": "inferred", "TIMING_END": "inferred", ', '"TIMING_MID": "inferred", ')
sub("a consumer rejects a TIMING_START, TIMING_MID or TIMING_END row", "a consumer rejects a TIMING_START or TIMING_MID row")
sub("(exactly one timing closes: TIMING_START 3, TIMING_MID 1, TIMING_END 0)", "(exactly one timing closes: TIMING_START 3, TIMING_MID 1)")
sub("'exactly one' (three values, one per admitted timing, of which TIMING_END is empty by construction)",
    "'exactly one' (two values, TIMING_START and TIMING_MID: END is the served convention and cannot be the other system's timing, so it is no value)")
sub('"TIMING_MID": 1, "TIMING_END": 0, ', '"TIMING_MID": 1, ')
# token_census entry
t, n = re.subn(r'  \{\n   "token": "TIMING_END",\n(?:   [^\n]*\n)*?  \},\n', "", t)
assert n == 1
# placement cell
t, n = re.subn(r'   \{"reconciles": "RESTATED_CLOSES_UNDER_OTHER_TIMING", "timing": "TIMING_END"[^\n]*\n', "", t)
assert n == 1
# new_tokens
sub('"TIMING_MID", "TIMING_END", "TIMING_NOT_DETERMINED"]', '"TIMING_MID", "TIMING_NOT_DETERMINED"]') if False else None
sub('"TIMING_START", "TIMING_MID", "TIMING_END", "TIMING_NOT_DETERMINED"],\n "superseded', '"TIMING_START", "TIMING_MID", "TIMING_NOT_DETERMINED"],\n "superseded', 0) if False else None
# the tail: add the two last members
assert t.endswith('\n }\n}\n'), repr(t[-20:])
add = {
    "retired_tokens": [
        {"token": "RESTATED_X", "retired_by": "", "why": ""},
    ],
}
tail = ''',
 "retired_tokens": [
  {"token": "RECONCILES_YES", "retired_by": "1.0.0_SA_CTO~DELL2 msg 5886 (2026-10-11 ~21:40Z)", "why": "END is the SERVED convention, and END closes in 0 of 51; so no segment's served return closes against the custodian's. RECONCILES_YES would be read as 'our number matches'. It does not. Replaced by RESTATED_CLOSES_UNDER_OTHER_TIMING."},
  {"token": "RECONCILES_NO", "retired_by": "1.0.0_SA_CTO~DELL2 msg 5886 (2026-10-11 ~21:40Z)", "why": "Retired with RECONCILES_YES: the axis is a restatement closing, not the served number matching. Replaced by RESTATED_DOES_NOT_CLOSE_UNDER_OTHER_TIMING."},
  {"token": "TIMING_END", "retired_by": "1.0.0_SA_CTO~DELL2 msg 5955 (2026-10-11 ~22:15Z)", "why": "With the first axis defined as a close under a timing OTHER than the served one, END can never be a member, and a value that cannot occur is not a value. TIMING is three: TIMING_START, TIMING_MID, TIMING_NOT_DETERMINED."}
 ],
 "ruled": {
  "by": "1.0.0_SA_CTO~DELL2 msg 5955 (2026-10-11 ~22:15Z)",
  "accepted_axis": "RESTATED_CLOSE",
  "accepted_values": ["RESTATED_CLOSES_UNDER_OTHER_TIMING", "RESTATED_DOES_NOT_CLOSE_UNDER_OTHER_TIMING"],
  "accepted_claim": "measured",
  "timing_values": ["TIMING_START", "TIMING_MID", "TIMING_NOT_DETERMINED"],
  "timing_claim": "inferred for TIMING_START and TIMING_MID",
  "placement_stands": "51 close under another timing: 3 START, 1 MID, 47 not determined",
  "served_relabelled": false,
  "entered_in": "the tie-out's records only",
  "not_claimed": "no record says the served return matches the custodian's on these 51"
 }
}
'''
t = t[: -len("\n}\n")] + tail
json.loads(t)
p.write_bytes(t.encode("utf-8"))
