"""ADVI_COTBKF TO-CB-ct-1 AC2 (issuer's check): after the apply, did each of the three served keys move to a NEW version while its prior
version stays readable (the rollback)?

Reads only object METADATA (head-object on the key, and on the key at each prior VersionId); no object body, account, name or value.
Prints one line:
  SERVED-WRITE keys=3 moved=<m> prior_readable=<p> sizes_grew=<g>
moved = keys whose current VersionId is not the recorded prior VersionId; prior_readable = keys whose prior VersionId still answers
head-object; sizes_grew = keys whose current ContentLength is larger than the prior (two columns were appended).
Expected after a correct apply: moved=3 prior_readable=3 sizes_grew=3. Before the apply: moved=0 (the criterion FAILS at the base).
Needs AWS read credentials (the applier's). Read-only.
"""
import boto3

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
PRIOR = {  # recorded in NEVER_WIDEN_R97_FWD3_LABELS_COO_HALF.md section 1: (prior VersionId, prior size)
    "daily_returns": ("w9j5YeV1LnNIakNlRTBX6jW1.SDHqmJR", 1651055),
    "account_day_value": ("qIWjLLwCIh_Gx6IblSgyaint2tfJ37pr", 54246028),
    "month_grades": ("QI5Ks8vQwGTwnc9ekyh.DOsyN8PKN3PB", 421751),
}

s3 = boto3.client("s3", region_name="us-east-1")
moved = readable = grew = 0
for t, (vid, size) in PRIOR.items():
    key = BASE % t
    cur = s3.head_object(Bucket=BUCKET, Key=key)
    if cur.get("VersionId") != vid:
        moved += 1
    if int(cur["ContentLength"]) > size:
        grew += 1
    try:
        s3.head_object(Bucket=BUCKET, Key=key, VersionId=vid)
        readable += 1
    except Exception:
        pass
print("SERVED-WRITE keys=3 moved=%d prior_readable=%d sizes_grew=%d" % (moved, readable, grew))
