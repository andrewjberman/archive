set -u
# CTO half branch B, ledger irpt-ycdgen-r6-branch-b-20261006 leg R1. READ-ONLY. Run on the resident host under its own role.
# The NEW package's retention module (extracted to a temp dir, NOT installed) and the RUNNING package's module each validate the SAME live v1
# retention rows through the package's own DynamoRetentionIndex over a read-only table proxy (no write method exists on it) with one fixed clock.
# Prints counts per firm and family and compares the two verdicts row by row. Zero writes, zero installs, zero service changes.
BUCKET=opal-313476888478-lambda-artifacts
NEW=09139ee34d-st23
OLD=3d705e700f-st22
R=/opt/irpt-resident
H=/opt/investor-reporting-ycharts
KEY=ec2/investor-reporting-ycharts/resident/irpt-resident-$NEW.tar.gz
WANT=7df58a9828cb5f900a65d02bb89b3f5492a34cd7bcd7f84183c65834d5193ebe
T=/tmp/r6b-step1
rm -rf $T; mkdir -p $T/new
aws s3 cp "s3://$BUCKET/$KEY" $T/new.tar.gz --only-show-errors --region us-east-1 || { echo "ERROR: fetch failed; nothing moved"; exit 30; }
[ "$(sha256sum $T/new.tar.gz | cut -d' ' -f1)" = "$WANT" ] || { echo "ERROR: fetched tar is not the built bytes"; exit 31; }
tar -xzf $T/new.tar.gz -C $T/new || exit 32
(cd $T/new && sha256sum -c SHA256SUMS --quiet) && echo "new package SHA256SUMS OK ($(wc -l < $T/new/SHA256SUMS) members)" || { echo "ERROR: SHA256SUMS"; exit 33; }
chmod 777 $T
echo "running root: $(systemctl show irpt-analysis-resident.service -p ExecStart | grep -o "$R/[0-9a-z-]*" | head -1) (compared root $R/$OLD)"
cat > $T/validate.py <<'PY'
import json, os, sys, time
root, out, now = sys.argv[1], sys.argv[2], int(sys.argv[3])
for rel in ("reports", "_authz", "_scope", "_ids", "_contracts", "lib", "_keys", "_gate", "ops", "intake"):
    sys.path.insert(0, os.path.join(root, rel))
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
sys.path.insert(0, root)
import boto3
from boto3.dynamodb.conditions import Key
import retention
from retention import RetentionPolicy, DynamoRetentionIndex, RetentionRefused, RetentionExpired
from opal_naming import reporting_policy

class ReadOnlyTable:
    """Only the two read calls the index uses; any other attribute is an error, so a write cannot happen."""
    def __init__(self, table):
        self._t = table
        self.name = table.name
    def get_item(self, **kw):
        return self._t.get_item(**kw)
    def query(self, **kw):
        return self._t.query(**kw)
    def __getattr__(self, name):
        raise AttributeError("READ-ONLY proxy refuses " + name)

table = ReadOnlyTable(boto3.resource("dynamodb", region_name="us-east-1").Table("irpt-requests"))
pol = RetentionPolicy(DynamoRetentionIndex(table), reporting_policy, lambda p, o: True, lambda: now)
rows = []
for firm in ("49financial", "cottonwood", "inflection"):
    kw = {"KeyConditionExpression": Key("tenant").eq(firm) & Key("request_revision").begins_with("RETENTION#")}
    while True:
        resp = table.query(**kw)
        for item in resp.get("Items", []):
            rows.append((firm, item))
        if not resp.get("LastEvaluatedKey"):
            break
        kw["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
verdict, counts, keys, samples = {}, {}, set(), {}
for firm, item in rows:
    fam = item.get("family")
    ref = item.get("ref")
    k = firm + "|" + str(item.get("request_revision"))
    keys |= set(item)
    if not isinstance(ref, dict):
        # not a retention reference row: no ref attribute at all (a same-prefix record of another kind); counted apart, never as a refusal
        v = "NOT_A_REFERENCE_ROW"
        verdict[k] = v
        c = counts.setdefault(firm + "|" + str(fam) + "|NOT_A_REFERENCE", {})
        c[v] = c.get(v, 0) + 1
        samples.setdefault(firm, []).append(sorted(item)[:8] + [str(item.get("request_revision"))[:40]]) if len(samples.get(firm, [])) < 2 else None
        continue
    try:
        pol.require_live({"firm_id": firm, "principal_class": "OPAL_GLOBAL"}, ref, accepted=False, data_firm=firm)
        v = "OK"
    except RetentionExpired as e:
        v = "EXPIRED"
    except RetentionRefused as e:
        v = "REFUSED:" + str(e)[:60]
    except Exception as e:
        v = "ERROR:" + type(e).__name__ + ":" + str(e)[:60]
    verdict[k] = v
    c = counts.setdefault(firm + "|" + str(fam) + "|" + str(((ref or {}).get("policy_revision"))), {})
    c[v] = c.get(v, 0) + 1
json.dump({"verdict": verdict, "counts": counts, "keys": sorted(keys), "rows": len(rows)}, open(out, "w"))
print("   non-reference row samples (attribute names, key prefix):", samples)
print("ROOT", root.rsplit("/", 1)[-1], "rows read", len(rows))
for k in sorted(counts):
    print("  ", k, counts[k])
print("   attribute names seen:", sorted(keys))
PY
NOW=$(date +%s)
echo "fixed clock $NOW ($(date -u -d @$NOW +%FT%TZ))"
sudo -u ec2-user /usr/bin/python3.12 $T/validate.py $R/$OLD $T/old.json $NOW 2>&1 | tail -30
echo "--- NEW"
sudo -u ec2-user /usr/bin/python3.12 $T/validate.py $T/new $T/new.json $NOW 2>&1 | tail -30
python3.12 - <<'PY'
import json
o = json.load(open("/tmp/r6b-step1/old.json")); n = json.load(open("/tmp/r6b-step1/new.json"))
ov, nv = o["verdict"], n["verdict"]
diff = {k: (ov.get(k), nv.get(k)) for k in set(ov) | set(nv) if ov.get(k) != nv.get(k)}
refused_new = [k for k, v in nv.items() if v.startswith("REFUSED") or v.startswith("ERROR")]
refused_old = [k for k, v in ov.items() if v.startswith("REFUSED") or v.startswith("ERROR")]
ref_rows_new = sum(1 for v in nv.values() if v != "NOT_A_REFERENCE_ROW")
print("COMPARE reference rows (with a ref):", ref_rows_new, "of", len(nv), "; non-reference rows:", len(nv) - ref_rows_new)
print("COMPARE rows old", len(ov), "new", len(nv), "verdict differences", len(diff))
print("COMPARE new refusals/errors", len(refused_new), "old refusals/errors", len(refused_old))
for k in list(diff)[:10]:
    print("  DIFF", k, diff[k])
print("R1 RESULT:", "PASS" if not diff and not refused_new and ref_rows_new > 0 else "STOP")
PY
rm -rf $T/new $T/new.tar.gz
echo "temp new package removed; only $T/old.json new.json validate.py remain; nothing installed, nothing written to any table"
