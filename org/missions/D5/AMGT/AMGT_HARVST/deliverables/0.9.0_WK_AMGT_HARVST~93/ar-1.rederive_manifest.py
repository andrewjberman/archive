"""HVST-ar-1 re-derivation manifest (DRY RUN, READ ONLY: S3 list/get only, no write, no vendor call).

For EVERY stored original (bronze `article` object) of barrons, bbg, ft and wsj, builds the row IN MEMORY with this
checkout's `silver_from_bronze.article_rows` and compares it with the served silver row of the same `bronze_key`
(latest `run_stamp`). The build arguments are the served row's own (`fetched_at`, `retrieval_mode`, `run_stamp` and
the discovery fields); an original with no served row is built from its key's own stamp as a backfill.

Per publisher it reports: originals; originals with a served row; rows that GAIN columns; the columns added (name ->
rows); rows whose PRE-EXISTING columns change (must be 0; every one is listed); originals with no served row; build
errors; and whether the new rows still build and write as parquet per fetch date (silver_append's own table build).

`record_hash` is excluded from the pre-existing comparison and counted on its own line: it is the hash of the row's
vendor fields, so it changes exactly when a column is added, by construction; silver_append recomputes it.

Usage: python ar-1.rederive_manifest.py [--out PATH] [--cache DIR] [--publishers barrons,bbg,ft,wsj]
`--cache DIR` is a local read-through cache of the S3 objects (bronze bodies and silver parts); without it every
object is read from S3.
"""
import argparse
import collections
import datetime
import hashlib
import io
import json
import math
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))

import pyarrow as pa  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.opal_data_harvest import silver_from_bronze as sfb  # noqa: E402
from lib.research.harvest import store  # noqa: E402

PUBLISHERS = ("barrons", "bbg", "ft", "wsj")
DISCOVERY_FIELDS = ("first_discovered_at", "retrieval_rung", "search_query", "search_rank", "search_page", "discovered_for")
DEFAULT_OUT = os.path.join(HERE, "ar-1.rederive_manifest.json")


class Reader:
    def __init__(self, cache):
        self.client = store._default_client()
        self.cache = cache
        if cache:
            os.makedirs(cache, exist_ok=True)

    def _path(self, key):
        return os.path.join(self.cache, hashlib.sha1(key.encode()).hexdigest())

    def list_keys(self, prefix):
        keys = []
        for page in self.client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            keys += [o["Key"] for o in page.get("Contents", []) or [] if not o["Key"].endswith("/")]
        return keys

    def get(self, key):
        """(body bytes, metadata dict)."""
        p = self._path(key) if self.cache else None
        if p and os.path.exists(p + ".body"):
            with open(p + ".body", "rb") as fh:
                body = fh.read()
            with open(p + ".meta", encoding="utf-8") as fh:
                return body, json.load(fh)["meta"]
        obj = self.client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
        body, meta = obj["Body"].read(), obj.get("Metadata")
        if p:
            with open(p + ".body", "wb") as fh:
                fh.write(body)
            with open(p + ".meta", "w", encoding="utf-8") as fh:
                json.dump({"key": key, "meta": meta}, fh)
        return body, meta


def same(a, b):
    """Value equality across the parquet round trip: a struct read back carries None for keys the batch's
    other rows had, so a missing key inside a struct equals None; a null is never equal to a struct; aware datetimes compare as instants; NaN equals NaN."""
    if a is None or b is None:
        return a is None and b is None      # a null and a struct of nulls are different values
    if isinstance(a, dict) or isinstance(b, dict):
        if not isinstance(a, dict) or not isinstance(b, dict):
            return False
        return all(same(a.get(k), b.get(k)) for k in set(a) | set(b))
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    num = (int, float)
    if type(a) is not type(b) and not (isinstance(a, num) and isinstance(b, num)
                                       and not isinstance(a, bool) and not isinstance(b, bool)):
        return False
    return a == b


def _split_by_date(rows):
    out = collections.defaultdict(list)
    for r in rows:
        out[r["fetched_at"].date()].append(r)
    return list(out.values())


