"""FAST-lease never-widen instrument -- the SERVED delta of an A1 code change, measured THROUGH each stage's own
handler_entry (the path the Lambda runs), never by calling build() over cached frames.

Why: the addendum-4 apply (ledger etfs-rivalfunds-fast-a1-r5) served a trend that still carried SCHY's index futures,
although an in-process build() over cached G1 had predicted their removal: gold_buying_trend.handler_entry read G1 with a
narrower column list than the cache carried. This instrument runs, for one page day, the three A1 producers'
handler_entry (rk-1 holding_contribution, tb-1 buying_trend, ic-1 input_census) on an OVERLAY sink -- every read from
S3, every write to a local directory -- and diffs each against the SERVED newest object of the same table and day.
READ-ONLY against S3. Run from a tree at the candidate pin:

    python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round5/served_delta_a1.py --day 2026-10-01 --out <json>

Prints, per table: the served object, rows served / new, rows changed, and per-fund counts; for holding_contribution
the per-fund YTD totals that move and the refused-day count; for buying_trend the index-line count and SCHY's sector
leans. ASCII only.
"""
from __future__ import annotations

import argparse
import io
import json
import pathlib
import subprocess
import sys
import tempfile


def root() -> pathlib.Path:
    return pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                                       check=True).stdout.strip())


class Overlay:
    kind = "overlay"

    def __init__(self, base, local):
        self.base, self.local = base, local

    def get(self, uri):
        return self.local.get(uri) if self.local.exists(uri) else self.base.get(uri)

    def exists(self, uri):
        return self.local.exists(uri) or self.base.exists(uri)

    def list(self, prefix):
        return sorted(set(self.base.list(prefix)) | set(self.local.list(prefix)))

    def put(self, uri, data, content_type=None):
        return self.local.put(uri, data, content_type)

    def served_only(self, prefix):
        return sorted(self.base.list(prefix))


KEYS = {"holding_contribution": ["fund_id", "period", "axis", "bucket"],
        "buying_trend": ["fund_id", "axis", "lean", "rank"],
        "input_census": ["date", "input_kind", "subject", "fund_id"]}
VALUE = {"holding_contribution": "contribution", "buying_trend": "net_notional_base", "input_census": "status"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True, help="the page day (YYYY-MM-DD)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    r = root()
    for p in (str(r / "data" / "etfs" / "scripts"), str(r)):
        sys.path.insert(0, p)
    import pandas as pd
    import pyarrow.parquet as pq

    from rivalfunds import gold_buying_trend, gold_holding_contribution, gold_input_census, homes, revision, sinks

    real = sinks.get_sink
    ov = Overlay(real("s3"), sinks.LocalSink(tempfile.mkdtemp(prefix="rv_sda1_")))
    sinks.get_sink = lambda spec: ov if spec in ("overlay", "s3") else real(spec)
    out = {"day": args.day, "tables": {}}
    for table, mod in (("holding_contribution", gold_holding_contribution), ("buying_trend", gold_buying_trend),
                       ("input_census", gold_input_census)):
        prefix = homes.address("rivalfunds", "etfs", "gold", table, f"date={args.day}") + "/"
        served_uris = [u for u in ov.served_only(prefix) if u.endswith(".parquet")]
        su = revision.newest(served_uris) if served_uris else None
        sdf = pd.read_parquet(io.BytesIO(ov.base.get(su))) if su else pd.DataFrame()
        res = mod.handler_entry({"date": args.day, "sink": "overlay"})
        nu = (res.get("outputs") or [None])[0]
        ndf = pq.read_table(io.BytesIO(ov.get(nu))).to_pandas() if nu else pd.DataFrame()
        rec = {"handler_status": res.get("status"), "served_object": su.rsplit("/", 1)[-1] if su else None,
               "new_object": nu.rsplit("/", 1)[-1] if nu else None, "rows_served": int(len(sdf)), "rows_new": int(len(ndf))}
        k, v = KEYS[table], VALUE[table]
        if len(sdf) and len(ndf) and all(c in sdf.columns and c in ndf.columns for c in k + [v]):
            m = sdf.merge(ndf, on=k, how="outer", suffixes=("_s", "_n"), indicator=True)
            if pd.api.types.is_numeric_dtype(m[f"{v}_s"]) and pd.api.types.is_numeric_dtype(m[f"{v}_n"]):
                # relative tolerance: a notional near $1e7 summed in another order differs by ~1e-9 absolute
                tol = 1e-9 * m[[f"{v}_s", f"{v}_n"]].abs().max(axis=1).clip(lower=1.0)
                same = ((m[f"{v}_s"] - m[f"{v}_n"]).abs() <= tol) | (m[f"{v}_s"].isna() & m[f"{v}_n"].isna())
            if "bucket" in k or "bucket" not in m.columns:
                pass
            elif "bucket_s" in m.columns:
                same = same & (m["bucket_s"].astype(str) == m["bucket_n"].astype(str))
            else:
                same = m[f"{v}_s"].astype(str) == m[f"{v}_n"].astype(str)
            changed = m[(m["_merge"] != "both") | ~same]
            rec["rows_changed"] = int(len(changed))
            rec["rows_changed_by_fund"] = {str(a): int(b) for a, b in changed.groupby("fund_id").size().items()}
        if table == "holding_contribution":
            def ytd(d):
                s = d[(d["axis"] == "security") & (d["period"] == "YTD")]
                return s.groupby("fund_id")["contribution"].sum().round(6)
            if len(sdf) and len(ndf):
                y = pd.concat([ytd(sdf).rename("served"), ytd(ndf).rename("new")], axis=1)
                rec["ytd_moves"] = {f: [float(a), float(b)] for f, (a, b) in y[(y["served"] - y["new"]).abs() > 1e-9].iterrows()}
            for lab, d in (("served", sdf), ("new", ndf)):
                if "n_days_refused" in d.columns:
                    s = d[(d["axis"] == "security") & (d["period"] == "YTD")]
                    rec[f"refused_days_{lab}"] = int(s["n_days_refused"].fillna(0).sum())
        if table == "buying_trend":
            for lab, d in (("served", sdf), ("new", ndf)):
                if len(d):
                    rec[f"index_lines_{lab}"] = int(d["bucket"].astype(str).str.contains(" Index").sum())
                    x = d[(d["fund_id"] == "SCHY") & (d["axis"] == "sector")].sort_values(["lean", "rank"])
                    rec[f"schy_sector_leans_{lab}"] = x[["lean", "rank", "bucket", "net_notional_base"]].round(0).values.tolist()[:4]
        out["tables"][table] = rec
        print(table, json.dumps(rec, default=str))
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
