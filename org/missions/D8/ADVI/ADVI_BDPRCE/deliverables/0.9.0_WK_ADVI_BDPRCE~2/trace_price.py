#!/usr/bin/env python3
"""trace_price.py -- ADVI_BDPRCE BP-a-2: trace one served Financial price to its rule and its trade ids.

READ-ONLY. Reads, in memory and through boto3 get_object / list_objects_v2 only:
  silver/prices/<date>.parquet, silver/prices/canonical_prices.parquet,
  silver/transactions/<date>.parquet, silver/historical_prices.parquet   (bucket opal-data-bd).
Writes nothing except the --out file. No download, no producer run, no lot read.

It reproduces the pipeline AS WRITTEN AT HEAD, bugs included:
  data/black_diamond/scripts/silver/bd_price_update.py
    build_target_date_rows :416-471 (scoped override -> yahoo -> transaction_observed -> carry_forward)
    extract_t1_prices      :327-344 (filters, |market_value|/|units|, median per asset_name)
  The constants MAX_UNIT_PRICE, SOURCE_RANK and _SCOPED_PRICE_OVERRIDES are PARSED from that file with
  ast (never copied), so the instrument cannot drift from the pipeline without the parse failing.
Stdlib, pandas, pyarrow (via pandas) and boto3 only.
"""
import argparse
import ast
import io
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

BUCKET = "opal-data-bd"
PIPE_REL = "data/black_diamond/scripts/silver/bd_price_update.py"
CANON_KEY = "silver/prices/canonical_prices.parquet"
DAILY_FMT = "silver/prices/{}.parquet"
DAILY_RE = re.compile(r"^silver/prices/(\d{4}-\d{2}-\d{2})\.parquet$")
TXN_FMT = "silver/transactions/{}.parquet"
HIST_KEY = "silver/historical_prices.parquet"
REL_TOL = 1e-6
EMPTY_TRADES = {"trade_ids": [], "rows_used": 0, "distinct_trade_ids": 0,
                "median_distinct": None, "recomputed_price": None}
B01_NOTE = ("gold/B_01.holdings_lots.py:355-360 keeps the first row per asset_name after "
            "sort_values('date', ascending=False) over EVERY silver/prices object. This instrument compares the "
            "two objects that carry the requested date (daily file first, canonical second, stable sort). B_01 "
            "sorts with the pandas default (unstable) at :359, so its pick between two rows of the SAME date is "
            "not guaranteed: a tie is reported as a tie, never as B_01's proven choice.")


def find_pipeline_src(explicit=None):
    """Locate bd_price_update.py: the --pipeline-src value, else walk up from this file."""
    if explicit:
        p = Path(explicit)
        if p.is_file():
            return p
        raise FileNotFoundError("pipeline source not found: %s" % explicit)
    for up in Path(__file__).resolve().parents:
        cand = up / PIPE_REL
        if cand.is_file():
            return cand
    raise FileNotFoundError("%s not found above %s" % (PIPE_REL, __file__))


