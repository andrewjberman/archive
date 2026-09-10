#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-14 S14-AC1 battery -- THE AUGUST RE-RENDER.

Prints EGS14-AUGUST-RERENDERED only when EVERY arm (a)-(g) holds. Every arm re-measures
LIVE (the schedule, S3, CloudWatch, CloudTrail, EC2, SES, SNS) except the invoke response
itself, which is read from the committed invoke_record.json (the response headers exist
only at the client) and is CROSS-CHECKED live: the recorded x-amzn-RequestId must appear
as a START RequestId in the orchestrator's log group READ BY TIME.

ARM (e) IS THE AMENDED CUT (@5507841f04, rows W1-S13 / W2-S7): lambda:Invoke is a
CloudTrail DATA event and 0 of 2 trails in this account select AWS::Lambda::Function, so
(i) the MANUAL fire is pinned by `logs filter-log-events` over the window -- never one
stream picked by its lastEventTimestamp -- carrying the client's request id exactly once,
(ii) a RULE-initiated fire would leave `etfs-reports-scheduler-role` AssumeRole events in
the window and there must be 0, and (iii) the CloudTrail Invoke read prints COVERAGE-ABSENT
with its 2-trail denominator, never a pass and never a fail.

Bounds: every AWS call goes through the vendored CLI v1 shim under a per-call timeout;
`--output text` is never used (CRLF); every S3 time is UTC via s3api; every list prints its
denominator. ASCII only.

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
# The vendored shim is a bash script `.tools/aws` plus a Windows forwarder `.tools/aws.cmd`
# (both or neither). CPython on win32 cannot exec the bash one (WinError 193).
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")

BUCKET = "opal-data-etfs"
MONTH = "2026-08"
SERVED_PREFIX = "platinum/reports/%s/" % MONTH
FN = "etfs-reports-orchestrator"
FN_ARN = "arn:aws:lambda:us-east-1:313476888478:function:%s" % FN
SCHEDULE = "etfs-reports-monthly-run"
SCHEDULER_ROLE = "etfs-reports-scheduler-role"
INSTANCE = "i-070477bf35fc54409"
LOG_GROUP = "/aws/lambda/%s" % FN
ALERT_TOPIC = "etfs-reports-alerts"
COO_SIGNOFF = "4155c85a1f"
COO_SIGNOFF_AMENDMENT = "5507841f04"
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


