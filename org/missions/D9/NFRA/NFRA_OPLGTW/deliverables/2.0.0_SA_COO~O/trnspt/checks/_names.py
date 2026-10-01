"""Builder-name and /ms/* invariance read for a TRNSPT-DEPS headless route. Run from the worktree root.

usage: python _names.py <route_key> <route_names.json>
<route_key> is `transcripts` or `mail`. The JSON (written by the build cell) carries, per route key:
  prefix, prefix_builder {system, scope, function, kind, qualifier}, secret_name, secret_builder {...}, bearer_label.
Checks: secret_name == lib.opal_naming.name(**secret_builder); prefix == "/" + name(**prefix_builder); the prefix
literal occurs in the gateway app code; no other route key shares the prefix or the secret name.
Last line: NAMES <ok|FAIL> <route_key>.
"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from lib.opal_naming import name  # noqa: E402

key, path = sys.argv[1], sys.argv[2]
doc = json.load(open(path, encoding="utf-8"))
r = doc[key]
ok = True
try:
    sec = name(**r["secret_builder"])
except Exception as e:  # a refusal is a missing registry row (rule 30), reported, never worked around
    sec = "REFUSED: %s" % e
try:
    pre = "/" + name(**r["prefix_builder"])
except Exception as e:
    pre = "REFUSED: %s" % e
print("secret: committed %r builder %r" % (r.get("secret_name"), sec))
print("prefix: committed %r builder %r" % (r.get("prefix"), pre))
ok &= sec == r.get("secret_name") and pre == r.get("prefix")
app = os.path.join("infra", "aws", "ec2", "opal-gateway", "app")
hits = sum(open(os.path.join(dp, f), encoding="utf-8", errors="replace").read().count(r.get("prefix") or "\0")
           for dp, _d, fs in os.walk(app) for f in fs if f.endswith(".py"))
print("prefix literal occurrences in app/*.py: %d" % hits)
ok &= hits >= 1
others = [k for k in doc if k != key]
clash = [k for k in others if doc[k].get("prefix") == r.get("prefix") or doc[k].get("secret_name") == r.get("secret_name")]
print("route keys sharing this prefix or secret: %d of %d" % (len(clash), len(others)))
ok &= not clash
print("NAMES %s %s" % ("ok" if ok else "FAIL", key))
