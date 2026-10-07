"""OG-rl-13 step 2: each shipped file's release hunk set (live feddb37244 .. release head) equals the owning cell's OWN diff.
Cells: OG-au-2 = `git diff ccf93dea8e 3153a1c764 -- infra/aws/ec2/opal-gateway`; OG-sd-1 = `git diff ccf93dea8e 6818de7e0d -- infra/aws/ec2/opal-gateway`.
Each of the five release files is touched by exactly one cell (checked: the two cells' file sets are disjoint). Compares the multiset of added and removed lines per file,
then the release blob against the CLOUD blob.
usage: python r27_hunk_equality.py <repo dir, C:/ form> <release head> [<CLOUD ref>]"""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE = "feddb372443adbcf139febab35b69f109e49b664"
REPO, REL = sys.argv[1], sys.argv[2]
CLOUD = sys.argv[3] if len(sys.argv) > 3 else "refs/heads/CLOUD"
BASE, AU2, SD1 = "ccf93dea8e", "3153a1c764", "6818de7e0d"


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def changed(diff):
    c = collections.Counter()
    for ln in diff.splitlines():
        if ln.startswith(("+++", "---")):
            continue
        if ln.startswith(("+", "-")):
            c[ln] += 1
    return c


def names(a, b):
    return set(x for x in git("diff", "--name-only", a, b, "--", G).split("\n") if x)


FILES = [
    ("app/audit.py", "OG-au-2", (BASE, AU2)),
    ("app/rivalfunds_view.py", "OG-au-2", (BASE, AU2)),
    ("tests/test_audit_rivalfunds_args.py", "OG-au-2", (BASE, AU2)),
    ("app/integrations/opal_portal/integration.py", "OG-sd-1", (BASE, SD1)),
    ("tests/test_opal_portal_status_displayed_date.py", "OG-sd-1", (BASE, SD1)),
]
au2n, sd1n = names(BASE, AU2), names(BASE, SD1)
print("cell file sets: OG-au-2 %d files, OG-sd-1 %d files, shared %d" % (len(au2n), len(sd1n), len(au2n & sd1n)))
ok = not (au2n & sd1n)
for f, cell, (a, b) in FILES:
    total = changed(git("diff", LIVE, REL, "--", G + f))
    own = changed(git("diff", a, b, "--", G + f))
    x, y = total - own, own - total
    v = "EQUAL" if not x and not y and sum(total.values()) > 0 else "DIFFER"
    blob_rel, blob_cloud = git("rev-parse", REL + ":" + G + f).strip(), git("rev-parse", CLOUD + ":" + G + f).strip()
    print("%s [%s]: release changed-lines %d, cell changed-lines %d, only-in-release %d, only-in-cell %d => %s; release blob == %s blob: %s"
          % (f, cell, sum(total.values()), sum(own.values()), sum(x.values()), sum(y.values()), v, CLOUD, "yes" if blob_rel and blob_rel == blob_cloud else "NO"))
    ok = ok and v == "EQUAL" and blob_rel == blob_cloud
nm = [x for x in git("diff", "--name-only", LIVE, REL).split("\n") if x]
print("release set files %d; paths outside %s: %d" % (len(nm), G, sum(1 for n in nm if not n.startswith(G))))
ok = ok and len(nm) == len(FILES)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
