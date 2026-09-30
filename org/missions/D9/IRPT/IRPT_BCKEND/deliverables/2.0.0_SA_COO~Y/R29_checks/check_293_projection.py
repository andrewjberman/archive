#!/usr/bin/env python3
"""IB-yr-293 AC2 -- the canonical profile projection carries allowedFirmIds when the row has it.

botocore Stubber, no network. The stub EXPECTS the projection expression to name allowedFirmIds
(the twelfth field, after userType); a reader that still projects eleven fields fails the stub's
parameter match, which is the base state. Then: a row carrying allowedFirmIds "cottonwood" returns it
verbatim; a row without it returns a dict with no such key; passwordHash never returns.
PASS iff all three. Base run (CLOUD HEAD before the cut): FAIL (projection lacks the field).
Issuer 2.0.0_SA_COO~Y, round 29. ASCII only.
"""
import os
import sys

import boto3
from botocore.stub import Stubber

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R29_checks itself; the repo root is parents[8]
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "_scope"))

from canonical_profile_reads import CanonicalProfileReaders  # noqa: E402

EMAIL = "svc-irpt-analysis@opalinvest.com"
KEY = {"PK": {"S": "USER#svc"}, "SK": {"S": "PROFILE"}, "email": {"S": EMAIL}}
QUERY = dict(TableName="opal-users-v2", IndexName="email-index",
             KeyConditionExpression="email = :email",
             ExpressionAttributeValues={":email": {"S": EMAIL}}, Limit=2)
FIELDS = ("PK", "SK", "email", "firmId", "status", "name", "updatedAt",
          "createdAt", "created_at", "role", "userType", "allowedFirmIds")


def projected(fields):
    names = {"#f" + str(i): field for i, field in enumerate(fields)}
    return dict(TableName="opal-users-v2", Key={k: KEY[k] for k in ("PK", "SK")}, ConsistentRead=True,
                ProjectionExpression=", ".join(names), ExpressionAttributeNames=names)


def read(row):
    client = boto3.client("dynamodb", region_name="us-east-1", aws_access_key_id="offline",
                          aws_secret_access_key="offline")
    with Stubber(client) as stub:
        stub.add_response("query", {"Items": [KEY]}, QUERY)
        stub.add_response("get_item", {"Item": row}, projected(FIELDS))
        user = CanonicalProfileReaders(client).get_user(EMAIL)
        stub.assert_no_pending_responses()
    return user


def main():
    base = {**KEY, "firmId": {"S": "opal-capital"}, "status": {"S": "active"}, "name": {"S": "svc"},
            "role": {"S": "admin"}, "userType": {"S": "service"}, "passwordHash": {"S": "NEVER-RETURN"}}
    try:
        with_attr = read({**base, "allowedFirmIds": {"S": "cottonwood"}})
    except Exception as exc:  # the stub's parameter mismatch is the base state
        print("FAIL: reader did not project allowedFirmIds --", str(exc).split("\n")[0][:200])
        return 1
    without = read(base)
    print("with attribute ->", with_attr.get("allowedFirmIds"), "| without -> key present:",
          "allowedFirmIds" in without, "| passwordHash returned:", "passwordHash" in with_attr)
    ok = (with_attr.get("allowedFirmIds") == "cottonwood" and "allowedFirmIds" not in without
          and "passwordHash" not in with_attr and "NEVER-RETURN" not in repr(with_attr))
    if ok:
        print("PASS: projection carries allowedFirmIds verbatim, absent stays absent, passwordHash never returned")
    else:
        print("FAIL: the projection read did not hold (read the line above)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
