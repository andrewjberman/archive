"""Read-only: download the CURRENT latest drafting draft of each of the five keys, pinned to its VersionId. usage: fetch_prior.py <outdir>"""
import sys
import hashlib
import boto3
s3 = boto3.client("s3", region_name="us-east-1")
B = "opal-data-harvest"
for k in ["ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity"]:
    h = s3.head_object(Bucket=B, Key="drafting/v1/%s.json" % k)
    o = s3.get_object(Bucket=B, Key="drafting/v1/%s.json" % k, VersionId=h["VersionId"])
    body = o["Body"].read()
    open("%s/%s.prior_%s.json" % (sys.argv[1], k, h["VersionId"][:8].replace(".", "_")), "wb").write(body)
    print(k, h["VersionId"], len(body), hashlib.sha256(body).hexdigest()[:12], h["ContentType"], h.get("ServerSideEncryption"), h.get("Metadata"))
