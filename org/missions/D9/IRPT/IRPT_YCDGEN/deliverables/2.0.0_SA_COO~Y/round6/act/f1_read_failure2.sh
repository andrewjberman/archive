set -u
# F1 failure read 2, READ-ONLY: anything created after 2026-10-06T00:00Z in requests and jobs (any tenant row type), queue depths and DLQ, journal poll count.
UNIT=irpt-analysis-resident.service
echo "polls since 03:40Z: $(journalctl -u $UNIT --since '2026-10-06 03:40:00' --no-pager | grep -c IRPT_RESIDENT_POLL) handled>0: $(journalctl -u $UNIT --since '2026-10-06 03:40:00' --no-pager | grep IRPT_RESIDENT_POLL | grep -vc 'handled=0')"
for q in https://sqs.us-east-1.amazonaws.com/313476888478/irpt-generation; do
  echo "QUEUE $q $(aws sqs get-queue-attributes --queue-url $q --attribute-names ApproximateNumberOfMessages ApproximateNumberOfMessagesNotVisible --region us-east-1 --query 'Attributes.[ApproximateNumberOfMessages,ApproximateNumberOfMessagesNotVisible]' --output text)"
done
sudo -u ec2-user HOME=/home/ec2-user AWS_DEFAULT_REGION=us-east-1 /usr/bin/python3.12 - <<'PY'
import json, sys
sys.path.append('/opt/investor-reporting-ycharts/pydeps')
import boto3
from boto3.dynamodb.conditions import Attr
ddb = boto3.resource("dynamodb", region_name="us-east-1")
CUT = 1791244800
from boto3.dynamodb.conditions import Key
CUT = 1791244800
for tenant in ("cottonwood", "opal-capital"):
  for name in ("irpt-requests", "irpt-jobs"):
    t = ddb.Table(name)
    items, kw = [], {"KeyConditionExpression": Key("tenant").eq(tenant)}
    while True:
        r = t.query(**kw)
        items += r.get("Items", [])
        if not r.get("LastEvaluatedKey"):
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    def ts(i):
        for k in ("created_at", "updated_at"):
            try:
                return int(i.get(k))
            except Exception:
                pass
        return 0
    new = [i for i in items if ts(i) >= CUT]
    print(tenant, name, "rows queried", len(items), "with a timestamp at or after 2026-10-06T00:00Z:", len(new), "rows with no timestamp field:", sum(1 for i in items if ts(i) == 0))
    for i in sorted(new, key=ts)[-8:]:
        print("NEW", tenant, name, json.dumps({k: str(v)[:300] for k, v in i.items() if k in ("request_revision","family","state","created_at","logical_id","owner","job","job_detail")}, sort_keys=True))
PY
