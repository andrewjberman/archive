"""COMM_ASSIST round 14 CA-f-1 AC2: after the deploy, the live channel_poll step is no longer silent.

Reads /aws/lambda/teams-global-chat-assist-ingress-lambda (us-east-1) from the later of (the ingress function's LastModified)
and (now - 60 min) to now. PASS when EITHER
  (a) at least one `channel_poll` line carries a non-empty `error` field AND at least one `ingress_step_failed` line names
      step `channels` (the failure is readable and escalated), OR
  (b) at least one `channel_poll` line exists and every one reads failed=0 (the step is healthy).
Prints the counts with their denominator and RESULT: PASS|FAIL. Log lines only; never message content.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~ZZ/r14/checks/d1_errorfield.py
"""
import datetime
import json
import os
import subprocess
import sys

FN = "teams-global-chat-assist-ingress-lambda"
GROUP = "/aws/lambda/" + FN


def aws(*args):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return None, ((r.stderr or "").strip().splitlines() or ["rc=%d" % r.returncode])[-1]
    return json.loads(r.stdout), None


def payload(msg):
    i = msg.find("{")
    try:
        return json.loads(msg[i:]) if i >= 0 else {}
    except ValueError:
        return {}


def main():
    cfg, err = aws("lambda", "get-function-configuration", "--function-name", FN)
    lm = (cfg or {}).get("LastModified") or ""
    now = datetime.datetime.now(datetime.timezone.utc)
    start = now - datetime.timedelta(minutes=60)
    try:
        deployed = datetime.datetime.strptime(lm[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc)
        start = max(start, deployed)
    except ValueError:
        print("WARN: LastModified unreadable (%r) %s" % (lm, err or ""))
    polls = errs = fails = steps = 0
    for pattern, kind in (("channel_poll", "poll"), ("ingress_step_failed", "step")):
        doc, err = aws("logs", "filter-log-events", "--log-group-name", GROUP, "--start-time",
                       str(int(start.timestamp() * 1000)), "--filter-pattern", pattern, "--max-items", "500")
        if err:
            print("ERROR: %s read failed: %s" % (pattern, err))
        for ev in (doc or {}).get("events", []):
            p = payload(ev.get("message") or "")
            if kind == "poll" and p.get("event") == "channel_poll":
                polls += 1
                fails += 1 if p.get("failed") else 0
                errs += 1 if str(p.get("error") or "").strip() else 0
            elif kind == "step" and p.get("event") == "ingress_step_failed" and p.get("step") == "channels":
                steps += 1
    print("WINDOW start=%s now=%s (ingress LastModified %s)" % (start.isoformat(), now.isoformat(), lm))
    print("COUNTS channel_poll=%d failed>0=%d with_error=%d ingress_step_failed[channels]=%d" % (polls, fails, errs, steps))
    loud = errs >= 1 and steps >= 1
    healthy = polls >= 1 and fails == 0
    print("CHECK readable-and-escalated=%s healthy=%s" % (loud, healthy))
    print("RESULT: %s" % ("PASS" if (loud or healthy) else "FAIL"))
    return 0 if (loud or healthy) else 1


if __name__ == "__main__":
    sys.exit(main())
