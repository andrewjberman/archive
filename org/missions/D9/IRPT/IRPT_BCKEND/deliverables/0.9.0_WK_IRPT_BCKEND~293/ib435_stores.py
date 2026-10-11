#!/usr/bin/env python3
"""IB-pr-435 phase B: for each ranked security and each date it is needed on, is its close in one of the six price stores the estate already holds?
Read only.  The six stores, their addresses, key and column declarations, readers and cache are the census module's OWN (data/assets/scripts/analysis/
commonwealth_price_census.py: STORES, CountingS3, grade_buckets, read_store via load_store_cached, build_views, match_security, symbol_claims).  Nothing is
hand-typed.  The module's bar on every other firm's buckets is kept: the S3 client is wrapped, a call under a barred bucket is refused and counted.

    python -I ib435_stores.py <phaseA.pkl> <store_cache_dir> <phaseB.pkl>     read the stores and match (a store already cached is not re-read)
    python -I ib435_stores.py --control                                       the planted fixture-store control, printed

A security matches a store as the module matches it: CUSIP first, ticker second, a ticker claimed by more than one ranked CUSIP is `ticker_reused` and NOT
credited.  A security-day is FOUND when the matched key has a positive price in the store on that date.  Needed days are the day and the prior trading day of every
account-day the security is carried on (phase A).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path[:0] = [str(ROOT), str(ROOT / "lib"), str(ROOT / "data/assets/scripts/analysis"), str(ROOT / "data/assets/scripts/silver")]
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import commonwealth_price_census as cpc  # noqa: E402

WINDOW = ("2026-06-09", "2026-10-09")
# price kind per store.  The two stores of the firm's own tree hold the custodian's own value of the same holding (CUSTODIAN MARK, per 2.0.0_SA_COO~C2, msg 5084);
# the other four are market stores.  Keyed by the id's tail so no firm key is typed.
CUSTODIAN_TAILS = ("silver-canonical-prices", "gold-canonical-holdings")


def price_kind(spec):
    return "custodian_mark" if spec["id"].endswith(CUSTODIAN_TAILS) else "market_close"


def day_int(s):
    return cpc.to_day(s)


def match_all(universe, view, claims):
    """-> {cusip: (kind, days array or None)} with the module's own match_security."""
    return {u["cusip"]: cpc.match_security(u, view, claims) for u in universe}


def found_days(kind, days, needed_ints):
    """The needed day-ints this store answers for a matched security; none when the match is not credited (none / ticker_reused)."""
    if kind not in ("cusip", "ticker") or days is None or not len(days):
        return []
    return sorted(set(int(x) for x in np.intersect1d(days, np.array(needed_ints, dtype="int64"))))


# ---------------------------------------------------------------------------- the planted control

class _FakeS3:
    """In-memory stand-in for the S3 client: serves one small parquet for any get_object, and lists nothing.  The census module's own read_store reads it."""

    def __init__(self, raw):
        self.raw = raw
        self.barred_read = 0

    def get_object(self, Bucket, Key, **kw):
        return {"Body": io.BytesIO(self.raw)}


def control_run():
    """Plant two security-days against a small fixture store read by the module's own read_store (spec of the first declared store, a ticker-only parquet):
    FIXA priced on day X (present), FIXB not priced on day X (absent: priced on another day only), FIXC priced with price 0 on day X (a zero is not a close),
    and a row for a key the universe does not ask for.  Needed: FIXA@X, FIXB@X.  Planted: FIXA@X found, FIXB@X not found."""
    spec = dict(cpc.STORES[0])
    X, Y = "2026-09-01", "2026-09-02"
    t = pd.DataFrame({spec["date_col"]: [X, Y, X, X], spec["price_col"]: [10.0, 11.0, 0.0, 5.0], "ticker": ["FIXA", "FIXB", "FIXC", "OTHER"],
                      spec["source_col"]: ["fixture"] * 4})
    buf = io.BytesIO()
    t.to_parquet(buf, index=False)
    universe = [dict(cusip="CUSIPFIXA", asset_type="x", first_day=day_int(X), symbols=["FIXA"]),
                dict(cusip="CUSIPFIXB", asset_type="x", first_day=day_int(X), symbols=["FIXB"]),
                dict(cusip="CUSIPFIXC", asset_type="x", first_day=day_int(X), symbols=["FIXC"])]
    wanted = {"ticker": {cpc.norm_key(s) for u in universe for s in u["symbols"]}, "cusip": {cpc.norm_key(u["cusip"]) for u in universe}}
    df, n_raw, n_obj = cpc.read_store(_FakeS3(buf.getvalue()), spec, wanted)
    view = cpc.build_views(df)["all"]
    m = match_all(universe, view, cpc.symbol_claims(universe))
    read = {}
    for sec, day in (("CUSIPFIXA", X), ("CUSIPFIXB", X), ("CUSIPFIXC", X)):
        kind, days = m[sec]
        read["%s@%s" % (sec, day)] = bool(found_days(kind, days, [day_int(day)]))
    return {"security_days": read, "rows_read_raw": int(n_raw), "rows_kept_for_wanted_keys": int(len(df))}


