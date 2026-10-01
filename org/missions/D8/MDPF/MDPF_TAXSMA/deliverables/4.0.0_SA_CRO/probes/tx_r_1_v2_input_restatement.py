"""Does the INPUT itself restate 2026-09-28 and 2026-09-29? SmartX fact_model_aum_daily: each partition's `day`
column carries the full history, and the Gold function reads only the latest partition. Compare the two newest
partitions at the restated days. Read-only."""
import io

import boto3
import pandas as pd
import pyarrow.parquet as pq

B, P = "opal-data-assets", "smartx/platform/silver/fact_model_aum_daily/"
s3 = boto3.client("s3")
parts = {}
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix=P):
    for o in page.get("Contents", []):
        seg = [s for s in o["Key"].split("/") if s.startswith("date=")]
        if seg and o["Key"].endswith(".parquet"):
            parts.setdefault(seg[0][5:], []).append((o["Key"], o["LastModified"].strftime("%Y-%m-%dT%H:%MZ")))
dates = sorted(parts)
print("partitions: %d, newest three: %s" % (len(dates), [(d, parts[d][0][1]) for d in dates[-3:]]))


def load(d):
    frames = [pq.read_table(io.BytesIO(s3.get_object(Bucket=B, Key=k)["Body"].read()),
                            columns=["rmid", "day", "closing_equity"]).to_pandas() for k, _ in parts[d]]
    df = pd.concat(frames, ignore_index=True)
    df["_day"] = pd.to_datetime(df["day"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["closing_equity"] = pd.to_numeric(df["closing_equity"], errors="coerce").fillna(0.0)
    return df


old, new = load(dates[-2]), load(dates[-1])
for day in ("2026-09-25", "2026-09-28", "2026-09-29"):
    a = old[old["_day"] == day].groupby("rmid")["closing_equity"].sum()
    b = new[new["_day"] == day].groupby("rmid")["closing_equity"].sum()
    j = pd.concat([a.rename("old"), b.rename("new")], axis=1).fillna(0.0)
    j["delta"] = (j["new"] - j["old"]).round(2)
    moved = j[j["delta"].abs() > 0.004]
    print("day %s: models %d | models whose closing_equity differs between partition %s and %s: %d | sum of deltas %+.2f | deltas %s"
          % (day, len(j), dates[-2], dates[-1], len(moved), moved["delta"].sum(), sorted(moved["delta"].tolist())[:8]))
