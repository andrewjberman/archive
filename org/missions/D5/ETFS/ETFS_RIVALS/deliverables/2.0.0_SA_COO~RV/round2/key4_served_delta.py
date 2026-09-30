"""RIV-d-3 never-widen key 4 -- the served delta (1.0.0_SA_CTO~Z's refusal, msg 27419): replay the round-2 code over the
CURRENT served inputs into a LOCAL sink and diff, per fund, against what /rivalfunds serves today.

Read-only against S3 (it downloads; it never puts). Run from a tree at the merged round-2 HEAD:
    python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round2/key4_served_delta.py --out <json>

Change classes per the CTO: income, corporate_action, source, cash_line, schema, other. The pair expects other == 0.
"""
from __future__ import annotations

import argparse
import io
import json
import pathlib
import subprocess
import sys
import tempfile

BUCKET = "opal-data-etfs"


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

    sink = pathlib.Path(tempfile.mkdtemp(prefix="rv_key4_"))
    # 1. mirror the served INPUTS the round-2 gold stages read for the served fund(s): issuer silver + issuer bronze sidecars
    silver_pre = pre("issuer-site", "etfs", "silver", "holdings", "date=")
    bronze_pre = pre("issuer-site", "etfs", "bronze", "holdings", "date=")
    n_in = 0
    for k in keys(silver_pre) + [k for k in keys(bronze_pre) if k.endswith(".json")]:
        dst = sink / BUCKET / k
        dst.parent.mkdir(parents=True, exist_ok=True)
        s3.download_file(BUCKET, k, str(dst))
        n_in += 1
    # 2. the SERVED outputs to compare against (latest object per date)
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
    newest = max(served["canonical_shape"]["_date"]) if len(served["canonical_shape"]) else None
    # 3. replay the round-2 code over those inputs into the local sink (G0 from the declared map; no G3 for BASG's securities)
    from rivalfunds import gold_canonical_shape, gold_peer_group_map, gold_trade_schedule, publish_page

    ev = {"mode": "replay", "batch_id": "key4-dry", "sink": f"local:{sink}", "date": newest}
    res = {"g0": gold_peer_group_map.handler_entry(dict(ev, mode="daily")),
           "g1": gold_canonical_shape.handler_entry(dict(ev)),
           "g5": gold_trade_schedule.handler_entry(dict(ev))}
    res["page"] = publish_page.handler_entry(dict(ev, mode="daily"))

    def local(table):
        d = sink / BUCKET / pre("rivalfunds", "etfs", "gold", table, "date=")
        parts = sorted(d.rglob("*.parquet"))
        frames = []
        for p in parts:
            df = pd.read_parquet(p)
            df["_date"] = p.parent.name.split("date=")[1][:10] if "date=" in p.parent.name else None
            frames.append(df)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    new_g1, new_g5 = local("canonical_shape"), local("trade_schedule")
    out = {"inputs_mirrored": n_in, "newest_report_date": newest, "stage_results": {k: str(v)[:300] for k, v in res.items()}}
    # G1: rows per (fund, date) and column set
    fcol_s = "fund_ticker" if "fund_ticker" in served["canonical_shape"].columns else "fund_id"
    fcol_n = "fund_ticker" if "fund_ticker" in new_g1.columns else "fund_id"
    s_rows = served["canonical_shape"].groupby([fcol_s, "_date"]).size()
    n_rows = new_g1.groupby([fcol_n, "_date"]).size() if len(new_g1) else pd.Series(dtype=int)
    joined = pd.concat([s_rows.rename("served"), n_rows.rename("new")], axis=1).fillna(0)
    out["g1"] = {"served_rows": int(s_rows.sum()), "new_rows": int(n_rows.sum()),
                 "fund_dates_differing": int((joined["served"] != joined["new"]).sum()),
                 "fund_dates": int(len(joined)),
                 "columns_added": sorted(set(new_g1.columns) - set(served["canonical_shape"].columns)),
                 "columns_removed": sorted(set(served["canonical_shape"].columns) - set(new_g1.columns) - {"_date"})}
    # G5: trade identity diff, classified
    s5, n5 = served["trade_schedule"], new_g5
    def tkey(df):
        sec = "security_id" if "security_id" in df.columns else "security_key"
        fc = "fund_id" if "fund_id" in df.columns else "fund_ticker"
        we = "window_end" if "window_end" in df.columns else "_date"
        return df.assign(_k=df[fc].astype(str) + "|" + df[sec].astype(str) + "|" + df[we].astype(str) + "|" + df["action"].astype(str))
    s5k, n5k = (tkey(s5) if len(s5) else s5), (tkey(n5) if len(n5) else n5)
    s_set = set(s5k["_k"]) if len(s5k) else set()
    n_set = set(n5k["_k"]) if len(n5k) else set()
    removed, added = s_set - n_set, n_set - s_set
    cash_ids = set(new_g1.loc[new_g1.get("is_cash_line", pd.Series(False, index=new_g1.index)).astype(bool), "position_id"].astype(str)) if len(new_g1) and "position_id" in new_g1.columns else set()
    classes = {"cash_line": 0, "corporate_action": 0, "income": 0, "source": 0, "other": 0}
    examples = {c: [] for c in classes}
    for k in sorted(removed | added):
        fund, sec, we, action = k.split("|")
        row = n5k[n5k["_k"] == k] if k in added else None
        if sec in cash_ids or sec.endswith(" Curncy"):
            c = "cash_line"
        elif row is not None and len(row) and "corporate_action_ref" in row.columns and row["corporate_action_ref"].notna().any():
            c = "corporate_action"
        elif row is not None and len(row) and "income_funded" in row.columns and bool(row["income_funded"].any()):
            c = "income"
        else:
            c = "other"
        classes[c] += 1
        if len(examples[c]) < 5:
            examples[c].append(("removed" if k in removed else "added") + ": " + k)
    out["g5"] = {"served_trades": len(s_set), "new_trades": len(n_set), "removed": len(removed), "added": len(added),
                 "classes": classes, "examples": examples}
    # VALUE diff on the rows both sides share (provenance columns excluded): cells that differ, per column
    PROV = {"revision", "produced_at", "producer_version", "input_manifest", "_date", "_k", "claim", "confidence_note"}

    def cell_diff(a, b, on):
        cols = [c for c in a.columns if c in b.columns and c not in PROV and c not in on]
        if not len(a) or not len(b):
            return {"rows_compared": 0, "differing_cells": {}}
        m = a[on + cols].merge(b[on + cols], on=on, suffixes=("_s", "_n"))
        diffs = {}
        for c in cols:
            x, y = m[c + "_s"], m[c + "_n"]
            try:
                neq = ~((x == y) | (x.isna() & y.isna()) | ((x.astype(float) - y.astype(float)).abs() <= 1e-9))
            except (TypeError, ValueError):
                neq = ~((x.astype(str) == y.astype(str)) | (x.isna() & y.isna()))
            k = int(neq.sum())
            if k:
                diffs[c] = k
        return {"rows_compared": int(len(m)), "columns_compared": len(cols), "differing_cells": diffs}

    g1_on = [fcol_s, "_date"] + (["position_id"] if "position_id" in served["canonical_shape"].columns else [])
    if fcol_s == fcol_n:
        out["g1"]["values"] = cell_diff(served["canonical_shape"], new_g1, g1_on)
    if len(s5k) and len(n5k):
        out["g5"]["values"] = cell_diff(s5k.drop(columns=["_date"], errors="ignore"), n5k.drop(columns=["_date"], errors="ignore"), ["_k"])
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("inputs_mirrored", "newest_report_date", "g1", "g5")}, indent=1, default=str)[:5000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
