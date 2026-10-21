#!/usr/bin/env python
"""OG-rl-18 Phase A step 2: take the ELEVEN files of the seventeenth release into the release tree (bytes, no newline translation) WHOLE from trunk_sha, and change the manifest's ONE key (mcportal_commit) by text edit.
usage: python rl18_take.py <live_ref> <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch17)
Prints, per file, the live->trunk hunk count. NOT taken: anything else."""
import json
import os
import re
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch17"
LIVE, TRUNK, OUT = [a for a in sys.argv[1:] if not a.startswith("--")][:3]
G = "infra/aws/ec2/opal-gateway/"
APP = ["app/data_entitlement.py", "app/account_ref.py", "app/integrations/schwab/integration.py", "app/server.py", "app/token_broker.py", "app/admin_api.py", "app/refs/DATA_CATALOG.yaml"]
TESTS = ["tests/test_og_rt1.py", "tests/test_og_ed1.py", "tests/test_scoped_consent_r253.py", "tests/test_login_admit_r24.py", "tests/test_og_mp1.py"]
MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"
taken = []
for rel in APP + TESTS:
    p = G + rel
    r = subprocess.run(["git", "show", "%s:%s" % (TRUNK, p)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("absent at trunk: " + p)
    full = os.path.join(TREE, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "wb").write(r.stdout)
    d = subprocess.run(["git", "diff", "-U0", LIVE, TRUNK, "--", p], capture_output=True).stdout.decode("utf-8", "replace")
    new_at_live = subprocess.run(["git", "cat-file", "-e", "%s:%s" % (LIVE, p)], capture_output=True).returncode != 0
    taken.append({"path": p, "bytes": len(r.stdout), "live_to_trunk_hunks": len(re.findall(r"(?m)^@@ ", d)), "new_file": new_at_live})
# the manifest: EXACTLY one key, by text edit of the live copy (no re-serialisation)
text = subprocess.run(["git", "show", "%s:%s" % (LIVE, MANIFEST)], capture_output=True).stdout.decode("utf-8")
gw = json.loads(text)["services"]["opal-gateway"]
old_pin = gw.get("mcportal_commit")
PIN = "a577f99afc81df4a42c1740c78cf58270c8991e5"
if old_pin != "21ad40432cae0d09c5ab9d806307944baaf45cb9":
    raise SystemExit("REFUSED: the live manifest pin is %r, not batch16's" % old_pin)
n = text.count('"mcportal_commit": "%s"' % old_pin)
print("manifest: mcportal_commit %r occurrences of that exact pair: %d" % (old_pin, n))
if n != 1:
    raise SystemExit("REFUSED: the pair occurs %d times" % n)
open(os.path.join(TREE, MANIFEST), "wb").write(text.replace('"mcportal_commit": "%s"' % old_pin, '"mcportal_commit": "%s"' % PIN).encode("utf-8"))
out = {"taken": taken, "manifest": {"old_mcportal_commit": old_pin, "new_mcportal_commit": PIN}}
json.dump(out, open(OUT, "w"), indent=1)
print("taken whole from trunk: %d" % len(taken))
for t in taken:
    print("  take %-58s %7d bytes, hunks %3d%s" % (t["path"].split("opal-gateway/")[1], t["bytes"], t["live_to_trunk_hunks"], " (new)" if t["new_file"] else ""))
