#!/usr/bin/env python
"""OG-cd-3 Phase B step 4 (the CTO's CT3, the COO's D6): a READ-ONLY census of the top-level prefixes of s3://opal-data-assets, from this seat's own role (list only; no object body is read, nothing is written).
  1. the top-level prefixes (Delimiter "/"): their number, and which are the eight silver sources
  2. for every top-level prefix BEYOND the eight: does it hold a `silver/` child, directly (<X>/silver/) or one level down (<X>/<scope>/silver/)? (a non-zero count narrows statement (a) in the OG-ap-50 cycle)
  3. the COO's extra: for the eight roots' silver tables, the partition folder names one level under each table, counted by whether they are `date=` names or not (the silver key shape was measured on one table only)
Counts and prefix names only; a bounded number of list calls per table (MaxKeys 200 pages cap).
usage: python cd3_ct3_census.py <out.json>"""
from __future__ import annotations

import json
import re
import sys
import time

import boto3

B = "opal-data-assets"
EIGHT = ["schwab", "orion", "eclipse", "blackdiamond", "trueshares", "pathfinder", "msn", "smartx"]
s3 = boto3.client("s3", region_name="us-east-1")
calls = [0]


def children(prefix, cap_pages=5):
    out, token, pages = [], None, 0
    while pages < cap_pages:
        kw = {"Bucket": B, "Prefix": prefix, "Delimiter": "/"}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        calls[0] += 1
        out += [p["Prefix"] for p in r.get("CommonPrefixes", [])]
        pages += 1
        token = r.get("NextContinuationToken") if r.get("IsTruncated") else None
        if not token:
            return out, True
    return out, False


def has_any(prefix):
    r = s3.list_objects_v2(Bucket=B, Prefix=prefix, MaxKeys=1)
    calls[0] += 1
    return r.get("KeyCount", 0) > 0


def main():
    top, complete = children("")
    names = sorted(p.rstrip("/") for p in top)
    beyond = [n for n in names if n not in EIGHT]
    holders, scopes_checked = [], 0
    for x in beyond:
        direct = has_any(x + "/silver/")
        sc, _c = children(x + "/")
        one_down = []
        for s in sc:
            scopes_checked += 1
            if has_any(s + "silver/"):
                one_down.append(s)
        if direct or one_down:
            holders.append({"prefix": x + "/", "silver_directly": direct, "scopes_with_silver_child": [s for s in one_down]})
    # the COO's extra: partition folder names under the eight roots' silver tables
    tables, non_date, date_named, capped = 0, [], 0, 0
    for root in EIGHT:
        scs, _c = children(root + "/")
        for sc in scs:
            tbls, c2 = children(sc + "silver/")
            for t in tbls:
                tables += 1
                parts, c3 = children(t, cap_pages=2)
                if not c3:
                    capped += 1
                for p in parts:
                    leaf = p[len(t):].rstrip("/")
                    if re.fullmatch(r"date=\d{4}-\d{2}-\d{2}", leaf):
                        date_named += 1
                    else:
                        non_date.append(p)
    rec = {"read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "bucket": B, "from": "this seat's own role: list_objects_v2 only (no object read, no write)",
           "top_level_prefixes": len(names), "top_level_listing_complete": complete, "the_eight_present": sorted(n for n in names if n in EIGHT), "eight_missing_from_listing": sorted(n for n in EIGHT if n not in names),
           "prefixes_beyond_the_eight": beyond, "beyond_checked_scopes": scopes_checked, "beyond_holding_a_silver_child": holders, "beyond_holding_a_silver_child_count": len(holders),
           "silver_partition_names": {"tables_checked": tables, "date_named_partition_folders": date_named, "non_date_named_partition_folders": len(non_date), "non_date_examples_first_10": non_date[:10],
                                      "tables_whose_listing_hit_the_page_cap": capped},
           "list_calls_made": calls[0]}
    with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, indent=1) + "\n")
    print(json.dumps({k: rec[k] for k in rec if k not in ("non_date_examples_first_10",)}, indent=1)[:2600])


if __name__ == "__main__":
    main()
