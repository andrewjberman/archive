"""plant_r15.py -- the issuer's cut-time planted arms for r15.AC4 (host output supplied by R15_AC4_HOST_OUT, the tree catalog by R15_TREE_CATALOG). Run from the repo root."""
import copy
import os
import subprocess
import sys
import tempfile

import yaml

S = "C:/Users/OPALBL~1/AppData/Local/Temp/claude/C--Users-Opal-Bloomberg-Desktop-ajb-workspace/0c774c5b-0103-40e0-9257-b71087af27bc/scratchpad"
C = "org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/round18/checks"
tmp = tempfile.mkdtemp(prefix="plant_r15_")
cat = yaml.safe_load(open(S + "/DATA_CATALOG.merged_c21.yaml", encoding="ascii"))
SECS = ("silver_datasets", "portal_datasets", "harvest_datasets")
for s in SECS:
    for r in cat[s]:
        r.pop("nl_tags_basis", None)


def dump(c, name):
    p = os.path.join(tmp, name)
    with open(p, "w", encoding="ascii", newline="\n") as fh:
        yaml.safe_dump(c, fh, sort_keys=False, allow_unicode=False, width=1000000)
    return p


def host_out(path):
    r = subprocess.run([sys.executable, C + "/r15_ac4_host.py", path], capture_output=True, text=True, check=True)
    p = os.path.join(tmp, "host_" + os.path.basename(path) + ".txt")
    open(p, "w", encoding="ascii", newline="\n").write(r.stdout)
    return p


good = dump(cat, "good.yaml")
inf = copy.deepcopy(cat)
inf["silver_datasets"][0]["nl_tags_basis"] = "inferred"
nobk = copy.deepcopy(cat)
nobk["harvest_datasets"][0].pop("bucket")
inf_p, nobk_p = dump(inf, "inferred.yaml"), dump(nobk, "nobucket.yaml")
arms = [("good: host equals tree, 0 inferred, a bucket on every row", host_out(good), good, 0), ("a row still inferred", host_out(inf_p), inf_p, 1),
        ("a row without a bucket", host_out(nobk_p), nobk_p, 1), ("the host differs from the tree (md5 and counts)", host_out(good), inf_p, 1)]
ok = wrong = 0
for label, hostf, treef, want in arms:
    r = subprocess.run(["bash", C + "/r15.AC4.sh"], env=dict(os.environ, R15_AC4_HOST_OUT=hostf, R15_TREE_CATALOG=treef), capture_output=True, text=True)
    if r.returncode == want:
        ok += 1
        print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
    else:
        wrong += 1
        print("ARM WRONG: %s -> rc=%d want %d\n%s" % (label, r.returncode, want, "\n".join(r.stdout.splitlines()[-5:])))
print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
sys.exit(0 if wrong == 0 else 1)
