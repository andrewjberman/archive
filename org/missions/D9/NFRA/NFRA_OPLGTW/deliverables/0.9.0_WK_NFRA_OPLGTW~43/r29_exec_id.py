"""OG-rl-14: print {"R28_EXEC_ID": <id>} -- the known 2026-10-07 ~01:26Z data-refresh execution, read read-only (one DynamoDB query) from the portal's execution table.
The caller passes it to the host ONLY inside an SSM parameter (R28_SECRET_ENV; the runner redacts it from the output); never write the value to the repository."""
import json

import boto3
from boto3.dynamodb.conditions import Key


def main():
    t = boto3.resource("dynamodb", region_name="us-east-1").Table("opal-data-refresh-executions")
    items = []
    kw = dict(KeyConditionExpression=Key("PK").eq("EXECUTION"), ProjectionExpression="SK, startedAt")
    while True:
        page = t.query(**kw)
        items += page["Items"]
        if "LastEvaluatedKey" not in page:
            break
        kw["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    w = [i for i in items if i.get("startedAt", "")[:16] in ("2026-10-07T01:26", "2026-10-07T01:25", "2026-10-07T01:27")]
    assert len(w) == 1, "expected exactly one execution record near 01:26Z, found %d" % len(w)
    print(json.dumps({"R28_EXEC_ID": w[0]["SK"]}))


main()
