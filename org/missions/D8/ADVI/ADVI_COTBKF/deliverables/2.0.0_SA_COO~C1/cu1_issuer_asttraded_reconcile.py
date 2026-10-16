"""ADVI_COTBKF round 99 (issuer 2.0.0_SA_COO~C1, 2026-10-16 ~08:2xZ): does applying the as-traded basis to the FRESH stores (worker ~188's
`cotbkf_r99/store_cache`, read from S3 with refresh=True) close the 184-point difference CB-cu-1 found between the store-derived Yahoo set and the
served `use_class` labels? Reads local caches and ONE get of the served account_day_value at its VersionId; counts only; writes nothing.
Result of the run (stdout): as_traded stats tickers 911, replaced 1049193, rederived 477980, dropped_unbracketed 3962 (equal to round 97);
S' 2030243; X 475103; A' 471195; B 471195; A'&B 471195; A'-B 0; B-A' 0. Needs the received run data and AWS read credentials."""
import io
import sys

sys.path.insert(0, "C:/Dev/ajb_workspace/data/assets/scripts/silver")
sys.path.insert(0, "C:/Dev/ajb_workspace/data/assets/scripts/analysis")
sys.path.insert(0, "C:/Dev/ajb_workspace/lib")
import boto3
import pandas as pd
import pyarrow.parquet as pq

import commonwealth_daily_holdings as dh
import commonwealth_daily_valuation as dv
import commonwealth_price_census as pc

CACHE = "C:/Dev/ajb_workspace/.scratch/advi_cotbkf/cache"
STORE_CACHE = "C:/Dev/ajb_workspace/.scratch/cotbkf_r99/store_cache"
YAHOO = "C:/Dev/ajb_workspace/.scratch/advi_cotbkf/yahoo_census"

tx, _pos = dh.load_tx_pos(CACHE)
universe = dv.universe_from_tx(tx)
uh = dv._uhash(universe)
wanted = {"ticker": {pc.norm_key(s) for u in universe for s in u["symbols"]},
          "cusip": {pc.norm_key(u["cusip"]) for u in universe}}
stores = []
for spec in pc.STORES:
    df, cached = dv.load_price_store(None, spec, uh, wanted, STORE_CACHE, False)
    stores.append((spec["id"], df))
    print("store", spec["id"], "rows", len(df), "cache", cached)
st_at, info = dv.apply_price_basis(stores, "as_traded", cache_dir=YAHOO)
print("as_traded stats", {k: v for k, v in (info["stats"] or {}).items() if k != "no_cache"})
prices, _ = dv.security_day_prices(universe, st_at, pc.symbol_claims(universe))
yh = prices["source"].astype(str).map(dv.is_yahoo_source).astype(bool)
S = set(zip(prices.loc[yh, "cusip"].astype(str), prices.loc[yh, "day"].astype("int64")))
print("S' (as_traded store-derived Yahoo points)", len(S))

s3 = boto3.client("s3", region_name="us-east-1")
r = s3.get_object(Bucket="opal-data-assets", Key="commonwealth/cottonwood/silver/account_day_value/date=2026-06-23/part-00000.parquet",
                  VersionId="ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a")
t = pq.read_table(io.BytesIO(r["Body"].read()), columns=["cusip", "date", "close", "price_source", "use_class"]).to_pandas()
t = t[t["close"].notna() & (t["price_source"].astype(str) != "cash-at-par")]
t["day"] = pd.to_datetime(t["date"]).values.astype("datetime64[D]").astype("int64")
X = set(zip(t["cusip"].astype(str), t["day"]))
B = set(zip(t.loc[t["use_class"] != "NOT_YAHOO", "cusip"].astype(str), t.loc[t["use_class"] != "NOT_YAHOO", "day"]))
A = X & S
print("X", len(X), "A'", len(A), "B", len(B), "A'&B", len(A & B), "A'-B", len(A - B), "B-A'", len(B - A))
