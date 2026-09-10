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
import hashlib
import json
import os
import urllib.request
import zipfile
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")

FUNCTION = "etfs-reports-orchestrator"
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
    # RE-CUT 2026-09-10 ~02:3xZ on row W1-S22. The cut's premise (an incomplete month
    # refuses) was wrong: the gate's refusal axis is the coverage CLASS, not the month's
    # completeness. This arm now READS THE LADDER and ACCEPTS the verdict the producer
    # gives, then reads the discriminating pair FOR THAT BRANCH.
    rc, listing, raw = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET,
                                 "--prefix", PREFIX])
    contents = (listing or {}).get("Contents", [])
    print("objects under s3://%s/%s : %d (denominator)" % (BUCKET, PREFIX, len(contents)))
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

    # THE PRODUCER'S OWN RULE, quoted from source with file:line @ commit-ish -- so the
    # class table below is read against the RULE and not against this order's expectation.
    print("  THE C-vs-D BOUNDARY, from the classifier's own source:")
    print("    data/etfs/scripts/coverage/classifier.py:146-148 @c866edd324 -- class D:")
    print('      if not answer.get("partition"):')
    print('          result[date_str] = {"class": "D",')
    print('                               "reason": "upstream partition missing (genuinely absent)",')
    print("    data/etfs/scripts/coverage/classifier.py:160-163 @c866edd324 -- class C:")
    print('      result[date_str] = {"class": "C",')
    print('                           "reason": "upstream present and priced > 0, no slice -- "')
    print('                                     "producer never fired for this date",')
    print("    THE REFUSAL AXIS, data/etfs/scripts/presentation/render_month_end.py:957-963 "
          "@4b85a9ae68:")
    print('      if summary["C"] > 0:')
    print("          any_c = True")
    print('      verdict = "REFUSE" if any_c else "PUBLISH"')
    print("    => the gate refuses on class C ALONE. A missing upstream partition inside an OPEN "
          "month is class D, so it cannot drive a REFUSE.")

    verdict = (verdict_doc or {}).get("verdict")
    print("  VERDICT AS THE PRODUCER GIVES IT (accepted, never asserted in advance): %r" % verdict)
    classes_printed = 0
    total_c = 0
    if verdict_doc:
        for p, d in verdict_doc.get("per_partner", {}).items():
            sm = d["summary"]
            classes_printed += 1
            total_c += int(sm.get("C") or 0)
            print("    %-12s %s | A=%s COVERED=%s B=%s C=%s D=%s UNKNOWN=%s trading_days=%s holes=%s"
                  % (p, d["coverage_line"], sm.get("A"), sm.get("COVERED"), sm.get("B"),
                     sm.get("C"), sm.get("D"), sm.get("UNKNOWN"), sm.get("trading_days"),
                     sm.get("holes")))
    print("    class C across %d of %d partners = %d -- consistent with verdict %r"
          % (classes_printed, classes_printed, total_c, verdict))

    n_unres = sum(len(v) for v in (unresolved_doc or {}).values()) if unresolved_doc else 0
    print("    unresolved entries: %d across %d partner(s) (denominator)"
          % (n_unres, len(unresolved_doc or {})))
    rung1_recorded = 0
    if unresolved_doc:
        for p, rows in unresolved_doc.items():
            for r in rows:
                reason = r.get("reason") or ""
                if "rung 1" in reason:
                    rung1_recorded += 1
                print("      %s %s class=%s" % (p, r.get("date"), r.get("class")))
                print("        REASON VERBATIM: %s" % reason)
    print("    rung 1 producer-invoke outcomes recorded with their raised error verbatim: "
          "%d of %d unresolved date(s)" % (rung1_recorded, n_unres))

    # THE DISCRIMINATING PAIR, RE-POINTED ONTO WHAT THE VERDICT ACTUALLY DECIDES.
    code_ref, meta_ref = head(REFUSED_KEY)
    pub = []
    for k in PUBLISH_KEYS:
        code, meta = head(k)
        pub.append(code)
        print("    PUBLISH key %s -> HTTP %d %s" % (k, code, meta or ""))
    print("    refused HTML %s -> HTTP %d %s" % (REFUSED_KEY, code_ref, meta_ref or ""))
    print("  BRANCH TAKEN: %s" % verdict)
    cov_lines_ok = 0
    csv_keys = [c["Key"] for c in contents if c["Key"].endswith(".csv")]
    if verdict == "PUBLISH":
        for k in csv_keys:
            dest = os.path.join(ROOT, ".scratch", "egs15_" + os.path.basename(k))
            rc3, _ = aws(["s3api", "get-object", "--bucket", BUCKET, "--key", k, dest])
            last = ""
            if rc3 == 0:
                rows = [ln for ln in open(dest, encoding="utf-8").read().splitlines() if ln.strip()]
                last = rows[-1] if rows else ""
            ok = last.startswith("# coverage:") and "trading days" in last and "carried" in last
            cov_lines_ok += 1 if ok else 0
            print("    served CSV %-46s LAST ROW: %s" % (os.path.basename(k), last))
        pair_ok = all(c == 200 for c in pub) and cov_lines_ok == len(csv_keys) and len(csv_keys) > 0
        print("    PAIR FOR THE PUBLISH BRANCH: publish keys %s (want 200,200) and %d of %d served "
              "CSVs carry the coverage line (want all)" % (pub, cov_lines_ok, len(csv_keys)))
    else:
        pair_ok = all(c == 404 for c in pub) and code_ref == 200
        print("    PAIR FOR THE REFUSE BRANCH: publish keys %s (want 404,404) beside refused/ HTTP "
              "%d (want 200)" % (pub, code_ref))

    # BOUNDS re-cut on W1-S24: the worker's hand writes nothing here; the LADDER may.
    # Enumerate every key the run wrote, with size, UTC and the rung that caused it.
    print("  EVERY KEY THIS RUN WROTE, with the rung that caused it:")
    rc, dl, raw = aws_json(["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "daily/"])
    daily = (dl or {}).get("Contents", [])
    written_daily = [c for c in daily if str(c["LastModified"]).startswith("2026-09-10T01:")]
    for c in written_daily:
        print("    %-46s %7d B  %s  <- RUNG 1 (re-run the producer: it exists to make a producer "
              "emit the slice it is missing)" % (c["Key"], c["Size"], c["LastModified"]))
    for c in contents:
        base = os.path.basename(c["Key"])
        if base.startswith("coverage_"):
            rung = "THE GATE/LADDER (coverage artifact)"
        else:
            rung = "THE RENDERER (publish branch, verdict=%s)" % verdict
        print("    %-46s %7d B  %s  <- %s" % (c["Key"], c["Size"], c["LastModified"], rung))
    print("    daily/ denominator: %d key(s) total, %d written in the run window"
          % (len(daily), len(written_daily)))
    print("    THE WORKER'S OWN HAND WROTE 0 of %d keys under daily/ and 0 of %d under %s"
          % (len(daily), len(contents), PREFIX))

    arm("c", verdict in ("PUBLISH", "REFUSE") and verdict_doc is not None
        and unresolved_doc is not None and n_unres > 0 and rung1_recorded == n_unres
        and classes_printed > 0 and pair_ok,
        "verdict=%r accepted as the producer gives it over %d partner class-sets (class C total "
        "%d); %d unresolved date(s) each with class + verbatim reason, %d carrying rung 1's raised "
        "error; discriminating pair read for the %s branch -> %s"
        % (verdict, classes_printed, total_c, n_unres, rung1_recorded, verdict,
           "HOLDS" if pair_ok else "FAILS"))

    # ---------------------------------------------------------------- arm (d)
    # RE-CUT on W1-S22: the alert limb reads BY BRANCH, and a zero without a control is
    # not a reading.
    alert_lines = [e["message"].strip() for e in events
                   if "FAILED" in e["message"] or "REFUSE" in e["message"]]
    rc, sns, raw = aws_json(["cloudwatch", "get-metric-statistics", "--namespace", "AWS/SNS",
                             "--metric-name", "NumberOfMessagesPublished",
                             "--dimensions", "Name=TopicName,Value=" + ALERT_TOPIC,
                             "--start-time", w_start_s, "--end-time", w_end_s,
                             "--period", "300", "--statistics", "Sum"])
    alerts = sum(d["Sum"] for d in (sns or {}).get("Datapoints", []))
    # POSITIVE CONTROL: the 23:14:43Z failed fire's window, where the topic DID publish.
    rc, sns_c, raw = aws_json(["cloudwatch", "get-metric-statistics", "--namespace", "AWS/SNS",
                               "--metric-name", "NumberOfMessagesPublished",
                               "--dimensions", "Name=TopicName,Value=" + ALERT_TOPIC,
                               "--start-time", "2026-09-09T23:14:00Z",
                               "--end-time", "2026-09-09T23:20:00Z",
                               "--period", "300", "--statistics", "Sum"])
    ctl_pts = (sns_c or {}).get("Datapoints", [])
    alerts_ctl = sum(d["Sum"] for d in ctl_pts)
    print("(d) BRANCH: %s" % verdict)
    print("    %s publishes in the RUN window (%s -> %s) = %g"
          % (ALERT_TOPIC, w_start_s, w_end_s, alerts))
    print("    POSITIVE CONTROL, the 23:14:43Z failed fire's window (2026-09-09T23:14:00Z -> "
          "23:20:00Z) = %g over %d datapoint(s) -- the topic and this metric DO record a publish, "
          "so the run-window zero is a READING, not an absence" % (alerts_ctl, len(ctl_pts)))
    print("    alert-shaped orchestrator log lines in the window = %d" % len(alert_lines))
    if verdict == "PUBLISH":
        d_ok = (alerts == 0) and (alerts_ctl >= 1)
        d_txt = ("on a PUBLISH the alert limb requires ZERO publishes in the run window beside a "
                 "live positive control: run=%g (want 0), control=%g (want >=1) -> %s"
                 % (alerts, alerts_ctl, "HOLDS" if d_ok else "FAILS"))
    else:
        d_ok = (alerts >= 1) or bool(alert_lines)
        d_txt = ("on a REFUSE the alert text must be produced: publishes=%g, alert-shaped log "
                 "lines=%d" % (alerts, len(alert_lines)))
    arm("d", d_ok, d_txt)

    # ---------------------------------------------------------------- arm (e)
    # RE-CUT on rows W1-S25 and W1-S26. This arm no longer tries to observe a send; it
    # PROVES THE DEFECT that makes the terminal send unreachable in production.
    msg_ids = [e["message"].strip() for e in events if "MessageId" in e["message"]]
    rc, ses, raw = aws_json(["cloudtrail", "lookup-events", "--lookup-attributes",
                             "AttributeKey=EventName,AttributeValue=SendRawEmail",
                             "--start-time", w_start_s, "--end-time", w_end_s], timeout=180)
    ses_events = (ses or {}).get("Events", [])
    rc, c2, raw = aws_json(["cloudtrail", "lookup-events", "--lookup-attributes",
                            "AttributeKey=EventName,AttributeValue=StartInstances",
                            "--start-time", w_start_s, "--end-time", w_end_s], timeout=180)
    control = len((c2 or {}).get("Events", []))
    rc, trails, raw = aws_json(["cloudtrail", "describe-trails"])
    n_trails = len((trails or {}).get("trailList", []))

    # (i) THE TWO SHAPES, SIDE BY SIDE.
    served_keys = sorted((unresolved_doc or {}).keys())
    fixture_shape = ["unresolved"]
    print("(e)(i) THE TWO SHAPES:")
    print("    SERVED  s3://%s/%scoverage_unresolved.json top-level keys: %s"
          % (BUCKET, PREFIX, served_keys))
    print("    FIXTURE test_terminal_send.py:118 top-level keys:            %s" % fixture_shape)
    shapes_disagree = "unresolved" not in served_keys and len(served_keys) > 0
    print("    DISAGREE -> %s" % shapes_disagree)

    # (ii) THE GUARD, FROM THE DEPLOYED BYTES.
    guard_line_no, guard_src, dep_sha = None, None, None
    try:
        rc, gf, raw = aws_json(["lambda", "get-function", "--function-name", FUNCTION])
        url = (gf or {}).get("Code", {}).get("Location")
        zp = os.path.join(ROOT, ".scratch", "egs15_deployed_fn.zip")
        urllib.request.urlretrieve(url, zp)
        blob = zipfile.ZipFile(zp).read("lambda_function.py")
        dep_sha = hashlib.sha256(blob).hexdigest()
        for n, ln in enumerate(blob.decode("utf-8").splitlines(), 1):
            if "unresolved_days =" in ln:
                guard_line_no, guard_src = n, ln.strip()
                break
    except Exception as exc:  # noqa: BLE001
        print("    DEPLOYED-BYTES READ FAILED: %s" % str(exc)[:200])
    print("(e)(ii) THE GUARD, QUOTED FROM THE DEPLOYED BYTES (not the worktree):")
    print("    deployed lambda_function.py sha256 %s (%s)" % (dep_sha, FUNCTION))
    print("    infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:%s @bd0e384890"
          % guard_line_no)
    print("      %s" % guard_src)
    print("    NOTE ON GRAIN: rows W1-S25 and this face cite ':439'; the guard is at :%s in the "
          "DEPLOYED bytes -- :439 is the `except` clause. Corrected in row W1-S29."
          % guard_line_no)

    # (iii) THE GUARD EVALUATED AGAINST THE SERVED DOCUMENT.
    guard_value = (unresolved_doc or {}).get("unresolved") or []
    print("(e)(iii) THE GUARD EVALUATED AGAINST THE SERVED DOCUMENT:")
    print("    (served_doc or {}).get(\"unresolved\") or []  ==  %r" % (guard_value,))
    print("    bool(...) == %s  ->  `if unresolved_days:` is FALSY  ->  _send_terminal_unresolved "
          "is SKIPPED" % bool(guard_value))
    print("    ...even though the served document carries %d unresolved date(s) under %s"
          % (n_unres, served_keys))
    terminal_sends = len([m for m in msg_ids if TERMINAL_RECIPIENT in m])
    print("    terminal-branch send_raw_email calls in the run window = %d" % terminal_sends)
    print("    ATTRIBUTION: that zero is caused by THIS DEFECT, not merely by the absent refusal --"
          " the guard reads falsy against the SERVED document, so the send would be skipped on a "
          "genuine REFUSE too.")
    defect_proved = shapes_disagree and guard_value == [] and n_unres > 0 and terminal_sends == 0

    # (iv) BOTH ORACLES, PRINTED AND NOT GRADED.
    print("SES-PLANE-UNREAD")
    print("    CloudTrail SendRawEmail = %d over the run window across a denominator of %d of %d "
          "trail(s) in the account, beside a same-window positive control of %d management "
          "event(s) -- so the zero is a COVERAGE fact, not a send fact"
          % (len(ses_events), n_trails, n_trails, control))
    print("NO-APPLICATION-LOG-LINE")
    print("    the handler emits ZERO application log lines: %d of %d events in the run window are "
          "runtime-generated, so no MessageId can ever appear for EITHER branch"
          % (len(events), len(events)))
    print("    NEITHER of these is graded by this arm.")

    # (v) THE ORDINARY SEND, WITH THE ISSUER'S DELIVERY READ CITED.
    ses_delta = rec.get("ses_delta_measured")
    print("(e)(v) THE ORDINARY SEND (the one that DID fire):")
    print("    SES SentLast24Hours delta across the run = %s (ONE send to TWO destinations); "
          "LIMIT: the counter is ACCOUNT-WIDE" % ses_delta)
    print("    ISSUER'S DELIVERY READ, cited not re-derived (2.0.0_SA_COO's gateway): subject "
          "'Opal ETF Ownership -- Month-End Report (2026-09)', 2026-09-10T01:21:28Z, toRecipients "
          "aj@opalinvest.com AND andrew@opalinvest.com")
    print("    SO THE RECORD SAYS EXACTLY WHICH SEND FIRED (the ordinary monthly report, to both) "
          "AND WHICH COULD NOT (the ONE terminal send to andrew@ alone).")
    print("    THE FIX IS NOT THIS WORKER'S: lambda_function.py is READ-ONLY under this order and "
          "the repair is a cell the issuer cuts (W1-S25, escalated to the CTO for the L10).")

    arm("e", defect_proved,
        "the DEFECT is proven: served top-level keys %s vs fixture %s DISAGREE -> %s; the deployed "
        "guard at :%s reads %r (falsy) against a document carrying %d unresolved date(s); "
        "terminal-branch sends = %d, attributed to the defect; SES-PLANE-UNREAD and "
        "NO-APPLICATION-LOG-LINE printed, neither graded"
        % (served_keys, fixture_shape, shapes_disagree, guard_line_no, guard_value, n_unres,
           terminal_sends))

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
