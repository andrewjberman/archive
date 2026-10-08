#!/usr/bin/env python3
"""armC_run -- run the FWD-6 design's arm C act (round 7) through the root check's own decision and print the lines.

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/armC_run.py

The act: a NEW Lambda named `daily-pull` (it carries no system word; the grader prints the form `{system}-daily-pull-lambda`)
is added to the item list of the root `infra/aws/terraform/investor-reporting/directory` and the root check's `check_root`
decides it. This is what the design's place() does for one staged name. Three runs, each against its own map:
  control : the registry's root map as it is (the entry gives the system)            -> FIX irpt-daily-pull-lambda
  C       : a COPY of the map with the root's entry removed (an unmapped root)       -> HOLE, {system}: no map entry for this root
  C2      : a COPY of the map whose entry for the root has fills ["scope"]           -> HOLE, the multi-firm clause
Copies are written under <repo>/.scratch/armC/ (untracked) and never under infra/; the registry is read, never written.
Run from the repository root. Last line, printed once: ARMC ok=<bool> control=<kind> c=<kind> c2=<kind>
Python 3.9; ASCII only; standard library only.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def repo_root(start):
    d = start
    for _ in range(40):
        if os.path.isdir(os.path.join(d, ".tools")) and os.path.isdir(os.path.join(d, "org")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("ARMC ok=False (no repository root above %s)" % start)


ROOT = repo_root(HERE)
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_rootcheck  # noqa: E402
import opal_naming_scope  # noqa: E402

REAL_MAP = "infra/logic/registry/root_map.json"
ROOT_DIR = "infra/aws/terraform/investor-reporting/directory"
MAP_KEY = "investor-reporting/directory"
NEW = {"plane": "repo", "type": "LAMBDA", "current": "daily-pull", "where": ROOT_DIR + "/schedule.tf:9999"}
SCRATCH = os.path.join(ROOT, ".scratch", "armC")


def run(map_path):
    real = opal_naming_scope.root_names

    def with_new(root, mp=None):
        items, unc, st = real(root, mp)
        return list(items) + [dict(NEW)], unc, st

    opal_naming_scope.root_names = with_new
    buf = []
    try:
        opal_naming_rootcheck.check_root(ROOT_DIR, map_path, out=buf.append, report_only=True)
    finally:
        opal_naming_scope.root_names = real
    return [ln for ln in buf if " daily-pull " in ln]


def main():
    with open(REAL_MAP, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    os.makedirs(SCRATCH, exist_ok=True)
    c_doc = copy.deepcopy(doc)
    del c_doc["roots"][MAP_KEY]
    c2_doc = copy.deepcopy(doc)
    c2_doc["roots"][MAP_KEY]["fills"] = ["scope"]
    paths = {}
    for tag, d in (("c", c_doc), ("c2", c2_doc)):
        paths[tag] = os.path.join(SCRATCH, "root_map.%s.json" % tag)
        with open(paths[tag], "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, indent=1)
    kinds = {}
    for tag, mp in (("control", REAL_MAP), ("c", paths["c"]), ("c2", paths["c2"])):
        lines = run(mp)
        print("--- %s (map: %s)" % (tag, mp.replace("\\", "/")))
        for ln in lines:
            print(ln)
        kinds[tag] = lines[0].split(" ", 1)[0] if len(lines) == 1 else "NONE"
    ok = (kinds["control"] == "FIX" and kinds["c"] == "HOLE" and kinds["c2"] == "HOLE")
    print("ARMC ok=%s control=%s c=%s c2=%s" % (ok, kinds["control"], kinds["c"], kinds["c2"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
