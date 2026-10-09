"""READ-ONLY census (CTO~DELL2 msg 2118): which registered partner firm has a row E5 can make an on-behalf owner?

E5 (served.py _advisor_owner) + resolve_prospect_owner (_scope/prospect.py:34) accept an owner only of class FIRM_ADVISOR (an advisorId
claim, from the partner row's advisorKey) or FIRM_OPERATIONS (role/advisorRole admin with a verified firm). For each firm in the registry
(infra/logic/registry/reporting_policies.json) this counts partner rows, rows with an advisorKey, and rows whose canonical user is active in
that firm with role admin. It prints COUNTS and role names only -- never an email or a name. Writes nothing.
"""
import json
import os
import sys

import boto3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 7))
POLICIES = json.load(open(os.path.join(ROOT, "infra", "logic", "registry", "reporting_policies.json"), encoding="utf-8"))
FIRMS = sorted({f for p in POLICIES["policies"] for f in p.get("firms", [])})
ddb = boto3.client("dynamodb", region_name="us-east-1")


def scan(table):
    items, kw = [], {"TableName": table}
    while True:
        page = ddb.scan(**kw)
        items += page.get("Items", [])
        if not page.get("LastEvaluatedKey"):
            return items
        kw["ExclusiveStartKey"] = page["LastEvaluatedKey"]


def user(email):
    rows = ddb.query(TableName="opal-users-v2", IndexName="email-index", KeyConditionExpression="email = :e",
                     ExpressionAttributeValues={":e": {"S": email}}, Limit=2).get("Items", [])
    if len(rows) != 1:
        return None
    return ddb.get_item(TableName="opal-users-v2", Key={"PK": {"S": rows[0]["PK"]["S"]}, "SK": {"S": "PROFILE"}},
                        ProjectionExpression="firmId, #s, #r, advisorRole",
                        ExpressionAttributeNames={"#s": "status", "#r": "role"}).get("Item")


def main():
    print("firms in the registry:", FIRMS)
    for firm in FIRMS:
        try:
            rows = scan("opal-partner-" + firm)
        except Exception as exc:  # noqa: BLE001 -- a firm whose table cannot be read is reported, never skipped silently
            print("%s: partner table unreadable (%s)" % (firm, type(exc).__name__))
            continue
        with_key = active = ops = 0
        roles = {}
        for it in rows:
            email = it.get("email", {}).get("S", "")
            if "advisorKey" in it:
                with_key += 1
            u = user(email) if email else None
            if not u or u.get("firmId", {}).get("S") != firm or u.get("status", {}).get("S") != "active":
                continue
            active += 1
            role = (u.get("role", {}).get("S") or "").lower()
            roles[role] = roles.get(role, 0) + 1
            if role == "admin" or (u.get("advisorRole", {}).get("S") or "").lower() == "admin":
                ops += 1
        print("%s: partner rows %d | with advisorKey (FIRM_ADVISOR-capable) %d | active users in firm %d (roles %s) | admin "
              "(FIRM_OPERATIONS-capable) %d" % (firm, len(rows), with_key, active, json.dumps(roles, sort_keys=True), ops))
    return 0


if __name__ == "__main__":
    sys.exit(main())
