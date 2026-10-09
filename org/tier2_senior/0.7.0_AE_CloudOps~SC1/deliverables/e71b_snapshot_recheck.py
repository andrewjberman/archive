"""e71b PRE-ACT SNAPSHOT RE-READ -- CTO condition 2, run immediately before step 4.

Re-reads each of the 15 snapshot rows with its own --consistent-read get-item and compares
EVERY field, last_updated INCLUDED: for "has this row moved since the issuer's 03:4xZ
snapshot", last_updated is the strongest signal available, and omitting it would weaken the
check. A row that moved, or is absent, is a STOP.

The denominator is printed beside the number. Exit 0 = clear to act; exit 2 = STOP.

  python org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/e71b_snapshot_recheck.py
"""
import json
import sys
from decimal import Decimal

import boto3

SNAPSHOT = "org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/E71_SEED_ROWS_SNAPSHOT_20261009.json"
TABLE = "etf-classifications"
REGION = "us-east-1"


def plain(value):
    """Normalize a DynamoDB resource-API value for comparison with the snapshot JSON."""
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, (list, set, tuple)):
        return sorted(plain(v) for v in value)
    return value


def main() -> int:
    with open(SNAPSHOT, encoding="utf-8") as fh:
        snap = json.load(fh)
    rows = snap["rows"]
    keys = sorted(rows)
    table = boto3.resource("dynamodb", region_name=REGION).Table(TABLE)

    equal = moved = absent = 0
    for k in keys:
        got = table.get_item(Key={"ticker": k}, ConsistentRead=True).get("Item")
        if got is None:
            absent += 1
            print("  ABSENT: %-6s row is gone -- STOP" % k)
            continue
        live = {f: plain(v) for f, v in got.items()}
        want = {f: plain(v) for f, v in rows[k].items()}
        if live == want:
            equal += 1
            continue
        moved += 1
        fields = sorted(set(live) | set(want))
        delta = ["%s: %r -> %r" % (f, want.get(f, "<absent>"), live.get(f, "<absent>"))
                 for f in fields if live.get(f, "<absent>") != want.get(f, "<absent>")]
        print("  MOVED: %-6s %s -- STOP" % (k, "; ".join(delta)))

    print("E71B-RECHECK denominator=%d equal_to_snapshot=%d MOVED=%d ABSENT=%d"
          % (len(keys), equal, moved, absent))
    if moved or absent:
        print("VERDICT: STOP -- a row moved since the snapshot; report, do not act.")
        return 2
    print("VERDICT: CLEAR -- nothing has written these rows since the snapshot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
