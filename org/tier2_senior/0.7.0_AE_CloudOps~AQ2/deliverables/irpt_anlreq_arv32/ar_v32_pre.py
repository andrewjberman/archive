"""AR-v32 attempt 2 pre-reads (read-only): A1 (hop_failure on the t55 job row), B2 (ticket status and package pointers), users row ABSENT. Closed values only."""
import boto3

R = "us-east-1"
d = boto3.client("dynamodb", region_name=R)
job = d.get_item(TableName="irpt-jobs", Key={"tenant": {"S": "49financial"}, "job": {"S": "REQ-d47252fe74634d0c5cdd8067"}}, ConsistentRead=True).get("Item") or {}
hf = (job.get("hop_failure") or {}).get("M", {})
print("A1 job_row state=%s hop_failure code=%s hop=%s at=%s" % ((job.get("state") or {}).get("S"), (hf.get("code") or {}).get("S"), (hf.get("hop") or {}).get("S"), (hf.get("at") or {}).get("S")))
pk = "USER#fwd1-staff-r41b@opal.invalid"
u = d.get_item(TableName="opal-users-v2", Key={"PK": {"S": pk}, "SK": {"S": "PROFILE"}}, ConsistentRead=True).get("Item")
q = d.query(TableName="opal-users-v2", IndexName="email-index", KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": "fwd1-staff-r41b@opal.invalid"}})
print("USERS row=%s gsi_count=%d" % ("PRESENT" if u else "ABSENT", q["Count"]))
tk = d.get_item(TableName="opal-tickets", Key={"ticket_id": {"S": "TCK-20261015-944c84f8"}}, ConsistentRead=True).get("Item") or {}
pk_names = sorted(k for k in tk if "package" in k.lower() or "pkg" in k.lower())
print("B2 ticket TCK-20261015-944c84f8 status=%s package=%s" % ((tk.get("status") or {}).get("S"), "PRESENT" if any(tk[k] for k in pk_names) else "ABSENT"))
