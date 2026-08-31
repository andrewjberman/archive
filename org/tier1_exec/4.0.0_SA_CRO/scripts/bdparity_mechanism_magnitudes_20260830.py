"""ADVI_BDPARITY BP1-4 -- the grounding measurements behind the CRO's N-bp word (4.0.0_SA_CRO, 2026-08-30).

Measures, on OUR gold twr_daily only (zero vendor egress), the magnitude of each pre-registered
convention mechanism so the classification thresholds are set on grounds independent of the BD
deltas in hand:
  [1] one-day |r_net| scale        -- what a single omitted/duplicated day does to a cumulative figure
  [2] fee events (cf_gross != cf_net) as a fraction of BMV, per event and per window (C2 amplitude)
  [3] flow-day timing sensitivity |r_EOD - r_BOD| (cash-flow timing convention, exact from bmv/emv/cf_net)
  [4] daily gross-net drag
  [A] the FALSE-CLASS rate of a single omitted day at candidate thresholds
  [B]/[C] outlier rows (surprise-channel candidates, not chased)
  [D] the fee-event calendar
Window defaults to the P1 probe window 2026-07-01..2026-08-28 (37 partitions). Reads schema-tolerantly:
2026-08-18 carries a reduced schema (BP1-4 @fa82a129d8 + @6ae366e8c0). Target-specific: bucket/prefix.
"""
import argparse

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import s3fs

BUCKET = "opal-data-49financial"
PREFIX = "gold/advi/canonical/twr_daily/"
WANT = ["account_id", "business_date", "r_net", "r_gross", "status", "bmv", "emv", "cf_net", "cf_gross"]


def pct(s, ps=(50, 90, 95, 99, 100)):
    return {("max" if p == 100 else "p%d" % p): float(np.nanpercentile(s, p)) for p in ps}


def fmt_bp(d):
    return "  ".join("%s=%.2fbp" % (k, v * 1e4) for k, v in d.items())


