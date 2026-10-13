#!/usr/bin/env python3
"""BP-b-3 lot census, ADVI_BDPRCE round 2. Worker 0.9.0_WK_ADVI_BDPRCE~7. READ-ONLY.

Reads:
  s3://opal-data-49financial/advi/49financial/platinum/entities/clients/<seg>/detail.json  (one per client object)
  s3://opal-data-bd/silver/prices/canonical_prices.parquet   (read once into memory)
  s3://opal-data-bd/config/ticker_lookup.json
  s3://opal-data-bd/silver/historical_prices.parquet         (downloaded copy, ticker column only)
Writes:
  C:/dev/wk-bdprce-r2-7-data/lot_extract.csv                 (full extract, outside the checkout)
  deliverables/CENSUS.json and deliverables/lot_extract_sample.csv (in the checkout)

Never printed or written: client_name, account_name, raw account_id, the raw acct_z key suffix (an account number),
and raw client keys (counts only; committed sample and failure refs use a hash). client_name is never read.
Run from the worktree root:  python -I <this file>
"""
import concurrent.futures as cf
import csv
import datetime as dt
import hashlib
import json
import math
import os
import random
import statistics
import sys
import time
from collections import Counter

import boto3
import botocore.config
import numpy as np
import pandas as pd

DATA = "C:/dev/wk-bdprce-r2-7-data"
DELIV = "org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~7"
CL_BUCKET = "opal-data-49financial"
CL_PREFIX = "advi/49financial/platinum/entities/clients/"
BD = "opal-data-bd"
M = 10 ** 6            # key = asset_id * M + day ordinal (days since 1970-01-01)
EPOCH = dt.date(1970, 1, 1)
NEAR_DAYS = 5
PRICE_TOL = 1e-6       # tolerance = PRICE_TOL * max(1, |price|)
MV_ABS_TOL = 0.01
SAMPLE_SEED = 20261013
SAMPLE_N = 200
CALLS = [
    "aws s3api list-objects-v2 --bucket opal-data-49financial --prefix advi/49financial/platinum/entities/clients/ --delimiter /",
    "aws s3api list-objects-v2 --bucket opal-data-49financial --prefix advi/49financial/platinum/entities/clients/ --output json (auto-paginated, full listing)",
    "aws s3api get-object --bucket opal-data-49financial --key advi/49financial/platinum/entities/clients/0/detail.json (structure probe, keys and types only)",
    "aws s3api head-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet",
    "aws s3api head-object --bucket opal-data-bd --key config/ticker_lookup.json",
    "aws s3api head-object --bucket opal-data-bd --key silver/historical_prices.parquet",
    "aws s3api get-object --bucket opal-data-bd --key silver/prices/canonical_prices.parquet (to DATA dir)",
    "aws s3api get-object --bucket opal-data-bd --key config/ticker_lookup.json (to DATA dir)",
    "aws s3api get-object --bucket opal-data-bd --key silver/historical_prices.parquet (to DATA dir)",
    "boto3 s3.get_object Bucket=opal-data-49financial Key=<clients prefix>/<seg>/detail.json, 3510 keys, 16 threads, 4 attempts each",
]
HEADER = ["object_key", "entity_class", "data_as_of", "asset_name", "ticker_served", "current_price", "quantity",
          "market_value", "price_class", "account_ref"]
CLASSES = ["PRICED_FROM_CANONICAL", "PRICED_OFF_NO_CANONICAL", "NOT_UNTICKERED"]


def log(msg):
    print(msg, flush=True)


