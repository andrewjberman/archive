"""ADVI_COTBKF round 103 (issuer 2.0.0_SA_COO~C1): coverage of the served UNPRICED holding-days by the TICKER-KEYED Bloomberg stores.

CB-cy-1's worker measured the CUSIP-keyed primary store (0 covered) and recorded that coverage through the two ticker-keyed stores was not measured. This script
measures it, read-only, counts only, no Bloomberg call, no write:
  stores:  opal-data-etfs bbg/ (parquet with columns security, date, PX_LAST; security looks like 'AAPL US Equity')
           opal-data-harvest bloomberg/harvest/bronze/price_history_px_last/ (json: series {label: [[date, px], ...]}; label looks like '1299 HK')
  mapping: a store label maps to a universe security when its first token (upper case, norm_key) equals exactly one security's ticker symbol in the
           transactions universe (dv.universe_from_tx); a ticker claimed by more than one security, or by none, is not mapped (both counted).
  join:    (mapped cusip, calendar date) against the served account_day_value rows with a null close and a null blank_reason (pinned VersionId).
Prints  TICKER-COVERAGE labels=<n> mapped_unique=<m> ambiguous=<a> unmapped=<u> points=<p> mapped_points=<q> unpriced_cusips_covered=<k> unpriced_rows_covered=<r> unpriced_rows=<N>
No cusip, ticker, account or value is printed. Needs AWS read credentials and the received transactions cache.
Result of the run (2026-10-16 ~10:00Z, one minute): TICKER-COVERAGE labels=283 mapped_unique=168 ambiguous=11 unmapped=104 points=36681 mapped_points=16281
unpriced_cusips_covered=4 unpriced_rows_covered=1960 unpriced_rows=15973399.
"""
import io
import json
import sys

import boto3
import pyarrow.parquet as pq

sys.path.insert(0, "C:/Dev/ajb_workspace/data/assets/scripts/silver")
sys.path.insert(0, "C:/Dev/ajb_workspace/data/assets/scripts/analysis")
sys.path.insert(0, "C:/Dev/ajb_workspace/lib")
import commonwealth_daily_holdings as dh  # noqa: E402
import commonwealth_daily_valuation as dv  # noqa: E402
import commonwealth_price_census as pc  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")


def keys(bucket, prefix):
    return [o["Key"] for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix) for o in pg.get("Contents", [])]


tx, _pos = dh.load_tx_pos("C:/Dev/ajb_workspace/.scratch/advi_cotbkf/cache")
claims = {}
for u in dv.universe_from_tx(tx):
    for s in u["symbols"]:
        claims.setdefault(pc.norm_key(s), set()).add(u["cusip"])

points = []  # (label_token, date, px)
labels = set()
for k in keys("opal-data-etfs", "bbg/"):
    if not k.endswith(".parquet"):
        continue
    t = pq.read_table(io.BytesIO(s3.get_object(Bucket="opal-data-etfs", Key=k)["Body"].read()))
    if "PX_LAST" not in t.column_names or "date" not in t.column_names or "security" not in t.column_names:
        continue
    d = t.select(["security", "date", "PX_LAST"]).to_pandas().dropna(subset=["PX_LAST"])
    d = d[d["PX_LAST"] > 0]
    for sec, dt, px in zip(d["security"].astype(str), d["date"].astype(str).str.slice(0, 10), d["PX_LAST"]):
        labels.add(sec)
        points.append((sec, dt))
for k in keys("opal-data-harvest", "bloomberg/harvest/bronze/price_history_px_last/"):
    if not k.endswith(".json"):
        continue
    j = json.loads(s3.get_object(Bucket="opal-data-harvest", Key=k)["Body"].read())
    for lab, rows in (j.get("series") or {}).items():
        for r in rows:
            if r and r[1] is not None and r[1] > 0:
                labels.add(lab)
                points.append((lab, str(r[0])[:10]))

mapped, ambiguous, unmapped = {}, set(), set()
for lab in labels:
    tok = pc.norm_key(lab.split(" ")[0])
    c = claims.get(tok, set())
    if len(c) == 1:
        mapped[lab] = next(iter(c))
    elif len(c) > 1:
        ambiguous.add(lab)
    else:
        unmapped.add(lab)
pts = {(mapped[lab], dt) for lab, dt in points if lab in mapped}

body = s3.get_object(Bucket="opal-data-assets", Key="commonwealth/cottonwood/silver/account_day_value/date=2026-06-23/part-00000.parquet",
                     VersionId="ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a")["Body"].read()
av = pq.read_table(io.BytesIO(body), columns=["cusip", "date", "close", "blank_reason"]).to_pandas()
un = av[av["close"].isna() & av["blank_reason"].isna()]
hit = [(c.strip(), d) in pts for c, d in zip(un["cusip"].astype(str), un["date"].astype(str).str.slice(0, 10))]
cov = un[hit]
print("TICKER-COVERAGE labels=%d mapped_unique=%d ambiguous=%d unmapped=%d points=%d mapped_points=%d unpriced_cusips_covered=%d unpriced_rows_covered=%d unpriced_rows=%d"
      % (len(labels), len(mapped), len(ambiguous), len(unmapped), len(set(points)), len(pts), cov["cusip"].astype(str).nunique(), len(cov), len(un)))