def to_dt(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def iso(ts: float) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:  # noqa: C901
    print("EGS14 BATTERY -- ETFS_GUARDRAIL.TO-EG-s-14, month %s" % MONTH)
    print("run_at_utc %s" % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    rec = json.load(open(os.path.join(HERE, "invoke_record.json"), encoding="utf-8"))
    invoke_start = rec["invoke_start_utc"]
    invoke_end = rec["invoke_end_utc"]
    req_id = rec["x_amzn_request_id"]
    ff = rec["failed_first_fire"]
    print("invoke_record (THE RE-INVOKE): StatusCode=%s RequestId=%s start=%s end=%s ssm=%s/%s"
          % (rec["status_code"], req_id, invoke_start, invoke_end,
             rec["ssm_command_id"], rec["ssm_status"]))
    print("FAILED FIRST FIRE (kept for the record): %s -> %s RequestId=%s ssm=%s/%s -- %s"
          % (ff["invoke_start_utc"], ff["invoke_end_utc"], ff["x_amzn_request_id"],
             ff["ssm_command_id"], ff["ssm_status"], ff["ssm_error"][:90]))

    w_start = to_dt(invoke_start) - dt.timedelta(minutes=2)
    w_end = to_dt(invoke_end) + dt.timedelta(minutes=5)
    w_start_s = w_start.strftime("%Y-%m-%dT%H:%M:%SZ")
    w_end_s = w_end.strftime("%Y-%m-%dT%H:%M:%SZ")
    print("READ WINDOW (UTC): %s -> %s" % (w_start_s, w_end_s))

    # ---------------------------------------------------------------- arm (a)
    # The ENTRY FILE is the graded object. `deploy_ledger.py close` REMOVES the sentinel
    # (all legs proven), so the sentinel is read only when it still exists; otherwise the
    # entry is resolved by slug under change_management/ and its own "Date opened:" line
    # is the opened-at. Either way the .md is what carries the NEVER-2 detail (row W1-S16:
    # it must be appended AFTER the final ledger mutation, and this arm is read after that).
    if os.path.exists(LEDGER_SENTINEL):
        led = json.load(open(LEDGER_SENTINEL, encoding="utf-8"))
        entry_path, opened_at = led["entry_path"], led["opened_at"]
        sentinel_state = "PRESENT (entry still open/held)"
    else:
        cm = os.path.join(ROOT, "org", "critical_paths", "change_management")
        hits = sorted(f for f in os.listdir(cm)
                      if "etfs-guardrail-eg-s-14-august-rerender" in f and f.endswith(".md"))
        entry_path = os.path.join("org", "critical_paths", "change_management",
                                  hits[-1]).replace("\\", "/")
        opened_at = ""
        for ln in open(os.path.join(ROOT, entry_path), encoding="utf-8").read().splitlines():
            if ln.startswith("**Date opened:**"):
                opened_at = ln.split("**Date opened:**", 1)[1].strip()
                break
        sentinel_state = "REMOVED by `close` (all legs proven) -- entry read by slug, %d of " \
                         "%d matching .md" % (len(hits), len(hits))
    print("ledger sentinel: %s" % sentinel_state)
    md = open(os.path.join(ROOT, entry_path), encoding="utf-8").read()
    led = {"entry_path": entry_path, "opened_at": opened_at}
    opened_before = opened_at < invoke_start.replace("Z", "")
    keys_named = sum(1 for n in PUBLISH_NAMES if (SERVED_PREFIX + n) in md)
    tab = json.load(open(os.path.join(HERE, "archive_table.json"), encoding="utf-8"))
    sha_named = sum(1 for n in PUBLISH_NAMES if tab["prior"][n]["sha256"] in md)
    has_rollback = "copy-object" in md and "ROLLBACK" in md
    signoffs = [COO_SIGNOFF in md, COO_SIGNOFF_AMENDMENT in md, CTO_SIGNOFF in md]
    ok_a = (opened_before and keys_named == len(PUBLISH_NAMES)
            and sha_named == len(PUBLISH_NAMES) and has_rollback and all(signoffs))
    arm("a", ok_a,
        "ledger %s opened_at=%s < invoke %s -> %s; served keys named %d of %d; prior sha256 "
        "named %d of %d; rollback=%s; signoffs COO %s + %s and CTO %s -> %d of 3"
        % (led["entry_path"], opened_at, invoke_start, opened_before,
           keys_named, len(PUBLISH_NAMES), sha_named, len(PUBLISH_NAMES), has_rollback,
           COO_SIGNOFF, COO_SIGNOFF_AMENDMENT, CTO_SIGNOFF, sum(signoffs)))

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
    os.environ.setdefault("REPORTS_SNS_TOPIC",
                          "arn:aws:sns:us-east-1:313476888478:etfs-reports-alerts")
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
    print("COVERAGE-LINE TABLE (denominator: %d served CSVs; month trading days = %d)"
          % (len(CSV_NAMES), len(tdays)))
    for n in CSV_NAMES:
        dest = os.path.join(ROOT, ".scratch", "battery_" + n)
        rc2, out2 = aws(["s3api", "get-object", "--bucket", BUCKET,
                         "--key", SERVED_PREFIX + n, dest])
        if rc2 != 0:
            cov_ok.append(False)
            print("  %-46s GET rc=%d (absent?)" % (n, rc2))
            continue
        text = open(dest, "rb").read().decode("utf-8")
        lines = text.splitlines()
        last = lines[-1]
        has = last.startswith("# coverage:")
        denom_ok = ("/%d trading days" % len(tdays)) in last
        cov_ok.append(has and denom_ok)
        print("  %-46s rows=%d LAST_ROW=%r startswith '# coverage:' -> %s; carries the "
              "month denominator /%d -> %s" % (n, len(lines), last[:80], has,
                                               len(tdays), denom_ok))

    print("ARCHIVE TABLE (prior vs archive sha256; two archives, denominator %d of %d each)"
          % (len(tab["prior"]), len(PUBLISH_NAMES)))
    arch_ok = []
    for pref_key in ("archive_prefix", "archive2_prefix"):
        pref = tab[pref_key]
        for n, v in tab["prior"].items():
            dest = os.path.join(ROOT, ".scratch", "battery_arch_" + pref_key + "_" + n)
            rc3, _ = aws(["s3api", "get-object", "--bucket", BUCKET,
                          "--key", pref + n, dest])
            h = hashlib.sha256(open(dest, "rb").read()).hexdigest() if rc3 == 0 else "GET-FAILED"
            eq = (h == v["sha256"])
            arch_ok.append(eq)
            print("  %-46s prior=%s %s%s -> %s EQUAL=%s"
                  % (n, v["sha256"][:24], pref, n, h[:24], eq))

    ok_d = all(fresh) and all(cov_ok) and all(arch_ok)
    arm("d", ok_d,
        "published-after-invoke %d of %d; CSV last row '# coverage:' with the /%d "
        "denominator %d of %d; archive sha256 match %d of %d (two archives)"
        % (sum(fresh), len(fresh), len(tdays), sum(cov_ok), len(cov_ok),
           sum(arch_ok), len(arch_ok)))

    # ---------------------------------------------------------------- arm (e)
    start_ms = int(w_start.timestamp() * 1000)
    end_ms = int(w_end.timestamp() * 1000)
    rc, ev, raw = aws_json(["logs", "filter-log-events", "--log-group-name", LOG_GROUP,
                            "--start-time", str(start_ms), "--end-time", str(end_ms)],
                           timeout=180)
    events = (ev or {}).get("events", [])
    print("log group %s read BY TIME (%s -> %s): %d event(s)"
          % (LOG_GROUP, w_start_s, w_end_s, len(events)))
    streams = sorted({e.get("logStreamName", "") for e in events})
    for e in events:
        print("  LOG %s %s" % (iso(e["timestamp"] / 1000.0), e["message"].strip()[:200]))
    start_lines = [e for e in events if e["message"].startswith("START RequestId: " + req_id)]
    print("  START RequestId: %s -> %d of %d START line(s) in the window (streams: %d)"
          % (req_id, len(start_lines),
             len([e for e in events if e["message"].startswith("START RequestId")]),
             len(streams)))

    rc, ct, raw = aws_json(["cloudtrail", "lookup-events",
                            "--lookup-attributes",
                            "AttributeKey=EventName,AttributeValue=AssumeRole",
                            "--start-time", w_start_s, "--end-time", w_end_s], timeout=240)
    ar_events = (ct or {}).get("Events", [])
    sched_role_hits = []
    for e in ar_events:
        blob = e.get("CloudTrailEvent", "") or ""
        if SCHEDULER_ROLE in blob or any(SCHEDULER_ROLE in (r.get("ResourceName") or "")
                                         for r in e.get("Resources", [])):
            sched_role_hits.append(e)
    print("  CloudTrail AssumeRole in the window: %d event(s) scanned; naming %s: %d "
          "(the rule did not fire)" % (len(ar_events), SCHEDULER_ROLE, len(sched_role_hits)))

    rc, cti, raw = aws_json(["cloudtrail", "lookup-events",
                             "--lookup-attributes",
                             "AttributeKey=EventName,AttributeValue=Invoke",
                             "--start-time", w_start_s, "--end-time", w_end_s], timeout=180)
    inv_events = (cti or {}).get("Events", [])
    rc, trails, raw = aws_json(["cloudtrail", "describe-trails",
                                "--query", "trailList[].Name"])
    n_trails = len(trails or [])
    n_lambda_sel = 0
    for t in (trails or []):
        rc, sel, raw = aws_json(["cloudtrail", "get-event-selectors", "--trail-name", t])
        blob = json.dumps(sel or {})
        if "AWS::Lambda::Function" in blob:
            n_lambda_sel += 1
    print("  COVERAGE-ABSENT: %d of %d trails select AWS::Lambda::Function "
          "(CloudTrail Invoke events returned in the window: %d -- neither a pass nor a fail)"
          % (n_lambda_sel, n_trails, len(inv_events)))
    print("  POSITIVE CONTROL (management events are logged in this window):")
    ctrl_total = 0
    for name in ("StartInstances", "StopInstances"):
        rc, c2, raw = aws_json(["cloudtrail", "lookup-events", "--lookup-attributes",
                                "AttributeKey=EventName,AttributeValue=" + name,
                                "--start-time", w_start_s, "--end-time", w_end_s],
                               timeout=180)
        c2e = (c2 or {}).get("Events", [])
        ctrl_total += len(c2e)
        for e in c2e:
            print("    %s %s user=%s" % (e.get("EventTime"), name, e.get("Username")))

    trigger_field = False
    for n in CSV_NAMES:
        p = os.path.join(ROOT, ".scratch", "battery_" + n)
        if os.path.exists(p):
            body = open(p, "rb").read().decode("utf-8", "replace")
            if req_id in body or "run-id" in body or "trigger" in body.lower():
                trigger_field = True
    if not trigger_field:
        print("ARTIFACT-CARRIES-NO-TRIGGER-FIELD")
    ok_e = (len(start_lines) == 1 and len(sched_role_hits) == 0 and ctrl_total > 0)
    arm("e", ok_e,
        "manual fire pinned: START RequestId %s appears %d of 1 time(s) in the log group "
        "read BY TIME; %s AssumeRole in the window = %d (rule did not fire); CloudTrail "
        "Invoke COVERAGE-ABSENT (%d of %d trails select AWS::Lambda::Function); positive "
        "control management events in the window = %d"
        % (req_id, len(start_lines), SCHEDULER_ROLE, len(sched_role_hits),
           n_lambda_sel, n_trails, ctrl_total))

    # ---------------------------------------------------------------- arm (f)
    msg_ids = [e["message"].strip() for e in events if "MessageId" in e["message"]]
    rc, ses, raw = aws_json(["cloudtrail", "lookup-events", "--lookup-attributes",
                             "AttributeKey=EventName,AttributeValue=SendRawEmail",
                             "--start-time", w_start_s, "--end-time", w_end_s], timeout=180)
    ses_events = (ses or {}).get("Events", [])
    rc, cfg, raw = aws_json(["lambda", "get-function-configuration", "--function-name", FN])
    live_recips = (cfg or {}).get("Environment", {}).get("Variables", {}).get(
        "EMAIL_RECIPIENT", "")
    join_ok = all(r in live_recips for r in RECIPIENTS)
    # SUBSTITUTE MEASUREMENTS (printed, not scored -- the named limbs above are the arm):
    rc, st, raw = aws_json(["ses", "get-send-statistics"])
    pts = sorted((st or {}).get("SendDataPoints", []), key=lambda p: p["Timestamp"])
    in_window = [p for p in pts if w_start_s[:16] <= p["Timestamp"][:16] <= w_end_s[:16]]
    attempts = sum(p["DeliveryAttempts"] for p in in_window)
    rc, sns, raw = aws_json(["cloudwatch", "get-metric-statistics", "--namespace", "AWS/SNS",
                             "--metric-name", "NumberOfMessagesPublished",
                             "--dimensions", "Name=TopicName,Value=" + ALERT_TOPIC,
                             "--start-time", w_start_s, "--end-time", w_end_s,
                             "--period", "300", "--statistics", "Sum"])
    alerts = sum(d["Sum"] for d in (sns or {}).get("Datapoints", []))
    print("SES: MessageId lines in the run's log: %d; CloudTrail SendRawEmail in the "
          "window: %d; live EMAIL_RECIPIENT=%r (JOIN of both recipients -> %s)"
          % (len(msg_ids), len(ses_events), live_recips, join_ok))
    print("  SUBSTITUTE (printed, not scored): SES get-send-statistics DeliveryAttempts in "
          "the window = %d over %d data point(s); %s NumberOfMessagesPublished in the "
          "window = %g (every failure branch of _run publishes there, so 0 = the send did "
          "not fail)" % (attempts, len(in_window), ALERT_TOPIC, alerts))
    arm("f", bool(msg_ids) and bool(ses_events) and join_ok,
        "SES MessageId(s) in the orchestrator log for this run: %d; CloudTrail "
        "SendRawEmail in the run's minute: %d; Destinations must name %s"
        % (len(msg_ids), len(ses_events), " + ".join(RECIPIENTS)))

    # ---------------------------------------------------------------- arm (g)
    rc, inst, raw = aws_json(["ec2", "describe-instances", "--instance-ids", INSTANCE,
                              "--query",
                              "Reservations[].Instances[].[InstanceId,State.Name]"])
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
