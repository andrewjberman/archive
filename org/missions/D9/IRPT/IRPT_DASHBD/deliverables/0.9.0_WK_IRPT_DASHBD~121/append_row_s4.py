"""Append row IRPT_DASHBD-D2-W121-S4 to the investigation file, as bytes (the existing content is not re-encoded)."""
import json
import sys

row = {
    "id": "IRPT_DASHBD-D2-W121-S4",
    "project": "IRPT_DASHBD",
    "fabric": "dell2",
    "surfaced_by": "0.9.0_WK_IRPT_DASHBD~121",
    "surfaced_at": "2026-10-11T22:04:00Z",
    "one_line": "DB-b-155: under the renamed first axis (a close under START or MID, the served END not counting) the ruling's kept TIMING_END value cannot hold a member by construction; it is empty today for the measured reason and empty always for the structural one.",
    "class": "OBSERVATION",
    "hazard_standing": "INERT",
    "spec_asserts": "CTO msg 5886: the first axis is renamed for what it measures, the return closes when RESTATED under an admitted timing other than the served one; the two axes and the TIMING tokens stand: 3 START, 1 MID, 47 not determined.",
    "world_is": "TIMING is asked only of segments in the first value, which now requires a close under START or MID. TIMING_END means exactly one admitted timing closes and it is END, which contradicts that requirement, so the value has no possible member, not only no member today (END closes in 0 of 51). The record keeps the token as the ruling says and states the emptiness on the TIMING_END value meaning. Whether to keep, retire or redefine TIMING_END is not decided here. The producer's rule line still counts any of the three timings as closing; on the 90 this changes no placement (51 close under START or MID, 39 fail the four-item dollar tie), recomputed by no one in this order.",
    "grounding": {
        "status": "GROUNDED",
        "evidence": [
            "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~121/TIMING_CLASSES_PROPOSAL.json (axes[1].value_meaning.TIMING_END, axes[0].domain_changed_by_the_rename)",
        ],
    },
    "disposition": "UNDER_INVESTIGATION",
}
text = "\n```json\n" + json.dumps(row, indent=2) + "\n```\n"
assert text.isascii()
p = sys.argv[1]
with open(p, "ab") as f:
    f.write(text.encode("ascii"))
print("appended", len(text), "bytes")
