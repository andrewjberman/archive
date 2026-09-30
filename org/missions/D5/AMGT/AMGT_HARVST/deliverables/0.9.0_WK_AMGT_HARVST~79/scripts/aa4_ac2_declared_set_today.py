"""aa-4 AC2 -- the DERIVED declared set today, over the real persisted run records and
ENABLED_PUBLISHERS, and the in-memory gold branch's POPULATION under it.

Read-only: run records, the universe object and the newest chatter_daily / article_security_mention
snapshots are READ from the pool bucket; write_fn is None, so no DynamoDB item, no S3 object and no
env value is written or changed. Prints DECLARED SET, the removed publishers with reasons, and the
POPULATION line per axis. The window of the run-record read is the gold branch's own window.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 8)))
sys.path.insert(0, ROOT)

from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.harvest import publication_gold as gold  # noqa: E402
from lib.research.metrics import chatter_axis as axis  # noqa: E402


def main():
    daily = pool_reader._gold_latest_snapshot_rows("chatter_daily")
    days = sorted({str(row["day"]) for row in daily})
    as_of = days[-1]
    start, end = axis.window_bounds(as_of)
    records = axis.read_run_records()
    print("RUN_RECORDS read=%d window=%s..%s as_of=%s" % (len(records), start, end, as_of))
    for record in records:
        print("  RECORD %s started_at=%s jobs=%s" % (
            record.get("run_id"), record.get("started_at"),
            [(j.get("publisher"), j.get("status")) for j in record.get("jobs") or []]))
    print("ENABLED_PUBLISHERS %s" % (list(gold.ENABLED_PUBLISHERS),))
    declared, removed = axis.derive_declared_set(records, start_date=start, end_date=end)
    print("DECLARED SET: %s" % (list(declared),))
    if not removed:
        print("REMOVED: none")
    for publisher, reason in sorted(removed.items()):
        print("REMOVED %s: %s" % (publisher, reason))
    print("CHATTER_AXIS_SOURCE_IN_ENV=%r (unchanged; this script sets nothing)"
          % (os.environ.get("CHATTER_AXIS_SOURCE"),))
    summary = axis.compute_chatter_axis(
        as_of_date=as_of, count_fn=axis.gold_daily_mention_scores, write_fn=None,
        run_records_fn=lambda: records)
    print("WRITE_FN=None rows_written=%d pointers_written=%d"
          % (summary["rows_written"], sum(1 for p in summary["products"] if p["pointer_written"])))
    print("GOLD BRANCH declared_publishers=%s removed_publishers=%s"
          % (summary["declared_publishers"], summary["removed_publishers"]))
    for product in summary["products"]:
        print("AXIS %s" % product["axis"])
        print(axis.population_line(product["population"]))
        print("FOOTER %s" % product["footer"])
        if product["state"] == axis.STATE_FAILED:
            print("STATE: HOLD empty_reason=%s" % (product["empty_reason"],))
        else:
            print("STATE: %s empty_reason=%s" % (product["state"], product["empty_reason"]))


if __name__ == "__main__":
    main()
