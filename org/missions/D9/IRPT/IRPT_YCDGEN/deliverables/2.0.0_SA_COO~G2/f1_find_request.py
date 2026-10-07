"""READ-ONLY. IRPT_YCDGEN F1 (2.0.0_SA_COO~G2): find Andrew's 2026-10-07 analysis request and say what the server did.

Andrew's run stopped at the page message "This action is unavailable (ENVELOPE_STATUS). Your request is kept for retry."
The code reading says the server ACCEPTED the POST and the browser rejected the success reply's `status` member,
because it carried `internal_correlation_id`. This read checks the server side: did a Cottonwood job row appear at
or after 17:52Z, and in what state? It prints field names, ids, states and timestamps only, plus the report title
Andrew typed. It prints no holdings and no figures, and writes nothing to AWS.

Usage (laptop, workspace root, credentials that can kms:Decrypt the irpt tables):
  python org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/f1_find_request.py > F1_FIND_REQUEST_20261007.txt
"""
import json

import boto3
from boto3.dynamodb.conditions import Key

SINCE = "2026-10-07T17:52"
TENANT = "cottonwood"
SAFE = ("job", "state", "stage", "operation_kind", "producer", "request_id", "revision", "public_reason_code",
        "created_at", "updated_at", "accepted_at", "completed_at", "report_id", "report_title", "prepared_for")


def main():
    ddb = boto3.resource("dynamodb", region_name="us-east-1")
    table = ddb.Table("irpt-jobs")
    items, kw = [], {"KeyConditionExpression": Key("tenant").eq(TENANT)}
    while True:
        page = table.query(**kw)
        items += page.get("Items", [])
        if not page.get("LastEvaluatedKey"):
            break
        kw["ExclusiveStartKey"] = page["LastEvaluatedKey"]
    names = sorted({k for i in items for k in i})
    def stamp(i):
        return max(str(i.get(k) or "") for k in ("created_at", "updated_at", "accepted_at", "completed_at"))

    recent = sorted((i for i in items if stamp(i) >= SINCE), key=stamp)
    print("table irpt-jobs tenant=%s: %d rows (all pages); field names: %s" % (TENANT, len(items), names))
    print("rows with any timestamp >= %sZ: %d" % (SINCE, len(recent)))
    for i in recent:
        print(json.dumps({k: str(i[k]) for k in SAFE if k in i}, sort_keys=True))
    print("positive control: newest row timestamp overall = %s" % (max((stamp(i) for i in items), default="NONE")))


if __name__ == "__main__":
    main()
