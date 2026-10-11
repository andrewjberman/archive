"""r2_daily.py -- MDPF_CANON, the issuer's read of the first scheduled daily write (2.0.0_SA_COO~D1).

Round-1 analysis @409182ae5a section 3, items 1 and 5: the 13:30Z fire of 2026-10-10 is the daily path's first real write.
This is an issuer read, not a cell. It grades CN-a-2 AC3 and FWD-1 REALIZED. Read-only: it lists and gets, never puts.

Usage (repo root):
  python <this file> snapshot              record every key + ETag under the 16 address() prefixes (run BEFORE the fire)
  python <this file> read --fire <ISO-UTC> grade the fire against the snapshot (run the tick AFTER the fire)

The partition date is the producer's own: the newest partition each series holds whose LastModified is at or after
--fire. It is never predicted from the calendar.
Arms (read), amended 2026-10-11 (round-2 analysis @71e85b7191 section 2: a fire whose as-of did not advance writes no new
partition by design, so "written at/after the fire" fails a correct producer). The unit is the partition AT THE T-1 FRONTIER,
frontier = lib/trading_calendar.prev_trading_day(fire date) (Friday is Monday's answer; Saturday's too):
  1 CURRENT    each of the 4 scopes x 3 legacy-sourced artifacts holds a partition dated the frontier at the key address()
               names (the listing is taken under the address() prefix, so the key IS builder output). Written by this fire or
               already there (unchanged) both pass; the line says which. A series whose newest date is behind the frontier
               fails and prints how many trading days behind.
  2 UNCHANGED  every snapshot key is still present with its snapshot ETag (history never rewritten); denominator printed.
  3 PARITY     for every series' frontier partition whose legacy dated JSON exists in opal-data-assets (portal/gold/mdpf/
               {scope}/{type}/{date}.json), the stored rows, decoded, equal the writer's own records_for(legacy) taken through
               the same pyarrow table. Values, not bytes: parquet bytes carry the encoder's version (the Lambda's layer writes
               arrow 20.0.0), so a local re-encode differs byte-wise on equal figures. The global scope must have at least one
               compared partition, and every compared partition must match.
  4 UNITS      account_units holds a partition dated at or after the frontier for 49financial, inflection and global
               (it is dated by the assignment day, which can be the fire date).
Prints one line per arm and "ROUND 2 DAILY: <k> of 4 arms"; exit 0 only when every arm passes.
"""
import argparse
import datetime as dt
import io
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
sys.path[:0] = [os.path.join(ROOT, "lib"), os.path.join(ROOT, "data/mdpf/scripts/gold")]

import boto3  # noqa: E402
import pyarrow as pa  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
from opal_naming import address  # noqa: E402

import mdpf_gold_parquet as gp  # noqa: E402
import trading_calendar as tc  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, "r2_daily_snapshot.json")
SCOPES = ["49financial", "inflection", "cottonwood", "global"]
LEGACY_TYPE = {"aum_metrics": "aum-metrics", "account_distribution": "account-distribution",
               "aggregate_aua_timeseries": "aggregate-aua-timeseries", "account_units": "account-units"}
LEGACY_BUCKET = "opal-data-assets"
UNITS_SCOPES = ["49financial", "inflection", "global"]


def prefix(scope, artifact):
    """(bucket, key prefix) of the series, from address()."""
    uri = address("mdpf", scope, "gold", artifact, "date=0000-00-00")
    bucket, key = uri[len("s3://"):].split("/", 1)
    return bucket, key[: key.rindex("date=")]


def listing(s3, scope, artifact):
    bucket, pfx = prefix(scope, artifact)
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=pfx):
        out.extend(page.get("Contents", []))
    return bucket, out


def snapshot(s3):
    snap, n = {}, 0
    for scope in SCOPES:
        for artifact in gp.ARTIFACTS:
            bucket, objs = listing(s3, scope, artifact)
            snap["%s/%s" % (scope, artifact)] = {o["Key"]: o["ETag"] for o in objs}
            n += len(objs)
            print("SNAPSHOT %s/%s: %d object(s) in %s" % (scope, artifact, len(objs), bucket))
    with open(SNAP, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"taken_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "series": snap}, f,
                  indent=1, sort_keys=True)
    print("SNAPSHOT: %d object(s) across %d series -> %s" % (n, len(snap), os.path.relpath(SNAP, ROOT)))


def date_of(key):
    return key.split("date=")[1].split("/")[0]


