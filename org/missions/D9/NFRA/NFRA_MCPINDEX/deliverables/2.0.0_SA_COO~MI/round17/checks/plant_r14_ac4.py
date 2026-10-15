"""plant_r14_ac4.py -- the ISSUER's cut-time planted arms for r14.AC4 (standing battery clause 1). NOT given to the worker, NOT a criterion. Run from the repo root.
r14.AC4 reads the host's output from R14_AC4_HOST_OUT when it is set. The good host output is the round 17 counts with THIS tree's md5 and read_tool names; the bad ones change one thing."""
import hashlib
import os
import subprocess
import sys
import tempfile

import yaml

P = "infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"
CHECK = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round17/checks/r14.AC4.sh"
raw = open(P, "rb").read()
cat = yaml.safe_load(raw.decode("ascii"))
tools = sorted({str(r["read_tool"]) for s in ("silver_datasets", "portal_datasets", "harvest_datasets") for r in (cat.get(s) or []) if isinstance(r, dict) and r.get("read_tool")})
GOOD = "version=0.5 harvest=78 table=216 key_template=216 retired=5 rows=304 nl_tags=304 inferred=44 firm=24"


def out(counts=GOOD, md5=None, extra_tool=None):
    t = tools + ([extra_tool] if extra_tool else [])
    return "CATALOG %s\nTOOLS %s\nMD5 %s\n" % (counts, ",".join(t), md5 or hashlib.md5(raw).hexdigest())


arms = [("host equals the tree, round 17 counts (good)", out(), 0),
        ("host nl_tags 260 (T1 not live)", out(GOOD.replace("nl_tags=304", "nl_tags=260")), 1),
        ("host inferred 0", out(GOOD.replace("inferred=44", "inferred=0")), 1),
        ("host firm 23", out(GOOD.replace("firm=24", "firm=23")), 1),
        ("host harvest rows 39", out(GOOD.replace("harvest=78", "harvest=39")), 1),
        ("host md5 differs from the tree", out(md5="0" * 32), 1),
        ("host names a tool the deployed commit does not serve", out(extra_tool="zz_not_a_served_tool"), 1)]
ok = wrong = 0
for label, text, want in arms:
    f = os.path.join(tempfile.mkdtemp(prefix="plant_ac4_"), "host.txt")
    open(f, "w", encoding="ascii", newline="\n").write(text)
    r = subprocess.run(["bash", CHECK], env=dict(os.environ, R14_AC4_HOST_OUT=f), capture_output=True, text=True)
    if r.returncode == want:
        ok += 1
        print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
    else:
        wrong += 1
        print("ARM WRONG: %s -> rc=%d want %d\n%s" % (label, r.returncode, want, "\n".join(r.stdout.splitlines()[-4:])))
print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
sys.exit(0 if wrong == 0 else 1)
