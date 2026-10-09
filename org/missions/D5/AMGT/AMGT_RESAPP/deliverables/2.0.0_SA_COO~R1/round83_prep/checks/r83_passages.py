"""AMGT_RESAPP round-83 PREP (DRAFT, not issued) -- the passage map over ASML NA's STORED re-cut excerpt (row AMGT_RESAPP-D1-W324-S1).

  python r83_passages.py --crit AC1 [--cache <file>]

Reads ONE stored object read-only: the round-82 silver part that carried ASML NA's parser-2.0.0 excerpt
(opal-data-harvest, sec/harvest/silver/filing_source/date=2026-10-09/part-20261009T082333Z.parquet, VersionId
k3bWqFRPQhvTephepe01vjYL0sPgTcky -- superseded by the rollback part, kept by versioning). --cache names a local copy of that
parquet instead. Runs lib.research.filings.passages.build_passage_map on the excerpt text and its item labels, in-process.
No model call, no write.

AC1 (build):
  P1  every excerpt item reaches the passage map: for each item, the passages' chars over the item's non-blank line chars,
      and Item 4.B (the business section) covers at least 50% (base: 8 passages, about 1%).
  P2  no two consecutive passages glue a word when their texts are concatenated the way analyze.py:411 renders content
      blocks ("".join): 0 adjacent-line pairs where one passage ends in a letter or digit and the next starts with one
      (base: the cited_text "continue torise" class).
Verdict: R83 PASSAGES AC1: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

BUCKET = "opal-data-harvest"
KEY = "sec/harvest/silver/filing_source/date=2026-10-09/part-20261009T082333Z.parquet"
VERSION = "k3bWqFRPQhvTephepe01vjYL0sPgTcky"
BUSINESS_FLOOR = 0.50


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _excerpt(cache):
    import io

    import pyarrow.parquet as pq

    if cache:
        data = open(cache, "rb").read()
    else:
        import boto3

        data = boto3.client("s3", region_name="us-east-1").get_object(
            Bucket=BUCKET, Key=KEY, VersionId=VERSION)["Body"].read()
    rows = pq.read_table(io.BytesIO(data)).to_pylist()
    row = [r for r in rows if r.get("security_key") == "ASML_NA_Equity"][0]
    return json.loads(row["object_json"])["excerpt"]


def _bands(text, labels):
    """(label, start, end) of each item, located by its heading line in the excerpt."""
    found = []
    offset = 0
    upper = [x.upper() for x in labels]
    for line in text.split("\n"):
        if line.strip().upper() in upper:
            found.append((line.strip().upper(), offset))
        offset += len(line) + 1
    return [(lab, s, found[i + 1][1] if i + 1 < len(found) else len(text)) for i, (lab, s) in enumerate(found)]


def crit_ac1(cache):
    root = _root()
    if root not in sys.path:
        sys.path.insert(0, root)
    from lib.research.filings.passages import build_passage_map

    excerpt = _excerpt(cache)
    text, labels = excerpt["text"], excerpt["items"]
    passages = build_passage_map(text, labels)
    print("excerpt chars %d, items %s, passages %d" % (len(text), labels, len(passages)))
    ok = True
    business_share = None
    for label, start, end in _bands(text, labels):
        item_chars = sum(len(x.strip()) for x in text[start:end].split("\n") if x.strip()) - len(label)
        covered = sum(len(p["text"].strip()) for p in passages if start <= p["start"] < end)
        n = sum(1 for p in passages if start <= p["start"] < end)
        share = covered / item_chars if item_chars else 0.0
        print("  %-55s passages %4d  chars %6d of %6d  (%.1f%%)" % (label, n, covered, item_chars, 100 * share))
        if label.startswith("ITEM 4.B"):
            business_share = share
    if business_share is None or business_share < BUSINESS_FLOOR:
        print("FAIL P1 Item 4.B coverage %s, floor %.0f%%" % (
            "absent" if business_share is None else "%.1f%%" % (100 * business_share), 100 * BUSINESS_FLOOR))
        ok = False
    else:
        print("PASS P1 Item 4.B coverage %.1f%%" % (100 * business_share))
    glue = 0
    pairs = 0
    for a, b in zip(passages, passages[1:]):
        if text[a["end"]:b["start"]].strip():
            continue  # not adjacent: text between them was dropped, a separate question (P1)
        pairs += 1
        if a["text"].rstrip()[-1:].isalnum() and b["text"].lstrip()[:1].isalnum() and a["text"] == a["text"].rstrip():
            glue += 1
    print("%s P2 adjacent passage pairs that glue a word under \"\".join: %d of %d" % ("PASS" if glue == 0 else "FAIL", glue, pairs))
    ok = ok and glue == 0
    print("R83 PASSAGES AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--cache", default=os.environ.get("R83_SILVER_CACHE"))
    args = ap.parse_args()
    sys.exit(crit_ac1(args.cache))


if __name__ == "__main__":
    main()