def read(s3, fire):
    snap = json.load(open(SNAP, encoding="utf-8"))["series"]
    frontier = tc.prev_trading_day(fire.date())
    print("FRONTIER %s (prev_trading_day of fire date %s)" % (frontier, fire.date()))
    arms, new = [], {}
    gone, moved, kept = [], [], 0
    for scope in SCOPES:
        for artifact in gp.ARTIFACTS:
            bucket, objs = listing(s3, scope, artifact)
            now = {o["Key"]: o for o in objs}
            for k, etag in snap.get("%s/%s" % (scope, artifact), {}).items():
                if k not in now:
                    gone.append(k)
                elif now[k]["ETag"] != etag:
                    moved.append(k)
                else:
                    kept += 1
            pq_objs = [o for o in objs if o["Key"].endswith("/data.parquet")]
            cur = [o for o in pq_objs if date_of(o["Key"]) == frontier.isoformat()]
            newest = max((date_of(o["Key"]) for o in pq_objs), default=None)
            new[(scope, artifact)] = (bucket, cur, newest, [o for o in cur if o["LastModified"] >= fire])
    # 1 CURRENT
    want = [(s, a) for s in SCOPES for a in gp.ARTIFACTS if a != "account_units"]
    miss = []
    for s, a in want:
        _, cur, newest, wrote = new[(s, a)]
        behind = tc.trading_days_behind(newest, frontier) if newest else None
        state = "at frontier, %s" % ("WRITTEN by this fire" if wrote else "already present (unchanged)") if cur             else "BEHIND by %s trading day(s), newest %s" % (behind, newest)
        print("  %s/%s: %s" % (s, a, state))
        if not cur:
            miss.append(s + "/" + a)
    arms.append(("CURRENT", not miss, "%d of %d series hold a partition at the frontier %s%s"
                 % (len(want) - len(miss), len(want), frontier, "; behind: " + ", ".join(miss) if miss else "")))
    # 2 UNCHANGED
    total = kept + len(gone) + len(moved)
    arms.append(("UNCHANGED", total > 0 and not gone and not moved,
                 "%d of %d snapshot key(s) kept their ETag; gone %d, rewritten %d" % (kept, total, len(gone), len(moved))))
    # 3 PARITY
    legacy = boto3.client("s3")
    cmp_n, ok_n, glob_n, bad = 0, 0, 0, []
    for (scope, artifact), (bucket, fresh, _newest, _wrote) in sorted(new.items()):
        if artifact == "account_units":
            continue
        for o in fresh:
            date = date_of(o["Key"])
            src = "portal/gold/mdpf/%s/%s/%s.json" % (scope, LEGACY_TYPE[artifact], date)
            payload = gp._read(legacy, LEGACY_BUCKET, src)
            if payload is None:
                continue
            want = pa.Table.from_pylist(gp.records_for(artifact, json.loads(payload))).to_pylist()
            have = pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=o["Key"])["Body"].read())).to_pylist()
            cmp_n += 1
            glob_n += scope == "global"
            if have == want:
                ok_n += 1
            else:
                bad.append("%s/%s/%s" % (scope, artifact, date))
    arms.append(("PARITY", cmp_n > 0 and glob_n > 0 and not bad,
                 "%d of %d frontier partition(s) value-equal to the writer's records of their legacy JSON (global compared: %d)%s"
                 % (ok_n, cmp_n, glob_n, "; differ " + ", ".join(bad) if bad else "")))
    # 4 UNITS
    for s_ in UNITS_SCOPES:
        print("  %s/account_units: newest %s" % (s_, new[(s_, "account_units")][2]))
    # account_units is dated by the assignment day, which may be the fire date (inflection read 2026-10-10 on the 10-10 fire):
    # the rule is a newest date at or after the frontier, never before it.
    umiss = [s for s in UNITS_SCOPES
             if not (new[(s, "account_units")][2] and new[(s, "account_units")][2] >= frontier.isoformat())]
    arms.append(("UNITS", not umiss, "%d of %d scopes hold an account_units partition at or after the frontier%s"
                 % (len(UNITS_SCOPES) - len(umiss), len(UNITS_SCOPES), "; missing " + ", ".join(umiss) if umiss else "")))
    for i, (name, ok, line) in enumerate(arms, 1):
        print("ARM %d %s: %s -- %s" % (i, name, "PASS" if ok else "FAIL", line))
    k = sum(1 for _, ok, _ in arms if ok)
    print("ROUND 2 DAILY: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["snapshot", "read"])
    ap.add_argument("--fire", help="ISO UTC instant of the fire, e.g. 2026-10-10T13:30:00Z")
    a = ap.parse_args()
    s3 = boto3.client("s3")
    if a.mode == "snapshot":
        snapshot(s3)
        return 0
    if not a.fire:
        ap.error("read needs --fire")
    return read(s3, dt.datetime.fromisoformat(a.fire.replace("Z", "+00:00")))


if __name__ == "__main__":
    sys.exit(main())
