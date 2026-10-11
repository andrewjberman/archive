#!/usr/bin/env python3
"""IB-pr-441 step 1.  Read only (S3 list + get).  Per calendar day: the source partition reduced to (CUSIP, Ticker, Symbol) -- no account column is read --
and the anchor partition reduced to (cusip, closing_price).  Cache outside the repo, deleted file by file at the end.

    python -I ib441_fetch_s3.py <cache_dir> <first_date> <last_date>
"""
import datetime as dt
import io
import json
import pickle
import sys
from pathlib import Path
import boto3
import pyarrow.parquet as pq
from botocore.config import Config

BUCKET = "opal-data-assets"
SRC_COLS = ["CUSIP", "Ticker", "Symbol"]
ANC_COLS = ["cusip", "closing_price"]


def declared():
    """The source prefix is RESOLVED the way the gold script resolves it; the anchor prefix is read from the declaration's own entry."""
    here = Path(__file__).resolve()
    root = here.parents[7]
    sys.path[:0] = [str(root / "lib"), str(root), str(root / "data/assets/scripts/gold/irpt_holdings_performance")]
    import holdings_performance as hp
    decl = json.load(open(root / "data/assets/scripts/gold/irpt_holdings_performance/sources.json", encoding="utf-8"))
    src = decl["blackdiamond_z09"]
    return hp.resolved_prefix(src, "positions_prefix", hp.firm_scope(src)), decl["schwab_08335338"]["positions_prefix"]


def get(s3, prefix, day, cols):
    for attempt in range(4):
        try:
            resp = s3.list_objects_v2(Bucket=BUCKET, Prefix="%sdate=%s/" % (prefix, day))
            objs = sorted((o for o in resp.get("Contents", []) if o["Key"].endswith(".parquet")), key=lambda o: o["Key"])
            if not objs:
                return None
            out = {c: [] for c in cols}
            for o in objs:
                buf = io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read())
                have = set(pq.read_schema(buf).names)
                t = pq.read_table(buf, columns=[c for c in cols if c in have]).to_pydict()
                n = len(next(iter(t.values()))) if t else 0
                for c in cols:
                    out[c] += t[c] if c in t else [None] * n
            return out
        except Exception:
            if attempt == 3:
                raise
    return None


def main():
    SRC_PREFIX, ANCHOR = declared()
    cache = Path(sys.argv[1])
    cache.mkdir(parents=True, exist_ok=True)
    a, b = dt.date.fromisoformat(sys.argv[2]), dt.date.fromisoformat(sys.argv[3])
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(retries={"max_attempts": 8, "mode": "standard"}, read_timeout=120))
    d = a
    while d <= b:
        day = d.isoformat()
        if d.weekday() < 5:
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
