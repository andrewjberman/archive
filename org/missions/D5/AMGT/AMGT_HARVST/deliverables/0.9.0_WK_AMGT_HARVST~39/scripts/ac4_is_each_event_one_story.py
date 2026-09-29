"""HVST-b-2 AC4 (JUDGMENT -- PRESENTED, NOT GRADED). READ-ONLY (S3 GET only).

Read from S3, not from the builder: the SERVED newest chatter_event snapshot gives each event, its lead and
its article_keys; the newest article_security_mention snapshot + silver headlines give each article's tier,
publisher and title; the PRIOR served snapshot (the second-newest part) gives the events that split or left,
and every one of their articles is followed to the served event it now sits in (or to none). Nothing here is
a verdict: the CVO (3.0.0_SA_CVO~Z, L9) grades whether each served event is ONE story about its own
company and whether its lead names that story.
"""
import io
import os
import sys

import pyarrow.parquet as pq

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 8))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

client = store._default_client()
prefix = store.table_prefix("amgt", "gold", pg.GOLD_EVENT_TABLE)
keys = []
for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
    for o in page.get("Contents", []) or []:
        if o["Key"].endswith(".parquet"):
            keys.append(o["Key"])
keys.sort(key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))
newest_key, prior_key = keys[-1], keys[-2]


def read_key(key):
    body = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(body)).to_pylist()


served = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE, client=client)
prior = read_key(prior_key)
mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
headlines = pg._headline_by_article_key(client=client)
row_of = {}
for r in mention:
    r = dict(r)
    r["title"] = headlines.get(r.get("article_key"))
    row_of[(r["security_key"], r["article_key"])] = r

print("newest part (served): %s -> %d events" % (newest_key, len(served)))
print("prior part          : %s -> %d events" % (prior_key, len(prior)))
print("mention rows %d; silver headlines %d" % (len(mention), len(headlines)))

print("\n=== EVERY SERVED EVENT (read from S3) ===")
served_of_article = {}
for ev in sorted(served, key=lambda e: (e["security_key"], e["first_day"])):
    arts = [row_of[(ev["security_key"], k)] for k in ev["article_keys"]]
    for k in ev["article_keys"]:
        served_of_article[(ev["security_key"], k)] = ev
    pubs = sorted({pg._row_publisher(r) for r in arts if r["signal_tier"] == "A"})
    print("\n== %s  %s..%s  event_id=%s  articles=%d (A=%d B=%d)"
          % (ev["security_key"], ev["first_day"], ev["last_day"], ev["event_id"], ev["articles_total"], ev["tier_a"], ev["tier_b"]))
    print("  tier-A publishers: %s" % pubs)
    print("  SERVED LEAD: %s | %s" % (ev["lead_article_key"], ev["lead_headline"]))
    for r in arts:
        print("      %s %-8s %s | %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"], r["title"]))

print("\n=== EVERY PRIOR EVENT: what became of its articles ===")
for pv in sorted(prior, key=lambda e: (e["security_key"], e["first_day"])):
    now = {}
    for k in pv["article_keys"]:
        ev = served_of_article.get((pv["security_key"], k))
        now.setdefault(ev["event_id"] if ev else None, []).append(k)
    kinds = ("SPLIT" if len([e for e in now if e]) > 1 else
             "LEFT (no article is in a served event)" if list(now) == [None] else
             "kept (some articles left)" if None in now else "kept whole")
    print("\n%s %s..%s  prior id=%s  -> %s" % (pv["security_key"], pv["first_day"], pv["last_day"], pv["event_id"][:16], kinds))
    for k in pv["article_keys"]:
        r = row_of[(pv["security_key"], k)]
        ev = served_of_article.get((pv["security_key"], k))
        where = ("served event %s..%s id=%s" % (ev["first_day"], ev["last_day"], ev["event_id"][:16])) if ev else "IN NO SERVED EVENT"
        print("    %s %-8s %s | %s   => %s" % (r["signal_tier"], pg._row_publisher(r), r["published_utc"].date(), r["title"], where))

print("\nJUDGMENT PRESENTED, NO VERDICT RECORDED. Question for 3.0.0_SA_CVO~Z at L9: is each served event ONE story about its own company, and does its lead name that story?")
