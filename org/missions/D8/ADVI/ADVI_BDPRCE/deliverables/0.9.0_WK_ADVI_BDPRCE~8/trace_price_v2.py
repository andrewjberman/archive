#!/usr/bin/env python3
"""trace_price_v2.py -- ADVI_BDPRCE BP-b-4 (round 2): trace the price the SERVED lot carries, not a daily default.

READ-ONLY. Reads through boto3 get_object / list_objects_v2 only:
  silver/prices/<date>.parquet, silver/prices/canonical_prices.parquet,
  silver/transactions/<date>.parquet, silver/historical_prices.parquet   (bucket opal-data-bd by default)
  and, in --lot-object mode, one served client detail object at an explicit VersionId.
Writes nothing except the --out file. No producer run, no download to the checkout.

Round 1's instrument (deliverables/0.9.0_WK_ADVI_BDPRCE~2/trace_price.py) is IMPORTED, not copied: its rule
functions (trace_asset_date, valid_trades, summarize_trades, is_match, load_constants, read_obj, read_txn,
read_hist and the constants) run unchanged. What v2 adds is the FOLLOW step: the followed row is the candidate
whose price equals the served price, not the daily row by default. The recompute is still the as-built rule.

Stdlib, pandas, pyarrow (via pandas) and boto3 only.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
R1_PATH = HERE.parent / "0.9.0_WK_ADVI_BDPRCE~2" / "trace_price.py"
R1_RULE_REL = "data/black_diamond/scripts/silver/bd_price_rule.py"


def _load_round1():
    if not R1_PATH.is_file():
        raise FileNotFoundError("round-1 instrument not found: %s" % R1_PATH)
    spec = importlib.util.spec_from_file_location("trace_price_r1", str(R1_PATH))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R1 = _load_round1()
BUCKET = R1.BUCKET
CANON_KEY = R1.CANON_KEY
DAILY_FMT = R1.DAILY_FMT
TXN_FMT = R1.TXN_FMT
REL_TOL = R1.REL_TOL


def same_price(a, b):
    """The served-price test: within 1e-6 * max(1, |served|), as the task order names it."""
    if a is None or b is None:
        return False
    return bool(abs(float(a) - float(b)) <= REL_TOL * max(1.0, abs(float(b))))


def _row(c):
    """The {price, source, version_id} shape the task order names for daily_row and canonical_row."""
    if c is None:
        return None
    return {"price": c["price"], "source": c["source"], "version_id": c["version_id"]}


def _same_date_mask(frame, asset, d):
    return (frame["asset_name"].astype(object) == asset) & (pd.to_datetime(frame["date"]) == d)


def _candidates(ref, which, asset, d):
    """All same-date rows for the asset in one object: ref is (frame, key, version_id) or None."""
    if ref is None or ref[0] is None or ref[0].empty:
        return []
    f = ref[0]
    m = _same_date_mask(f, asset, d)
    out = []
    for idx in f.index[m.to_numpy()]:
        r = f.loc[idx]
        out.append({"obj": which, "idx": idx, "price": float(r["price"]),
                    "source": R1._opt(r["source"]), "version_id": ref[2], "key": ref[1]})
    return out


def trace_followed(asset, date, served, daily, canon, consts, txns, hist):
    """Pure core (offline-testable). daily / canon: (frame, key, version_id) or None. txns / hist: as round 1.
    Returns the v2 record. followed_source is canonical or daily, or null when no candidate equals served."""
    served = float(served)
    d = pd.Timestamp(date)
    dcs = _candidates(daily, "daily", asset, d)
    ccs = _candidates(canon, "canonical", asset, d)
    cands = dcs + ccs
    eq_c = [c for c in ccs if same_price(c["price"], served)]
    eq_d = [c for c in dcs if same_price(c["price"], served)]
    both_equal = bool(eq_c and eq_d)
    if eq_c:
        followed = eq_c[0]
    elif eq_d:
        followed = eq_d[0]
    else:
        followed = None

    base = {
        "asset_name": asset,
        "date": date,
        "served_price": served,
        "daily_row": _row(dcs[0]) if dcs else None,
        "canonical_row": _row(ccs[0]) if ccs else None,
        "same_date_rows": {"daily": len(dcs), "canonical": len(ccs)},
        "served_rows": [{"object": c["key"], "version_id": c["version_id"], "source": c["source"],
                         "price": c["price"], "followed": c is followed} for c in cands],
        "tie": bool(dcs and ccs),
    }
    if followed is None:
        base.update({
            "followed_source": None,
            "followed_price": None,
            "follows_served": False,
            "rule": ("no same-date row for this asset in the daily file or canonical_prices.parquet has a price "
                     "equal to the served price %s (tolerance %g * max(1,|served|)); no row is followed and no "
                     "rule is traced. The candidates are listed in served_rows; none is picked."
                     % (served, REL_TOL)),
            "trade_ids": [],
            "rows_used": 0,
            "distinct_trade_ids": 0,
            "median_distinct": None,
            "recomputed_price": None,
            "match": False,
            "claim": "measured",
            "follow_note": "served price matches neither candidate row; follows_served is false",
        })
        return base

    is_same_c = _same_date_mask(canon[0], asset, d) if canon is not None else None
    if followed["obj"] == "canonical":
        # Keep every canonical row EXCEPT the asset's same-date rows, plus the followed row only.
        keep = (~is_same_c) | (canon[0].index == followed["idx"])
        canon_arg = (canon[0][keep.to_numpy()], canon[1], canon[2])
        daily_arg = None
    else:
        # Followed daily: the daily object carries only the followed row; canonical keeps its earlier and
        # later rows (carry_forward reads the earlier one) and drops the same-date rows so they do not compete.
        daily_arg = (daily[0].loc[[followed["idx"]]], daily[1], daily[2])
        canon_arg = (canon[0][(~is_same_c).to_numpy()], canon[1], canon[2]) if canon is not None else None

    rec = R1.trace_asset_date(asset, date, consts, daily_arg, canon_arg, txns, hist)
    followed_source = "canonical" if followed["obj"] == "canonical" else "daily"
    if both_equal:
        follow_note = ("both the daily row and the canonical row equal the served price; the canonical row is "
                       "followed by rule. B_01 breaks a same-date tie by an unstable sort, so which of the two "
                       "the lot read is not proven here.")
    else:
        follow_note = "the %s row is the only candidate equal to the served price" % followed_source
    out = dict(base)
    out.update({
        "followed_source": followed_source,
        "followed_price": followed["price"],
        "follows_served": same_price(followed["price"], served),
        "rule": rec["rule"],
        "trade_ids": rec["trade_ids"],
        "rows_used": rec.get("rows_used", 0),
        "distinct_trade_ids": rec.get("distinct_trade_ids", 0),
        "median_distinct": rec.get("median_distinct"),
        "recomputed_price": rec["recomputed_price"],
        "match": rec["match"],
        "claim": rec["claim"],
        "price_source": rec["price_source"],
        "served_from": {"key": followed["key"], "version_id": followed["version_id"]},
        "both_equal": both_equal,
        "follow_note": follow_note,
        "superseded_by_later_date": rec.get("superseded_by_later_date"),
        "rule_inputs": rec.get("rule_inputs", {}),
        "partition": rec.get("partition"),
        "b01_note": rec.get("b01_note"),
    })
    return out


def r1_price_note():
    """r1_price is added only when the parallel cell's module exists in this tree. Never blocks."""
    for up in HERE.parents:
        cand = up / R1_RULE_REL
        if cand.is_file():
            return {"r1_price_module": "present (not wired by BP-b-4; API unread at build time)"}
    return {"r1_price_module": "absent in this tree; r1_price not added"}


