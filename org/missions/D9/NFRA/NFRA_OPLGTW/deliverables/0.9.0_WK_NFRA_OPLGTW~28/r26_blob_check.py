"""OG-rl-12 step 1/2 helper: a md5 list (`<md5>  <path under the gateway tree>`) against the git blobs of a commit.
usage: python r26_blob_check.py <repo dir (C:/... form)> <commit> <md5 list>   Prints listed / equal / differing names; exit 0 only when all equal."""
import hashlib
import subprocess
import sys

GW = "infra/aws/ec2/opal-gateway/"
repo, commit, lst = sys.argv[1:4]
rows = [ln.rstrip("\r\n").split("  ", 1) for ln in open(lst, encoding="utf-8") if ln.strip()]
bad = []
for h, f in rows:
    p = subprocess.run(["git", "-C", repo, "show", commit + ":" + GW + f], capture_output=True)
    if p.returncode != 0 or hashlib.md5(p.stdout).hexdigest() != h:
        bad.append(f)
print("listed %d equal to the git blobs at %s: %d differing %s" % (len(rows), commit[:10], len(rows) - len(bad), bad))
sys.exit(0 if not bad else 1)
