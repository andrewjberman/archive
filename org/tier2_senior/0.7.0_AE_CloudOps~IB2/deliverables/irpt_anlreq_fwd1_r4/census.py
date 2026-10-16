"""Window 4 step 1: every live worktree's org/critical_paths/.open_deploys/ read, the denominator printed, any entry whose ledger is NOT closed and which names the
resident, either Lambda, the ticket service, the users table or the intake store listed. READ ONLY. Exit 3 when one is found (other than this run's own slug)."""
import glob
import re
import subprocess
import sys

OWN = "irpt-fwd1-run4-20261016"
TERMS = re.compile(r"irpt-analysis-resident|irpt-resident|resident host|irpt-ycharts-generate|irpt-status|opal-ticket-api|ticket service|ticket-api|opal-users-v2|users table|users-v2|intake", re.I)


def run(*a):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


wts = [ln[9:] for ln in run("git", "worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
seen = {}
files = 0
for wt in wts:
    for n in [x for x in run("git", "-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
        files += 1
        seen.setdefault(n.rsplit("/", 1)[-1].rsplit(".", 1)[0], []).append((wt, n))
# the shared tree's own current markers too (an uncommitted marker is still a marker)
for p in glob.glob("org/critical_paths/.open_deploys/*.json"):
    seen.setdefault(p.rsplit("/", 1)[-1].rsplit(".", 1)[0].replace("\\", "/").rsplit("/", 1)[-1], []).append(("SHARED-WORKTREE", p))
live, hits = [], []
for slug, locs in sorted(seen.items()):
    led = glob.glob("org/critical_paths/change_management/*_%s_deploy_completion.md" % slug)
    head = open(led[0], encoding="utf-8", errors="replace").read(1500) if led else ""
    state = "CLOSED" if "**Status:** CLOSED" in head else ("ROLLED-BACK" if "**Status:** ROLLED-BACK" in head else "OPEN-or-unknown")
    if state != "OPEN-or-unknown" or slug == OWN:
        continue
    live.append(slug)
    wt, n = locs[0]
    body = open(n, encoding="utf-8", errors="replace").read() if wt == "SHARED-WORKTREE" else run("git", "-C", wt, "show", "HEAD:" + n)
    found = sorted({m.group(0).lower() for m in TERMS.finditer(body)})
    print("  NOT-CLOSED %-64s names: %s" % (slug, found or "-"))
    if found:
        hits.append((slug, found))
print("CENSUS worktrees_read=%d marker_files_read=%d distinct_slugs=%d not_closed_other_than_own=%d naming_the_surfaces=%d" % (len(wts), files, len(seen), len(live), len(hits)))
for h in hits:
    print("CENSUS HIT", h)
sys.exit(3 if hits else 0)