def load(start, end):
    fs = s3fs.S3FileSystem(skip_instance_cache=True, use_listings_cache=False)
    files = sorted(f for f in fs.find(f"{BUCKET}/{PREFIX}") if f.endswith("data.parquet"))
    want = [f for f in files if start <= f.split("date=")[1][:10] <= end]
    frames, short = [], []
    for f in want:
        sch = pq.read_schema(f, filesystem=fs).names
        cols = [c for c in WANT if c in sch]
        if len(cols) < len(WANT):
            short.append((f.split("date=")[1][:10], len(sch)))
        t = pq.read_table(f, filesystem=fs, columns=cols).to_pandas()
        if len(t):
            frames.append(t)
    df = pd.concat(frames, ignore_index=True)
    for c in ["r_net", "r_gross", "bmv", "emv", "cf_net", "cf_gross"]:
        df[c] = pd.to_numeric(df.get(c), errors="coerce")
    vint = max(fs.info(f)["LastModified"] for f in want)
    print("GOLD VINTAGE (newest write in range): %s" % vint)
    print("PARTITIONS %d of %d in history; rows %d; accounts %d; reduced-schema partitions: %s"
          % (len(want), len(files), len(df), df.account_id.nunique(), short))
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2026-07-01")
    ap.add_argument("--end", default="2026-08-28")
    a = ap.parse_args()
    df = load(a.start, a.end)
    ok = df[df.r_net.notna()].copy()
    absr = ok.r_net.abs()
    print("OK account-days (r_net non-null): %d of %d rows (%.1f%%)" % (len(ok), len(df), 100 * len(ok) / len(df)))
    print("status counts:", df.status.value_counts(dropna=False).to_dict())

    print("\n[1] |r_net| per OK account-day (one-omitted-day scale), n=%d:\n    %s" % (len(ok), fmt_bp(pct(absr))))
    sane = ok[absr <= 0.5]
    print("    excluding |r_net|>50%% rows (n=%d): %s" % (len(sane), fmt_bp(pct(sane.r_net.abs()))))

    fe = df[df.cf_gross.notna() & df.cf_net.notna() & (df.cf_gross != df.cf_net) & (df.bmv > 0)].copy()
    fe["fee_frac"] = (fe.cf_gross - fe.cf_net).abs() / fe.bmv
    print("\n[2] FEE EVENTS: %d events on %d accounts (of %d); per-event fee/BMV:\n    %s"
          % (len(fe), fe.account_id.nunique(), df.account_id.nunique(), fmt_bp(pct(fe.fee_frac))))
    print("    events per account in window: %s" % fe.groupby("account_id").size().value_counts().sort_index().to_dict())
    cum = fe.groupby("account_id").fee_frac.sum()
    print("    cumulative fee/BMV per account over the window (C2 net-leg amplitude), n=%d:\n    %s" % (len(cum), fmt_bp(pct(cum))))
    print("    fee events with fee/BMV > 100 bp: %d of %d; > 1000 bp: %d" % ((fe.fee_frac > 0.01).sum(), len(fe), (fe.fee_frac > 0.1).sum()))

    fl = df[df.cf_net.notna() & (df.cf_net != 0) & (df.bmv > 0) & df.emv.notna() & df.r_net.notna()].copy()
    fl = fl[(fl.bmv + fl.cf_net) > 0]
    fl["r_eod"] = (fl.emv - fl.cf_net) / fl.bmv - 1.0
    fl["r_bod"] = fl.emv / (fl.bmv + fl.cf_net) - 1.0
    fl["timing_diff"] = (fl.r_eod - fl.r_bod).abs()
    fl["flow_w"] = fl.cf_net.abs() / fl.bmv
    print("\n[3] FLOW DAYS (cf_net != 0, bmv > 0, emv present): %d account-days on %d accounts; |r_EOD - r_BOD|:\n    %s"
          % (len(fl), fl.account_id.nunique(), fmt_bp(pct(fl.timing_diff))))
    print("    flow weight |cf_net|/bmv: p50=%.3f p90=%.3f p99=%.3f max=%.3f" % tuple(np.nanpercentile(fl.flow_w, [50, 90, 99, 100])))
    small = fl[fl.flow_w <= 0.10]
    print("    flows <= 10%% of BMV (n=%d): %s" % (len(small), fmt_bp(pct(small.timing_diff))))

    fd = ok[ok.r_gross.notna() & (ok.r_gross != ok.r_net)]
    print("\n[4] days with r_gross != r_net: %d; |r_gross - r_net|: %s" % (len(fd), fmt_bp(pct((fd.r_gross - fd.r_net).abs()))))

    print("\n[A] FALSE-CLASS RATE OF A SINGLE OMITTED DAY: share of OK account-days with |r_net| <= X")
    for x in [0.5, 1, 2, 5, 10, 15, 25, 50]:
        print("    |r_net| <= %5.1f bp : %6.2f%%" % (x, 100 * (absr <= x * 1e-4).mean()))

    print("\n[B] TOP |r_net| among status OK (surprise-channel candidates):")
    print(ok.loc[absr.sort_values(ascending=False).index[:6],
                 ["account_id", "business_date", "status", "r_net", "r_gross", "bmv", "emv", "cf_net", "cf_gross"]].to_string(index=False))
    print("    status-OK rows with |r_net| > 50%%: %d" % int((absr > 0.5).sum()))
    print("\n[C] TOP fee/BMV events:")
    print(fe.sort_values("fee_frac", ascending=False).head(5)[["account_id", "business_date", "status", "bmv", "cf_net", "cf_gross", "fee_frac"]].to_string(index=False))
    print("\n[D] fee-event calendar (events per business_date, top 8):")
    print(fe.groupby("business_date").size().sort_values(ascending=False).head(8).to_dict())


if __name__ == "__main__":
    main()
