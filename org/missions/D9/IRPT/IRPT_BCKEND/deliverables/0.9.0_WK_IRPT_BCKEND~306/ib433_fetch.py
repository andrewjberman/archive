#!/usr/bin/env python3
"""IB-pr-435 step 1 (copied from IB-pr-429's ib429_fetch.py, deliverables/0.9.0_WK_IRPT_BCKEND~288/, untouched; extended by three security-identifier columns).

    python -I ib429_fetch.py <cache_dir> <first_date> <last_date>      (calendar dates, inclusive; bounded step, e.g. one month)

Reads only (S3 list + get).  The cache holds, per source partition, one row per position reduced to (CUSIP, Market Value, Units,
AccountID, Cash Equivalent) and per anchor partition (cusip, closing_price).  AccountID is replaced AT READ TIME by a 12-character
one-way digest so the cache never holds a raw account id.  Each cached partition also carries "_meta": the object count and the
earliest and latest object LastModified (UTC) -- times only, for the instrument's daily-needs timing.  The cache stays in
<cache_dir> (outside the repo) and is deleted file by file at the end.
"""
import hashlib
import io
import json
import pickle
import sys
from pathlib import Path
import boto3
import pyarrow.parquet as pq
from botocore.config import Config

BUCKET = "opal-data-assets"
SRC_COLS = ["CUSIP", "Market Value", "Units", "AccountID", "Cash Equivalent", "Ticker", "Symbol", "Asset Name"]   # last three added by IB-pr-435: security identifiers only
ANC_COLS = ["cusip", "closing_price"]


def declared():
    """The source prefix is RESOLVED the way the gold script resolves it; the anchor prefix is read from the declaration's own entry."""
    here = Path(__file__).resolve()
    root = here.parents[7]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/gold/irpt_holdings_performance")]
    import holdings_performance as hp
    decl = json.load(open(root / "data/assets/scripts/gold/irpt_holdings_performance/sources.json", encoding="utf-8"))
    src = decl["blackdiamond_z09"]
    return hp.resolved_prefix(src, "positions_prefix", hp.firm_scope(src)), decl["schwab_08335338"]["positions_prefix"], src["bucket"]


def get(s3, prefix, day, cols):
    for attempt in range(4):
        try:
            resp = s3.list_objects_v2(Bucket=BUCKET, Prefix="%sdate=%s/" % (prefix, day))
            objs = sorted((o for o in resp.get("Contents", []) if o["Key"].endswith(".parquet")), key=lambda o: o["Key"])
            if not objs:
                return None
            out = {c: [] for c in cols}
            lm = [o["LastModified"] for o in objs]
            out["_meta"] = {"objects": len(objs), "first_modified_utc": min(lm).isoformat(), "last_modified_utc": max(lm).isoformat()}
            for o in objs:
                buf = io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read())
                have = set(pq.read_schema(buf).names)
                t = pq.read_table(buf, columns=[c for c in cols if c in have]).to_pydict()
                n = len(next(iter(t.values()))) if t else 0
                out.setdefault("_absent_columns", sorted(set(cols) - have))
                for c in cols:
                    if c not in t:
                        t[c] = [None] * n   # column absent from this partition's schema: recorded in _absent_columns
                    out[c] += ([hashlib.sha256(str(x).encode()).hexdigest()[:12] for x in t[c]] if c == "AccountID" else t[c])
            return out
        except Exception:
            if attempt == 3:
                raise
    return None


def main():
    SRC_PREFIX, ANCHOR, _ = declared()
    cache = Path(sys.argv[1])
    cache.mkdir(parents=True, exist_ok=True)
    import datetime as dt
    a, b = dt.date.fromisoformat(sys.argv[2]), dt.date.fromisoformat(sys.argv[3])
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(retries={"max_attempts": 8, "mode": "standard"}, read_timeout=120))
    d = a
    while d <= b:
        day = d.isoformat()
        for kind, prefix, cols in (("src", SRC_PREFIX, SRC_COLS), ("anc", ANCHOR, ANC_COLS)):
            f = cache / ("%s_%s.pkl" % (kind, day))
            if f.exists():
                continue
            t = get(s3, prefix, day, cols)
            pickle.dump(t, open(f, "wb"))   # None is cached as absent
            print(kind, day, "ABSENT" if t is None else len(t[cols[0]]), flush=True)
        d += dt.timedelta(days=1)


if __name__ == "__main__":
    main()
