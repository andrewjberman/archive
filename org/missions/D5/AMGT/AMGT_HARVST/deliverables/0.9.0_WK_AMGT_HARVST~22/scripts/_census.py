"""Shared READ-ONLY census helpers for HVST-v-2 (slot ~22).

Nothing here mutates any state: every function is a list/get against S3 or a `mode=ro` sqlite
read of the MAIN tree's runtime root. The five-publisher denominator comes from the producer's own
`SOURCE_FOR_PUBLISHER` map, never typed here.
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.getcwd())

import lib.research.harvest.store as store
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER
from lib.research.harvest.publication_gold import _iter_all_listing_hits

# The expansion of the task order's <placeholders>MAIN_TREE</placeholders>, given in the spawn
# prompt. Recorded here so every invocation's evidence carries the expanded token.
MAIN_TREE = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace"
RUNTIME_ROOT = MAIN_TREE + "/.runtime/opal-data-harvest"

PUBLISHERS = tuple(sorted(SOURCE_FOR_PUBLISHER))  # barrons, bbg, ft, sa, wsj -- 5, the denominator


def client():
    return store._default_client()


def listing_hit_rows(c):
    """Every silver listing_hit row across all five publishers (no per-key collapse)."""
    return list(_iter_all_listing_hits(client=c))


def row_key(row):
    """The record key silver_append uses for listing_hit, as JSON-safe strings."""
    return "|".join([
        str(row.get("source")),
        str(row.get("query_sha256")),
        str(row.get("fetch_date_utc")),
        str(row.get("search_page")),
        str(row.get("search_rank")),
    ])


def silver_counts(rows):
    counts = {p: 0 for p in PUBLISHERS}
    for row in rows:
        pub = row.get("publisher")
        counts[pub] = counts.get(pub, 0) + 1
    return counts


def silver_part_counts(c):
    """{publisher: part-file count} under each source's silver listing_hit prefix."""
    counts = {}
    for pub, source in sorted(SOURCE_FOR_PUBLISHER.items()):
        prefix = store.table_prefix(source, "silver", "listing_hit")
        n = 0
        for page in c.get_paginator("list_objects_v2").paginate(
                Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                if obj["Key"].endswith(".parquet"):
                    n += 1
        counts[pub] = n
    return counts


def bronze_news_listing_counts(c):
    """{publisher: object count} under each source's bronze news_listing prefix."""
    counts = {}
    for pub, source in sorted(SOURCE_FOR_PUBLISHER.items()):
        prefix = store.table_prefix(source, "bronze", "news_listing")
        n = 0
        for page in c.get_paginator("list_objects_v2").paginate(
                Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            n += len(page.get("Contents", []) or [])
        counts[pub] = n
    return counts


def outbox_census():
    """(publisher, status, count) for both local outbox tables, opened mode=ro."""
    uri = "file:%s/progress.sqlite3?mode=ro" % RUNTIME_ROOT
    con = sqlite3.connect(uri, uri=True)
    try:
        listings = con.execute(
            "SELECT publisher,status,count(*) FROM harvest_listing_outbox GROUP BY publisher,status"
        ).fetchall()
        raws = con.execute(
            "SELECT publisher,status,count(*) FROM harvest_raw_outbox GROUP BY publisher,status"
        ).fetchall()
        pending_listing = con.execute(
            "SELECT id,publisher,query,page,fetched_at,error_code,attempts,retry_at "
            "FROM harvest_listing_outbox WHERE status='pending' ORDER BY rowid"
        ).fetchall()
    finally:
        con.close()
    return {"listing_by_publisher_status": listings, "raw_by_publisher_status": raws,
            "pending_listing_rows": pending_listing}


def print_state(label, rows, parts, bronze, outbox):
    print("%s -- five-publisher denominator: %d (%s)" % (label, len(PUBLISHERS), ", ".join(PUBLISHERS)))
    counts = silver_counts(rows)
    print("  silver listing_hit ROWS per publisher (denominator 5 publishers, %d rows total):"
          % sum(counts.values()))
    for p in PUBLISHERS:
        print("    %-8s %d" % (p, counts.get(p, 0)))
    print("  silver listing_hit PART FILES per publisher:")
    for p in PUBLISHERS:
        print("    %-8s %d" % (p, parts.get(p, 0)))
    print("  bronze news_listing OBJECTS per publisher:")
    for p in PUBLISHERS:
        print("    %-8s %d" % (p, bronze.get(p, 0)))
    print("  local outbox (MAIN tree runtime root, mode=ro):")
    print("    harvest_listing_outbox (publisher,status,n): %r" % (outbox["listing_by_publisher_status"],))
    print("    harvest_raw_outbox     (publisher,status,n): %r" % (outbox["raw_by_publisher_status"],))
    print("    pending listing rows: %r" % (outbox["pending_listing_rows"],))
    return counts
