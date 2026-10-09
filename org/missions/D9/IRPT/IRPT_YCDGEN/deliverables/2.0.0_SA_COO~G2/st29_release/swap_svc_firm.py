"""Ledger irpt-ycdgen-f1-st28-20261009, legs W1 (swap) and W2 (swap back): svc-irpt-analysis's allowedFirmIds, ONE firm, conditional.

    python swap_svc_firm.py <from_firm> <to_firm>      e.g.  cottonwood 49financial   (W1)   /   49financial cottonwood   (W2)

CTO~DELL2 msg 2148: svc moves cottonwood -> 49financial (a SWAP: it still reaches exactly one firm, never ALL), because no cottonwood
partner row is an E5-eligible on-behalf owner (row IRPT_YCDGEN-D2-S4). One conditional UpdateItem on the PROFILE row: it writes only when
the row reads exactly <from_firm>, so a second run or a stale read moves nothing. Prints the before and after values of the three fields it
reads (allowedFirmIds, status, userType) -- never the password hash. ASCII only.
"""
import datetime
import sys

import boto3
from botocore.exceptions import ClientError

TABLE = "opal-users-v2"
KEY = {"PK": {"S": "USER#svc-irpt-analysis@opalinvest.com"}, "SK": {"S": "PROFILE"}}
FIRMS = ("49financial", "cottonwood", "inflection")


def read(ddb):
    item = ddb.get_item(TableName=TABLE, Key=KEY, ConsistentRead=True,
                        ProjectionExpression="allowedFirmIds, #s, userType, updatedAt",
                        ExpressionAttributeNames={"#s": "status"}).get("Item") or {}
    return {k: list(v.values())[0] for k, v in item.items()}


def main(argv):
    if len(argv) != 3 or argv[1] not in FIRMS or argv[2] not in FIRMS or argv[1] == argv[2]:
        raise SystemExit(__doc__)
    src, dst = argv[1], argv[2]
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    print("before:", read(ddb))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    try:
        ddb.update_item(TableName=TABLE, Key=KEY, UpdateExpression="SET allowedFirmIds = :to, updatedAt = :t",
                        ConditionExpression="allowedFirmIds = :from AND userType = :svc AND #s = :active",
                        ExpressionAttributeNames={"#s": "status"},
                        ExpressionAttributeValues={":to": {"S": dst}, ":from": {"S": src}, ":svc": {"S": "service"},
                                                   ":active": {"S": "active"}, ":t": {"S": now}})
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("REFUSED: the row does not read allowedFirmIds=%s, service, active; nothing written" % src)
            print("after:", read(ddb))
            return 1
        raise
    after = read(ddb)
    print("after:", after)
    return 0 if after.get("allowedFirmIds") == dst else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
