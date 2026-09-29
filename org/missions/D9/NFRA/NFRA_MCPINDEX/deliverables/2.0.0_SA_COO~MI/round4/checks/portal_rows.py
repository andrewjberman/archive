"""x2_catalog.py -- MX-x-2 AC1 helper (row Z-W3-S4, as amended A1 on the CTO's ruling of Z-W13-S3 @8ed938b2d7).

Every catalog row whose entity starts with `portal_` sits in the catalog's own `portal_datasets:` section and names
WHERE it is read -- `read_tool` and `accessor`, equal to the portal_index integration's own ROWS entry for that entity
-- and carries NO raw key literal (`s3_key`). None sits under `silver_datasets:`.

usage: python portal_rows.py <DATA_CATALOG.yaml> <portal_index/integration.py> [min_rows=3]
"""
import re
import sys

import yaml

ROW_RE = re.compile(r'"([a-z0-9_]+)"\s*:\s*ToolRow\(\s*"([A-Za-z0-9_]+)"\s*,\s*"([a-z0-9_]+)"')


def main():
    cat = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
    src = open(sys.argv[2], encoding="utf-8").read()
    rows = {m.group(3): (m.group(1), m.group(2)) for m in ROW_RE.finditer(src)}   # entity -> (tool, accessor)
    silver = cat.get("silver_datasets") or []
    portal = cat.get("portal_datasets") or []
    in_silver = [r.get("entity") for r in silver if str(r.get("entity", "")).startswith("portal_")]
    in_portal = [r for r in portal if str(r.get("entity", "")).startswith("portal_")]
    good, bad = 0, []
    for r in in_portal:
        want = rows.get(r.get("entity"))
        if "s3_key" in r:
            bad.append("%s: carries s3_key" % r.get("entity"))
        elif not want:
            bad.append("%s: no portal_index ROWS entry" % r.get("entity"))
        elif (r.get("read_tool"), r.get("accessor")) != want:
            bad.append("%s: read_tool/accessor do not equal portal_index ROWS" % r.get("entity"))
        else:
            good += 1
    n = len(in_silver) + len(in_portal)
    print("portal_index ROWS entries read: %d" % len(rows))
    print("portal rows: %d total; under silver_datasets %d; under portal_datasets %d" % (n, len(in_silver), len(in_portal)))
    for b in bad:
        print("  " + b)
    print("placed and naming their reader %d of %d" % (good, n))
    need = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    print("minimum rows required: %d" % need)
    return 0 if (n >= need and good == n and len(rows) >= need) else 1


if __name__ == "__main__":
    sys.exit(main())