PLANTED = {"security_days": {"CUSIPFIXA@2026-09-01": True, "CUSIPFIXB@2026-09-01": False, "CUSIPFIXC@2026-09-01": False},
           "rows_read_raw": 4, "rows_kept_for_wanted_keys": 2}   # kept: FIXA@X and FIXB@Y (FIXC's zero price and the OTHER key are dropped)


def main():
    if sys.argv[1:] == ["--control"]:
        r = control_run()
        print(json.dumps(r, indent=1), "\nEQUAL:", r == PLANTED)
        return 0 if r == PLANTED else 1
    pa = pickle.load(open(sys.argv[1], "rb"))
    cache_dir, out = sys.argv[2], Path(sys.argv[3])
    secs = dict(pa["securities"])
    for c, v in pa["securities_added"].items():
        secs.setdefault(c, v)
    needed = {c: sorted(set(pa["needed_dates"].get(c, [])) | set(pa["needed_dates_added"].get(c, []))) for c in secs}
    needed_pre = {c: pa["needed_dates"][c] for c in pa["securities"]}
    universe = [dict(cusip=c, asset_type="x", first_day=day_int(min(needed[c])), symbols=list(v["tickers"])) for c, v in sorted(secs.items())]
    claims = cpc.symbol_claims(universe)
    wanted = {"ticker": {cpc.norm_key(s) for u in universe for s in u["symbols"]}, "cusip": {cpc.norm_key(u["cusip"]) for u in universe}}
    uhash = hashlib.sha256(json.dumps([[u["cusip"], u["symbols"]] for u in universe] + ["ib435"]).encode()).hexdigest()[:12]

    import boto3
    from botocore.config import Config
    raw = boto3.client("s3", region_name="us-east-1", config=Config(retries={"max_attempts": 8, "mode": "standard"}, read_timeout=120))
    scopes = cpc.load_scopes()
    names = [b["Name"] for b in raw.list_buckets()["Buckets"]]
    graded = cpc.grade_buckets(names, scopes)
    barred = {g["name"] for g in graded if g["grade"] == "BARRED"}
    s3 = cpc.CountingS3(raw, barred)
    res = {"uhash": uhash, "stores": [], "universe_securities": len(universe), "symbols_claimed_by_more_than_one": sum(1 for c in claims.values() if c > 1)}
    w0, w1 = day_int(WINDOW[0]), day_int(WINDOW[1])
    for spec in cpc.STORES:
        rec = {"id": spec["id"], "legacy_key": spec["legacy"], "price_kind": price_kind(spec), "fmt": spec["fmt"], "key_cols": spec["key_cols"],
               "bucket": cpc.store_home(spec), "bucket_class": next(g["grade"] for g in graded if g["name"] == cpc.store_home(spec))}
        try:
            if rec["bucket_class"] == "BARRED":
                raise cpc.BarredBucketError("store bucket is BARRED")
            df, meta, cached = cpc.load_store_cached(s3, spec, uhash, wanted, cache_dir, False)
        except Exception as e:  # a failed read is recorded with its reason, never a silent zero
            rec.update(opened=False, not_opened_reason="%s: %s" % (type(e).__name__, str(e)[:200]))
            res["stores"].append(rec)
            print("store", spec["id"], "NOT OPENED", rec["not_opened_reason"], file=sys.stderr, flush=True)
            continue
        views = cpc.build_views(df)
        view = views.pop("all")
        in_win = df[(df["day"] >= w0) & (df["day"] <= w1)]
        rec.update(opened=True, from_cache=bool(cached), rows_raw=meta["rows_raw"], rows_kept=meta["rows_kept"], objects_read=meta["objects_read"],
                   first_date_any=str(cpc.EPOCH + dt.timedelta(days=int(df["day"].min()))) if len(df) else None,
                   last_date_any=str(cpc.EPOCH + dt.timedelta(days=int(df["day"].max()))) if len(df) else None,
                   first_date=str(cpc.EPOCH + dt.timedelta(days=int(in_win["day"].min()))) if len(in_win) else None,
                   last_date=str(cpc.EPOCH + dt.timedelta(days=int(in_win["day"].max()))) if len(in_win) else None,
                   sources=sorted(df["source"].astype(str).unique())[:12] if len(df) else [])
        m = match_all(universe, view, claims)
        found, kinds = {}, {}
        for c, (kind, days) in m.items():
            kinds[c] = kind
            ints = [day_int(d) for d in needed[c]]
            found[c] = [str(cpc.EPOCH + dt.timedelta(days=x)) for x in found_days(kind, days, ints)]
        rec["match_kind"] = {k: sum(1 for v in kinds.values() if v == k) for k in ("cusip", "ticker", "ticker_reused", "none")}
        rec["found"] = found
        res["stores"].append(rec)
        print("store", spec["id"], "opened", rec["first_date"], rec["last_date"], rec["match_kind"], "found", sum(len(v) for v in found.values()), flush=True)
    res["barred_read"] = s3.barred_read
    res["calls_by_bucket"] = dict(s3.calls)
    res["needed_pre_security_days"] = sum(len(v) for v in needed_pre.values())
    pickle.dump(res, open(out, "wb"))
    print("wrote", out, "barred_read", s3.barred_read)
    return 0 if s3.barred_read == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
