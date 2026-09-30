"""HVST-p-1 AC2 (issuer check, read-only): the SERVED snapshot now carries a mention count on every pair, including
the pairs the rebuild added (ANDREW-DIRECT @8135566a29: a mention count per article).

PASS requires: the newest served snapshot (read the way the timeline route reads it) equals the signed expected rows;
`mention_count` is a non-null integer >= 1 on every served row; every signed NEW pair is served with its count; and the
Lenovo pair count equals the signed figure. Prints the mention_count distribution and the NEW pairs by publisher.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_common as c  # noqa: E402


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "p1_before.json"))
    served = c.served_rows()
    got = c.norm_rows(served)
    if got != before["expected_rows"]:
        failures.append("served snapshot != signed expected rows (%d vs %d)" % (len(got), len(before["expected_rows"])))
    bad = [r for r in served if not isinstance(r.get("mention_count"), int) or r.get("mention_count") < 1]
    print("served rows: %d; mention_count missing or < 1: %d" % (len(served), len(bad)))
    if bad:
        failures.append("%d served row(s) lack a mention_count >= 1" % len(bad))
    print("mention_count distribution: %s" % sorted(collections.Counter(r.get("mention_count") for r in served).items()))
    new = before["diff"]["new"]
    missing = [k for k in new if k not in got]
    print("NEW pairs served: %d of %d; by publisher %s" % (len(new) - len(missing), len(new), before["new_by_publisher"]))
    if missing:
        failures.append("%d signed NEW pair(s) not served" % len(missing))
    lenovo = sum(1 for r in served if r.get("security_key") == "992_HK_Equity")
    print("Lenovo pairs served: %d (signed %d)" % (lenovo, before["lenovo_rows"]))
    if lenovo != before["lenovo_rows"]:
        failures.append("Lenovo pairs %d != signed %d" % (lenovo, before["lenovo_rows"]))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
