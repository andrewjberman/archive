"""TCKT_VNEXT TO-R19-MIG applier (0.7.0_AE_CloudOps~TV2): scope_all_firms = BOOL true on the selected rows of opal-users-v2.

Modes:
  select  read-only: print the three counts and the opaque row keys; exit 1 when any count differs from the pair's.
  apply   select, then one conditional update-item per selected row, then a ConsistentRead read-back of each.

Opaque row key = first 12 hex of sha256(PK). 7 of the 23 internal PKs embed an address, so a raw PK is never
printed, logged or written; the real keys live only in this process's memory. No other attribute is printed.
"""
from __future__ import annotations

import hashlib
import json
import sys

import boto3
from botocore.exceptions import ClientError

TABLE = "opal-users-v2"
REGION = "us-east-1"
MARKER = "scope_all_firms"
EXPECT = {"selected": 19, "with_list_attr": 3, "not_active": 1, "internal": 23}
OUT_DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r19_mig/"
COND = "attribute_not_exists(allowedFirmIds) AND attribute_not_exists(scope_all_firms)"


def opaque(pk):
    return hashlib.sha256(pk.encode("utf-8")).hexdigest()[:12]


def digest(item):
    rest = {k: v for k, v in item.items() if k != MARKER}
    return hashlib.sha256(json.dumps(rest, sort_keys=True).encode("utf-8")).hexdigest()


def read_internal(ddb):
    items, kwargs = [], dict(
        TableName=TABLE, ConsistentRead=True,
        FilterExpression="SK = :p AND firmId = :f",
        ExpressionAttributeValues={":p": {"S": "PROFILE"}, ":f": {"S": "opal-capital"}})
    scanned = 0
    while True:
        r = ddb.scan(**kwargs)
        items += r.get("Items", [])
        scanned += r.get("ScannedCount", 0)
        if "LastEvaluatedKey" not in r:
            return items, scanned
        kwargs["ExclusiveStartKey"] = r["LastEvaluatedKey"]


def classify(items):
    sel, with_attr, not_active = [], [], []
    for it in items:
        if "allowedFirmIds" in it:
            with_attr.append(it)
        if it.get("status", {}).get("S") != "active":
            not_active.append(it)
        elif "allowedFirmIds" not in it:
            sel.append(it)
    return sel, with_attr, not_active


def counts_ok(items, sel, with_attr, not_active):
    got = {"selected": len(sel), "with_list_attr": len(with_attr), "not_active": len(not_active), "internal": len(items)}
    print("counts read:", got, "| expected:", EXPECT)
    return got == EXPECT, got


def main(argv):
    mode = argv[1] if len(argv) > 1 else "select"
    ddb = boto3.client("dynamodb", region_name=REGION)
    items, scanned = read_internal(ddb)
    sel, with_attr, not_active = classify(items)
    print("table %s ScannedCount=%d internal PROFILE rows=%d" % (TABLE, scanned, len(items)))
    already = [it for it in sel if MARKER in it]
    print("selected rows already carrying the marker:", len(already))
    ok, got = counts_ok(items, sel, with_attr, not_active)
    keys = sorted(opaque(it["PK"]["S"]) for it in sel)
    print("selected opaque keys (%d):" % len(keys), " ".join(keys))
    if not ok or already:
        print("STOP: count differs from the pair (or a selected row already has the marker); report to the issuer, decide nothing")
        return 1
    if mode == "select":
        return 0
    before = {opaque(it["PK"]["S"]): digest(it) for it in sel}
    with open(OUT_DIR + "R19_MIG_BEFORE.json", "w", encoding="utf-8") as f:
        json.dump({"claim": "measured", "selected_before": got, "other_attrs_sha256_by_opaque_key": before}, f, indent=1, sort_keys=True)
    written, failed = [], []
    for it in sel:
        k = opaque(it["PK"]["S"])
        try:
            ddb.update_item(TableName=TABLE, Key={"PK": it["PK"], "SK": it["SK"]},
                            UpdateExpression="SET scope_all_firms = :t", ConditionExpression=COND,
                            ExpressionAttributeValues={":t": {"BOOL": True}})
            written.append(k)
        except ClientError as e:
            code = e.response["Error"]["Code"]
            failed.append({"key": k, "error": code})
            print("FAILED-CONDITION/ERROR recorded (not forced):", k, code)
    bad = []
    for it in sel:
        k = opaque(it["PK"]["S"])
        if k not in written:
            continue
        r = ddb.get_item(TableName=TABLE, Key={"PK": it["PK"], "SK": it["SK"]}, ConsistentRead=True).get("Item", {})
        if r.get(MARKER) != {"BOOL": True} or digest(r) != before[k]:
            bad.append(k)
    print("written=%d failed=%d readback_bad=%d" % (len(written), len(failed), len(bad)))
    res = {"rows_written": len(written), "row_keys": sorted(written), "selected_before": got, "failed_conditions": failed,
           "readback_bad": bad, "key_scheme": "first 12 hex of sha256(PK); raw PKs embed addresses on 7 of 23 internal rows",
           "other_attrs_unchanged_all_written": not bad, "claim": "measured"}
    with open(OUT_DIR + "R19_MIG_RESULT.partial.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    return 1 if (failed or bad) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
