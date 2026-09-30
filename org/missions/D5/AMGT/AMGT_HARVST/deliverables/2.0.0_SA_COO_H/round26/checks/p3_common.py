"""Shared reads for HVST-p-3(a)'s issuer checks (2.0.0_SA_COO~H): the chatter_daily rebuild. Read-only against S3.

`dry_build()` runs the producer's OWN `publication_gold.build_daily` for the pinned as-of against p-1's pass-through client
that captures the put (round-25 ruling 1). 52,143 rows are too many to sign row by row in git, so the signed expectation is:
the row count, a sha256 over the sorted canonical rows, and the named changes against the served snapshot.
"""
import collections
import datetime
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_common as c  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

AS_OF = datetime.date(2026, 9, 30)
LENOVO = "992_HK_Equity"
WK = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~68")
SIGNING = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round26/p3_signing_expected.json")


def daily_prefix():
    return store.table_prefix("amgt", "gold", pg.GOLD_DAILY_TABLE)


def list_parts(cl=None):
    cl = cl or store._default_client()
    out = {}
    for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=daily_prefix()):
        for obj in page.get("Contents", []) or []:
            out[obj["Key"]] = [obj["ETag"].strip('"'), obj["Size"]]
    return out


def canon(rows):
    """{'security|day': canonical JSON} over every row."""
    return {"%s|%s" % (r["security_key"], r["day"]): json.dumps(r, sort_keys=True, default=str) for r in rows}


def digest(canon_rows):
    h = hashlib.sha256()
    for k in sorted(canon_rows):
        h.update(k.encode("utf-8"))
        h.update(b"\x00")
        h.update(canon_rows[k].encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def dry_build():
    cl = c.CapturingClient(store._default_client())
    summary = pg.build_daily(c.securities(), AS_OF, client=cl)
    if len(cl.puts) != 1:
        raise SystemExit("dry build captured %d puts, expected exactly 1" % len(cl.puts))
    body = next(iter(cl.puts.values()))["body"]
    return summary, pq.read_table(io.BytesIO(body)).to_pylist()


def served():
    return pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)


def changes(new_rows, old_rows):
    N, S = canon(new_rows), canon(old_rows)
    by_n = {"%s|%s" % (r["security_key"], r["day"]): r for r in new_rows}
    by_s = {"%s|%s" % (r["security_key"], r["day"]): r for r in old_rows}
    moved = sorted(k for k in N if k in S and N[k] != S[k])
    status = sorted(k for k in moved if by_s[k].get("data_status") != by_n[k].get("data_status"))
    counts = sorted(k for k in moved if by_s[k].get("articles_total") != by_n[k].get("articles_total"))
    return {
        "rows": len(N), "rows_served": len(S),
        "new_keys": sorted(set(N) - set(S)), "gone_keys": sorted(set(S) - set(N)),
        "moved": len(moved), "moved_securities": sorted({k.split("|")[0] for k in moved}),
        "status_changed": status,
        "status_transitions": dict(collections.Counter("%s->%s" % (by_s[k]["data_status"], by_n[k]["data_status"]) for k in status)),
        "articles_total_changed": counts,
        "lenovo_status": dict(collections.Counter(r["data_status"] for r in new_rows if r["security_key"] == LENOVO)),
    }
