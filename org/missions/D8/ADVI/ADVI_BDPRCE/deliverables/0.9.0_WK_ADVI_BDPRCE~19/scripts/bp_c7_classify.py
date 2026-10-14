#!/usr/bin/env python3
"""BP-c-7 classify, ADVI_BDPRCE round 3. Worker 0.9.0_WK_ADVI_BDPRCE~19. READ-ONLY (no S3 call here).

Input 1: the round-2 extract, C:/dev/wk-bdprce-r2-7-data/lot_extract.csv (sha256 checked against CENSUS.json).
Input 2: the per-version projections written by bp_c7_fetch.py (C:/dev/wk-bdprce-r3-19-data/proj/).
Input 3: the canonical version listing, C:/dev/wk-bdprce-r3-19-data/canon_versions.json (IsLatest per version).

Classification, per DISTINCT (asset_name, current_price, data_as_of) triple, first match wins:
  1 EQUALS_OLDER_CANONICAL_VERSION  a canonical row for the asset, in a canonical version that is NOT the latest
                                    listed version, equal to the served price (any row date).
  2 EQUALS_DAILY_FILE_ROW           a row for the asset in any version of any silver/prices/<date>.parquet, equal.
  3 EQUALS_NAMED_OTHER_SOURCE       assigned only by named_checks() (currently none; see OFFCANON.md).
  4 UNEXPLAINED                     none of the above.
Equality: |row_price - served| <= 1e-6 * max(1, |served|), the census tolerance.
Side outputs (outside the checkout): C:/dev/wk-bdprce-r3-19-data/classified/triples.csv, lots_classified.csv.
Run from the worktree root:  python -I <this file>
"""
import glob
import hashlib
import json
import os
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd

