#!/usr/bin/env python3
"""IB-pr-425 step 1: reduce each needed partition to its security-level columns and cache the result OUTSIDE the worktree.

    python -I s252_fetch.py <cache_dir> <first_date> <last_date>      (calendar dates, inclusive; bounded step, e.g. one month)

Reads only (S3 list + get, same boto3 path as the instruments in IRPT_MVP_P). The cache holds, per source partition, one row per
position reduced to (CUSIP, Market Value, Units, Symbol, Asset Name, Cash Equivalent, Expense Ratio) -- NO account id, no account
number -- and per anchor partition (cusip, ticker, closing_price, secprice_lstupdte). The cache stays in <cache_dir> (outside the repo).
"""
import io
import json
import pickle
import sys
from pathlib import Path
import boto3
import pyarrow.parquet as pq
from botocore.config import Config

BUCKET = "opal-data-assets"


def declared():
    """The source prefix is RESOLVED the way the gold script resolves it (registry-derived scope, never a typed firm token);
    the anchor prefix is read from the declaration's own schwab entry."""
    here = Path(__file__).resolve()
    root = here.parents[7]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/gold/irpt_holdings_performance")]
    import holdings_performance as hp
    decl = json.load(open(root / "data/assets/scripts/gold/irpt_holdings_performance/sources.json", encoding="utf-8"))
    src = decl["blackdiamond_z09"]
    return hp.resolved_prefix(src, "positions_prefix", hp.firm_scope(src)), decl["schwab_08335338"]["positions_prefix"], src["bucket"]
SRC_COLS = ["CUSIP", "Market Value", "Units", "Symbol", "Asset Name", "Cash Equivalent", "Expense Ratio"]
ANC_COLS = ["cusip", "ticker_symbol", "closing_price", "secprice_lstupdte"]


def get(s3, prefix, day, cols):
    for attempt in range(4):
        try:
            resp = s3.list_objects_v2(Bucket=BUCKET, Prefix="%sdate=%s/" % (prefix, day))
            keys = sorted(o["Key"] for o in resp.get("Contents", []) if o["Key"].endswith(".parquet"))
            if not keys:
                return None
            out = {c: [] for c in cols}
            for k in keys:
                t = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()), columns=cols).to_pydict()
                for c in cols:
                    out[c] += t[c]
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
