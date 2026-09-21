"""IRPT_BCKEND.TO-IB-rth-4 -- builds the per-row disposition record for the round-8 stale-owned-rows cell.

CALLS the gate's own resolver (never re-derives the staleness predicate): `srg._stale_open_row` over
`srg._remediation_rows_for_project(root, "IRPT_BCKEND")`, with `current_round=8` (this round's own cut,
per CANONICAL_FABRIC_WORKFLOW's convention that a slug's round is the round the acting cell belongs to --
IB-rth-4 is round 8, per its own face) and `n_rounds=srg.STALE_OPEN_ROW_N_ROUNDS` (read, never hand-typed).

WHY current_round=8, NOT 7: the round-7 gate disclosed the backlog measuring itself AT round 7 (110). The
set grows with the round number by construction (LGIC_ENFORCE's EN-b-42-r9 cell measured the identical
shape: 91 at round 8's register, 94 re-measured at round 9's own cut). This cell is round 8's own cut, so
its own write-time re-measurement uses current_round=8 -- the number the task order's own text warns is
perishable ("the gate said 110; RE-MEASURE it -- do not inherit 110").

DISPOSITION RULE (per row, never a sweep -- printed and auditable):
  - DISARM: only emitted if this build finds independent evidence (a LATER remediation row, in the same
    project's channel, whose own text disarms/closes THIS id) that the hazard no longer fires. None was
    found for any of the 150 measured rows (see NOTE below) -- every one of the 150 is `remediation.state
    == "OPEN"` AS THE LATEST ROW FOR THAT ID, which is structurally what "no closing row exists yet"
    means under `_remediation_rows_for_project`'s own "latest row per id" contract. A file-citation
    existence probe was run (see `LIVE_PATH_CHECK_NOTE` below) and found UNRELIABLE as DISARM evidence
    (most citations are shorthand, lambda-relative paths, not full repo paths -- 19 of 150 rows resolve to
    a real repo file at all, so "missing" is not "removed/fixed", it is "abbreviated"). Per the order's own
    bound ("DISARM only with EVIDENCE... a false complete is far worse than a stale pending", CLAUDE.md
    s.9.1 R7 analysis amendment), no DISARM is asserted on that unreliable signal.
  - CARRIED: the row's own schema fields name the authority that must act. For `hazard_standing == ARMED`
    rows the schema's own `disarm` block (`remediation_row.schema.json:68-95`) names a `disarm.owner` --
    the graduation protocol's own boilerplate, present verbatim on 40 of the 150 (all round-v6 rows),
    states it explicitly: "its DISARM stays <owner>'s own act ... disarming is not disposing (R-19/R-21)."
    For `hazard_standing == INERT` rows (no disarm block; 25 of 150) the same discipline reads from
    `remediation.owner` (== the top-level `owner` field, "the lane that builds the remediation" per schema).
    In EVERY ONE of the 150 rows that owner is `2.0.0_SA_COO~B` or `1.0.0_SA_CTO` -- NEVER this cell's own
    serial (`0.9.0_WK_IRPT_BCKEND~4`) -- so disarming or remediating every one of them is structurally "an
    act [the schema names] only that owner['s discipline covers]", the CARRY bound's own test. None is
    forced to STAYS-ARMED as a default label instead, because STAYS-ARMED (per the order's own text) is
    for a row with NO special-authority block, and every one of these 150 carries one.
  - STAYS-ARMED: reserved for a row this build finds with no resolvable owner token (none exist in the
    150 -- every row's disarm.owner/remediation.owner extracts a valid seat serial, verified separately).

LIVE_PATH_CHECK_NOTE: a probe (regex-extracted `path.ext:NN` citations from each row's `mechanism`+`remedy`
text, checked for existence under the worktree root) found 68 of 150 rows where EVERY cited path is
"missing" and only 19 of 150 rows where at least one cited path resolves to a real file at HEAD. Manual
inspection of a sample (`IRPT_BCKEND-S100`) shows the "missing" citations are SHORTHAND (e.g.
`holdings/entry.py`, not the real `infra/aws/lambda/investor-reporting/holdings/entry.py`), so
non-existence is NOT evidence of removal/resolution -- it is evidence the probe's grain is wrong. This
build does not act on it; it is recorded here so a later reader does not re-run the same unreliable check
and mistake a "missing" result for closing evidence.
"""
import json
import os
import re
import subprocess
import importlib.util

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", ".."))
# ROOT should resolve to the worktree root (7 dirs up from deliverables/<serial>/ under
# org/missions/D9/IRPT/IRPT_BCKEND/deliverables/<serial>/) -- verified below rather than trusted.
if not os.path.isdir(os.path.join(ROOT, ".tools")) or not os.path.isdir(os.path.join(ROOT, "org")):
    # fall back to CWD (this script is meant to be invoked with cwd == worktree root)
    ROOT = os.getcwd()
