"""AMGT_RESAPP round 51, AMGT-zz-5 -- lead-list rows carry a name (crosswalk fallback) and "places moved since the last run" (CTO round-50
ruling 5; DSGN FWD-2/3; the page lists `places_moved` as an unserved column at RankedList.tsx:258-261).

Reads `scoped_amgt.read_rankings(movement, subject)` IN PROCESS on this tree over the four lead-panel axes (TRENDING|BREAKOUT x
CHATTER|PRICE) and prints, over every row R:
  --what names:  rows with a name N of R; by source (`name_source`: etf-classifications | crosswalk); rows named by their ticker 0.
                 PASS when N > BASE_NAMED (16 of 66 at the cut, measured over the four axes) and every named row carries `name_source`, and no row is named by its ticker.
  --what moved:  every row carries `places_moved` -- an int (the previous COMPLETE generation's rank minus this rank; positive = moved
                 up) or null WITH `places_moved_reason` (no prior generation / not ranked then). PASS when that holds on all R rows and
                 at least one row carries an int.
usage: python <this> --what names|moved   (from the repo root; reads DynamoDB read-only)"""
import argparse
import os
import sys

sys.path.insert(0, os.getcwd())
BASE_NAMED = 16
AXES = [("trending", "chatter"), ("trending", "price"), ("breakout", "chatter"), ("breakout", "price")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("names", "moved"), required=True)
    a = ap.parse_args()
    from lib.research.api import scoped_amgt as sa
    rows = []
    for mv, sj in AXES:
        got = (sa.read_rankings(mv, sj) or {}).get("rows") or []
        print("axis %s/%s: %d rows" % (mv, sj, len(got)))
        rows.extend(got)
    bad = []
    if a.what == "names":
        named = [r for r in rows if r.get("name")]
        by = {}
        for r in named:
            by[r.get("name_source")] = by.get(r.get("name_source"), 0) + 1
            if not r.get("name_source"):
                bad.append("%s named without name_source" % r.get("ticker"))
            if str(r.get("name")).strip() == str(r.get("ticker") or "").split(" ")[0]:
                bad.append("%s named by its ticker" % r.get("ticker"))
        print("rows with a name %d of %d; by source %s (base %d)" % (len(named), len(rows), by, BASE_NAMED))
        ok = len(named) > BASE_NAMED and not bad
        label = "LEAD-LIST ROWS CARRY MORE NAMES, EACH WITH ITS SOURCE"
    else:
        ints = 0
        for r in rows:
            if "places_moved" not in r:
                bad.append("%s lacks places_moved" % r.get("ticker"))
            elif r["places_moved"] is None:
                if not r.get("places_moved_reason"):
                    bad.append("%s places_moved null without a reason" % r.get("ticker"))
            elif isinstance(r["places_moved"], int):
                ints += 1
            else:
                bad.append("%s places_moved %r not an int" % (r.get("ticker"), r["places_moved"]))
        print("rows %d; places_moved int on %d; null-with-reason on %d" % (len(rows), ints, len(rows) - ints - len(bad)))
        ok = rows and not bad and ints > 0
        label = "LEAD-LIST ROWS CARRY PLACES MOVED"
    for b in bad[:6]:
        print("  BAD", b)
    print("%s: %s" % (label, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
