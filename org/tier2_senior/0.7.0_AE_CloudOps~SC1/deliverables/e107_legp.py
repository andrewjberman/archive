"""MDPF_SECCLASS.TO-SC-e107b LEG P -- reads only, nothing written to AWS.

Prints org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/E107_LEGP_20261016.json (the path is argv[1]):
  - get_item of the 22 baseline tickers (13 planned + 9 seed_pending): present/absent
  - the table's ItemCount, TableStatus, key schema and PITR state
  - a census of the first 200 keys of a SORTED full key scan, with last_updated (denominator = items scanned)
  - IsLatest, VersionId, ETag, LastModified of the two served mix summaries in the canonical bucket
Run as: python org/tier2_senior/0.7.0_AE_CloudOps~SC1/deliverables/e107_legp.py <out.json>
"""
from __future__ import annotations

import datetime
import json
import sys

import boto3

PLAN = "org/missions/D8/MDPF/MDPF_SECCLASS/deliverables/0.9.0_WK_MDPF_SECCLASS~97/SEED22_PLAN.json"
TABLE = "etf-classifications"
REGION = "us-east-1"
BUCKET_49F = "opal-data-49financial"
SERVED = (
    "advi/49financial/platinum/views/mix_daily_summary.json",
    "advi/49financial/platinum/firm/mix_summary.json",
)


def _val(a):
    if a is None:
        return None
    (k, v), = a.items()
    return v


def main(out_path):
    plan = json.load(open(PLAN, encoding="utf-8"))
    planned = [r["ticker"] for r in plan["planned"]]
    held = [r["ticker"] for r in plan["seed_pending"]]
    ddb = boto3.client("dynamodb", region_name=REGION)
    s3 = boto3.client("s3")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    desc = ddb.describe_table(TableName=TABLE)["Table"]
    pitr = ddb.describe_continuous_backups(TableName=TABLE)["ContinuousBackupsDescription"]["PointInTimeRecoveryDescription"]
    keyname = [k["AttributeName"] for k in desc["KeySchema"] if k["KeyType"] == "HASH"][0]

    items = {}
    for group, tickers in (("planned", planned), ("held_out", held)):
        for t in tickers:
            r = ddb.get_item(TableName=TABLE, Key={keyname: {"S": t}}, ConsistentRead=True)
            items[t] = {"group": group, "present": "Item" in r}

    keys = []
    kw = {"TableName": TABLE, "ProjectionExpression": "#t, last_updated", "ExpressionAttributeNames": {"#t": keyname}}
    scanned = 0
    while True:
        r = ddb.scan(**kw)
        for it in r["Items"]:
            scanned += 1
            keys.append((_val(it.get(keyname)), _val(it.get("last_updated"))))
        if "LastEvaluatedKey" not in r:
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    keys.sort(key=lambda kv: kv[0])
    census = [{"ticker": k, "last_updated": lu} for k, lu in keys[:200]]
    # control: the 22 baseline tickers must be absent from the scan too (a scan that cannot see them proves nothing)
    in_scan = sorted(set(planned + held) & {k for k, _ in keys})

    served = {}
    for key in SERVED:
        vs = s3.list_object_versions(Bucket=BUCKET_49F, Prefix=key).get("Versions", [])
        vs = [v for v in vs if v["Key"] == key]
        latest = [v for v in vs if v["IsLatest"]]
        served[key] = {
            "versions_listed": len(vs),
            "latest": ({"IsLatest": latest[0]["IsLatest"], "VersionId": latest[0]["VersionId"], "ETag": latest[0]["ETag"],
                        "LastModified": latest[0]["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), "Size": latest[0]["Size"]}
                       if latest else None),
        }

    doc = {
        "read_at": now,
        "claim": "measured (read this session by 0.7.0_AE_CloudOps~SC1, nothing written)",
        "table": TABLE, "region": REGION, "key_attribute": keyname,
        "plan": PLAN,
        "item_count_describe_table": desc.get("ItemCount"),
        "table_status": desc.get("TableStatus"),
        "pitr": {"status": pitr.get("PointInTimeRecoveryStatus"),
                 "earliest_restorable": (pitr["EarliestRestorableDateTime"].strftime("%Y-%m-%dT%H:%M:%SZ")
                                         if pitr.get("EarliestRestorableDateTime") else None)},
        "get_item_22": items,
        "get_item_summary": {"planned_present": sum(1 for v in items.values() if v["group"] == "planned" and v["present"]),
                             "held_out_present": sum(1 for v in items.values() if v["group"] == "held_out" and v["present"]),
                             "planned_n": len(planned), "held_out_n": len(held)},
        "scan": {"items_scanned": scanned, "baseline_tickers_seen_in_scan": in_scan},
        "census_200_sorted_first": census,
        "served_objects": served,
    }
    with open(out_path, "w", encoding="ascii", newline="\n") as f:
        json.dump(doc, f, indent=1, sort_keys=True, ensure_ascii=True)
    print("LEGP read_at=%s ItemCount=%s scanned=%d planned_present=%d/%d held_out_present=%d/%d in_scan=%d pitr=%s census=%d" % (
        now, desc.get("ItemCount"), scanned, doc["get_item_summary"]["planned_present"], len(planned),
        doc["get_item_summary"]["held_out_present"], len(held), len(in_scan), pitr.get("PointInTimeRecoveryStatus"), len(census)))
    for k, v in served.items():
        print("SERVED %s latest=%s" % (k, v["latest"]))


if __name__ == "__main__":
    main(sys.argv[1])
