"""OG-rl-15 Phase A: the release-time edits that SHIPPING THE DOMAIN ENTRIES forces, applied to the (uncommitted) candidate. Each is a hunk that is in NO cell's own diff,
so each is named in the ask for the issuer's word (row Z-W43-S2, narrowed by row Z-W43-S6 after amendment A6 withdrew the Bloomberg rows and with them E1 and E4).
 E2 tests/test_mail_route_domain.py test_ogmd1_ac06 : the pin 'the shipped domain table holds no domain' becomes 'holds exactly the signed entries'.
 E3 deploy/mail_sender_domain_table.txt : the first two header comment lines said the file ships EMPTY; they now say it ships the signed entries.
 E4 deploy-to-ec2.sh : the MAIL_BEARER leg hunk (A7 D4 option A), built by r29_mail_bearer_leg_patch.py from the cell's own file. The one Terraform line is r29_tf_edit.py.
usage: python r29_release_time_edits.py <candidate worktree>"""
import os
import subprocess
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


rw("tests/test_mail_route_domain.py", e2)
rw("deploy/mail_sender_domain_table.txt", e3)
HERE = os.path.dirname(os.path.abspath(__file__))
dep = wt + G + "deploy-to-ec2.sh"
subprocess.run([sys.executable, os.path.join(HERE, "r29_mail_bearer_leg_patch.py"), dep, dep], check=True)   # E4
print("release-time edits E2 E3 E4 applied to", wt)
