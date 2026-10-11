"""r4_daily_bronze.py -- MDPF_CANON round 4, the issuer's read of the daily chain's FIRST new-home bronze delivery (2.0.0_SA_COO~D1).

Round-3 analysis @ae094ea51d section 3 item 1: "The Inflection feed's first new-home daily delivery is read in the same pass" as the
Monday fire read. The bronze is pulled by Stage 0 of the runner's daily dispatch (mdpf-daily-dispatch.sh), not by the 13:30Z gold fire,
so this read is timed to the dispatch, not to the fire. Read-only: it lists and gets, never puts.

Usage (repo root):
  python <this file> --run-date 2026-10-11 --since 2026-10-11T06:00:00Z

--since is an instant AFTER the CloudOps on-demand pull of 2026-10-11 (ledger mdpf-canon-r3-bronze-intake-dell1-20261011, closed 05:06Z),
so an object written at or after it was written by the daily chain, not by the hand pull.

Arms:
  1 PULL     the builder's partition for --run-date holds nine model_<id>.json and _meta/pull_complete.json, and the sentinel's
             LastModified is at or after --since (the daily wrote it)
  2 STEP     the runner's telemetry history holds a run with run_date == --run-date whose STAGE0-BRONZE step reads status ok
  3 FEEDER   each of the three Inflection feeds (model_composition, model_aua_positions, non_model_aua) holds an object whose
             LastModified is at or after --since (the feeder ran on the new home)
  4 OLDHOME  the old bronze prefix holds NO object with LastModified at or after --since (the writer no longer writes there)
Prints one line per arm and "ROUND 4 BRONZE-HOME: <k> of 4 arms"; exit 0 only when every arm passes.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
sys.path[:0] = [os.path.join(ROOT, "lib")]

import boto3  # noqa: E402
from opal_naming import address  # noqa: E402

FEEDS = ("model_composition", "model_aua_positions", "non_model_aua")
MDPF_BUCKET = "opal-data-mdpf"
OLD_PREFIX = "mdpf/bronze/orion_model_composition/"
TELEM_HISTORY = "telemetry/mdpf-daily-runner/history/"


def _list(s3, bucket, prefix):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        out.extend(page.get("Contents", []))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-date", required=True, help="YYYY-MM-DD, the daily run's date")
    ap.add_argument("--since", required=True, help="ISO UTC instant after the hand pull, e.g. 2026-10-11T06:00:00Z")
    a = ap.parse_args()
    since = dt.datetime.fromisoformat(a.since.replace("Z", "+00:00"))
    s3 = boto3.client("s3", region_name="us-east-1")
    arms = []

    # 1 PULL
    uri = address("mdpf", "inflection", "bronze", "orion_model_composition", "date=" + a.run_date)
    bucket, key = uri[len("s3://"):].split("/", 1)
    objs = _list(s3, bucket, key.rstrip("/") + "/")
    models = [o for o in objs if os.path.basename(o["Key"]).startswith("model_") and o["Key"].endswith(".json")]
    sent = [o for o in objs if o["Key"].endswith("_meta/pull_complete.json")]
    fresh = bool(sent) and sent[0]["LastModified"] >= since
    ok = len(models) == 9 and len(sent) == 1 and fresh
    arms.append(("PULL", ok, "%s: %d model file(s), %d sentinel(s), sentinel LastModified %s (since %s)" % (
        uri, len(models), len(sent), sent[0]["LastModified"].isoformat() if sent else "none", since.isoformat())))

    # 2 STEP
    hist = _list(s3, MDPF_BUCKET, TELEM_HISTORY)
    found = None
    for o in sorted(hist, key=lambda x: x["LastModified"], reverse=True)[:40]:
        doc = json.loads(s3.get_object(Bucket=MDPF_BUCKET, Key=o["Key"])["Body"].read())
        if doc.get("run_date") == a.run_date:
            found = doc
            break
    if found is None:
        arms.append(("STEP", False, "no telemetry history run with run_date %s among the newest 40 of %d" % (a.run_date, len(hist))))
    else:
        steps = {s.get("name"): s.get("status") for s in ((found.get("progress") or {}).get("steps_done") or [])}
        arms.append(("STEP", steps.get("STAGE0-BRONZE") == "ok",
                     "run %s status %s: STAGE0-BRONZE %s" % (found.get("run_id"), found.get("status"), steps.get("STAGE0-BRONZE"))))

    # 3 FEEDER
    miss = []
    for feed in FEEDS:
        fo = _list(s3, MDPF_BUCKET, "mdpf/feeds/%s/inflection/" % feed)
        newest = max(fo, key=lambda x: x["LastModified"], default=None)
        state = newest["LastModified"].isoformat() if newest else "none"
        print("  feed %s: newest %s %s" % (feed, os.path.basename(newest["Key"]) if newest else "-", state))
        if newest is None or newest["LastModified"] < since:
            miss.append(feed)
    arms.append(("FEEDER", not miss, "%d of %d feeds written at or after %s%s" % (
        len(FEEDS) - len(miss), len(FEEDS), since.isoformat(), "; not written: " + ", ".join(miss) if miss else "")))

    # 4 OLDHOME
    oo = _list(s3, MDPF_BUCKET, OLD_PREFIX)
    late = [o for o in oo if o["LastModified"] >= since]
    arms.append(("OLDHOME", not late, "%d of %d old-prefix object(s) written at or after %s" % (len(late), len(oo), since.isoformat())))

    for i, (name, ok, line) in enumerate(arms, 1):
        print("ARM %d %s: %s -- %s" % (i, name, "PASS" if ok else "FAIL", line))
    k = sum(1 for _, ok, _ in arms if ok)
    print("ROUND 4 BRONZE-HOME: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
