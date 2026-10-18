# scratch helper (not a deliverable): READ-ONLY look at the enqueue Lambda's deployed artifact.
# lambda get_function_configuration (one resource), s3 head_object and get_object of ONE zip (read into memory,
# never extracted), and an in-memory listing and byte search of the zip for any crosswalk or slash_safe_key copy.
import base64
import hashlib
import io
import sys
import zipfile

sys.path.insert(0, "C:/Dev/ajb_workspace")
import boto3

REGION = "us-east-1"
FN = "opal-research-pull-enqueue"
BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "research/opal-research-pull-enqueue.zip"

lam = boto3.client("lambda", region_name=REGION)
cfg = lam.get_function_configuration(FunctionName=FN)
print("LAMBDA %s runtime=%s handler=%s codesha256=%s codesize=%s last_modified=%s" % (
    FN, cfg.get("Runtime"), cfg.get("Handler"), cfg.get("CodeSha256"), cfg.get("CodeSize"), cfg.get("LastModified")))
env = (cfg.get("Environment") or {}).get("Variables", {})
print("LAMBDA-ENV keys=%s HARVEST_BUCKET=%s RESEARCH_BUCKET=%s" % (
    sorted(env), env.get("HARVEST_BUCKET"), env.get("RESEARCH_BUCKET")))

s3 = boto3.client("s3", region_name=REGION)
head = s3.head_object(Bucket=BUCKET, Key=KEY)
print("ARTIFACT s3://%s/%s size=%s last_modified=%s version=%s content_sha256_meta=%s" % (
    BUCKET, KEY, head.get("ContentLength"), head.get("LastModified"), head.get("VersionId"),
    (head.get("Metadata") or {}).get("content-sha256")))
body = s3.get_object(Bucket=BUCKET, Key=KEY)["Body"].read()
sha_b64 = base64.b64encode(hashlib.sha256(body).digest()).decode()
print("ARTIFACT-READ bytes=%d sha256_b64=%s matches_live_codesha256=%s" % (
    len(body), sha_b64, sha_b64 == cfg.get("CodeSha256")))
zf = zipfile.ZipFile(io.BytesIO(body))
names = zf.namelist()
print("ARTIFACT-ZIP entries=%d names=%s" % (len(names), names))
hits = []
for n in names:
    data = zf.read(n)
    for needle in (b"slash_safe_key", b"SLASH-", b"crosswalk", b"-SLASH-"):
        if needle in data:
            hits.append((n, needle.decode()))
print("ARTIFACT-ZIP needle_hits=%s" % hits)
src = open("C:/Dev/ajb_workspace/infra/aws/lambda/research/pull_enqueue/lambda_function.py", "rb").read()
deployed = zf.read("lambda_function.py") if "lambda_function.py" in names else b""
print("SOURCE-VS-DEPLOYED lambda_function.py source_sha256=%s deployed_sha256=%s equal=%s" % (
    hashlib.sha256(src).hexdigest(), hashlib.sha256(deployed).hexdigest(), src == deployed))
