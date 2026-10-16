"""TCKT_VNEXT rounds 18 and 19 -- the CTO's after-read (combined release pair, condition 1; msg 9624).

After the ticket-service release no client notice may go to a body-named address: from the release's apply-end timestamp the log group
/aws/lambda/opal-ticket-api must hold ZERO `WE_CLIENT_SENT` lines AND AT LEAST ONE `WE_CLIENT_NO_CONTACT` line (a zero SENT with no
NO_CONTACT is an UNEXERCISED path, not a pass). The instrument is proven able to see the token first: the same filter from an earlier
window (2026-10-09) must return at least one `WE_CLIENT_SENT` (the live pickup notices of 2026-10-09 to 2026-10-11).

Prints AFTERREAD-OK <counts> or AFTERREAD-BAD <reason>; exit 0/1. Read-only; one filter-log-events per window with the events scanned
printed beside every count. Usage: python r18_afterread.py [START_ISO_UTC]   (default: the release's apply end, 2026-10-16T17:57:19Z)
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

LOG_GROUP = "/aws/lambda/opal-ticket-api"
APPLY_END = "2026-10-16T17:57:19Z"
CONTROL_START = "2026-10-09T00:00:00Z"
AWS = os.path.abspath(".tools/aws.cmd")
MAX_ITEMS = 5000


def count(start_iso):
    ms = int(datetime.strptime(start_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp() * 1000)
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    scanned = sent = nocontact = 0
    token = None
    truncated = False
    while True:
        cmd = [AWS, "logs", "filter-log-events", "--log-group-name", LOG_GROUP, "--start-time", str(ms),
               "--region", "us-east-1", "--output", "json", "--max-items", str(MAX_ITEMS)]
        if token:
            cmd += ["--starting-token", token]
        out = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=170)
        if out.returncode != 0:
            raise RuntimeError("filter-log-events rc=%d" % out.returncode)
        doc = json.loads(out.stdout)
        for e in doc.get("events", []):
            scanned += 1
            msg = e.get("message", "")
            sent += "WE_CLIENT_SENT" in msg
            nocontact += "WE_CLIENT_NO_CONTACT" in msg
        token = doc.get("NextToken")
        if not token:
            break
        truncated = True  # more than one page was needed; the loop follows it, this only records it
    return scanned, sent, nocontact, truncated


def main(argv):
    start = argv[0] if argv else APPLY_END
    try:
        c_scanned, c_sent, _, _ = count(CONTROL_START)
        scanned, sent, nocontact, paged = count(start)
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as e:
        print("AFTERREAD-BAD live read failed: %s" % e)
        return 1
    detail = "from %s: events_scanned=%d WE_CLIENT_SENT=%d WE_CLIENT_NO_CONTACT=%d paged=%s | control from %s: events_scanned=%d WE_CLIENT_SENT=%d" % (
        start, scanned, sent, nocontact, paged, CONTROL_START, c_scanned, c_sent)
    if c_sent < 1:
        print("AFTERREAD-BAD the instrument cannot see the token (the control window holds no WE_CLIENT_SENT): " + detail)
        return 1
    if scanned < 1:
        print("AFTERREAD-BAD no events scanned in the window: " + detail)
        return 1
    if sent != 0:
        print("AFTERREAD-BAD a client notice was SENT after the release: " + detail)
        return 1
    if nocontact < 1:
        print("AFTERREAD-BAD zero SENT but no WE_CLIENT_NO_CONTACT: the notice path is UNEXERCISED, not a pass: " + detail)
        return 1
    print("AFTERREAD-OK " + detail)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
