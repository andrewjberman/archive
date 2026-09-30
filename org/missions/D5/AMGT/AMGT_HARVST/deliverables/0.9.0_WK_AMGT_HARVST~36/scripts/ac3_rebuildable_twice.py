"""HVST-a-3 AC3 -- C-HV-GOLD-REBUILDABLE under the new rule: two in-memory builds over the same landed
input serialise (exactly as write_gold does) to byte-identical parquet. READ-ONLY (S3 GET only).
Also printed, informational: a third build over the input in REVERSED row order.
"""
import hashlib
import io
import os
import subprocess
import sys

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import lib.research.harvest.publication_gold as g  # noqa: E402


def landed_input():
    mention = g._latest_gold_snapshot_rows(g.GOLD_TABLE)
    headlines = g._headline_by_article_key()
    out = []
    for row in mention:
        row = dict(row)
        row["title"] = headlines.get(row.get("article_key"))
        out.append(row)
    return out


def serialise(rows):
    table = pa.Table.from_pylist(list(rows), schema=g.GOLD_EVENT_SCHEMA)
    buf = io.BytesIO()
    pq.write_table(table, buf)
    return buf.getvalue(), len(rows)


b1, n1 = serialise(g.event_rows(landed_input()))
b2, n2 = serialise(g.event_rows(landed_input()))
b3, n3 = serialise(g.event_rows(list(reversed(landed_input()))))
h1, h2, h3 = (hashlib.sha256(b).hexdigest() for b in (b1, b2, b3))
print("build 1: rows=%d bytes=%d sha256=%s" % (n1, len(b1), h1))
print("build 2: rows=%d bytes=%d sha256=%s" % (n2, len(b2), h2))
print("build 3 (input reversed, informational): rows=%d bytes=%d sha256=%s" % (n3, len(b3), h3))
ok = b1 == b2 and n1 == n2 == 8
print("AC3 %s (two builds byte-identical: %s; reversed-input identical: %s)" % ("PASS" if ok else "FAIL", b1 == b2, b1 == b3))
sys.exit(0 if ok else 1)
