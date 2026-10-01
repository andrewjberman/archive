"""RIV-d-5 never-widen -- the SERVED delta of round 4, measured per fund (round 3's served_delta_r3.py widened to GQGU and G6).

Replays the merged round-4 code over the CURRENT served inputs PLUS the device-local GQGU archive into a LOCAL sink, and diffs,
PER FUND, against what /rivalfunds serves today. READ-ONLY against S3 (it downloads; it never puts). Run from a tree at the
merged round-4 HEAD (t-5, v-2, i-2, q-1, f-3 merged):
    python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round4/served_delta_r4.py --out <json>

Widened over round 3:
- GQGU: every archived day is landed as issuer bronze with land_bronze(..., fund="GQGU") at the archive's own capture time
  (d-5's step 2), then silver in replay mode over those bronze dates. GQGU's rows are new by design (class 'gqgu').
- G6 flow_reconciliation is replayed and compared per fund on window_start (t-5 moves daily windows to the fund's own prior).
- The local readers take each date's newest object through revision.newest (v-2), never the greatest name.
- Per fund, the newest report date's resolved fraction and its source are printed: d-5's per-source floors come from these.
- `replay_window` names the G1/G5/G6 dates whose served bytes would change, all funds and excluding GQGU.

Trade key is identity-independent (fund, window_end, action, shares_delta to 1e-6), as in round 3."""
from __future__ import annotations

import argparse
import io
import json
import pathlib
import subprocess
import sys
import tempfile

BUCKET = "opal-data-etfs"


def log(*a):
    import datetime as _dt
    print(_dt.datetime.now(_dt.timezone.utc).strftime('%H:%M:%SZ'), *a, file=sys.stderr, flush=True)
HOME = {"IDVZ", "PFOE"}
NEW_FUND = "GQGU"


