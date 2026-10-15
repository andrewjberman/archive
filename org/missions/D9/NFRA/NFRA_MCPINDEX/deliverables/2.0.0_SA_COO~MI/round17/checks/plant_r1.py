"""plant_r1.py -- the ISSUER's cut-time planted arms for r1.AC1 to AC3 (standing battery clause 1). NOT given to the worker, NOT a criterion. Run from the repo root.

Inputs from the issuer's scratchpad (S, argv[1]): r1rows/ (the generator run against the 99-tool census, 15 rows changed), DATA_CATALOG.r1_trial.yaml (the catalog emitted with the
7 right rows and the pending members, --overlay-ref 06cfb6db64). Builds a good entries folder (the repo's rows with the 7 right rows replaced) and bad ones; runs r1_check with
R1_ENTRIES / R1_CATALOG set and compares every exit code with the wanted one."""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r1_check as rc  # noqa: E402

S = sys.argv[1]
SRC = "workflows/atom_decomposition/catalog_entries"
trial = os.path.join(S, "DATA_CATALOG.r1_trial.yaml")
tmp = tempfile.mkdtemp(prefix="plant_r1_")


def entries(name, rows):
    d = os.path.join(tmp, name)
    shutil.copytree(SRC, d)
    for e in rows:
        shutil.copyfile(os.path.join(S, "r1rows", e + ".yaml"), os.path.join(d, e + ".yaml"))
    return d


good = entries("good", list(rc.EXPECT))
fifteen = entries("fifteen", [os.path.basename(p)[:-5] for p in glob.glob(os.path.join(S, "r1rows", "*.yaml"))
                              if yaml.safe_load(open(p, encoding="utf-8")) != yaml.safe_load(open(os.path.join(SRC, os.path.basename(p)), encoding="utf-8"))])
six = entries("six", list(rc.EXPECT)[:-1])
other = entries("other", list(rc.EXPECT))
o = os.path.join(other, "opal_data_etfs_gold_book.yaml")
d = yaml.safe_load(open(o, encoding="utf-8"))
d["nl_tags"] = list(d.get("nl_tags") or []) + ["an unrelated edit"]
with open(o, "w", encoding="utf-8", newline="\n") as fh:
    yaml.safe_dump(d, fh, sort_keys=False)
cur = rc.GW + "/app/refs/DATA_CATALOG.yaml"
# a catalog that drops the six pending members (tool index 93) and one that adds an unrelated row edit
cat = yaml.safe_load(open(trial, encoding="ascii").read())
cat_edit = yaml.safe_load(open(trial, encoding="ascii").read())
cat_edit["silver_datasets"][0]["business_meaning"] = cat_edit["silver_datasets"][0]["business_meaning"] + " An unrelated edit."
edit_path = os.path.join(tmp, "cat_edit.yaml")
with open(edit_path, "w", encoding="ascii", newline="\n") as fh:
    yaml.safe_dump(cat_edit, fh, sort_keys=False, allow_unicode=False)

arms = [("good rows, ac1", "ac1", good, trial, 0), ("good catalog, ac2", "ac2", good, trial, 0), ("good catalog, ac3", "ac3", good, trial, 0),
        ("the 15 contract-proposed rows (8 false readers), ac1", "ac1", fifteen, trial, 1), ("only 6 of the 7 rows, ac1", "ac1", six, trial, 1),
        ("an unrelated row edit (gold_book tags), ac1", "ac1", other, trial, 1),
        ("the current catalog (tool index 93), ac2", "ac2", good, cur, 1), ("the current catalog (no 7 rows), ac3", "ac3", good, cur, 1),
        ("an unrelated edit in a catalog row, ac3", "ac3", good, edit_path, 1)]
ok = wrong = 0
for label, ac, ent, catalog, want in arms:
    r = subprocess.run([sys.executable, os.path.join(HERE, "r1_check.py"), ac], env=dict(os.environ, R1_ENTRIES=ent, R1_CATALOG=catalog), capture_output=True, text=True, timeout=290)
    if r.returncode == want:
        ok += 1
        print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
    else:
        wrong += 1
        print("ARM WRONG: %s -> rc=%d want %d\n%s" % (label, r.returncode, want, "\n".join(r.stdout.splitlines()[-6:])))
print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
shutil.rmtree(tmp, ignore_errors=True)
sys.exit(0 if wrong == 0 else 1)
