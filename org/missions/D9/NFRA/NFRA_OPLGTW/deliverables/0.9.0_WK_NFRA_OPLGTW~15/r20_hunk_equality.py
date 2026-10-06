"""OG-rl-8 step 2: each file's release hunk set (live cf4b036e62 .. release head) equals the owning cell's OWN diff.
usage: python r20_hunk_equality.py <release head> (run from any worktree of the repo). Compares the multiset of added and removed lines.
Cells: OG-lg-1 = the span ad81918ea3^..46e1b0af2b (net) (server.py, audit.py, tests/test_login_admit_r24.py); OG-fl-1 = b065029296 (engine.py) and cc44859ac0 (tests/test_schwab_rss_poll.py)."""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE = "cf4b036e62"
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
    ("app/server.py", "OG-lg-1", ["ad81918ea3^..46e1b0af2b"]),
    ("app/audit.py", "OG-lg-1", ["ad81918ea3^..46e1b0af2b"]),
    ("tests/test_login_admit_r24.py", "OG-lg-1", ["ad81918ea3^..46e1b0af2b"]),
    ("app/integrations/schwab/engine.py", "OG-fl-1", ["b065029296"]),
    ("tests/test_schwab_rss_poll.py", "OG-fl-1", ["cc44859ac0"]),
]
ok = True
for f, cell, commits in CELLS:
    total = changed(git("diff", LIVE, REL, "--", G + f))
    own = collections.Counter()
    for c in commits:
        if ".." in c:   # a span: the cell's NET diff of that file (a later commit may remove what an earlier one added)
            a, b = c.split("..")
            own += changed(git("diff", a, b, "--", G + f))
            print("   blob check: live==%s %s; CLOUD-after-span==%s %s" % (a, git("rev-parse", LIVE + ":" + G + f) == git("rev-parse", a + ":" + G + f),
                                                                       b, git("rev-parse", REL + ":" + G + f) == git("rev-parse", b + ":" + G + f)))
        else:
            own += changed(git("show", "--format=", c, "--", G + f))
    only_total, only_own = total - own, own - total
    verdict = "EQUAL" if not only_total and not only_own else "DIFFER"
    print("%s [%s] commits %s: release changed-lines %d, cell changed-lines %d, only-in-release %d, only-in-cell %d => %s"
          % (f, cell, ",".join(commits), sum(total.values()), sum(own.values()), sum(only_total.values()), sum(only_own.values()), verdict))
    if verdict != "EQUAL":
        ok = False
        for ln in list(only_total)[:6]:
            print("   release-only:", ln[:140])
        for ln in list(only_own)[:6]:
            print("   cell-only   :", ln[:140])
names = [x for x in git("diff", "--name-only", LIVE, REL).split("\n") if x]
print("release set files %d; paths outside %s: %d" % (len(names), G, sum(1 for n in names if not n.startswith(G))))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
