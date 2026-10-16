"""HVST-cb-10 read: the S3 GETs of ONE `harvest_grammar.watermark` call per publisher, with no browser and no vendor.

The watermark is the S3 read every backfill job makes at its start (`backfill_bound`). This calls it alone, in this
process, for one security and each publisher given, and prints the process counters after each call. Read-only: the
function only lists and GETs silver parts. Run it while the production runner is live: it opens no browser profile.

Usage: python cb10_watermark_probe.py <security_key> <publisher> [<publisher> ...]
Prints one line per publisher: WATERMARK publisher=.. get_count=.. get_bytes=.. mib=..
"""

import sys

sys.path.insert(0, r"C:\dev\ajb_workspace")
from lib.opal_data_harvest import harvest_grammar  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    security_key, publishers = sys.argv[1], sys.argv[2:]
    for publisher in publishers:
        store.get_stats_reset()
        harvest_grammar.watermark(security_key, publisher)
        snap = store.get_stats_snapshot()
        print("WATERMARK publisher=%s get_count=%d get_bytes=%d mib=%.1f" % (
            publisher, snap["get_count"], snap["get_bytes"], snap["get_bytes"] / 1048576.0))


if __name__ == "__main__":
    main()
