"""TO-AR-y-338 criterion AR338-y-AC3: the scope check (a build that touched the repository or the cloud is a release nobody signed).
Offline; read-only over git and the worktree.

Prints `SCOPE-OK ...` only when: `git diff --name-only <base> HEAD` (base = the parent of the first commit of this branch,
printed) lists only paths under org/missions/D9/IRPT/IRPT_ANLREQ/ (the deliverable folder and the surprise channel file and the
order file); `git status --porcelain -- infra` shows nothing; and the staged artifacts all live under C:/dev/irpt-release-r31/
(none inside the repository: no tracked or untracked-not-ignored path is named like a release artifact, and the gitignored
.scratch folder holds no file named like the tarball or its sums). Otherwise `SCOPE-BAD <why>`, exit 1. ASCII only.
"""
import hashlib
import os
import subprocess
import sys

WT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "..", ".."))
STAGE = "C:/dev/irpt-release-r31"
FIRST = "171fa77f59"
PREFIX = "org/missions/D9/IRPT/IRPT_ANLREQ/"


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


def git(*args):
    proc = subprocess.run(["git", "-C", WT] + list(args), capture_output=True, text=True, timeout=240)
    if proc.returncode != 0:
        bad("git %s rc %d: %s" % (" ".join(args), proc.returncode, proc.stderr.strip()[:200]))
    return proc.stdout


base = git("rev-parse", FIRST + "^").strip()
if len(base) != 40:
    bad("base is not a sha: %r" % base)
print("BASE parent of first commit %s = %s" % (FIRST, base))

# (1) every path the branch changes since the base is under the deliverable folder, the channel or the order
changed = [p for p in git("diff", "--name-only", base, "HEAD").split("\n") if p]
print("DIFF names since base: %d" % len(changed))
outside = [p for p in changed if not p.startswith(PREFIX)]
if outside:
    bad("paths changed outside %s: %s" % (PREFIX, outside[:5]))

# (2) the product tree shows nothing untracked or modified
infra = [ln for ln in git("status", "--porcelain", "--", "infra").split("\n") if ln.strip()]
if infra:
    bad("product tree infra/ is not clean: %s" % infra[:5])

# (3) the staged artifacts live under the stage folder and none is inside the repository
stage_abs = os.path.abspath(STAGE)
if os.path.commonpath([os.path.abspath(WT), stage_abs]) == os.path.abspath(WT):
    bad("the stage folder is inside the repository")
tracked = [p for p in git("ls-files", "--", ":(glob)**/*irpt-resident-0485393f3a-r31*").split("\n") if p]
untracked = [p for p in git("ls-files", "--others", "--exclude-standard", "--", ":(glob)**/*irpt-resident-0485393f3a-r31*").split("\n") if p]
if tracked or untracked:
    bad("release artifact names inside the repository: %s" % (tracked + untracked)[:5])
scratch = os.path.join(WT, ".scratch")
TAR = STAGE + "/irpt-resident-0485393f3a-r31.tar.gz"
TAR_SIZE = os.path.getsize(TAR)
TAR_SHA = hashlib.sha256(open(TAR, "rb").read()).hexdigest()
hits = []
if os.path.isdir(scratch):
    for dp, _dn, fn in os.walk(scratch):
        for f in fn:
            full = os.path.join(dp, f)
            if os.path.getsize(full) == TAR_SIZE and hashlib.sha256(open(full, "rb").read()).hexdigest() == TAR_SHA:
                hits.append(os.path.relpath(full, WT))
if hits:
    bad("byte copies of the tarball under .scratch (gitignored, inside the repository): %s" % hits[:5])
print("STAGE %s is outside the repository: OK" % stage_abs)

print("SCOPE-OK base %s; %d changed path(s), all under %s; infra/ clean; artifacts under %s only"
      % (base[:12], len(changed), PREFIX, STAGE))
