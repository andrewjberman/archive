"""AMGT_RESAPP round 48, AMGT-ww-3 AC3 (the seat's run at the drain) -- EVERY LIBRARY NAME HAS A CLASSIFICATION ROW.

After the writer's real run: each of the 95 library bare tickers (fixtures/library95.json) is held by `etf-classifications` with
asset_class set and a non-empty sub_asset_class. A name may be absent (withheld: no clean source); a held name is never all-caps.
usage: python <this>   (from the repo root; reads DynamoDB read-only)"""
import json
import os
import re
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    lib = json.load(open(os.path.join(HERE, "fixtures", "library95.json"), encoding="utf-8"))["names"]
    t = boto3.resource("dynamodb", region_name="us-east-1").Table("etf-classifications")
    held = named = 0
    bad = []
    for b in sorted({n["bare"] for n in lib}):
        it = t.get_item(Key={"ticker": b}).get("Item")
        if not it:
            bad.append("%s absent" % b)
            continue
        held += 1
        if not it.get("asset_class") or not it.get("sub_asset_class"):
            bad.append("%s unclassified" % b)
        nm = it.get("name")
        if nm:
            named += 1
            if nm == b or (re.search(r"[A-Z]{2}", nm) and nm == nm.upper() and b not in ("BP", "GSK")):
                bad.append("%s name %r" % (b, nm))
    for x in bad[:12]:
        print("  BAD", x)
    print("library 95: held %d, named %d, defects %d" % (held, named, len(bad)))
    ok = not bad and held == 95
    print("EVERY LIBRARY NAME HAS A CLASSIFICATION ROW: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
