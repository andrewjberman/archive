#!/usr/bin/env python
"""channel-commit-guard.py -- run this IMMEDIATELY BEFORE committing a surprise-channel file.

WHY IT EXISTS, and the reason is a measured failure of its own predecessor rather than a hypothetical.
On 2026-09-03 at ~17:53Z this seat's channel-append script ran a correct foreign-row guard AT APPEND
TIME, then invoked safe-commit; a peer's row (NFRA_OPSEC202609-Z-S56, 0.7.0_AE_CloudOps~Z) landed in
the shared worktree in the gap between the two acts, and the pathspec swept it into commit 35ca1debfb
under this seat's author line. Content was intact and self-attributing, so no reader was misled; what
was lost was the peer's own commit message and its reasoning.

  >> A GUARD HAS A DIRECTION AND A TIME, AND BOTH CAN BE WRONG INDEPENDENTLY. <<

The predecessor was right about direction ("is anything here not mine?") and scheduled at the wrong
moment. The rule this encodes: IF A GUARD'S PREDICATE CAN BE FALSIFIED BY ANYTHING THAT HAPPENS
BETWEEN THE CHECK AND THE ACT IT PROTECTS, THE GUARD BELONGS AT THE ACT.

COST: one `git show HEAD:<path>` plus one file read, ~100 ms, per channel commit.

NON-APPLICATION, stated so this does not creep:
  * It does NOT check content, schema or hazard fields -- `.tools/surprise-row-gate.py` owns those and
    runs at commit for every seat. This only answers "whose rows am I about to commit?".
  * It is NOT a block on committing a peer's row. Sometimes that is correct (a peer has gone, the row
    must land). It EXITS 3 so the caller decides, and prints what a truthful commit message must say.
  * It does not fire on the MIRROR of its own failure. A guard asking "am I committing someone else's
    row?" structurally CANNOT fire when someone else commits mine (0.7.0_AE_CloudOps~Z's framing,
    2026-09-03: "a class closed on one direction is not closed"). That direction needs a different
    remedy and this file is not it.

USAGE:  python org/tier1_exec/2.0.0_SA_COO/tools/channel-commit-guard.py <channel-file-rel-path> <my-serial>
EXIT:   0 = only your own new rows (or no new rows)   2 = usage/parse error   3 = FOREIGN ROWS PRESENT
"""
import json
import re
import subprocess
import sys

BLOCK = re.compile(r"```json\n(\[.*?\n\])\n```", re.S)


def rows(text):
    m = BLOCK.search(text)
    if not m:
        raise ValueError("no fenced json array found")
    return json.loads(m.group(1))


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip().splitlines()[-3])
        return 2
    rel, serial = sys.argv[1], sys.argv[2]

    try:
        worktree = rows(open(rel, "rb").read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 -- a parse failure must be loud, not silent
        print("GUARD: cannot parse worktree copy of %s: %s" % (rel, exc))
        return 2

    shown = subprocess.run(["git", "show", "HEAD:" + rel], capture_output=True)
    if shown.returncode != 0:
        head = []  # the file is new at HEAD; every row is new
    else:
        try:
            head = rows(shown.stdout.decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            print("GUARD: cannot parse HEAD copy of %s: %s" % (rel, exc))
            return 2

    head_ids = {r.get("id") for r in head}
    new = [r for r in worktree if r.get("id") not in head_ids]
    mine = [r for r in new if serial in (r.get("surfaced_by") or "")]
    foreign = [r for r in new if r not in mine]

    print("channel-commit-guard: %s" % rel)
    print("  rows at HEAD %d | worktree %d | NEW %d (mine %d, foreign %d)"
          % (len(head), len(worktree), len(new), len(mine), len(foreign)))

    if not foreign:
        print("  OK: every new row self-attributes to %s." % serial)
        return 0

    print("  FOREIGN ROWS PRESENT -- this commit would carry rows this seat did not author:")
    for r in foreign:
        author = (r.get("surfaced_by") or "<no surfaced_by>").split("(")[0].strip()
        print("    %-30s by %s" % (r.get("id"), author or "<unattributed>"))
    print("  DECIDE, do not default:")
    print("    (a) wait for that seat to commit its own row, re-run this, then commit; OR")
    print("    (b) commit deliberately -- and then the commit message MUST name the foreign rows and")
    print("        their authors, and the affected seat MUST be told unprompted. A commit message that")
    print("        claims the append refuses foreign rows while carrying one is the actual defect.")
    return 3


if __name__ == "__main__":
    sys.exit(main())
