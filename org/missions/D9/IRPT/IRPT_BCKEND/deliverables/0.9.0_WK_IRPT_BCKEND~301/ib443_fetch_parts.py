#!/usr/bin/env python3
"""IB-pr-443 step 1.  Read only (S3 list + get).  Per weekday: the holdings-source partition reduced to the rows of FOUR named securities only
(CUSIP, Ticker, Symbol, Market Value, Units -- no account column is read) and the anchor partition reduced to (cusip, closing_price) of
those securities' CUSIPs.  Each partition's object count and earliest / latest LastModified (UTC) is kept.  Cache outside the repo, deleted
file by file at the end.  Uses the declared-prefix resolution of ib441_fetch_s3.py (copied, untouched).

    python -I ib443_fetch_parts.py discover <cache_dir> <date> [<date> ...]      -> prints ticker -> CUSIP(s) found on those dates
    python -I ib443_fetch_parts.py fetch <cache_dir> <first_date> <last_date> <CUSIP,CUSIP,...>
"""
import datetime as dt
import io
import pickle
import sys
from pathlib import Path

import boto3
import pyarrow.parquet as pq
from botocore.config import Config

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ib441_fetch_s3 as f  # noqa: E402

TICKERS = ("MEIIX", "MISIX", "SHM", "PZA")
SRC_COLS = ["CUSIP", "Ticker", "Symbol", "Market Value", "Units"]
ANC_COLS = ["cusip", "closing_price"]


def objs_of(s3, prefix, day):
    resp = s3.list_objects_v2(Bucket=f.BUCKET, Prefix="%sdate=%s/" % (prefix, day))
    return sorted((o for o in resp.get("Contents", []) if o["Key"].endswith(".parquet")), key=lambda o: o["Key"])


def read_part(s3, prefix, day, cols, keep):
    """-> dict of lists for the kept rows, plus _meta; None when the partition is absent."""
    objs = objs_of(s3, prefix, day)
    if not objs:
        return None
    out = {c: [] for c in cols}
    n_rows = 0
    for o in objs:
        buf = io.BytesIO(s3.get_object(Bucket=f.BUCKET, Key=o["Key"])["Body"].read())
        have = set(pq.read_schema(buf).names)
        t = pq.read_table(buf, columns=[c for c in cols if c in have]).to_pydict()
        n = len(next(iter(t.values()))) if t else 0
        n_rows += n
        for i in range(n):
            if keep({c: (t[c][i] if c in t else None) for c in cols}):
                for c in cols:
                    out[c].append(t[c][i] if c in t else None)
    lm = [o["LastModified"] for o in objs]
    out["_meta"] = {"objects": len(objs), "rows_in_partition": n_rows, "first_modified_utc": min(lm).isoformat(), "last_modified_utc": max(lm).isoformat()}
    return out


def main():
    mode, cache = sys.argv[1], Path(sys.argv[2])
    cache.mkdir(parents=True, exist_ok=True)
    SRC, ANCHOR = f.declared()
    s3 = boto3.client("s3", region_name="us-east-1", config=Config(retries={"max_attempts": 8, "mode": "standard"}, read_timeout=120))

    def src_keep_ticker(r):
        return any((str(r.get(k) or "").strip().upper() in TICKERS) for k in ("Ticker", "Symbol"))
    if mode == "discover":
        found = {}
        for day in sys.argv[3:]:
            t = read_part(s3, SRC, day, SRC_COLS, src_keep_ticker)
            if t is None:
                print(day, "ABSENT")
                continue
            for c, a, b in zip(t["CUSIP"], t["Ticker"], t["Symbol"]):
                for x in (a, b):
                    x = str(x or "").strip().upper()
                    if x in TICKERS:
                        found.setdefault(x, set()).add((c or "").strip())
            print(day, "rows kept", len(t["CUSIP"]), t["_meta"])
        for k in sorted(found):
            print(k, sorted(found[k]))
        return
    a, b = dt.date.fromisoformat(sys.argv[3]), dt.date.fromisoformat(sys.argv[4])
    cusips = set(sys.argv[5].split(","))
    d = a
    while d <= b:
        day = d.isoformat()
        if d.weekday() < 5:
            for kind, prefix, cols, keep in (
                    ("src", SRC, SRC_COLS, lambda r: (str(r.get("CUSIP") or "").strip() in cusips)),
                    ("anc", ANCHOR, ANC_COLS, lambda r: (str(r.get("cusip") or "").strip() in cusips))):
                fn = cache / ("%s_%s.pkl" % (kind, day))
                if fn.exists():
                    continue
                t = read_part(s3, prefix, day, cols, keep)
                pickle.dump(t, open(fn, "wb"))     # None is cached as absent
                print(kind, day, "ABSENT" if t is None else "kept %d of %d" % (len(t[cols[0]]), t["_meta"]["rows_in_partition"]), flush=True)
        d += dt.timedelta(days=1)


if __name__ == "__main__":
    main()
