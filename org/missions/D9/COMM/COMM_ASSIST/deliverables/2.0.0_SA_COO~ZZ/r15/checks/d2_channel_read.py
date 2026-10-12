"""COMM_ASSIST round 15 CA-g-1 (D2): channel @mentions reach Andrew's phone, read from the live logs, never from a report.

Two arms, both over the last --minutes (default 60) to now, us-east-1:
  HOUR      /aws/lambda/teams-global-chat-assist-ingress-lambda: at least 50 `channel_poll` lines (one a minute), and every
            one reads failed=0.
  TEXTED    /aws/lambda/teams-global-chat-assist-handler-lambda: at least one `ldo_event` with kind teams.channel_mention and
            result "texted" (one text sent to him for a channel @mention). --mention-minutes widens this arm's window.
Prints the counts with their denominators and RESULT: PASS only when both arms hold. Log lines only; never message content.

    python org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~ZZ/r15/checks/d2_channel_read.py [--minutes 60] [--mention-minutes 1440]
"""
import argparse
import json
import os
import subprocess
import sys
import time

INGRESS = "/aws/lambda/teams-global-chat-assist-ingress-lambda"
HANDLER = "/aws/lambda/teams-global-chat-assist-handler-lambda"


def events(group, pattern, minutes):
    exe = "aws.cmd" if os.name == "nt" else "aws"
    start = str(int((time.time() - minutes * 60) * 1000))
    r = subprocess.run([exe, "logs", "filter-log-events", "--log-group-name", group, "--start-time", start,
                        "--filter-pattern", pattern, "--max-items", "2000", "--output", "json"],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("ERROR: %s %s read failed: %s" % (group, pattern, ((r.stderr or "").strip().splitlines() or ["?"])[-1]))
        return None
    out = []
    for ev in json.loads(r.stdout).get("events", []):
        msg = ev.get("message") or ""
        i = msg.find("{")
        try:
            out.append(json.loads(msg[i:]) if i >= 0 else {})
        except ValueError:
            continue
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=int, default=60)
    ap.add_argument("--mention-minutes", type=int, default=None)
    a = ap.parse_args()
    polls = events(INGRESS, "channel_poll", a.minutes)
    polls = [p for p in (polls or []) if p.get("event") == "channel_poll"]
    bad = sum(1 for p in polls if p.get("failed"))
    hour_ok = len(polls) >= 50 and bad == 0
    print("HOUR window=%dm channel_poll=%d failed>0=%d channels_listed_last=%s ok=%s"
          % (a.minutes, len(polls), bad, polls[-1].get("channels") if polls else None, hour_ok))
    mm = a.mention_minutes or a.minutes
    evs = events(HANDLER, "teams.channel_mention", mm)
    evs = [e for e in (evs or []) if e.get("event") == "ldo_event" and e.get("kind") == "teams.channel_mention"]
    texted = sum(1 for e in evs if e.get("result") == "texted")
    print("TEXTED window=%dm channel_mention_events=%d texted=%d ok=%s" % (mm, len(evs), texted, texted >= 1))
    ok = hour_ok and texted >= 1
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
