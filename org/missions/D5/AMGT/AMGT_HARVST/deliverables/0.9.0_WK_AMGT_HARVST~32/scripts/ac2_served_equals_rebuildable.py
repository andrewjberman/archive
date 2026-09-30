"""HVST-z-1 AC2: C-HV-GOLD-REBUILDABLE on the SERVED plane. READ-ONLY (S3 LIST/GET only).

Builds the event rows IN MEMORY from the newest article_security_mention snapshot (+ silver
headlines, exactly as build_event enriches) and compares row by row, field by field, against the
rows the SERVED newest chatter_event snapshot carries (re-read from S3 through
publication_gold._latest_gold_snapshot_rows).
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

client = store._default_client()
keys = []
for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=store.HARVEST_BUCKET, Prefix=store.table_prefix("amgt", "gold", pg.GOLD_EVENT_TABLE)):
    keys += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
newest = sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]
print("SERVED newest chatter_event snapshot: s3://%s/%s (%d parts listed)" % (store.HARVEST_BUCKET, newest, len(keys)))

served = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)
mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
headlines = pg._headline_by_article_key(client=client)
enriched = [dict(r, title=headlines.get(r.get("article_key"))) for r in mention]
built = pg.event_rows(enriched)
print("input: %d mention rows (newest article_security_mention snapshot); in-memory build = %d events; served = %d events"
      % (len(mention), len(built), len(served)))

served_by_id = {r["event_id"]: r for r in served}
built_by_id = {r["event_id"]: r for r in built}
diffs = []
only_served = sorted(set(served_by_id) - set(built_by_id))
only_built = sorted(set(built_by_id) - set(served_by_id))
for i in only_served:
    diffs.append("served-only event_id %s (%s)" % (i, served_by_id[i]["security_key"]))
for i in only_built:
    diffs.append("built-only event_id %s (%s)" % (i, built_by_id[i]["security_key"]))
if len(served_by_id) != len(served) or len(built_by_id) != len(built):
    diffs.append("duplicate event_id within a side: served %d/%d built %d/%d"
                 % (len(served_by_id), len(served), len(built_by_id), len(built)))

matched = 0
fields_compared = 0
for i in sorted(set(served_by_id) & set(built_by_id)):
    s, b = served_by_id[i], built_by_id[i]
    fields = sorted(set(s) | set(b))
    row_ok = True
    for f in fields:
        fields_compared += 1
        if s.get(f) != b.get(f):
            row_ok = False
            diffs.append("event_id %s field %s: served=%r built=%r" % (i, f, s.get(f), b.get(f)))
    matched += 1 if row_ok else 0
    print("  %-16s %s..%s  row %s  (%d fields)" % (s["security_key"], s["first_day"], s["last_day"],
                                                  "EQUAL" if row_ok else "DIFFERS", len(fields)))

denominator = max(len(built), len(served))
print("ROWS EQUAL: %d of %d (fields compared: %d)" % (matched, denominator, fields_compared))
print("DIFFERENCES (%d):" % len(diffs))
for d in diffs:
    print("  " + d)
ok = (not diffs) and matched == len(served) == len(built) == 8
print("RESULT: %s" % ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
