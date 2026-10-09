"""OPLGTW OG-bh-1 AC1 (Andrew-direct 2026-10-09 ~06:3xZ, FWD-13): the source-start census for master 08403355.

Reads the worker's census record and RE-READS the SSM invocation it names from AWS (the real neighbour, not the record):
  - the invocation is on the SI2 box, terminal Success, started OUTSIDE the daily-pull windows [09:15, 11:35) and
    [21:15, 23:35) UTC (08335338 09:45/21:45, 08242234 10:15/22:15, 08403355 10:45/22:45, each with its deadline);
  - its own output carries `mode=enumerate` and `master=08403355` and one `DATE <YYYY-MM-DD> <n>` line per served date;
  - the set of DATE lines equals the record's `served_dates`, their minimum equals `earliest_served`, and their sum
    equals the record's `enumerated` (> 0).

  python bh1.AC1.py <census_record.json>
"""
import datetime as dt
import json
import re
import sys

import boto3

BOX = "i-0f3d57a97f14727af"
MASTER = "08403355"
FORBIDDEN = ((dt.time(9, 15), dt.time(11, 35)), (dt.time(21, 15), dt.time(23, 35)))


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        rec = json.load(open(argv[1], encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("census record unreadable: %s (%s)" % (argv[1], type(exc).__name__))
        print("RESULT: FAIL")
        return 1
    ok = True
    cid = rec.get("command_id") or ""
    ssm = boto3.client("ssm", region_name="us-east-1")
    try:
        inv = ssm.get_command_invocation(CommandId=cid, InstanceId=BOX)
    except Exception as exc:  # a failed retrieval is a FAIL, never an empty pass
        print("FAIL: invocation %r on %s unreadable (%s)" % (cid, BOX, type(exc).__name__))
        print("RESULT: FAIL")
        return 1
    started = inv.get("ExecutionStartDateTime") or ""
    print("%s: invocation %s status %s started %s" % (MASTER, cid, inv.get("Status"), started))
    if inv.get("Status") != "Success":
        print("FAIL: invocation not Success")
        ok = False
    try:
        t = dt.datetime.fromisoformat(started.replace("Z", "+00:00")).astimezone(dt.timezone.utc).time()
        if any(a <= t < b for a, b in FORBIDDEN):
            print("FAIL: started inside a daily-pull window (%s UTC)" % t)
            ok = False
    except ValueError:
        print("FAIL: start time unparseable: %r" % started)
        ok = False
    out = (inv.get("StandardOutputContent") or "").replace("\r", "")
    if "mode=enumerate" not in out or ("master=" + MASTER) not in out:
        print("FAIL: output lacks mode=enumerate / master=%s" % MASTER)
        ok = False
    dates = {}
    for d, n in re.findall(r"^.*\bDATE (\d{4}-\d{2}-\d{2}) (\d+)\s*$", out, re.M):
        dates[d] = int(n)
    served = sorted(rec.get("served_dates") or [])
    total = sum(dates.values())
    print("DATE lines %d; record served_dates %d; enumerated (sum) %d; record enumerated %s; earliest %s; record "
          "earliest_served %s" % (len(dates), len(served), total, rec.get("enumerated"),
                                   min(dates) if dates else None, rec.get("earliest_served")))
    if not dates:
        print("FAIL: no DATE lines in the invocation output")
        ok = False
    elif sorted(dates) != served:
        print("FAIL: served_dates differ from the invocation: only-output %s; only-record %s" % (
            sorted(set(dates) - set(served))[:10], sorted(set(served) - set(dates))[:10]))
        ok = False
    elif min(dates) != rec.get("earliest_served"):
        print("FAIL: earliest_served is not the earliest DATE line")
        ok = False
    if total <= 0 or total != rec.get("enumerated"):
        print("FAIL: enumerated sum %d != record %s (or zero)" % (total, rec.get("enumerated")))
        ok = False
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
