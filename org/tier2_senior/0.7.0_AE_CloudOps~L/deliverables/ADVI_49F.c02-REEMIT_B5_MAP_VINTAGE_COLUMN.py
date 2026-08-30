"""ADVI_49F.C02-g-7 B-5: the map-vintage column for dim_identity_crosswalk.

RULED AT 1.0.0_SA_CTO 86535, SHARPENED AT 86702. The B-5 line prints, for each of the
five re-driven dates, the crosswalk's STAMPED map_date beside the nearest stored
neighbours' INFERRED map vintage. Two columns, never conflated:

    map_date (stamped)                    -- exists only after c02-MAPVINTAGE M-3
    map_vintage (inferred from S3 metadata) -- computable now, for every stored partition

WHY THE INFERRED COLUMN MUST READ S3 OBJECT METADATA AND NEVER AN IN-OBJECT FIELD.
This is NOT a defect workaround. `_ingested_at` is the ASOF PARTITION DATE by design --
runner_common.py:16 and :88 (Atom 9, "never a clock"), read at source by 3.0.0_SA_CVO
86712 -- so that a re-run is byte-reproducible. Determinism DELIBERATELY excludes the
production instant from the object. An inferred column built from `_ingested_at` would
therefore return the partition key on every row and agree with itself perfectly: the
anti-correlated shape, where the instrument looks healthiest exactly when it is blind.
The production instant lives in the bucket (LastModified / VersionId) and nowhere else.
DO NOT "fix" Atom 9 to make this column easier -- the exclusion is the feature.

⛔ THE TRAP THIS FILE EXISTS TO STOP ANYONE REPEATING. Do not probe the inference at a
timestamp quoted in a message. The first run of this analysis probed 2026-08-28T09:55Z,
taken from prose reading "written 2026-08-28T09:5xZ", and returned the 08-27 map --
which, combined with the true 224/311 two-day split of the campaign, was one step from a
reported "the campaign split across two map vintages, 224/311". It is false: NO partition
was written at 09:55Z that day; the 08-28 partitions begin at 16:08Z, AFTER the map
landed at 13:16:20Z. A quoted timestamp is a CLAIM, not a coordinate -- probing at it
measures the sentence. This module therefore resolves EVERY partition against its OWN
recorded instant and never accepts a time as an argument.

MEASURED 2026-08-30T08:37Z, denominator 535 crosswalk partitions / 46 map partitions:
    inferred 2026-08-28 map: 533     inferred 2026-08-27 map: 2
    the 2 are date=2024-07-08 (produced 08-28T00:46:18Z) and date=2024-07-09 (00:52:36Z),
    both written before the 08-28 map landed; the vintage flips at date=2024-07-10
    (produced 08-28T16:08:53Z), and the flip IS that landing.
    newest-POPULATED vs newest-ANY semantics DISAGREE on 0 of 535.
    neighbours of the five: date=2026-08-10 -> 08-28 map; date=2026-08-18 -> 08-28 map.

Author: 0.7.0_AE_CloudOps~L
"""

from __future__ import annotations

import argparse
import collections
import sys

import boto3

XWALK_BUCKET = "opal-data-49financial"
XWALK_PREFIX = "gold/advi/dimensions/dim_identity_crosswalk/"
MAP_BUCKET = "opal-data-assets"
MAP_PREFIX = "smartx/platform/silver/fact_allocation_account_map/"

# Header-only map partitions measure 4,507 B; populated ones 775-780 KB. The threshold
# sits between the two by three orders of magnitude, not near either.
EMPTY_MAX_BYTES = 20000

FIVE_DATES = ("2026-08-11", "2026-08-12", "2026-08-13", "2026-08-14", "2026-08-17")


def _partitions(client, bucket, prefix):
    """date -> (LastModified, Size) for every data.parquet under prefix.

    Paginated deliberately: a `list-*` page count is not an object count.
    """
    out = {}
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            if not obj["Key"].endswith("data.parquet"):
                continue
            tag = [seg for seg in obj["Key"].split("/") if seg.startswith("date=")]
            if tag:
                out[tag[0][len("date="):]] = (obj["LastModified"], obj["Size"])
    return out


def _newest_at(candidates, instant):
    """Newest map partition existing AT `instant`, resolved BY TIME.

    Returns (date, tie_count). A tie is reported, never silently broken -- two map
    partitions landing in the same second would make the column ambiguous, and an
    ambiguous column must say so rather than pick.
    """
    live = [c for c in candidates if c[0] <= instant]
    if not live:
        return None, 0
    live.sort()
    newest_t = live[-1][0]
    return live[-1][1], sum(1 for c in live if c[0] == newest_t)


