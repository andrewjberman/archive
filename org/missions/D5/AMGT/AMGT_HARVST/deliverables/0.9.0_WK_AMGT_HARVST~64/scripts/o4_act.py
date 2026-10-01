"""HVST-o-4 act (run ONCE): rebuild the served sa silver article table under the signed never-widen pair.

One writer: lib.research.harvest.store.silver_append. No bronze write, no gold build, no vendor call.
"""
import collections
import datetime
import os
import sys

CHECKS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "2.0.0_SA_COO_H", "round25", "checks",
)
sys.path.insert(0, os.path.normpath(CHECKS))
import o4_common  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    cl = o4_common.client()
    latest, _hashes = o4_common.latest_hashes(cl)
    keyed = o4_common.rebuilt_rows(cl)
    rows = [row for _key, row in keyed]
    write = o4_common.expected_write(keyed, latest)
    kinds = collections.Counter(t[0] for t in write)
    print("rebuilt rows: %d" % len(rows))
    print("expected write: %d rows -- %s" % (len(write), dict(kinds)))
    if len(write) != 11 or dict(kinds) != {"MOVED": 5, "NEW": 6}:
        print("STOP: expected write is not 11 (MOVED 5, NEW 6); no write made")
        return 2
    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    print("run_stamp: %s" % run_stamp)
    receipt = store.silver_append("seeking-alpha", "article", rows, ("article_key",), run_stamp, client=cl)
    print("receipt: written_rows=%s skipped_unchanged=%s" % (receipt["written_rows"], receipt["skipped_unchanged"]))
    for p in receipt["parts"]:
        print("part: %s" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
