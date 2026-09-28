"""x2_catalog.py -- MX-x-2 AC1 helper (row Z-W3-S4). Every catalog row whose entity starts with `portal_` sits in the
catalog's own `portal_datasets:` section and carries a non-empty `s3_key` field; none sits under `silver_datasets:`.

usage: python x2_catalog.py <DATA_CATALOG.yaml>
"""
import sys

import yaml


def main():
    cat = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
    silver = cat.get("silver_datasets") or []
    portal = cat.get("portal_datasets") or []
    in_silver = [r.get("entity") for r in silver if str(r.get("entity", "")).startswith("portal_")]
    in_portal = [r for r in portal if str(r.get("entity", "")).startswith("portal_")]
    keyed = [r for r in in_portal if str(r.get("s3_key") or "").strip()]
    n = len(in_silver) + len(in_portal)
    print("portal rows: %d total; under silver_datasets %d; under portal_datasets %d, of which with a non-empty s3_key %d"
          % (n, len(in_silver), len(in_portal), len(keyed)))
    print("placed and keyed %d of %d" % (len(keyed), n))
    return 0 if (n >= 3 and len(keyed) == n) else 1


if __name__ == "__main__":
    sys.exit(main())
