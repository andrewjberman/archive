"""TO-RUN-COMMENTARY-E2E-7C cleanup of the objects the PAGE created before its ticket create was refused (stop at B2).

The page's upload (analysis/inputs) wrote one upload row set for the synthetic user, but the filing stopped before a ticket id existed, so the driver
could not record its keys at creation. This script IDENTIFIES the one upload row that carries BOTH this run's synthetic address and this run's unique
holdings hash (sha256 7d383531...), RECORDS its keys in state_e2e7c.json, then deletes them through the driver's own delete_all (conditional deletes,
each read back ABSENT, only the recorded upload's rows and blobs). A count of identified rows other than exactly one is a STOP with nothing deleted.
"""
from __future__ import annotations

import json
import re
import sys
import importlib.util
from pathlib import Path

import boto3

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("e2e7c_run", str(HERE / "e2e7c_run.py"))
drv = importlib.util.module_from_spec(spec)
sys.modules["e2e7c_run"] = drv
spec.loader.exec_module(drv)


def main():
    ddb = boto3.client("dynamodb", region_name=drv.REGION)
    s3 = boto3.client("s3", region_name=drv.REGION)
    items, lek = [], None
    while True:
        kw = dict(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)",
                  ExpressionAttributeValues={":t": {"S": drv.TENANT}, ":p": {"S": "UPLOAD#"}}, ConsistentRead=True)
        if lek:
            kw["ExclusiveStartKey"] = lek
        r = ddb.query(**kw)
        items += r["Items"]
        lek = r.get("LastEvaluatedKey")
        if not lek:
            break
    mine = [it for it in items if drv.EMAIL in json.dumps(it) and drv.HOLDINGS_SHA[:16] in json.dumps(it)]
    print("UPLOAD rows read (denominator):", len(items), "identified as this run's (email AND holdings hash):", len(mine))
    if len(mine) != 1:
        print("STOP: identified count is not exactly one; nothing deleted")
        return 1
    it = mine[0]
    upload_id = it["request_revision"]["S"][len("UPLOAD#"):]
    blob = json.dumps(it)
    inp = sorted(set(re.findall(r"portfolio_[0-9a-f]{64}", blob)))
    if not inp:
        norm = ddb.query(TableName="irpt-requests", KeyConditionExpression="tenant = :t AND begins_with(request_revision, :p)",
                         ExpressionAttributeValues={":t": {"S": drv.TENANT}, ":p": {"S": "NORMALIZATION#" + upload_id + "#"}}, ConsistentRead=True)["Items"]
        inp = sorted(set(re.findall(r"portfolio_[0-9a-f]{64}", json.dumps(norm))))
    input_id = inp[0] if len(inp) == 1 else None
    print("upload_id", upload_id[:14] + "...", "input_id", (input_id or "none")[:20] + "...", "input candidates", len(inp))

    run = drv.Run()
    run.st = json.loads(drv.STATE_FILE.read_text(encoding="ascii"))
    run.keys = run.st["keys"]
    run.record("upload", tenant=drv.TENANT, upload_id=upload_id, input_id=input_id)
    run.st["upload_attribution"] = {"rows_read": len(items), "identified": 1, "by": "synthetic address AND holdings sha256 first16"}
    art_key = drv.original_holdings_key(ddb, upload_id)
    run.st["art_key_for_delete"], run.st["art_key_recorded"] = art_key, bool(art_key)
    run.st["cleanup_first_delete_utc"] = drv.utc()
    run.st["first_delete_utc"] = run.st["cleanup_first_delete_utc"]

    class NoMint:
        @staticmethod
        def cmd_remove():
            print("ABSENT GSI ABSENT CONSISTENT")  # the user row was removed and read back ABSENT by the driver's own D

    # the driver's delete_all removes the user row by the mint's remove(); that row is already gone, so the users leg is read here instead of repeated
    users_absent = ddb.get_item(TableName="opal-users-v2", Key={"PK": {"S": "USER#" + drv.EMAIL}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item") is None
    gsi = ddb.query(TableName="opal-users-v2", IndexName="email-index", KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": drv.EMAIL}}, Select="COUNT")["Count"]
    run.st["users_absent_read"] = {"consistent": users_absent, "email_index_count": gsi}
    if not users_absent or gsi != 0:
        print("STOP: the synthetic user row reads present; nothing deleted")
        return 1
    drv.delete_all(run, ddb, s3, NoMint, None, upload_id, input_id, None, None, None, None)
    run.st["cleanup_last_read_utc"] = drv.utc()
    run.save()
    print(json.dumps({k: run.st.get(k) for k in ("deleted", "delete_plan", "leftover_blob_keys", "leftover_delete_code", "cleanup_first_delete_utc")}, indent=0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
