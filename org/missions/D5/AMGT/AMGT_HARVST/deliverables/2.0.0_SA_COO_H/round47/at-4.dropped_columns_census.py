"""Round 47 row Z-W95-S2: did `store.silver_append` drop columns from served silver article rows? READ-ONLY.

`pa.Table.from_pylist(rows)` takes its columns from the FIRST row, so a later row's extra keys are silently dropped (measured:
pyarrow 24.0.0, [{'a':1},{'a':2,'b':3}] -> ['a'], and row 2 loses b). For every silver article part of barrons, bbg, ft, sa and
wsj whose object LastModified is at or after SINCE, every row is rebuilt from its own stored original by this checkout's
`silver_from_bronze.article_rows`, with the row's own arguments (fetched_at, retrieval_mode, run_stamp, discovery fields), and
its non-null keys are compared. A key that the rebuilt row carries non-null and the written row lacks (or holds null) is DROPPED.

Prints per publisher: parts read, rows checked, rows with a dropped key, distinct dropped keys (top 10), and build errors.
Writes `round47/at-4.dropped_columns_census.json`.
"""

import collections
import datetime
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 8)))
sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.opal_data_harvest import silver_from_bronze as sfb  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SINCE = datetime.datetime(2026, 10, 4, 23, 0, tzinfo=datetime.timezone.utc)
DISCOVERY = ("first_discovered_at", "retrieval_rung", "search_query", "search_rank", "search_page", "discovered_for")
OUT = os.path.join(HERE, "at-4.dropped_columns_census.json")


def main():
    c = store._default_client()
    result = {"since": SINCE.isoformat(), "measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "publishers": {}}
    for pub in ("barrons", "bbg", "ft", "sa", "wsj"):
        src = hg.SOURCE_FOR_PUBLISHER[pub]
        parts = []
        for page in c.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=store.table_prefix(src, "silver", "article")):
            parts += [o for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet") and o["LastModified"] >= SINCE]
        rows_checked, rows_dropped, errors = 0, 0, []
        dropped = collections.Counter()
        per_part = {}
        for o in parts:
            table = pq.read_table(io.BytesIO(c.get_object(Bucket=store.HARVEST_BUCKET, Key=o["Key"])["Body"].read()))
            n_drop = 0
            for row in table.to_pylist():
                rows_checked += 1
                bk = row.get("bronze_key")
                try:
                    obj = c.get_object(Bucket=store.HARVEST_BUCKET, Key=bk)
                    body, form = obj["Body"].read(), store.classify_bronze_form(obj.get("Metadata"))
                    received = "normalised_record" if form == store.FORM_NORMALISED else "as_received"
                    rebuilt = sfb.article_rows(pub, body, received, bk, row["fetched_at"], row.get("retrieval_mode") or "backfill",
                                               row.get("run_stamp"), discovery={f: row.get(f) for f in DISCOVERY})
                except Exception as exc:  # noqa: BLE001 -- reported, never hidden
                    errors.append([bk, "%s: %s" % (type(exc).__name__, str(exc)[:120])])
                    continue
                lost = [k for k, v in rebuilt.items() if v is not None and row.get(k) is None and k != "record_hash"]
                if lost:
                    rows_dropped += 1
                    n_drop += 1
                    dropped.update(lost)
            per_part[o["Key"]] = {"rows": table.num_rows, "rows_with_dropped": n_drop,
                                  "last_modified": o["LastModified"].isoformat()}
        result["publishers"][pub] = {"parts": len(parts), "rows_checked": rows_checked, "rows_with_dropped_key": rows_dropped,
                                     "dropped_keys": dict(dropped.most_common(25)), "errors": errors[:20],
                                     "parts_detail": per_part}
        print("%-8s parts %4d; rows %5d; rows with a dropped key %5d; errors %d; top dropped %s" % (
            pub, len(parts), rows_checked, rows_dropped, len(errors), dropped.most_common(10)))
    json.dump(result, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("RECORD: %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
