"""OG-rl-15 Phase A: build the CANDIDATE release tree (uncommitted) in the release worktree from the blobs of the hand-off commit.
Candidate = live aa75078e1b + the four cells' files (md-1, sf-1, rf-1, cm-1) + A2/A3's four allowlist rows + the two host-input constants + the
domain-table entries proposed in the ask. EXCLUDED (extras, row Z-W43-S1): app/admin_api.py, app/admin_fabric.py, app/refs/fabric_boxes.json,
app/teams_route.py, tests/test_admin_fabric.py, tests/test_teams_route.py, and the three Route lines CT-i-11 added to app/server.py.
usage: python r29_build_candidate.py <worktree> <hand-off rev> <domain-table-file or ->"""
import re
import subprocess
import sys

G = "infra/aws/ec2/opal-gateway/"
wt, rev, dom = sys.argv[1], sys.argv[2], sys.argv[3]
FILES = ["app/mail_route.py", "app/config.py", "deploy-to-ec2.sh", "deploy/mail_sender_domain_table.txt", "tests/test_mail_route_domain.py",
         "app/destructive_ops.py", "tests/test_asker_safe_tool.py",
         "app/server.py", "app/oauth_as.py", "tests/test_oauth_send_budget.py",
         "app/integrations/schwab/catalog.py", "app/integrations/schwab/integration.py", "app/data_entitlement.py", "app/admin_grants.py",
         "ops/schwab_entitlement_admin.py", "deploy/NFRA_OPLGTW_CONTRACT.json", "tests/test_grant_calendar_months.py"]
Q = chr(34)
ROWS = chr(10).join([
    "# andrew-asked: 2026-10-09 ~01:5xZ at the 4.0.0_SA_CRO~Z terminal, VERBATIM: " + Q + "any account at black diamond, orion, eclipse, bloomberg,",
    "# ycharts, schwab, smartx, eclipse, any vendor any everything" + Q + " and " + Q + "do not hold up progress or work about theoretical users that",
    "# arent even connected" + Q + " (record org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/ANDREW_DIRECT_20261009_015xZ_OPAL_STAFF_MAY_READ_BLACK_DIAMOND_THROUGH_GATEWAY.md",
    "# @0035550443; CTO msg 32258, narrowed by msg 32278 / PRD v2.2 item 2, ADMITTED @1825ea3472: the concierge gets NO data grant).",
    "# The Bloomberg concierge may call these four tools, unqualified (no client=). blackdiamond_list_fees is NOT admitted here.",
    "@@ID@@ opal_discover", "@@ID@@ opal_describe",
    "@@ID@@ find_sharepoint_site", "@@ID@@ search_files", ""])


def show(path):
    return subprocess.run(["git", "show", "%s:%s" % (rev, path)], capture_output=True, check=True).stdout


def put(rel, data):
    with open(wt + "/" + G + rel, "wb") as fh:
        fh.write(data)


for f in FILES:
    b = show(G + f)
    if f == "app/server.py":
        t = b.decode("utf-8")
        cut = ("        Route(teams_route.TEAMS_ROUTE, teams_route.teams_endpoint, methods=list(teams_route.GET_METHODS)),\n"
               "        Route(teams_route.CHANNELS_ROUTE, teams_route.channels_endpoint, methods=list(teams_route.GET_METHODS)),\n"
               "        Route(teams_route.CHANNEL_MESSAGES_ROUTE, teams_route.channel_messages_endpoint,\n"
               "              methods=list(teams_route.GET_METHODS)),\n")
        assert t.count(cut) == 1
        b = t.replace(cut, "").encode("utf-8")
    if f == "deploy/mail_sender_domain_table.txt" and dom != "-":
        b = b + open(dom, "rb").read()
    put(f, b)
for f in ("app/graph_scope_map.py", "tests/test_scoped_consent_r253.py"):   # restored to the live bytes: r29_release_time_edits.py edits them
    put(f, show(G + f))
put("../../../../org/standards/NFRA_OPLGTW_CONTRACT.json", show("org/standards/NFRA_OPLGTW_CONTRACT.json"))
al = show(G + "identity_tool_allowlist.txt").decode("utf-8")   # the live blob, so a re-run never doubles the rows
if not al.endswith("\n"):
    al += "\n"
ident = re.search(r"^(\S+@\S+) opal_data_refresh_upload ", al, re.M).group(1)   # the identity of the live file's own first row, never typed here
put("identity_tool_allowlist.txt", (al + "#" + chr(10) + ROWS.replace("@@ID@@", ident)).encode("utf-8"))
ht = show(G + "tests/test_schwab_host_inputs.py").decode("utf-8")   # the live blob: re-runnable
assert ht.count('== "%s") == 18') == 1 and ht.count("assert len(raw) == 51") == 1
ht = ht.replace('== "%s") == 18', '== "%s") == 19').replace("assert len(raw) == 51", "assert len(raw) == 52")
put("tests/test_schwab_host_inputs.py", ht.encode("utf-8"))
print("candidate built in", wt, "(run r29_release_time_edits.py next)")
