"""OG-rl-7 A2-3 (r19b, R22): each SERVICE file (now TWO: server.py is unchanged)'s release hunk set (live 37be3485db .. CLOUD base ea483704fe) equals the owning cell's OWN diff.
usage: python r19_hunk_equality.py  (run from any worktree of the repo). Compares the multiset of added and removed lines (a hunk header
differs across trees whose context differs; the changed lines do not). Prints one line per file and RESULT."""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE, CLOUD = "37be3485db", "cf4b036e62"   # CLOUD here = the r19b release head (== CLOUD after R22, proven in r19b_equality.out)


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


CELLS = [  # (file, owning cell, [(commit, label)] whose OWN diff of that file is the cell's)
    ("app/integrations/schwab/envelope.py", "NFRA_OPLGTW OG-o-4", ["877339606f"]),
    # live's blob equals 5af362d473's (MS-rq-1 build); CLOUD's equals e138cec769's: the MS-sg-1 change is that span.
    ("app/admin_refusals.py", "NFRA_MCPMSP MS-sg-1 (5af362d473..e138cec769)", ["5af362d473..e138cec769"]),
]
ok = True
for f, cell, commits in CELLS:
    total = changed(git("diff", LIVE, CLOUD, "--", G + f))
    own = collections.Counter()
    for c in commits:
        if ".." in c:
            a, b = c.split("..")
            own += changed(git("diff", a, b, "--", G + f))
            print("   blob check: live==%s %s; CLOUD==%s %s" % (a, git("rev-parse", LIVE + ":" + G + f) == git("rev-parse", a + ":" + G + f),
                                                               b, git("rev-parse", CLOUD + ":" + G + f) == git("rev-parse", b + ":" + G + f)))
        else:
            own += changed(git("show", "--format=", c, "--", G + f))
    only_total = total - own
    only_own = own - total
    verdict = "EQUAL" if not only_total and not only_own else "DIFFER"
    print("%s [%s] commits %s: release changed-lines %d, cell changed-lines %d, only-in-release %d, only-in-cell %d => %s"
          % (f, cell, ",".join(commits), sum(total.values()), sum(own.values()), sum(only_total.values()), sum(only_own.values()), verdict))
    if verdict != "EQUAL":
        ok = False
        for ln in list(only_total)[:6]:
            print("   release-only:", ln[:140])
        for ln in list(only_own)[:6]:
            print("   cell-only   :", ln[:140])
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
