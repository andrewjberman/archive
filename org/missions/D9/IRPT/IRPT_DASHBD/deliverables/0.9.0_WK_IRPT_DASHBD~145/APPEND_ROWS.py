"""Append the worker 0.9.0_WK_IRPT_DASHBD~145 surprise rows to the investigation file as raw bytes (never re-encoded).

Usage: python -I append_w145.py <investigation_file> <surfaced_at_utc>
"""
import json
import sys
from pathlib import Path

INV = Path(sys.argv[1])
NOW = sys.argv[2]
SURFACER = "0.9.0_WK_IRPT_DASHBD~145"

ROWS = [
    {
        "title": "The account return table does not say whether total_return_daily is served on a FLOW_UNRECONCILED or GRADED_DISAGREED day, so the window return fold rests on an inference",
        "id": "IRPT_DASHBD-D2-W145-S1",
        "one_line": "account_return_daily defines total_return_daily as null only on NOT_MEASURABLE, yet ruling 17 says a guard disagreement serves no number; the cumulative-return fold had to choose, and chose ABSENT for a GRADED_DISAGREED day and as-served-with-a-flag for a FLOW_UNRECONCILED day.",
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "spec_asserts": "DB-b-179 directs every fold to name the account return table's guard and day_quality rules, and the cumulative return to compound total_return_daily under those rules.",
        "world_is": "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json at base f3186318ba defines total_return_daily as null on NOT_MEASURABLE only, and its supersedes block says ruling 17 means a guard disagreement serves no number. No sentence states whether a GRADED_DISAGREED or FLOW_UNRECONCILED row's total_return_daily is served as a number or nulled. The fold of avs.<window>.return_cumulative therefore makes the window ABSENT on any GRADED_DISAGREED row and compounds FLOW_UNRECONCILED rows as served with a flag; both choices are the worker's inference from the sibling, not a sibling rule.",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json at f3186318ba: total_return_daily meaning reads 'null on NOT_MEASURABLE'",
                "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json at f3186318ba: supersedes.changes reads 'a guard disagreement serves no number'",
                "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json at f3186318ba: day_quality enum holds FLOW_UNRECONCILED and guard_state enum holds GRADED_DISAGREED as separate members",
                "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json in this worktree: avs.<window>.return_cumulative fold names the choice",
            ],
        },
        "disposition": "UNDER_INVESTIGATION",
    },
    {
        "title": "The DB94-6-AC1 prose says no custodian is named, and the base contract already uses the word custodian in five lines outside the 36 re-sourced members",
        "id": "IRPT_DASHBD-D2-W145-S2",
        "one_line": "The criterion's 'no vendor or custodian is named' cannot be read as a literal word test: the base contract carries the common noun custodian in five lines outside the 36 members, the grant names no edit to them, and none is a custodian's name.",
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "spec_asserts": "DB94-6-AC1 (order criterion line) and the Bounds state that no vendor or custodian is named in the contract, and the Worker Face says nothing in the file may name a vendor or a custodian.",
        "world_is": "The base contract at f3186318ba (0.1.0) contains the word custodian in five lines: 25 (the vendor_agnostic statement that nothing in the file names a vendor or a custodian), 74 (account_id, custodian account form), 1381 and 1390 (reasons citing the custodian account id), and 1519 (the account id spaces). None of them names a custodian. The checker's vendor pattern (black diamond, orion, schwab, commonwealth, bloomberg, ycharts, fidelity) does not include the word, and DB94-1-AC1 and DB94-6-AC1 both PASS. None of the 36 re-sourced folds contains the word, and those five lines lie outside the grant, so they were not edited.",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                "grep -n -i custodian over org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json at f3186318ba prints five lines: 25, 74, 1381, 1390, 1519",
                "p94_round94.py VENDOR pattern lists black diamond, blackdiamond, orion, schwab, commonwealth, bloomberg, ycharts, fidelity; custodian is not among them",
                "DB94-6-AC1 output in this worktree: 'DB94-6-AC1 PASS' rc 0 after the edit; the word custodian is absent from the 36 re-sourced folds",
            ],
        },
        "disposition": "UNDER_INVESTIGATION",
    },
]


def block(row):
    body = {
        "id": row["id"],
        "project": "IRPT_DASHBD",
        "fabric": "dell2",
        "surfaced_by": SURFACER,
        "surfaced_at": NOW,
        "one_line": row["one_line"],
        "class": row["class"],
        "hazard_standing": row["hazard_standing"],
        "spec_asserts": row["spec_asserts"],
        "world_is": row["world_is"],
        "grounding": row["grounding"],
        "disposition": row["disposition"],
    }
    text = json.dumps(body, indent=2, ensure_ascii=True)
    return "\n## %s -- %s\n\n```json\n%s\n```\n" % (row["id"], row["title"], text)


def main():
    chunk = "".join(block(r) for r in ROWS).encode("ascii")
    before = INV.read_bytes()
    assert before.endswith(b"```\n"), "investigation file does not end with a fenced block"
    with open(str(INV), "ab") as fh:
        fh.write(chunk)
    after = INV.read_bytes()
    print("appended %d bytes; file %d -> %d bytes; prefix preserved: %s; ascii chunk: %s" % (
        len(chunk), len(before), len(after), after[:len(before)] == before, all(b < 128 for b in chunk)))


if __name__ == "__main__":
    main()
