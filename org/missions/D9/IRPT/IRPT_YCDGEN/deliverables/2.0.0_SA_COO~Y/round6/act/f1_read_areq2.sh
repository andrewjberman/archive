set -u
# F1 read, READ-ONLY: everything carrying areq-1b3396e2 in the cottonwood tables, plus the resident journal since 08:30Z. No write, no retry.
UNIT=irpt-analysis-resident.service
echo "== now $(date -u +%Y-%m-%dT%H:%M:%SZ) active=$(systemctl is-active $UNIT) NRestarts=$(systemctl show $UNIT -p NRestarts --value)"
echo "== journal lines that are not an empty poll, since 2026-10-06 03:40Z"
journalctl -u $UNIT --since '2026-10-06 03:40:00' --no-pager | grep -v 'IRPT_RESIDENT_POLL handled=0' | grep -v 'Stopp\|Deactivated\|Consumed\|Started' | cut -c1-500 | tail -40
echo "== polls handled>0: $(journalctl -u $UNIT --since '2026-10-06 03:40:00' --no-pager | grep IRPT_RESIDENT_POLL | grep -vc 'handled=0')"
sudo -u ec2-user HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import json, sys
sys.path.append('/opt/investor-reporting-ycharts/pydeps')
import boto3
from boto3.dynamodb.conditions import Key
ddb = boto3.resource("dynamodb", region_name="us-east-1")
NEEDLE = "1b3396e2"
for name in ("irpt-requests", "irpt-jobs"):
    t = ddb.Table(name)
    items, kw = [], {"KeyConditionExpression": Key("tenant").eq("cottonwood")}
    while True:
        r = t.query(**kw)
        items += r.get("Items", [])
        if not r.get("LastEvaluatedKey"):
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    hits = [i for i in items if NEEDLE in json.dumps(i, default=str)]
    print(name, "rows", len(items), "rows naming", NEEDLE, ":", len(hits))
    for i in hits[:6]:
        print("HIT", name, json.dumps(i, default=str, sort_keys=True)[:3500])
PY
