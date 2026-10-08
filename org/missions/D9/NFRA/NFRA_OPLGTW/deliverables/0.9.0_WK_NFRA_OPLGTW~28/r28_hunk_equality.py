"""OG-rl-14 step 2: each release file's hunk set (live 510c8cfed2 .. release head) equals the owning cell's OWN diff.
Cells (the issuer's ranges): OG-lk-1 = `git diff db6af9feaf 3e1b858b63 -- infra/aws/ec2/opal-gateway`;
OG-bi-1 + OG-bi-2 + OG-bi-3 together = `git diff 7cc16c57ac 7e069c788d -- infra/aws/ec2/opal-gateway` (one worker, one branch; the NET diff).
The bi range also carries the lk-1 merge (3e1b858b63 is an ancestor of 7e069c788d and not of 7cc16c57ac), so the bi net diff lists the lk-1 files too; both are compared, and a file is EQUAL when
its changed-line multiset (added and removed lines) equals the multiset of the cell that owns it. Then the release blob against the CLOUD blob at the hand-off commit and at the CLOUD ref now.
usage: python r28_hunk_equality.py <repo dir, C:/ form> <release head> [<CLOUD hand-off ref>]"""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE = "510c8cfed2c852946e3e57fb4dd1c0467e2f3a52"
REPO, REL = sys.argv[1], sys.argv[2]
HANDOFF = sys.argv[3] if len(sys.argv) > 3 else "6124b079f3"
LK1 = ("db6af9feaf", "3e1b858b63")
BI = ("7cc16c57ac", "7e069c788d")


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
    return set(x[len(G):] for x in git("diff", "--name-only", a, b, "--", G).split("\n") if x)


lkn, bin_ = names(*LK1), names(*BI)
FILES = [("app/audit.py", "OG-lk-1", LK1), ("tests/test_audit_lake_key_stamp.py", "OG-lk-1", LK1),
         ("deploy-to-ec2.sh", "OG-bi-1+2", BI), ("ops/bun_cache_precheck.py", "OG-bi-1+3", BI),
         ("tests/test_deploy_install_no_fetch.py", "OG-bi-1", BI), ("tests/test_deploy_install_no_fetch_complete.py", "OG-bi-3", BI),
         ("tests/test_deploy_host_pip_no_upgrade.py", "OG-bi-2", BI)]
print("cell file sets: OG-lk-1 %d files %s; OG-bi net %d files; the lk-1 files inside the bi net range: %s" % (len(lkn), sorted(lkn), len(bin_), sorted(lkn & bin_)))
ok = set(f for f, _, _ in FILES) == (lkn | bin_)
print("the union of the two cells' files equals the 7 release files: %s" % ("yes" if ok else "NO"))
for f, cell, (a, b) in FILES:
    total = changed(git("diff", LIVE, REL, "--", G + f))
    own = changed(git("diff", a, b, "--", G + f))
    x, y = total - own, own - total
    v = "EQUAL" if not x and not y and sum(total.values()) > 0 else "DIFFER"
    other = ""
    if f in lkn and f in bin_:      # the bi net range also carries the lk-1 hunks: report it
        ob = changed(git("diff", BI[0], BI[1], "--", G + f))
        other = "; also equal to the bi net diff: %s" % ("yes" if ob == total else "NO")
        ok = ok and ob == total
    blob_rel = git("rev-parse", REL + ":" + G + f).strip()
    b_hand, b_now = git("rev-parse", HANDOFF + ":" + G + f).strip(), git("rev-parse", "refs/heads/CLOUD:" + G + f).strip()
    print("%s [%s]: release changed-lines %d, cell changed-lines %d, only-in-release %d, only-in-cell %d => %s%s; release blob == %s blob: %s; == refs/heads/CLOUD blob now: %s"
          % (f, cell, sum(total.values()), sum(own.values()), sum(x.values()), sum(y.values()), v, other, HANDOFF, "yes" if blob_rel and blob_rel == b_hand else "NO",
             "yes" if blob_rel and blob_rel == b_now else "NO"))
    ok = ok and v == "EQUAL" and blob_rel == b_hand
nm = [x for x in git("diff", "--name-only", LIVE, REL).split("\n") if x]
print("release set files %d; paths outside %s: %d" % (len(nm), G, sum(1 for n in nm if not n.startswith(G))))
ok = ok and len(nm) == len(FILES)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
