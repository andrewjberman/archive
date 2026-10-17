"""HVST-cg-1 dry run of the rewrite (nothing put). For each kept silver research-report row (the newest
row per (security_key, report_id), as cg1_census.py keeps it) this builds dict(row) plus fund_relation,
and hands the rows to lib.research.harvest.store.silver_append with the same source, table and
record-key arguments typed.py passes (typed.py, the silver_append call), a fresh run_stamp, and a
RECORDING client. The recording client delegates list_objects_v2 (paginator), get_object and head_object to
the real client, and RECORDS each put_object (key, byte length) WITHOUT performing it and without
raising. A spy on the real client's put_object counts any call that reaches it; it never performs one.

Run from the worktree root, unbuffered, stdout to the .out:

    python -u org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~161/cg1_rebuild_plan.py > .../cg1_rebuild_plan.out

Budget enforced: 200 requests (list pages + object gets), 300 MiB.
"""
import datetime
import io
import os
import re
import sys
from collections import Counter

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.corpus import fund_relation  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BUDGET_REQUESTS = 200
BUDGET_BYTES = 300 * 1024 * 1024


class BudgetExceeded(RuntimeError):
    pass


class RecordingClient:
    """Delegates list, get and head to the real client; records put_object and never performs it."""

    def __init__(self, real):
        self.real = real
        self.puts = []  # (key, byte length)
        self.lists = 0
        self.gets = 0
        self.bytes = 0

    def _spend(self):
        if self.lists + self.gets + 1 > BUDGET_REQUESTS:
            raise BudgetExceeded("request budget %d exceeded" % BUDGET_REQUESTS)

    def get_paginator(self, name):
        real_pag = self.real.get_paginator(name)
        outer = self

        class _Paginator:
            def paginate(self, **kwargs):
                for page in real_pag.paginate(**kwargs):
                    outer._spend()
                    outer.lists += 1
                    yield page

        return _Paginator()

    def get_object(self, **kwargs):
        self._spend()
        self.gets += 1
        resp = self.real.get_object(**kwargs)
        body = resp["Body"]
        raw = body.read() if hasattr(body, "read") else body
        self.bytes += len(raw)
        if self.bytes > BUDGET_BYTES:
            raise BudgetExceeded("byte budget %d exceeded" % BUDGET_BYTES)
        return {"Body": io.BytesIO(raw)}

    def head_object(self, **kwargs):
        self._spend()
        self.gets += 1
        return self.real.head_object(**kwargs)

    def put_object(self, **kwargs):
        body = kwargs["Body"]
        nrows = pq.read_table(io.BytesIO(body)).num_rows  # the body is parsed, never sent
        self.puts.append((kwargs["Key"], len(body), nrows))
        return {}


def kept_rows(reader_client):
    """The newest row per (security_key, report_id) by the gateway rule, MISFILED excluded (as cg1_census.py)."""
    prefix = store.table_prefix(typed.SOURCE, "silver", typed.TABLE)
    keys = []
    for page in reader_client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        keys.extend(obj["Key"] for obj in (page.get("Contents", []) or []) if obj["Key"].endswith(".parquet"))
    keys.sort()
    newest = {}
    rows_read = 0
    for key in keys:
        resp = reader_client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
        part_rows = pq.read_table(io.BytesIO(resp["Body"].read())).to_pylist()
        rows_read += len(part_rows)
        for row in part_rows:
            ident = (row.get("security_key"), row.get("report_id"))
            prev = newest.get(ident)
            if prev is None or key > prev[0]:
                newest[ident] = (key, row)
    excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
    rows = [dict(newest[ident][1]) for ident in sorted(newest, key=lambda x: (str(x[0]), str(x[1])))
            if ident not in excluded]
    return rows, len(keys), rows_read


def main():
    real = store._default_client()
    spied = []

    def spy_put_object(*args, **kwargs):
        # a spy on the REAL client: counts any call that reaches it, and performs nothing
        spied.append(kwargs.get("Key"))
        return {}

    real.put_object = spy_put_object

    client = RecordingClient(real)
    rows, parts, rows_read = kept_rows(client)
    for row in rows:
        row["fund_relation"] = fund_relation.classify(row.get("fund"), row.get("fund_evidence"))
    relations = Counter(row["fund_relation"] for row in rows)

    print("# DENOMINATOR parts=%d rows_read=%d rows_given=%d relations=%s"
          % (parts, rows_read, len(rows), dict(sorted(relations.items()))))
    print("# METHOD silver_append(%r, %r, rows, %r, run_stamp, client=RecordingClient)"
          % (typed.SOURCE, typed.TABLE, typed.RECORD_KEY_FIELDS))
    print("# METHOD gets counts every S3 request (list pages and object gets); bytes counts object bytes read")

    run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
    try:
        result = store.silver_append(typed.SOURCE, typed.TABLE, rows, typed.RECORD_KEY_FIELDS, run_stamp,
                                     client=client)
    except Exception as exc:  # a refusal is printed verbatim; the step stops here
        print("REFUSAL %s: %s" % (type(exc).__name__, str(exc).replace("\n", " ")))
        print("REBUILD-PLAN refused=1 rows=%d puts_recorded=%d puts_performed=%d"
              % (len(rows), len(client.puts), len(spied)))
        return 1

    for key, nbytes, nrows in client.puts:
        print("WOULD_PUT %s rows=%d bytes=%d" % (key, nrows, nbytes))
    dates = sorted({re.search(r"date=(\d{4}-\d{2}-\d{2})", key).group(1) for key, _n, _r in client.puts
                    if re.search(r"date=(\d{4}-\d{2}-\d{2})", key)})
    written = result["written_rows"]
    print("REBUILD-PLAN rows=%d skipped_unchanged=%d new_parts=%d dates=%d puts_recorded=%d puts_performed=%d "
          "gets=%d bytes=%d"
          % (len(rows), result["skipped_unchanged"], len(client.puts), len(dates), len(client.puts),
             len(spied), client.lists + client.gets, client.bytes))
    print("# written_rows_per_silver_append=%d run_stamp=%s" % (written, run_stamp))
    return 0


if __name__ == "__main__":
    sys.exit(main())
