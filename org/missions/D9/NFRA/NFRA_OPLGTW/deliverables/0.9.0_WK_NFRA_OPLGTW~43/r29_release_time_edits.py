"""OG-rl-15 Phase A: the release-time edits the four cells + A2/A3 FORCE, applied to the (uncommitted) candidate. Each is a hunk that is in NO cell's own diff,
so each is named in the ask for the issuer's word (row Z-W43-S2).
 E1 app/graph_scope_map.py : four TOOL_GRAPH_SCOPES entries for the four allowlisted tools (tests/test_scoped_consent_r253.py fails without them;
    the consent URL would also lack the scopes the tools' own Graph calls need). Measured from the code, see the comments.
 E2 tests/test_mail_route_domain.py test_ogmd1_ac06 : the pin 'the shipped domain table holds no domain' becomes 'holds exactly the signed entries'.
 E4 tests/test_scoped_consent_r253.py : its last bound-consent assertion required the taxsma caller to ADD scopes; search_files now maps to Files.ReadWrite.All,
    the same scope, so the binding adds nothing new (the assertion becomes 'adds at most the caller's scopes').
 E3 deploy/mail_sender_domain_table.txt : the first two header comment lines said the file ships EMPTY; they now say it ships the signed entries.
usage: python r29_release_time_edits.py <candidate worktree>"""
import sys

G = "/infra/aws/ec2/opal-gateway/"
wt = sys.argv[1]


def rw(rel, fn):
    p = wt + G + rel
    t = open(p, encoding="utf-8", newline="").read()
    n = fn(t)
    assert n != t, rel
    open(p, "w", encoding="utf-8", newline="").write(n)


NL = chr(10)
ENTRIES = ["49financial.com", "cottonwoodmail.com", "inflectionwealth.com", "opalinvest.com"]


def e1(t):
    anchor = '    "opal_data_refresh_status": frozenset(),' + NL
    assert t.count(anchor) == 1
    add = NL.join([
        "    # OG-rl-15 A2/A3 (Andrew-direct record @0035550443; PRD v2.2 item 2: no data grant). MEASURED, from the code:",
        "    # opal_discover / opal_describe read the gateway catalog and S3 freshness through boto3 and make NO Graph call (integrations/opal_discover/integration.py).",
        '    "opal_discover": frozenset(),',
        '    "opal_describe": frozenset(),',
        "    # GET /sites?search= and GET /sites/{id}/drive/root:/{folder}:/children -- tools.py find_sharepoint_site; Sites.Read.All (config.py:64) covers both.",
        '    "find_sharepoint_site": frozenset({"Sites.Read.All"}),',
        "    # GET /me/drive/root/search(q=...) and GET /me/drive/items/{id}/content -- tools.py search_files; the one file scope consented in GRAPH_SCOPES is",
        "    # Files.ReadWrite.All (config.py:64; no Files.Read variant is consented), the scope the concierge's consent already carries through the taxsma_workbook caller.",
        '    "search_files": frozenset({"Files.ReadWrite.All"}),',
        ""])
    return t.replace(anchor, anchor + add)


def e2(t):
    old = '    assert lines == [], "the shipped domain table holds no domain"'
    assert t.count(old) == 1
    new = ("    assert sorted(lines) == %r, \"the shipped domain table holds exactly the entries the three halves signed (OG-rl-15)\"" % (ENTRIES,))
    t = t.replace(old, new)
    return t.replace("# the shipped file is EMPTY of domains, and with BOTH tables empty", "# the shipped file holds the signed domains (OG-rl-15; it shipped empty before), and with BOTH TABLES EMPTY in config")


def e3(t):
    a = "# MAIL_SENDER_DOMAIN_TABLE (NFRA_OPLGTW OG-md-1, PRD v1.9 C7): one sender domain per line; this file ships EMPTY."
    b = "# While it holds no domain, the headless mail route admits NOTHING by domain and refuses every sender_domain request 403."
    assert a in t and b in t
    return (t.replace(a, "# MAIL_SENDER_DOMAIN_TABLE (NFRA_OPLGTW OG-md-1, PRD v1.9 C7): one sender domain per line; OG-rl-15 ships the entries signed below.")
             .replace(b, "# While it holds no domain, the headless mail route admits NOTHING by domain and refuses every sender_domain request 403 (the OG-md-1 state)."))


def e4(t):
    old = 'assert set(got) < set(bound) and set(bound) - set(got) == CALLER_GRAPH_SCOPES["taxsma_workbook"].scopes'
    assert t.count(old) == 1
    return t.replace(old, 'assert set(got) <= set(bound) and set(bound) - set(got) <= CALLER_GRAPH_SCOPES["taxsma_workbook"].scopes')


rw("app/graph_scope_map.py", e1)
rw("tests/test_scoped_consent_r253.py", e4)
rw("tests/test_mail_route_domain.py", e2)
rw("deploy/mail_sender_domain_table.txt", e3)
print("release-time edits E1 E2 E3 applied to", wt)
