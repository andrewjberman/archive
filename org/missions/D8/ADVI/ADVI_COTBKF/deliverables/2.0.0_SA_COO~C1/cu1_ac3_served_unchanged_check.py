"""ADVI_COTBKF TO-CB-cu-1 AC3 (issuer's check): the read-only cell wrote nothing -- the three served FWD-3 keys still carry the VersionIds
the round-98 apply left.

Reads object METADATA only (head-object); no object body, account, name or value. Prints one line:
  SERVED-UNCHANGED versions_equal=<n> of 3
Expected: versions_equal=3 of 3. Needs AWS read credentials. Read-only.
"""
import boto3

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
APPLIED = {  # the round-98 apply (commit a593268704), read by the issuer 2026-10-16 ~07:19Z
    "daily_returns": "lNzQMjfx6uX2zdFdWKsDANboShtDUz2N",
    "account_day_value": "ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a",
    "month_grades": "nkTE.F82uFSboXr9PEamIENCwFL9cwcC",
}

s3 = boto3.client("s3", region_name="us-east-1")
equal = sum(1 for t, vid in APPLIED.items() if s3.head_object(Bucket=BUCKET, Key=BASE % t).get("VersionId") == vid)
print("SERVED-UNCHANGED versions_equal=%d of 3" % equal)
