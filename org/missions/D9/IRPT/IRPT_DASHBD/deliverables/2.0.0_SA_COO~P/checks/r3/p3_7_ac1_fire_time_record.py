"""DB-7-AC1 -- the reporting gold's fire time is READ from its inputs' landing times, never guessed.

Reads org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/REPORTING_GOLD_FIRE_TIME_R3.json:
  {"inputs": [{"name", "bucket", "prefix", "days_measured", "latest_landing_et": "HH:MM", "landings": [{"date", "landed_et"}]}],
   "timezone": "America/New_York", "chosen_et": "HH:MM", "chosen_cron": "cron(M H ? * MON-FRI *)",
   "margin_minutes": n, "publisher_et": "08:15"}
Grades: at least 4 inputs, including the three Schwab silver prefixes (fact_trn, dim_position, dim_balance) and the
holdings-performance gold; every input has days_measured >= 10 with that many landings listed; chosen_et is at or after
max(latest_landing_et) + margin_minutes, margin_minutes >= 10, and strictly before publisher_et 08:15; chosen_cron encodes
chosen_et Monday to Friday. Usage: python <this file> <repo_root>
"""
import json
import re
import sys
from pathlib import Path


def fail(msg):
    print("FAIL: " + msg)
    print("DB-7-AC1 FAIL")
    sys.exit(1)


def minutes(hhmm):
    m = re.fullmatch(r"(\d{2}):(\d{2})", str(hhmm or ""))
    if not m:
        fail("not an HH:MM time: %r" % hhmm)
    return int(m.group(1)) * 60 + int(m.group(2))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/REPORTING_GOLD_FIRE_TIME_R3.json"
    if not p.is_file():
        fail("no record at %s" % p)
    r = json.loads(p.read_text(encoding="utf-8"))
    inputs = r.get("inputs") or []
    if len(inputs) < 4:
        fail("%d inputs, need at least 4" % len(inputs))
    prefixes = " ".join(str(i.get("prefix", "")) for i in inputs)
    for need in ("silver/fact_trn", "silver/dim_position", "silver/dim_balance", "holdings_performance"):
        if need not in prefixes:
            fail("no input whose prefix carries %r" % need)
    latest = 0
    for i in inputs:
        days = int(i.get("days_measured") or 0)
        if days < 10 or len(i.get("landings") or []) < days:
            fail("input %r measured %d day(s) with %d landing(s) listed; need >= 10" % (i.get("name"), days, len(i.get("landings") or [])))
        latest = max(latest, minutes(i.get("latest_landing_et")))
    if r.get("timezone") != "America/New_York":
        fail("timezone %r" % r.get("timezone"))
    margin = int(r.get("margin_minutes") or 0)
    chosen = minutes(r.get("chosen_et"))
    pub = minutes(r.get("publisher_et") or "08:15")
    if margin < 10:
        fail("margin_minutes %d < 10" % margin)
    if chosen < latest + margin:
        fail("chosen %s is before the latest landing + margin" % r.get("chosen_et"))
    if not chosen < pub:
        fail("chosen %s is not before the publisher's %s" % (r.get("chosen_et"), r.get("publisher_et")))
    want = "cron(%d %d ? * MON-FRI *)" % (chosen % 60, chosen // 60)
    if r.get("chosen_cron") != want:
        fail("chosen_cron %r != %r" % (r.get("chosen_cron"), want))
    print("OK: %d inputs, latest landing %02d:%02d ET, chosen %s ET (%s), publisher %s" % (
        len(inputs), latest // 60, latest % 60, r["chosen_et"], r["chosen_cron"], r.get("publisher_et")))
    print("DB-7-AC1 PASS")


if __name__ == "__main__":
    main()
