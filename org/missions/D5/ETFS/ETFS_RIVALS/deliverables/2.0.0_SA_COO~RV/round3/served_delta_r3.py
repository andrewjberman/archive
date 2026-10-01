"""RIV-d-4 never-widen -- the SERVED delta of round 3, measured (the round-2 key-4 method, widened to every input round 3 reads).

Replays the merged round-3 code over the CURRENT served inputs into a LOCAL sink and diffs, PER FUND, against what
/rivalfunds serves today. READ-ONLY against S3 (it downloads; it never puts). Run from a tree at the merged round-3 HEAD:
    python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round3/served_delta_r3.py --out <json>

Mirrored inputs: issuer silver + issuer bronze sidecars; Bloomberg silver; the newest served G3; the Positioning home
landings bbg/<D>/constituents/constituents_issuer_fill.parquet for every <D>; and G4 imported from the newest
bbg/<D>/characteristics.parquet (the act's own step 4).

Trades are compared on an IDENTITY-INDEPENDENT key (fund, window_end, action, shares_delta rounded to 1e-6), because round 3
resolves identity (RIV-i-1): a trade whose security key merely moved from unresolved to resolved is not a removed + added pair.
Classes for a key present on one side only: home (a home fund -- new by design), held (the fund is held in the newest batch),
other. The expected served outcome is: G1 for every non-home fund keeps its row counts per (fund, date); G5 'other' == 0 for
every fund whose inputs are unchanged."""
from __future__ import annotations

import argparse
import io
import json
import pathlib
import subprocess
import sys
import tempfile

BUCKET = "opal-data-etfs"
HOME = {"IDVZ", "PFOE"}


def root() -> pathlib.Path:
    return pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                                       check=True).stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    r = root()
    for p in (str(r / "data" / "etfs" / "scripts"), str(r)):
        sys.path.insert(0, p)
    import boto3
    import pandas as pd
    from lib.opal_naming import address

    s3 = boto3.client("s3", region_name="us-east-1")
    pg = s3.get_paginator("list_objects_v2")

    def pre(*a):
        return address(*a)[len(f"s3://{BUCKET}/"):].rsplit("date=", 1)[0]

    def keys(prefix):
        return [o["Key"] for p in pg.paginate(Bucket=BUCKET, Prefix=prefix) for o in p.get("Contents", [])]

    sink = pathlib.Path(tempfile.mkdtemp(prefix="rv_sd3_"))

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
    for name, ks in sets.items():
        for k in ks:
            mirror(k)
        counts[name] = len(ks)
    chars = sorted(k for k in keys("bbg/") if k.endswith("/characteristics.parquet"))
    counts["characteristics"] = chars[-1] if chars else None

    served = {}
    for table in ("canonical_shape", "trade_schedule"):
        per_date = {}
        for k in keys(pre("rivalfunds", "etfs", "gold", table, "date=")):
            if k.endswith(".parquet"):
                d = k.split("date=")[1][:10]
                per_date[d] = max(per_date.get(d, ""), k)
        frames = []
        for d, k in per_date.items():
            df = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()))
            df["_date"] = d
            frames.append(df)
        served[table] = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    newest = max(served["canonical_shape"]["_date"])

    from rivalfunds import enrichment_bloomberg, gold_canonical_shape, gold_peer_group_map, gold_trade_schedule

    ev = {"mode": "replay", "batch_id": "sd3-dry", "sink": f"local:{sink}", "date": newest}
    res = {"g0": gold_peer_group_map.handler_entry(dict(ev, mode="daily"))}
    if chars:
        cd = chars[-1].split("/")[1]
        res["g4"] = enrichment_bloomberg.handler_entry({"mode": "import-market", "characteristics": str(mirror(chars[-1])),
                                                        "date": cd, "batch_id": "sd3-g4", "sink": f"local:{sink}"})
    res["g1"] = gold_canonical_shape.handler_entry(dict(ev))
    res["g5"] = gold_trade_schedule.handler_entry(dict(ev))

    def local(table):
        d = sink / BUCKET / pre("rivalfunds", "etfs", "gold", table, "date=")
        frames = []
        for p in sorted(d.rglob("*.parquet")):
            df = pd.read_parquet(p)
            df["_date"] = p.parent.name.split("date=")[1][:10]
            frames.append(df)
        if not frames:
            return pd.DataFrame()
        df = pd.concat(frames, ignore_index=True)
        if "dataset_revision" in df.columns:  # newest revision per date, as the readers take it
            df = df[df["dataset_revision"].astype(str) == df.groupby("_date")["dataset_revision"].transform("max").astype(str)]
        return df

    g1n, g5n = local("canonical_shape"), local("trade_schedule")
    g1s, g5s = served["canonical_shape"], served["trade_schedule"]
    fc = lambda df: df["fund_ticker"].astype(str).str.strip() if "fund_ticker" in df.columns else df["fund_id"].astype(str)  # noqa: E731

    out = {"inputs": counts, "newest_report_date": newest, "stage_results": {k: str(v)[:240] for k, v in res.items()},
           "per_fund": {}}
    funds = sorted(set(fc(g1s)) | set(fc(g1n)))
    for f in funds:
        a, b = g1s[fc(g1s) == f], g1n[fc(g1n) == f]
        ra, rb = a.groupby("_date").size(), b.groupby("_date").size()
        j = pd.concat([ra.rename("s"), rb.rename("n")], axis=1).fillna(0)
        nc = b[~b["is_cash_line"].astype(bool)] if len(b) and "is_cash_line" in b.columns else b
        rec = {"g1_rows_served": int(ra.sum()), "g1_rows_new": int(rb.sum()), "g1_dates_served": int(len(ra)),
               "g1_dates_new": int(len(rb)), "g1_dates_rowcount_differs": int(((j["s"] != j["n"]) & (j["s"] > 0) & (j["n"] > 0)).sum()),
               "g1_resolved_frac_new": round(float((nc["resolution_status"] == "RESOLVED").mean()), 4) if len(nc) else None,
               "g1_gics_resolved_new": int((b.get("gics_status", pd.Series(dtype=str)).astype(str) == "RESOLVED").sum())}

        def tk(df):
            if not len(df):
                return set()
            sd = df["shares_delta"].astype(float).round(6).astype(str) if "shares_delta" in df.columns else ""
            return set(df["window_end"].astype(str) + "|" + df["action"].astype(str) + "|" + sd)
        s5, n5 = g5s[fc(g5s) == f] if len(g5s) else g5s, g5n[fc(g5n) == f] if len(g5n) else g5n
        ss, ns = tk(s5), tk(n5)
        cls = "home" if f in HOME else "other"
        rec.update({"g5_trades_served": len(ss), "g5_trades_new": len(ns), "g5_removed": len(ss - ns),
                    "g5_added": len(ns - ss), "g5_class_of_differences": cls,
                    "g5_examples": sorted(list((ss - ns))[:2]) + sorted(list((ns - ss))[:2])})
        out["per_fund"][f] = rec
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps({"inputs": counts, "newest": newest}, default=str))
    for f, rec in out["per_fund"].items():
        print(f, {k: rec[k] for k in ("g1_rows_served", "g1_rows_new", "g1_dates_rowcount_differs", "g1_resolved_frac_new",
                                      "g1_gics_resolved_new", "g5_trades_served", "g5_trades_new", "g5_removed", "g5_added")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
