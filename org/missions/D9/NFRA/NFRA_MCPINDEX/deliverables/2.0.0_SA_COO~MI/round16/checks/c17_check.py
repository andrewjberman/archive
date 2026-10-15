"""c17_check.py -- grades MX-c-17 (the G5r enrichment of the 14 rival-fund rows), run from the repo root.

  python c17_check.py ac2   each of the 14 rows named in workflows/atom_decomposition/g5r_enrichment.json carries its additions (business_meaning ends with
                            meaning_add; never_sum_rules is a list ending with never_sum; nl_tags ends with nl_tags_add), and the set of table rows whose
                            bytes differ from BASE_REF is EXACTLY those 14 (no other row moved)

The rows' directory is workflows/atom_decomposition/catalog_entries, or C17_DIR (a planted copy). BASE is git ref BASE_REF read with `git show`.
Exit 0 PASS, 1 FAIL, 9 no run.
"""
import glob
import json
import os
import subprocess
import sys

import yaml

BASE_REF = "0f40810fa2"
ROWS = os.environ.get("C17_DIR") or "workflows/atom_decomposition/catalog_entries"
ENRICH = "workflows/atom_decomposition/g5r_enrichment.json"
BASE_ROWS = "workflows/atom_decomposition/catalog_entries"


def base_bytes(name):
    r = subprocess.run(["git", "show", "%s:%s/%s.yaml" % (BASE_REF, BASE_ROWS, name)], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "ac2":
        print(__doc__)
        return 9
    enr = json.load(open(ENRICH, encoding="utf-8"))["rows"]
    res = []
    for ent, e in sorted(enr.items()):
        p = os.path.join(ROWS, ent + ".yaml")
        if not os.path.exists(p):
            res.append(("row %s exists" % ent, False))
            continue
        d = yaml.safe_load(open(p, encoding="utf-8"))
        bm, ns, tags = str(d.get("business_meaning", "")), d.get("never_sum_rules"), d.get("nl_tags") or []
        ok = (bm.endswith(e["meaning_add"]) and isinstance(ns, list) and ns and ns[-1] == e["never_sum"]
              and list(tags)[-len(e["nl_tags_add"]):] == list(e["nl_tags_add"]))
        res.append(("row %s carries its G5r additions" % ent, ok))
    names = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ROWS, "*.yaml"))
                   if not os.path.basename(p).startswith(("need_", "harvest_")))
    changed = []
    for n in names:
        b = base_bytes(n)
        if b is None:
            continue   # a row the base lacks is not a table row of the base set
        if b != open(os.path.join(ROWS, n + ".yaml"), "rb").read():
            changed.append(n)
    print("DENOMINATOR table rows %d; enriched %d; rows whose bytes differ from %s: %d" % (len(names), len(enr), BASE_REF, len(changed)))
    res.append(("the rows that differ from the base are exactly the %d enriched ones" % len(enr), sorted(changed) == sorted(enr)))
    if sorted(changed) != sorted(enr):
        print("  differ but not enriched: %s" % ", ".join(sorted(set(changed) - set(enr))[:6]))
        print("  enriched but unchanged:  %s" % ", ".join(sorted(set(enr) - set(changed))[:6]))
    for name, ok in res:
        if not ok:
            print("CHECK FAIL: %s" % name)
    ok = bool(res) and all(o for _n, o in res)
    print("CHECKS pass %d of %d" % (sum(1 for _n, o in res if o), len(res)))
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
