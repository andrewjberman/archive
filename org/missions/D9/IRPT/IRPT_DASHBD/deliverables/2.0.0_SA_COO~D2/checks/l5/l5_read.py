"""IRPT_DASHBD R45 REFRESH 4, ledger leg L5 (owner 2.0.0_SA_COO~D2): the first scheduled fire after the release, read.

Release: irpt-49f-reporting-gold-lambda i2r7CbVr, LastModified 2026-10-12T13:58:42Z. Fire: 2026-10-13 11:41Z.

Usage:
  python l5_read.py                         live read (needs AWS credentials via the environment the .tools/aws shim uses)
  python l5_read.py --manifest-file <path>  CONTROL: grade one local returns manifest only (no AWS); the pre-release manifest must FAIL

Prints key NAMES, counts and booleans only. It never prints a value from the thresholds object or an account-keyed map
(first_data_date is keyed by account number and is never listed). Last line: "L5 READ CLEAN" or "L5 READ NOT CLEAN: ...".
Exit 0 only on CLEAN; "NOT FIRED" is not clean.
"""
import datetime
import json
import re
import sys

BUCKET = "opal-data-49financial"
PREFIX = "irpt/49financial/gold/account_return_daily/"
FUNCTION = "irpt-49f-reporting-gold-lambda"
RELEASE = datetime.datetime(2026, 10, 12, 13, 58, 42, tzinfo=datetime.timezone.utc)
FIRE_WINDOW_START = datetime.datetime(2026, 10, 13, 11, 30, 0, tzinfo=datetime.timezone.utc)
SIX = {"tolerance", "large_flow_share", "plausibility_band_low", "plausibility_band_high",
       "comparability_max_excluded_weight", "threshold_claims"}
CLAIMS_FIVE = SIX - {"threshold_claims"}
ADDED = {"valuation_source", "fee_treatment", "price_basis"}
DURATION_LINE_MS = 765000
MEMORY_LINE_MB = 2556.8
RUN8 = re.compile(r"\d{8,}")


def grade_manifest(m):
    """Return (list of problems, dict of printable facts) for one parsed returns manifest."""
    problems, facts = [], {}
    top = set(m)
    facts["top_level_key_count"] = len(top)
    facts["added_keys_present"] = sorted(ADDED & top)
    if not ADDED <= top:
        problems.append("added keys missing: %s" % sorted(ADDED - top))
    th = m.get("thresholds")
    if not isinstance(th, dict):
        problems.append("thresholds is not an object")
        th = {}
    facts["thresholds_key_count"] = len(th)
    facts["thresholds_key_names"] = sorted(th)
    if set(th) != SIX:
        problems.append("thresholds keys are not the six: extra %s, missing %s" % (sorted(set(th) - SIX), sorted(SIX - set(th))))
    claims = th.get("threshold_claims")
    if not isinstance(claims, dict) or set(claims) != CLAIMS_FIVE:
        problems.append("threshold_claims is not the five claims")
    facts["thresholds_has_8plus_digit_run"] = bool(RUN8.search(json.dumps(th, sort_keys=True)))
    if facts["thresholds_has_8plus_digit_run"]:
        problems.append("thresholds holds a run of 8 or more digits")
    facts["method_version"] = m.get("method_version")
    if m.get("method_version") != 2:
        problems.append("method_version is %r, not 2" % (m.get("method_version"),))
    return problems, facts


def live_read():
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    logs = boto3.client("logs", region_name="us-east-1")
    lam = boto3.client("lambda", region_name="us-east-1")
    problems = []

    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    print("live function: CodeSha256 %s, MemorySize %s, Timeout %s" % (cfg["CodeSha256"], cfg["MemorySize"], cfg["Timeout"]))
    if not cfg["CodeSha256"].startswith("i2r7CbVr"):
        problems.append("live CodeSha256 is not i2r7CbVr (moved since the release)")

    objs, token = [], None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=PREFIX)
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        objs += r.get("Contents", [])
        token = r.get("NextContinuationToken")
        if not token:
            break
    fresh = sorted([o for o in objs if o["Key"].endswith("/manifest.json") and o["LastModified"] > FIRE_WINDOW_START],
                   key=lambda o: o["LastModified"])
    print("returns objects scanned: %d; manifests written since %s: %d" % (len(objs), FIRE_WINDOW_START.isoformat(), len(fresh)))

    ev = logs.filter_log_events(logGroupName="/aws/lambda/" + FUNCTION, startTime=int(FIRE_WINDOW_START.timestamp() * 1000), filterPattern="REPORT")
    reports = [e["message"] for e in ev.get("events", [])]
    print("REPORT lines since the fire window: %d" % len(reports))
    for line in reports:
        print("  " + line.strip())
    if not fresh or not reports:
        return ["NOT FIRED: no manifest written since the window start, or no REPORT line yet (this is not a pass)"] + problems, "NOT FIRED"

    for line in reports:
        d = re.search(r"Duration: ([\d.]+) ms", line)
        mm = re.search(r"Max Memory Used: (\d+) MB", line)
        if not d or not mm:
            problems.append("a REPORT line has no Duration or Max Memory Used")
            continue
        if float(d.group(1)) >= DURATION_LINE_MS:
            problems.append("Duration %s ms is not under %d" % (d.group(1), DURATION_LINE_MS))
        if float(mm.group(1)) >= MEMORY_LINE_MB:
            problems.append("Max Memory Used %s MB is not under %s" % (mm.group(1), MEMORY_LINE_MB))
    err = logs.filter_log_events(logGroupName="/aws/lambda/" + FUNCTION, startTime=int(FIRE_WINDOW_START.timestamp() * 1000), filterPattern="?ERROR ?Traceback")
    print("ERROR/Traceback events since the window: %d" % len(err.get("events", [])))
    if err.get("events"):
        problems.append("ERROR or Traceback lines in the fire's log")

    o = fresh[-1]
    print("newest manifest: %s (LastModified %s)" % (o["Key"], o["LastModified"].isoformat()))
    body = s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()
    p, facts = grade_manifest(json.loads(body.decode("utf-8")))
    for k, v in facts.items():
        print("  %s: %s" % (k, v))
    return problems + p, None


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--manifest-file":
        with open(sys.argv[2], "rb") as f:
            problems, facts = grade_manifest(json.loads(f.read().decode("utf-8")))
        for k, v in facts.items():
            print("  %s: %s" % (k, v))
        state = None
    else:
        problems, state = live_read()
    if problems:
        print("L5 READ NOT CLEAN: " + "; ".join(problems))
        sys.exit(1)
    print("L5 READ CLEAN")


if __name__ == "__main__":
    main()