def load_constants(src):
    """Parse MAX_UNIT_PRICE, SOURCE_RANK and _SCOPED_PRICE_OVERRIDES from the pipeline source with ast."""
    tree = ast.parse(Path(src).read_text(encoding="utf-8"), filename=str(src))
    got, lines = {}, {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names = [node.target.id]
        else:
            continue
        for name in names:
            if name == "MAX_UNIT_PRICE":
                got["max_unit_price"] = float(ast.literal_eval(node.value))
                lines["MAX_UNIT_PRICE"] = node.lineno
            elif name == "SOURCE_RANK":
                got["source_rank"] = ast.literal_eval(node.value)
                lines["SOURCE_RANK"] = node.lineno
            elif name == "_SCOPED_PRICE_OVERRIDES":
                ov = []
                for elt in node.value.elts:
                    d = ast.literal_eval(elt)
                    ov.append({"asset_name": d["asset_name"], "ticker": d["ticker"],
                               "price": float(d["price"]), "line": elt.lineno})
                got["overrides"] = ov
                lines["_SCOPED_PRICE_OVERRIDES"] = node.lineno
    missing = [k for k in ("max_unit_price", "source_rank", "overrides") if k not in got]
    if missing:
        raise ValueError("constants not parsed from %s: %s" % (src, missing))
    got["src_rel"] = PIPE_REL
    got["lines"] = lines
    return got


def override_entry(consts, asset):
    """Last entry wins, as in the dict comprehension _SCOPED_OVERRIDE_MAP (bd_price_update.py:186-188)."""
    hit = None
    for o in consts["overrides"]:
        if o["asset_name"] == asset:
            hit = o
    return hit


def valid_trades(txns, asset, consts):
    """The rule of extract_t1_prices:335-341, restricted to one asset (grouped by asset_name at :344)."""
    cols = ["transaction_id", "units", "market_value", "calc_price"]
    if txns is None or txns.empty:
        return pd.DataFrame(columns=cols)
    t = txns[txns["asset_name"].astype(object) == asset]
    t = t[t["asset_name"].notna() & t["units"].notna() & (t["units"].abs() > 1e-8)
          & t["market_value"].notna() & (t["market_value"] != 0)].copy()
    t["calc_price"] = t["market_value"].abs() / t["units"].abs()
    t = t[(t["calc_price"] > 0) & (t["calc_price"] < consts["max_unit_price"])]
    return t


def summarize_trades(rows):
    if rows.empty:
        return dict(EMPTY_TRADES)
    ids = [None if pd.isna(x) else str(x) for x in rows["transaction_id"].tolist()]
    distinct = rows.drop_duplicates(subset=["transaction_id"], keep="first")
    return {"trade_ids": ids,
            "rows_used": int(len(rows)),
            "distinct_trade_ids": int(len(distinct)),
            "median_distinct": float(distinct["calc_price"].median()),
            "recomputed_price": float(rows["calc_price"].median())}


def is_match(recomputed, served):
    if recomputed is None or served is None:
        return False
    return bool(abs(recomputed - served) <= REL_TOL * max(1.0, abs(served)))


def _opt(x):
    return None if x is None or pd.isna(x) else str(x)


def _yahoo_close(hist, ticker, d):
    """fetch_yahoo_closes_for_date:375-390: last non-null positive close, window [d-7d, d]."""
    if hist is None or ticker is None:
        return None
    start = d - timedelta(days=7)
    sub = hist[(hist["ticker"].astype(object) == ticker) & (hist["date"] >= start) & (hist["date"] <= d)]
    sub = sub.sort_values("date")
    sub = sub[sub["close"].notna() & (sub["close"] > 0)]
    if sub.empty:
        return None
    last = sub.iloc[-1]
    return {"ticker": ticker, "close": float(last["close"]), "close_date": str(pd.Timestamp(last["date"]).date())}


def _absent_record(asset, date, reason):
    rec = {"asset_name": asset, "date": date, "served_price": None, "price_source": None,
           "rule": reason, "claim": "absent", "match": False, "served_from": {"key": None, "version_id": None},
           "served_rows": [], "tie": False, "superseded_by_later_date": None, "rule_inputs": {}}
    rec.update(EMPTY_TRADES)
    return rec


def trace_asset_date(asset, date, consts, daily, canon, txns, hist):
    """Pure core. daily / canon: (frame, key, version_id) or None. txns / hist: (frame, key) or None, or a
    zero-argument callable returning that tuple (called only when the served source needs it).
    Returns the record for one (asset, date) with the keys the task order names."""
    d = pd.Timestamp(date)
    objs = []
    for ref in (daily, canon):
        if ref is not None:
            objs.append({"key": ref[1], "version_id": ref[2], "frame": ref[0]})
    objs.sort(key=lambda o: o["key"])  # B_01 concatenates in sorted key order (gold/B_01:331-353)
    parts = []
    for o in objs:
        f = o["frame"]
        if f is None or f.empty:
            continue
        sub = f[f["asset_name"].astype(object) == asset].copy()
        if sub.empty:
            continue
        sub["_object"] = o["key"]
        sub["_version"] = o["version_id"]
        parts.append(sub)
    if not parts:
        return _absent_record(asset, date, "no served row for this asset in any silver/prices object read")
    allr = pd.concat(parts, ignore_index=True)
    allr["date"] = pd.to_datetime(allr["date"])
    same = allr[allr["date"] == d]
    part_key = TXN_FMT.format(date)
    if same.empty:
        rec = _absent_record(asset, date, "no served row for this asset on this date in the objects read")
        later = allr[allr["date"] > d]
        if not later.empty:
            rec["superseded_by_later_date"] = str(later["date"].max().date())
        return rec

    top_date = allr["date"].max()
    winner = same.iloc[0]
    src = str(winner["source"])
    price = float(winner["price"])
    ticker = _opt(winner["ticker"]) if "ticker" in winner.index else None
    canon_key = canon[1] if canon is not None else None
    tie = bool(same["_object"].nunique() > 1)
    served_rows = []
    for i, (_, r) in enumerate(same.iterrows()):
        served_rows.append({"object": r["_object"], "version_id": _opt(r["_version"]), "source": _opt(r["source"]),
                            "price": float(r["price"]), "ticker": _opt(r.get("ticker")), "stable_pick": i == 0})

    inputs = {}
    tr = dict(EMPTY_TRADES)
    partition_present = None
    if src == "transaction_observed":
        tup = txns() if callable(txns) else txns
        partition_present = tup is not None
        if tup is None:
            inputs["transaction_partition"] = "absent: %s not read" % part_key
            tr = dict(EMPTY_TRADES)
        else:
            tr = summarize_trades(valid_trades(tup[0], asset, consts))
            inputs["transaction_partition"] = {"key": tup[1], "rows": int(len(tup[0]))}
        rule = ("transaction_observed: median over the asset's rows in %s after the filters at "
                "extract_t1_prices:335-341 (units > 1e-8, market_value != 0, 0 < |market_value|/|units| < "
                "MAX_UNIT_PRICE=%g at %s:%d); build_target_date_rows:463-464 applies it when no scoped override "
                "or yahoo close exists. The partition is read by load_transactions_for_date:263-271 with no "
                "de-duplication on transaction_id. A row written by backfill_new_assets is computed from "
                "load_transactions_for_new_assets:257-259, which DOES de-duplicate; the object alone cannot "
                "show which writer produced it."
                % (part_key, consts["max_unit_price"], consts["src_rel"], consts["lines"]["MAX_UNIT_PRICE"]))
        recomputed = tr["recomputed_price"]
        match = is_match(recomputed, price)
        claim = "measured" if partition_present else "absent"
    elif src == "scoped_override":
        ov = override_entry(consts, asset)
        if ov is not None:
            rule = ("scoped_override: the asset is in _SCOPED_PRICE_OVERRIDES (%s:%d; entry at line %d, ticker %s, "
                    "price %s); build_target_date_rows:445-451 writes that constant before any other source, so "
                    "the price is the constant and no data input is used."
                    % (consts["src_rel"], consts["lines"]["_SCOPED_PRICE_OVERRIDES"], ov["line"], ov["ticker"],
                       ov["price"]))
            inputs["scoped_override_entry"] = {"line": ov["line"], "ticker": ov["ticker"], "price": ov["price"]}
        else:
            rule = ("scoped_override: the served row says scoped_override but the asset is NOT in "
                    "_SCOPED_PRICE_OVERRIDES in %s (list opens at line %d); the constant list does not explain it."
                    % (consts["src_rel"], consts["lines"]["_SCOPED_PRICE_OVERRIDES"]))
        match, claim = False, "measured"
    elif src == "yahoo_finance":
        tup = hist() if callable(hist) else hist
        yc = _yahoo_close(tup[0] if tup is not None else None, ticker, d)
        inputs["yahoo_close_read"] = yc if yc is not None else ("absent: %s not read" % HIST_KEY if tup is None
                                                                else None)
        rule = ("yahoo_finance: ticker %s had a close on or before %s within 7 days in %s "
                "(fetch_yahoo_closes_for_date:365-393, applied at build_target_date_rows:459-461); close read "
                "here: %s." % (ticker, date, HIST_KEY,
                               ("%s on %s" % (yc["close"], yc["close_date"])) if yc else "no close found"))
        match, claim = False, ("measured" if tup is not None else "absent")
    elif src == "linear_interpolation":
        rule = ("linear_interpolation: no daily input; backfill_new_assets:546-562 interpolates between the bracketing "
                "known prices (yahoo or transaction_observed) for dates inside the asset's range. This instrument "
                "does not recompute it; the bracketing inputs were not read (claim absent for them).")
        match, claim = False, "absent"
    elif src == "carry_forward":
        prev_txt = "canonical object not read"
        if canon is not None:
            prev = allr[(allr["_object"] == canon_key) & (allr["date"] < d)].sort_values("date")
            if prev.empty:
                prev_txt = "no earlier canonical row for this asset"
            else:
                p = prev.iloc[-1]
                prev_txt = "%s at %s (source %s)" % (str(p["date"].date()), float(p["price"]), _opt(p["source"]))
                inputs["carry_forward_input"] = {"date": str(p["date"].date()), "price": float(p["price"]),
                                                 "source": _opt(p["source"])}
        rule = ("carry_forward: build_target_date_rows:465-467 carries the asset's last canonical price forward "
                "(backfill_new_assets:568 for backfilled history); the nearest earlier canonical row is %s."
                % prev_txt)
        match, claim = False, "measured"
    else:
        rule = ("unrecognised source %r: not in SOURCE_RANK (%s:%d); upsert_canonical:595 maps it to rank 99."
                % (src, consts["src_rel"], consts["lines"]["SOURCE_RANK"]))
        match, claim = False, "measured"

    rec = {
        "asset_name": asset,
        "date": date,
        "served_price": price,
        "price_source": src,
        "rule": rule,
        "match": match,
        "served_from": {"key": winner["_object"], "version_id": _opt(winner["_version"])},
        "served_rows": served_rows,
        "tie": tie,
        "superseded_by_later_date": (str(top_date.date()) if top_date > d else None),
        "claim": claim,
        "rule_inputs": inputs,
        "partition": {"key": part_key, "present": partition_present},
        "b01_note": B01_NOTE,
    }
    rec.update(tr)
    rec["recomputed_price"] = tr["recomputed_price"]
    return rec


# ---------------------------------------------------------------- S3 reads (READ verbs only)

def s3_client():
    import boto3  # imported here so --self-test runs with no AWS at all
    return boto3.client("s3")


def read_obj(s3, bucket, key):
    """(frame, key, version_id) or None when the key does not exist. Other errors propagate."""
    from botocore.exceptions import ClientError
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") in ("NoSuchKey", "404"):
            return None
        raise
    frame = pd.read_parquet(io.BytesIO(resp["Body"].read()))
    return frame, key, resp.get("VersionId")


def read_txn(s3, bucket, date):
    key = TXN_FMT.format(date)
    got = read_obj(s3, bucket, key)
    return None if got is None else (got[0], key)


def read_hist(s3, bucket):
    got = read_obj(s3, bucket, HIST_KEY)
    if got is None:
        return None
    h = got[0]
    h["date"] = pd.to_datetime(h["date"], errors="coerce")
    return (h, HIST_KEY)


def list_daily(s3, bucket):
    """Daily price objects, newest first, and the denominator (every key under silver/prices/)."""
    out, n_keys = [], 0
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix="silver/prices/"):
        for o in page.get("Contents", []):
            n_keys += 1
            m = DAILY_RE.match(o["Key"])
            if m:
                out.append((m.group(1), o["Key"]))
    out.sort(reverse=True)
    return out, n_keys


