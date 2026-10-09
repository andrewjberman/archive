"""OG-rl-15 step 2 (form): each RELEASE file's hunk set (live aa75078e1b .. candidate working tree) equals the owning cell's OWN diff, where a cell's own diff is
the NET diff of its build-commit chain (first commit's parent .. last commit) per file. Cells: OG-md-1 = 15b08fdca1; OG-sf-1 = 17b2977f4c; OG-rf-1 = 41b0c7903b + cd730f3bb5; OG-cm-1 = fcedf00b1e.
A file is EQUAL when its changed-line multiset (added and removed lines, header lines dropped) equals the cell's. The extra-hunk rows are named as such.
usage: python r29_hunk_equality.py <candidate worktree> <repo with the cell commits>"""
import collections
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
WT, REPO = sys.argv[1], sys.argv[2]
CELLS = {"OG-md-1": ["15b08fdca1"], "OG-sf-1": ["17b2977f4c"], "OG-rf-1": ["41b0c7903b", "cd730f3bb5"], "OG-cm-1": ["fcedf00b1e"]}
FILES = [("app/mail_route.py", "OG-md-1"), ("app/config.py", "OG-md-1"), ("deploy-to-ec2.sh", "OG-md-1"), ("deploy/mail_sender_domain_table.txt", "OG-md-1"),
         ("tests/test_mail_route_domain.py", "OG-md-1"), ("app/destructive_ops.py", "OG-sf-1"), ("tests/test_asker_safe_tool.py", "OG-sf-1"),
         ("app/server.py", "OG-rf-1"), ("app/oauth_as.py", "OG-rf-1"), ("tests/test_oauth_send_budget.py", "OG-rf-1"),
         ("app/integrations/schwab/catalog.py", "OG-cm-1"), ("app/integrations/schwab/integration.py", "OG-cm-1"), ("app/data_entitlement.py", "OG-cm-1"),
         ("app/admin_grants.py", "OG-cm-1"), ("ops/schwab_entitlement_admin.py", "OG-cm-1"), ("deploy/NFRA_OPLGTW_CONTRACT.json", "OG-cm-1"),
         ("tests/test_grant_calendar_months.py", "OG-cm-1")]


def run(repo, *a):
    return subprocess.run(["git", "-C", repo] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


def changed(diff):
    c = collections.Counter()
    for ln in diff.splitlines():
        if ln.startswith(("+++", "---", "diff ", "index ", "@@", "new file", "deleted file", "similarity", "rename ")):
            continue
        if ln.startswith(("+", "-")):
            c[ln] += 1
    return c


LIVE = "aa75078e1b72a28219e6148d3ec8e9bf705ea111"


def net(path):
    """The release's net change to `path`: live..HEAD of the release worktree (the committed release when the tree is clean; the working tree on top of it otherwise)."""
    return changed(run(WT, "diff", LIVE, "--", path))


ok = True
for f, cell in FILES + [("../../../../org/standards/NFRA_OPLGTW_CONTRACT.json", "OG-cm-1 (org/standards copy)")]:
    path = G + f if not f.startswith("..") else "org/standards/NFRA_OPLGTW_CONTRACT.json"
    cellname = cell.split(" ")[0]
    own = collections.Counter()
    first, last = CELLS[cellname][0], CELLS[cellname][-1]
    own = changed(run(REPO, "diff", first + "^", last, "--", path))   # the cell's chain as ONE net diff (a later commit may rewrite an earlier one's lines)
    n = net(path)
    x, y = n - own, own - n
    v = "EQUAL" if not x and not y and sum(n.values()) > 0 else ("DIFFER" if sum(n.values()) else "EMPTY")
    extra = ""
    if f == "deploy/mail_sender_domain_table.txt" and v == "DIFFER":
        extra = " (only-in-candidate: the %d proposed entries and their comments, and the 2 header lines E3 rewrote; only-in-cell: those 2 header lines)" % sum(x.values())
        v = "CELL+ENTRIES+E3" if sum(y.values()) == 2 else v
    if f == "deploy-to-ec2.sh" and v == "DIFFER":
        xo = [k for k in x if k.startswith("+") and "MAIL_BEARER_LABELS=" in k]
        yo = [k for k in y if k.startswith("+") and "MAIL_BEARER_LABELS=" in k]
        one_token = len(xo) == 1 and len(yo) == 1 and xo[0][1:].replace("msgpull,commassist", "msgpull") == yo[0][1:]
        extra = " (E4: only-in-candidate %d lines = the 10-line MAIL_BEARER leg hunk + the printf line; only-in-cell %d = the old printf line; the printf line differs by the one token msgpull -> msgpull,commassist: %s)" % (sum(x.values()), sum(y.values()), one_token)
        v = "CELL+E4" if (sum(x.values()) == 11 and sum(y.values()) == 1 and one_token) else v
    if f == "tests/test_mail_route_domain.py" and v == "DIFFER":
        extra = " (E2: only-in-candidate %d line(s), only-in-cell %d line(s): the ac06 pin and its comment)" % (sum(x.values()), sum(y.values()))
        v = "CELL+E2" if sum(y.values()) == sum(x.values()) <= 2 else v
    print("%s [%s]: candidate changed-lines %d, cell changed-lines %d, only-in-candidate %d, only-in-cell %d => %s%s" % (
        f if not f.startswith("..") else "org/standards/NFRA_OPLGTW_CONTRACT.json", cell, sum(n.values()), sum(own.values()), sum(x.values()), sum(y.values()), v, extra))
    ok = ok and v in ("EQUAL", "CELL+ENTRIES+E3", "CELL+E2", "CELL+E4")
for f in ("identity_tool_allowlist.txt", "app/identity_scope.py", "app/graph_scope_map.py", "tests/test_scoped_consent_r253.py"):   # A6: nothing Bloomberg ships
    n = net(G + f)
    print("%s [A6: must be untouched]: changed lines %d => %s" % (f, sum(n.values()), "UNTOUCHED" if not n else "TOUCHED"))
    ok = ok and not n
ht = net(G + "tests/test_schwab_host_inputs.py")
print("tests/test_schwab_host_inputs.py [floor constants]: %s" % sorted(ht.items()))
nm = [x for x in run(WT, "diff", "--name-only", LIVE).split("\n") if x.strip()]
print("release HEAD %s; files differing live..HEAD: %d; worktree clean: %s" % (run(WT, "rev-parse", "HEAD").strip(), len(nm), "yes" if not run(WT, "status", "--short").strip() else "NO"))
ok = ok and len(nm) == 19
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
