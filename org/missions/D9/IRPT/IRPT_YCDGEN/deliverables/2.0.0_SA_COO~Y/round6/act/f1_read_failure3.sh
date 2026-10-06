set -u
# F1 failure read 3, READ-ONLY: any cottonwood request or job row carrying an epoch value from 2026-10-06 (1791244800 to 1791331200) in ANY field, found by regex over the whole row.
sudo -u ec2-user HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import json, re, sys
sys.path.append('/opt/investor-reporting-ycharts/pydeps')
import boto3
from boto3.dynamodb.conditions import Key
ddb = boto3.resource("dynamodb", region_name="us-east-1")
pat = re.compile(r"(?<![0-9])(17912[4-9][0-9]{4}|17913[0-2][0-9]{4})(?![0-9])")
def blob(i):
    return json.dumps(i, default=str, sort_keys=True)
for name in ("irpt-requests", "irpt-jobs"):
    t = ddb.Table(name)
    items, kw = [], {"KeyConditionExpression": Key("tenant").eq("cottonwood")}
    while True:
        r = t.query(**kw)
        items += r.get("Items", [])
        if not r.get("LastEvaluatedKey"):
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    hits = []
    for i in items:
        m = [int(x) for x in pat.findall(blob(i)) if 1791244800 <= int(x) < 1791331200]
        if m:
            hits.append((max(m), i))
    print(name, "rows", len(items), "rows with an epoch from 2026-10-06:", len(hits))
    for mx, i in sorted(hits, key=lambda h: h[0])[-6:]:
        print("HIT", name, mx, json.dumps({k: str(v)[:240] for k, v in i.items() if k in ("request_revision", "family", "state", "job", "logical_id", "owner")}, sort_keys=True))
PY
