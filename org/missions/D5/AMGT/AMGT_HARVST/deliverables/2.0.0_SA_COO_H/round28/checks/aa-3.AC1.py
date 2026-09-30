"""HVST-aa-3 AC1 (issuer check, read-only): the served objects moved exactly as the pair names.

PASS requires, against the act-start snapshot (`~78/aa3_before.json`, written by `o-4.signing.py` without --signing):
every pre-existing bbg silver article part unchanged (ETag, size) and none removed; every bbg bronze article object
unchanged and none added; exactly as many NEW silver parts as the expected write's fetch-date groups, each
`part-<stamp>.parquet` with a stamp later than every pre-existing part; and the rows in the new parts, as
(article_key, record_hash), equal the expected write exactly.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aa3_common as c  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import store  # noqa: E402


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "aa3_before.json"))
    cl = c.client()
    parts_after = c.list_objects(c.silver_prefix(), cl)
    bronze_after = c.list_objects(c.bronze_prefix(), cl)
    pb = before["silver_parts"]
    moved = [k for k in pb if k in parts_after and parts_after[k] != pb[k]]
    removed = [k for k in pb if k not in parts_after]
    new_parts = sorted(k for k in parts_after if k not in pb)
    print("bbg silver article parts: before %d, after %d; moved %d, removed %d, new %d"
          % (len(pb), len(parts_after), len(moved), len(removed), len(new_parts)))
    if moved or removed:
        failures.append("pre-existing silver parts moved %d / removed %d" % (len(moved), len(removed)))
    if bronze_after != before["bronze_objects"]:
        failures.append("bbg bronze article objects changed (%d -> %d)" % (len(before["bronze_objects"]), len(bronze_after)))
    print("bbg bronze article objects: before %d, after %d, identical: %s"
          % (len(before["bronze_objects"]), len(bronze_after), bronze_after == before["bronze_objects"]))

    expected = before["expected_write"]
    groups = sorted({t[4] for t in expected})
    if len(new_parts) != len(groups):
        failures.append("new parts %d != expected fetch-date groups %d %s" % (len(new_parts), len(groups), groups))
    newest_before = max((store.part_order_key(k) for k in pb), default=("", 0))
    written = []
    for k in new_parts:
        print("  new part " + k)
        if store.part_order_key(k) <= newest_before:
            failures.append("new part %s does not sort after every pre-existing part" % k)
        raw = cl.get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read()
        for r in pq.read_table(io.BytesIO(raw)).to_pylist():
            written.append((r.get("article_key"), r.get("record_hash")))
    want = sorted((t[1], t[3]) for t in expected)
    got = sorted(written)
    print("rows in new parts: %d; expected write: %d (%s)" % (len(got), len(want),
          {k: sum(1 for t in expected if t[0] == k) for k in ("MOVED", "NEW")}))
    if got != want:
        extra = sorted(set(got) - set(want))
        missing = sorted(set(want) - set(got))
        failures.append("written rows != expected: %d outside the pair, %d missing (first outside: %s; first missing: %s)"
                        % (len(extra), len(missing), extra[:1], missing[:1]))

    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
