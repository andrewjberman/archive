"""NFRA_OPLGTW OG-i-5 -- the one-shot conditional copy, old table -> new table.

Scans the OLD table with ConsistentRead, and PutItems into the NEW table with a condition that
never overwrites (attribute_not_exists(pk), mirroring app/access_state.py's IF_ABSENT). No item
content is printed or written to a file by this script -- only a summary count.
"""
from __future__ import annotations

import sys

import boto3
from botocore.exceptions import ClientError

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from og_i5_lib import OLD_TABLE, NEW_TABLE, REGION  # noqa: E402


def main() -> int:
    ddb = boto3.client("dynamodb", region_name=REGION)
    kwargs = {"TableName": OLD_TABLE, "ConsistentRead": True}
    copied = 0
    condition_failed = 0
    scanned = 0
    while True:
        resp = ddb.scan(**kwargs)
        for raw in resp.get("Items", []):
            scanned += 1
            try:
                ddb.put_item(
                    TableName=NEW_TABLE,
                    Item=raw,
                    ConditionExpression="attribute_not_exists(pk)",
                )
                copied += 1
            except ClientError as e:
                if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                    condition_failed += 1
                    print("STOP: condition failed on one item (never overwrite) -- pk/sk withheld from log", file=sys.stderr)
                else:
                    raise
        if "LastEvaluatedKey" not in resp:
            break
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    print(f"scanned={scanned} copied={copied} condition_failed={condition_failed}")
    return 1 if condition_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
