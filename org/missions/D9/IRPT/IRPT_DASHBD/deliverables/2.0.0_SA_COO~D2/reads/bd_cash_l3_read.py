"""Read-only L3 read of ledger bd-gold-etf-classifier-cash-type-20261014 (order TO-DB-b-183), issuer 2.0.0_SA_COO~D2.

The 17 canonical rows typed Cash (sub_asset_class) whose asset_class is not cash are found by a filtered scan of the DynamoDB table etf-classifications (tickers only, no client data). The served advisor positions
files (s3://opal-data-49financial/advi/49financial/platinum/advisors/<id>/positions.json) are read INTO MEMORY and graded by count only: how many positions carry one of the 17 tickers and what asset_class they
carry, the objects' LastModified range, and how many files were written after the upload (2026-10-14T12:11Z). No advisor id, position or value is printed or kept. Usage: python -I <this file> [--out <json>]
"""
import datetime
import json
import sys
from pathlib import Path

import boto3

UPLOAD_UTC = datetime.datetime(2026, 10, 14, 12, 11, tzinfo=datetime.timezone.utc)
BUCKET, PREFIX = "opal-data-49financial", "advi/49financial/platinum/advisors/"
TABLE = "etf-classifications"


def moved_tickers(ddb):
    out, kw = [], {"TableName": TABLE, "ProjectionExpression": "ticker, asset_class, sub_asset_class",
                   "FilterExpression": "sub_asset_class = :c AND asset_class <> :k", "ExpressionAttributeValues": {":c": {"S": "Cash"}, ":k": {"S": "cash"}}}
    pages = 0
    while True:
        r = ddb.scan(**kw)
        pages += 1
        out += [i["ticker"]["S"] for i in r.get("Items", [])]
        if "LastEvaluatedKey" not in r:
            return sorted(out), pages
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]


def positions_of(doc):
    """The list of position dicts of a decoded positions.json, whatever the top-level shape (list, or an object holding one list of dicts)."""
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        for v in doc.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v
    return []


def main():
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    s3 = boto3.client("s3", region_name="us-east-1")
    tickers, pages = moved_tickers(ddb)
    tset = set(tickers)
    keys, tok = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": PREFIX}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        keys += [(o["Key"], o["LastModified"]) for o in r.get("Contents", []) if o["Key"].endswith("/positions.json")]
        tok = r.get("NextContinuationToken")
        if not tok:
            break
    out = {"claim": "measured", "moved_rows": len(tickers), "scan_pages": pages, "positions_files": len(keys), "files_after_upload": sum(1 for _, m in keys if m > UPLOAD_UTC),
           "last_modified_min": min(m for _, m in keys).strftime("%Y-%m-%dT%H:%MZ") if keys else None, "last_modified_max": max(m for _, m in keys).strftime("%Y-%m-%dT%H:%MZ") if keys else None}
    classes, total, shape_keys = {}, 0, None
    for k, _ in keys:
        doc = json.loads(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read())
        pos = positions_of(doc)
        if shape_keys is None and pos:
            shape_keys = sorted(pos[0])[:20]
        for p in pos:
            total += 1
            t = p.get("ticker") or p.get("symbol") or p.get("security") or ""
            if t in tset:
                c = str(p.get("asset_class") or p.get("assetClass") or p.get("class") or "?")
                classes[c] = classes.get(c, 0) + 1
    out.update({"positions_total": total, "position_keys_seen": shape_keys, "positions_on_a_moved_ticker_by_class": classes, "positions_on_a_moved_ticker": sum(classes.values()),
                "still_fixed_income": classes.get("fixed_income", 0)})
    text = json.dumps(out, indent=1)
    if "--out" in sys.argv:
        Path(sys.argv[sys.argv.index("--out") + 1]).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
