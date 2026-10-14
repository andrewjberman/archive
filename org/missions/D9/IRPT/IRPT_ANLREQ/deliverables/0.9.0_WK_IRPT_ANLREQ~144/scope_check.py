"""TO-AR-y-338 criterion AR338-y-AC3: the build was BUILD ONLY and touched nothing outside its grant. Offline, read-only.

Prints `SCOPE-OK ...` only when: `git diff --name-only <base> HEAD` (base = the parent of this worker's first commit, printed)
lists only paths under org/missions/D9/IRPT/IRPT_ANLREQ/; `git status --porcelain -- infra` of this worktree is empty; and
the staged artifacts all live under C:/dev/irpt-release-r31/ with none inside the repository. Otherwise `SCOPE-BAD <why>`,
exit 1. ASCII only.
"""
import os
import subprocess
import sys

DL = os.path.dirname(os.path.abspath(__file__))
WT = os.path.abspath(os.path.join(DL, "..", "..", "..", "..", "..", "..", ".."))
ORDER_BASE = "f117aac140"
PREFIX = "org/missions/D9/IRPT/IRPT_ANLREQ/"
STAGE = "C:/dev/irpt-release-r31"
STAGED = [
    STAGE + "/irpt-resident-0485393f3a-r31.tar.gz",
    STAGE + "/irpt-resident-0485393f3a-r31.package.SHA256SUMS",
    STAGE + "/build_a",
    STAGE + "/build_b",
]


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


def git(*args):
    proc = subprocess.run(["git", "-C", WT] + list(args), capture_output=True)
    if proc.returncode != 0:
        bad("git %s rc=%d" % (" ".join(args), proc.returncode))
    return proc.stdout.decode("utf-8")


first = git("rev-list", "--reverse", ORDER_BASE + "..HEAD").split()
if not first:
    bad("no commit of this worker after the order commit %s" % ORDER_BASE)
base = git("rev-parse", first[0] + "^").strip()
changed = [p for p in git("diff", "--name-only", base, "HEAD").split("\n") if p.strip()]
outside = [p for p in changed if not p.startswith(PREFIX)]
if outside:
    bad("committed paths outside %s: %s" % (PREFIX, outside[:5]))
infra = git("status", "--porcelain", "--", "infra").strip()
if infra:
    bad("product tree infra/ is not clean: %s" % infra[:200])
for path in STAGED:
    if not os.path.exists(path):
        bad("staged artifact missing: %s" % path)
    if os.path.commonpath([os.path.abspath(path).lower(), WT.lower()]) == WT.lower():
        bad("staged artifact inside the repository: %s" % path)
tracked = git("ls-files").split("\n")
stray = [p for p in tracked if "irpt-resident-0485393f3a-r31" in p]
if stray:
    bad("a release-31 artifact is tracked in the repository: %s" % stray[:3])
print("SCOPE-OK base %s, %d committed paths, all under %s; infra/ clean; %d staged artifacts outside the repository under %s/"
      % (base[:12], len(changed), PREFIX, len(STAGED), STAGE))
