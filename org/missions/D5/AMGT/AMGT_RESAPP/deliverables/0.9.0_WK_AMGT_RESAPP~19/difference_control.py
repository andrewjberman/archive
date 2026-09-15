"""AMGT_RESAPP.TO-AMGT-rj-5 DELIVER item 4 -- THE DIFFERENCE CONTROL.

THE TWO STORES ARE EXPECTED TO DIFFER, and this prints both sides beside each other so
the difference is a MEASUREMENT rather than an assumption:

  LEFT   the pool (s3://opal-data-harvest), read through INTERFACE P-1 -- the number of
         distinct articles associated with the identity, how many of them the 30-day
         window holds, and the four failure states, each with its own counter.
  RIGHT  the RETIRED DynamoDB articles table (opal-harvest-articles), read ONCE per
         ticker through its old ticker_date_index GSI, FOR THE RECORD ONLY. This is the
         one read of that table this cell makes; nothing here writes it, and the
         producer no longer names it at all.

EQUAL NUMBERS WOULD BE THE SURPRISE. The table has never been populated by any
harvester (its own ItemCount reads 0), so a nonzero count on the right would mean some
writer nobody has named is filling it.

THE COUNT TRAP IS HANDLED ON THE RETRIEVAL: a DynamoDB Query returns a PER-PAGE `Count`,
so this paginates to exhaustion and sums client-side rather than reporting page one as
the answer. The same discipline the pool census needed.

Run: python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~19/difference_control.py"
"""
from __future__ import annotations

import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 7)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from lib.research.coverage import pool_reader  # noqa: E402 -- after the path graft

ARTICLES_TABLE = "opal-harvest-articles"
ARTICLES_TICKER_INDEX = "ticker_date_index"
AS_OF = "2026-09-15"
WINDOW_DAYS = 30

# The three commissioned names, plus ONE name the pool holds no link for (the control:
# a security the store has never heard of must read 0 on BOTH sides, and it is what
# distinguishes "the adapter found nothing" from "the adapter cannot find anything").
NAMES = [
    ("BA_US_Equity", "BA US"),
    ("COST_US_Equity", "COST US"),
    ("HD_US_Equity", "HD US"),
    ("SAP_GY_Equity", "SAP GY"),  # CONTROL: commissioned for packs, never for publications
]


def table_item_count(ticker):
    """One Query against the retired table's old index, paginated to exhaustion.

    Returns (count, note). A missing table or a denied read is REPORTED, never returned
    as a zero -- a zero that means 'refused' is the exact confusion this whole cell is
    about."""
    try:
        import boto3
        from botocore.exceptions import ClientError
    except Exception as exc:  # noqa: BLE001
        return None, "boto3-unavailable:%s" % (type(exc).__name__,)
    client = boto3.client("dynamodb")
    total = 0
    pages = 0
    kwargs = {
        "TableName": ARTICLES_TABLE,
        "IndexName": ARTICLES_TICKER_INDEX,
        "KeyConditionExpression": "ticker = :t",
        "ExpressionAttributeValues": {":t": {"S": ticker}},
        "Select": "COUNT",
    }
    try:
        while True:
            response = client.query(**kwargs)
            pages += 1
            total += response.get("Count", 0)
            last = response.get("LastEvaluatedKey")
            if not last:
                break
            kwargs["ExclusiveStartKey"] = last
    except ClientError as exc:
        return None, "%s" % (exc.response.get("Error", {}).get("Code", "ClientError"),)
    return total, "pages=%d" % (pages,)


def main():
    start, end = pool_reader.window_bounds(WINDOW_DAYS, AS_OF)
    print(
        "DIFFERENCE CONTROL pool=s3://%s vs table=%s (RETIRED as a source) window=%s..%s"
        % (pool_reader.POOL_BUCKET, ARTICLES_TABLE, start, end)
    )
    totals = {"links": 0, "window": 0, "table": 0}
    for identity, ticker in NAMES:
        read = pool_reader.window_read(identity, start, end)
        count, note = table_item_count(ticker)
        states = read["states"]
        totals["links"] += read["store_item_count"]
        totals["window"] += read["items_in_window"]
        totals["table"] += count or 0
        print(
            "%-14s ticker=%-8s pool-links %-3d pool-bodies-in-window %-3d "
            "states missing_body=%d malformed=%d denied=%d partial=%d "
            "key_forms=%s table-items %s (%s)"
            % (
                identity,
                ticker,
                read["store_item_count"],
                read["items_in_window"],
                states["missing_body"],
                states["malformed"],
                states["denied"],
                states["partial"],
                ",".join(read["key_forms"]) or "-",
                "UNREAD" if count is None else count,
                note,
            )
        )
    print(
        "TOTALS pool-links %d pool-bodies-in-window %d table-items %d -- the two stores "
        "DIFFER (equal numbers would be the surprise); denominator 4 of 4 names read"
        % (totals["links"], totals["window"], totals["table"])
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
