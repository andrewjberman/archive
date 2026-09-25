"""HVST-s-1 AC2 -- the AFTER state on the SAME instrument as AC0, with the per-publisher DELTA."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import snapshot_lib  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent


def main():
    before, _before_rows = snapshot_lib.load(HERE / "before.pickle")
    print("AC2 -- AFTER state, read live from s3://%s AFTER AC1b, same instrument as AC0"
          % snapshot_lib.store.HARVEST_BUCKET)
    after, rows = snapshot_lib.snapshot()
    snapshot_lib.print_counts("AFTER", after)
    snapshot_lib.dump(HERE / "after.pickle", after, rows)
    print("")
    print("DELTA (AFTER minus BEFORE), denominator %d publishers:" % len(snapshot_lib.PUBLISHERS))
    for publisher in snapshot_lib.PUBLISHERS:
        d_silver = after[publisher]["silver_listing_hit_rows"] - before[publisher]["silver_listing_hit_rows"]
        d_bronze = after[publisher]["bronze_news_listing_objects"] - before[publisher]["bronze_news_listing_objects"]
        print("  %-8s silver listing_hit rows %+d (%d -> %d)   bronze news_listing objects %+d (%d -> %d)"
              % (publisher, d_silver, before[publisher]["silver_listing_hit_rows"],
                 after[publisher]["silver_listing_hit_rows"], d_bronze,
                 before[publisher]["bronze_news_listing_objects"],
                 after[publisher]["bronze_news_listing_objects"]))
    sa_silver = after["sa"]["silver_listing_hit_rows"] - before["sa"]["silver_listing_hit_rows"]
    sa_bronze = after["sa"]["bronze_news_listing_objects"] - before["sa"]["bronze_news_listing_objects"]
    print("  sa DELTA STATED: silver listing_hit rows %+d against its AC0 value of %d ; "
          "bronze news_listing objects %+d against its AC0 value of %d"
          % (sa_silver, before["sa"]["silver_listing_hit_rows"], sa_bronze,
             before["sa"]["bronze_news_listing_objects"]))
    print("  A ZERO DELTA IS REPORTED AS A ZERO DELTA. Its cause is named in row AMGT_HARVST-Z-W20-S1: "
          "AC1a was not run (the authorized bounded vendor act is unreachable from this worktree), and "
          "AC1b drained an empty local outbox ({\"results\": [], \"remaining_pending\": 0}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