def first_observed(s3, bucket, consts):
    """--date latest --first-transaction-observed. Walks daily files newest first; in file order, takes the
    first transaction_observed row whose full trace is transaction_observed with >= 1 valid trade. Earlier
    transaction_observed rows with no trade are counted, never hidden."""
    dates, n_keys = list_daily(s3, bucket)
    if not dates:
        return None, {"daily_files_listed": 0, "listed_keys": n_keys}
    counts = {"daily_files_listed": len(dates), "listed_keys": n_keys, "files_scanned": 0,
              "observed_rows_in_newest_file": None, "rows_scanned": 0, "skipped_without_trades": 0,
              "skipped_partition_missing": 0, "skipped_b01_other_source": 0, "skipped_date_mismatch": 0}
    canon_full = read_obj(s3, bucket, CANON_KEY)
    canon_cache = {}
    txn_cache = {}

    def canon_for(asset):
        if canon_full is None:
            return None
        if asset not in canon_cache:
            f = canon_full[0]
            canon_cache[asset] = (f[f["asset_name"].astype(object) == asset], CANON_KEY, canon_full[2])
        return canon_cache[asset]

    def txns_for(dstr):
        if dstr not in txn_cache:
            txn_cache[dstr] = read_txn(s3, bucket, dstr)
        return txn_cache[dstr]

    newest = dates[0][0]
    for dstr, key in dates:
        daily = read_obj(s3, bucket, key)
        counts["files_scanned"] += 1
        f = daily[0]
        obs = f[f["source"].astype(object) == "transaction_observed"]
        if dstr == newest:
            counts["observed_rows_in_newest_file"] = int(len(obs))
        for _, row in obs.iterrows():
            counts["rows_scanned"] += 1
            asset = row["asset_name"]
            if str(pd.Timestamp(row["date"]).date()) != dstr:
                counts["skipped_date_mismatch"] += 1
                continue
            tx = txns_for(dstr)
            if tx is None:
                counts["skipped_partition_missing"] += 1
                counts["skipped_without_trades"] += 1
                continue
            if valid_trades(tx[0], asset, consts).empty:
                counts["skipped_without_trades"] += 1
                continue
            rec = trace_asset_date(asset, dstr, consts, daily, canon_for(asset), lambda t=tx: t, None)
            if rec["price_source"] != "transaction_observed" or not rec["trade_ids"]:
                counts["skipped_b01_other_source"] += 1
                continue
            counts["newest_daily_date"] = newest
            counts["selected_daily_date"] = dstr
            counts["walked_back"] = dstr != newest
            return rec, counts
    return None, counts


