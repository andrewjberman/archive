#!/usr/bin/env python3
"""AR330-y-AC3 (IRPT_ANLREQ.TO-AR-y-330): the scope of the branch. Prints SCOPE-OK only when `git diff --name-only <base>
HEAD` lists only layout_overview.py, the new test file and paths under org/missions/D9/IRPT/IRPT_ANLREQ/, AND the
layout_overview.py diff against <base> is ONE hunk that removes exactly the base constant lines and adds exactly the
comment and the label constant. Otherwise SCOPE-BAD <why>, exit 1. <base> is the `base` field of the record JSON."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]  # deliverables/<serial>/ -> ... -> worktree root
SERIAL_DIR = HERE.parent
RECORD = SERIAL_DIR / "r41" / "DISCLAIMER_PENDING_LABEL_RECORD.json"
REL = "infra/aws/lambda/investor-reporting/ycharts/research/layout_overview.py"
NEW_TEST = "infra/aws/lambda/investor-reporting/ycharts/research/tests/test_commentary_disclaimer_pending.py"
ORDER_PREFIX = "org/missions/D9/IRPT/IRPT_ANLREQ/"
EXPECT_ADDED = [
    "# The approved disclaimer wording is held for Andrew (call 095e); this visible label stands in for it.",
    "# The approved wording is a release gate for any client delivery.",
    'COMMENTARY_DISCLAIMER = "[Opal disclaimer pending approval]"',
]


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT)] + list(args), capture_output=True, text=True, timeout=60,
                          check=True).stdout


def bad(why):
    print("SCOPE-BAD %s" % why)
    return 1


def main():
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    base = record["base"]
    print("BASE %s" % base)
    names = [n for n in git("diff", "--name-only", base, "HEAD").splitlines() if n.strip()]
    print("CHANGED-PATHS (%d):" % len(names))
    for n in names:
        print("  " + n)
    for n in names:
        if n not in (REL, NEW_TEST) and not n.startswith(ORDER_PREFIX):
            return bad("path outside the grant: %s" % n)
    if REL not in names or NEW_TEST not in names:
        return bad("the source or the new test file is not in the diff")
    diff = git("diff", "-U0", base, "HEAD", "--", REL)
    hunks = [ln for ln in diff.splitlines() if ln.startswith("@@")]
    if len(hunks) != 1:
        return bad("layout_overview.py has %d hunks, expected 1" % len(hunks))
    removed = [ln[1:] for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    base_text = git("show", "%s:%s" % (base, REL)).splitlines()
    start = [i for i, ln in enumerate(base_text) if ln.startswith("COMMENTARY_DISCLAIMER = (")]
    if len(start) != 1:
        return bad("base constant not found once")
    end = start[0]
    while 'ratification.")' not in base_text[end]:
        end += 1
    expect_removed = base_text[start[0]:end + 1]
    if removed != expect_removed:
        return bad("removed lines are not exactly the base constant: %r" % removed)
    if added != EXPECT_ADDED:
        return bad("added lines are not exactly the comment and the label constant: %r" % added)
    print("HUNKS 1; REMOVED %d line(s) = base constant; ADDED %d line(s) = comment + label" % (
        len(removed), len(added)))
    print("SCOPE-OK %d path(s) in the diff against %s" % (len(names), base))
    return 0


if __name__ == "__main__":
    sys.exit(main())
