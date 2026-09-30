"""HVST-ab-2 AC1 (issuer check, read-only): exactly one new mention part, and its rows are the signed expected rows.

PASS requires, against the act-start BEFORE (`~82/ab2_before.json`): every pre-existing article_security_mention part
unchanged and none removed; exactly ONE new part; its rows, as (article_key|security_key) -> canonical row, equal the
signed expected rows exactly; its byte size equals the signed serializing dry run's (the aa-3 STOP).
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ab2_common as c  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import store  # noqa: E402


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "ab2_before.json"))
    after = c.list_parts()
    pb = before["parts"]
    moved = [k for k in pb if k in after and after[k] != pb[k]]
    removed = [k for k in pb if k not in after]
    new = sorted(k for k in after if k not in pb)
    print("mention parts: before %d, after %d; moved %d, removed %d, new %d" % (len(pb), len(after), len(moved), len(removed), len(new)))
    if moved or removed:
        failures.append("pre-existing parts moved %d / removed %d" % (len(moved), len(removed)))
    if len(new) != 1:
        failures.append("expected exactly 1 new part, found %d" % len(new))
    for k in new:
        size = after[k][1]
        print("  new part %s, %d bytes (signed dry run %d)" % (k, size, before["expected_bytes"]))
        if size != before["expected_bytes"]:
            failures.append("STOP: put bytes %d != signed dry-run bytes %d" % (size, before["expected_bytes"]))
        raw = store._default_client().get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read()
        got = c.norm_rows(pq.read_table(io.BytesIO(raw)).to_pylist())
        want = before["expected_rows"]
        extra = sorted(set(got) - set(want))
        missing = sorted(set(want) - set(got))
        differ = sorted(x for x in got if x in want and got[x] != want[x])
        print("  rows written %d, expected %d; outside the pair %d, missing %d, differing %d"
              % (len(got), len(want), len(extra), len(missing), len(differ)))
        if extra or missing or differ:
            failures.append("written rows != signed expected (outside %d, missing %d, differing %d; first: %s)"
                            % (len(extra), len(missing), len(differ), (extra + missing + differ)[:1]))
    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
