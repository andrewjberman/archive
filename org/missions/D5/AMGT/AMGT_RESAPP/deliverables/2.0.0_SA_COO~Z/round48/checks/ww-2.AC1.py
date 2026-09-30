"""AMGT_RESAPP round 48, AMGT-ww-2 AC1 -- LIST ROWS CARRY THE SERVED COMPANY NAME AND CLASSIFICATION, JOINED SERVER-SIDE.

`scoped_amgt._classification_for_ticker(ticker)` reads the canonical `etf-classifications` table (DynamoDB, key `ticker`, the BARE
ticker: "BA US" -> "BA") and answers {"status": "SERVED" | "ABSENT", "name", "classification": {"asset_class", "sub_asset_class",
"sector"}, "reason"} -- every value copied as the table holds it (a missing field is null, never guessed); ABSENT carries a reason
and a null name. `read_rankings(...)` rows each carry `name`, `classification` and `name_state` from it.
Checked: "BA US" (held) equals the table row; "ZZZNOTHELD US" is ABSENT with a reason; every live trending/chatter ranking row
carries the three keys and, where the table holds its bare ticker, the table's name.
usage: python <this>   (from the repo root; reads DynamoDB read-only)"""
import os
import sys

import boto3

sys.path.insert(0, os.getcwd())
from lib.research.api import scoped_amgt as sa  # noqa: E402


def table_row(bare):
    item = boto3.resource("dynamodb", region_name="us-east-1").Table("etf-classifications").get_item(Key={"ticker": bare}).get("Item")
    return {k: (str(v) if v is not None else None) for k, v in (item or {}).items()} or None


def main():
    bad = []
    if not hasattr(sa, "_classification_for_ticker"):
        print("scoped_amgt has no _classification_for_ticker")
        print("LIST ROWS CARRY THE SERVED NAME AND CLASSIFICATION: NO")
        return 1
    row = table_row("BA")
    got = sa._classification_for_ticker("BA US") or {}
    want_cls = {"asset_class": row.get("asset_class"), "sub_asset_class": row.get("sub_asset_class"), "sector": row.get("sector")}
    if got.get("status") != "SERVED" or got.get("name") != row.get("name") or got.get("classification") != want_cls:
        bad.append("BA US: %r" % {k: got.get(k) for k in ("status", "name", "classification")})
    miss = sa._classification_for_ticker("ZZZNOTHELD US") or {}
    if miss.get("status") != "ABSENT" or miss.get("name") is not None or not miss.get("reason"):
        bad.append("absent ticker: %r" % miss)
    rows = (sa.read_rankings("trending", "chatter") or {}).get("rows") or []
    for r in rows:
        if not all(k in r for k in ("name", "classification", "name_state")):
            bad.append("row %s lacks name/classification/name_state" % r.get("ticker"))
            continue
        t = table_row(str(r.get("ticker") or "").split(" ")[0])
        if t and r.get("name") != t.get("name"):
            bad.append("row %s name %r != table %r" % (r.get("ticker"), r.get("name"), t.get("name")))
    for b in bad:
        print("  BAD", b)
    print("ranking rows read: %d" % len(rows))
    ok = not bad and len(rows) > 0
    print("LIST ROWS CARRY THE SERVED NAME AND CLASSIFICATION: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
