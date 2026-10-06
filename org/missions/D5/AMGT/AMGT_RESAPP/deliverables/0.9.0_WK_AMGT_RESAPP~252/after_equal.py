"""AMGT-ax-1 AC2: /freshness answers the same values after the change as before it.

Reads before.json (the body captured before any edit), calls the route handler twice (cold, then warm),
and compares every row of each with it, ignoring `generated_at` and any per-request timing field.
Prints `EQUAL n of n rows` and exits 0 only when every row of both reads equals its before row and the
row counts match; otherwise prints `DIFFERENT ...` and exits 1."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

IGNORED = {"generated_at", "elapsed_ms", "took_ms", "timing", "duration_ms"}


def _strip(value):
    if isinstance(value, dict):
        return {k: _strip(v) for k, v in value.items() if k not in IGNORED}
    if isinstance(value, list):
        return [_strip(v) for v in value]
    return value


def _body():
    from lib.research.api import scoped_amgt

    event = {"rawPath": "/api/scoped/amgt/freshness", "requestContext": {"http": {"method": "GET"}},
             "headers": {"x-firm-id": "opal"}, "queryStringParameters": None}
    response = scoped_amgt.handler(event)
    if response.get("statusCode") != 200:
        print("DIFFERENT status {0}".format(response.get("statusCode")))
        sys.exit(1)
    return json.loads(response["body"])


def main() -> int:
    before = json.load(open(os.path.join(HERE, "before.json"), encoding="utf-8"))
    before_rows = _strip(before["rows"])
    bad = 0
    for label in ("cold", "warm"):
        rows = _strip(_body()["rows"])
        diff = [i for i in range(max(len(rows), len(before_rows)))
                if i >= len(rows) or i >= len(before_rows) or rows[i] != before_rows[i]]
        print("{0}: {1} rows served, {2} rows before, {3} differing".format(label, len(rows), len(before_rows), len(diff)))
        for i in diff[:5]:
            print("  row {0}: before {1} / after {2}".format(
                i, json.dumps(before_rows[i] if i < len(before_rows) else None, sort_keys=True)[:300],
                json.dumps(rows[i] if i < len(rows) else None, sort_keys=True)[:300]))
        bad += len(diff)
        n = len(rows)
    if bad:
        print("DIFFERENT {0} rows".format(bad))
        return 1
    print("EQUAL {0} of {0} rows".format(n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
