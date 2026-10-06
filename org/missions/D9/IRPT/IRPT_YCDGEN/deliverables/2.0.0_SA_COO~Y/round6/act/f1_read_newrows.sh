set -u
# F1 retry 2, READ-ONLY: the newest cottonwood request rows by created_at, and the row-type census (prefix of request_revision), to find the 3 rows added since 887.
sudo -u ec2-user HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import json, sys, collections
sys.path.append('/opt/investor-reporting-ycharts/pydeps')
import boto3
from boto3.dynamodb.conditions import Key
ddb = boto3.resource("dynamodb", region_name="us-east-1")
t = ddb.Table("irpt-requests")
items, kw = [], {"KeyConditionExpression": Key("tenant").eq("cottonwood")}
while True:
    r = t.query(**kw)
    items += r.get("Items", [])
    if not r.get("LastEvaluatedKey"):
        break
    kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
cen = collections.Counter(str(i.get("request_revision", "")).split("#")[0] for i in items)
print("rows", len(items), "census by prefix", dict(cen))
def ts(i):
    for k in ("created_at", "updated_at"):
        try:
            return int(i.get(k))
        except Exception:
            pass
    return 0
for i in sorted(items, key=ts)[-5:]:
    print("NEWEST", ts(i), json.dumps({k: str(v)[:200] for k, v in i.items() if k in ("request_revision", "family", "state", "logical_id")}, sort_keys=True))
# rows that are not artifact/retention/upload: the request-level rows
others = [i for i in items if not str(i.get("request_revision", "")).startswith(("ARTIFACT#", "RETENTION#"))]
print("request-level rows", len(others))
for i in others[-6:]:
    print("REQROW", json.dumps({k: str(v)[:260] for k, v in i.items()}, sort_keys=True)[:1500])
PY
