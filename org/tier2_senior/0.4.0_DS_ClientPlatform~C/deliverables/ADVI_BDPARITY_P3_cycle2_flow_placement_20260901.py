"""P3-EXACT cycle 2 -- the flow-placement test over ALL THREE periods (gate precondition ii).

1.0.0_SA_CTO 90838 s.3(ii): a convention registered on a third of the population is a definition
asserted over an unexamined majority. This runs the QTD test over YTD and 1Y as well, and
characterises the accounts flow placement provably CANNOT explain.

Loads the 1Y window ONCE (2025-08-28..2026-08-28) and derives YTD from it as a date subset, because
the periods nest -- source-read at parity_period_returns.py:330-396 @2762f02f6a, where the only
period-conditional branches are two `period == "SI"` cases.

ZERO vendor egress. Every count prints its denominator.
"""
import csv
import io

import boto3
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import s3fs

GOLD = "opal-data-49financial"
SILVER = "opal-data-assets"
XREF = "blackdiamond/49f/silver/dim_account_xref/"
CELLS = "org/tier2_senior/0.4.0_DS_ClientPlatform~Y/deliverables/ADVI_BDPARITY_P2-2_CELLS_20260901.csv"
EXCL = "org/tier2_senior/0.4.0_DS_ClientPlatform~Y/deliverables/ADVI_BDPARITY_P2-2_NOTCOMPARABLE_ACCOUNTS_20260901.csv"

WINDOWS = {"QTD": ("2026-07-01", "2026-08-28"),
           "YTD": ("2026-01-01", "2026-08-28"),
           "1Y": ("2025-08-28", "2026-08-28")}


def main():
    s3 = boto3.client("s3")
    pag = s3.get_paginator("list_objects_v2")
    xkey = sorted(o["Key"] for pg in pag.paginate(Bucket=SILVER, Prefix=XREF)
                  for o in pg.get("Contents", []) if o["Key"].endswith("data.parquet"))[-1]
    xr = pd.read_parquet(io.BytesIO(s3.get_object(Bucket=SILVER, Key=xkey)["Body"].read()))
    xr = xr[xr["bd_account_id"].notna() & xr["schwab_account_id"].notna()]
    m = {str(b)[3:]: str(s) for b, s in zip(xr["bd_account_id"], xr["schwab_account_id"])}
    print("XREF %s | mapped ids %d" % (xkey, len(m)))

    fs = s3fs.S3FileSystem(skip_instance_cache=True, use_listings_cache=False)
    files = sorted(f for f in fs.find("%s/gold/advi/canonical/twr_daily/" % GOLD)
                   if f.endswith("data.parquet"))
    lo, hi = WINDOWS["1Y"]
    win = [f for f in files if lo <= f.split("date=")[1][:10] <= hi]
    print("1Y-window partitions: %d of %d in history" % (len(win), len(files)))
    fr = []
    for f in win:
        sch = pq.read_schema(f, filesystem=fs).names
        cols = [c for c in ["account_id", "r_net", "bmv", "emv", "cf_net"] if c in sch]
        t = pq.read_table(f, filesystem=fs, columns=cols).to_pandas()
        t["_d"] = f.split("date=")[1][:10]
        fr.append(t)
    df = pd.concat(fr, ignore_index=True)
    for c in ["r_net", "bmv", "emv", "cf_net"]:
        df[c] = pd.to_numeric(df.get(c), errors="coerce")
    df["acct"] = df["account_id"].astype(str)
    df = df[df["r_net"].notna()].copy()
    df["cf"] = df["cf_net"].fillna(0.0)
    num = df["emv"] - df["bmv"] - df["cf"]
    base = df["bmv"] + df["cf"]
    df["alt"] = np.where((base > 0) & (df["cf"] != 0), num / base, df["r_net"])
    print("rows %d | accounts %d" % (len(df), df.acct.nunique()))

    ex = {r["bd_account_id"] for r in csv.DictReader(open(EXCL))}
    cells = [r for r in csv.DictReader(open(CELLS)) if r["bd"] not in ex and r["bd"] in m]
    for r in cells:
        r["our_days"] = int(r["our_days"])
        r["bd_days"] = int(r["bd_days"])
        r["delta_bp"] = float(r["delta_bp"])

    print("\n=== FLOW-PLACEMENT TEST, ALL THREE PERIODS (gate precondition ii) ===")
    for per in ("QTD", "YTD", "1Y"):
        lo, hi = WINDOWS[per]
        d = df[(df["_d"] >= lo) & (df["_d"] <= hi)]
        g = d.groupby("acct")
        our = g["r_net"].apply(lambda s: (1.0 + s).prod() - 1.0)
        alt = g["alt"].apply(lambda s: (1.0 + s).prod() - 1.0)
        pred = (our - alt) * 1e4
        sel = [r for r in cells if r["period"] == per]
        large = {m[r["bd"]] for r in sel if r["cls"] == "LARGE" and r["our_days"] == r["bd_days"]}
        ctl = {m[r["bd"]] for r in sel if r["cls"] == "EXACT" and r["our_days"] == r["bd_days"]} - large
        obs = {m[r["bd"]]: r["delta_bp"] for r in sel
               if r["cls"] == "LARGE" and r["our_days"] == r["bd_days"]}

        def flowrate(s):
            dd = d[d["acct"].isin(s)]
            if not len(dd):
                return 0.0, 0
            fl = dd[dd["cf"] != 0]
            return 100.0 * fl.acct.nunique() / dd.acct.nunique(), dd.acct.nunique()
        lr, ln = flowrate(large)
        cr, cn = flowrate(ctl)
        pairs = [(o, float(pred.get(a, np.nan))) for a, o in obs.items()
                 if a in pred.index and np.isfinite(pred.get(a, np.nan))]
        o = np.array([q[0] for q in pairs])
        p = np.array([q[1] for q in pairs])
        movers = p != 0
        zero = int((~movers).sum())
        ratio = np.abs(o[movers]) / np.maximum(np.abs(p[movers]), 1e-9)
        sign = int(np.sum(np.sign(o[movers]) == np.sign(p[movers])))
        print("\n  %s  window %s..%s" % (per, lo, hi))
        print("     LARGE both-sides-linked accts %-5d  flow-bearing %5.1f%%   | EXACT control %-5d  flow-bearing %5.1f%%"
              % (ln, lr, cn, cr))
        print("     separation                    %.1fx" % (lr / cr if cr else float("nan")))
        print("     accts with a prediction %-5d | MOVERS %-5d | ZERO-SENSITIVITY %-5d (%4.1f%% UNEXPLAINABLE by placement)"
              % (len(p), int(movers.sum()), zero, 100.0 * zero / max(1, len(p))))
        if movers.sum():
            print("     |obs|/|pred| median %.2f (p25 %.2f p75 %.2f) | SIGN agreement %d of %d (%.1f%%)"
                  % (np.median(ratio), np.percentile(ratio, 25), np.percentile(ratio, 75),
                     sign, int(movers.sum()), 100.0 * sign / int(movers.sum())))
            print("     median |predicted| on LARGE %.2f bp | on EXACT control %.4f bp"
                  % (float(np.median(np.abs(p))),
                     float(np.median(np.abs(pred.reindex(list(ctl)).dropna()))) if ctl else -1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
