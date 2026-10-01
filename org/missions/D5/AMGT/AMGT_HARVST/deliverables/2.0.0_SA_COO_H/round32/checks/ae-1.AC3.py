"""HVST-ae-1 AC3 (issuer, read-only): the served gold carries no quarantined sa article.

Reads the worker's quarantine manifest (`~90/ae1_quarantine.json`: {"written_at", "article_keys": ["sa:<id>", ...],
"rows_checked", ...}) and the NEWEST `article_security_mention` part.
PASS requires: the manifest exists with at least one key; the newest mention part was written after the manifest; and
that part holds 0 rows whose `article_key` is in the manifest.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ae1_common as c  # noqa: E402

import io  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402


def main():
    failures = []
    if not os.path.exists(c.MANIFEST):
        print("MANIFEST: absent (%s)" % c.MANIFEST)
        print("AC3 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no quarantine manifest")
        return 1
    m = json.load(open(c.MANIFEST, encoding="utf-8"))
    quarantined = set(m.get("article_keys") or [])
    print("MANIFEST: %d article keys, written_at %s, rows_checked %s" % (len(quarantined), m.get("written_at"),
                                                                       m.get("rows_checked")))
    if not quarantined:
        failures.append("the manifest lists no article")
    cl = c.client()
    parts = sorted(c.keys(c.MENTION, cl), key=lambda kv: kv[1])
    if not parts:
        failures.append("no gold mention part")
    else:
        newest, written = parts[-1]
        t = pq.read_table(io.BytesIO(cl.get_object(Bucket=c.B, Key=newest)["Body"].read())).to_pylist()
        sa = [r for r in t if r.get("publisher") == "sa"]
        hit = [r for r in sa if r.get("article_key") in quarantined]
        print("NEWEST MENTION PART: %s (written %s): %d rows, %d sa, %d quarantined keys present"
              % (newest, written, len(t), len(sa), len(hit)))
        if str(written) <= str(m.get("written_at")):
            failures.append("the newest mention part predates the manifest (gold not rebuilt)")
        if hit:
            failures.append("%d quarantined sa rows still served in gold" % len(hit))
    print("AC3 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
