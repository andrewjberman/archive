#!/usr/bin/env python3
"""battery_ib_rth_3.py -- IRPT_BCKEND.TO-IB-rth-3 status-word hygiene battery.

R78-AC1: "the status-word count and the gate's proof-based resolver AGREE for
IRPT_BCKEND, OR the residual is EXACTLY the faces (b) left NON-TERMINAL by the
honest-word rule, each NAMED with its reason." The cell PASSES by NAMING the
residual, never by flipping a failing order to `complete`.

THIS RUN'S FINDING (CTO ruling 98990/98993, the per-order honest-word rule --
no uniform terminal value): of the seven orders the resolver names
terminal-by-proof with a non-terminal status word (IB-rt-6, rtf-3, rtf-4,
rtf-7, rtf-10, rtf-12, rtf-14), NONE qualifies for `complete` (no order's own
bound expressly permits completion with a disclosed FAIL -- the OG-r-1/R-58
shape is present in none of the seven; three of the seven's own proof text
literally says "the order stays open") and NONE qualifies for `superseded`
(no later round's decomp cell names any of the seven in a `supersedes`
column -- rounds 3-8 read directly -- and no later order's own text claims to
re-cut one of them; a project-wide text search for "supersed" against each id
corroborates). So the honest word for all seven is LEFT NON-TERMINAL: the
residual is the same seven, unchanged, each with a one-line ISSUER-CORRECTION
reason appended to its own <status> field (committed at 023b4697df) --
the word itself untouched.

Invocation: `timeout 600 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rth_3.py`
run from the repo root (the worktree). No network. No source/build/deploy.
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys

ROOT = "."
CODE = "IRPT_BCKEND"

EXPECTED_CELL_IDS = ["IB-rt-6", "IB-rtf-3", "IB-rtf-4", "IB-rtf-7", "IB-rtf-10", "IB-rtf-12", "IB-rtf-14"]

TASK_ORDERS_DIR = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders"

ISSUER_MARKER = "ISSUER-CORRECTION (round 8 IB-rth-3, ruling 98990/98993):"

# Basename stem -> its own AC id, for the table (read from the proof instances
# earlier in this drive; restated here as a cross-check, not a new source).
KNOWN_AC = {
    "IB-rt-6": "RT6-AC1",
    "IB-rtf-3": "R60-AC1",
    "IB-rtf-4": "R61-AC1",
    "IB-rtf-7": "R64-AC1",
    "IB-rtf-10": "R67-AC1",
    "IB-rtf-12": "R69-AC1",
    "IB-rtf-14": "R71-AC1",
}


def load_gate():
    spec = importlib.util.spec_from_file_location("srg", os.path.join(ROOT, ".tools", "surprise-row-gate.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolver_head_commit():
    out = subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    return out.stdout.strip()


def resolver_vintage():
    out = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", ".tools/surprise-row-gate.py"],
        cwd=ROOT, capture_output=True, text=True,
    )
    return out.stdout.strip()


CELL_ID_RE = re.compile(r"TO-(IB-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\.")


def cell_id_from_basename(basename: str) -> str:
    m = CELL_ID_RE.search(basename)
    if not m:
        return "<unparsed>"
    return m.group(1)


def find_face_path(cell_id: str) -> str | None:
    for fn in os.listdir(os.path.join(ROOT, TASK_ORDERS_DIR)):
        if fn.startswith(f"IRPT_BCKEND.TO-{cell_id}.") and fn.endswith(".md"):
            return os.path.join(TASK_ORDERS_DIR, fn)
    return None


def read_status_word_and_reason(face_path: str) -> tuple[str, str]:
    with open(os.path.join(ROOT, face_path), "r", encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"<status>(.*?)</status>", text, re.S)
    if not m:
        return "<no status tag>", ""
    status_text = m.group(1)
    word = status_text.strip().split()[0].rstrip(".,;:").lower()
    if ISSUER_MARKER in status_text:
        reason = status_text.split(ISSUER_MARKER, 1)[1].strip()
    else:
        reason = "<no ISSUER-CORRECTION reason found>"
    return word, reason


TERMINAL_WORDS = ("complete", "completed", "closed", "done", "superseded", "cancelled", "canceled", "withdrawn")


def main() -> int:
    gate = load_gate()
    open_ids, total, note = gate._open_tos_for_project(ROOT, CODE)  # noqa: SLF001
    if open_ids is None:
        print("FAIL: resolver could not run: %s" % note)
        return 1

    proven_labels = []
    if note:
        # note = "<n> order(s) terminal by a VALID proof-of-spec instance at HEAD ... : <label1>, <label2>, ..."
        after_colon = note.split(": ", 1)[1] if ": " in note else ""
        proven_labels = [x.strip() for x in after_colon.split(", ") if x.strip()]

    print("=== RESOLVER STATE (HEAD %s, .tools/surprise-row-gate.py vintage %s) ===" % (
        resolver_head_commit(), resolver_vintage()))
    print("total order(s) on both roots (denominator): %d" % total)
    print("open_ids (truly open, non-terminal, no valid proof): %d of %d" % (len(open_ids or []), total))
    print("proven (terminal-by-proof, status word non-terminal): %d of %d" % (len(proven_labels), total))
    print()

    resolver_cell_ids = set()
    for label in proven_labels:
        basename = label.split(" [", 1)[0]
        cid = cell_id_from_basename(basename)
        resolver_cell_ids.add(cid)

    expected_set = set(EXPECTED_CELL_IDS)
    print("=== PER-ORDER DISPOSITION TABLE (denominator: %d of %d expected cells) ===" % (
        len(EXPECTED_CELL_IDS), len(EXPECTED_CELL_IDS)))
    print("%-10s %-10s %-10s %-14s %s" % ("cell", "AC id", "status", "in-resolver?", "reason (from face's own <status>)"))
    rows_ok = 0
    for cid in EXPECTED_CELL_IDS:
        face = find_face_path(cid)
        if face is None:
            print("%-10s %-10s %-10s %-14s FACE NOT FOUND" % (cid, KNOWN_AC.get(cid, "?"), "?", "?"))
            continue
        word, reason = read_status_word_and_reason(face)
        in_resolver = cid in resolver_cell_ids
        is_terminal_word = word in TERMINAL_WORDS
        ok = (not is_terminal_word) and in_resolver and reason and "<no ISSUER-CORRECTION" not in reason
        if ok:
            rows_ok += 1
        print("%-10s %-10s %-10s %-14s %s" % (
            cid, KNOWN_AC.get(cid, "?"), word, str(in_resolver), reason[:160]))

    print()
    print("rows honest (non-terminal word, present in resolver's proven set, reason recorded): %d of %d" % (
        rows_ok, len(EXPECTED_CELL_IDS)))

    resolver_matches_expected = resolver_cell_ids == expected_set
    print()
    print("resolver proven-set == expected 7-cell set: %s" % resolver_matches_expected)
    if not resolver_matches_expected:
        print("  resolver has, expected does not: %s" % sorted(resolver_cell_ids - expected_set))
        print("  expected has, resolver does not: %s" % sorted(expected_set - resolver_cell_ids))

    all_honest = rows_ok == len(EXPECTED_CELL_IDS)
    verdict = resolver_matches_expected and all_honest

    print()
    print("=== VERDICT ===")
    if verdict:
        print("R78-AC1: PASS -- the residual is EXACTLY the 7 faces left NON-TERMINAL by the honest-word")
        print("rule, each named with its reason; the resolver's own proven-set agrees with that residual.")
        print("IBR78-STATUS-WORD-AND-PROOF-RESOLVER-AGREE")
        return 0
    print("R78-AC1: FAIL -- residual/resolver mismatch or a missing/unhonest reason row.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
