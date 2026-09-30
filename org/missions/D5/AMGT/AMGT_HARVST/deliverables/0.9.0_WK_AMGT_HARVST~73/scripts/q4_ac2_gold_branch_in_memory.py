"""q4 AC2 -- the producer's GOLD branch run IN MEMORY over the served gold.

Read-only: the universe object, the newest chatter_daily snapshot and the newest
article_security_mention snapshot are READ from the pool bucket; write_fn is None, so no
DynamoDB item, no S3 object and no env value is written or changed. Declared set (bbg, wsj).
Prints the POPULATION line, the state (COMPLETE, or HOLD with its empty_reason) and the
ranked rows if any.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 8)))
sys.path.insert(0, ROOT)

from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.metrics import chatter_axis as axis  # noqa: E402

DECLARED = ("bbg", "wsj")


def main():
    daily = pool_reader._gold_latest_snapshot_rows("chatter_daily")
    days = sorted({str(row["day"]) for row in daily})
    as_of = days[-1]
    print("SERVED_GOLD chatter_daily rows=%d names=%d days=%s..%s as_of=%s"
          % (len(daily), len({row["security_key"] for row in daily}), days[0], as_of, as_of))
    print("CHATTER_AXIS_SOURCE_IN_ENV=%r (unchanged; this script sets nothing)"
          % (os.environ.get("CHATTER_AXIS_SOURCE"),))
    summary = axis.compute_chatter_axis(
        as_of_date=as_of, count_fn=axis.gold_daily_mention_scores, write_fn=None,
        declared_publishers=DECLARED)
    print("WRITE_FN=None rows_written=%d pointers_written=%d"
          % (summary["rows_written"], sum(1 for p in summary["products"] if p["pointer_written"])))
    print("WINDOW %s..%s universe=%s" % (summary["window"]["start_date"], summary["window"]["end_date"],
                                        summary["universe"]["source"]))
    print("DECLARED_SET %s not_searched_publishers=%s"
          % (",".join(summary["declared_publishers"]), summary["not_searched_publishers"]))
    for product in summary["products"]:
        print("AXIS %s" % product["axis"])
        print(axis.population_line(product["population"]))
        print("FOOTER %s" % product["footer"])
        if product["state"] == axis.STATE_FAILED:
            print("STATE: HOLD empty_reason=%s" % (product["empty_reason"],))
            print("REASON %s" % product["failure_reason"])
        else:
            print("STATE: %s empty_reason=%s" % (product["state"], product["empty_reason"]))
        ranked = [row for row in summary["rows"] if row["axis"] == product["axis"]]
        for row in ranked:
            print("  RANK %s %s score=%.2f window_total=%s"
                  % (row["rank_sort"], row["ticker"], row["score"], row.get("window_total_count")))
        if not ranked:
            print("  RANKED ROWS: none")
        for name, reason in sorted(product["excluded_names"].items()):
            print("  EXCLUDED %s %s" % (name, reason))


if __name__ == "__main__":
    main()
