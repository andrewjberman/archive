"""COMM_ASSIST round 12 close read (the issuer's real run for FWD-4): one UTC day's mail lines, counted, never read.

The FWD-3 count reader (inbound_count.py) does not see mail. This reads the two structured lines the round-9 code logs:
  mail_poll       (each ingress minute: domains, listed, fetched, sent, calls, refused, failed)
  mail_considered (each considered batch: ok, sender_domain, body_no_andrew, no_sender, no_body)
from both functions' log groups, sums them, and prints one MAIL line plus one MAIL-CLOSE line:
  exercised=True  needs considered ok >= 1 (a mail from the five naming Andrew was texted), body_no_andrew + sender_domain >= 1
                  (a mail was refused before any model), and failed == 0.
Whether each text carried the right client/internal flag is a judgment the CVO grades, not this script.
Usage: python d2_mail_day.py --day YYYY-MM-DD    (read-only: logs:FilterLogEvents only; counts only, never message text)
"""
import argparse
import datetime
import json
import sys

import boto3

GROUPS = ["/aws/lambda/teams-global-chat-assist-handler-lambda", "/aws/lambda/teams-global-chat-assist-ingress-lambda"]
POLL_KEYS = ("domains", "listed", "fetched", "sent", "calls", "refused", "failed")
CONS_KEYS = ("ok", "sender_domain", "body_no_andrew", "no_sender", "no_body")


def lines(client, group, event, start_ms, end_ms):
    kw = {"logGroupName": group, "startTime": start_ms, "endTime": end_ms,
          "filterPattern": '{ $.event = "%s" }' % event}
    while True:
        r = client.filter_log_events(**kw)
        for e in r.get("events", []):
            try:
                yield json.loads(e["message"])
            except (ValueError, KeyError):
                continue
        tok = r.get("nextToken")
        if not tok:
            return
        kw["nextToken"] = tok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", required=True)
    day = ap.parse_args().day
    d0 = datetime.datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    start_ms = int(d0.timestamp() * 1000)
    end_ms = int((d0 + datetime.timedelta(days=1)).timestamp() * 1000) - 1
    c = boto3.client("logs", region_name="us-east-1")
    poll = {k: 0 for k in POLL_KEYS}
    cons = {k: 0 for k in CONS_KEYS}
    n_poll = n_cons = 0
    for g in GROUPS:
        for rec in lines(c, g, "mail_poll", start_ms, end_ms):
            n_poll += 1
            for k in POLL_KEYS:
                v = rec.get(k, 0)
                poll[k] += len(v) if isinstance(v, list) else int(v or 0)
        for rec in lines(c, g, "mail_considered", start_ms, end_ms):
            n_cons += 1
            for k in CONS_KEYS:
                cons[k] += int(rec.get(k, 0) or 0)
    print("MAIL day=%s groups=%d poll_lines=%d %s considered_lines=%d %s" % (
        day, len(GROUPS), n_poll, " ".join("%s=%d" % (k, poll[k]) for k in POLL_KEYS), n_cons,
        " ".join("considered_%s=%d" % (k, cons[k]) for k in CONS_KEYS)))
    refused_before_model = cons["sender_domain"] + cons["body_no_andrew"]
    exercised = cons["ok"] >= 1 and refused_before_model >= 1 and poll["failed"] == 0
    print("MAIL-CLOSE day=%s texted_ok=%d refused_before_model=%d poll_failed=%d exercised=%s" % (
        day, cons["ok"], refused_before_model, poll["failed"], exercised))
    return 0


if __name__ == "__main__":
    sys.exit(main())
