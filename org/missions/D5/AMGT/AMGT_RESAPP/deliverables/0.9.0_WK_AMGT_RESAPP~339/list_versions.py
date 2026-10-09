"""List every object version under drafting/v1/ (read only). usage: list_versions.py <out.txt>"""
import sys
import boto3
s3 = boto3.client("s3", region_name="us-east-1")
rows = []
for page in s3.get_paginator("list_object_versions").paginate(Bucket="opal-data-harvest", Prefix="drafting/v1/"):
    for v in page.get("Versions", []):
        rows.append("%s | %s | %s | latest=%s | %d" % (v["Key"], v["VersionId"], v["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), v["IsLatest"], v["Size"]))
    for m in page.get("DeleteMarkers", []):
        rows.append("%s | %s | DELETEMARKER" % (m["Key"], m["VersionId"]))
rows.sort()
open(sys.argv[1], "w", newline="\n").write("\n".join(rows) + "\n")
print("versions listed under drafting/v1/: %d; NU rows: %d" % (len(rows), sum(1 for r in rows if "/NU_US_Equity.json" in r)))
