"""AR327-y-AC3 (IRPT_ANLREQ AR-y-327): the files this order changed lie inside its grant. `base` is read from the record
r41/COMMENTARY_PDF_RENDERER_RECORD.json and checked to be the parent of the order's first commit. Lists `git diff --name-only
<base> HEAD` in the worktree. Prints SCOPE-OK only when every changed path is one of the three producer and packager and
layout modules under ycharts/research, a file under ycharts/research/tests/, or a path under org/missions/D9/IRPT/IRPT_ANLREQ/.
Otherwise SCOPE-BAD <why> and exit 1."""
import json
import subprocess
import sys
from pathlib import Path

DELIV = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~134"
RECORD = DELIV + "/r41/COMMENTARY_PDF_RENDERER_RECORD.json"
RESEARCH = "infra/aws/lambda/investor-reporting/ycharts/research"
ALLOWED_EXACT = {RESEARCH + "/layout_overview.py", RESEARCH + "/opal_producer.py", RESEARCH + "/opal_packager.py"}
ALLOWED_PREFIX = (RESEARCH + "/tests/", "org/missions/D9/IRPT/IRPT_ANLREQ/")


def root():
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / ".tools").is_dir() and (p / "org").is_dir():
            return p
    print("SCOPE-BAD root with .tools and org not found above " + str(here))
    sys.exit(1)


def git(r, *args):
    proc = subprocess.run(["git", "-C", str(r)] + list(args), capture_output=True, text=True, timeout=60)
    return proc.returncode, proc.stdout.strip()


def main():
    r = root()
    rec = json.loads((r / RECORD).read_text(encoding="utf-8"))
    base, first = rec["base"], rec["first_commit"]
    rc, parent = git(r, "rev-parse", first + "^")
    print("BASE " + base + " (record)")
    print("FIRST-COMMIT-PARENT " + parent + " (git rev-parse " + first + "^)")
    if rc != 0 or parent != base:
        print("SCOPE-BAD base is not the parent of the first commit of this order")
        return 1
    rc, out = git(r, "diff", "--name-only", base, "HEAD")
    if rc != 0:
        print("SCOPE-BAD git diff rc=%d" % rc)
        return 1
    names = [n for n in out.splitlines() if n.strip()]
    print("CHANGED %d path(s) from %s to HEAD" % (len(names), base))
    for n in names:
        print("  " + n)
    if not names:
        print("SCOPE-BAD no change from the base")
        return 1
    bad = [n for n in names if not (n in ALLOWED_EXACT or n.startswith(ALLOWED_PREFIX))]
    if bad:
        print("SCOPE-BAD outside the grant: " + ", ".join(bad))
        return 1
    print("SCOPE-OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
