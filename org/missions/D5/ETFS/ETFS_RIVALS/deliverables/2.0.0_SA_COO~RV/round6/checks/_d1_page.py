"""Shared fixture for the RIV-st-1 checks (issuer-written, 2.0.0_SA_COO~RV): the round-5 page fixture (test_p2:
TXUE and BASG on 2026-09-25, 09-28 and 09-29, G5 replayed), published for page day 2026-09-30 so the A1 producers
build their three tables once; then a NEWER canonical_shape (G1) object for the existing date 2026-09-29 can be
planted.

Offline: a `local:` sink, and `market_context.read_context` is replaced by a stub returning no readings (the census
producer would otherwise read S3)."""
import datetime as dt
import json
import os
import time

import _common as c

DAY = "2026-09-30"  # page day
AS_OF = "2026-09-29"  # prev_trading_day(DAY): the planted date
PRODUCED = ("holding_contribution", "buying_trend", "input_census")  # the tables produce_a1 builds


def start():
    """The page fixture plus one publish (batch d1a). Returns (spec, sink, first publish result)."""
    c.setup_path()
    from rivalfunds import market_context, publish_page

    market_context.read_context = lambda day, *a, **k: []
    os.environ.pop(publish_page.PRODUCE_ENV, None)
    spec, s, _ = c.page_fixture()
    return spec, s, publish(spec, "d1a")


def publish(spec, batch, **kw):
    from rivalfunds import publish_page

    return publish_page.handler_entry({"date": DAY, "mode": "daily", "batch_id": batch, "sink": spec, **kw})


def objects(s, table):
    from rivalfunds import homes

    return sorted(u for u in s.list(homes.address("rivalfunds", "etfs", "gold", table, f"date={DAY}") + "/")
                  if u.endswith(".parquet"))


def newest_time(s, tables=PRODUCED):
    """The latest revision time over the newest object of each table."""
    from rivalfunds import revision

    return max(revision.capture_time(revision.newest(objects(s, t))) for t in tables if objects(s, t))


def plant_g1(s, drift=0.5):
    """Plant a canonical_shape object for 2026-09-29 whose revision time is one second LATER than every A1
    table's newest object, with different valuations (drift 0.5 for 0.2); then wait until the clock is one second
    past it, so a build that follows is strictly later than the planted input. Returns the planted object's uri."""
    from rivalfunds import homes, revision
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    t = newest_time(s) + dt.timedelta(seconds=1)
    rev = revision.compact(t) + "-bbbbbbbbbbbb"
    tp2._put(s, AS_OF, {"TXUE": (tp2._book(2), "bloomberg", drift), "BASG": (tp2._book(2), "issuer", drift)}, rev=rev)
    while dt.datetime.now(dt.timezone.utc) < t + dt.timedelta(seconds=1):
        time.sleep(0.2)
    return homes.canonical_shape(AS_OF, f"holdings-{rev}.parquet")


def plant_g4(s):
    """Plant a security_market (G4) object for 2026-09-29, one second later than every A1 table's newest object."""
    import io

    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq

    from rivalfunds import enrichment_bloomberg as eb
    from rivalfunds import revision

    rev = revision.compact(newest_time(s) + dt.timedelta(seconds=1)) + "-dddddddddddd"
    row = {"security_id": "S01", "date": AS_OF, "px_close": 11.0, "total_return_index": None, "gics_sector": "Energy"}
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pandas(pd.DataFrame([row]), preserve_index=False), buf)
    uri = eb.market_target_uri(AS_OF, rev)
    s.put(uri, buf.getvalue())
    return uri


def manifest(s):
    from rivalfunds import homes

    return json.loads(s.get(homes.page(DAY, "manifest.json")).decode("utf-8"))