# ---------------------------------------------------------------- S3 reads (READ verbs only)

def s3_client():
    import boto3  # imported here so --self-test runs with no AWS at all
    return boto3.client("s3")


def parse_lot_spec(spec):
    if "@" not in spec or "/" not in spec.split("@", 1)[0]:
        raise ValueError("--lot-object needs <bucket>/<key>@<VersionId>")
    loc, vid = spec.rsplit("@", 1)
    bucket, key = loc.split("/", 1)
    if not bucket or not key or not vid:
        raise ValueError("--lot-object needs <bucket>/<key>@<VersionId>")
    return bucket, key, vid


def read_lot(s3, spec, asset):
    """The served lot: its data_as_of date and the one current_price it carries for the asset."""
    bucket, key, vid = parse_lot_spec(spec)
    resp = s3.get_object(Bucket=bucket, Key=key, VersionId=vid)
    lot = json.loads(resp["Body"].read().decode("utf-8"))
    as_of = lot.get("data_as_of")
    if not as_of:
        raise ValueError("served object carries no data_as_of")
    lots = [x for x in (lot.get("tax") or {}).get("open_lots", []) if x.get("asset_name") == asset]
    prices = sorted({float(x["current_price"]) for x in lots if x.get("current_price") is not None})
    if not lots:
        raise ValueError("asset not among the served open_lots (%d lots read)" % len(lots))
    if len(prices) != 1:
        raise ValueError("asset carries %d distinct current_price values in the served lot" % len(prices))
    meta = {"kind": "lot_object", "bucket": bucket,
            "key_sha256": hashlib.sha256(key.encode("utf-8")).hexdigest()[:16],
            "version_id": resp.get("VersionId", vid), "lot_rows_for_asset": len(lots),
            "date_source": "served object data_as_of", "data_as_of": str(as_of)}
    return str(as_of), prices[0], meta