def build(client=None):
    client = client or boto3.client("s3")
    xwalk = _partitions(client, XWALK_BUCKET, XWALK_PREFIX)
    maps = _partitions(client, MAP_BUCKET, MAP_PREFIX)
    populated = sorted((v[0], k) for k, v in maps.items() if v[1] > EMPTY_MAX_BYTES)
    every = sorted((v[0], k) for k, v in maps.items())

    rows = {}
    for date, (lm, _size) in xwalk.items():
        pop_v, pop_tie = _newest_at(populated, lm)
        any_v, any_tie = _newest_at(every, lm)
        rows[date] = {
            "produced": lm,
            "inferred_populated": pop_v,
            "inferred_any": any_v,
            "ambiguous": pop_tie > 1 or any_tie > 1,
        }
    return rows, xwalk, maps, populated


def main(argv=None):
    args = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    args.add_argument("--dates", nargs="*", default=list(FIVE_DATES),
                      help="dates to print the STAMPED-vs-INFERRED line for")
    ns = args.parse_args(argv)

    client = boto3.client("s3")
    rows, xwalk, maps, populated = build(client)

    print("DENOMINATOR: %d crosswalk partitions | %d map partitions (%d populated, %d header-only)"
          % (len(xwalk), len(maps), len(populated), len(maps) - len(populated)))
    if not rows:
        print("REFUSE: 0 crosswalk partitions scanned -- a zero denominator is not a result.")
        return 2

    dist_pop = collections.Counter(r["inferred_populated"] for r in rows.values())
    dist_any = collections.Counter(r["inferred_any"] for r in rows.values())
    print("\nINFERRED map vintage (from S3 LastModified, NEVER an in-object field):")
    print("  %-14s %-12s %s" % ("map vintage", "newest-POP", "newest-ANY"))
    for vintage in sorted(set(dist_pop) | set(dist_any), key=lambda v: (v is None, v)):
        print("  %-14s %-12d %d" % (vintage, dist_pop.get(vintage, 0), dist_any.get(vintage, 0)))
    disagree = sum(1 for r in rows.values() if r["inferred_populated"] != r["inferred_any"])
    print("  SEMANTICS DISAGREE (newest-POP vs newest-ANY): %d of %d" % (disagree, len(rows)))

    ambiguous = [d for d, r in rows.items() if r["ambiguous"]]
    print("  AMBIGUOUS (tied landing times, column cannot be stated): %d%s"
          % (len(ambiguous), (" -> %s" % sorted(ambiguous)[:5]) if ambiguous else ""))

    print("\nB-5 LINE -- STAMPED vs INFERRED, for the five re-driven dates:")
    print("  %-12s %-22s %-22s %s" % ("date", "map_date (stamped)", "map_vintage (inferred)", "produced"))
    stored = sorted(xwalk)
    for date in ns.dates:
        if date in rows:
            r = rows[date]
            print("  %-12s %-22s %-22s %s"
                  % (date, "<read from object at re-drive>", r["inferred_populated"],
                     r["produced"].strftime("%Y-%m-%dT%H:%M:%SZ")))
        else:
            print("  %-12s %-22s %-22s %s"
                  % (date, "NOT YET PRODUCED", "n/a -- no object, no instant", "-"))

    below = [d for d in stored if d < min(ns.dates)]
    above = [d for d in stored if d > max(ns.dates)]
    print("\n  NEAREST STORED NEIGHBOURS (the comparison the island question turns on):")
    for date in ([below[-1]] if below else []) + ([above[0]] if above else []):
        r = rows[date]
        print("    %-12s inferred %-12s produced %s"
              % (date, r["inferred_populated"], r["produced"].strftime("%Y-%m-%dT%H:%M:%SZ")))

    instants = sorted(r["produced"] for r in rows.values())
    print("\n  PRODUCTION SPAN of the stored set: %s .. %s"
          % (instants[0].strftime("%Y-%m-%dT%H:%M:%SZ"), instants[-1].strftime("%Y-%m-%dT%H:%M:%SZ")))
    by_day = collections.Counter(i.strftime("%Y-%m-%d") for i in instants)
    print("  by UTC day: %s" % dict(sorted(by_day.items())))
    print("\nISLAND VERDICT IS A PRINT, NOT AN ARGUMENT: equal inferred vintage across the five")
    print("and their neighbours = no island BY MEASUREMENT; unequal = printed and ruled at the gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
