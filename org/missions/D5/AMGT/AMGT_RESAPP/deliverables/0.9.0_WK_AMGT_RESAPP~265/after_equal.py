"""AMGT_RESAPP AMGT-az-4 AC2: the chatter route's served body is unchanged by the cold-start cuts.

For days 30, 90 and 365 this prints one line and ends with `EQUAL n of 3`:
  1. the route as it is now (small snapshot read as one object, `ParquetFile.read`, month text without `strftime`,
     reads started together) is served;
  2. the SAME route is served again with the readers it replaced standing in, on the same snapshots (the newest-object
     and newest-key lookups are pinned for the process, so a snapshot that lands mid-run cannot make the two differ):
     both snapshots read whole with `pq.read_table`, and the publisher count done by the per-row loop (verbatim from
     AMGT-ax-3, `_the_row_loop`) over `to_pylist()`;
  3. the two body texts must be byte-equal, and the two snapshots' column tables must be `equals`;
  4. the body captured BEFORE the edit (`before/days<N>.json`, by `capture.py`) is also compared: equal, or, when the
     snapshots it was captured on are no longer the newest (its vintage/as_of differ from now), reported as DRIFT, never
     counted against the cut.
Exit 0 only for EQUAL 3 of 3.
"""
from __future__ import annotations

import io
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def _the_row_loop(rows, covered, months):
    seen = set()
    by_pub = defaultdict(lambda: defaultdict(int))
    for r in rows:
        k = (r.get("article_key"), r.get("security_key"))
        if k in seen:
            continue
        seen.add(k)
        month = str(r.get("published_utc") or "")[:7]
        if month in months and r.get("publisher"):
            by_pub[(r["security_key"], month)][r["publisher"]] += 1
    return {k: dict(v) for k, v in by_pub.items() if k[0] in set(covered)}


def _serve(scoped_amgt, days):
    ev = {"rawPath": "/api/scoped/amgt/lead-panel/timeseries/collected/chatter",
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
          "queryStringParameters": {"days": str(days)}}
    r = scoped_amgt.handler(ev)
    return "%s\n%s" % (r.get("statusCode"), r.get("body") or "")


def main():
    import pyarrow.parquet as pq

    from lib.research.api import monthly_chatter, scoped_amgt
    from lib.research.coverage import pool_reader

    pinned = {}
    sizes = {}
    real_object = pool_reader._gold_newest_object
    real_key = monthly_chatter._newest_snapshot_key

    def pin_object(table, client=None):
        if table not in pinned:
            pinned[table] = real_object(table, client)
            sizes[table] = pool_reader._LISTED_SIZE.get((pinned[table][1], pinned[table][2]))
        found = pinned[table]
        if sizes[table] is not None:  # the handler clears the size memo every invocation; the listing is pinned
            pool_reader._LISTED_SIZE[(found[1], found[2])] = sizes[table]
        return found

    keys = {}

    def pin_key(table):
        if table not in keys:
            keys[table] = real_key(table)
        return keys[table]

    pool_reader._gold_newest_object = pin_object
    monthly_chatter._newest_snapshot_key = pin_key

    new_bodies = {days: _serve(scoped_amgt, days) for days in (30, 90, 365)}

    def whole(table, columns):
        client, bucket, key, _etag = pin_object(table)
        raw = client.get_object(Bucket=bucket, Key=key)["Body"].read()
        present = set(pq.ParquetFile(io.BytesIO(raw)).schema_arrow.names)
        return pq.read_table(io.BytesIO(raw), columns=[c for c in columns if c in present])

    # the snapshots, as the new reader gives them and as the replaced reader gave them
    tables_equal = True
    for table, columns in ((monthly_chatter.DAILY_TABLE, monthly_chatter.DAILY_COLUMNS),
                           (monthly_chatter.MENTION_TABLE, monthly_chatter.MENTION_COLUMNS)):
        pool_reader.clear_caches()
        pin_object(table)
        now = pool_reader._gold_latest_snapshot_arrow(table, columns=columns)
        same = now.equals(whole(table, columns))
        print("snapshot %s: %d rows, new read %s the whole-object read" % (table, now.num_rows, "EQUALS" if same else "DIFFERS FROM"))
        tables_equal = tables_equal and same
    pool_reader.clear_caches()

    new_rows, new_arrow, new_counts = (pool_reader._gold_latest_snapshot_rows, pool_reader._gold_latest_snapshot_arrow,
                                       monthly_chatter._publisher_counts)
    pool_reader._gold_latest_snapshot_rows = lambda table, client=None, columns=None: whole(table, columns or ()).to_pylist()
    pool_reader._gold_latest_snapshot_arrow = lambda table, client=None, columns=None: whole(table, columns or ())
    whole_mentions = whole(monthly_chatter.MENTION_TABLE, monthly_chatter.MENTION_COLUMNS).to_pylist()
    monthly_chatter._publisher_counts = lambda mentions, covered, months: _the_row_loop(whole_mentions, covered, months)
    old_bodies = {days: _serve(scoped_amgt, days) for days in (30, 90, 365)}
    pool_reader._gold_latest_snapshot_rows, pool_reader._gold_latest_snapshot_arrow = new_rows, new_arrow
    monthly_chatter._publisher_counts = new_counts

    equal = 0
    for days in (30, 90, 365):
        same = new_bodies[days] == old_bodies[days] and tables_equal
        recorded_path = os.path.join(HERE, "before", "days%d.json" % days)
        note = "no recorded body"
        if os.path.exists(recorded_path):
            with open(recorded_path, encoding="utf-8", newline="") as fh:
                recorded = fh.read()
            if recorded == new_bodies[days]:
                note = "recorded before-body byte-equal"
            else:
                try:
                    a = json.loads(recorded.split("\n", 1)[1])
                    b = json.loads(new_bodies[days].split("\n", 1)[1])
                    moved = a.get("vintage") != b.get("vintage") or a.get("as_of") != b.get("as_of")
                except ValueError:
                    moved = False
                note = "recorded before-body differs: DRIFT (snapshots landed since capture)" if moved else \
                    "recorded before-body differs on the SAME snapshots"
                if not moved:
                    same = False
        print("days %d: %s  bytes %d  [%s]" % (days, "EQUAL" if same else "DIFFERENT", len(new_bodies[days]), note))
        equal += 1 if same else 0
    print("EQUAL %d of 3" % equal)
    return 0 if equal == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