def root() -> pathlib.Path:
    return pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                                       check=True).stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--gqgu-archive", default=None, help="default: <root>/.runtime/amgt-reconn-daily-census-20260929/gqgu")
    args = ap.parse_args()
    r = root()
    for p in (str(r / "data" / "etfs" / "scripts"), str(r)):
        sys.path.insert(0, p)
    import boto3
    import pandas as pd
    from lib.opal_naming import address

    archive = pathlib.Path(args.gqgu_archive) if args.gqgu_archive else (
        r / ".runtime" / "amgt-reconn-daily-census-20260929" / "gqgu")
    s3 = boto3.client("s3", region_name="us-east-1")
    pg = s3.get_paginator("list_objects_v2")

    def pre(*a):
        return address(*a)[len(f"s3://{BUCKET}/"):].rsplit("date=", 1)[0]

    def keys(prefix):
        return [o["Key"] for p in pg.paginate(Bucket=BUCKET, Prefix=prefix) for o in p.get("Contents", [])]

    sink = pathlib.Path(tempfile.mkdtemp(prefix="rv_sd4_"))
    lsink = f"local:{sink}"

    def mirror(k):
        dst = sink / BUCKET / k
        dst.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(BUCKET, k, str(dst))
        return dst

    counts = {}
    sets = {
        "issuer_silver": keys(pre("issuer-site", "etfs", "silver", "holdings", "date=")),
        "issuer_sidecars": [k for k in keys(pre("issuer-site", "etfs", "bronze", "holdings", "date=")) if k.endswith(".json")],
        "bloomberg_silver": keys(pre("bloomberg", "etfs", "silver", "holdings", "date=")),
        "g3": sorted(keys(pre("rivalfunds", "etfs", "gold", "corporate_actions", "date=")))[-1:],
        "home_landings": [k for k in keys("bbg/") if k.endswith("/constituents/constituents_issuer_fill.parquet")],
    }
    from concurrent.futures import ThreadPoolExecutor
    for name, ks in sets.items():
        log('mirror', name, len(ks))
        with ThreadPoolExecutor(max_workers=24) as pool:
            list(pool.map(mirror, ks))  # list() re-raises the first download error
        counts[name] = len(ks)
    chars = sorted(k for k in keys("bbg/") if k.endswith("/characteristics.parquet"))
    counts["characteristics"] = chars[-1] if chars else None

    from rivalfunds import (collector_issuer, enrichment_bloomberg, gold_canonical_shape, gold_flow_reconciliation,
                            gold_peer_group_map, gold_trade_schedule, revision, silver_issuer)

    log('mirrored', counts)
    # GQGU import (d-5 step 2), local only
    landed, bronze_dates, not_ok = 0, set(), {}
    for side in sorted(archive.glob("????-??-??.json")):
        txt = side.with_suffix(".txt")
        if not txt.exists():
            continue
        meta = json.loads(side.read_text(encoding="utf-8"))
        sc = collector_issuer.land_bronze(txt.read_bytes(), meta["requested_date"], meta.get("url", ""), lsink,
                                          captured_at=meta.get("at"), http_status=int(meta.get("http_status", 200)),
                                          fund=NEW_FUND)
        landed += 1
        bronze_dates.add(sc["bronze_uri"].split("date=")[1][:10])
        if sc.get("status") != "OK":
            not_ok[sc.get("status")] = not_ok.get(sc.get("status"), 0) + 1
    counts["gqgu_archive_days_landed"] = landed
    counts["gqgu_bronze_dates"] = sorted(bronze_dates)
    counts["gqgu_not_ok"] = not_ok
    log('gqgu landed', landed, sorted(bronze_dates), not_ok)
    res = {}
    if bronze_dates:
        res["silver_gqgu"] = silver_issuer.handler_entry({"mode": "replay", "batch_id": "sd4-gqgu", "sink": lsink,
                                                          "start": min(bronze_dates), "end": max(bronze_dates)})

    log('silver_gqgu', str(res.get('silver_gqgu'))[:200])
    served = {}
    for table in ("canonical_shape", "trade_schedule", "flow_reconciliation"):
        per_date = {}
        for k in keys(pre("rivalfunds", "etfs", "gold", table, "date=")):
            if k.endswith(".parquet"):
                per_date.setdefault(k.split("date=")[1][:10], []).append(k)
        frames = []
        for d, ks in per_date.items():
            k = max(ks)  # the served pick was made by the round-3 readers (greatest name)
            df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()))
            df["_date"] = d
            frames.append(df)
        served[table] = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    newest = max(served["canonical_shape"]["_date"])

    ev = {"mode": "replay", "batch_id": "sd4-dry", "sink": lsink, "date": newest}
    res["g0"] = gold_peer_group_map.handler_entry(dict(ev, mode="daily"))
    if chars:
        cd = chars[-1].split("/")[1]
        res["g4"] = enrichment_bloomberg.handler_entry({"mode": "import-market", "characteristics": str(mirror(chars[-1])),
                                                        "date": cd, "batch_id": "sd4-g4", "sink": lsink})
    log('served read; newest', newest)
    res["g1"] = gold_canonical_shape.handler_entry(dict(ev))
    log('g1', str(res['g1'])[:200])
    res["g5"] = gold_trade_schedule.handler_entry(dict(ev))
    log('g5', str(res['g5'])[:200])
    res["g6"] = gold_flow_reconciliation.handler_entry(dict(ev))
    log('g6', str(res['g6'])[:200])

    def local(table):
        d = sink / BUCKET / pre("rivalfunds", "etfs", "gold", table, "date=")
        frames = []
        for part in sorted(p for p in d.glob("date=*") if p.is_dir()):
            objs = [str(p) for p in part.glob("*.parquet")]
            pick = revision.newest(objs)
            if not pick:
                continue
            df = pd.read_parquet(io.BytesIO(pathlib.Path(pick).read_bytes()))
            df["_date"] = part.name.split("date=")[1][:10]
            frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    g1n, g5n, g6n = local("canonical_shape"), local("trade_schedule"), local("flow_reconciliation")
    g1s, g5s, g6s = served["canonical_shape"], served["trade_schedule"], served["flow_reconciliation"]

    def fc(df):
        if not len(df):
            return pd.Series(dtype=str)
        return df["fund_ticker"].astype(str).str.strip() if "fund_ticker" in df.columns else df["fund_id"].astype(str)

    src_col = next((c for c in ("source_channel", "source", "holdings_source", "source_system") if c in g1n.columns), None)
    out = {"inputs": counts, "newest_report_date": newest, "stage_results": {k: str(v)[:240] for k, v in res.items()},
           "g1_source_column": src_col, "per_fund": {}}
    changed_dates_all, changed_dates_old = set(), set()
    funds = sorted(set(fc(g1s)) | set(fc(g1n)))
    for f in funds:
        a, b = g1s[fc(g1s) == f], g1n[fc(g1n) == f]
        ra, rb = a.groupby("_date").size(), b.groupby("_date").size()
        j = pd.concat([ra.rename("s"), rb.rename("n")], axis=1).fillna(0)
        diff_dates = set(j.index[j["s"] != j["n"]])
        nc = b[~b["is_cash_line"].astype(bool)] if len(b) and "is_cash_line" in b.columns else b
        nd = max(nc["_date"]) if len(nc) else None
        ncd = nc[nc["_date"] == nd] if nd else nc
        rec = {"g1_rows_served": int(ra.sum()), "g1_rows_new": int(rb.sum()), "g1_dates_served": int(len(ra)),
               "g1_dates_new": int(len(rb)),
               "g1_dates_rowcount_differs": int(((j["s"] != j["n"]) & (j["s"] > 0) & (j["n"] > 0)).sum()),
               "g1_dates_only_new": int(((j["s"] == 0) & (j["n"] > 0)).sum()),
               "g1_dates_only_served": int(((j["s"] > 0) & (j["n"] == 0)).sum()),
               "g1_resolved_frac_new": round(float((nc["resolution_status"] == "RESOLVED").mean()), 4) if len(nc) else None,
               "newest_date_new": nd,
               "newest_resolved_frac_new": round(float((ncd["resolution_status"] == "RESOLVED").mean()), 4) if len(ncd) else None,
               "newest_source_new": sorted(set(ncd[src_col].astype(str))) if src_col and len(ncd) else None,
               "g1_gics_resolved_new": int((b.get("gics_status", pd.Series(dtype=str)).astype(str) == "RESOLVED").sum())}

        def tk(df):
            if not len(df):
                return set()
            sd = df["shares_delta"].astype(float).round(6).astype(str) if "shares_delta" in df.columns else ""
            return set(df["window_end"].astype(str) + "|" + df["action"].astype(str) + "|" + sd)
        s5 = g5s[fc(g5s) == f] if len(g5s) else g5s
        n5 = g5n[fc(g5n) == f] if len(g5n) else g5n
        ss, ns = tk(s5), tk(n5)
        g5_dates = {x.split("|")[0][:10] for x in (ss ^ ns)}

        def wk(df):
            if not len(df) or "window_start" not in df.columns:
                return set()
            return set(df["window_start"].astype(str).str[:10] + ">" + df["window_end"].astype(str).str[:10])
        s6 = g6s[fc(g6s) == f] if len(g6s) else g6s
        n6 = g6n[fc(g6n) == f] if len(g6n) else g6n
        sw, nw = wk(s6), wk(n6)
        g6_dates = {x.split(">")[1] for x in (sw ^ nw)}
        cls = "gqgu" if f == NEW_FUND else ("home" if f in HOME else "other")
        rec.update({"g5_trades_served": len(ss), "g5_trades_new": len(ns), "g5_removed": len(ss - ns),
                    "g5_added": len(ns - ss), "g6_windows_served": len(sw), "g6_windows_new": len(nw),
                    "g6_windows_removed": sorted(sw - nw)[:6], "g6_windows_added": sorted(nw - sw)[:6],
                    "class": cls, "g5_examples": sorted(list((ss - ns))[:2]) + sorted(list((ns - ss))[:2])})
        out["per_fund"][f] = rec
        fund_dates = diff_dates | g5_dates | g6_dates
        changed_dates_all |= fund_dates
        if f != NEW_FUND:
            changed_dates_old |= fund_dates
    out["replay_window"] = {"all": [min(changed_dates_all), max(changed_dates_all)] if changed_dates_all else None,
                            "excluding_gqgu": [min(changed_dates_old), max(changed_dates_old)] if changed_dates_old else None,
                            "changed_dates_excluding_gqgu": sorted(changed_dates_old)}
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps({"inputs": {k: v for k, v in counts.items() if k != "gqgu_bronze_dates"}, "newest": newest,
                      "replay_window": out["replay_window"]}, default=str))
    for f, rec in out["per_fund"].items():
        print(f, {k: rec[k] for k in ("class", "g1_rows_served", "g1_rows_new", "g1_dates_rowcount_differs",
                                      "g1_dates_only_new", "g1_dates_only_served", "newest_date_new",
                                      "newest_resolved_frac_new", "newest_source_new", "g5_removed", "g5_added",
                                      "g6_windows_served", "g6_windows_new")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
