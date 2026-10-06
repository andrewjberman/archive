"""AMGT_RESAPP AMGT-ax-3 AC2: the chatter route's served body is unchanged by the faster mention read.

For days 30, 90 and 365 this prints one line and ends with `EQUAL n of 3`:
  1. the route as it is now (ranged column read, counts by column) is served;
  2. the SAME route is served again with the per-row loop it replaced (`_the_row_loop`, verbatim, over the same
     snapshot read whole and decoded to dicts) standing in for the count, on the same snapshots (the newest-object
     lookups are pinned for the process, so a snapshot that lands mid-run cannot make the two differ);
  3. the two body texts must be byte-equal;
  4. the body captured BEFORE the edit (`before/days<N>.json`, by `capture.py`) is also compared: equal, or, when
     the snapshots it was captured on are no longer the newest (its vintage/as_of differ from now), reported as
     DRIFT, never counted against the cut.
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
    real_object = pool_reader._gold_newest_object
    real_key = monthly_chatter._newest_snapshot_key

    def pin_object(table, client=None):
        if table not in pinned:
            pinned[table] = real_object(table, client)
        return pinned[table]

    keys = {}

    def pin_key(table):
        if table not in keys:
            keys[table] = real_key(table)
        return keys[table]

    pool_reader._gold_newest_object = pin_object
    monthly_chatter._newest_snapshot_key = pin_key

    new_bodies = {days: _serve(scoped_amgt, days) for days in (30, 90, 365)}

    # the same snapshot, every column, one dict per row: what the replaced loop read
    found = pin_object(monthly_chatter.MENTION_TABLE)
    client, bucket, key, _etag = found
    raw = client.get_object(Bucket=bucket, Key=key)["Body"].read()
    whole_rows = pq.read_table(io.BytesIO(raw)).to_pylist()
    new_counts = monthly_chatter._publisher_counts
    monthly_chatter._publisher_counts = lambda mentions, covered, months: _the_row_loop(whole_rows, covered, months)
    old_bodies = {days: _serve(scoped_amgt, days) for days in (30, 90, 365)}
    monthly_chatter._publisher_counts = new_counts

    equal = 0
    for days in (30, 90, 365):
        same = new_bodies[days] == old_bodies[days]
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