def run_live(args, consts):
    s3 = s3_client()
    bucket = args.bucket
    calls = []
    if args.lot_object:
        date, served, served_meta = read_lot(s3, args.lot_object, args.asset)
        calls.append("s3 get_object (served lot, explicit VersionId)")
    else:
        date, served, served_meta = args.date, float(args.served_price), {"kind": "--served-price"}
    calls.append("s3 get_object %s %s" % (bucket, DAILY_FMT.format(date)))
    daily = R1.read_obj(s3, bucket, DAILY_FMT.format(date))
    calls.append("s3 get_object %s %s" % (bucket, CANON_KEY))
    canon = R1.read_obj(s3, bucket, CANON_KEY)

    def txns():
        calls.append("s3 get_object %s %s" % (bucket, TXN_FMT.format(date)))
        return R1.read_txn(s3, bucket, date)

    def hist():
        calls.append("s3 get_object %s %s" % (bucket, R1.HIST_KEY))
        return R1.read_hist(s3, bucket)

    rec = trace_followed(args.asset, date, served, daily, canon, consts, txns, hist)
    rec["served_source"] = served_meta
    rec["bucket"] = bucket
    rec["constants"] = {"src": consts["src_rel"], "max_unit_price": consts["max_unit_price"],
                        "lines": consts["lines"]}
    rec.update(r1_price_note())
    rec["calls"] = calls
    rec["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec["script"] = "trace_price_v2.py (ADVI_BDPRCE BP-b-4), imports trace_price.py (BP-a-2) for the rule"
    return rec


# ---------------------------------------------------------------- self-test (offline, planted frames)

def run_self_test():
    c = R1._planted_consts()
    D = "2026-10-12"
    P = "2026-10-11"
    A = "PLANT ASSET B"
    _txns = R1._txns
    _daily = R1._daily
    arms = []

    def arm(name, ok, detail):
        arms.append(name)
        print("arm %d %s: %s -- %s" % (len(arms), "ok" if ok else "FAIL", name, detail))
        return ok

    def fail(name):
        print("TRACE2 SELFTEST: FAIL %s" % name)
        return 1

    def canon_frame(rows):
        return _daily(rows)

    # trades whose median is 168.94 (prices 168.94, 200, 150); a repeat-free set
    def tr():
        return (_txns([("T1", A, 10, 1689.4), ("T2", A, 10, 2000), ("T3", A, 10, 1500)]),
                "silver/transactions/planted.parquet")

    d_eq =(_daily([(D, A, None, 168.94, "transaction_observed")]), "silver/prices/%s.parquet" % D, "V-D")
    c_eq = (canon_frame([(P, A, None, 140.0, "transaction_observed"), (D, A, None, 168.94, "transaction_observed")]),
            "silver/prices/canonical_prices.parquet", "V-CANON")

    # arm 1: daily and canonical both present and equal -> follows canonical
    r = trace_followed(A, D, 168.94, d_eq, c_eq, c, tr, None)
    ok1 = (r["followed_source"] == "canonical" and r["follows_served"] is True and r["both_equal"] is True
           and r["canonical_row"] is not None and r["daily_row"] is not None and r["match"] is True
           and all(k in r for k in ("asset_name", "date", "served_price", "followed_price", "rule", "trade_ids",
                                    "recomputed_price", "daily_row", "canonical_row", "claim")))
    if not arm("daily and canonical equal -> follows canonical", ok1,
               "followed=%s follows=%s both=%s match=%s" % (r["followed_source"], r["follows_served"],
                                                              r["both_equal"], r["match"])):
        return fail("arm 1: equal rows")

    # arm 2 (NEGATIVE ARM): daily 162.155 carry_forward, canonical 168.94 transaction_observed, served 168.94
    d_cf = (_daily([(D, A, None, 162.155, "carry_forward")]), "silver/prices/%s.parquet" % D, "V-D")
    c_obs = (canon_frame([(P, A, None, 140.0, "transaction_observed"), (D, A, None, 168.94, "transaction_observed")]),
             "silver/prices/canonical_prices.parquet", "V-CANON")
    r2 = trace_followed(A, D, 168.94, d_cf, c_obs, c, tr, None)
    ok2 = (r2["followed_source"] == "canonical" and r2["follows_served"] is True
           and r2["daily_row"] == {"price": 162.155, "source": "carry_forward", "version_id": "V-D"}
           and r2["followed_price"] == 168.94 and r2["match"] is True)
    if not arm("NEGATIVE: daily 162.155 reported, canonical followed", ok2,
               "followed=%s daily=%s follows=%s" % (r2["followed_source"], r2["daily_row"], r2["follows_served"])):
        return fail("arm 2: negative")

    # arm 3: same frames, served 162.155 -> follows the daily row (carry_forward, so no recompute)
    r3 = trace_followed(A, D, 162.155, d_cf, c_obs, c, tr, None)
    ok3 = (r3["followed_source"] == "daily" and r3["follows_served"] is True and r3["followed_price"] == 162.155
           and r3["match"] is False and r3["trade_ids"] == [] and "carry_forward" in r3["rule"]
           and "140.0" in r3["rule"])
    if not arm("served 162.155 follows the daily row", ok3,
               "followed=%s rule_has_prev=%s match=%s" % (r3["followed_source"], "140.0" in r3["rule"], r3["match"])):
        return fail("arm 3: daily followed")

    # arm 4: served matches neither -> follows_served false, nothing followed silently
    r4 = trace_followed(A, D, 170.0, d_cf, c_obs, c, tr, None)
    ok4 = (r4["follows_served"] is False and r4["followed_source"] is None and r4["trade_ids"] == []
           and r4["match"] is False and "no row is followed" in r4["rule"]
           and r4["followed_price"] is None)
    if not arm("served matches neither -> follows_served false", ok4,
               "follows=%s followed=%s ids=%s" % (r4["follows_served"], r4["followed_source"], r4["trade_ids"])):
        return fail("arm 4: neither")

    # arm 5: repeated transaction_id is listed with repeats kept (round-1 rule, followed canonical)
    def rep():
        return (_txns([("T1", A, 10, 1689.4), ("T1", A, 10, 1689.4), ("T2", A, 10, 2000)]),
                "silver/transactions/planted.parquet")

    r5 =trace_followed(A, D, 168.94, d_eq, c_eq, c, rep, None)
    ok5 = (r5["trade_ids"] == ["T1", "T1", "T2"] and r5["rows_used"] == 3 and r5["distinct_trade_ids"] == 2)
    if not arm("repeated transaction_id kept", ok5, "ids=%s rows=%s distinct=%s"
               % (r5["trade_ids"], r5["rows_used"], r5["distinct_trade_ids"])):
        return fail("arm 5: repeats")

    # arm 6: daily-only (no canonical row on the date) and served equals it -> follows daily
    r6 = trace_followed(A, D, 162.155, d_cf, (canon_frame([(P, A, None, 140.0, "transaction_observed")]),
                                              "silver/prices/canonical_prices.parquet", "V-CANON"), c, tr, None)
    ok6 = (r6["followed_source"] == "daily" and r6["canonical_row"] is None and r6["both_equal"] is False)
    if not arm("daily-only row followed, canonical_row null", ok6,
               "followed=%s canonical_row=%s" % (r6["followed_source"], r6["canonical_row"])):
        return fail("arm 6: daily only")

    # arm 7: a served price inside the tolerance still follows canonical (1e-6 * max(1,|served|))
    r7 = trace_followed(A, D, 168.94 + 1e-7, d_eq, c_eq, c, tr, None)
    ok7 = (r7["followed_source"] == "canonical" and r7["follows_served"] is True)
    if not arm("served within tolerance follows canonical", ok7,
               "followed=%s follows=%s" % (r7["followed_source"], r7["follows_served"])):
        return fail("arm 7: tolerance")

    print("TRACE2 SELFTEST: OK %d arms" % len(arms))
    return 0


# ---------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="Trace the price the served lot carries (read-only, BP-b-4).")
    ap.add_argument("--asset", help="asset_name exactly as stored")
    ap.add_argument("--date", help="YYYY-MM-DD (with --served-price)")
    ap.add_argument("--served-price", help="the served price, as read from the lot")
    ap.add_argument("--lot-object", help="<bucket>/<key>@<VersionId> of a served client detail object")
    ap.add_argument("--bucket", default=BUCKET)
    ap.add_argument("--out", help="write the JSON record here (default: stdout)")
    ap.add_argument("--pipeline-src", help="bd_price_update.py path (default: found above the round-1 file)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if not args.asset:
        ap.error("need --asset")
    if args.lot_object:
        if args.date or args.served_price:
            ap.error("--lot-object takes the date and the served price from the object; drop --date and --served-price")
    else:
        if not args.date or not args.served_price:
            ap.error("need --date YYYY-MM-DD and --served-price (or --lot-object)")
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date):
            ap.error("--date must be YYYY-MM-DD")
    try:
        consts = R1.load_constants(R1.find_pipeline_src(args.pipeline_src))
        rec = run_live(args, consts)
    except Exception as e:  # noqa: BLE001 -- report the failure loudly, never a partial record
        print("TRACE2 ERROR %s: %s" % (type(e).__name__, str(e)[:300]), file=sys.stderr)
        return 2
    text = json.dumps(rec, indent=2, ensure_ascii=True, default=str)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print("TRACE2 WROTE %s asset=%s date=%s followed=%s follows_served=%s trades=%d match=%s"
              % (args.out, json.dumps(rec["asset_name"]), rec["date"], rec["followed_source"],
                 str(rec["follows_served"]).lower(), len(rec["trade_ids"]), str(rec["match"]).lower()))
    else:
        print(text)
    return 0 if (rec["claim"] == "measured" and rec["follows_served"] is True) else 1


if __name__ == "__main__":
    sys.exit(main())
