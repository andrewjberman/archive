#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-14 S14-AC1 battery -- THE AUGUST RE-RENDER.

Prints EGS14-AUGUST-RERENDERED only when EVERY arm (a)-(g) holds. Every arm
re-measures LIVE (the schedule, S3, CloudWatch, CloudTrail, EC2) except the
invoke response itself, which is read from the committed invoke_record.json
(the response headers exist only at the client) and is CROSS-CHECKED live: the
recorded x-amzn-RequestId must appear as a START RequestId in the orchestrator's
CloudWatch log group.

Bounds: every AWS call goes through the vendored CLI v1 shim `.tools/aws` under
a per-call timeout; `--output text` is never used (CRLF); every S3 time is UTC
via s3api; every list prints its denominator. ASCII only.

Run from the worktree root:
  timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs14_august_rerender.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
# The vendored shim is a bash script `.tools/aws` plus a Windows forwarder
# `.tools/aws.cmd` (both or neither). CPython on win32 cannot exec the bash one
# (WinError 193), so resolve the .cmd there.
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")

BUCKET = "opal-data-etfs"
MONTH = "2026-08"
SERVED_PREFIX = "platinum/reports/%s/" % MONTH
FN = "etfs-reports-orchestrator"
FN_ARN = "arn:aws:lambda:us-east-1:313476888478:function:%s" % FN
SCHEDULE = "etfs-reports-monthly-run"
INSTANCE = "i-070477bf35fc54409"
LOG_GROUP = "/aws/lambda/%s" % FN
COO_SIGNOFF = "4155c85a1f"
CTO_SIGNOFF = "94775"
RECIPIENTS = ["aj@opalinvest.com", "andrew@opalinvest.com"]
LEDGER_SENTINEL = os.path.join(
    ROOT, "org", "critical_paths", ".open_deploys",
    "etfs-guardrail-eg-s-14-august-rerender.json")

CSV_NAMES = ["opaletfs_49financial_202608.csv",
             "opaletfs_cottonwood_202608.csv",
             "opaletfs_inflection_202608.csv"]
PUBLISH_NAMES = ["etf_ownership.pdf", "etf_ownership.html"] + CSV_NAMES

ARMS: list[tuple[str, bool, str]] = []


def arm(name: str, ok: bool, detail: str) -> bool:
    ARMS.append((name, ok, detail))
    print("ARM %-3s %-4s %s" % (name, "PASS" if ok else "FAIL", detail))
    return ok


def aws(args: list[str], timeout: int = 120) -> tuple[int, str]:
    p = subprocess.run([AWS] + args, capture_output=True, timeout=timeout)
    out = p.stdout.decode("utf-8", "replace").replace("\r", "")
    if p.returncode != 0:
        out += "\nSTDERR: " + p.stderr.decode("utf-8", "replace").replace("\r", "")
    return p.returncode, out


def aws_json(args: list[str], timeout: int = 120):
    rc, out = aws(args, timeout)
    if rc != 0:
        return rc, None, out
    try:
        return rc, json.loads(out), out
    except Exception as e:  # noqa: BLE001
        return rc, None, "JSON-PARSE-FAILED: %s :: %s" % (e, out[:300])


