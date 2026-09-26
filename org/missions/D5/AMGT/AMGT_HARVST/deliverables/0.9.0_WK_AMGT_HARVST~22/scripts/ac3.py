"""AC3 -- publisher_coverage + daily_rows, PURE and IN MEMORY, over the post-run listing_hit rows.

NO GOLD WRITE: `write_gold` is never imported or called here. The only S3 traffic is READS (the
silver listing_hit rows and the newest `article_security_mention` gold snapshot, the same two
inputs `build_daily` reads).

BEFORE vs AFTER is not a second S3 read at two times: AC1 recorded the PRE-CELL listing_hit record
keys to `ac1_before_after.json`, so BEFORE is that subset of today's rows and AFTER is all of them.
Both arms therefore run on ONE instrument and ONE read.

TWO POPULATIONS, both with printed denominators:
  A. the gold builder's own `securities.json` (0.9.0_WK_AMGT_HARVST~4) -- the 6 names `build_daily`
     is actually invoked with, each carrying a real `security_key`.
  B. the producer's `--all-securities` universe (the population AC2 captured from). Those rows
     carry `key`, NOT `security_key`, so `security_key` is DERIVED here as `key` for this
     in-memory measurement only -- nothing is written and no gold row is minted from it.
"""
import datetime
import json
import os
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(
    os.getcwd(), "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~22", "scripts"))

from _census import client, listing_hit_rows, row_key
from lib.opal_data_harvest.__main__ import universe
from lib.research.harvest.publication_gold import (BACKFILL_FLOOR, ENABLED_PUBLISHERS,
                                                   GOLD_TABLE, _latest_gold_snapshot_rows,
                                                   daily_rows, publisher_coverage)

OUT_DIR = os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                       "0.9.0_WK_AMGT_HARVST~22")
AS_OF = datetime.datetime.now(datetime.timezone.utc).date()

with open(os.path.join(OUT_DIR, "ac1_before_after.json"), encoding="utf-8") as fh:
    ac1 = json.load(fh)
before_keys = set(ac1["before"]["row_keys"])

c = client()
all_rows = listing_hit_rows(c)
before_rows = [r for r in all_rows if row_key(r) in before_keys]
after_rows = all_rows
mention = _latest_gold_snapshot_rows(GOLD_TABLE, client=c)

print("AC3 -- publisher_coverage + daily_rows, PURE, no gold write")
print("as_of (end): %s   start (BACKFILL_FLOOR): %s   days: %d"
      % (AS_OF, BACKFILL_FLOOR, (AS_OF - BACKFILL_FLOOR).days + 1))
print("ENABLED_PUBLISHERS: %d (%s) -- NOT narrowed" % (len(ENABLED_PUBLISHERS), ", ".join(ENABLED_PUBLISHERS)))
print("listing_hit rows read from silver: %d total; BEFORE arm (pre-cell keys) %d; AFTER arm %d"
      % (len(all_rows), len(before_rows), len(after_rows)))
print("newest %s gold snapshot rows read (mention input): %d" % (GOLD_TABLE, len(mention)))
print("")

with open(os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                       "0.9.0_WK_AMGT_HARVST~4", "securities.json"), encoding="utf-8") as fh:
    pop_a = json.load(fh)

config = json.loads(open(os.path.join("lib", "opal_data_harvest", "config.json"),
                         encoding="utf-8").read())
pop_b = [dict(s, security_key=s["key"]) for s in universe(config)]

summary = {}

