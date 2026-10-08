"""OPLGTW OG-bf-1 AC2 (difference control, C3 "Do not repair source data or rewrite silver values"): the backfill
wrote completion records only.

For every date the worker's record lists under `backfilled`, per master: read the completion record now on S3, and
for every served-dataset object it names (catalog.head_set) HEAD it at that VersionId and require its LastModified to
be EARLIER than the record's `started_utc` (the backfill's own start). A silver object written by the backfill reads
later and fails. Prints the denominator of objects checked.

  python bf1.AC2.py <record.json> <repo_root>
"""
import datetime as dt
import json
import sys
from pathlib import Path

import boto3

BUCKET = "opal-data-assets"


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        rec = json.load(open(argv[1], encoding="utf-8"))
        started = dt.datetime.fromisoformat(str(rec["started_utc"]).replace("Z", "+00:00"))
    except (OSError, ValueError, KeyError) as exc:
        print("record unreadable or no started_utc: %s (%s)" % (argv[1], type(exc).__name__))
        print("RESULT: FAIL")
        return 1
    root = Path(argv[2])
    sys.path.insert(0, str(root / "infra/aws/ec2/opal-gateway"))
    from app.integrations.schwab import catalog as cat
    contract = cat.parse_contract(json.loads((root / "org/standards/NFRA_OPLGTW_CONTRACT.json").read_text(encoding="utf-8")))
    s3 = boto3.client("s3", region_name="us-east-1")
    ok, checked, dates = True, 0, 0
    for m, mrec in sorted((rec.get("masters") or {}).items()):
        for d in mrec.get("backfilled") or []:
            dates += 1
            key = "schwab/%s/meta/complete/date=%s.json" % (m, d)
            try:
                marker = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
            except Exception as exc:
                print("FAIL: %s unreadable (%s)" % (key, type(exc).__name__))
                ok = False
                continue
            for ref in cat.head_set(marker.get("closure") or {}, contract):
                checked += 1
                try:
                    h = s3.head_object(Bucket=BUCKET, Key=ref["key"], VersionId=ref["version_id"] or "")
                except Exception as exc:
                    print("FAIL: %s@%s does not HEAD (%s)" % (ref["key"], ref["version_id"], type(exc).__name__))
                    ok = False
                    continue
                if h["LastModified"] >= started:
                    print("FAIL: %s was modified %s, after the backfill began %s" % (ref["key"], h["LastModified"],
                                                                                   started))
                    ok = False
    print("backfilled dates %d; served objects checked %d" % (dates, checked))
    if dates == 0 or checked == 0:
        ok = False
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
