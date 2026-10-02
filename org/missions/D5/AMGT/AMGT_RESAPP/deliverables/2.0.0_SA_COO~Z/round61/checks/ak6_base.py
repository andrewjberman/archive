"""AMGT_RESAPP round 61 -- ak-6's base, read live: for every entry of the frozen rewrite plans, the stored object's
current VersionId (the rollback) and whether `store_field` still equals the plan's `before` (the precondition).

  python ak6_base.py --plan <json> [--plan <json> ...] --out <json>

Each plan entry carries `store_key`, `store_field` (a dotted path inside the stored object; `[i]` indexes a list) and
`before`. The output lists one row per DISTINCT key: {store_key, version_id, etag, last_modified, entries, mismatches}.
Prints the denominator (keys, entries) and every mismatch; exit 1 when any entry's stored value differs from `before`.
Read-only: GetObject/HeadObject on the pool bucket, nothing written.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict

import boto3

BUCKET = "opal-data-harvest"
_TOK = re.compile(r"([A-Za-z0-9_]+)|\[(\d+)\]")


def _get(doc, path):
    node = doc
    for key, idx in _TOK.findall(path):
        node = node[key] if key else node[int(idx)]
    return node


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="append", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    by_key = defaultdict(list)
    for path in a.plan:
        for e in json.load(open(path, encoding="utf-8")).get("entries") or []:
            by_key[e["store_key"]].append(e)
    s3 = boto3.client("s3", region_name="us-east-1")
    rows, bad = [], []
    for key in sorted(by_key):
        obj = s3.get_object(Bucket=BUCKET, Key=key)
        doc = json.loads(obj["Body"].read().decode("utf-8"))
        mism = []
        for e in by_key[key]:
            try:
                now = _get(doc, e["store_field"])
            except (KeyError, IndexError, TypeError) as err:
                now = f"UNLOCATABLE: {err}"
            if now != e.get("before"):
                mism.append({"store_field": e["store_field"], "stored": now if isinstance(now, str) else "<non-string>",
                             "before": e.get("before") if isinstance(e.get("before"), str) else "<non-string>"})
        rows.append({"store_key": key, "version_id": obj.get("VersionId"), "etag": obj.get("ETag"),
                     "last_modified": obj["LastModified"].isoformat(), "entries": len(by_key[key]), "mismatches": mism})
        bad.extend((key, m["store_field"]) for m in mism)
    json.dump({"bucket": BUCKET, "keys": len(rows), "entries": sum(r["entries"] for r in rows), "rows": rows},
              open(a.out, "w", encoding="utf-8"), indent=1)
    print(f"keys {len(rows)} entries {sum(r['entries'] for r in rows)} mismatches {len(bad)} {bad[:5]}")
    print(f"versioned rows {sum(1 for r in rows if r['version_id'] and r['version_id'] != 'null')} of {len(rows)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
