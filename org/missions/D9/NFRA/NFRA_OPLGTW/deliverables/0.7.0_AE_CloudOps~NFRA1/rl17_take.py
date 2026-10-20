#!/usr/bin/env python
"""OG-rl-17 Phase A step 2: take the 25 files of the sixteenth release into the release tree (bytes, no newline translation) WHOLE from trunk_sha, and make the manifest's TWO key changes by text edit.
usage: python rl17_take.py <live_ref> <trunk_sha> <out.json>   (repository root; the tree is C:/tmp/og-rel-batch16)
Prints, per file, the live->trunk hunk count (attributed to the cells by hand in the ask). NOT taken: anything else."""
import json
import os
import re
import subprocess
import sys

TREE = "C:/tmp/og-rel-batch16"
LIVE, TRUNK, OUT = [a for a in sys.argv[1:] if not a.startswith("--")][:3]
G = "infra/aws/ec2/opal-gateway/"
APP = ["app/client_core.py", "app/client_adapter_bdcottonwood.py", "app/family_depth.py", "app/integrations/ycharts/integration.py", "app/integrations/opal_portal/integration.py", "app/harvest_typed.py",
       "app/integrations/portal_index/integration.py", "app/integrations/opal_discover/integration.py", "app/inflight_guard.py", "app/tools.py", "app/admin_gateway_breakdown.py", "app/news_typed.py", "app/admin_people_access.py",
       "deploy/NFRA_OPLGTW_CONTRACT.json"]
TESTS = ["tests/test_og_fc1.py", "tests/test_og_sx1.py", "tests/test_og_sz1.py", "tests/test_og_mg3.py", "tests/test_og_tp1.py", "tests/test_og_ix1.py", "tests/test_og_nf1.py", "tests/test_og_gt0.py", "tests/test_og_gt5.py",
         "tests/test_og_rv2.py", "tests/test_admin_people_access.py"]
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
# the manifest: EXACTLY two keys, by text edit of the live copy (no re-serialisation)
mtxt = subprocess.run(["git", "show", "%s:%s" % (LIVE, MANIFEST)], capture_output=True).stdout
text = mtxt.decode("utf-8")
m = json.loads(text)
gw = m["services"]["opal-gateway"]
old_mc, old_pin = gw.get("machine_type"), gw.get("mcportal_commit")
PIN = "21ad40432cae0d09c5ab9d806307944baaf45cb9"
n1 = len(re.findall(r'"machine_type":\s*"%s"' % re.escape(str(old_mc)), text))
print("manifest: machine_type %r (occurrences of that exact pair: %d), mcportal_commit %r" % (old_mc, n1, old_pin))
out = {"taken": taken, "manifest": {"old_machine_type": old_mc, "old_mcportal_commit": old_pin, "new_machine_type": "t4g.large", "new_mcportal_commit": PIN}}
json.dump(out, open(OUT, "w"), indent=1)
print("taken whole from trunk: %d" % len(taken))
for t in taken:
    print("  take %-58s %7d bytes, hunks %3d%s" % (t["path"].split("opal-gateway/")[1], t["bytes"], t["live_to_trunk_hunks"], " (new)" if t["new_file"] else ""))
