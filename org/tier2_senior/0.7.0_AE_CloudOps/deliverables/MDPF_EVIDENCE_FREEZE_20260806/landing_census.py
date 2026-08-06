"""MDPF_PROPVALIDATION Phase 0 -- H1/H2 landing-clock census, v3 (boto3/true-UTC).

WHY v3 EXISTS -- the v1/v2 defect, recorded because it is the whole lesson:
`aws s3 ls` prints LastModified in the CALLER'S LOCAL TIME, not UTC. This box is ET.
v1/v2 parsed that local string, stamped tzinfo=UTC on it, then converted to ET a
second time -- shifting every reading 4h early and appearing to falsify the pack's
H1 Eclipse landing (10:16 ET -> a fake 06:16 ET). Caught only by a positive control:
head-object returned 2026-08-06T14:16:06+00:00 for the object `s3 ls` printed as
10:16:06. Two instruments, same object, four hours apart, both plausible.

v3 uses boto3 ListObjectsV2, whose LastModified is a real tz-aware UTC datetime, so
no string parsing and no offset can be applied twice. It also paginates explicitly --
the partition counts here run past 2000, and a page count wearing a total's clothing
is the sibling failure.

Still true from v2 and still needed:
 - DUE is per-cadence: partition D is due 08:40 ET on D+offset, not at a bare wall clock.
 - BACKFILL rewrites report the rewrite time; >1 partition sharing a landing minute is
   a bulk event, reported separately, never silently dropped.

READ-ONLY.
"""
from __future__ import annotations

import collections
import datetime as dt
import re
import sys
from zoneinfo import ZoneInfo

import boto3

ET = ZoneInfo("America/New_York")
DUE_ET = (8, 40)
OFFSET = {"same_day": 0, "T-1": 1, "D+2": 2}

FEEDS = [
    ("49financial", "smartx_model_aum_daily",         "same_day", "opal-data-assets", "smartx/platform/silver/fact_model_aum_daily"),
    ("49financial", "smartx_model_allocation_roster", "same_day", "opal-data-assets", "smartx/platform/silver/fact_model_allocation_roster"),
    ("49financial", "schwab_rps_s2",                  "T-1",      "opal-data-assets", "schwab/08242234/silver/fact_rps_s2"),
    ("inflection",  "eclipse_portfolios_full",        "T-1",      "opal-data-assets", "eclipse/inflection/silver/fact_portfolios_full"),
    ("inflection",  "orion_assets",                   "same_day", "opal-data-assets", "orion/inflection/silver/fact_assets"),
    ("cottonwood",  "bd_model_roster",                "same_day", "opal-data-assets", "blackdiamond/cottonwood/silver/fact_model_roster"),
    ("cottonwood",  "bd_holdings_s2",                 "D+2",      "opal-data-assets", "blackdiamond/cottonwood/silver/fact_holdings_s2"),
    ("cottonwood",  "bd_allocations_s2",              "D+2",      "opal-data-assets", "blackdiamond/cottonwood/silver/fact_allocations_s2"),
]

DATE_RE = re.compile(r"date=(\d{4}-\d{2}-\d{2})/")
WINDOW = int(sys.argv[1]) if len(sys.argv) > 1 else 30
SHOW = sys.argv[2:] or None
s3 = boto3.client("s3")


def hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def scan(bucket, prefix):
    parts, objs, pages, empties = collections.defaultdict(list), 0, 0, 0
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix + "/"):
        pages += 1
        for o in page.get("Contents", []):
            objs += 1
            if o["Size"] == 0:
                empties += 1
                continue
            m = DATE_RE.search(o["Key"])
            if m:
                parts[m.group(1)].append(o["LastModified"])   # tz-aware UTC, no parsing
    return parts, objs, pages, empties


