"""plant_c17.py -- the ISSUER's cut-time planted arms for c17.AC2 (standing battery clause 1). NOT given to the worker, NOT a criterion. Run from the repo root."""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "workflows/atom_decomposition/catalog_entries"
ENRICH = "workflows/atom_decomposition/g5r_enrichment.json"
sys.path.insert(0, HERE)
import c17_check as cc  # noqa: E402


def copy_rows(dst):
    os.makedirs(dst)
    for ent in glob.glob(SRC + "/*.yaml"):
        n = os.path.basename(ent)[:-5]
        b = cc.base_bytes(n)
        if b is not None:   # the BASE bytes, so the plant never inherits a worker's edit
            open(os.path.join(dst, n + ".yaml"), "wb").write(b)


def enrich(dst, skip_tag=None):
    enr = json.load(open(ENRICH, encoding="utf-8"))["rows"]
    for ent, e in enr.items():
        p = os.path.join(dst, ent + ".yaml")
        d = yaml.safe_load(open(p, encoding="utf-8"))
        d["business_meaning"] = d["business_meaning"] + " " + e["meaning_add"]
        rules = d["never_sum_rules"]
        d["never_sum_rules"] = (rules if isinstance(rules, list) else []) + [e["never_sum"]]
        tags = list(e["nl_tags_add"])
        if skip_tag and ent == skip_tag:
            tags = tags[:-1]
        d["nl_tags"] = list(d["nl_tags"]) + tags
        yaml.safe_dump(d, open(p, "w", encoding="utf-8", newline="\n"), sort_keys=False, allow_unicode=True)


def main():
    tmp = tempfile.mkdtemp(prefix="plant17_")
    good = os.path.join(tmp, "good")
    copy_rows(good)
    enrich(good)
    base = os.path.join(tmp, "base")
    copy_rows(base)
    short = os.path.join(tmp, "short")
    copy_rows(short)
    enrich(short, skip_tag="opal_data_etfs_gold_canonical_shape")
    extra = os.path.join(tmp, "extra")
    shutil.copytree(good, extra)
    victim = sorted(p for p in glob.glob(extra + "/opal_data_*.yaml") if "etfs_gold" not in p)[0]
    open(victim, "a", encoding="utf-8").write("# touched\n")
    arms = [("good rows, ac2", good, 0), ("base rows (nothing enriched), ac2", base, 1), ("one tag missing, ac2", short, 1),
            ("an unrelated row touched, ac2", extra, 1)]
    ok = wrong = 0
    for label, d, want in arms:
        r = subprocess.run([sys.executable, os.path.join(HERE, "c17_check.py"), "ac2"], env=dict(os.environ, C17_DIR=d), capture_output=True, text=True)
        if r.returncode == want:
            ok += 1
            print("ARM ok:    %s -> rc=%d" % (label, r.returncode))
        else:
            wrong += 1
            print("ARM WRONG: %s -> rc=%d want %d" % (label, r.returncode, want))
            print("\n".join(r.stdout.splitlines()[-5:]))
    print("PLANTED ARMS: ok %d, wrong %d" % (ok, wrong))
    return 0 if wrong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
