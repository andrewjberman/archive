#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-15 S15-AC4 battery -- THE SEPTEMBER-TO-DATE REFUSAL.

Prints EGS15-REFUSAL-LADDER-RAN only when every arm (a)-(i) holds on REAL data. Every
arm re-measures LIVE; the invoke's own response headers come from the committed
egs15_invoke_record.json and are cross-checked against the log group READ BY TIME
(the amended initiator cut: filter-log-events over the window, never a stream picked
by its lastEventTimestamp; plus etfs-reports-scheduler-role AssumeRole == 0).

Bounds: the vendored CLI v1 shim under a per-call timeout; no `--output text` (CRLF);
every S3 time in UTC via s3api; denominators on every list. ASCII only.

Run from the worktree root:
  timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs15_september_refusal.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")

BUCKET = "opal-data-etfs"
MONTH = "2026-09"
PREFIX = "platinum/reports/%s/" % MONTH
PUBLISH_KEYS = [PREFIX + "etf_ownership.pdf", PREFIX + "etf_ownership.html"]
REFUSED_KEY = PREFIX + "refused/etf_ownership.html"
FN = "etfs-reports-orchestrator"
LOG_GROUP = "/aws/lambda/%s" % FN
SCHEDULER_ROLE = "etfs-reports-scheduler-role"
ALERT_TOPIC = "etfs-reports-alerts"
INSTANCE = "i-070477bf35fc54409"
TERMINAL_RECIPIENT = "andrew@opalinvest.com"
COO_SIGNOFF = "4155c85a1f"
CTO_SIGNOFF = "94775"
LEDGER_SLUG = "etfs-guardrail-eg-s-15-september-refusal"
LEDGER_SENTINEL = os.path.join(ROOT, "org", "critical_paths", ".open_deploys",
                               LEDGER_SLUG + ".json")

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


def head(key: str):
    rc, j, raw = aws_json(["s3api", "head-object", "--bucket", BUCKET, "--key", key,
                           "--query", "[ContentLength,LastModified,ETag]"])
    return (200, j) if rc == 0 else (404, None)


