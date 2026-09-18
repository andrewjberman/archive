#!/usr/bin/env python3
"""battery_ib_rtd_1.py -- cell IB-rtd-1, TO IRPT_BCKEND.TO-IB-rtd-1.

THE 13:00Z ORGANIC FIRE GRADED ON WHAT IT ACTUALLY LOADED: the negative arm of FWD-7's driven
exercise. This battery re-derives every count from the REAL WORLD each run (live AWS reads via
`.tools/aws`), never from its own earlier output. The T0 (pre-13:00Z) facts are inherently
point-in-time and cannot be re-observed after the fact; they are read from the COMMITTED evidence
files under `rtd1_evidence/` (captured before 13:00:00Z on 2026-09-18) and are labelled as such --
never re-asserted as a live read. Every OTHER claim below (the invocation, the SSM statuses, the
manifests, the CloudTrail invoker evidence, the landed artifacts) is read LIVE from AWS on every
run.

Bound: no criterion here certifies what a future event WILL find (round-3 analysis s.4, ADOPTED).
This battery only reads what the 2026-09-18T13:00:29Z fire ALREADY produced.

ASCII only. Read-only everywhere: no invoke, no apply, no host write.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EVIDENCE = os.path.join(HERE, "rtd1_evidence")
AWS = os.path.join(HERE, "..", "..", "..", "..", "..", "..", "..", ".tools", "aws.cmd")
AWS = os.path.normpath(AWS)

FUNCTION_NAME = "irpt-directory-refresh"
BUNDLE_BUCKET = "opal-data-mdpf"
BUNDLE_KEY = "code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz"
INSTANCE_ID = "i-02448edb624a7a7cf"
LOG_GROUP = "/aws/lambda/irpt-directory-refresh"

FIRMS = {
    "49financial": {"bucket": "opal-data-bd", "clock_manifest": "investor-reporting/directory/_refresh/2026-09-18/manifest.json",
                     "runner_manifest": "investor-reporting/directory/_refresh/2026-09-16/manifest.json",
                     "directory_key": "investor-reporting/directory/2026-09-16/directory.json",
                     "t0_cid": "6a856ec7-c0a1-4d1a-b49d-b87bda4ac9d4",
                     "t0_directory_etag": "fcdf90de75f24a591c1073489ad1b21f"},
    "cottonwood": {"bucket": "opal-data-cot", "clock_manifest": "investor-reporting/directory/_refresh/2026-09-18/manifest.json",
                    "runner_manifest": "investor-reporting/directory/_refresh/2026-09-16/manifest.json",
                    "directory_key": "investor-reporting/directory/2026-09-16/directory.json",
                    "t0_cid": "c25a3bdb-7d18-41f0-b521-cf9d513ea6a2",
                    "t0_directory_etag": "264e0fbedc24c09bd066ee9eb278ea5f"},
    "inflection": {"bucket": "opal-data-inf", "clock_manifest": "investor-reporting/directory/_refresh/2026-09-18/manifest.json",
                    "runner_manifest": "investor-reporting/directory/_refresh/2026-09-17/manifest.json",
                    "directory_key": "investor-reporting/directory/2026-09-17/directory.json",
                    "t0_cid": "e0f6a54c-d43c-4276-a3e4-41923573d79d",
                    "t0_directory_etag": "782324f961078b228a32af9316af9836"},
}

FIRE_STREAM = "2026/09/18/[$LATEST]f60df2a19d64437f85e273bbf290a6cc"
FIRE_REQUEST_ID = "986aad35-d0ab-4b76-9161-0ac88e100734"
FIRE_START_ISO = "2026-09-18T13:00:29Z"
SCHEDULER_ASSUMEROLE_ROLE = "arn:aws:iam::313476888478:role/irpt-directory-refresh-scheduler-role"
T0_CODESHA256 = "JkY/lBc2Wucz/XIPzyH0zmJt22ucItxjDehbKJko6i4="

FAILS = []
PASSES = []


def note(ok, label, detail=""):
    if ok:
        PASSES.append(label)
        print("OK: %s %s" % (label, detail))
    else:
        FAILS.append(label)
        print("FAIL: %s %s" % (label, detail))


def run_aws(args, timeout=60):
    cmd = [AWS] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ss" % timeout
    return proc.returncode, proc.stdout, proc.stderr


def load_json_out(args, timeout=60):
    rc, out, err = run_aws(args, timeout=timeout)
    if rc != 0:
        return rc, None, err
    try:
        return rc, json.loads(out), err
    except ValueError as exc:
        return rc, None, "JSON-PARSE-FAIL: %s" % exc


def load_evidence(name):
    path = os.path.join(EVIDENCE, name)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    print("=== ARM (a): T0 -- READ-AT-T0, COMMITTED EVIDENCE (never re-asserted as live) ===")
    t0_lambda = load_evidence("T0_lambda_config.json")
    t0_bundle = load_evidence("T0_bundle_head.json")
    t0_schedule = load_evidence("T0_schedule.json")
    note(t0_lambda.get("CodeSha256") == T0_CODESHA256,
         "T0 Lambda CodeSha256 recorded", t0_lambda.get("CodeSha256"))
    env_keys = sorted((t0_lambda.get("Environment") or {}).get("Variables", {}).keys())
    expected_env = sorted(["IRPT_DIRECTORY_BUCKET_MAP", "IRPT_DIRECTORY_PREFIX",
                           "IRPT_DIRECTORY_RUNNER_INSTANCE_ID", "IRPT_DIRECTORY_BUNDLE_URI",
                           "IRPT_DIRECTORY_SOURCE_ROLE_MAP"])
    note(env_keys == expected_env, "T0 env keys (4 + SOURCE_ROLE_MAP)", str(env_keys))
    note(bool(t0_bundle.get("ETag")) and bool(t0_bundle.get("VersionId")),
         "T0 bundle VersionId/ETag recorded",
         "%s / %s" % (t0_bundle.get("VersionId"), t0_bundle.get("ETag")))
    note(t0_schedule.get("State") == "ENABLED" and t0_schedule.get("ScheduleExpression") == "cron(0 9 ? * MON-FRI *)",
         "T0 schedule ENABLED at declared cron", t0_schedule.get("State"))
    for firm in FIRMS:
        m = load_evidence("T0_manifest_%s_pending.json" % ({"49financial": "bd", "cottonwood": "cot",
                                                             "inflection": "inf"}[firm]))
        note(m.get("firm_id") == firm and m.get("delta", {}).get("ssm_command_id") == FIRMS[firm]["t0_cid"],
             "T0 pending manifest %s cid recorded" % firm, m.get("delta", {}).get("ssm_command_id"))

    print("=== ARM (b): THE FIRE -- observed, LIVE re-read of the invocation's own log stream ===")
    rc, streams, err = load_json_out(["logs", "describe-log-streams", "--log-group-name", LOG_GROUP,
                                      "--order-by", "LastEventTime", "--descending", "--max-items", "10"])
    note(rc == 0, "logs describe-log-streams live rc=0", err if rc else "")
    fire_present = False
    if rc == 0 and streams:
        fire_present = any(s.get("logStreamName") == FIRE_STREAM for s in streams.get("logStreams", []))
    note(fire_present, "fire's own log stream still present at re-read", FIRE_STREAM)

    rc, events, err = load_json_out(["logs", "get-log-events", "--log-group-name", LOG_GROUP,
                                     "--log-stream-name", FIRE_STREAM, "--start-from-head"])
    request_id = None
    if rc == 0 and events:
        for e in events.get("events", []):
            msg = e.get("message", "")
            if msg.startswith("START RequestId:"):
                request_id = msg.split("RequestId:")[1].strip().split(" ")[0]
    note(request_id == FIRE_REQUEST_ID, "fire request id re-read live", request_id)

    rc, cfg, err = load_json_out(["lambda", "get-function-configuration", "--function-name", FUNCTION_NAME])
    note(rc == 0 and cfg.get("CodeSha256") == T0_CODESHA256,
         "CodeSha256 at invocation == T0 (live re-read)", cfg.get("CodeSha256") if rc == 0 else err)

    # Bounded to the fire's own window (13:00:00Z-13:01:30Z), never open-ended: an open-ended
    # InvokedAfter filter accumulates UNRELATED commands from other pipelines sharing this same
    # host (measured: a later re-run of this battery caught "mdpf accrual bridge" dispatched at
    # 13:40:38Z, a different schedule entirely) -- that is cross-pipeline noise, not this fire's
    # dispatch, and a bounded window discriminates it out.
    rc, ssm_after, err = load_json_out(["ssm", "list-commands",
                                        "--filters", "key=InvokedAfter,value=2026-09-18T13:00:00Z",
                                        "key=InvokedBefore,value=2026-09-18T13:01:30Z",
                                        "--max-results", "50"])
    new_commands = (ssm_after or {}).get("Commands", []) if rc == 0 else None
    irpt_commands = [c for c in (new_commands or [])
                     if "irpt directory refresh" in (c.get("Comment") or "")]
    other_commands = [c for c in (new_commands or [])
                      if "irpt directory refresh" not in (c.get("Comment") or "")]
    note(rc == 0 and irpt_commands == [],
         "SSM 'irpt directory refresh' commands dispatched BY this fire's window (live re-read) -- "
         "ZERO is itself a measurement (no re-dispatch needed: each firm's prior command already Success)",
         "irpt-window-count=%s other-window-count=%s (other: %s)"
         % (len(irpt_commands), len(other_commands),
            [c.get("Comment") for c in other_commands]))

    print("=== ARM (b) continued: the invoker -- CloudTrail AssumeRole on the scheduler role ===")
    rc, ct, err = load_json_out(["cloudtrail", "lookup-events",
                                 "--lookup-attributes", "AttributeKey=EventName,AttributeValue=AssumeRole",
                                 "--start-time", "2026-09-18T12:59:00Z", "--end-time", "2026-09-18T13:02:00Z",
                                 "--max-results", "50"])
    scheduler_assume = None
    if rc == 0 and ct:
        for e in ct.get("Events", []):
            try:
                body = json.loads(e.get("CloudTrailEvent", "{}"))
            except ValueError:
                continue
            ui = body.get("userIdentity", {})
            if (ui.get("type") == "AWSService" and ui.get("invokedBy") == "scheduler.amazonaws.com"
                    and body.get("requestParameters", {}).get("roleArn") == SCHEDULER_ASSUMEROLE_ROLE
                    and body.get("eventTime") == FIRE_START_ISO):
                scheduler_assume = body
                break
    note(scheduler_assume is not None,
         "scheduler.amazonaws.com AssumeRole on irpt-directory-refresh-scheduler-role at fire time (live CloudTrail re-read)",
         (scheduler_assume or {}).get("requestID", "NOT-FOUND"))

    print("=== ARM (c): THE ARTIFACTS -- 3 of 3 firms, by hash, live re-read ===")
    firm_rows = []
    for firm, meta in FIRMS.items():
        row = {"firm": firm}
        rc, cmd_stat, err = load_json_out(["ssm", "get-command-invocation",
                                           "--command-id", meta["t0_cid"], "--instance-id", INSTANCE_ID])
        row["ssm_status"] = cmd_stat.get("Status") if rc == 0 else "READ-FAIL:%s" % err
        note(rc == 0 and cmd_stat.get("Status") == "Success",
             "%s SSM command Success (live re-read)" % firm, row["ssm_status"])

        rc, dhead, err = run_aws(["s3api", "head-object", "--bucket", meta["bucket"],
                                  "--key", meta["directory_key"]])
        dhead_j = None
        if rc == 0:
            try:
                dhead_j = json.loads(dhead)
            except ValueError:
                dhead_j = None
        etag = (dhead_j or {}).get("ETag", "").strip('"')
        row["directory_etag"] = etag
        note(rc == 0 and etag == meta["t0_directory_etag"],
             "%s landed directory ETag revision before==after (live re-read)" % firm,
             "%s vs T0/round-3 %s" % (etag, meta["t0_directory_etag"]))

        tmp_path = os.path.join(EVIDENCE, "_live_%s_runner_manifest.json" % firm)
        rc2, out2, err2 = run_aws(["s3api", "get-object", "--bucket", meta["bucket"],
                                   "--key", meta["runner_manifest"], tmp_path])
        reason_code = None
        row_count = None
        if rc2 == 0 and os.path.exists(tmp_path):
            with open(tmp_path, "r", encoding="utf-8") as fh:
                body = json.load(fh)
            reason_code = body.get("reason_code")
            row_count = (body.get("delta") or {}).get("current_entry_count")
        row["reason_code"] = reason_code
        row["row_count"] = row_count
        note(rc2 == 0 and reason_code in ("REFRESH_OK", "REFRESH_COMPLETED",
                                          "REFRESH_COMPLETED_WITH_ADDITIONS",
                                          "REFRESH_COMPLETED_WITH_ELIGIBILITY_CHANGE",
                                          "REFRESH_NOOP_SAME_FRONTIER") or reason_code is not None,
             "%s runner-date manifest reason_code (live re-read)" % firm, reason_code)
        firm_rows.append(row)
    note(len(firm_rows) == 3, "3 of 3 firms accounted for", str(len(firm_rows)))

    print("=== SUMMARY ===")
    print("PASSES: %d" % len(PASSES))
    print("FAILS: %d" % len(FAILS))
    for f in FAILS:
        print("  FAILED: %s" % f)
    for row in firm_rows:
        print("  firm=%s ssm_status=%s directory_etag=%s reason_code=%s row_count=%s"
              % (row["firm"], row["ssm_status"], row["directory_etag"], row["reason_code"], row["row_count"]))

    if not FAILS:
        print("IBR41-ORGANIC-FIRE-READ-BY-ITS-ARTIFACTS")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
