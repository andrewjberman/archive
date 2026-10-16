"""ap30 helper: the three email_deny keys (derived with access_state's own salt) and a strongly consistent live read of them.

usage: _deny.py live      -> one line of key=value pairs (counts and booleans only; no oid, no hash printed)
       _deny.py keys      -> the three derived pk values, one per line, label first (used by the applier's record check)
"""
import hashlib
import sys

SALT = "og-email-deny/v1|"
TABLE = "gateway-access-state-table"
EMAILS = {
    "andrew": "andrew@opalinvest.com",
    "opalbloomberg": "opalbloomberg@opalinvest.com",
    "alyssa": "alyssa@opalinvest.com",
}


def pk_of(email):
    return "POLICY#EMAILDENY#" + hashlib.sha256((SALT + email.strip().lower()).encode("utf-8")).hexdigest()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "live"
    if mode == "keys":
        for label, email in EMAILS.items():
            print(label, pk_of(email))
        return
    try:
        import boto3
        c = boto3.client("dynamodb", region_name="us-east-1")
        out = {}
        for label, email in EMAILS.items():
            r = c.get_item(TableName=TABLE, ConsistentRead=True, Key={"pk": {"S": pk_of(email)}, "sk": {"S": "email_deny"}})
            it = r.get("Item")
            out[label + "_present"] = "yes" if it else "no"
            out[label + "_active"] = "yes" if it and it.get("status", {}).get("S") == "active" else "no"
        kw = {"TableName": TABLE, "ConsistentRead": True, "FilterExpression": "begins_with(pk,:p) AND sk = :s",
              "ExpressionAttributeValues": {":p": {"S": "POLICY#EMAILDENY#"}, ":s": {"S": "email_deny"}}, "Select": "COUNT"}
        n = 0
        while True:
            r = c.scan(**kw)
            n += r["Count"]
            if "LastEvaluatedKey" not in r:
                break
            kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
        out["email_deny_total"] = n
    except Exception as e:  # a failed read is a value; say so
        print("live_read=FAILED:%s" % type(e).__name__)
        return
    print("live_read=ok " + " ".join("%s=%s" % kv for kv in out.items()))


main()
