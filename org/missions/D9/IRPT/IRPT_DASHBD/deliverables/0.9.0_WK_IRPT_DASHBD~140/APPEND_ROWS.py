"""Append the worker's surprise rows to the investigation file as raw bytes (never re-encoded).

Usage: python -I append_rows.py <investigation_file> <surfaced_at_utc>
Each row is one fenced json block under a heading, the form the existing rows use.
"""
import json
import sys
from pathlib import Path

INV = Path(sys.argv[1])
NOW = sys.argv[2]
SURFACER = "0.9.0_WK_IRPT_DASHBD~140"

ROWS = [
    {
        "title": "The FWD-20 figure map is filed under the older FWD-9 numbering in the CUSTDY tree, not under FWD-20; it is folded in",
        "id": "IRPT_DASHBD-D2-W140-S1",
        "one_line": "A FWD-20 search of the IRPT_CUSTDY and IRPT_YCDGEN trees does not find the figure map; the map is the CUSTDY field map of one 49 Financial report, filed under the pre-consolidation FWD-9 numbering, and it was folded in.",
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "spec_asserts": "The order directs the worker to look for the FWD-20 figure map with comp-find --files 'FWD-20' over the mission trees, and in the IRPT_CUSTDY and IRPT_YCDGEN trees, and to set fwd20_map_folded true when the map is found there.",
        "world_is": "The FWD-20 search finds no file in IRPT_CUSTDY (0 hits across 79 files) and only prose hits in the IRPT_YCDGEN PRD. The map exists at org/missions/D9/IRPT/IRPT_CUSTDY/deliverables/0.9.0_WK_IRPT_CUSTDY~17/ as BD_FIELD_MAP_CU-g-3.md and .json: the field map of one 49 Financial report, 49 fields and 70 rows, 23 rows MISSING with their reasons. The PRD's FWD-20 SOURCE line records that this outcome was IRPT_CUSTDY FWD-9 before the round consolidation. The map was folded in, and fwd20_map_folded is true; its MISSING reasons are carried into the contract's absent reasons.",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                "comp-find 'FWD-20' org/missions/D9/IRPT/IRPT_CUSTDY returned 0 hit(s) across 79 file(s) in corpus=all",
                "comp-find --files 'map' org/missions/D9/IRPT/IRPT_CUSTDY lists deliverables/0.9.0_WK_IRPT_CUSTDY~17/BD_FIELD_MAP_CU-g-3.md and .json",
                "org/missions/D9/IRPT/IRPT_DASHBD/prd/IRPT_DASHBD_PRD.md at base ea59dfcdec, FWD-20 SOURCE line: was IRPT_CUSTDY FWD-9",
            ],
        },
        "disposition": "UNDER_INVESTIGATION",
    },
    {
        "title": "The round-94 checker tests a source field by substring over the sibling's raw text, not by the field being a column or key",
        "id": "IRPT_DASHBD-D2-W140-S2",
        "one_line": "DB94-1-AC1 asks that each source field really occur in its sibling contract; the checker's test is a substring test over the file's raw text, so a field name that appears only in prose would pass.",
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "spec_asserts": "DB94-1-AC1 requires a source whose field really occurs in the named sibling contract.",
        "world_is": "The checker tests s['field'] in the sibling file's text (p94_round94.py line 131 at base ea59dfcdec), which is a substring test over raw bytes and does not check that the name is a column or key of the sibling. The verdict PASS therefore does not, by itself, establish semantic occurrence. This cell checked each source field by reading the sibling's column or key list, and every source field used is a column or key of the named sibling.",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r94/p94_round94.py at base ea59dfcdec line 131: need(s['field'] in sp.read_bytes().decode('utf-8'), ...)",
                "the eight sibling contracts under org/standards/ at base ea59dfcdec, read for their column and key lists",
            ],
        },
        "disposition": "UNDER_INVESTIGATION",
    },
    {
        "title": "The baseline says since inception is annualized past a year, but its value-summary rows read Return (Cumulative) in every column",
        "id": "IRPT_DASHBD-D2-W140-S3",
        "one_line": "The baseline's conventions note and its value-summary tables disagree on whether the since-inception return is annualized; no sibling carries an annualized figure, so the contract prints it cumulative and records the question as an open change.",
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "spec_asserts": "The baseline's conventions note says returns are cumulative for windows under a year and since-inception is annualized past a year, footnote 1.",
        "world_is": "The Portfolio Value Summary and Account Value Summary tables print the row 'Return (Cumulative)' in every column, including the since-inception column, and footnote 1 (annualized return) appears only under the Holdings Overview table. The served since-inception figure is cumulative and no sibling carries an annualized figure. The contract prints since-inception cumulative and lists annualization as an open change until a ruling settles the baseline's convention.",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                "the round-94 baseline structure note held in the CTO's round-94 deliverables (conventions section and the two value-summary table rows), read at base ea59dfcdec",
                "org/standards/IRPT_DASHBD_CLIENT_SUMMARY_CONTRACT.json at base ea59dfcdec: windows is cumulative geometric link; no annualized field",
            ],
        },
        "disposition": "UNDER_INVESTIGATION",
    },
    {
        "title": "The client summary holds issued opaque account ids while the account tables key on the custodian account id, and no sibling maps one to the other",
        "id": "IRPT_DASHBD-D2-W140-S4",
        "one_line": "The cover's masked account numbers need the custodian account id, which the account tables carry; the client summary carries only issued opaque ids, and no sibling maps one id space to the other.",
        "class": "OBSERVATION",
        "hazard_standing": "INERT",
        "spec_asserts": "The client summary is the report's read surface, and the report's cover shows each account as its registration name and last four digits (XXXX followed by the last four characters).",
        "world_is": "The client summary's account_id is 'the issued opaque account id ... the id space the viewer's scope is tested in' (IRPT_DASHBD_CLIENT_SUMMARY_CONTRACT.json, summary.account_entry.fields.account_id), while the account tables key on the custodian account id in the declaration's account form (account_id in the activity, return and lot contracts). No sibling in org/standards/ maps the issued id to the custodian id, and the summary holds no custodian number by design. The cover's masked number therefore cannot be read from the summary, and the account list is ABSENT with its reason; the sample builder will need the mapping before the cover can carry it.",
        "grounding": {
            "status": "GROUNDED",
            "evidence": [
                "org/standards/IRPT_DASHBD_CLIENT_SUMMARY_CONTRACT.json at base ea59dfcdec: account_id described as the issued opaque account id; shape says ids only, no custodian account number",
                "org/standards/IRPT_DASHBD_ACCOUNT_ACTIVITY_DAILY_CONTRACT.json at base ea59dfcdec: account_id described as the custodian account id in the declaration's account form",
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
    with open(str(INV), "ab") as fh:
        fh.write(chunk)
    after = INV.read_bytes()
    print("appended %d bytes; file %d -> %d bytes; prefix preserved: %s" % (
        len(chunk), len(before), len(after), after[:len(before)] == before))


if __name__ == "__main__":
    main()
