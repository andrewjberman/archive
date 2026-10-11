"""ADVI_FIRMBKTS round 4: the write-surface bound of one cut (the control arm of an order), issuer 2.0.0_SA_COO~B1.

  --root <tree>            the worker's worktree
  --allow <path|dir/>      a path the cell may change (repeatable; an entry ending in / is a directory prefix)
  --require <path>         a path the cell MUST have changed (repeatable)
Compares the tree's HEAD with the merge-base of HEAD and the primary checkout's HEAD (the commit the worktree was cut
from), plus any uncommitted change. Prints every changed path and the verdict; the last line reads
`ROUND 4 SCOPE: OK n changed, 0 outside` or `ROUND 4 SCOPE: FAIL ...`. Never edit this file.
"""
import argparse
import subprocess
import sys


def _git(root, *a):
    r = subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--allow", action="append", default=[])
    ap.add_argument("--require", action="append", default=[])
    a = ap.parse_args()
    rc, wl = _git(a.root, "worktree", "list", "--porcelain")
    primary = next((ln.split()[1] for ln in wl.split("\n") if ln.startswith("HEAD ")), "")
    rc, base = _git(a.root, "merge-base", "HEAD", primary)
    if rc or not base:
        print("ROUND 4 SCOPE: FAIL no merge-base with the primary checkout")
        return 1
    _, committed = _git(a.root, "diff", "--name-only", base, "HEAD")
    _, dirty = _git(a.root, "diff", "--name-only", "HEAD")
    _, untracked = _git(a.root, "ls-files", "--others", "--exclude-standard")
    changed = sorted({p for p in (committed + "\n" + dirty + "\n" + untracked).split("\n") if p.strip()})

    def allowed(p):
        return any(p == e or (e.endswith("/") and p.startswith(e)) for e in a.allow)
    outside = [p for p in changed if not allowed(p)]
    absent = [p for p in a.require if p not in changed]
    for p in changed:
        print("  CHANGED %s%s" % (p, "" if allowed(p) else "   <-- OUTSIDE"))
    for p in absent:
        print("  REQUIRED-NOT-CHANGED %s" % p)
    ok = not outside and not absent and bool(changed)
    print("ROUND 4 SCOPE: %s %d changed, %d outside, %d required missing"
          % ("OK" if ok else "FAIL", len(changed), len(outside), len(absent)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