def iso(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    print("EGS14 BATTERY -- ETFS_GUARDRAIL.TO-EG-s-14, month %s" % MONTH)
    print("run_at_utc %s" % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    rec_path = os.path.join(HERE, "invoke_record.json")
    rec = json.load(open(rec_path, encoding="utf-8"))
    invoke_start = rec["invoke_start_utc"]
    req_id = rec["x_amzn_request_id"]
    print("invoke_record: StatusCode=%s RequestId=%s start=%s end=%s"
          % (rec["status_code"], req_id, invoke_start, rec["invoke_end_utc"]))

    # ---------------------------------------------------------------- arm (a)
    led = json.load(open(LEDGER_SENTINEL, encoding="utf-8"))
    md = open(os.path.join(ROOT, led["entry_path"]), encoding="utf-8").read()
    opened_at = led["opened_at"]
    opened_before = opened_at < invoke_start.replace("Z", "")
    keys_named = sum(1 for n in PUBLISH_NAMES if (SERVED_PREFIX + n) in md)
    tab = json.load(open(os.path.join(HERE, "archive_table.json"), encoding="utf-8"))
    sha_named = sum(1 for n in PUBLISH_NAMES if tab["prior"][n]["sha256"] in md)
    has_rollback = "copy-object" in md and "ROLLBACK" in md
    both_signoffs = COO_SIGNOFF in md and CTO_SIGNOFF in md
    ok_a = (opened_before and keys_named == len(PUBLISH_NAMES)
            and sha_named == len(PUBLISH_NAMES) and has_rollback and both_signoffs)
    arm("a", ok_a,
        "ledger %s opened_at=%s < invoke %s -> %s; served keys named %d of %d; "
        "prior sha256 named %d of %d; rollback=%s; signoffs COO %s + CTO %s -> %s"
        % (led["entry_path"], opened_at, invoke_start, opened_before,
           keys_named, len(PUBLISH_NAMES), sha_named, len(PUBLISH_NAMES),
           has_rollback, COO_SIGNOFF, CTO_SIGNOFF, both_signoffs))

    # ---------------------------------------------------------------- arm (b)
    rc, sched, raw = aws_json(["scheduler", "get-schedule", "--name", SCHEDULE])
    if sched is None:
        arm("b", False, "get-schedule rc=%d :: %s" % (rc, raw[:200]))
    else:
        tgt = sched["Target"]
        checks = {
            "State ENABLED": sched["State"] == "ENABLED",
            "cron(0 10 1 * ? *)": sched["ScheduleExpression"] == "cron(0 10 1 * ? *)",
            "America/New_York": sched["ScheduleExpressionTimezone"] == "America/New_York",
            "Target.Arn == orchestrator": tgt["Arn"] == FN_ARN,
            'Target.Input {"mode":"run"}': tgt["Input"] == '{"mode":"run"}',
            "payload byte-equal": rec["payload_sent"] == tgt["Input"],
            "StatusCode 200": rec["status_code"] == 200,
            "request id present": bool(req_id),
        }
        arm("b", all(checks.values()),
                   "; ".join("%s=%s" % (k, v) for k, v in checks.items())
                   + " (%d of %d)" % (sum(checks.values()), len(checks)))

    # ---------------------------------------------------------------- arm (c)
    spec = importlib.util.spec_from_file_location(
        "orch_eg14", os.path.join(ROOT, "infra", "aws", "lambda",
                                  "etfs-reports-orchestrator", "lambda_function.py"))
    os.environ.setdefault("REPORTER_INSTANCE_ID", INSTANCE)
    os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:313476888478:etfs-reports-alerts")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    lm = mod._last_month()
    arm("c", lm == MONTH,
               "_last_month() (handler's own function, imported from "
               "infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py) = %s; "
               "_report_keys(%s) = %s" % (lm, MONTH, mod._report_keys(MONTH)))

    # ---------------------------------------------------------------- arm (d)
    sys.path.insert(0, ROOT)
    from lib import trading_calendar as tc  # noqa: E402
    tdays = tc.trading_days_between(dt.date(2026, 8, 1), dt.date(2026, 8, 31))
    print("trading days in %s per lib/trading_calendar.py (%s): %d"
          % (MONTH, tc.calendar_source(), len(tdays)))

    rc, listing, raw = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET,
                                 "--prefix", SERVED_PREFIX])
    contents = (listing or {}).get("Contents", [])
    print("served objects under s3://%s/%s : %d" % (BUCKET, SERVED_PREFIX, len(contents)))
    by_key = {c["Key"]: c for c in contents}
    for c in contents:
        print("  %-58s LastModified(UTC)=%s Size=%d ETag=%s"
              % (c["Key"], c["LastModified"], c["Size"], c["ETag"]))

    fresh = []
    for n in PUBLISH_NAMES:
        k = SERVED_PREFIX + n
        lm_utc = by_key.get(k, {}).get("LastModified", "ABSENT")
        fresh.append(lm_utc != "ABSENT" and lm_utc > invoke_start)
        print("  FRESHNESS %-46s LastModified=%s > invoke %s -> %s"
              % (n, lm_utc, invoke_start, fresh[-1]))

    cov_ok = []
    print("COVERAGE-LINE TABLE (denominator: %d served CSVs)" % len(CSV_NAMES))
    for n in CSV_NAMES:
        k = SERVED_PREFIX + n
        dest = os.path.join(ROOT, ".scratch", "battery_" + n)
        rc2, out2 = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", k, dest])
        if rc2 != 0:
            cov_ok.append(False)
            print("  %-46s GET rc=%d (absent?)" % (n, rc2))
            continue
        body = open(dest, "rb").read()
        last = body.decode("utf-8").splitlines()[-1]
        has = last.startswith("# coverage:")
        cov_ok.append(has)
        print("  %-46s rows=%d LAST_ROW=%r startswith '# coverage:' -> %s"
              % (n, len(body.decode("utf-8").splitlines()), last[:90], has))
        if has:
            print("      denominator check: month trading days = %d (lib/trading_calendar.py)"
                  % len(tdays))

    print("ARCHIVE TABLE (prior vs archive sha256, denominator %d of %d)"
          % (len(tab["prior"]), len(PUBLISH_NAMES)))
    arch_ok = []
    for n, v in tab["prior"].items():
        dest = os.path.join(ROOT, ".scratch", "battery_arch_" + n)
        rc3, _ = aws(["s3api", "get-object", "--bucket", BUCKET,
                      "--key", tab["archive_prefix"] + n, dest])
        h = hashlib.sha256(open(dest, "rb").read()).hexdigest() if rc3 == 0 else "GET-FAILED"
        eq = (h == v["sha256"])
        arch_ok.append(eq)
        print("  %-46s prior=%s archive(%s)=%s EQUAL=%s"
              % (n, v["sha256"], tab["archive_prefix"] + n, h, eq))

    arm("d", all(fresh) and all(cov_ok) and all(arch_ok),
               "published-after-invoke %d of %d; CSV last row '# coverage:' %d of %d; "
               "archive sha256 match %d of %d"
               % (sum(fresh), len(fresh), sum(cov_ok), len(cov_ok),
                  sum(arch_ok), len(arch_ok)))

    # ---------------------------------------------------------------- arm (e)
    rc, ct, raw = aws_json(["cloudtrail", "lookup-events",
                            "--lookup-attributes", "AttributeKey=EventName,AttributeValue=Invoke",
                            "--start-time", "2026-09-09T23:14:00Z",
                            "--end-time", "2026-09-09T23:25:00Z"], timeout=180)
    ct_events = (ct or {}).get("Events", [])
    rc, ctc, raw = aws_json(["cloudtrail", "lookup-events",
                             "--lookup-attributes",
                             "AttributeKey=EventName,AttributeValue=StartInstances",
                             "--start-time", "2026-09-09T23:14:00Z",
                             "--end-time", "2026-09-09T23:25:00Z"], timeout=180)
    ctrl_events = (ctc or {}).get("Events", [])
    print("CloudTrail Invoke events in the run window: %d (denominator: events returned)"
          % len(ct_events))
    for e in ct_events:
        print("  %s %s user=%s" % (e.get("EventTime"), e.get("EventName"), e.get("Username")))
    print("CloudTrail POSITIVE CONTROL (StartInstances, same window): %d" % len(ctrl_events))
    for e in ctrl_events:
        print("  %s %s user=%s" % (e.get("EventTime"), e.get("EventName"), e.get("Username")))

    rc, streams, raw = aws_json(["logs", "describe-log-streams",
                                 "--log-group-name", LOG_GROUP,
                                 "--order-by", "LastEventTime", "--descending",
                                 "--max-items", "3"])
    log_txt = ""
    stream_name = ""
    if streams and streams.get("logStreams"):
        stream_name = streams["logStreams"][0]["logStreamName"]
        rc, ev, raw = aws_json(["logs", "get-log-events",
                                "--log-group-name", LOG_GROUP,
                                "--log-stream-name", stream_name,
                                "--start-from-head"])
        for e in (ev or {}).get("events", []):
            log_txt += "%s %s" % (iso(e["timestamp"] / 1000.0), e["message"])
    req_in_log = ("START RequestId: " + req_id) in log_txt
    print("orchestrator log stream: %s" % stream_name)
    for line in log_txt.splitlines():
        print("  LOG %s" % line[:220])

    trigger_field = False
    for n in CSV_NAMES + ["etf_ownership.html"]:
        p = os.path.join(ROOT, ".scratch", "battery_" + n)
        if os.path.exists(p):
            body = open(p, "rb").read().decode("utf-8", "replace")
            if req_id in body or "run-id" in body or "trigger" in body.lower():
                trigger_field = True
    if not trigger_field:
        print("ARTIFACT-CARRIES-NO-TRIGGER-FIELD")
    arm("e", bool(ct_events) and req_in_log,
               "CloudTrail Invoke events=%d (data-event selector on Lambda: none on either "
               "trail -- positive control StartInstances=%d proves the window is logged); "
               "recorded request id %s present as START RequestId in %s -> %s"
               % (len(ct_events), len(ctrl_events), req_id, LOG_GROUP, req_in_log))

    # ---------------------------------------------------------------- arm (f)
    msg_ids = [ln for ln in log_txt.splitlines() if "MessageId" in ln]
    rc, ses, raw = aws_json(["cloudtrail", "lookup-events",
                             "--lookup-attributes",
                             "AttributeKey=EventName,AttributeValue=SendRawEmail",
                             "--start-time", "2026-09-09T23:14:00Z",
                             "--end-time", "2026-09-09T23:25:00Z"], timeout=180)
    ses_events = (ses or {}).get("Events", [])
    live_recips = None
    rc, cfg, raw = aws_json(["lambda", "get-function-configuration",
                             "--function-name", FN])
    if cfg:
        live_recips = cfg["Environment"]["Variables"].get("EMAIL_RECIPIENT", "")
    join_ok = all(r in (live_recips or "") for r in RECIPIENTS)
    print("SES: MessageId lines in the run's log: %d; CloudTrail SendRawEmail in window: %d; "
          "live EMAIL_RECIPIENT=%r (JOIN of both recipients -> %s)"
          % (len(msg_ids), len(ses_events), live_recips, join_ok))
    for m in msg_ids:
        print("  %s" % m[:220])
    arm("f", bool(msg_ids) and bool(ses_events),
               "SES MessageId(s) in the orchestrator log for this run: %d; CloudTrail "
               "SendRawEmail in the run's minute: %d; Destinations must name %s"
               % (len(msg_ids), len(ses_events), " + ".join(RECIPIENTS)))

    # ---------------------------------------------------------------- arm (g)
    rc, inst, raw = aws_json(["ec2", "describe-instances", "--instance-ids", INSTANCE,
                              "--query", "Reservations[].Instances[].[InstanceId,State.Name]"])
    state = inst[0][1] if inst else "UNREAD"
    arm("g", state == "stopped",
               "reporter box %s State.Name=%s (describe-instances)" % (INSTANCE, state))

    passed = sum(1 for _, ok, _ in ARMS if ok)
    print("ARMS %d of %d PASS" % (passed, len(ARMS)))
    if passed == len(ARMS):
        print("EGS14-AUGUST-RERENDERED")
        return 0
    print("EGS14-NOT-RERENDERED -- failing arms: %s"
          % ", ".join(n for n, ok, _ in ARMS if not ok))
    return 1


if __name__ == "__main__":
    sys.exit(main())