def run_live(args, consts):
    s3 = s3_client()
    bucket = args.bucket
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if args.date == "latest":
        rec, counts = first_observed(s3, bucket, consts)
        if rec is None:
            rec = _absent_record("", "latest", "no transaction_observed row with a valid trade in any daily file")
        rec["selection"] = dict(counts, mode="--date latest --first-transaction-observed")
    else:
        daily = read_obj(s3, bucket, DAILY_FMT.format(args.date))
        canon = read_obj(s3, bucket, CANON_KEY)
        rec = trace_asset_date(args.asset, args.date, consts, daily, canon,
                               lambda: read_txn(s3, bucket, args.date),
                               lambda: read_hist(s3, bucket))
    rec["bucket"] = bucket
    rec["constants"] = {"src": consts["src_rel"], "max_unit_price": consts["max_unit_price"],
                        "lines": consts["lines"]}
    rec["generated_at"] = stamp
    rec["script"] = "trace_price.py (ADVI_BDPRCE BP-a-2)"
    return rec


# ---------------------------------------------------------------- self-test (offline, planted frames)

def _ts(s):
    return pd.Timestamp(s)


def _txns(rows):
    return pd.DataFrame({"transaction_id": [r[0] for r in rows], "asset_name": [r[1] for r in rows],
                         "units": [float(r[2]) for r in rows], "market_value": [float(r[3]) for r in rows],
                         "trade_date": [_ts("2026-10-12")] * len(rows)})