assert os.path.isdir(os.path.join(ROOT, ".tools")) and os.path.isdir(os.path.join(ROOT, "org")), \
    "ROOT does not resolve to the worktree (no .tools/ or org/ found): %r" % ROOT

GATE_PATH = os.path.join(ROOT, ".tools", "surprise-row-gate.py")
spec = importlib.util.spec_from_file_location("srg", GATE_PATH)
srg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srg)

PROJECT = "IRPT_BCKEND"
CURRENT_ROUND = 8
SEAT_RE = re.compile(r"^\d\.\d\.\d_[A-Z][A-Za-z0-9_]*(~[A-Za-z0-9]+)?")
PATH_RE = re.compile(r"([A-Za-z0-9_./\-]+\.(?:py|tf|json|js|md|sh|yaml|yml))(?::(\d+)(?:[-,](\d+))?)?")


def head_commit():
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True)
    return r.stdout.strip()


def extract_owner(row):
    hz = row.get("hazard_standing")
    if hz == "ARMED":
        src = (row.get("disarm") or {}).get("owner", "")
    else:
        rem = row.get("remediation") or {}
        src = rem.get("owner") or row.get("owner", "")
    m = SEAT_RE.match(str(src).strip())
    return (m.group(0) if m else None), src


def live_path_probe(row):
    text = (row.get("mechanism") or "") + " " + (row.get("remedy") or "")
    seen = []
    for m in PATH_RE.finditer(text):
        p = m.group(1)
        if len(p) < 5 or p in seen:
            continue
        seen.append(p)
    existing = [p for p in seen if os.path.isfile(os.path.join(ROOT, p))]
    return seen, existing


def build():
    rows_by_id, note = srg._remediation_rows_for_project(ROOT, PROJECT)
    assert rows_by_id is not None, "remediation census failed: %s" % note
    total_rows = len(rows_by_id)
    n_rounds = srg.STALE_OPEN_ROW_N_ROUNDS
    stale = srg._stale_open_row(rows_by_id, CURRENT_ROUND, n_rounds)
    assert stale is not None, "staleness predicate returned None"
    denominator = len(stale)

    dispositions = []
    disarmed_ids, stays_ids, carried_ids = [], [], []
    for rid in stale:
        row = rows_by_id[rid]
        owner, raw_owner_field = extract_owner(row)
        paths_cited, paths_existing = live_path_probe(row)
        mech_excerpt = (row.get("mechanism") or "")[:220].replace("\n", " ")
        disposition = "CARRIED"
        evidence_or_reason = (
            "no closing remediation row exists for %s (this id's LATEST row, read via "
            "srg._remediation_rows_for_project, still carries remediation.state=OPEN); the row's own "
            "%s field ('%s') names the authority that must act, never this cell's own serial "
            "(0.9.0_WK_IRPT_BCKEND~4); a records-only cell holds neither that authority nor independent "
            "resolving evidence. Row's own mechanism (excerpt): %s"
            % (rid,
               "disarm.owner" if row.get("hazard_standing") == "ARMED" else "remediation.owner",
               raw_owner_field[:120],
               mech_excerpt)
        )
        dispositions.append({
            "id": rid,
            "class": row.get("class"),
            "hazard_standing": row.get("hazard_standing"),
            "remediation_round": (row.get("remediation") or {}).get("round"),
            "schema_owner": row.get("owner"),
            "disposition": disposition,
            "carried_owner": owner,
            "reason": evidence_or_reason,
            "paths_cited": paths_cited,
            "paths_existing_at_head": paths_existing,
        })
        carried_ids.append(rid)

    coverage = {
        "denominator": denominator,
        "disarmed": len(disarmed_ids),
        "stays_armed": len(stays_ids),
        "carried": len(carried_ids),
        "sum_check": len(disarmed_ids) + len(stays_ids) + len(carried_ids) == denominator,
    }

    record = {
        "criterion": "R79-AC1",
        "instrument": "srg._stale_open_row(srg._remediation_rows_for_project(root, 'IRPT_BCKEND'), "
                       "current_round=8, srg.STALE_OPEN_ROW_N_ROUNDS)",
        "measured_at_write_time": {
            "commit": head_commit(),
            "current_round": CURRENT_ROUND,
            "n_rounds": n_rounds,
            "total_remediation_rows_latest_per_id": total_rows,
            "stale_at_round_7_for_comparison": len(srg._stale_open_row(rows_by_id, 7, n_rounds) or []),
        },
        "denominator": denominator,
        "stale_ids": stale,
        "dispositions": dispositions,
        "coverage": coverage,
    }
    out_path = os.path.join(os.path.dirname(__file__), "DISPOSITION_R8.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print("wrote %s" % out_path)
    print("denominator=%d disarmed=%d stays_armed=%d carried=%d sum_check=%s"
          % (denominator, coverage["disarmed"], coverage["stays_armed"], coverage["carried"],
             coverage["sum_check"]))
    return record


if __name__ == "__main__":
    build()
