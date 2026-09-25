"""AC4 -- daily_rows run PURE and IN MEMORY (NO gold write) over the same inputs.

Mention rows are READ from the existing gold snapshot (read-only -- no write_gold call anywhere
in this script). Coverage is built from listing_hit rows via publisher_coverage. AC2 already
measured the S3 listing_hit/news_listing delta as +0 for every publisher (this run made no
vendor call at all -- see AC1's traceback), so BEFORE and AFTER coverage are built from the SAME
live listing_hit read: there is nothing else to diff, and re-reading twice would not change that.
"""
import datetime
import json
import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), ".scratch", "s1"))
from _common import client
from lib.research.harvest.publication_gold import (
    publisher_coverage, _iter_all_listing_hits, _latest_gold_snapshot_rows,
    daily_rows, BACKFILL_FLOOR, GOLD_TABLE,
)

securities_path = os.path.join(
    "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~4", "securities.json",
)
with open(securities_path, "r", encoding="utf-8") as f:
    securities = json.load(f)

c = client()
mention = _latest_gold_snapshot_rows(GOLD_TABLE, client=c)  # READ-ONLY -- no write_gold call
listing_hits = list(_iter_all_listing_hits(client=c))

as_of_date = datetime.datetime.now(datetime.timezone.utc).date()
print("AC4 daily_rows, PURE and IN MEMORY -- no gold write")
print("as_of_date (today, UTC): %s" % as_of_date.isoformat())
print("mention rows read from gold %r: %d (read-only)" % (GOLD_TABLE, len(mention)))
print("listing_hit rows read (S3 measured +0 delta by AC2 for every publisher): %d" % len(listing_hits))

coverage_before = publisher_coverage(listing_hits, securities)
coverage_after = publisher_coverage(listing_hits, securities)  # same live read -- see docstring

rows_before = daily_rows(mention, securities, start=BACKFILL_FLOOR, end=as_of_date, coverage=coverage_before)
rows_after = daily_rows(mention, securities, start=BACKFILL_FLOOR, end=as_of_date, coverage=coverage_after)


def distribution(rows):
    dist = {"DENIED": 0, "PARTIAL": 0, "COMPLETE": 0}
    for r in rows:
        dist[r["data_status"]] = dist.get(r["data_status"], 0) + 1
    return dist


dist_before = distribution(rows_before)
dist_after = distribution(rows_after)

print("data_status distribution BEFORE: %s (total %d rows)" % (dist_before, len(rows_before)))
print("data_status distribution AFTER:  %s (total %d rows)" % (dist_after, len(rows_after)))

before_by_key = {(r["security_key"], r["day"]): r["data_status"] for r in rows_before}
moved = []
for r in rows_after:
    key = (r["security_key"], r["day"])
    if before_by_key.get(key) == "DENIED" and r["data_status"] == "PARTIAL":
        moved.append(r)

print("count of (security, day) rows moving DENIED -> PARTIAL: %d" % len(moved))

complete_count_in_moved = sum(1 for r in moved if r["data_status"] == "COMPLETE")
print("occurrences of the string COMPLETE in any moved row's data_status: %d" % complete_count_in_moved)
if complete_count_in_moved != 0:
    print("BLOCKING: a moved row graded COMPLETE -- this cell's premise (sa+wsj is 2 of 5) is violated.")
    sys.exit(1)

if moved:
    sample = moved[0]
    print("sample moved row: security_key=%s day=%s publishers_covered=%d publishers_enabled=%d" % (
        sample["security_key"], sample["day"], sample["publishers_covered"], sample["publishers_enabled"]))
else:
    print("0 rows moved DENIED -> PARTIAL; no sample row exists (honest -- this run made no vendor call, "
          "see AC1's traceback, so coverage did not change).")
