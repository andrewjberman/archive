"""HVST-at-1 timing control. LOCAL ONLY: a stub S3 client, a temp sqlite outbox, no network.

Drives HarvestUploader._run_listings (via .run) over the SAME 100 planted listing pages (distinct per-page
fetched_at seconds), the OLD per-group path (a copy kept in the test module, control use only) against the
NEW batched path, against a stub client whose listing_hit prefix already holds about 1,000 parts.
Prints: silver prefix reads, wall seconds, rows identical, AC2 RESULT.
PASS: new reads == 1 per source, old > new, rows identical.
"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
sys.path.insert(0, ROOT)

from lib.opal_data_harvest import test_at1_batched_listing_upload as T  # noqa: E402
from lib.opal_data_harvest import uploads  # noqa: E402

PAGES, PARTS = 100, 1000


def main():
    specs = T.sa_specs(PAGES)
    sources = {T.harvest_grammar.SOURCE_FOR_PUBLISHER[s[0]] for s in specs}
    with tempfile.TemporaryDirectory() as tmp:
        stub_o, _db_o, rec_o, calls_o, wall_o = T.run_pass(T.OldUploader, os.path.join(tmp, "old"), specs, preload=PARTS)
        stub_n, _db_n, rec_n, calls_n, wall_n = T.run_pass(uploads.HarvestUploader, os.path.join(tmp, "new"), specs, preload=PARTS)
        rows_o, rows_n = T.silver_rows(stub_o), T.silver_rows(stub_n)
        identical = bool(rows_n) and sorted(rows_o) == sorted(rows_n) and all(rows_o[k][0] == rows_n[k][0] for k in rows_o)
        uploaded = all(r["status"] == "uploaded" for r in rec_o["results"] + rec_n["results"]) \
            and len(rec_o["results"]) == len(rec_n["results"]) == PAGES
        parts_o = len({k for _r, k in rows_o.values()})
        parts_n = len({k for _r, k in rows_n.values()})
    print("pages: %d  preloaded parts: %d  sources: %s" % (PAGES, PARTS, sorted(sources)))
    print("silver prefix reads: old %d new %d" % (len(calls_o), len(calls_n)))
    print("wall seconds: old %.2f new %.2f" % (wall_o, wall_n))
    print("rows identical: %s  (rows %d old, %d new; new parquet objects %d vs old %d)"
          % (identical, len(rows_o), len(rows_n), parts_n, parts_o))
    ok = len(calls_n) == len(sources) and len(calls_o) > len(calls_n) and identical and uploaded
    print("AC2 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
