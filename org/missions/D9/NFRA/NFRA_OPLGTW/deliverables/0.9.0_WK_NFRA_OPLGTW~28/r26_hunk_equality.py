"""OG-rl-12 step 2: each shipped file's release hunk set (live 240ac2fe5a .. release head) equals the owning cells' OWN diff.
Cells: OG-al-2 = 82da719ba2 + d1f9077190 (AMENDMENT 2); OG-up-2 = a7bf684bcd. A file touched by more than one commit has its expected set = the cells' NET
diff over the range 82da719ba2^..a7bf684bcd (a per-commit SUM would count twice a line one commit adds and a later one rewrites; the first run did, and showed
only-in-cell 2 and 8). The check first asserts the commits that touch the file in that range are exactly the listed ones, so the net diff is the cells' alone.
usage: python r26_hunk_equality.py <repo dir, C:/ form> <release head> [<CLOUD ref>]. Compares the multiset of added and removed lines per file, then the release blob
against the CLOUD blob."""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE = "240ac2fe5abde944f15358ab563cb4b2ab63f09f"
REPO, REL = sys.argv[1], sys.argv[2]
CLOUD = sys.argv[3] if len(sys.argv) > 3 else "refs/heads/CLOUD"
AL2A, AL2B, UP2 = "82da719ba2", "d1f9077190", "a7bf684bcd"
RIV = "f7f2cb7c2e"   # RIV-rt-1 (A3): the cell's own diff is the merge against its first parent, `git diff f7f2cb7c2e^1 f7f2cb7c2e`


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


def commit(c, f):
    return changed(git("show", "--format=", c, "--", G + f))


FILES = [
    ("identity_tool_allowlist.txt", "OG-al-2", (AL2A,)),
    ("app/integrations/opal_portal/integration.py", "OG-al-2 + OG-up-2", (AL2A, AL2B, UP2)),
    ("tests/test_identity_scope_status_row.py", "OG-al-2", (AL2A,)),
    ("tests/test_opal_portal_status_id_shape.py", "OG-al-2 + OG-up-2 (one fake given a hash)", (AL2A, AL2B, UP2)),
    ("tests/test_opal_portal_dedupe_content.py", "OG-up-2", (UP2,)),
    ("tests/test_opal_portal_send_split.py", "OG-up-2 (fakes given a hash)", (UP2,)),
    ("app/rivalfunds_view.py", "RIV-rt-1", (RIV,)),
    ("app/server.py", "RIV-rt-1 (one Route line)", (RIV,)),
    ("app/tests/test_rivalfunds_view.py", "RIV-rt-1", (RIV,)),
    ("tests/test_principal_cutover.py", "RIV-rt-1 (ROUTE_CLASS line)", (RIV,)),
]
ok = True
for f, cell, cs in FILES:
    total = changed(git("diff", LIVE, REL, "--", G + f))
    if cs == (RIV,):
        own = changed(git("diff", RIV + "^1", RIV, "--", G + f))
    elif len(cs) == 1:
        own = commit(cs[0], f)
    else:
        touching = [x for x in git("log", "--format=%h", AL2A + "^.." + UP2, "--", G + f).split() if x]
        assert sorted(touching) == sorted(c[:len(touching[0])] for c in cs), (f, touching)
        own = changed(git("diff", AL2A + "^", UP2, "--", G + f))
    a, b = total - own, own - total
    v = "EQUAL" if not a and not b and sum(total.values()) > 0 else "DIFFER"
    blob_rel, blob_cloud = git("rev-parse", REL + ":" + G + f).strip(), git("rev-parse", CLOUD + ":" + G + f).strip()
    print("%s [%s]: release changed-lines %d, cell commit(s) changed-lines %d, only-in-release %d, only-in-cell %d => %s; release blob == %s blob: %s"
          % (f, cell, sum(total.values()), sum(own.values()), sum(a.values()), sum(b.values()), v, CLOUD, "yes" if blob_rel and blob_rel == blob_cloud else "NO"))
    ok = ok and v == "EQUAL" and blob_rel == blob_cloud
names = [x for x in git("diff", "--name-only", LIVE, REL).split("\n") if x]
print("release set files %d; paths outside %s: %d" % (len(names), G, sum(1 for n in names if not n.startswith(G))))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
