"""One versioned put of a repaired drafting document (AMGT-kk-3). usage: put_kk3.py <KEY> <repaired.json> <expected live VersionId>
Refuses unless the live latest VersionId is the expected one; carries the live object's ContentType, SSE and metadata; sets
document-sha256 to the sha256 of the NEW body bytes (lib/research/corpus/gold.py:81-91). Never a delete."""
import hashlib
import sys
import boto3
B, K = "opal-data-harvest", "drafting/v1/%s.json" % sys.argv[1]
s3 = boto3.client("s3", region_name="us-east-1")
h = s3.head_object(Bucket=B, Key=K)
print("live before:", h["VersionId"], h["ContentType"], h.get("Metadata"), h.get("ServerSideEncryption"))
if h["VersionId"] != sys.argv[3]:
    print("STOP: live latest is not the expected VersionId")
    sys.exit(2)
body = open(sys.argv[2], "rb").read()
digest = hashlib.sha256(body).hexdigest()
kw = dict(Bucket=B, Key=K, Body=body, ContentType=h["ContentType"], Metadata=dict(h.get("Metadata") or {}, **{"document-sha256": digest}))
if h.get("ServerSideEncryption"):
    kw["ServerSideEncryption"] = h["ServerSideEncryption"]
r = s3.put_object(**kw)
back = s3.head_object(Bucket=B, Key=K, VersionId=r["VersionId"])
print("PUT OK: new VersionId", r["VersionId"], "bytes", len(body), "sha256", digest, "read-back metadata", back.get("Metadata"))
