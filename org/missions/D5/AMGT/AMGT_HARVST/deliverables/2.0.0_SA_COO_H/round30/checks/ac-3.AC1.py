"""HVST-ac-3 AC1 (issuer check, read-only): exactly one new chatter_daily part, equal to the signed serializing dry run.

PASS requires, against the act-start BEFORE (`~86/ac3_before.json`):
- every pre-existing chatter_daily part is unchanged and none is removed;
- exactly ONE new part;
- its byte size equals the signed dry run's;
- its rows' sha256 over the sorted canonical rows equals the signed digest;
- re-diffed against the snapshot that was served before the act, it moves exactly the signed (row, field) list, with OTHER
  equal to 0.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ac3_common as c  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import store  # noqa: E402


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "ac3_before.json"))
    after = c.list_parts()
    pb = before["parts"]
    moved = [k for k in pb if k in after and after[k] != pb[k]]
    removed = [k for k in pb if k not in after]
    new = sorted(k for k in after if k not in pb)
    print("chatter_daily parts: before %d, after %d; moved %d, removed %d, new %d"
          % (len(pb), len(after), len(moved), len(removed), len(new)))
    if moved or removed:
        failures.append("pre-existing parts moved %d / removed %d" % (len(moved), len(removed)))
    if len(new) != 1:
        failures.append("expected exactly 1 new part, found %d" % len(new))
    for k in new:
        size = after[k][1]
        raw = store._default_client().get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read()
        rows = pq.read_table(io.BytesIO(raw)).to_pylist()
        dig = c.digest(c.canon(rows))
        print("  new part %s: %d rows, %d bytes (signed %d), digest %s (signed %s)"
              % (k, len(rows), size, before["bytes"], dig[:16], before["digest"][:16]))
        if size != before["bytes"]:
            failures.append("STOP: put bytes %d != signed dry-run bytes %d" % (size, before["bytes"]))
        if dig != before["digest"]:
            failures.append("rows digest differs from the signed dry run")
    print("signed moves: %d (expected rows %d, rolling later %d, OTHER %d)"
          % (len(before["moved"]), len(before["in_window"]), len(before["rolling_later"]), len(before["other"])))
    if before["other"]:
        failures.append("the signed diff carries %d move(s) outside the expected rows" % len(before["other"]))
    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
