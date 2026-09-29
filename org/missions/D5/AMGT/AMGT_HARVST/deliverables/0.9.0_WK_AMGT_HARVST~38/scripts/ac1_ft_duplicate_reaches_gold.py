"""AC1 (HVST-w-4): follow ft article_id 79c86a189372f457e82c5969 from the device-local sqlite rows to
the table gold reads. READ-ONLY: sqlite via a mode=ro URI, S3 via list_objects_v2 + get_object only.
"""
import io
import os
import sys
from pathlib import Path

os.environ["HARVEST_REFUSE_NETWORK"] = "1"  # standing clause 1 (no vendor call); S3 reads are boto3, not transport.py
ROOT = Path(__file__).resolve()
while not (ROOT / "lib").is_dir():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

import sqlite3  # noqa: E402
import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
import lib.research.harvest.store as store  # noqa: E402
import lib.research.harvest.publication_gold as pg  # noqa: E402

ART = "79c86a189372f457e82c5969"
DB = "file:C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest/progress.sqlite3?mode=ro"
client = boto3.client("s3", region_name="us-east-1")
BUCKET = store.HARVEST_BUCKET


def rows_of(key):
    raw = client.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(raw)).to_pylist()


def keys_under(prefix):
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        out += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
    return out


# 1. the device-local sqlite rows (NOT read by gold)
db = sqlite3.connect(DB, uri=True)
sq = db.execute("select publisher,security_key,article_id,body_sha256 from articles where publisher='ft' and article_id=?", (ART,)).fetchall()
tot = db.execute("select count(*),count(distinct article_id) from articles where publisher='ft'").fetchone()
pk = db.execute("select sql from sqlite_master where name='articles'").fetchone()[0]
print("SQLITE articles ft: %d rows, %d distinct article_id" % tot)
print("SQLITE table DDL: %s" % " ".join(pk.split()))
print("SQLITE rows for %s: %d" % (ART, len(sq)))
for r in sq:
    print("  sqlite row: publisher=%s security_key=%s article_id=%s body_sha256=%s" % r)
print("  distinct body_sha256 across those rows: %d" % len({r[3] for r in sq}))

# 2. ft SILVER article, scanned in full (denominator = rows scanned)
silver_keys = keys_under(store.table_prefix("ft", "silver", "article"))
silver = []
for k in silver_keys:
    for r in rows_of(k):
        silver.append((k, r))
match = [(k, r) for k, r in silver if r.get("article_id") == ART or ART in str(r.get("article_key"))]
akeys = sorted({r["article_key"] for _k, r in match})
print("SILVER ft article: %d parquet parts, %d rows scanned (denominator), %d distinct article_key overall"
      % (len(silver_keys), len(silver), len({r["article_key"] for _k, r in silver})))
print("SILVER rows carrying %s: %d; distinct article_keys: %d %s" % (ART, len(match), len(akeys), akeys))
for k, r in match:
    print("  silver part=%s fetched_at=%s discovered_for=%s title=%r" % (k, r["fetched_at"], r.get("discovered_for"), r.get("title")))

# 3. newest article_security_mention gold snapshot (what chatter_daily reads)
gprefix = store.table_prefix("amgt", "gold", pg.GOLD_TABLE)
gkeys = keys_under(gprefix)
newest = sorted(gkeys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]
gold = rows_of(newest)
print("GOLD article_security_mention: %d snapshot parts, newest=%s, %d rows (denominator)" % (len(gkeys), newest, len(gold)))
grows = [r for r in gold if r["article_key"] in akeys]
print("GOLD rows for %s: %d" % (akeys, len(grows)))
for r in grows:
    print("  gold row: article_key=%s security_key=%s tier=%s mention_count=%s published_utc=%s"
          % (r["article_key"], r["security_key"], r["signal_tier"], r["mention_count"], r["published_utc"]))
pairs = [(r["article_key"], r["security_key"]) for r in grows]
print("  (article_key, security_key) pairs: %d, distinct pairs: %d" % (len(pairs), len(set(pairs))))

# 4. articles_total contribution per security = |set of article_keys| on the security's day (publication_gold.py:584/:621)
contrib = {}
for r in grows:
    day = pg._day_of(r.get("published_utc"))
    contrib.setdefault((r["security_key"], day), set()).add(r["article_key"])
for (sec, day), s in sorted(contrib.items(), key=lambda x: str(x[0])):
    print("  articles_total contribution: security_key=%s day=%s -> %d (set of article_keys %s)" % (sec, day, len(s), sorted(s)))

# whole-table check: any (article_key, security_key) pair repeated in the gold snapshot, ft only
ft_pairs = [(r["article_key"], r["security_key"]) for r in gold if r["publisher"] == "ft"]
print("GOLD ft rows: %d, distinct (article_key,security_key): %d, distinct article_key: %d"
      % (len(ft_pairs), len(set(ft_pairs)), len({p[0] for p in ft_pairs})))

# 5. the served chatter_daily counts for the same (security, day), if present
try:
    dprefix = store.table_prefix("amgt", "gold", pg.GOLD_DAILY_TABLE)
    dkeys = keys_under(dprefix)
    if dkeys:
        dnew = sorted(dkeys, key=lambda k: (pg._DATE_PARTITION_RE.search(k).group(1), k))[-1]
        daily = rows_of(dnew)
        for (sec, day) in sorted(contrib, key=str):
            m = [d for d in daily if d["security_key"] == sec and d["day"] == day]
            print("CHATTER_DAILY newest=%s (%d rows): security_key=%s day=%s articles_total=%s" % (dnew, len(daily), sec, day, [d["articles_total"] for d in m]))
except Exception as exc:  # a read failure is printed, never swallowed
    print("CHATTER_DAILY read: %s: %s" % (type(exc).__name__, exc))

double = len(akeys) > 1 or len(pairs) != len(set(pairs)) or any(len(s) > 1 for s in contrib.values())
print("gold double-counts: %s  (silver article_keys for the article=%d, silver rows=%d, gold rows=%d, distinct gold pairs=%d, max articles_total contribution per (security,day)=%s)"
      % ("YES" if double else "NO", len(akeys), len(match), len(grows), len(set(pairs)),
         max((len(s) for s in contrib.values()), default=0)))
