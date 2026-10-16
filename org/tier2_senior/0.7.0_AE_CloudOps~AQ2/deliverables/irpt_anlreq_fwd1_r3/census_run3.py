"""IRPT_ANLREQ TO-RUN-FWD1 window 3, step 1 NEVER-2 census (read-only): every live worktree's org/critical_paths/.open_deploys/ by ls-tree, deduplicated by blob,
then the entries that name a watched surface (the resident host or unit, either Lambda, the ticket service, the users table, the intake store) are printed with whether
the shared tree still holds the file (an entry the shared tree no longer holds was closed on trunk)."""
from __future__ import annotations

import os
import re
import subprocess
import sys

KEYS = re.compile(r"i-0167fd745ad906a66|irpt-analysis-resident|irpt-ycharts-generate|irpt-status|opal-ticket-api|opal-users-v2|opal-data-irpt|outlook-global-commentary-draft|ticket service|fwd1-staff|resident", re.I)
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SUB = "org/critical_paths/.open_deploys/"


def git(wt, *a):
    return subprocess.run(["git", "-C", wt, *a], capture_output=True)


def main():
    wts = [ln.split(" ", 1)[1] for ln in git(ROOT, "worktree", "list", "--porcelain").stdout.decode().splitlines() if ln.startswith("worktree ")]
    blobs = {}
    denom = 0
    for wt in wts:
        r = git(wt, "ls-tree", "-r", "HEAD", SUB)
        if r.returncode != 0:
            continue
        denom += 1
        for line in r.stdout.decode().splitlines():
            meta, path = line.split("\t", 1)
            blob = meta.split()[2]
            blobs.setdefault((path, blob), wt)
    slugs = sorted({p for p, _ in blobs})
    print("CENSUS worktrees read %d of %d listed; distinct (path, blob) %d; distinct paths %d" % (denom, len(wts), len(blobs), len(slugs)))
    hits = 0
    for (path, blob), wt in sorted(blobs.items()):
        body = git(wt, "cat-file", "-p", blob).stdout.decode("utf-8", "replace")
        m = KEYS.findall(body)
        if m:
            hits += 1
            held = os.path.exists(os.path.join(ROOT, path))
            print("NAMES-WATCHED %s keys=%s shared-tree-holds-file=%s" % (os.path.basename(path), sorted({k.lower() for k in m})[:5], held))
    print("CENSUS entries naming a watched surface: %d" % hits)
    return 0


if __name__ == "__main__":
    sys.exit(main())
