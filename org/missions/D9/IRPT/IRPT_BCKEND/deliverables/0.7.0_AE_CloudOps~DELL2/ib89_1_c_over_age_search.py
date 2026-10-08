#!/usr/bin/env python3
"""IB89-1 arm (c) -- LAPTOP-RUN: the over-age search read, and an HONEST drivability check first.

WHY A FILE: standing rule 1.0.0_SA_CTO~DELL2 msg 215, and TO IB-pr-377 BOUNDS ("No read of
opal-data-* firm buckets from dell2").

READ THIS BEFORE RUNNING -- arm (c) IS NOT UNCONDITIONALLY DRIVABLE, and that is a measured
property of the DEPLOYED code, not an opinion:

  * The configured handler of irpt-directory-search is `entry.lambda_handler`, which the deployed
    entry.py builds as `lambda_handler = _entry.lambda_entry(ENTRY)`.
  * `directory_fixture` -- the injection point that could force an over-age directory -- exists
    ONLY in the legacy `handler.py` inside the same zip, which entry.py's own header describes as
    the thing it replaced ("WHAT CHANGED AND WHY IT IS A SECURITY CHANGE, NOT A REFACTOR").
    Measured 2026-10-08 on the UNZIPPED LIVE zip: 'directory_fixture' appears in handler.py and
    in NO other deployed member.
  * So the over-age branch cannot be injected through the served door. It fires only when a firm's
    directory `as_of_business_date` is genuinely more than expiry.MAX_AGE_TRADING_DAYS (2) trading
    days behind, or when the age cannot be computed.

THEREFORE this script does TWO things and never conflates them:
  STEP 1  measure each firm's current directory age from latest.json -> is arm (c) drivable NOW?
  STEP 2  only for a firm that IS over-age, issue the search and record the {_data,_status}
          envelope, asserting DIRECTORY_OVER_AGE/STALE (or CALENDAR_UNAVAILABLE/UNCERTAIN).

If no firm is over-age the verdict is NOT_DRIVABLE -- which is a REPORT, not a pass and not a
failure. The over-age branch itself is already proven against the DEPLOYED expiry.py by arm (e)
of the five-arm controlled-clock drive (mechanism driven deliberately, no calendar wait); what
this arm adds is the live served envelope, and that needs a really-aged directory.

NO _data CONTENT IS EVER WRITTEN OUT: only the hit COUNT and the _status envelope. The directory
is client data.

ASCII only. Read-only. No vendor call. No write of any kind.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

import boto3

FUNCTION = "irpt-directory-search"
LATEST = "investor-reporting/directory/latest.json"
MAX_AGE_TRADING_DAYS = 2  # expiry.MAX_AGE_TRADING_DAYS in the deployed zip
FIRMS = {"49financial": "opal-data-bd",
         "inflection": "opal-data-inf",
         "cottonwood": "opal-data-cot"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--query", default="a", help="search term; content is never written out")
    a = ap.parse_args()

    s3 = boto3.client("s3")
    res = {"arm": "IB89-1-(c) over-age search read",
           "function": FUNCTION, "max_age_trading_days": MAX_AGE_TRADING_DAYS,
           "run_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "firms": {}, "verdict": None,
           "note": ("arm (c) is drivable only against a genuinely over-age directory; the deployed "
                    "entry.py has no directory_fixture injection point (security change)")}

    # AGE ON THE TRADING-DAY FRONTIER, never a weekday subtraction (CLAUDE.md: one frontier,
    # lib/trading_calendar.py). The first version of this script computed no age at all and left
    # `over_age` empty, so it could only ever answer NOT_DRIVABLE -- a verdict that would have
    # looked like a measurement. Fixed before first use.
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    *([os.pardir] * 7) ) )
    sys.path.insert(0, "lib")
    import trading_calendar as tc  # noqa: E402

    today = dt.date.today()
    over_age = []
    for firm, bucket in sorted(FIRMS.items()):
        row = {"bucket": bucket, "latest_key": LATEST}
        try:
            latest = json.loads(s3.get_object(Bucket=bucket, Key=LATEST)["Body"].read())
            as_of = latest.get("as_of_business_date") or latest.get("as_of")
            row["as_of_business_date"] = as_of
            row["directory_revision"] = latest.get("directory_revision")
            if as_of:
                behind = tc.trading_days_behind(dt.date.fromisoformat(str(as_of)[:10]), today)
                row["trading_days_behind"] = behind
                row["ceiling"] = MAX_AGE_TRADING_DAYS
                row["over_age"] = behind > MAX_AGE_TRADING_DAYS
                if row["over_age"]:
                    over_age.append(firm)
            else:
                row["over_age"] = None
                row["note"] = "no as_of on latest.json -- age CANNOT be computed, which is the CALENDAR_UNAVAILABLE/UNCERTAIN arm, not an over-age one"
        except Exception as exc:  # noqa: BLE001
            row["error"] = "%s: %s" % (type(exc).__name__, exc)
        res["firms"][firm] = row

    res["age_basis"] = "freshness_basis: trading-day-frontier (lib/trading_calendar.py)"
    res["drivable_firms"] = over_age
    res["verdict"] = "NOT_DRIVABLE" if not over_age else "DRIVABLE"

    if over_age:
        lam = boto3.client("lambda")
        for firm in over_age:
            r = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse",
                           Payload=json.dumps({"firm_token": firm, "q": a.query}).encode("utf-8"))
            payload = json.loads(r["Payload"].read().decode("utf-8", "replace"))
            body = payload.get("body")
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except ValueError:
                    body = {"_unparsed": True}
            status = (body or {}).get("_status")
            data = (body or {}).get("_data")
            res["firms"][firm]["served"] = {
                "status_envelope": status,              # the envelope IS the finding
                "data_hit_count": len(data) if isinstance(data, list) else None,
                "reason_code": (status or {}).get("reason_code") if isinstance(status, dict) else None,
                "state": (status or {}).get("state") if isinstance(status, dict) else None,
            }
        codes = {res["firms"][f]["served"].get("reason_code") for f in over_age}
        res["verdict"] = "PASS" if codes <= {"DIRECTORY_OVER_AGE", "CALENDAR_UNAVAILABLE"} and codes else "FAIL"

    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("arm (c) %s -> %s" % (res["verdict"], a.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
