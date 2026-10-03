"""HVST-ak-3 AC2 (issuer, read-only): the event-density census (FWD-6 density enrichment; HARVST brief O5) is complete
and internally consistent.

Reads `deliverables/0.9.0_WK_AMGT_HARVST~91/ak3_event_density.json`. PASS requires:
- integers: securities, events_served, events_dry_built and puts_sent, with puts_sent == 0;
- spike_days and spike_days_covered, each a dict with keys "2x" and "3x" of non-negative integers;
- covered <= spike_days at each threshold;
- mention_rows_read, an integer > 0, and served_event_part, a non-empty string naming the served snapshot read;
- events_served equals the row count of the served chatter_event snapshot that this check reads itself, so the census
  read the live store and not a stale copy.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
CENSUS = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~91/ak3_event_density.json")

from lib.research.harvest import publication_gold as pg  # noqa: E402


def main():
    failures = []
    if not os.path.exists(CENSUS):
        print("NO CENSUS at %s" % CENSUS)
        print("AC2 RESULT: FAIL (1 failure(s))")
        return 1
    d = json.load(open(CENSUS, encoding="utf-8"))
    for k in ("securities", "events_served", "events_dry_built", "puts_sent", "mention_rows_read"):
        if not isinstance(d.get(k), int):
            failures.append("%s is %r, not an integer" % (k, d.get(k)))
    if d.get("puts_sent") != 0:
        failures.append("puts_sent %r" % d.get("puts_sent"))
    if not (isinstance(d.get("mention_rows_read"), int) and d["mention_rows_read"] > 0):
        failures.append("mention_rows_read %r" % d.get("mention_rows_read"))
    if not (isinstance(d.get("served_event_part"), str) and d["served_event_part"]):
        failures.append("served_event_part %r" % d.get("served_event_part"))
    for k in ("spike_days", "spike_days_covered"):
        v = d.get(k)
        if not (isinstance(v, dict) and all(isinstance(v.get(t), int) and v[t] >= 0 for t in ("2x", "3x"))):
            failures.append("%s is %r" % (k, v))
    if not failures:
        for t in ("2x", "3x"):
            if d["spike_days_covered"][t] > d["spike_days"][t]:
                failures.append("covered %s %d > spike days %d" % (t, d["spike_days_covered"][t], d["spike_days"][t]))
    served = len(pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE))
    print("CENSUS events_served %r; served snapshot read by this check: %d rows" % (d.get("events_served"), served))
    if d.get("events_served") != served:
        failures.append("events_served %r != served snapshot %d" % (d.get("events_served"), served))
    print("CENSUS dry_built %r; spikes %r; covered %r" % (d.get("events_dry_built"), d.get("spike_days"),
                                                          d.get("spike_days_covered")))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