def _daily(rows):
    return pd.DataFrame({"date": [_ts(r[0]) for r in rows], "asset_name": [r[1] for r in rows],
                         "ticker": [r[2] for r in rows], "price": [float(r[3]) for r in rows],
                         "source": [r[4] for r in rows]})


def _planted_consts():
    return {"max_unit_price": 100000.0,
            "source_rank": {"scoped_override": -2, "yahoo_finance": -1, "transaction_observed": 0,
                            "linear_interpolation": 2, "carry_forward": 3},
            "overrides": [{"asset_name": "PLANT OVERRIDE", "ticker": "PLANT_OVR", "price": 1.5, "line": 90}],
            "src_rel": "SELF-TEST (planted)",
            "lines": {"MAX_UNIT_PRICE": 59, "SOURCE_RANK": 65, "_SCOPED_PRICE_OVERRIDES": 86}}


def run_self_test():
    c = _planted_consts()
    D = "2026-10-12"
    A = "PLANT ASSET A"
    arms = []

    def arm(name, ok, detail):
        arms.append(name)
        print("arm %d %s: %s -- %s" % (len(arms), "ok" if ok else "FAIL", name, detail))
        return ok

    def trades3(extra=()):
        return _txns([("T1", A, 10, 100), ("T2", A, 10, 300), ("T3", A, 5, 75)] + list(extra))

    prev = (_daily([("2026-10-11", A, None, 14.0, "transaction_observed")]), "silver/prices/canonical_prices.parquet",
            "V-CANON")
    daily_ok = (_daily([(D, A, None, 15.0, "transaction_observed")]), "silver/prices/%s.parquet" % D, "V-D")

    # arm 1: three planted trades, known median 15
    extra = [("T9", "OTHER ASSET", 1, 1), ("T8", A, 0, 50), ("T7", A, 4, 0)]
    r = trace_asset_date(A, D, c, daily_ok, prev, lambda: (trades3(extra), "silver/transactions/x.parquet"), None)
    ok1 = (r["recomputed_price"] == 15.0 and r["trade_ids"] == ["T1", "T2", "T3"] and r["match"] is True)
    if not arm("three trades, known median", ok1, "recomputed=%s ids=%s match=%s"
               % (r["recomputed_price"], r["trade_ids"], r["match"])):
        return fail("arm 1: three trades")

    # arm 2: repeated transaction_id row
    rep = _txns([("T1", A, 10, 100), ("T1", A, 10, 100), ("T2", A, 10, 300)])
    d2 = (_daily([(D, A, None, 10.0, "transaction_observed")]), "silver/prices/%s.parquet" % D, "V-D")
    r2 = trace_asset_date(A, D, c, d2, prev, lambda: (rep, "silver/transactions/x.parquet"), None)
    ok2 = (r2["rows_used"] == r2["distinct_trade_ids"] + 1 and r2["trade_ids"] == ["T1", "T1", "T2"]
           and r2["recomputed_price"] == 10.0)
    if not arm("repeated row kept in rows_used", ok2, "rows_used=%s distinct=%s ids=%s"
               % (r2["rows_used"], r2["distinct_trade_ids"], r2["trade_ids"])):
        return fail("arm 2: repeated row")

    # arm 3: served price differs from the median
    d3 = (_daily([(D, A, None, 99.0, "transaction_observed")]), "silver/prices/%s.parquet" % D, "V-D")
    r3 = trace_asset_date(A, D, c, d3, prev, lambda: (trades3(), "silver/transactions/x.parquet"), None)
    if not arm("served != median gives match false", (r3["match"] is False and r3["recomputed_price"] == 15.0),
               "served=%s recomputed=%s match=%s" % (r3["served_price"], r3["recomputed_price"], r3["match"])):
        return fail("arm 3: mismatch")

    # arm 4: yahoo_finance row names the close and carries no trade ids
    hist = pd.DataFrame({"ticker": ["PLANT.T", "PLANT.T"], "date": [_ts("2026-10-10"), _ts("2026-10-20")],
                         "close": [12.5, 99.0]})
    d4 = (_daily([(D, A, "PLANT.T", 12.5, "yahoo_finance")]), "silver/prices/%s.parquet" % D, "V-D")
    r4 = trace_asset_date(A, D, c, d4, prev, lambda: (trades3(), "silver/transactions/x.parquet"),
                          lambda: (hist, "silver/historical_prices.parquet"))
    ok4 = (r4["trade_ids"] == [] and "historical_prices" in r4["rule"] and "close" in r4["rule"]
           and r4["rule_inputs"].get("yahoo_close_read", {}).get("close") == 12.5)
    if not arm("yahoo_finance names the close, no trades", ok4, "ids=%s close=%s"
               % (r4["trade_ids"], r4["rule_inputs"].get("yahoo_close_read"))):
        return fail("arm 4: yahoo")

    # arm 5: same-date tie between daily and canonical is reported as a tie
    canon_tie = (_daily([(D, A, None, 16.0, "carry_forward")]), "silver/prices/canonical_prices.parquet", "V-CANON")
    r5 = trace_asset_date(A, D, c, daily_ok, canon_tie, lambda: (trades3(), "silver/transactions/x.parquet"), None)
    if not arm("same-date tie reported as tie", (r5["tie"] is True and len(r5["served_rows"]) == 2),
               "tie=%s rows=%d stable_pick_object=%s" % (r5["tie"], len(r5["served_rows"]),
                                                          r5["served_from"]["key"])):
        return fail("arm 5: tie")

    # arm 6: MAX_UNIT_PRICE and units floor exclude the planted rows
    big = _txns([("T1", A, 10, 100), ("T5", A, 1, 1e6), ("T6", A, 1e-9, 5.0)])
    r6 = trace_asset_date(A, D, c, d2, prev, lambda: (big, "silver/transactions/x.parquet"), None)
    if not arm("MAX_UNIT_PRICE and units floor applied", (r6["trade_ids"] == ["T1"] and r6["rows_used"] == 1),
               "ids=%s rows_used=%s" % (r6["trade_ids"], r6["rows_used"])):
        return fail("arm 6: filters")

    # arm 7: scoped_override names the constant list entry and carries no trades
    so = (_daily([(D, "PLANT OVERRIDE", "PLANT_OVR", 1.5, "scoped_override")]),
          "silver/prices/%s.parquet" % D, "V-D")
    r7 = trace_asset_date("PLANT OVERRIDE", D, c, so, None, lambda: (trades3(), "silver/transactions/x.parquet"),
                          None)
    if not arm("scoped_override names the constant list", ("_SCOPED_PRICE_OVERRIDES" in r7["rule"]
                                                          and r7["trade_ids"] == []
                                                          and r7["rule_inputs"]["scoped_override_entry"]["line"] == 90),
               "rule_has_list=%s ids=%s" % ("_SCOPED_PRICE_OVERRIDES" in r7["rule"], r7["trade_ids"])):
        return fail("arm 7: override")

    print("TRACE SELFTEST: OK %d arms" % len(arms))
    return 0


