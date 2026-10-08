#!/usr/bin/env python3
"""IB89-1 arm (a) -- LAPTOP-RUN: one driven refresh fire, then read READY at all three firms.

WHY THIS IS A FILE AND NOT A dell2 RUN: the standing rule of 1.0.0_SA_CTO~DELL2 msg 215 --
a fenced firm-bucket read goes straight to the laptop as a FILE -- and TO IB-pr-377's BOUNDS
say "No read of opal-data-* firm buckets from dell2."

WHAT IT DOES, in order:
  1. Fires irpt-directory-refresh ONCE with {"business_date": <D>}. That is the DRIVEN form the
     deployed refresh.py documents (`_event_business_date`: "An explicit business date on the
     event, for a DRIVEN fire. Never a default."). A scheduled fire carries no business_date and
     reads the real clock; this one is explicit, so the manifest key is computed, never guessed.
  2. Reads investor-reporting/directory/_refresh/<D>/manifest.json at EACH firm bucket and
     records reason_code + directory_revision.

ARM (a) PASSES only when all three firms read READY with a non-empty revision.

The fire WRITES (one PutObject under _refresh/* per firm, by the FUNCTION's role, which
schedule.tf line 204 states is exactly what this function is permitted to write). It touches
neither latest.json nor any directory object. Nothing else is written.

ASCII only. No vendor call. Read-only apart from the one driven fire.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

import boto3

FUNCTION = "irpt-directory-refresh"
PREFIX = "investor-reporting/directory/_refresh"
# From the applied root's `firm_bucket_map` output (terraform, 2026-10-08). These are the SHORT
# names the directory release actually uses -- NOT opal-data-{49financial,inflection,cottonwood},
# which is where rows S347/S352 measured the dell2 deny. See row IRPT_BCKEND-D2-S12.
FIRMS = {"49financial": "opal-data-bd",
         "inflection": "opal-data-inf",
         "cottonwood": "opal-data-cot"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--business-date", required=True,
                    help="YYYY-MM-DD, the business date to drive the fire for")
    ap.add_argument("--out", required=True, help="result JSON path")
    ap.add_argument("--no-fire", action="store_true",
                    help="skip the fire and only read the manifests (pure read-only)")
    a = ap.parse_args()
    d = dt.date.fromisoformat(a.business_date).isoformat()

    res = {"arm": "IB89-1-(a) driven refresh fire READY manifest",
           "function": FUNCTION, "business_date": d, "fired": not a.no_fire,
           "run_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "firms": {}, "verdict": None}

    if not a.no_fire:
        lam = boto3.client("lambda")
        r = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse",
                       Payload=json.dumps({"business_date": d}).encode("utf-8"))
        payload = r["Payload"].read().decode("utf-8", "replace")
        res["fire"] = {"status_code": r.get("StatusCode"),
                       "function_error": r.get("FunctionError"),
                       "payload_sha_len": len(payload),
                       "payload": json.loads(payload) if payload.strip().startswith(("{", "[")) else payload}

    s3 = boto3.client("s3")
    ok = 0
    for firm, bucket in sorted(FIRMS.items()):
        key = "%s/%s/manifest.json" % (PREFIX, d)
        row = {"bucket": bucket, "key": key}
        try:
            body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
            m = json.loads(body)
            row["reason_code"] = m.get("reason_code")
            row["directory_revision"] = m.get("directory_revision")
            row["as_of_business_date"] = m.get("as_of_business_date")
            # counts only -- a manifest is a durable log and carries no client entries
            row["delta_counts"] = m.get("delta")
            row["ready"] = (m.get("reason_code") == "READY"
                            and bool(str(m.get("directory_revision") or "").strip()))
            if row["ready"]:
                ok += 1
        except Exception as exc:  # noqa: BLE001 -- the error IS the reading
            row["error"] = "%s: %s" % (type(exc).__name__, exc)
            row["ready"] = False
        res["firms"][firm] = row

    res["firms_ready"] = ok
    res["firms_total"] = len(FIRMS)
    res["verdict"] = "PASS" if ok == len(FIRMS) else "FAIL"
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("arm (a) %s -- %d of %d firms READY -> %s" % (res["verdict"], ok, len(FIRMS), a.out))
    return 0 if res["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
