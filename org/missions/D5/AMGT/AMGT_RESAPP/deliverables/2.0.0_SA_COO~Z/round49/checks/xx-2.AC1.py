"""AMGT_RESAPP round 49, AMGT-xx-2 AC1 -- THE RANK-HISTORY SERIES CARRY THE SERVED COMPANY NAME, JOINED SERVER-SIDE (DSGN FWD-3 labels).

`scoped_amgt.read_rank_series(movement, subject, tickers, ...)` -- each entry of `series` carries `name`, `classification` and
`name_state` from `_classification_for_ticker` (the SAME join ww-2 put on list rows; one read per distinct ticker). Checked on the
live trending/chatter axis: the first five ranked tickers plus "ZZZNOTHELD US"; a ticker the table holds carries the table's name;
the unheld ticker reads name_state ABSENT with a null name; every series keeps its `ticker` and `points` as before.
usage: python <this>   (from the repo root; reads DynamoDB read-only)"""
import os
import sys

import boto3

sys.path.insert(0, os.getcwd())
from lib.research.api import scoped_amgt as sa  # noqa: E402


def table_name(bare):
    item = boto3.resource("dynamodb", region_name="us-east-1").Table("etf-classifications").get_item(Key={"ticker": bare}).get("Item")
    return (item or {}).get("name"), bool(item)


def main():
    rows = (sa.read_rankings("trending", "chatter") or {}).get("rows") or []
    tickers = [str(r.get("ticker")) for r in rows[:5] if r.get("ticker")] + ["ZZZNOTHELD US"]
    out = sa.read_rank_series("trending", "chatter", tickers) or {}
    series = out.get("series") or []
    by = {str(s.get("ticker")): s for s in series}
    bad = []
    named = 0
    for t in tickers:
        s = by.get(t)
        if s is None:
            bad.append("%s: no series entry" % t)
            continue
        if not all(k in s for k in ("name", "classification", "name_state", "points")):
            bad.append("%s: series lacks name/classification/name_state/points" % t)
            continue
        want, held = table_name(t.split(" ")[0])
        if held and s.get("name") != want:
            bad.append("%s: name %r != table %r" % (t, s.get("name"), want))
        if not held and (s.get("name_state") != "ABSENT" or s.get("name") is not None):
            bad.append("%s: unheld ticker reads %r / %r" % (t, s.get("name_state"), s.get("name")))
        named += s.get("name_state") == "SERVED"
    for b in bad:
        print("  BAD", b)
    print("tickers asked %d, series %d, name SERVED %d" % (len(tickers), len(series), named))
    ok = not bad and named > 0
    print("RANK-HISTORY SERIES CARRY THE SERVED NAME: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