for label, securities in (("A: gold builder securities.json", pop_a),
                          ("B: --all-securities universe (security_key DERIVED from key)", pop_b)):
    print("=" * 78)
    print("POPULATION %s -- denominator tested: %d securities" % (label, len(securities)))
    cov_before = publisher_coverage(before_rows, securities)
    cov_after = publisher_coverage(after_rows, securities)

    sa_spans = {k: v.get("sa") for k, v in cov_after.items() if v.get("sa") is not None}
    print("securities for which sa NOW yields a NON-EMPTY span: %d of %d"
          % (len(sa_spans), len(securities)))
    for key in sorted(sa_spans):
        span = sa_spans[key]
        print("    %-26s sa span (start, end) = (%s, %s)" % (key, span[0].isoformat(), span[1].isoformat()))
    if not sa_spans:
        print("    (none -- reported as the measured outcome, not explained away)")
    sa_before = {k: v.get("sa") for k, v in cov_before.items() if v.get("sa") is not None}
    print("  same measure on the BEFORE arm: %d of %d" % (len(sa_before), len(securities)))

    rows_before = daily_rows(mention, securities, start=BACKFILL_FLOOR, end=AS_OF, coverage=cov_before)
    rows_after = daily_rows(mention, securities, start=BACKFILL_FLOOR, end=AS_OF, coverage=cov_after)

    def dist(rows):
        d = {}
        for r in rows:
            d[r["data_status"]] = d.get(r["data_status"], 0) + 1
        return d

    db, da = dist(rows_before), dist(rows_after)
    print("  data_status distribution BEFORE (denominator %d rows): %r" % (len(rows_before), db))
    print("  data_status distribution AFTER  (denominator %d rows): %r" % (len(rows_after), da))

    idx_before = {(r["security_key"], r["day"]): r for r in rows_before}
    moved = []
    for r in rows_after:
        prior = idx_before[(r["security_key"], r["day"])]
        if prior["data_status"] != r["data_status"]:
            moved.append((prior, r))
    denied_to_partial = [(p, a) for p, a in moved
                         if p["data_status"] == "DENIED" and a["data_status"] == "PARTIAL"]
    print("  (security, day) rows that MOVED at all: %d of %d" % (len(moved), len(rows_after)))
    print("  (security, day) rows that moved DENIED -> PARTIAL: %d of %d"
          % (len(denied_to_partial), len(rows_after)))
    other = [(p["data_status"], a["data_status"]) for p, a in moved
             if not (p["data_status"] == "DENIED" and a["data_status"] == "PARTIAL")]
    print("  any OTHER transition observed: %r" % (sorted(set(other)),))

    complete_hits = sum(1 for _p, a in moved if "COMPLETE" in json.dumps(a, default=str))
    print("  occurrences of the string COMPLETE in any MOVED row: %d (must be 0)" % complete_hits)

    if denied_to_partial:
        sample = denied_to_partial[0][1]
        print("  SAMPLE moved row: security_key=%s day=%s data_status=%s "
              "publishers_covered=%d publishers_enabled=%d"
              % (sample["security_key"], sample["day"], sample["data_status"],
                 sample["publishers_covered"], sample["publishers_enabled"]))
        last = denied_to_partial[-1][1]
        print("  LAST  moved row: security_key=%s day=%s data_status=%s "
              "publishers_covered=%d publishers_enabled=%d"
              % (last["security_key"], last["day"], last["data_status"],
                 last["publishers_covered"], last["publishers_enabled"]))
    else:
        print("  SAMPLE moved row: NONE -- zero rows moved; this is the measured outcome")

    summary[label] = {
        "denominator_securities": len(securities),
        "sa_non_empty_spans_after": len(sa_spans),
        "sa_non_empty_spans_before": len(sa_before),
        "sa_spans": {k: [v[0].isoformat(), v[1].isoformat()] for k, v in sa_spans.items()},
        "daily_rows_denominator": len(rows_after),
        "data_status_before": db,
        "data_status_after": da,
        "moved_rows": len(moved),
        "denied_to_partial": len(denied_to_partial),
        "other_transitions": sorted(set(other)),
        "complete_in_moved_rows": complete_hits,
        "sample_moved_row": ({"security_key": denied_to_partial[0][1]["security_key"],
                              "day": denied_to_partial[0][1]["day"].isoformat(),
                              "data_status": denied_to_partial[0][1]["data_status"],
                              "publishers_covered": denied_to_partial[0][1]["publishers_covered"],
                              "publishers_enabled": denied_to_partial[0][1]["publishers_enabled"]}
                             if denied_to_partial else None),
    }
    print("")

print("=" * 78)
print("GOLD WRITE PERFORMED: none (write_gold never imported; only silver + gold READS)")
path = os.path.join(OUT_DIR, "ac3_summary.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"as_of": AS_OF.isoformat(), "backfill_floor": BACKFILL_FLOOR.isoformat(),
               "enabled_publishers": list(ENABLED_PUBLISHERS), "populations": summary},
              fh, indent=2, sort_keys=True)
print("wrote %s" % path)
