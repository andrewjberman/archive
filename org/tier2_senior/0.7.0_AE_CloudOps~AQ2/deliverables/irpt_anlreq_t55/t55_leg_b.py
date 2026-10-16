"""IRPT_ANLREQ TO-APPLY-t55 LEG B (0.7.0_AE_CloudOps~AQ2): ONE conditional REMOVE of hop_failure on irpt-jobs 49financial REQ-d47252fe74634d0c5cdd8067.

  python t55_leg_b.py --selftest
  python t55_leg_b.py --go

Guards (STOP, nothing written): the row exists, state READY, hop_failure present with code COMMENTARY_DRAFT_REFUSED (the recorded one in t55_after_a.json), and the
item sha256 without hop_failure equals PRE. Then ONE update_item REMOVE hop_failure with ConditionExpression hop_failure.code = :c. Reads the row back ConsistentRead:
hop_failure ABSENT, state READY, the whole item sha256 equals PRE. No put-item, no delete-item, no retry.
"""
from __future__ import annotations

import hashlib
import json
import sys

REGION = "us-east-1"
ROW = {"tenant": {"S": "49financial"}, "job": {"S": "REQ-d47252fe74634d0c5cdd8067"}}


def digest(item, drop=()):
    return hashlib.sha256(json.dumps({k: v for k, v in item.items() if k not in drop}, sort_keys=True).encode()).hexdigest()


def selftest():
    a = {"tenant": {"S": "t"}, "state": {"S": "READY"}}
    b = dict(a, hop_failure={"M": {"code": {"S": "X"}}})
    assert digest(b, drop=("hop_failure",)) == digest(a) != digest(b)
    print("SELFTEST OK digest with and without hop_failure")
    return 0


def go():
    import boto3
    from botocore.exceptions import ClientError
    ddb = boto3.client("dynamodb", region_name=REGION)
    rec = json.load(open("C:/dev/aq2-t54/t55_after_a.json"))
    pre = rec["pre"]
    code = rec["recorded_hop_failure"]["code"]
    r = ddb.get_item(TableName="irpt-jobs", Key=ROW, ConsistentRead=True).get("Item")
    hf = (r or {}).get("hop_failure", {}).get("M", {})
    print("GUARD row=%s state=%s hop_failure code=%s hop=%s at=%s; item sha256 without hop_failure=%s PRE=%s" % (
        "present" if r else "ABSENT", (r or {}).get("state", {}).get("S"), hf.get("code", {}).get("S"), hf.get("hop", {}).get("S"), hf.get("at", {}).get("S"),
        digest(r, drop=("hop_failure",)) if r else None, pre))
    if r is None or r["state"]["S"] != "READY" or hf.get("code", {}).get("S") != code or digest(r, drop=("hop_failure",)) != pre:
        print("STOP: the row is absent, not READY, the hop_failure is absent or differs from the recorded code, or the item differs from PRE; nothing written")
        return 2
    print("RECORDED hop_failure %s" % json.dumps({k: v.get("S") for k, v in hf.items()}, sort_keys=True))
    try:
        ddb.update_item(TableName="irpt-jobs", Key=ROW, UpdateExpression="REMOVE hop_failure", ConditionExpression="hop_failure.#c = :c",
                        ExpressionAttributeNames={"#c": "code"}, ExpressionAttributeValues={":c": {"S": code}})
        print("UPDATE ok (one conditional REMOVE, condition hop_failure.code = %s)" % code)
    except ClientError as e:
        print("UPDATE refused: %s" % e.response["Error"]["Code"])
        return 3
    r2 = ddb.get_item(TableName="irpt-jobs", Key=ROW, ConsistentRead=True).get("Item")
    print("READBACK hop_failure=%s state=%s item sha256=%s PRE=%s equal=%s" % (
        "PRESENT" if "hop_failure" in r2 else "ABSENT", r2["state"]["S"], digest(r2), pre, digest(r2) == pre))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--go" in sys.argv:
        sys.exit(go())
    print(__doc__)
    sys.exit(2)
