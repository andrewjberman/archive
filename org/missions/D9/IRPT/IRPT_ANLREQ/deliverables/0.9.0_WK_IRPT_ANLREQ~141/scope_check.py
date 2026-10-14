"""AR333-y-AC3: the scope of this cell, read from git. Prints SCOPE-OK only when every changed path since the record's
`base` lies inside the grant, and the producer-list edit in resident_worker.py adds exactly one entry and touches no other
line except its comment block. Otherwise SCOPE-BAD <why>, exit 1. ASCII only.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]  # the worktree: deliverables/<serial> -> deliverables -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> ROOT
PKG = "infra/aws/lambda/investor-reporting/"
RECORD = HERE.parent / "r41" / "RESIDENT_R31_SOURCE_RECORD.json"
ORDER_DIR = "org/missions/D9/IRPT/IRPT_ANLREQ/"
GRANT_FILES = {
    PKG + "reports/build_resident_package.py",
    PKG + "ycharts/generate/resident_worker.py",
    PKG + "ycharts/generate/tests/test_resident_worker.py",
}
NEW_TEST_DIRS = (PKG + "reports/tests/", PKG + "ycharts/generate/tests/")
SOURCE = PKG + "ycharts/generate/resident_worker.py"
LIST_PREFIX = "OPAL_PRODUCER_PRINCIPALS = ("


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT)] + list(args), capture_output=True, encoding="utf-8",
                          errors="replace", check=True).stdout


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


if not RECORD.is_file():
    bad("RECORD_ABSENT " + str(RECORD))
base = json.loads(RECORD.read_text(encoding="utf-8"))["base"]
print("BASE " + base)
print("HEAD " + git("rev-parse", "HEAD").strip())

status = [ln.split("\t", 1) for ln in git("diff", "--name-status", base, "HEAD").splitlines() if ln.strip()]
print("CHANGED %d path(s) since base" % len(status))
for state, path in status:
    print("  " + state + " " + path)
    if path.startswith(ORDER_DIR):
        continue
    if path in GRANT_FILES:
        continue
    if path.startswith(NEW_TEST_DIRS) and state == "A" and Path(path).name.startswith("test_"):
        continue
    bad("OUTSIDE_GRANT " + path)

# The one list edit: exactly one entry added, and every changed line is the list line or a comment line.
hunks = git("diff", "-U0", base, "HEAD", "--", SOURCE).splitlines()
removed = [ln[1:] for ln in hunks if ln.startswith("-") and not ln.startswith("---")]
added = [ln[1:] for ln in hunks if ln.startswith("+") and not ln.startswith("+++")]
for ln in removed + added:
    if not (ln.lstrip().startswith("#") or ln.startswith(LIST_PREFIX)):
        bad("NON_COMMENT_HUNK " + ln[:120])
old_list = [ln for ln in removed if ln.startswith(LIST_PREFIX)]
new_list = [ln for ln in added if ln.startswith(LIST_PREFIX)]
if len(old_list) != 1 or len(new_list) != 1:
    bad("LIST_LINE_COUNT old=%d new=%d" % (len(old_list), len(new_list)))


def entries(line):
    body = line[len(LIST_PREFIX):].rsplit(")", 1)[0]
    return [item.strip().strip('"').strip("'") for item in body.split(",") if item.strip()]


old_entries, new_entries = entries(old_list[0]), entries(new_list[0])
print("LIST old=%r new=%r" % (old_entries, new_entries))
if [e for e in new_entries if e not in old_entries] != ["fwd1-staff-r41a@opal.invalid"] or \
        [e for e in old_entries if e not in new_entries]:
    bad("LIST_NOT_ONE_ADDED old=%r new=%r" % (old_entries, new_entries))
print("SCOPE-OK")
sys.exit(0)