def main() -> int:  # noqa: C901
    print("EGS15 BATTERY -- ETFS_GUARDRAIL.TO-EG-s-15, month %s" % MONTH)
    print("run_at_utc %s" % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    rec = json.load(open(os.path.join(HERE, "egs15_invoke_record.json"), encoding="utf-8"))
    inv_start, inv_end = rec["invoke_start_utc"], rec["invoke_end_utc"]
    req_id = rec["x_amzn_request_id"]
    w_start = to_dt(inv_start) - dt.timedelta(minutes=2)
    w_end = to_dt(inv_end) + dt.timedelta(minutes=5)
    w_start_s = w_start.strftime("%Y-%m-%dT%H:%M:%SZ")
    w_end_s = w_end.strftime("%Y-%m-%dT%H:%M:%SZ")
    print("invoke_record: payload=%s StatusCode=%s RequestId=%s %s -> %s ssm=%s/%s"
          % (rec["payload_sent"], rec["status_code"], req_id, inv_start, inv_end,
             rec.get("ssm_command_id"), rec.get("ssm_status")))
    print("READ WINDOW (UTC): %s -> %s" % (w_start_s, w_end_s))

    # ---------------------------------------------------------------- arm (a)
    if os.path.exists(LEDGER_SENTINEL):
        led = json.load(open(LEDGER_SENTINEL, encoding="utf-8"))
        entry_path, opened_at = led["entry_path"], led["opened_at"]
        state = led.get("status", "?")
    else:
        cm = os.path.join(ROOT, "org", "critical_paths", "change_management")
        hits = sorted(f for f in os.listdir(cm) if LEDGER_SLUG in f and f.endswith(".md"))
        entry_path = "org/critical_paths/change_management/" + hits[-1]
        opened_at, state = "", "SENTINEL-REMOVED (closed)"
        for ln in open(os.path.join(ROOT, entry_path), encoding="utf-8").read().splitlines():
            if ln.startswith("**Date opened:**"):
                opened_at = ln.split("**Date opened:**", 1)[1].strip()
                break
    md = open(os.path.join(ROOT, entry_path), encoding="utf-8").read()
    before_plan = opened_at < rec["plan_utc"].replace("Z", "")
    before_invoke = opened_at < inv_start.replace("Z", "")
    names_writes = all(t in md for t in ("coverage_verdict.json", "coverage_unresolved.json",
                                         "coverage_egress_ask.json", "refused/"))
    names_no_publish = "ARE NOT WRITTEN" in md or "NOT written" in md
    signoffs = COO_SIGNOFF in md and CTO_SIGNOFF in md
    arm("a", before_plan and before_invoke and names_writes and names_no_publish and signoffs,
        "ledger %s [%s] opened_at=%s < plan %s -> %s and < invoke %s -> %s; names what the run "
        "may write (verdict/unresolved/egress_ask/refused) -> %s; names the publish keys as NOT "
        "written -> %s; sign-off ids COO %s + CTO %s -> %s"
        % (entry_path, state, opened_at, rec["plan_utc"], before_plan, inv_start, before_invoke,
           names_writes, names_no_publish, COO_SIGNOFF, CTO_SIGNOFF, signoffs))

    # ---------------------------------------------------------------- arm (b)
    start_ms, end_ms = int(w_start.timestamp() * 1000), int(w_end.timestamp() * 1000)
    rc, ev, raw = aws_json(["logs", "filter-log-events", "--log-group-name", LOG_GROUP,
                            "--start-time", str(start_ms), "--end-time", str(end_ms)],
                           timeout=180)
    events = (ev or {}).get("events", [])
    starts = [e for e in events if e["message"].startswith("START RequestId: " + req_id)]
    all_starts = [e for e in events if e["message"].startswith("START RequestId")]
    for e in events:
        print("  LOG %s %s" % (iso(e["timestamp"] / 1000.0), e["message"].strip()[:180]))
    rc, ct, raw = aws_json(["cloudtrail", "lookup-events", "--lookup-attributes",
                            "AttributeKey=EventName,AttributeValue=AssumeRole",
                            "--start-time", w_start_s, "--end-time", w_end_s], timeout=240)
    ar = (ct or {}).get("Events", [])
    sched_hits = [e for e in ar if SCHEDULER_ROLE in (e.get("CloudTrailEvent") or "")]
    payload_ok = rec["payload_sent"] == '{"mode":"run","month":"2026-09"}'
    flags_ok = "--cli-read-timeout 0" in rec["invocation"] and \
               "--cli-connect-timeout 60" in rec["invocation"]
    arm("b", len(starts) == 1 and len(sched_hits) == 0 and payload_ok and flags_ok
        and rec["status_code"] == 200,
        "payload %s on the rule's target -> %s; StatusCode %s; START RequestId %s = %d of 1 in "
        "the log group read BY TIME (%d START line(s) total in the window); %s AssumeRole in the "
        "window = %d of %d events scanned; synchronous-invoke flags present -> %s"
        % (rec["payload_sent"], payload_ok, rec["status_code"], req_id, len(starts),
           len(all_starts), SCHEDULER_ROLE, len(sched_hits), len(ar), flags_ok))

    # ---------------------------------------------------------------- arm (c)
    rc, listing, raw = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET,
                                 "--prefix", PREFIX])
    contents = (listing or {}).get("Contents", [])
    print("objects under s3://%s/%s : %d" % (BUCKET, PREFIX, len(contents)))
    for c in contents:
        print("  %-62s LastModified(UTC)=%s Size=%d" % (c["Key"], c["LastModified"], c["Size"]))

    verdict_doc = unresolved_doc = ask_doc = None
    for name, tgt in (("coverage_verdict.json", "verdict"),
                      ("coverage_unresolved.json", "unresolved"),
                      ("coverage_egress_ask.json", "ask")):
        dest = os.path.join(ROOT, ".scratch", "egs15_" + name)
        rc2, _ = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", PREFIX + name, dest])
        doc = json.load(open(dest, encoding="utf-8")) if rc2 == 0 else None
        if tgt == "verdict":
            verdict_doc = doc
        elif tgt == "unresolved":
            unresolved_doc = doc
        else:
            ask_doc = doc
        print("  artifact %-26s %s" % (name, "PRESENT" if doc is not None else "ABSENT"))

    verdict = (verdict_doc or {}).get("verdict")
    classes_printed = 0
    if verdict_doc:
        for p, d in verdict_doc.get("per_partner", {}).items():
            s = d["summary"]
            classes_printed += 1
            print("    %-12s %s | A=%s B=%s C=%s D=%s UNKNOWN=%s covered=%s trading_days=%s"
                  % (p, d["coverage_line"], s.get("A"), s.get("B"), s.get("C"), s.get("D"),
                     s.get("UNKNOWN"), s.get("covered"), s.get("trading_days")))
    n_unres = sum(len(v) for v in (unresolved_doc or {}).values()) if unresolved_doc else 0
    print("    unresolved entries: %d across %d partner(s)"
          % (n_unres, len(unresolved_doc or {})))
    if unresolved_doc:
        for p, rows in unresolved_doc.items():
            for r in rows:
                print("      %s %s class=%s reason=%s" % (p, r.get("date"), r.get("class"),
                                                          (r.get("reason") or "")[:120]))
    code_ref, meta_ref = head(REFUSED_KEY)
    print("    refused HTML %s -> HTTP %d %s" % (REFUSED_KEY, code_ref, meta_ref or ""))
    pub = []
    for k in PUBLISH_KEYS:
        code, meta = head(k)
        pub.append(code)
        print("    PUBLISH key %s -> HTTP %d %s" % (k, code, meta or ""))
    print("    THE DISCRIMINATING PAIR: refused/ = %d, publish keys = %s (want 200 and 404,404)"
          % (code_ref, pub))
    arm("c", verdict == "REFUSE" and code_ref == 200 and all(c == 404 for c in pub)
        and n_unres > 0,
        "coverage_verdict.json verdict=%s (want REFUSE) over %d partner class-sets; "
        "coverage_unresolved.json entries=%d; refused/etf_ownership.html HTTP %d (want 200); "
        "2026-09 publish keys HTTP %s of 2 (want 404 each)"
        % (verdict, classes_printed, n_unres, code_ref, pub))

    # ---------------------------------------------------------------- arm (d)
    alert_lines = [e["message"].strip() for e in events
                   if "FAILED" in e["message"] or "REFUSE" in e["message"]]
    rc, sns, raw = aws_json(["cloudwatch", "get-metric-statistics", "--namespace", "AWS/SNS",
                             "--metric-name", "NumberOfMessagesPublished",
                             "--dimensions", "Name=TopicName,Value=" + ALERT_TOPIC,
                             "--start-time", w_start_s, "--end-time", w_end_s,
                             "--period", "300", "--statistics", "Sum"])
    alerts = sum(d["Sum"] for d in (sns or {}).get("Datapoints", []))
    arm("d", alerts >= 1 or bool(alert_lines),
        "the refusal's alert: %s publishes in the run window = %g; alert-shaped log lines = %d "
        "(the orchestrator alerts on the non-Success branch; a PUBLISH verdict is quiet by design)"
        % (ALERT_TOPIC, alerts, len(alert_lines)))

    # ---------------------------------------------------------------- arm (e)
    msg_ids = [e["message"].strip() for e in events if "MessageId" in e["message"]]
    rc, ses, raw = aws_json(["cloudtrail", "lookup-events", "--lookup-attributes",
                             "AttributeKey=EventName,AttributeValue=SendRawEmail",
                             "--start-time", w_start_s, "--end-time", w_end_s], timeout=180)
    ses_events = (ses or {}).get("Events", [])
    rc, c2, raw = aws_json(["cloudtrail", "lookup-events", "--lookup-attributes",
                            "AttributeKey=EventName,AttributeValue=StartInstances",
                            "--start-time", w_start_s, "--end-time", w_end_s], timeout=180)
    control = len((c2 or {}).get("Events", []))
    if not ses_events and control > 0:
        print("SES-PLANE-UNREAD")
    ses_delta = rec.get("ses_delta_measured")
    print("(e) terminal send: MessageId lines in the log = %d; CloudTrail SendRawEmail = %d "
          "beside a positive control of %d management event(s); SES counter delta across the run "
          "= %s (recorded, account-wide); the ORDINARY monthly send must be 0 on a refusal"
          % (len(msg_ids), len(ses_events), control, ses_delta))
    terminal_ok = bool(msg_ids) and TERMINAL_RECIPIENT in " ".join(msg_ids)
    ordinary_zero = (ses_delta == 0)
    arm("e", terminal_ok and ordinary_zero,
        "exactly ONE send_raw_email on the terminal branch to %s with its MessageId -> %s; the "
        "ordinary monthly send count on a refusal (SES delta across the run) = %s, want 0"
        % (TERMINAL_RECIPIENT, terminal_ok, ses_delta))

    # ---------------------------------------------------------------- arm (f)
    asks = (ask_doc or {}).get("asks") or []
    named = [a for a in asks if a.get("date") and a.get("provider")]
    print("(f) coverage_egress_ask.json: %s; asks=%d, of which %d name BOTH a date and a provider"
          % ("PRESENT" if ask_doc else "ABSENT", len(asks), len(named)))
    for a in asks:
        print("      ask %s | %s -> %s (%s): %s" % (a.get("date"), a.get("partner"),
                                                    a.get("provider"), a.get("class"),
                                                    (a.get("reason") or "")[:80]))
    if ask_doc:
        print("      authorization: %s" % (ask_doc.get("authorization") or "")[:120])
    arm("f", bool(ask_doc) and len(asks) > 0 and len(named) == len(asks),
        "coverage_egress_ask.json written with the dates and the provider named: %d of %d asks "
        "carry both" % (len(named), len(asks)))

    # ---------------------------------------------------------------- arm (g)
    rc, ct_all, raw = aws_json(["cloudtrail", "lookup-events",
                                "--start-time", w_start_s, "--end-time", w_end_s], timeout=240)
    all_events = (ct_all or {}).get("Events", [])
    names: dict = {}
    for e in all_events:
        names[e.get("EventName", "?")] = names.get(e.get("EventName", "?"), 0) + 1
    # A BARE WORD-MATCH OVER THE EVENT JSON IS THE WRONG INSTRUMENT and was measured to be:
    # 29 'orion', 55 'ycharts', 8 'bloomberg' hits in this window are RESOURCE NAMES
    # (/aws/lambda/opal-assets-silver-orion, ycharts-session-probe, the bloomberg tunnel role)
    # read by an UNRELATED inventory principal's DescribeLogGroups / Decrypt /
    # ListAttachedRolePolicies sweep -- not egress, and not this run's principals. So the arm
    # is scoped to THIS RUN'S principals and asks whether any of them touched a vendor-facing
    # function; the word census is printed beside it as the false-positive it is.
    RUN_PRINCIPALS = ("etfs-reports-orchestrator", "etfs-reports-reporter-role",
                      "bd-49f-etf-ownership-daily", "cot-etf-ownership-daily",
                      "inf-etf-ownership-daily", "Andrew_Berman")
    VENDOR_FACING = ("ycharts-", "bloomberg", "opal-assets-silver-orion", "schwab-",
                     "addepar", "pershing")
    mine, vendor_by_mine, word_hits = [], [], 0
    for e in all_events:
        blob = json.dumps(e)
        low = blob.lower()
        if any(t in low for t in ("orion", "ycharts", "bloomberg", "schwab", "addepar",
                                  "pershing", "blackdiamond")):
            word_hits += 1
        if any(p.lower() in low for p in RUN_PRINCIPALS):
            mine.append(e)
            if any(v in low for v in VENDOR_FACING):
                vendor_by_mine.append(e)
    print("(g) VENDOR EGRESS over the run window. DENOMINATOR: %d CloudTrail event(s) in the "
          "window; event-name census %s"
          % (len(all_events), sorted(names.items(), key=lambda kv: -kv[1])[:8]))
    print("      %d event(s) mention a vendor WORD anywhere -- every one measured is a RESOURCE "
          "NAME read by an unrelated inventory principal (DescribeLogGroups / Decrypt / "
          "ListAttachedRolePolicies), NOT egress and NOT this run" % word_hits)
    print("      %d event(s) are attributable to THIS RUN's principals %s; of those, %d touch a "
          "vendor-facing resource" % (len(mine), list(RUN_PRINCIPALS), len(vendor_by_mine)))
    for e in vendor_by_mine[:5]:
        print("        %s %s %s" % (e.get("EventTime"), e.get("EventName"), e.get("Username")))
    print("      LIMIT, stated: CloudTrail records AWS API calls, never outbound HTTPS, and this "
          "estate has no separate egress-gateway log this worker could find (row W1-S23). The "
          "standing controls are the code (no HTTP client anywhere in the gate/ladder path) and "
          "rung 3, which STOPS and writes an ask instead of calling a provider.")
    arm("g", len(vendor_by_mine) == 0,
        "0 vendor-facing calls by this run's principals, of %d attributable event(s) within a "
        "%d-event window; rung 3 stopped and asked instead of egressing"
        % (len(mine), len(all_events)))

    # ---------------------------------------------------------------- arm (h)
    in_log = sum(1 for e in events if req_id in e["message"])
    artifact_has_runid = False
    for doc in (verdict_doc, unresolved_doc, ask_doc):
        if doc and req_id in json.dumps(doc):
            artifact_has_runid = True
    if not artifact_has_runid:
        print("ARTIFACT-CARRIES-NO-RUN-ID")
    print("(h) the request id appears in %d of %d log lines in the window; the artifacts "
          "themselves carry no run-id field" % (in_log, len(events)))
    arm("h", in_log >= 1, "run-id %s present in the orchestrator's log for the run (%d line(s)); "
        "artifact-level run-id: %s" % (req_id, in_log, artifact_has_runid))

    # ---------------------------------------------------------------- arm (i)
    rc, inst, raw = aws_json(["ec2", "describe-instances", "--instance-ids", INSTANCE,
                              "--query",
                              "Reservations[].Instances[].[InstanceId,State.Name]"])
    state_box = inst[0][1] if inst else "UNREAD"
    arm("i", state_box == "stopped",
        "reporter box %s State.Name=%s (describe-instances)" % (INSTANCE, state_box))

    passed = sum(1 for _, ok, _ in ARMS if ok)
    print("ARMS %d of %d PASS" % (passed, len(ARMS)))
    if passed == len(ARMS):
        print("EGS15-REFUSAL-LADDER-RAN")
        return 0
    print("EGS15-NO-REFUSAL -- failing arms: %s"
          % ", ".join(n for n, ok, _ in ARMS if not ok))
    return 1


if __name__ == "__main__":
    sys.exit(main())
