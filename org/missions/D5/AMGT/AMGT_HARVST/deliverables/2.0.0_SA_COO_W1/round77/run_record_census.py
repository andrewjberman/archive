"""HARVST round 77 -- read-only census of the persisted harvest run records written since the runner's activation.

Groups every run record under `store.table_prefix("amgt", "bronze", "run_record")` written at or after 2026-10-09T08:57Z
by the publisher prefix of the keys it names, and sums its fetch outcome counts. GETs only; nothing is written.
Run from the repo root: `PYTHONPATH=. python <this file>`.
"""
import collections
import json

import lib.research.harvest.store as store

SINCE = "2026-10-09T08:57"
KEY_FIELDS = ("keys_fetched", "keys_skipped_as_held", "keys_rejected", "keys_fetched_not_stored", "keys_stored_join",
              "keys_held")


def publishers(record):
    found = set()
    for field in KEY_FIELDS:
        for entry in record.get(field) or []:
            key = entry.get("key") if isinstance(entry, dict) else entry
            if isinstance(key, str) and ":" in key:
                found.add(key.split(":")[0])
    for job in record.get("jobs") or []:
        if isinstance(job, dict):
            for field in ("publisher", "source"):
                if job.get(field):
                    found.add(str(job[field]))
    return ",".join(sorted(found)) or "NONE"


def main():
    client = store._default_client()
    prefix = store.table_prefix("amgt", "bronze", "run_record")
    keys, total = [], 0
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            total += 1
            if obj["LastModified"].isoformat() >= SINCE:
                keys.append(obj["Key"])
    print("PREFIX %s: %d run record(s), %d written since %sZ" % (prefix, total, len(keys), SINCE))
    agg = collections.defaultdict(collections.Counter)
    first, last = {}, {}
    for key in sorted(keys):
        record = json.loads(client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read())
        pub = publishers(record)
        agg[pub]["runs"] += 1
        for name, value in (record.get("fetch_outcome_counts") or {}).items():
            agg[pub][name] += value
        agg[pub]["mode_" + str(record.get("retrieval_mode"))] += 1
        first.setdefault(pub, record["started_at"][:19])
        last[pub] = record["finished_at"][:19]
    for pub, counts in agg.items():
        print(pub, dict(counts), "first", first[pub], "last", last[pub])


if __name__ == "__main__":
    main()
