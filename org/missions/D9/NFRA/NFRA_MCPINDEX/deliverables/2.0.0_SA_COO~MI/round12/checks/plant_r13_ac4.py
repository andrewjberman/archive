"""plant_r13_ac4.py -- the ISSUER's cut-time planted arms for r13.AC4 (standing battery clause 1). NOT given to the worker, NOT a criterion. Run from the repo root.
r13.AC4 reads the host's output from R13_AC4_HOST_OUT when it is set. The good host output is built from THIS tree's catalog (so it equals the tree); the bad ones change one thing."""
import hashlib
import os
import subprocess
import sys
import tempfile

import yaml

P = "infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"
CHECK = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round12/checks/r13.AC4.sh"
raw = open(P, "rb").read()
cat = yaml.safe_load(raw.decode("ascii"))
table = [r for k in ("silver_datasets", "portal_datasets") for r in (cat.get(k) or []) if isinstance(r, dict) and "contract" in r]
tools = sorted({str(r["read_tool"]) for s in ("silver_datasets", "portal_datasets", "harvest_datasets") for r in (cat.get(s) or []) if isinstance(r, dict) and r.get("read_tool")})


def out(version=None, harvest=None, md5=None, extra_tool=None):
    t = tools + ([extra_tool] if extra_tool else [])
    return ("CATALOG version=%s harvest=%d table=%d key_template=%d retired=%d\nTOOLS %s\nMD5 %s\n" % (
        version or cat["version"], harvest if harvest is not None else len(cat["harvest_datasets"]), len(table),
        sum(1 for r in table if r.get("key_template")), sum(1 for r in table if r.get("retired") is True), ",".join(t),
        md5 or hashlib.md5(raw).hexdigest()))


arms = [("host equals the tree (good)", out(), 0), ("host catalog version 0.4", out(version="0.4"), 1), ("host harvest rows 39", out(harvest=39), 1),
        ("host md5 differs from the tree", out(md5="0" * 32), 1), ("host names a tool the deployed commit does not serve", out(extra_tool="zz_not_a_served_tool"), 1)]
ok = wrong = 0
for label, text, want in arms:
    f = os.path.join(tempfile.mkdtemp(prefix="plant_ac4_"), "host.txt")
    open(f, "w", encoding="ascii", newline="\n").write(text)
    r = subprocess.run(["bash", CHECK], env=dict(os.environ, R13_AC4_HOST_OUT=f), capture_output=True, text=True)
    if r.returncode == want:
        ok += 1
        print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
    else:
        wrong += 1
        print("ARM WRONG: %s -> rc=%d want %d\n%s" % (label, r.returncode, want, "\n".join(r.stdout.splitlines()[-4:])))
print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
sys.exit(0 if wrong == 0 else 1)