def sha12(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def untickered(t):
    """A served ticker that is null, empty or UNKNOWN (case-insensitive, whitespace-trimmed)."""
    if t is None:
        return True
    if not isinstance(t, str):
        try:
            if pd.isna(t):
                return True
        except (TypeError, ValueError):
            pass
        t = str(t)
    s = t.strip()
    return s == "" or s.upper() == "UNKNOWN"


def key_seg(key):
    return key[len(CL_PREFIX):].split("/")[0]


def key_class(seg):
    if seg == "0":
        return "catch_all"
    if seg.startswith("acct_z"):
        return "acct_z"
    if seg.startswith("z0"):
        return "z0"
    return "other"


def masked_path(seg):
    """Path under the clients prefix. acct_z suffix is an account number: hashed everywhere it is written."""
    if seg.startswith("acct_z"):
        return "acct_z#" + sha12(seg[len("acct_z"):]) + "/detail.json"
    return seg + "/detail.json"


def sample_path(seg):
    """Committed sample: every client key hashed (counts-and-hash discipline)."""
    return "obj#" + sha12(seg) + "/detail.json"


# ---------------------------------------------------------------- price and ticker sources
def load_canonical():
    cp = pd.read_parquet(f"{DATA}/canonical_prices.parquet", columns=["date", "asset_name", "ticker", "price"])
    rows_raw = len(cp)
    cp = cp[cp["date"].notna() & cp["price"].notna()].copy()
    cp["asset_name"] = cp["asset_name"].fillna("")
    tk = cp["ticker"].fillna("").astype(str).str.strip().str.upper()
    tk_ok = ((tk != "") & (tk != "UNKNOWN")).to_numpy()
    d = pd.to_datetime(cp["date"]).dt.normalize()
    day = (d - pd.Timestamp("1970-01-01")).dt.days.to_numpy(dtype=np.int64)
    cat = pd.Categorical(cp["asset_name"])
    aid = np.asarray(cat.codes, dtype=np.int64)
    names = [str(x) for x in cat.categories]
    price = cp["price"].to_numpy(dtype=np.float64)
    key = aid * M + day
    order = np.argsort(key, kind="stable")
    info = {
        "rows_raw": rows_raw,
        "rows_used": int(len(cp)),
        "assets": len(names),
        "rows_with_ticker": int(tk_ok.sum()),
        "assets_with_canonical_ticker": set(names[i] for i in np.unique(aid[tk_ok])),
        "name_to_id": {n: i for i, n in enumerate(names)},
        "k": key[order],
        "p": price[order],
    }
    del cp, tk, d, day, cat, aid, price, key, order
    return info


def load_ticker_lookup():
    with open(f"{DATA}/ticker_lookup.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
    mapping = {}
    for rec in data:
        name = rec.get("asset_name")
        t = rec.get("ticker")
        if not name or untickered(t):
            continue
        mapping.setdefault(str(name), set()).add(str(t).strip())
    return len(data), mapping


def load_historical_tickers():
    hp = pd.read_parquet(f"{DATA}/historical_prices.parquet", columns=["ticker"])
    tks = set(str(x).strip() for x in hp["ticker"].dropna().unique())
    return len(hp), tks


# ---------------------------------------------------------------- canonical lookups
def exact_match(C, a, dday, p):
    k = a * M + dday
    lo = int(np.searchsorted(C["k"], k, "left"))
    hi = int(np.searchsorted(C["k"], k, "right"))
    if hi <= lo:
        return False
    pr = C["p"][lo:hi]
    return bool(np.any(np.abs(pr - p) <= PRICE_TOL * np.maximum(1.0, np.abs(pr))))


def nearest_within(C, a, dday, p):
    lo = int(np.searchsorted(C["k"], a * M + dday - NEAR_DAYS, "left"))
    hi = int(np.searchsorted(C["k"], a * M + dday + NEAR_DAYS, "right"))
    if hi <= lo:
        return None
    days = C["k"][lo:hi] - a * M
    pr = C["p"][lo:hi]
    dist = np.abs(days - dday)
    dmin = int(dist.min())
    cand = pr[dist == dmin]
    gap_best = float(np.min(np.abs(cand - p)))
    return dmin, gap_best


def any_date_match(C, a, dday, p):
    """None if the asset has no canonical rows; else (equal_any, min |day offset| of an equal price)."""
    lo = int(np.searchsorted(C["k"], a * M, "left"))
    hi = int(np.searchsorted(C["k"], (a + 1) * M, "left"))
    if hi <= lo:
        return None
    pr = C["p"][lo:hi]
    days = C["k"][lo:hi] - a * M
    m = np.abs(pr - p) <= PRICE_TOL * np.maximum(1.0, np.abs(pr))
    if not m.any():
        return False, None
    return True, int(np.min(np.abs(days[m] - dday)))


# ---------------------------------------------------------------- objects
def fetch(s3, key):
    last = None
    for attempt in range(4):
        try:
            return s3.get_object(Bucket=CL_BUCKET, Key=key)["Body"].read()
        except Exception as e:  # noqa: BLE001 -- recorded, never silent
            last = getattr(e, "response", {}).get("Error", {}).get("Code", type(e).__name__)
            if last == "NoSuchKey":
                break
            time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(str(last))


def parse(body):
    o = json.loads(body)          # client_name is parsed but never read or printed
    as_of = o.get("data_as_of")
    tax = o.get("tax") or {}
    raw = tax.get("open_lots")
    lots = []
    for lot in raw or []:
        acct = lot.get("account_id")
        lots.append((
            "" if acct is None else str(acct),
            lot.get("asset_name"),
            lot.get("ticker"),
            lot.get("quantity"),
            lot.get("current_price"),
            lot.get("market_value"),
        ))
    return {"as_of": as_of, "lots": lots, "has_lots_field": raw is not None}


def read_one(s3, key):
    try:
        return key, parse(fetch(s3, key)), None
    except Exception as e:  # noqa: BLE001
        return key, None, str(e)[:80]


def num(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def main():
    t0 = time.time()
    read_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(DELIV, exist_ok=True)
    s3 = boto3.session.Session().client(
        "s3", config=botocore.config.Config(max_pool_connections=32, retries={"max_attempts": 5, "mode": "standard"}))

    # 1. list the client detail objects (one per client folder)
    keys = []
    pg = s3.get_paginator("list_objects_v2")
    for page in pg.paginate(Bucket=CL_BUCKET, Prefix=CL_PREFIX):
        for o in page.get("Contents", []):
            k = o["Key"]
            if k.endswith("/detail.json") and k[len(CL_PREFIX):].count("/") == 1:
                keys.append(k)
    keys.sort()
    objects_total = len(keys)
    log(f"LIST detail.json objects={objects_total}")
    cls_obj = Counter(key_class(key_seg(k)) for k in keys)
    log(f"LIST by_entity_class={dict(cls_obj)}")

    # 2. canonical, ticker sources
    C = load_canonical()
    log(f"CANON rows_raw={C['rows_raw']} rows_used={C['rows_used']} assets={C['assets']} "
        f"rows_with_ticker={C['rows_with_ticker']}")
    tl_n, tl_map = load_ticker_lookup()
    log(f"TICKER_LOOKUP entries={tl_n} names_with_ticker={len(tl_map)}")
    hp_rows, hp_tickers = load_historical_tickers()
    log(f"HISTORICAL rows={hp_rows} distinct_tickers={len(hp_tickers)} (no asset_name column)")

    # 3. read objects, 16 threads, retries, failures recorded
    ok = {}
    failed = []
    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        futs = [ex.submit(read_one, s3, k) for k in keys]
        n_done = 0
        for fu in cf.as_completed(futs):
            key, parsed, err = fu.result()
            n_done += 1
            if parsed is None:
                failed.append({"ref": "obj:" + sha12(key_seg(key)), "error": err})
            else:
                ok[key] = parsed
            if n_done % 500 == 0:
                log(f"READ progress {n_done}/{objects_total} failed={len(failed)} elapsed={int(time.time()-t0)}s")
    log(f"READ objects_read={len(ok)} of {objects_total} failed={len(failed)} elapsed={int(time.time()-t0)}s")

    # 4. classify every lot, write the extract
    os.makedirs(DATA, exist_ok=True)
    ext_path = f"{DATA}/lot_extract.csv"
    cls_lot = Counter()
    by_entity = Counter()
    date_dist = Counter()
    lots_total = 0
    untick_lots = 0
    untick_name_count = Counter()
    off_equal = 0
    off_none = 0
    off_asset_absent = 0
    off_no_price = 0
    off_no_asof = 0
    gaps = []
    no_near = 0
    near_off_hist = Counter()
    match_off_hist = Counter()
    off_asset_hist = Counter()
    mv_checked = 0
    mv_off = 0
    mv_off_1pct = 0
    mv_rel = []
    listed_assets = set()
    listed_lots = 0

    def bucket(d):
        if d is None:
            return "none"
        if d <= 5:
            return str(d)
        return ">5"

    with open(ext_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        for key in sorted(ok):
            parsed = ok[key]
            seg = key_seg(key)
            cls = key_class(seg)
            by_entity[cls] += 1
            as_of = parsed["as_of"]
            as_of_s = "" if as_of is None else str(as_of)[:10]
            date_dist[as_of_s if as_of_s else "<missing>"] += 1
            dday = None
            try:
                dday = (dt.date.fromisoformat(as_of_s) - EPOCH).days
            except ValueError:
                dday = None
            obj_path = masked_path(seg)
            for (acct, name_raw, tk_raw, q_raw, p_raw, mv_raw) in parsed["lots"]:
                lots_total += 1
                name = "" if name_raw is None else str(name_raw)
                q = num(q_raw)
                p = num(p_raw)
                mv = num(mv_raw)
                if q is not None and p is not None and mv is not None:
                    mv_checked += 1
                    diff = abs(mv - q * p)
                    tol = max(MV_ABS_TOL, PRICE_TOL * abs(mv))
                    if diff > tol:
                        mv_off += 1
                        if diff > 0.01 * max(abs(mv), 1e-9):
                            mv_off_1pct += 1
                        if abs(mv) > 0:
                            mv_rel.append(diff / abs(mv))
                if not untickered(tk_raw):
                    pclass = "NOT_UNTICKERED"
                    ticker_served = str(tk_raw).strip()
                else:
                    untick_lots += 1
                    untick_name_count[name] += 1
                    ticker_served = "" if tk_raw is None else str(tk_raw)
                    a = C["name_to_id"].get(name)
                    if a is not None and dday is not None and p is not None and exact_match(C, a, dday, p):
                        pclass = "PRICED_FROM_CANONICAL"
                    else:
                        pclass = "PRICED_OFF_NO_CANONICAL"
                        if a is None:
                            off_asset_absent += 1
                            off_none += 1
                        elif p is None:
                            off_no_price += 1
                            off_none += 1
                        else:
                            if dday is None:
                                off_no_asof += 1
                            nw = nearest_within(C, a, dday, p) if dday is not None else None
                            if nw is None:
                                no_near += 1
                                near_off_hist["none"] += 1
                            else:
                                near_off_hist[bucket(nw[0])] += 1
                                gaps.append(nw[1])
                            am = any_date_match(C, a, dday, p) if dday is not None else None
                            if am is None:
                                off_none += 1
                            elif am[0]:
                                off_equal += 1
                                match_off_hist[bucket(am[1])] += 1
                            else:
                                off_none += 1
                        # the asset-level stratum of off lots (names of assets only, no account data)
                        off_asset_hist["asset_has_canonical_rows" if a is not None else "asset_absent"] += 1
                    if name in tl_map or name in C["assets_with_canonical_ticker"]:
                        listed_assets.add(name)
                        listed_lots += 1
                cls_lot[pclass] += 1
                acct_ref = sha12(acct) if acct else ""
                w.writerow([obj_path, cls, as_of_s, name, ticker_served,
                            "" if p_raw is None else p_raw, "" if q_raw is None else q_raw,
                            "" if mv_raw is None else mv_raw, pclass, acct_ref])
    # the untickered-lot count among listed assets: names in the listing are sorted; count lots of listed assets
    listed_untick_lots = sum(untick_name_count[n] for n in listed_assets)
    extract_rows = lots_total
    with open(ext_path, "rb") as fh:
        ext_sha = hashlib.sha256(fh.read()).hexdigest()
    log(f"CLASSIFY lots_total={lots_total} classes={dict(cls_lot)} untickered={untick_lots}")
    log(f"EXTRACT rows={extract_rows} sha256={ext_sha}")

    # 5. committed sample: stratified, seeded, client keys hashed
    rng = random.Random(SAMPLE_SEED)
    rows = []
    with open(ext_path, "r", newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        for i, row in enumerate(rd):
            rows.append((i, row[8]))
    by_cls = {c: [i for i, pc in rows if pc == c] for c in CLASSES}
    n_off = min(100, len(by_cls["PRICED_OFF_NO_CANONICAL"]))
    n_nu = min(50, len(by_cls["NOT_UNTICKERED"]))
    n_fc = SAMPLE_N - n_off - n_nu
    picks = (rng.sample(by_cls["PRICED_OFF_NO_CANONICAL"], n_off)
             + rng.sample(by_cls["NOT_UNTICKERED"], n_nu)
             + rng.sample(by_cls["PRICED_FROM_CANONICAL"], min(n_fc, len(by_cls["PRICED_FROM_CANONICAL"]))))
    picks = sorted(picks)
    sample_rel = os.path.join(DELIV, "lot_extract_sample.csv")
    with open(ext_path, "r", newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        hdr = next(rd)
        want = set(picks)
        out_rows = []
        for i, row in enumerate(rd):
            if i in want:
                seg_path = row[0]
                if not seg_path.startswith("acct_z#"):
                    seg_path = "obj#" + sha12(seg_path.split("/")[0]) + "/detail.json"
                row[0] = seg_path
                out_rows.append(row)
    with open(sample_rel, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(hdr)
        w.writerows(out_rows)
    log(f"SAMPLE rows={len(out_rows)} off={n_off} not_untickered={n_nu} from_canon={min(n_fc, len(by_cls['PRICED_FROM_CANONICAL']))} seed={SAMPLE_SEED}")

    # 6. the record
    mv_rel.sort()
    census = {
        "order": "BP-b-3",
        "read_at": read_at,
        "claim": "measured" if not failed else "absent",
        "calls": CALLS,
        "objects_total": objects_total,
        "objects_read": len(ok),
        "objects_failed": failed,
        "lots_total": lots_total,
        "classes": {
            "PRICED_FROM_CANONICAL": cls_lot["PRICED_FROM_CANONICAL"],
            "PRICED_OFF_NO_CANONICAL": cls_lot["PRICED_OFF_NO_CANONICAL"],
            "NOT_UNTICKERED": cls_lot["NOT_UNTICKERED"],
        },
        "by_entity_class": {
            "catch_all": by_entity["catch_all"],
            "acct_z": by_entity["acct_z"],
            "z0": by_entity["z0"],
            "other": by_entity["other"],
        },
        "listed_untickered": {
            "count": len(listed_assets),
            "lots": listed_untick_lots,
            "assets": sorted(listed_assets),
            "method": "untickered asset name present in config/ticker_lookup.json with a non-UNKNOWN ticker, "
                      "OR in canonical rows carrying a non-empty non-UNKNOWN ticker",
            "condition3": "UNEVALUABLE: silver/historical_prices.parquet has no asset_name column (columns: date, ticker, close, fetch_date, source); "
                          "the name-to-ticker test cannot be run against it",
        },
        "off_canonical_detail": {
            "equals_some_canonical_price": off_equal,
            "equals_none": off_none,
            "median_abs_gap_to_nearest": round(statistics.median(gaps), 6) if gaps else 0.0,
            "nearest_within_5d": len(gaps),
            "no_nearest_within_5d": no_near,
            "asset_absent_from_canonical": off_asset_absent,
            "no_price": off_no_price,
            "no_as_of": off_no_asof,
            "nearest_offset_days": dict(sorted(near_off_hist.items())),
            "equal_price_offset_days": dict(sorted(match_off_hist.items())),
        },
        "market_value_identity": {
            "lots_checked": mv_checked,
            "lots_off_quantity_times_price": mv_off,
            "tolerance": "max(0.01, 1e-6*abs(market_value))",
            "lots_off_over_1pct": mv_off_1pct,
            "median_rel_diff_of_off_lots": round(statistics.median(mv_rel), 6) if mv_rel else 0.0,
        },
        "data_as_of_distribution": dict(sorted(date_dist.items())),
        "untickered_lots": untick_lots,
        "sources": {
            "canonical_rows_raw": C["rows_raw"],
            "canonical_rows_used": C["rows_used"],
            "canonical_assets": C["assets"],
            "canonical_rows_with_ticker": C["rows_with_ticker"],
            "ticker_lookup_entries": tl_n,
            "historical_rows": hp_rows,
            "historical_distinct_tickers": len(hp_tickers),
        },
        "extract_file": ext_path,
        "extract_sha256": ext_sha,
        "extract_rows": extract_rows,
        "sample_file": sample_rel.replace(os.sep, "/"),
        "sample_rows": len(out_rows),
        "elapsed_s": int(time.time() - t0),
    }
    with open(os.path.join(DELIV, "CENSUS.json"), "w", encoding="utf-8") as fh:
        json.dump(census, fh, indent=2, sort_keys=False)
        fh.write("\n")
    log("CENSUS.json written")
    log(f"DONE objects_read={len(ok)}/{objects_total} lots={lots_total} classes={census['classes']} "
        f"listed_untickered={len(listed_assets)} assets / {listed_untick_lots} lots mv_off={mv_off}/{mv_checked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
