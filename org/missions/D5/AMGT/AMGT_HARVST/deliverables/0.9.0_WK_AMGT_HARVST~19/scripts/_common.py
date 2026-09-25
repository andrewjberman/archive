"""Shared helpers for HVST-s-1's AC scripts. Read-only; no state mutated here."""
import sys
import os

sys.path.insert(0, os.getcwd())

import lib.research.harvest.store as store
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER
from lib.research.harvest.publication_gold import _iter_all_listing_hits

PUBLISHERS = tuple(sorted(SOURCE_FOR_PUBLISHER))  # barrons, bbg, ft, sa, wsj -- 5, the denominator


def client():
    return store._default_client()


def silver_listing_hit_counts(c):
    """{publisher_code: row_count} across ALL five publishers, denominator PRINTED by caller."""
    counts = {p: 0 for p in PUBLISHERS}
    for row in _iter_all_listing_hits(client=c):
        pub = row.get("publisher")
        if pub in counts:
            counts[pub] += 1
        else:
            counts[pub] = counts.get(pub, 0) + 1
    return counts


def bronze_news_listing_object_counts(c):
    """{publisher_code: object_count} for bronze news_listing, one list_objects_v2 sweep per
    publisher's source prefix."""
    counts = {}
    for pub, source in sorted(SOURCE_FOR_PUBLISHER.items()):
        prefix = store.table_prefix(source, "bronze", "news_listing")
        n = 0
        paginator = c.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            n += len(page.get("Contents", []) or [])
        counts[pub] = n
    return counts
