"""HVST-s-1 AC4 -- daily_rows PURE and IN MEMORY. NO GOLD WRITE: write_gold is never called."""

import collections
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import snapshot_lib  # noqa: E402
import lib.research.harvest.publication_gold as pg  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
SECURITIES = pathlib.Path("org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~4/securities.json")


def distribution(rows):
    counter = collections.Counter(r["data_status"] for r in rows)
    return counter


def main():
    securities = json.loads(SECURITIES.read_text(encoding="utf-8"))
    before_counts, before_rows = snapshot_lib.load(HERE / "before.pickle")
    after_counts, after_rows = snapshot_lib.load(HERE / "after.pickle")

    end = datetime.datetime.now(datetime.timezone.utc).date()
    mentions = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    print("AC4 -- daily_rows PURE, IN MEMORY, NO GOLD WRITE (pg.write_gold is not called by this script)")
    print("  mention rows read from the NEWEST %s gold snapshot: %d" % (pg.GOLD_TABLE, len(mentions)))
    print("  securities: %d ; window: %s -> %s inclusive (%d days) ; ENABLED_PUBLISHERS: %s (n=%d)"
          % (len(securities), pg.BACKFILL_FLOOR, end, (end - pg.BACKFILL_FLOOR).days + 1,
             list(pg.ENABLED_PUBLISHERS), len(pg.ENABLED_PUBLISHERS)))
    print("  BEFORE listing_hit rows: %d ; AFTER listing_hit rows: %d"
          % (len(before_rows), len(after_rows)))

    cov_before = pg.publisher_coverage(before_rows, securities)
    cov_after = pg.publisher_coverage(after_rows, securities)

    rows_before = pg.daily_rows(mentions, securities, start=pg.BACKFILL_FLOOR, end=end, coverage=cov_before)
    rows_after = pg.daily_rows(mentions, securities, start=pg.BACKFILL_FLOOR, end=end, coverage=cov_after)

    dist_before = distribution(rows_before)
    dist_after = distribution(rows_after)
    denominator = len(rows_before)
    print("  data_status distribution BEFORE (denominator %d (security, day) rows): %s"
          % (denominator, dict(sorted(dist_before.items()))))
    print("  data_status distribution AFTER  (denominator %d (security, day) rows): %s"
          % (len(rows_after), dict(sorted(dist_after.items()))))

    index_before = {(r["security_key"], r["day"]): r for r in rows_before}
    moved = []
    for row in rows_after:
        prior = index_before.get((row["security_key"], row["day"]))
        if prior is None:
            continue
        if prior["data_status"] == "DENIED" and row["data_status"] == "PARTIAL":
            moved.append(row)
    print("  (security, day) rows that moved DENIED -> PARTIAL: %d of %d" % (len(moved), denominator))

    complete_in_moved = sum(1 for r in moved if r["data_status"] == "COMPLETE")
    print("  the string COMPLETE among moved rows: %d occurrence(s)" % complete_in_moved)
    if complete_in_moved:
        print("  BLOCKING: COMPLETE appeared on a moved row -- stopping per the task order")
        return 1

    if moved:
        sample = moved[0]
        print("  SAMPLE MOVED ROW: security_key=%s day=%s publishers_covered=%d publishers_enabled=%d "
              "data_status=%s" % (sample["security_key"], sample["day"], sample["publishers_covered"],
                                  sample["publishers_enabled"], sample["data_status"]))
    else:
        print("  NO MOVED ROW TO SAMPLE -- zero rows moved, so there is no publishers_covered / "
              "publishers_enabled to print from a moved row. Cause named in AMGT_HARVST-Z-W20-S1: "
              "AC1a was not run and AC2's sa delta is +0, so the AFTER coverage equals the BEFORE coverage.")
        print("  COVERAGE EQUALITY CHECK (the reason there is no movement): cov_before == cov_after -> %s"
              % (cov_before == cov_after))
        nonzero = [(k, {p: (str(s[0]), str(s[1])) for p, s in v.items()}) for k, v in sorted(cov_after.items()) if v]
        print("  AFTER coverage, non-empty entries only: %s" % (nonzero or "none"))
        highest = [r for r in rows_after if r["data_status"] == "PARTIAL"]
        if highest:
            s = highest[0]
            print("  HIGHEST GRADE PRESENT ANYWHERE AFTER (not a moved row): security_key=%s day=%s "
                  "publishers_covered=%d publishers_enabled=%d data_status=%s"
                  % (s["security_key"], s["day"], s["publishers_covered"], s["publishers_enabled"],
                     s["data_status"]))
    print("  COMPLETE anywhere in the AFTER rows: %d of %d" % (dist_after.get("COMPLETE", 0), len(rows_after)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