def main():
    now_et = dt.datetime.now(ET)
    print(f"MDPF H1/H2 LANDING CENSUS v3 (boto3, true UTC) | now={now_et:%Y-%m-%d %H:%M %Z} "
          f"| window={WINDOW}d")
    print(f"DUE = {DUE_ET[0]:02d}:{DUE_ET[1]:02d} ET on (partition + cadence offset)."
          f"  BACKFILL = >1 partition sharing one landing minute.\n")
    floor = (now_et.date() - dt.timedelta(days=WINDOW)).isoformat()
    summary = []

    for firm, feed_id, cadence, bucket, prefix in FEEDS:
        if SHOW and feed_id not in SHOW:
            continue
        parts, objs, pages, empties = scan(bucket, prefix)
        print("=" * 106)
        print(f"{firm}/{feed_id}  cadence={cadence}  (due D+{OFFSET[cadence]} 08:40 ET)")
        print(f"  s3://{bucket}/{prefix}/")
        print(f"  DENOMINATOR: {objs} objects across {pages} API pages, "
              f"{len(parts)} partitions, {empties} zero-byte skipped")
        if not parts:
            print("  ZERO PARTITIONS -- absent or wrong prefix. Not silently dropped.")
            summary.append((feed_id, cadence, "ZERO-PARTITIONS", "", ""))
            continue
        inwin = {k: v for k, v in parts.items() if k >= floor}
        print(f"  IN WINDOW: {len(inwin)} of {len(parts)} (history {min(parts)}..{max(parts)})")
        if not inwin:
            summary.append((feed_id, cadence, "NONE-IN-WINDOW", "", ""))
            continue

        landings = {p: min(v) for p, v in inwin.items()}
        groups = collections.Counter(v.strftime("%Y-%m-%d %H:%M") for v in landings.values())

        rows, daily, bf, late = [], 0, 0, []
        for p in sorted(landings):
            lu = landings[p]
            le = lu.astimezone(ET)
            isbf = groups[lu.strftime("%Y-%m-%d %H:%M")] > 1
            due = dt.datetime.combine(
                dt.date.fromisoformat(p) + dt.timedelta(days=OFFSET[cadence]),
                dt.time(*DUE_ET), tzinfo=ET)
            dh = (le - due).total_seconds() / 3600
            rows.append((p, lu, le, isbf, dh))
            if isbf:
                bf += 1
            else:
                daily += 1
                if dh > 0:
                    late.append((p, le, dh))

        print(f"  {'partition':<12}{'landed UTC':<22}{'landed ET':<22}{'vs DUE':>9}  flag")
        for p, lu, le, isbf, dh in rows:
            print(f"  {p:<12}{lu:%Y-%m-%dT%H:%M:%SZ}     {le:%Y-%m-%d %H:%M:%S %Z}  "
                  f"{dh:>+8.1f}h  {'BACKFILL' if isbf else ('LATE' if dh > 0 else 'ok')}")

        clean = [r for r in rows if not r[3]]
        if clean:
            mins = sorted(r[2].hour * 60 + r[2].minute for r in clean)
            clock = (f"min={hhmm(mins[0])} med={hhmm(mins[len(mins)//2])} "
                     f"max={hhmm(mins[-1])}")
        else:
            clock = "no daily rows"
        print(f"  DAILY n={daily}   BACKFILL-CONTAMINATED n={bf}")
        print(f"  DAILY ET landing clock: {clock}")
        print(f"  MISSES 08:40 ET due (daily rows only): {len(late)} of {daily}")
        for p, le, dh in late:
            print(f"      MISS {p} landed {le:%Y-%m-%d %H:%M %Z}  {dh:+.1f}h past due")
        summary.append((feed_id, cadence, f"{daily}d/{bf}bf", clock, f"{len(late)}/{daily}"))

    print("\n" + "=" * 106)
    print("SUMMARY -- daily landing clock in ET, backfill excluded, true-UTC sourced")
    print(f"  {'feed':<34}{'cadence':<10}{'n(daily/bf)':<14}{'ET clock':<34}{'miss 08:40'}")
    for r in summary:
        print(f"  {r[0]:<34}{r[1]:<10}{r[2]:<14}{r[3]:<34}{r[4]}")


if __name__ == "__main__":
    main()
