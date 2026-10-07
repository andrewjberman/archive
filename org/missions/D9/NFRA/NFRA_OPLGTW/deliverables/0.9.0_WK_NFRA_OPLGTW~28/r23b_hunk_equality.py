"""OG-rl-9 step 2: each shipped file's release hunk set (live 9d3e2eb3fc .. release head) equals the owning cell's OWN diff (OG-q-8 = 31043ba49b; ETFS_RIVALS gw-1 = e4023f7921 + A1 7ea252026d, both on CLOUD via 291bb5bb4b).
usage: python r23b_hunk_equality.py <release head>. Compares the multiset of added and removed lines, per file."""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE = "9d3e2eb3fc"
REL = sys.argv[1]


def git(*a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def changed(diff):
    c = collections.Counter()
    for ln in diff.splitlines():
        if ln.startswith(("+++", "---")):
            continue
        if ln.startswith(("+", "-")):
            c[ln] += 1
    return c


CELLS = [
    ("app/integrations/schwab/integration.py", "OG-q-8", ["31043ba49b"]),
    ("tests/test_schwab_q8_blank_cusip.py", "OG-q-8", ["31043ba49b"]),
    ("app/rivalfunds_view.py", "ETFS_RIVALS gw-1", ["e4023f7921"]),
    ("app/tests/test_rivalfunds_view.py", "ETFS_RIVALS gw-1", ["e4023f7921"]),
    ("app/server.py", "ETFS_RIVALS gw-1 A1", ["7ea252026d"]),
    ("tests/test_principal_cutover.py", "ETFS_RIVALS gw-1 A1", ["7ea252026d"]),
]
ok = True
for f, cell, commits in CELLS:
    total = changed(git("diff", LIVE, REL, "--", G + f))
    own = collections.Counter()
    for c in commits:
        own += changed(git("show", "--format=", c, "--", G + f))
    a, b = total - own, own - total
    v = "EQUAL" if not a and not b else "DIFFER"
    print("%s [%s %s]: release changed-lines %d, cell changed-lines %d, only-in-release %d, only-in-cell %d => %s" % (f, cell, ",".join(commits), sum(total.values()), sum(own.values()), sum(a.values()), sum(b.values()), v))
    ok = ok and v == "EQUAL"
names = [x for x in git("diff", "--name-only", LIVE, REL).split("\n") if x]
print("release set files %d; paths outside %s: %d" % (len(names), G, sum(1 for n in names if not n.startswith(G))))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
