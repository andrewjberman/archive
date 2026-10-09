"""One versioned put of the repaired NU drafting document (the write of AMGT-jj-2). usage: put_repaired.py <repaired.json> <expected live VersionId>
Refuses unless the live latest VersionId is the expected one; carries the live object's ContentType and SSE; sets the
document-sha256 metadata to the sha256 of the NEW body bytes (the repo's own convention, lib/research/corpus/gold.py:81-91)."""
import hashlib
import sys
import boto3
B, K = "opal-data-harvest", "drafting/v1/NU_US_Equity.json"
s3 = boto3.client("s3", region_name="us-east-1")
h = s3.head_object(Bucket=B, Key=K)
print("live before:", h["VersionId"], h["ContentType"], h.get("Metadata"), h.get("ServerSideEncryption"))
if h["VersionId"] != sys.argv[2]:
    print("STOP: live latest is not the expected VersionId")
    sys.exit(2)
body = open(sys.argv[1], "rb").read()
digest = hashlib.sha256(body).hexdigest()
kw = dict(Bucket=B, Key=K, Body=body, ContentType=h["ContentType"], Metadata=dict(h.get("Metadata") or {}, **{"document-sha256": digest}))
if h.get("ServerSideEncryption"):
    kw["ServerSideEncryption"] = h["ServerSideEncryption"]
r = s3.put_object(**kw)
back = s3.head_object(Bucket=B, Key=K, VersionId=r["VersionId"])
print("PUT OK: new VersionId", r["VersionId"], "bytes", len(body), "sha256", digest, "read-back metadata", back.get("Metadata"))
