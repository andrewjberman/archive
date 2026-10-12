"""TCKT_VNEXT round 8 -- R8-ds-1: the disabled-users read has its three parts, its status counts sum to the
PROFILE denominator, every cited path exists, and no address is in the file.

Prints DS1-READ-OK <detail> or DS1-READ-FAIL <reason>; exit 0/1.
"""
import json
import os
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r8_ds1/DISABLED_USERS_READ_20261012.json"
KEYS = {"authorizer", "disabled_internal_rows", "status_values", "what_was_not_read", "claim"}


def main():
    try:
        raw = open(RES, encoding="utf-8").read()
        doc = json.loads(raw)
    except (OSError, ValueError) as e:
        print("DS1-READ-FAIL cannot read the result file: %s" % e)
        return 1
    if "@" in raw:
        print("DS1-READ-FAIL the file holds an address")
        return 1
    missing = sorted(KEYS - set(doc))
    if missing:
        print("DS1-READ-FAIL missing key(s): %s" % missing)
        return 1
    sv = doc["status_values"]
    counts = sv.get("counts") or {}
    total = sv.get("profile_rows")
    if not counts or not isinstance(total, int) or sum(counts.values()) != total:
        print("DS1-READ-FAIL status counts do not sum to profile_rows")
        return 1
    files = doc["authorizer"].get("files_read") or []
    absent = [f for f in files if not os.path.exists(str(f).split(":")[0])]
    if not files or absent:
        print("DS1-READ-FAIL authorizer files_read empty or absent: %s" % absent[:4])
        return 1
    if doc["claim"] not in ("measured", "inferred"):
        print("DS1-READ-FAIL claim must be measured or inferred")
        return 1
    print("DS1-READ-OK profile_rows=%d status_values=%d disabled_internal=%d files_read=%d" % (
        total, len(counts), len(doc["disabled_internal_rows"]), len(files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
