"""DB-b-12 LOCAL dry run: build one per-client summary per 49 Financial directory client that has a published account.

READS ONLY. Nothing is uploaded, no S3 write, no invoke. Reads: (1) the directory the `directory/` function serves
(latest.json pointer -> the dated directory.json), (2) the published `account=<raw>/` prefixes of the firm's platinum
reporting table and each one's series + manifest. A published account's raw key is minted to its issued opaque id with
the ONE normalizer (_ids/ids.py) so it joins the directory's account ids exactly as the read route does.

Writes CLIENT_SUMMARY_R5.json beside this file: ids only -- no client or account name, no custodian account number.
Usage (from the repo root): python <this file>
"""
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
IR = ROOT / "infra" / "aws" / "lambda" / "investor-reporting"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(IR / "reporting-publish"))
sys.path.insert(0, str(IR / "_ids"))

import boto3  # noqa: E402
import ids as _ids  # noqa: E402
import handler  # noqa: E402  (resolve_firm only; no network at import)
import publisher  # noqa: E402
from lib import opal_naming  # noqa: E402

OUT = Path(__file__).resolve().parent / "CLIENT_SUMMARY_R5.json"
DIRECTORY_BUCKET = "opal-data-bd"  # data/firm_registry.json: the client firm's directory bucket (legacy bd bucket)
POINTER_KEY = "investor-reporting/directory/latest.json"  # directory/handler.py: DIRECTORY_PREFIX + "/latest.json"


def main():
    t0 = time.time()
    s3 = boto3.client("s3", region_name="us-east-1")
    _, firm = handler.resolve_firm()
    pointer = json.loads(s3.get_object(Bucket=DIRECTORY_BUCKET, Key=POINTER_KEY)["Body"].read())
    directory = json.loads(s3.get_object(Bucket=DIRECTORY_BUCKET, Key=pointer["key"])["Body"].read())
    entries = directory["entries"]

    probe_bucket, probe_key = handler._split(opal_naming.address("irpt", firm, "platinum", "reporting", "account=0"))
    prefix = probe_key.rsplit("account=", 1)[0]
    raws = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=probe_bucket, Prefix=prefix, Delimiter="/"):
        for c in page.get("CommonPrefixes", []):
            tail = c["Prefix"][len(prefix):].strip("/")
            if tail.startswith("account="):
                raws.append(tail[len("account="):])
    published = {}
    for raw in raws:
        base = "account=%s/" % raw
        series = json.loads(gzip.decompress(s3.get_object(Bucket=probe_bucket, Key=prefix + base + publisher.SERIES_OBJECT)["Body"].read()))
        manifest = json.loads(s3.get_object(Bucket=probe_bucket, Key=prefix + base + publisher.MANIFEST_OBJECT)["Body"].read())
        published[_ids.opaque_account(firm, raw)] = {"series": series, "manifest": manifest}
    t_read = time.time() - t0

    t1 = time.time()
    summaries, refused_no_published, other_refused = {}, 0, 0
    directory_accounts = set()
    for e in entries:
        client = {"client_id": e["ids"]["client_id"], "account_ids": e["ids"]["account_ids"]}
        directory_accounts.update(client["account_ids"])
        mine = {a: published[a] for a in client["account_ids"] if a in published}
        try:
            summaries[client["client_id"]] = publisher.build_client_summary(client, mine)
        except publisher.ClientNotPublished:
            refused_no_published += 1
        except publisher.PublishRefused:
            other_refused += 1
    build_seconds = time.time() - t1

    covered = sum(len(s["accounts"]) for s in summaries.values())
    unmatched = sorted(a for a in published if a not in directory_accounts)
    cid = sorted(summaries)[0]
    example = summaries[cid]
    builder_call = 'address("irpt", "%s", "platinum", "reporting", "client=%s", "summary.json")' % (firm, cid)
    record = {
        "builder_call": builder_call,
        "address_example": publisher.summary_address(firm, cid),
        "clients": len(summaries),
        "accounts_covered": covered,
        "seconds": round(time.time() - t0, 3),
        "shape": example,
        "directory_source": "s3://%s/%s -> %s (pointer as_of_business_date %s, directory_revision %s, %d entries, %d account ids): "
                            "the file directory/handler.py loads for the 49 Financial viewer; entry ids.client_id -> ids.account_ids"
                            % (DIRECTORY_BUCKET, POINTER_KEY, pointer["key"], pointer["as_of_business_date"],
                               pointer["directory_revision"], len(entries), len(directory_accounts)),
        "directory_clients": len(entries),
        "directory_accounts": len(directory_accounts),
        "published_accounts_read": len(published),
        "published_accounts_not_in_directory": len(unmatched),
        "clients_refused_no_published_account": refused_no_published,
        "clients_refused_other": other_refused,
        "read_seconds": round(t_read, 3),
        "build_seconds": round(build_seconds, 4),
        "uploaded": False,
    }
    OUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("clients=%d accounts_covered=%d directory_clients=%d refused_no_published=%d other_refused=%d seconds=%.2f" % (
        len(summaries), covered, len(entries), refused_no_published, other_refused, record["seconds"]))
    print("address_example=%s" % record["address_example"])


if __name__ == "__main__":
    main()
