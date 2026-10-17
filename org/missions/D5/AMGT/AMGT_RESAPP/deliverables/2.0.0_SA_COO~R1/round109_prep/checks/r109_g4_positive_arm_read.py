"""AMGT_RESAPP round-109 PREP -- `AMGT-bp-5`: the read of the G4 filings task's POSITIVE ARM (the first fire on a trading day, Mon 2026-10-19 07:30 ET = 11:30Z).

  python r109_g4_positive_arm_read.py --since 2026-10-19T11:29:00Z [--bucket opal-data-harvest]

Read-only. For the 8 keys in `lib/research/llm_batch/first_fire_limit.json` it prints, each with its denominator:
  A  the scheduled task's last run and result (Get-ScheduledTaskInfo via powershell) and whether `tmp/llm_batch/last_run.json` exists and carries `filings`;
  B  per key, the objects under `filings/v1/<key>/` and `drafting/v1/<key>.json` modified at or after --since (key, LastModified, VersionId), and the count of objects
     under `amgt/harvest/state/filing_attempt/security_key=<key>/` (baseline 0 each before the first positive run, except the AAPL HELD marker which is not one of the 8);
  C  `usage.usd` of every analysis object modified since --since, and their mean against 0.80 (above 0.80 goes to the CTO);
  D  the trigger's own reading `python -m lib.research.llm_batch.run filings --dry-run` (after a run it must read due=False, no new filing).
Prints `R109 G4 READ: <n> analysis object(s) modified since <t>, <m> drafting, mean usage.usd <x or ABSENT>, last_run.json <present|absent>` and exits 0; it grades nothing: the issuer reads the lines.
The script is exercised before use with a NEGATIVE control (--since a time after the last write: 0 modified) and a POSITIVE control (--since 2026-09-01: the stored analysis objects are listed).
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

import boto3

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([".."] * 9)))
LIMIT = os.path.join(ROOT, "lib", "research", "llm_batch", "first_fire_limit.json")
LAST_RUN = os.path.join(ROOT, "tmp", "llm_batch", "last_run.json")
TASK = "OpalResearch-FilingsAnalyzer"


def keys():
    with open(LIMIT, encoding="utf-8") as fh:
        return json.load(fh)["security_keys"]["filings"]


def parse(stamp):
    return dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def task_info():
    cmd = "$i=Get-ScheduledTaskInfo -TaskName %s; 'LastRun=' + $i.LastRunTime + ' LastResult=' + $i.LastTaskResult + ' NextRun=' + $i.NextRunTime" % TASK
    out = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=60)
    return (out.stdout or out.stderr).strip()


def list_prefix(s3, bucket, prefix):
    out, token = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        out.extend(r.get("Contents", []))
        if not r.get("IsTruncated"):
            return out
        token = r.get("NextContinuationToken")


def usage_usd(s3, bucket, key):
    body = json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read())
    node = body.get("usage") if isinstance(body, dict) else None
    val = node.get("usd") if isinstance(node, dict) else None
    return val if isinstance(val, (int, float)) and not isinstance(val, bool) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True)
    ap.add_argument("--bucket", default="opal-data-harvest")
    a = ap.parse_args()
    since = parse(a.since)
    s3 = boto3.client("s3", region_name="us-east-1")
    ks = keys()
    print("A task: " + task_info())
    present = os.path.exists(LAST_RUN)
    carries = None
    if present:
        with open(LAST_RUN, encoding="utf-8") as fh:
            carries = "filings" in json.load(fh)
    print("A last_run.json: %s%s" % ("present" if present else "absent", "" if carries is None else (", carries filings" if carries else ", no filings entry")))
    n_an = n_dr = 0
    usages = []
    for k in ks:
        an = [o for o in list_prefix(s3, a.bucket, "filings/v1/%s/" % k) if o["Key"].endswith(".analysis.json") and o["LastModified"] >= since]
        dr = [o for o in list_prefix(s3, a.bucket, "drafting/v1/%s.json" % k) if o["LastModified"] >= since]
        fa = list_prefix(s3, a.bucket, "amgt/harvest/state/filing_attempt/security_key=%s/" % k)
        n_an += len(an)
        n_dr += len(dr)
        print("B %-16s analysis modified %d | drafting modified %d | filing_attempt objects %d (baseline 0)" % (k, len(an), len(dr), len(fa)))
        for o in an + dr:
            print("    %s  %s" % (o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), o["Key"]))
        for o in an:
            u = usage_usd(s3, a.bucket, o["Key"])
            print("C   usage.usd %s  %s" % (u if u is not None else "ABSENT", o["Key"]))
            if u is not None:
                usages.append(u)
    mean = (sum(usages) / len(usages)) if usages else None
    print("C mean usage.usd: %s over %d of %d analysis object(s) (threshold 0.80)" % ("%.4f" % mean if mean is not None else "ABSENT", len(usages), n_an))
    out = subprocess.run([sys.executable, "-m", "lib.research.llm_batch.run", "filings", "--dry-run"], cwd=ROOT, capture_output=True, text=True, timeout=180)
    print("D trigger: " + (out.stdout or out.stderr).strip().splitlines()[-1])
    print("R109 G4 READ: %d analysis object(s) modified since %s, %d drafting, mean usage.usd %s, last_run.json %s" % (
        n_an, a.since, n_dr, "%.4f" % mean if mean is not None else "ABSENT", "present" if present else "absent"))


if __name__ == "__main__":
    main()
