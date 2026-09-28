"""HVST-z-1 AC4 (JUDGMENT -- PRESENTED, NOT GRADED). READ-ONLY (S3 LIST/GET only).

status: UNVERIFIABLE-BY-INSTRUMENT. status_reason: the oracle is 3.0.0_SA_CVO at L9.
Reads the SERVED newest chatter_event snapshot from S3 (never the builder), and for each event
prints security, span, lead_headline, articles_total, publishers_distinct, tier_a/tier_b and the
headline of every article in the span. Records NO verdict of its own.
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

sys.stdout.reconfigure(encoding="ascii", errors="backslashreplace")
client = store._default_client()
keys = []
for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=store.HARVEST_BUCKET, Prefix=store.table_prefix("amgt", "gold", pg.GOLD_EVENT_TABLE)):
    keys += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
newest = sorted(keys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]
print("status: UNVERIFIABLE-BY-INSTRUMENT   status_reason: judgment; oracle is 3.0.0_SA_CVO at L9")
print("SERVED newest chatter_event snapshot: s3://%s/%s" % (store.HARVEST_BUCKET, newest))

events = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)
mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
# keyed by (security, article): one article can carry a mention row for several securities
mention_by_key = {(r["security_key"], r["article_key"]): r for r in mention}
headlines = pg._headline_by_article_key(client=client)
print("events served: %d\n" % len(events))

for n, e in enumerate(sorted(events, key=lambda r: (r["security_key"], r["first_day"])), 1):
    print("=" * 100)
    print("EVENT %d: security=%s  span=%s..%s (%d day(s))" % (n, e["security_key"], e["first_day"], e["last_day"], e["days_span"]))
    print("  articles_total=%d  publishers_distinct=%d  tier_a=%d  tier_b=%d" % (
        e["articles_total"], e["publishers_distinct"], e["tier_a"], e["tier_b"]))
    print("  lead_headline: %s" % e["lead_headline"])
    print("  articles in the span (%d):" % len(e["article_keys"]))
    for k in e["article_keys"]:
        m = mention_by_key.get((e["security_key"], k), {})
        print("    [%s] %s | %s | %s" % (m.get("signal_tier"), str(m.get("published_utc"))[:16],
                                        pg._row_publisher(m) if m else "?", headlines.get(k)))
print("=" * 100)
print("NO VERDICT RECORDED by this script. Per event, whether the lead names what the burst was about is 3.0.0_SA_CVO's call at L9.")
