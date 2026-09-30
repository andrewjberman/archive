"""HVST-p-3(a) AC1 (issuer check, read-only): exactly one new chatter_daily part, and its rows hash to the signed digest.

PASS requires, against the act-start BEFORE (`~68/p3_before.json`): every pre-existing part unchanged and none removed;
exactly ONE new part under date=2026-09-30; its row count equals the signed count; and the sha256 over its sorted canonical
rows equals the signed digest.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_common as p  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import store  # noqa: E402


def main():
    failures = []
    before = p.c.load(os.path.join(p.WK, "p3_before.json"))
    after = p.list_parts()
    pb = before["parts"]
    moved = [k for k in pb if k in after and after[k] != pb[k]]
    removed = [k for k in pb if k not in after]
    new = sorted(k for k in after if k not in pb)
    print("daily parts: before %d, after %d; moved %d, removed %d, new %d" % (len(pb), len(after), len(moved), len(removed), len(new)))
    if moved or removed:
        failures.append("pre-existing parts moved %d / removed %d" % (len(moved), len(removed)))
    if len(new) != 1 or "date=%s/" % before["as_of"] not in new[0]:
        failures.append("expected exactly 1 new part under date=%s, found %s" % (before["as_of"], new))
    for k in new:
        raw = store._default_client().get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read()
        rows = pq.read_table(io.BytesIO(raw)).to_pylist()
        d = p.digest(p.canon(rows))
        print("  new part %s: rows %d (signed %d), digest %s (signed %s)" % (k, len(rows), before["rows"], d[:16], before["digest"][:16]))
        if len(rows) != before["rows"] or d != before["digest"]:
            failures.append("written rows do not match the signed expectation")
    print("AC1 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
