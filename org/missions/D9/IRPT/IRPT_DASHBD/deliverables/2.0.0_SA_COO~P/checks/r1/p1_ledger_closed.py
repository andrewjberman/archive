"""IRPT_DASHBD round 1 -- a cell's change-management ledger entry (CLAUDE.md NEVER-2) exists, is CLOSED, and its sentinel is gone.

Usage: python p1_ledger_closed.py <worktree root> <slug> <criterion id>
Pass line: <criterion id> PASS. Base (at the cut): FAIL -- no entry for the slug exists.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
slug = sys.argv[2]
cid = sys.argv[3]


def fail(msg):
    print("%s FAIL: %s" % (cid, msg))
    sys.exit(1)


entries = sorted((root / "org/critical_paths/change_management").glob("*_%s_deploy_completion.md" % slug))
if not entries:
    fail("no change_management entry for slug %s" % slug)
entry = entries[-1]
text = entry.read_text(encoding="utf-8")
m = re.search(r"^\*\*Status:\*\*\s*(.+)$", text, re.M)
if not m or not m.group(1).strip().upper().startswith("CLOSED"):
    fail("%s Status line: %r" % (entry.name, m.group(1) if m else None))
legs = re.findall(r"^\| (\w+) \| \w+ \|.*\| (OPEN|CLOSED[^|]*) \|$", text, re.M)
if not legs:
    fail("no manifest legs parsed in %s" % entry.name)
open_legs = [lid for lid, state in legs if state.strip().upper() == "OPEN"]
if open_legs:
    fail("legs still OPEN: %s" % ", ".join(open_legs))
sentinel = root / "org/critical_paths/.open_deploys" / ("%s.json" % slug)
if sentinel.exists():
    fail("sentinel still present: %s" % sentinel)
print("  %s: CLOSED, %d legs closed, sentinel absent" % (entry.name, len(legs)))
print("%s PASS" % cid)
