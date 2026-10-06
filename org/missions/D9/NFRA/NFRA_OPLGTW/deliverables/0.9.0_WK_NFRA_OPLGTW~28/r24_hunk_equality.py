"""OG-rl-10 step 2: the release file hunk set (live 2c27f3a795 .. release head) equals the fix commit a34a007a25's OWN diff of the gateway tree. usage: python r24_hunk_equality.py <release head>. Compares the multiset of added and removed lines, per file."""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE = "2c27f3a795"
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
    ("app/integrations/opal_portal/integration.py", "OG-rl-10 fix", ["a34a007a25"]),
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
