"""OG-rl-11 step 2: each shipped file's release hunk set (live 7d65a28db0 .. release head) equals the owning cell(s)' OWN diff.
Cells: OG-up-1 = a357b3bdf6 (one commit); NFRA_OPALAI OA-f-14 = 1fb6300bcb + ee22aced29 (A1), taken as the cell's NET diff 1fb6300bcb^..ee22aced29 (A1 edits lines the first commit
added, so a per-commit sum would count them twice); app/graph_scope_map.py is touched by BOTH cells, so its expected set is OA-f-14's net diff PLUS OG-up-1's own diff together.
usage: python r25_hunk_equality.py <release head> [<CLOUD ref>]. Compares the multiset of added and removed lines per file, then the release blob against the CLOUD blob."""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
LIVE = "7d65a28db026a44d7199ffe52a97e44952df75a1"
REL = sys.argv[1]
CLOUD = sys.argv[2] if len(sys.argv) > 2 else "CLOUD"
UP1, F14A, F14B = "a357b3bdf6", "1fb6300bcb", "ee22aced29"


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


def up1(f):
    return changed(git("show", "--format=", UP1, "--", G + f))


def f14(f):
    return changed(git("diff", F14A + "^", F14B, "--", G + f))


CELLS = [
    ("app/integrations/opal_portal/integration.py", "OG-up-1", up1),
    ("app/data_entitlement.py", "OG-up-1", up1),
    ("tests/test_entitlement_admin.py", "OG-up-1", up1),
    ("tests/test_opal_portal_send_split.py", "OG-up-1", up1),
    ("app/graph_scope_map.py", "OA-f-14 net + OG-up-1", lambda f: f14(f) + up1(f)),
    ("app/identity_scope.py", "OA-f-14 net", f14),
    ("app/token_broker.py", "OA-f-14 net", f14),
    ("tests/test_scoped_consent_r253.py", "OA-f-14 net", f14),
]
ok = True
for f, cell, own_fn in CELLS:
    total = changed(git("diff", LIVE, REL, "--", G + f))
    own = own_fn(f)
    a, b = total - own, own - total
    v = "EQUAL" if not a and not b else "DIFFER"
    blob_rel, blob_cloud = git("rev-parse", REL + ":" + G + f).strip(), git("rev-parse", CLOUD + ":" + G + f).strip()
    print("%s [%s]: release changed-lines %d, cell(s) changed-lines %d, only-in-release %d, only-in-cell %d => %s; release blob == %s blob: %s"
          % (f, cell, sum(total.values()), sum(own.values()), sum(a.values()), sum(b.values()), v, CLOUD, "yes" if blob_rel and blob_rel == blob_cloud else "NO"))
    ok = ok and v == "EQUAL" and blob_rel == blob_cloud
names = [x for x in git("diff", "--name-only", LIVE, REL).split("\n") if x]
print("release set files %d; paths outside %s: %d" % (len(names), G, sum(1 for n in names if not n.startswith(G))))
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
