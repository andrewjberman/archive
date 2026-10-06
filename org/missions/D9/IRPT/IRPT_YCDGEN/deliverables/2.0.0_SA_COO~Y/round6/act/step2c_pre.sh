set -u
# CTO half 20261006 condition 2 / ledger irpt-ycdgen-r6-branch-a-20261006 legs D2 and V1. READ-ONLY. Run on the resident host.
# Usage: step2_reads.sh <package-root>   (the root whose retention module gives the verdict: the running one)
# Prints, with no timestamps, the answers a pre-install and a post-install run must equal:
#   (a) one READY job row of the cottonwood tenant (smallest job id): state, report_id, revision, certification_sha256;
#   (b) one retained ORIGINAL_VENDOR_PDF-class artifact read by S3 version: bytes and sha256, and that module's retention verdict for it.
ROOT=/opt/irpt-resident/3d705e700f-st22
[ -n "$ROOT" ] && [ -d "$ROOT" ] || { echo "ERROR: package root required"; exit 2; }
H=/opt/investor-reporting-ycharts
sudo -u ec2-user ROOT="$ROOT" /usr/bin/python3.12 - <<'PY'
import hashlib, json, os, sys, time
root = os.environ["ROOT"]
for rel in ("reports", "_authz", "_scope", "_ids", "_contracts", "lib", "_keys", "_gate", "ops", "intake"):
    sys.path.insert(0, os.path.join(root, rel))
sys.path.append("/opt/investor-reporting-ycharts/pydeps")
sys.path.insert(0, root)
import boto3
from boto3.dynamodb.conditions import Key, Attr
ddb = boto3.resource("dynamodb", region_name="us-east-1")
out = {"root": root.rsplit("/", 1)[-1]}
# (a) a READY job
jobs = ddb.Table("irpt-jobs")
ready, kw = [], {"KeyConditionExpression": Key("tenant").eq("cottonwood"), "FilterExpression": Attr("state").eq("READY")}
while True:
    r = jobs.query(**kw)
    ready += r.get("Items", [])
    if not r.get("LastEvaluatedKey") or len(ready) >= 50:
        break
    kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
ready.sort(key=lambda i: i["job"])
if ready:
    j = ready[0]
    d = json.loads(j.get("job_detail") or "{}")
    out["ready_job"] = {"job": j["job"], "state": j["state"], "report_id": d.get("report_id"), "revision": d.get("revision"),
                        "certification_sha256": d.get("certification_sha256"), "ready_jobs_seen": len(ready)}
else:
    out["ready_job"] = None
# (b) a retained artifact read by version
reqs = ddb.Table("irpt-requests")
art, kw = [], {"KeyConditionExpression": Key("tenant").eq("cottonwood") & Key("request_revision").begins_with("ARTIFACT#")}
while True:
    r = reqs.query(**kw)
    art += r.get("Items", [])
    if not r.get("LastEvaluatedKey") or len(art) >= 400:
        break
    kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
out["artifact_rows_seen"] = len(art)
out["artifact_row_attribute_names"] = sorted({k for i in art[:50] for k in i})
cand = sorted([i for i in art if isinstance(i.get("blob"), dict) and i["blob"].get("key") and i["blob"].get("version_id")
               and str(i["blob"]["key"]).endswith(".pdf")], key=lambda i: i["request_revision"])
out["pdf_artifacts_seen"] = len(cand)
if cand:
    a = cand[0]
    b = a["blob"]
    s3 = boto3.client("s3", region_name="us-east-1")
    body = s3.get_object(Bucket=b["bucket"], Key=b["key"], VersionId=b["version_id"])["Body"].read()
    out["artifact"] = {"artifact_row": a["request_revision"], "bucket": b["bucket"], "key": b["key"], "version_id": b["version_id"],
                       "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "recorded_sha256": b.get("sha256"),
                       "family": a.get("family")}
    # that package module's retention verdict for the retention row this artifact names, if it names one
    rr = a.get("retention_ref")   # an ARTIFACT# row's own `ref` is its artifact reference, not a retention reference; step 1 owns the retention verdicts
    out["artifact"]["retention_ref_present"] = isinstance(rr, dict)
    if isinstance(rr, dict):
        from retention import RetentionPolicy, DynamoRetentionIndex, RetentionRefused, RetentionExpired
        from opal_naming import reporting_policy
        class RO:
            def __init__(self, t): self._t = t; self.name = t.name
            def get_item(self, **kw): return self._t.get_item(**kw)
            def query(self, **kw): return self._t.query(**kw)
            def __getattr__(self, n): raise AttributeError("READ-ONLY proxy refuses " + n)
        pol = RetentionPolicy(DynamoRetentionIndex(RO(reqs)), reporting_policy, lambda p, o: True, lambda: int(time.time()))
        try:
            pol.require_live({"firm_id": "cottonwood", "principal_class": "OPAL_GLOBAL"}, rr, accepted=False, data_firm="cottonwood")
            out["artifact"]["retention_verdict"] = "OK"
        except RetentionExpired:
            out["artifact"]["retention_verdict"] = "EXPIRED"
        except Exception as e:
            out["artifact"]["retention_verdict"] = type(e).__name__ + ":" + str(e)[:60]
else:
    out["artifact"] = None
print("STEP2_ANSWER " + json.dumps(out, sort_keys=True))
PY
