"""ETFS_RIVALS -- which DAY do the closes of each gold security_market object belong to? (CTO ruling msg 31477, ask 1;
BLOCKING for FWD-24.) Read-only.

    python g4_date_offset_read.py <code root> <out json>

For every object of the table: (1) its own `as_of` and `date` columns against its partition date; (2) for each security
stored in USD that a fund holds, its `px_close` against the funds' own valuation price (market_value / quantity, gold
canonical_shape) on the report dated the partition date and on the reports one and two trading reports either side.
A close "matches" a day when it is within 0.2 percent of a fund's valuation price that day. Per object the count of
closes matching each offset is printed, and the count matching ONLY one offset (a price unchanged across two days
matches both and decides nothing). Non-USD listings are left out: a fund's valuation is in dollars.
Limit: a fund may value a holding at a price other than the listing's close (an ADR, a stale price); the offsets are
read as a distribution, not per security."""
import collections
import io
import json
import pathlib
import sys

import pandas as pd

ROOT = pathlib.Path(sys.argv[1]).resolve()
OUT = sys.argv[2]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))
sys.path.insert(1, str(ROOT))
from rivalfunds import gold_holding_contribution as hc, homes, sinks  # noqa: E402

TOL = 0.002
s = sinks.S3Sink()
pre = homes.address("rivalfunds", "etfs", "gold", "security_market", "x")[:-1]
objs = sorted(u for u in s.list(pre) if u.endswith(".parquet"))
g1u = hc._newest_by_date(s, homes.canonical_shape(""), "2026-09-15", "2026-10-07")
g1 = hc._read(s, g1u, hc.G1_COLUMNS)
g1 = g1[(g1["quantity"].fillna(0) > 0) & g1["market_value"].notna() & g1["security_id"].notna()]
g1 = g1.assign(d=g1["report_date"].astype(str).str[:10], p=g1["market_value"] / g1["quantity"])
val = collections.defaultdict(list)  # (security, date) -> valuation prices across funds
for r in g1.itertuples():
    val[(str(r.security_id), r.d)].append(float(r.p))
rdates = sorted(g1u)
rec = {"tolerance": TOL, "report_dates": rdates, "objects": []}
print("fund report dates:", rdates)
for u in objs:
    part = u.split("date=")[1][:10]
    name = u.rsplit("/", 1)[-1]
    df = pd.read_parquet(io.BytesIO(s.get(u)))
    as_of = df["as_of"].astype(str).str[:10].value_counts().to_dict() if "as_of" in df.columns else {}
    dcol = df["date"].astype(str).str[:10].value_counts().to_dict() if "date" in df.columns else {}
    src = sorted(df["source"].astype(str).str[:28].unique().tolist()) if "source" in df.columns else []
    usd = df[(df["currency"].astype(str) == "USD") & df["px_close"].notna()] if "currency" in df.columns else df.iloc[0:0]
    i = rdates.index(part) if part in rdates else None
    offs = {k: rdates[i + k] for k in (-2, -1, 0, 1, 2) if i is not None and 0 <= i + k < len(rdates)}
    hit, only, compared = collections.Counter(), collections.Counter(), 0
    for r in usd.itertuples():
        m = [k for k, d in offs.items() if any(abs(float(r.px_close) / v - 1.0) <= TOL for v in val.get((str(r.security_id), d), []) if v)]
        if any(val.get((str(r.security_id), d)) for d in offs.values()):
            compared += 1
        for k in m:
            hit[k] += 1
        if len(m) == 1:
            only[m[0]] += 1
        if not m and any(val.get((str(r.security_id), d)) for d in offs.values()):
            hit["none"] += 1
    o = {"partition": part, "object": name, "rows": len(df), "closes": int(df["px_close"].notna().sum()) if "px_close" in df.columns else 0,
         "source": src, "as_of_column": as_of, "date_column": dcol, "usd_closes_held_by_a_fund": compared,
         "offset_dates": offs, "matches_by_offset": {str(k): hit[k] for k in (-2, -1, 0, 1, 2, "none")},
         "matches_only_one_offset": {str(k): only[k] for k in (-2, -1, 0, 1, 2)}}
    rec["objects"].append(o)
    print(f"{part} {name[:38]:<38} rows {len(df):>4} closes {o['closes']:>4} | as_of {as_of} | date col {dcol} | {src}")
    print(f"      USD closes a fund holds: {compared:>4} | match by offset {o['matches_by_offset']} | ONLY that offset {o['matches_only_one_offset']} | offsets {offs}")
json.dump(rec, open(OUT, "w", encoding="utf-8"), indent=1)
