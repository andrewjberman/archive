"""Shared reads for HVST-aa-3's issuer checks and act (the bbg silver rebuild; the o-4 pattern) (2.0.0_SA_COO~H). Read-only: S3 GET/LIST.

`rebuilt_rows()` is the ONE rebuild of served sa silver from sa bronze. It carries HVST-n-2's lineage rules (a served
object keeps its served row's fetched_at / retrieval_mode / run_stamp / discovery record; an object with no served row
takes fetched_at and run_stamp from its bronze key's stamp and retrieval_mode "backfill"), so only the BUILDER's change
can move a value. `expected_write()` mirrors `store.silver_append`'s own filter (skip a row whose record_hash equals
the latest served row for its record key) without writing.
"""
import io
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.opal_data_harvest import harvest_grammar  # noqa: E402
from lib.opal_data_harvest import silver_from_bronze as sfb  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SOURCE = "bloomberg"
PUB = "bbg"
TABLE = "article"
RECORD_KEY = ("article_key",)
STAMP_RE = re.compile(r"/(\d{8}T\d{6}Z)\.json$")
WK = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~78")
SIGNING = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round28/aa3_signing_expected.json")


def client():
    return store._default_client()


def list_objects(prefix, cl=None):
    cl = cl or client()
    out = {}
    for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            out[obj["Key"]] = [obj["ETag"].strip('"'), obj["Size"]]
    return out


def bronze_prefix():
    return store.table_prefix(SOURCE, "bronze", TABLE)


def silver_prefix():
    return store.table_prefix(SOURCE, "silver", TABLE)


def served_rows(cl=None):
    """Every served sa silver article row, keyed by bronze_key (the last part read wins, as n-2 read it)."""
    cl = cl or client()
    served = {}
    for key in sorted(list_objects(silver_prefix(), cl)):
        if not key.endswith(".parquet"):
            continue
        raw = cl.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
        for r in pq.read_table(io.BytesIO(raw)).to_pylist():
            served[r["bronze_key"]] = r
    return served


def rebuilt_rows(cl=None):
    """[(bronze_key, row)] -- one rebuilt row per sa bronze article object, by the merged builder."""
    cl = cl or client()
    served = served_rows(cl)
    out = []
    for key in sorted(list_objects(bronze_prefix(), cl)):
        resp = cl.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
        body, meta = resp["Body"].read(), dict(resp.get("Metadata", {}))
        form = meta.get("received-form", "unlabelled")
        s = served.get(key)
        if s is not None:
            fetched_at, mode, run_stamp = s["fetched_at"], s["retrieval_mode"], s["run_stamp"]
            discovery = {f: s.get(f) for f in ("first_discovered_at", "retrieval_rung", "search_query",
                                               "search_rank", "search_page", "discovered_for")}
        else:
            m = STAMP_RE.search(key)
            if not m:
                continue
            st = m.group(1)
            fetched_at = harvest_grammar.parse_timestamp(
                "%s-%s-%sT%s:%s:%sZ" % (st[0:4], st[4:6], st[6:8], st[9:11], st[11:13], st[13:15]))
            mode, run_stamp, discovery = "backfill", st, None
        row = sfb.article_rows(PUB, body, form, key, fetched_at, mode, run_stamp, discovery=discovery)
        if row:
            out.append((key, row))
    return out


def expected_write(rebuilt, latest):
    """What silver_append would write: [(kind, article_key, bronze_key, record_hash, fetch_date)]."""
    out = []
    for bronze_key, row in rebuilt:
        rk = tuple(row.get(f) for f in RECORD_KEY)
        h = store.record_hash(row)
        prior = latest.get(rk)
        if prior is not None and prior.get("record_hash") == h:
            continue
        kind = "NEW" if prior is None else "MOVED"
        out.append((kind, rk[0], bronze_key, h, row["fetched_at"].date().isoformat()))
    return sorted(out, key=lambda t: (t[0], t[1], t[2]))


def latest_hashes(cl=None):
    latest = store.silver_latest(SOURCE, TABLE, RECORD_KEY, client=cl or client())
    return latest, {k[0]: v.get("record_hash") for k, v in latest.items()}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)


def dry_append(cl=None):
    """HVST-aa-3 AMENDMENT 2: run the REAL `store.silver_append` over the rebuild against a put-capturing pass-through
    client, so the signing measurement SERIALIZES (attempt 1's dry run mirrored the filter only and missed a parquet
    empty-struct failure). Returns (receipt, captured put keys); raises exactly as the act would."""
    import datetime as _dt
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(here)), "round26", "checks"))
    import p1_common as _p1
    cap = _p1.CapturingClient(cl or client())
    rows = [row for _key, row in rebuilt_rows(cap)]
    receipt = store.silver_append(SOURCE, TABLE, rows, RECORD_KEY, store.stamp(_dt.datetime.now(_dt.timezone.utc)), client=cap)
    return receipt, {k: len(v["body"]) for k, v in cap.puts.items()}