DATA = "C:/dev/wk-bdprce-r3-19-data"
R2 = "C:/dev/wk-bdprce-r2-7-data"
EXTRACT = f"{R2}/lot_extract.csv"
EXPECT_SHA = "e7e618d76516c8b7977179aefb3f77ce4fc13c17fbcf1dbeb92001a6e0a2b50b"
TOL = 1e-6
CLASSES = ["EQUALS_OLDER_CANONICAL_VERSION", "EQUALS_DAILY_FILE_ROW", "EQUALS_NAMED_OTHER_SOURCE", "UNEXPLAINED"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_lots():
    got = sha256_file(EXTRACT)
    if got != EXPECT_SHA:
        print(f"ERROR: extract sha256 {got} != expected {EXPECT_SHA}")
        sys.exit(2)
    df = pd.read_csv(EXTRACT, dtype=str, keep_default_na=False)
    return df[df["price_class"] == "PRICED_OFF_NO_CANONICAL"].copy()


def kind_of(name):
    """Name-pattern kind, a diagnostic label (the extract carries no asset type)."""
    n = name.upper()
    if re.search(r"\bETF\b", n):
        return "ETF"
    if re.search(r"\bETN\b", n):
        return "ETN"
    if re.search(r"BOND|INCOME|MUNI|MUNICIPAL|HIGH YIELD|TREASURY|DURATION|TAX FREE|TAX-FREE|CREDIT|INTERMEDIATE", n):
        return "BOND_OR_INCOME_FUND"
    return "OTHER_FUND_OR_SECURITY"


def match_projections(triples):
    """Vectorized match of each triple against each projected file. Returns (canon_hits, daily_hits) frames."""
    latest = {v["VersionId"] for v in json.load(open(f"{DATA}/canon_versions.json"))["Versions"] if v["IsLatest"]}
    tri = triples[["tkey", "asset_name", "served_price"]]
    canon_parts, daily_parts, n_files = [], [], 0
    for path in sorted(glob.glob(f"{DATA}/proj/*.parquet")):
        base = os.path.basename(path)
        df = pd.read_parquet(path, columns=["date", "asset_name", "price", "source", "version_id", "last_modified"])
        n_files += 1
        if df.empty:
            continue
        m = df.merge(tri, on="asset_name", how="inner")
        if m.empty:
            continue
        ok = (m["price"] - m["served_price"]).abs() <= TOL * np.maximum(1.0, m["served_price"].abs())
        m = m[ok]
        if m.empty:
            continue
        m = m.assign(row_date=m["date"].astype(str).str[:10], file=base)
        if base.startswith("canon_"):
            m = m.assign(is_latest=m["version_id"].isin(latest))
            canon_parts.append(m[["tkey", "asset_name", "served_price", "row_date", "price", "source", "version_id",
                                  "last_modified", "is_latest", "file"]])
        elif base.startswith("daily_"):
            fkey = re.match(r"daily_(\d{4}-\d{2}-\d{2})_", base).group(1)
            m = m.assign(file_key=fkey)
            daily_parts.append(m[["tkey", "asset_name", "served_price", "row_date", "price", "source", "version_id",
                                  "file_key", "file"]])
    canon = pd.concat(canon_parts, ignore_index=True) if canon_parts else pd.DataFrame()
    daily = pd.concat(daily_parts, ignore_index=True) if daily_parts else pd.DataFrame()
    print(f"OK: projected files read={n_files} canonical match rows={len(canon)} daily match rows={len(daily)}")
    return canon, daily


def main():
    lots = load_lots()
    print(f"OK: extract sha256 matched; PRICED_OFF_NO_CANONICAL lots={len(lots)}")
    lots = lots.assign(served_price=pd.to_numeric(lots["current_price"], errors="coerce"))
    # A served price of the literal string "nan" is NOT a price: it keys a triple that can match nothing.
    tri = (lots[["asset_name", "current_price", "served_price", "data_as_of"]].drop_duplicates()
           .reset_index(drop=True))
    tri["tkey"] = [f"T{i:03d}" for i in range(len(tri))]
    tri["no_price"] = tri["served_price"].isna()
    print(f"OK: triples with no served price (literal nan)={int(tri['no_price'].sum())}")
    print(f"OK: distinct triples={len(tri)} distinct assets={tri['asset_name'].nunique()}")
    canon, daily = match_projections(tri)

    res = {}
    for r in tri.itertuples(index=False):
        c = canon[canon["tkey"] == r.tkey] if len(canon) else canon
        d = daily[daily["tkey"] == r.tkey] if len(daily) else daily
        older = c[~c["is_latest"]] if len(c) else c
        latest_only = c[c["is_latest"]] if len(c) else c
        if len(older):
            cls = "EQUALS_OLDER_CANONICAL_VERSION"
        elif len(d):
            cls = "EQUALS_DAILY_FILE_ROW"
        else:
            cls = "UNEXPLAINED"
        res[r.tkey] = {"class": cls, "older": older, "latest_only": latest_only, "daily": d, "named": ""}

    res = named_checks(tri, res)

    cnt = Counter(v["class"] for v in res.values())
    print("TRIPLE COUNTS", {k: cnt.get(k, 0) for k in CLASSES}, "total", len(res))
    os.makedirs(f"{DATA}/classified", exist_ok=True)
    rows = []
    for r in tri.itertuples(index=False):
        v = res[r.tkey]
        older, d = v["older"], v["daily"]
        rows.append({
            "asset_name": r.asset_name, "served_price": f"{r.served_price:.10g}", "data_as_of": r.data_as_of,
            "class": v["class"], "n_older_rows": len(older),
            "older_versions": older["version_id"].nunique() if len(older) else 0,
            "n_latest_only_rows": len(v["latest_only"]), "n_daily_rows": len(d),
            "first_older_hit": (f"{older.sort_values('last_modified').iloc[0]['version_id']}@"
                                f"{older.sort_values('last_modified').iloc[0]['last_modified']} "
                                f"row_date={older.sort_values('last_modified').iloc[0]['row_date']} "
                                f"source={older.sort_values('last_modified').iloc[0]['source']}") if len(older) else "",
            "first_daily_hit": (f"{d.sort_values(['file_key', 'version_id']).iloc[0]['file']} "
                                f"row_date={d.sort_values(['file_key', 'version_id']).iloc[0]['row_date']} "
                                f"source={d.sort_values(['file_key', 'version_id']).iloc[0]['source']}") if len(d) else "",
            "named": v["named"],
        })
    tdf = pd.DataFrame(rows)
    tdf.to_csv(f"{DATA}/classified/triples.csv", index=False)

    # lot level
    lot_rows = []
    tkey_of = {(r.asset_name, r.current_price, r.data_as_of): r.tkey for r in tri.itertuples(index=False)}
    for r in lots.itertuples(index=False):
        tk = tkey_of[(r.asset_name, r.current_price, r.data_as_of)]
        v = res[tk]
        if v["class"] == "EQUALS_OLDER_CANONICAL_VERSION":
            h = v["older"].sort_values("last_modified").iloc[0]
            ev = f"canon:{h['version_id']}:row_date={h['row_date']}"
        elif v["class"] == "EQUALS_DAILY_FILE_ROW":
            h = v["daily"].sort_values(["file_key", "version_id"]).iloc[0]
            ev = f"daily:{h['file_key']}:{h['version_id']}:row_date={h['row_date']}"
        elif v["class"] == "EQUALS_NAMED_OTHER_SOURCE":
            ev = f"named:{v['named']}"
        else:
            ev = "NONE"
        lot_rows.append({
            "object_key": r.object_key, "entity_class": r.entity_class, "asset_name": r.asset_name,
            "served_price": r.current_price, "data_as_of": r.data_as_of, "class": v["class"], "evidence": ev,
            "kind": kind_of(r.asset_name), "account_ref": r.account_ref,
        })
    lc = Counter(x["class"] for x in lot_rows)
    print("LOT COUNTS", {k: lc.get(k, 0) for k in CLASSES}, "total", len(lot_rows))
    pd.DataFrame(lot_rows).to_csv(f"{DATA}/classified/lots_classified.csv", index=False)
    return 0


NAMED_RPS = ("schwab/silver/rps/date=20260723/data.parquet closing_price, account+price match "
             "(mapping gold/dimensions/schwab_bd_account_mapping.parquet; B_01.holdings_lots.py:2215-2276 "
             "_apply_rps_price_override and :690-705 price lookup); negative control 0 of 305")


def named_checks(tri, res):
    """Class 3: a triple left UNEXPLAINED by the canonical and daily passes is EQUALS_NAMED_OTHER_SOURCE when
    bp_c7_named_rps.py finds a same-day Schwab RPS closing price (account + exact price, or x100 for bond
    percent-of-par) for an account holding the lot. The check is run separately and writes named_rps.json."""
    path = f"{DATA}/classified/named_rps.json"
    if not os.path.exists(path):
        return res
    named = json.load(open(path))
    hit = {(m["asset_name"], m["served_price"], m["data_as_of"]) for m in named["matches"]}
    n = 0
    for r in tri.itertuples(index=False):
        v = res[r.tkey]
        if v["class"] == "UNEXPLAINED" and (r.asset_name, r.current_price, r.data_as_of) in hit:
            v["class"] = "EQUALS_NAMED_OTHER_SOURCE"
            v["named"] = NAMED_RPS
            n += 1
    print(f"OK: named RPS class applied to {n} triples")
    return res


if __name__ == "__main__":
    sys.exit(main())
