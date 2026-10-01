"""Route-name and secret-name read for a TRNSPT-DEPS headless route (PRD v1.3 C7). Run from the worktree root.

usage: python _names.py <route_key> <route_names.json>
<route_key> is `transcripts` or `mail`. The JSON (written by the build cell) carries, per route key:
  prefix, secret_name, bearer_label.
v1.3 C7: a route path is not a lib/opal_naming.py kind, so the prefixes are the FIXED LITERALS below, graded for
distinctness only: not under /ms/, not a prefix of the other route's literal, and not already present in
app/server.py at the cut base (the merge-base with CLOUD), so it collides with no mounted route. Bearer secrets keep
the SECRET grammar: grade(secret_name, "SECRET") must read CONFORMANT.
Checks: prefix == the literal; the three distinctness arms; the secret grades CONFORMANT; the prefix literal occurs
in the gateway app code; no other route key shares the prefix or the secret name.
Last line: NAMES <ok|FAIL> <route_key>.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
from lib.opal_naming import grade  # noqa: E402

LITERALS = {"transcripts": "/hx/transcripts", "mail": "/hx/mail"}  # PRD v1.3 C7, verbatim

key, path = sys.argv[1], sys.argv[2]
doc = json.load(open(path, encoding="utf-8"))
r = doc[key]
pre = r.get("prefix")
ok = pre == LITERALS[key]
print("prefix: committed %r v1.3 literal %r" % (pre, LITERALS[key]))
under_ms = (pre or "").startswith("/ms/") or pre == "/ms"
print("prefix under /ms/: %s" % under_ms)
ok &= not under_ms
other = [v for k, v in LITERALS.items() if k != key][0]
nested = (pre or "\0").startswith(other) or other.startswith(pre or "\0")
print("prefix nests with %r: %s" % (other, nested))
ok &= not nested
server = "infra/aws/ec2/opal-gateway/app/server.py"
MODULES = {"transcripts": "infra/aws/ec2/opal-gateway/app/transcript_route.py",
           "mail": "infra/aws/ec2/opal-gateway/app/mail_route.py"}
# The CUT BASE is the parent of the commit that ADDED this route's module (so a drained branch still grades against
# the tree before the cell); before the module exists it is the merge-base with CLOUD.
added = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "HEAD", "--", MODULES[key]],
                       capture_output=True, text=True).stdout.split()
if added:
    base = subprocess.run(["git", "rev-parse", added[-1] + "^"], capture_output=True, text=True).stdout.strip()
else:
    base = subprocess.run(["git", "merge-base", "HEAD", "CLOUD"], capture_output=True, text=True).stdout.strip()
if base:
    at_base = subprocess.run(["git", "show", "%s:%s" % (base, server)], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
    if at_base.returncode == 0:
        coll = at_base.stdout.count(pre or "\0")
        print("prefix occurrences in %s at base %s: %d" % (server, base[:10], coll))
        ok &= coll == 0
    else:
        print("prefix collision: UNREAD (git show rc=%d)" % at_base.returncode)
        ok = False
else:
    print("prefix collision: UNREAD (no merge-base with CLOUD)")
    ok = False
try:
    verdict = grade(r.get("secret_name") or "", "SECRET")
except Exception as e:  # a name the rule cannot place is reported, never worked around
    verdict = ("REFUSED: %s" % e, None)
print("secret: %r grade %r" % (r.get("secret_name"), verdict))
ok &= verdict[0] == "CONFORMANT"
app = os.path.join("infra", "aws", "ec2", "opal-gateway", "app")
hits = sum(open(os.path.join(dp, f), encoding="utf-8", errors="replace").read().count(pre or "\0")
           for dp, _d, fs in os.walk(app) for f in fs if f.endswith(".py"))
print("prefix literal occurrences in app/*.py: %d" % hits)
ok &= hits >= 1
others = [k for k in doc if k != key]
clash = [k for k in others if doc[k].get("prefix") == pre or doc[k].get("secret_name") == r.get("secret_name")]
print("route keys sharing this prefix or secret: %d of %d" % (len(clash), len(others)))
ok &= not clash
print("NAMES %s %s" % ("ok" if ok else "FAIL", key))
