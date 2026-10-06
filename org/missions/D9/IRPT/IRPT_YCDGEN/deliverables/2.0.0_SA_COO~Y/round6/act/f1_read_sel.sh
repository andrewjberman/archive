set -u
# F1 retry 2, READ-ONLY: SELECTION and any other cottonwood request row whose record JSON carries an epoch from 2026-10-06, with its owner principal and tenant fields.
sudo -u ec2-user HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import json, re, sys
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
pat = re.compile(r"(?<![0-9])(1791[2-9][0-9]{5})(?![0-9])")
for i in items:
    blob = json.dumps(i, default=str)
    m = [int(x) for x in pat.findall(blob) if int(x) >= 1791244800]
    if m:
        print("TODAY", max(m), str(i.get("request_revision"))[:60], blob[:1400])
print("scanned", len(items))
PY
