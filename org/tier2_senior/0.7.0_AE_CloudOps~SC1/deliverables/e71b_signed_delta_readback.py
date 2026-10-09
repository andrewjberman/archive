"""e71b POST-ACT SIGNED-DELTA READ-BACK -- grade the real delta against the delta the halves signed.

Signed delta, on the 15 snapshot rows:
  updated_by      mdpf-secclass-remap-b -> seed-script   on all 15
  low_confidence  True -> ABSENT                         on all 15
  name            -> clean_name()'s output               on the 12 only (NOT LIPKX VSMGX VTIVX)
  asset_class / sub_asset_class                          MUST NOT MOVE on any row
  every other field                                      MUST NOT MOVE
last_updated is EXCLUDED here and only here: the act is its writer, so a move is expected, and
including it would mask the fields that matter. The pre-act arm (e71b_snapshot_recheck.py) is
where last_updated carries the "has anything else written this row" signal.

An UNSIGNED move on any field is a failure, printed with its denominator. Exit 2 on any failure.
"""
import json
import sys
from decimal import Decimal

import boto3

SNAPSHOT = "org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E71_SEED_ROWS_SNAPSHOT_20261009.json"
TABLE = "etf-classifications"
REGION = "us-east-1"
CLEAN_12 = set("AAETX AMECX CAIBX CFIHX CLBAX FBALX FKIQX FTYPX KAGIX MDLOX SGIIX VTTHX".split())
CLASS_FIELDS = ("asset_class", "sub_asset_class")
ABSENT = "<absent>"


def plain(value):
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, (list, set, tuple)):
        return sorted(plain(v) for v in value)
    return value


def main() -> int:
    with open(SNAPSHOT, encoding="utf-8") as fh:
        rows = json.load(fh)["rows"]
    keys = sorted(rows)
    table = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)

    by_ok = lc_ok = name_ok = name_held = class_ok = 0
    unsigned = []
    for k in keys:
        got = table.get_item(Key={"ticker": k}, ConsistentRead=True).get("Item")
        if got is None:
            unsigned.append("%s ABSENT from the table" % k)
            continue
        live = {f: plain(v) for f, v in got.items()}
        want = {f: plain(v) for f, v in rows[k].items()}

        if live.get("updated_by", ABSENT) == "seed-script":
            by_ok += 1
        else:
            unsigned.append("%s updated_by=%r, signed seed-script" % (k, live.get("updated_by", ABSENT)))

        if "low_confidence" not in live:
            lc_ok += 1
        else:
            unsigned.append("%s low_confidence still present (%r)" % (k, live["low_confidence"]))

        if k in CLEAN_12:
            if live.get("name") != want.get("name"):
                name_ok += 1
            else:
                unsigned.append("%s name did NOT move, signed clean" % k)
        else:
            if live.get("name") == want.get("name"):
                name_held += 1
            else:
                unsigned.append("%s name MOVED, signed to hold: %r -> %r"
                                % (k, want.get("name"), live.get("name")))

        moved_class = [f for f in CLASS_FIELDS
                       if live.get(f, ABSENT) != want.get(f, ABSENT)]
        if moved_class:
            unsigned.append("%s CLASS FIELD MOVED: %s" % (k, moved_class))
        else:
            class_ok += 1

        signed = {"updated_by", "low_confidence", "name", "last_updated"}
        for f in sorted(set(live) | set(want)):
            if f in signed:
                continue
            if live.get(f, ABSENT) != want.get(f, ABSENT):
                unsigned.append("%s UNSIGNED field move %s: %r -> %r"
                                % (k, f, want.get(f, ABSENT), live.get(f, ABSENT)))

    n = len(keys)
    print("E71B-READBACK denominator=%d" % n)
    print("  updated_by -> seed-script        : %d of %d" % (by_ok, n))
    print("  low_confidence -> ABSENT         : %d of %d" % (lc_ok, n))
    print("  name cleaned (the 12)            : %d of %d" % (name_ok, len(CLEAN_12)))
    print("  name held (LIPKX VSMGX VTIVX)    : %d of %d" % (name_held, n - len(CLEAN_12)))
    print("  class fields byte-equal           : %d of %d" % (class_ok, n))
    print("  UNSIGNED moves                    : %d" % len(unsigned))
    for u in unsigned:
        print("    %s" % u)
    ok = (by_ok == lc_ok == class_ok == n and name_ok == len(CLEAN_12)
          and name_held == n - len(CLEAN_12) and not unsigned)
    print("VERDICT: %s" % ("the real delta EQUALS the signed delta, nothing else moved"
                           if ok else "FAILURE -- see the lines above"))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