def build_args(key, served):
    stem = key.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    if served is not None:
        discovery = {f: served.get(f) for f in DISCOVERY_FIELDS}
        return served["fetched_at"], served.get("retrieval_mode") or "backfill", served.get("run_stamp") or stem, discovery
    stamp = datetime.datetime.strptime(stem[:15], "%Y%m%dT%H%M%S").replace(tzinfo=datetime.timezone.utc)
    return stamp, "backfill", stem, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--cache", default=None)
    ap.add_argument("--publishers", default=",".join(PUBLISHERS))
    args = ap.parse_args()
    rd = Reader(args.cache)
    result = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "publishers": {}}
    for pub in args.publishers.split(","):
        src = hg.SOURCE_FOR_PUBLISHER[pub]
        bronze_keys = sorted(rd.list_keys(store.table_prefix(src, "bronze", "article")))
        served, held_part = {}, {}
        silver_parts = [k for k in rd.list_keys(store.table_prefix(src, "silver", "article")) if k.endswith(".parquet")]
        served_rows_total = 0
        multi = 0
        for sk in silver_parts:
            raw, _m = rd.get(sk)
            for row in pq.read_table(io.BytesIO(raw)).to_pylist():
                served_rows_total += 1
                bk = row.get("bronze_key")
                held = served.get(bk)
                if held is None:
                    served[bk], held_part[bk] = row, sk
                else:
                    multi += 1
                    # latest run_stamp; a run_stamp tie goes to the later part (store.part_order_key, the rule every
                    # silver reader shares): a re-derived part (`rt-...-rN.parquet`) carries its row's ORIGINAL run_stamp
                    if (str(row.get("run_stamp")), store.part_order_key(sk)) > (
                            str(held.get("run_stamp")), store.part_order_key(held_part[bk])):
                        served[bk], held_part[bk] = row, sk
        cols_added = collections.Counter()
        gain_rows = 0
        changed = []
        record_hash_rows = 0
        no_served, errors = [], []
        new_rows = []
        for bk in bronze_keys:
            body, meta = rd.get(bk)
            form = store.classify_bronze_form(meta)
            srow = served.get(bk)
            if srow is None:
                no_served.append(bk)
            fetched_at, mode, stamp, discovery = build_args(bk, srow)
            try:
                new = sfb.article_rows(pub, body, "normalised_record" if form == store.FORM_NORMALISED else "as_received",
                                       bk, fetched_at, mode, stamp, discovery=discovery)
            except Exception as exc:  # noqa: BLE001 -- reported, never hidden
                errors.append([bk, "%s: %s" % (type(exc).__name__, str(exc)[:160])])
                continue
            new_rows.append(new)
            if srow is None:
                continue
            diff = [c for c in srow if c != "record_hash" and not same(srow.get(c), new.get(c))]
            lost_or_changed = [c for c in diff if srow.get(c) is not None]
            gained = [c for c in diff if srow.get(c) is None]
            gained += [c for c in new if c not in srow and new[c] is not None and c not in gained]
            if lost_or_changed:
                changed.append({"bronze_key": bk, "columns": sorted(lost_or_changed)})
            if gained:
                gain_rows += 1
                cols_added.update(set(gained))
            if "record_hash" in srow:
                record_hash_rows += 1  # every re-derived row is re-hashed by silver_append
        # silver_append builds one parquet table per fetch date from the rows of ONE append. Rebuild that for the new
        # rows: each served part's rows together (the batch composition that part was written with), and every row
        # alone; an original with no served row is checked alone and against the rows of its fetch date's served parts.
        table_errors = []
        by_part = collections.defaultdict(list)
        for row in new_rows:
            srow = served.get(row["bronze_key"])
            by_part[held_part.get(row["bronze_key"]) if srow is not None else None].append(row)
        groups = [(k, v) for k, v in sorted(by_part.items(), key=lambda kv: str(kv[0])) if k is not None]
        groups += [("alone:" + r["bronze_key"], [r]) for r in by_part.get(None, [])]
        for name, rows in groups:
            for d_rows in _split_by_date(rows):
                try:
                    pq.write_table(pa.Table.from_pylist(d_rows), io.BytesIO())
                except Exception as exc:  # noqa: BLE001
                    table_errors.append([name, len(d_rows), "%s: %s" % (type(exc).__name__, str(exc)[:300])])
        for row in new_rows:
            try:
                pq.write_table(pa.Table.from_pylist([row]), io.BytesIO())
            except Exception as exc:  # noqa: BLE001
                table_errors.append(["row:" + row["bronze_key"], 1, "%s: %s" % (type(exc).__name__, str(exc)[:300])])
        by_date = groups
        # cross-row conflict risk: a path of a NEW column that holds two kinds of value across the rows (one parquet table
        # cannot hold both, so two such rows in one append conflict)
        kinds = {}
        for row in new_rows:
            for c in cols_added:
                if c in row:
                    sfb._collect_kinds(row[c], c, kinds)
        polymorphic = {p: sorted(ks) for p, ks in sorted(kinds.items()) if len(ks) > 1}
        result["publishers"][pub] = {
            "originals": len(bronze_keys), "served_silver_rows_read": served_rows_total, "served_keys": len(served),
            "served_keys_with_more_than_one_row": multi,
            "rows_that_gain_columns": gain_rows, "columns_added": dict(sorted(cols_added.items())),
            "rows_whose_preexisting_columns_change": len(changed), "changed_rows": changed,
            "record_hash_rewritten_rows": record_hash_rows,
            "originals_with_no_served_row": no_served, "build_errors": errors,
            "new_rows_built": len(new_rows), "batch_tables_checked": len(by_date), "table_build_errors": table_errors,
            "new_column_paths_with_two_kinds_across_rows": polymorphic,
        }
        r = result["publishers"][pub]
        print("=== %s: originals %d; served keys %d (silver rows read %d, keys with >1 row %d)" % (
            pub, r["originals"], r["served_keys"], served_rows_total, multi))
        print("  rows that gain columns: %d; columns added (%d): %s" % (gain_rows, len(cols_added), dict(sorted(cols_added.items()))))
        print("  rows whose PRE-EXISTING columns change: %d %s" % (len(changed), changed[:5]))
        print("  originals with no served row: %d %s" % (len(no_served), no_served[:5]))
        print("  build errors: %d %s" % (len(errors), errors[:5]))
        print("  new-column paths holding two kinds across rows: %d %s" % (len(polymorphic), polymorphic))
        print("  parquet table build over %d served-part batches (plus every row alone): %d errors %s" % (len(by_date), len(table_errors), table_errors[:3]))
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, default=str)
    print("RECORD:", args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
