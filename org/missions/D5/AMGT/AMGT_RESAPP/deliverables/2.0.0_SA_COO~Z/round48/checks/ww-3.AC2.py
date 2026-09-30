"""AMGT_RESAPP round 48, AMGT-ww-3 AC2 -- THE 36 ROWS THE TABLE ALREADY HELD ARE BYTE-UNCHANGED (the bound on the write).

Reads each of the 36 library tickers `etf-classifications` held at the cut (fixtures/etfc_held_before.json, str values) and compares
every attribute. Passes before the write and must still pass after it: the writer preserves an existing row.
usage: python <this>   (from the repo root; reads DynamoDB read-only)"""
import json
import os
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    before = json.load(open(os.path.join(HERE, "fixtures", "etfc_held_before.json"), encoding="utf-8"))["rows"]
    t = boto3.resource("dynamodb", region_name="us-east-1").Table("etf-classifications")
    bad = []
    for tk, row in sorted(before.items()):
        item = t.get_item(Key={"ticker": tk}).get("Item") or {}
        now = {k: (str(v) if v is not None else None) for k, v in item.items()}
        if now != row:
            bad.append("%s: %r" % (tk, sorted(set(now.items()) ^ set(row.items()))[:3]))
    for b in bad:
        print("  BAD", b)
    print("held rows compared: %d, changed: %d" % (len(before), len(bad)))
    ok = not bad and len(before) == 36
    print("THE 36 HELD ROWS ARE UNCHANGED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
