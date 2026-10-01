"""RIV-i-1 AC2 (amendment 2) -- identity never moves a trade: BASG's trade schedule, replayed by the branch's code over the
SERVED inputs of a bounded window, equals what is served today (row Z-S8: round-3 identity made a security's key flip
between resolved and unresolved across a window, and the flips read as 1489 added / 322 removed BASG trades).

READ-ONLY against S3. Window: BASG report dates 2026-01-02 .. 2026-02-17 (the dry run's densest churn: 52 entries+exits
on 2026-01-13, 50 on 2026-02-17). Mirrors: issuer silver + issuer bronze sidecars for the window, the BASG Bloomberg silver
objects for the window (named BASG-<capture>.parquet), the newest served G3. Replays G0, G1 and G5 for the window into a
local sink, then compares BASG G5 against the newest SERVED G5 object per date on an identity-independent key
(window_end, action, shares_delta rounded to 1e-6):
  - removed == 0 and added == 0;
  - control: at least 20 served BASG trades fall in the window (the comparison is not vacuous);
  - control: BASG's G1 in the window carries RESOLVED rows (identity is on, not switched off to pass)."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

LO, HI = "2026-01-02", "2026-02-17"
BUCKET = "opal-data-etfs"


def run(v):
    c.setup_path()
    import boto3
    import pandas as pd
    from rivalfunds import gold_canonical_shape, gold_peer_group_map, gold_trade_schedule

    s3 = boto3.client("s3")
    pg = s3.get_paginator("list_objects_v2")
    keys = lambda p: [o["Key"] for pp in pg.paginate(Bucket=BUCKET, Prefix=p) for o in pp.get("Contents", [])]  # noqa: E731
    inwin = lambda k: "date=" in k and LO <= k.split("date=")[1][:10] <= HI  # noqa: E731
    sink = c.tmpdir("rv_i1b_")
    want = [k for k in keys("issuer-site/etfs/silver/holdings/") if inwin(k)]
    want += [k for k in keys("issuer-site/etfs/bronze/holdings/") if inwin(k) and k.endswith(".json")]
    want += [k for k in keys("bloomberg/etfs/silver/holdings/") if inwin(k) and k.rsplit("/", 1)[-1].startswith("BASG-")]
    want += sorted(keys("rivalfunds/etfs/gold/corporate_actions/"))[-1:]
    for k in want:
        c.mirror_s3(sink, f"s3://{BUCKET}/{k}")
    print(f"mirrored {len(want)} objects for {LO}..{HI}")
    ev = {"mode": "replay", "batch_id": "i1-ac2", "sink": f"local:{sink}", "date": HI, "start": LO, "end": HI}
    gold_peer_group_map.handler_entry(dict(ev, mode="daily"))
    gold_canonical_shape.handler_entry(dict(ev))
    gold_trade_schedule.handler_entry(dict(ev))

    def newest_local(table):
        fr = []
        for p in sorted(c.gold_dir(sink, table).rglob("*.parquet")):
            df = pd.read_parquet(p)
            df["_date"] = p.parent.name[5:15]
            fr.append(df)
        if not fr:
            return pd.DataFrame()
        df = pd.concat(fr, ignore_index=True)
        return df[df["dataset_revision"].astype(str) == df.groupby("_date")["dataset_revision"].transform("max").astype(str)]

    g1, g5 = newest_local("canonical_shape"), newest_local("trade_schedule")
    served = []
    per_date = {}
    for k in keys("rivalfunds/etfs/gold/trade_schedule/"):
        if k.endswith(".parquet") and inwin(k):
            d = k.split("date=")[1][:10]
            per_date[d] = max(per_date.get(d, ""), k)
    for d, k in per_date.items():
        served.append(pd.read_parquet(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read())))
    s5 = pd.concat(served, ignore_index=True) if served else pd.DataFrame()
    isb = lambda df: df["fund_id"].astype(str).isin(["BASG", "4823"]) if len(df) else []  # noqa: E731
    tk = lambda df: set(df["window_end"].astype(str) + "|" + df["action"].astype(str) + "|"  # noqa: E731
                        + df["shares_delta"].astype(float).round(6).astype(str)) if len(df) else set()
    ss, ns = tk(s5[isb(s5)] if len(s5) else s5), tk(g5[isb(g5)] if len(g5) else g5)
    print(f"BASG trades in window: served {len(ss)}, branch {len(ns)}; removed {len(ss - ns)}, added {len(ns - ss)}")
    print("  removed e.g.", sorted(ss - ns)[:3], " added e.g.", sorted(ns - ss)[:3])
    v.check(len(ss) >= 20, f"control: >= 20 served BASG trades in the window ({len(ss)})")
    v.check(not (ss - ns) and not (ns - ss), "BASG trades unchanged by identity (0 removed, 0 added)")
    b1 = g1[g1["fund_ticker"].astype(str).str.strip() == "BASG"] if len(g1) else g1
    v.check(len(b1) > 0 and (b1["resolution_status"] == "RESOLVED").any(), "control: BASG G1 carries RESOLVED rows")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
