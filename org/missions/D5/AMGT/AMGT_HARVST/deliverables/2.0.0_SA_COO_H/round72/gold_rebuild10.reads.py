"""HARVST served gold rebuild #10 -- THE TWO READS `1.0.0_SA_CTO~Z` msg 31812 asks for, from the rows the diagnostic dump
kept (`.runtime/harvest-backfill/r72_dump/`, PUTS 0). No S3 call, no build.

READ ONE: of the daily rows that changed, which FIELDS moved and on how many rows; and THE STOP TEST: a daily row whose
own-day count field moved on a (security, day) with NO mention pair added, removed or changed for that security on that
published day. Any such row is not new silver.
READ TWO: GSK_LN_Equity's added pairs: how many, by publisher and by match forms, and ten with their titles.
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 8))
DUMP = os.path.join(ROOT, ".runtime", "harvest-backfill", "r72_dump")

OWN_DAY = ("articles_total", "tier_a", "tier_b", "tier_c", "tier_d", "mention_score", "mention_count_total",
           "publishers_distinct", "first_published_utc", "last_published_utc", "publishers_found_codes")
ROLLING = ("trailing_7d_sum", "trailing_30d_sum", "baseline_30d_sum", "baseline_30d_days", "cumulative_ytd")
COVERAGE = ("data_status", "publishers_covered", "publishers_enabled", "publishers_covered_codes")
MENTION_COUNTED = ("mention_count", "signal_tier", "signal_weight", "published_utc", "publisher")


def load(name):
    with io.open(os.path.join(DUMP, name + ".json"), encoding="utf-8") as handle:
        return json.load(handle)


def main():
    sm, bm, sd, bd = load("served_mention"), load("built_mention"), load("served_daily"), load("built_daily")
    print("ROWS READ: mention served %d built %d; daily served %d built %d" % (len(sm), len(bm), len(sd), len(bd)))
    fields = set(bd[0]) - {"security_key", "day"}
    unclassed = sorted(fields - set(OWN_DAY) - set(ROLLING) - set(COVERAGE))
    print("DAILY FIELDS NOT PLACED IN A GROUP (must be only identity fields): %s" % unclassed)

    om = {(r["article_key"], r["security_key"]): r for r in sm}
    nm = {(r["article_key"], r["security_key"]): r for r in bm}
    touched = collections.Counter()
    for key in set(om) ^ set(nm):
        row = om.get(key) or nm[key]
        touched[(row["security_key"], str(row["published_utc"])[:10])] += 1
    for key in set(om) & set(nm):
        if any(om[key].get(f) != nm[key].get(f) for f in MENTION_COUNTED):
            for row in (om[key], nm[key]):
                touched[(row["security_key"], str(row["published_utc"])[:10])] += 1
    print("MENTION: added %d, gone %d; (security, published day) cells with a pair added, gone or re-counted: %d" % (
        len(set(nm) - set(om)), len(set(om) - set(nm)), len(touched)))

    od = {(r["security_key"], str(r["day"])[:10]): r for r in sd}
    nd = {(r["security_key"], str(r["day"])[:10]): r for r in bd}
    per_field = collections.Counter()
    shape = collections.Counter()
    own_moved, own_moved_untouched = 0, []
    changed = 0
    for key in set(od) & set(nd):
        moved = sorted(f for f in fields if od[key].get(f) != nd[key].get(f))
        if not moved:
            continue
        changed += 1
        per_field.update(moved)
        groups = tuple(g for g, names in (("own-day", OWN_DAY), ("rolling", ROLLING), ("coverage", COVERAGE))
                       if any(f in names for f in moved))
        shape[groups] += 1
        if "own-day" in groups:
            own_moved += 1
            if key not in touched:
                own_moved_untouched.append((key, [f for f in moved if f in OWN_DAY]))
    print("DAILY: rows in both %d, changed %d" % (len(set(od) & set(nd)), changed))
    print("  BY GROUP OF FIELDS MOVED: %s" % {" + ".join(k): v for k, v in shape.most_common()})
    print("  ROWS PER FIELD: %s" % dict(per_field.most_common()))
    print("  OWN-DAY COUNT FIELD MOVED: %d rows" % own_moved)
    print("THE STOP TEST: own-day count moved on a (security, day) with NO pair added, gone or re-counted: %d" % len(own_moved_untouched))
    for key, moved in sorted(own_moved_untouched)[:15]:
        print("    %s %s" % (key, moved))

    gsk = sorted((nm[k] for k in set(nm) - set(om) if k[1] == "GSK_LN_Equity"), key=lambda r: str(r["published_utc"]))
    print("GSK_LN_Equity: pairs served %d, built %d, added %d" % (
        sum(1 for k in om if k[1] == "GSK_LN_Equity"), sum(1 for k in nm if k[1] == "GSK_LN_Equity"), len(gsk)))
    print("  ADDED BY PUBLISHER: %s" % dict(collections.Counter(r["publisher"] for r in gsk)))
    print("  ADDED BY MATCH FORMS: %s" % dict(collections.Counter(json.dumps(r["match_forms"]) for r in gsk).most_common()))
    print("  ADDED BY FETCH DAY: %s" % dict(sorted(collections.Counter(str(r["fetched_at"])[:10] for r in gsk).items())))
    step = max(1, len(gsk) // 10)
    for row in gsk[::step][:10]:
        print("    %s | %s | forms %s | count %s | title: %s" % (
            row["article_key"], str(row["published_utc"])[:10], json.dumps(row["match_forms"]), row["mention_count"],
            (row.get("title") or "").encode("ascii", "replace").decode("ascii")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
