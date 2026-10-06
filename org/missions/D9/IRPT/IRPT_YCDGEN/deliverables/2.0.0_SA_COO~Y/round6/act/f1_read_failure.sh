set -u
# F1 failure read, READ-ONLY (CTO msg 105519): newest cottonwood job and request rows, the resident journal since the install, the root's allow list.
# No write, no retry, no host change.
UNIT=irpt-analysis-resident.service
echo "== now $(date -u +%Y-%m-%dT%H:%M:%SZ) active=$(systemctl is-active $UNIT) root=$(systemctl show $UNIT -p ExecStart | grep -o '/opt/irpt-resident/[0-9a-z-]*' | head -1) MainPID=$(systemctl show $UNIT -p MainPID --value) NRestarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "== journal, lines that are not an empty poll (since 03:40Z)"
journalctl -u $UNIT --since '2026-10-06 03:40:00' --no-pager | grep -v 'IRPT_RESIDENT_POLL handled=0' | cut -c1-400 | tail -80
echo "== poll lines with handled>0"
journalctl -u $UNIT --since '2026-10-06 03:40:00' --no-pager | grep 'IRPT_RESIDENT_POLL' | grep -v 'handled=0' | cut -c1-300 | tail -20
echo "== newest job and request rows"
sudo -u ec2-user HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import json, sys
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
import boto3
from boto3.dynamodb.conditions import Key
ddb = boto3.resource("dynamodb", region_name="us-east-1")
jobs = ddb.Table("irpt-jobs")
items, kw = [], {"KeyConditionExpression": Key("tenant").eq("cottonwood")}
while True:
    r = jobs.query(**kw)
    items += r.get("Items", [])
    if not r.get("LastEvaluatedKey"):
        break
    kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
print("jobs seen", len(items), "attribute names", sorted({k for i in items for k in i}))
def stamp(i):
    return str(i.get("updated_at") or i.get("created_at") or i.get("job") or "")
for i in sorted(items, key=stamp)[-4:]:
    d = {k: (str(v)[:900]) for k, v in i.items()}
    print("JOB", json.dumps(d, sort_keys=True))
reqs = ddb.Table("irpt-requests")
rows, kw = [], {"KeyConditionExpression": Key("tenant").eq("cottonwood")}
while True:
    r = reqs.query(**kw)
    rows += r.get("Items", [])
    if not r.get("LastEvaluatedKey"):
        break
    kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
print("request rows seen", len(rows))
nonart = [i for i in rows if not str(i.get("request_revision", "")).startswith("ARTIFACT#")]
def rstamp(i):
    return str(i.get("created_at") or i.get("updated_at") or "")
for i in sorted(nonart, key=rstamp)[-4:]:
    d = {k: (str(v)[:700]) for k, v in i.items()}
    print("REQ", json.dumps(d, sort_keys=True))
PY
