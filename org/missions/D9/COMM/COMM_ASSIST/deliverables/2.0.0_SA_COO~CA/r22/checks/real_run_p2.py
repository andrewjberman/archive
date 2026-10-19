"""COMM_ASSIST round 22 close read (the issuer's real run for FWD-2 after CA-p-2): the mail lines since the apply, counted, never read.

Reads the structured line the mail handler logs, `mail_considered` (each considered batch: ok, sender_domain, body_no_andrew,
no_sender, no_body and, since CA-p-2, from_andrew), from both functions' log groups, from --since (an ISO UTC time, the apply's
LastModified) to now, and the handler's error lines (a raised `me-without-mail`). Counts only; never message text.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r22/checks/real_run_p2.py --since 2026-10-19T21:50:00Z

Prints one REALRUN line:  REALRUN-P2 since=<t> batches=<n> ok=<n> from_andrew=<n> body_no_andrew=<n> sender_domain=<n> me_raises=<n>
verdict=<NO-MAIL-YET|REFUSES-HIS-OWN|ME-RAISE|NO-HIS-OWN-YET>.
  ME-RAISE              me_raises >= 1 (the CTO half: roll back in the same window);
  REFUSES-HIS-OWN       from_andrew >= 1 and ok >= 1 (his own mail refused and a colleague's still texted);
  NO-HIS-OWN-YET        ok >= 1 and from_andrew == 0 (colleague mail texted; his own mail has not arrived in the window);
  NO-MAIL-YET           no considered batch since --since.
Read-only: logs:FilterLogEvents only.
"""
import argparse
import datetime
import json
import sys

import boto3

GROUPS = ["/aws/lambda/teams-global-chat-assist-handler-lambda", "/aws/lambda/teams-global-chat-assist-ingress-lambda"]
KEYS = ("ok", "sender_domain", "body_no_andrew", "no_sender", "no_body", "from_andrew")


def events(client, group, pattern, start_ms, end_ms):
    kw = {"logGroupName": group, "startTime": start_ms, "endTime": end_ms, "filterPattern": pattern}
    while True:
        r = client.filter_log_events(**kw)
        for e in r.get("events", []):
            yield e["message"]
        tok = r.get("nextToken")
        if not tok:
            return
        kw["nextToken"] = tok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", required=True, help="ISO UTC, e.g. 2026-10-19T21:50:00Z")
    since = ap.parse_args().since
    t0 = datetime.datetime.strptime(since, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    start_ms = int(t0.timestamp() * 1000)
    end_ms = int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    c = boto3.client("logs", region_name="us-east-1")
    tot = {k: 0 for k in KEYS}
    batches = raises = 0
    for g in GROUPS:
        for msg in events(c, g, '{ $.event = "mail_considered" }', start_ms, end_ms):
            try:
                rec = json.loads(msg)
            except ValueError:
                continue
            batches += 1
            for k in KEYS:
                tot[k] += int(rec.get(k, 0) or 0)
        for _ in events(c, g, '"me-without-mail"', start_ms, end_ms):
            raises += 1
    # Each mail is its own object (mail:<message id>) and the line carries that object's counts, so the sums across lines are
    # near one count per mail; presence is what decides: from_andrew >= 1 appears only after the new code, me_raises only on its fault.
    if raises:
        verdict = "ME-RAISE"
    elif not batches:
        verdict = "NO-MAIL-YET"
    elif tot["from_andrew"] >= 1 and tot["ok"] >= 1:
        verdict = "REFUSES-HIS-OWN"
    else:
        verdict = "NO-HIS-OWN-YET"
    print("REALRUN-P2 since=%s batches=%d %s me_raises=%d verdict=%s" % (
        since, batches, " ".join("%s=%d" % (k, tot[k]) for k in KEYS), raises, verdict))
    return 0


if __name__ == "__main__":
    sys.exit(main())