def fail(arm_name):
    print("TRACE SELFTEST: FAIL %s" % arm_name)
    return 1


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="Trace one served Financial price to its rule and trade ids (read-only).")
    ap.add_argument("--asset", help="asset_name exactly as stored")
    ap.add_argument("--date", help="YYYY-MM-DD, or 'latest' (with --first-transaction-observed)")
    ap.add_argument("--first-transaction-observed", action="store_true")
    ap.add_argument("--bucket", default=BUCKET)
    ap.add_argument("--out", help="write the JSON record here (default: stdout)")
    ap.add_argument("--pipeline-src", help="bd_price_update.py path (default: found above this file)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if args.date == "latest":
        if not args.first_transaction_observed:
            ap.error("--date latest requires --first-transaction-observed")
    else:
        if not args.asset or not args.date or not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date or ""):
            ap.error("need --asset and --date YYYY-MM-DD (or --date latest --first-transaction-observed)")
        if args.first_transaction_observed:
            ap.error("--first-transaction-observed needs --date latest")
    try:
        consts = load_constants(find_pipeline_src(args.pipeline_src))
        rec = run_live(args, consts)
    except Exception as e:  # noqa: BLE001 -- report the failure loudly, never a partial record
        print("TRACE ERROR %s: %s" % (type(e).__name__, str(e)[:300]), file=sys.stderr)
        return 2
    text = json.dumps(rec, indent=2, ensure_ascii=True, default=str)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("TRACE WROTE %s asset=%s date=%s source=%s trades=%d match=%s"
              % (args.out, json.dumps(rec["asset_name"]), rec["date"], rec["price_source"],
                 len(rec["trade_ids"]), str(rec["match"]).lower()))
    else:
        print(text)
    return 0 if rec["claim"] == "measured" else 1


if __name__ == "__main__":
    sys.exit(main())
