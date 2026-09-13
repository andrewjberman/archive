#!/usr/bin/env python3
"""
POSN_ASTTAX.TO-S1A-1 -- S1a-AC5: compare the hardcoded ETF_CLASSIFICATIONS dict
(the candidate AUTHORING one-place) against the live DynamoDB `etf-classifications`
table (the candidate STORE one-place, and the SERVING source's backing store).

READ-ONLY. Only `describe_table` (already covered by AC4) and paginated `scan` are
issued against DynamoDB. No put/update/delete, ever.

Usage:
    python compare_table_to_dict.py --compare-table-to-dict

Prints, in order:
  1. DICT_COUNT    -- number of tickers in ETF_CLASSIFICATIONS (the dict's denominator).
  2. TABLE_COUNT   -- number of items actually scanned from the table, counted
                      CLIENT-SIDE across every page (the table's denominator; NOT
                      the DescribeTable ItemCount estimate used in AC4).
  3. DISAGREE_COUNT -- size of the disagreement set, always printed even when 0.
  4. The disagreement set itself, one line per ticker, in the form:
        TICKER: dict says X, table says Y
     where X or Y is the literal string MISSING when the ticker is absent from
     that side entirely (a ticker in one place and not the other IS a
     disagreement for this order's purposes -- FWD-5 asks whether a change in one
     place is reflected in the other, and absence-on-one-side is the sharpest
     possible failure to reflect).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# _shared holds the hardcoded dict; import it directly by path so this script
# does not need to be run from any particular cwd. Resolve the repo root via
# `git rev-parse` rather than parent-walking a fixed depth, so a future move of
# this script cannot silently walk to the wrong directory.
import subprocess  # noqa: E402

def _repo_root() -> Path:
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(Path(__file__).resolve().parent),
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(out.stdout.strip())


ROOT = _repo_root()
SHARED_DIR = ROOT / "infra" / "aws" / "lambda" / "v2_portal" / "_shared"
sys.path.insert(0, str(SHARED_DIR))

import etf_classification as ec  # noqa: E402

import boto3  # noqa: E402
from botocore.exceptions import BotoCoreError, ClientError  # noqa: E402

TABLE_NAME = "etf-classifications"
REGION = "us-east-1"


def load_dict():
    """Return {ticker: asset_class} from the hardcoded module."""
    return dict(ec.ETF_CLASSIFICATIONS)


def scan_table():
    """Paginate the DynamoDB scan and count CLIENT-SIDE.

    Returns (items_by_ticker, page_count) where items_by_ticker maps
    ticker -> asset_class as served by the table.
    """
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)

    items_by_ticker = {}
    page_count = 0
    scan_kwargs = {}
    while True:
        page_count += 1
        try:
            resp = table.scan(**scan_kwargs)
        except (BotoCoreError, ClientError) as e:
            print(f"ERROR: scan failed on page {page_count}: {e}", file=sys.stderr)
            raise
        for item in resp.get("Items", []):
            ticker = item.get("ticker")
            if ticker is None:
                continue
            items_by_ticker[ticker] = item.get("asset_class", "MISSING-FIELD")
        lek = resp.get("LastEvaluatedKey")
        if not lek:
            break
        scan_kwargs["ExclusiveStartKey"] = lek

    return items_by_ticker, page_count


def compare(dict_map, table_map):
    all_tickers = sorted(set(dict_map) | set(table_map))
    disagreements = []
    for t in all_tickers:
        d = dict_map.get(t, "MISSING")
        s = table_map.get(t, "MISSING")
        if d != s:
            disagreements.append((t, d, s))
    return disagreements


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compare-table-to-dict", action="store_true", required=True)
    ap.parse_args()

    dict_map = load_dict()
    dict_count = len(dict_map)

    table_map, pages = scan_table()
    table_count = len(table_map)  # client-side count across all pages, keyed by ticker

    disagreements = compare(dict_map, table_map)

    print(f"DICT_COUNT: {dict_count}")
    print(f"TABLE_COUNT (client-side, {pages} scan page(s)): {table_count}")
    print(f"DISAGREE_COUNT: {len(disagreements)}")
    if disagreements:
        for t, d, s in disagreements:
            print(f"  {t}: dict says {d}, table says {s}")
    else:
        print("  (empty -- dict and table agree on asset_class for every ticker present in either)")


if __name__ == "__main__":
    main()
