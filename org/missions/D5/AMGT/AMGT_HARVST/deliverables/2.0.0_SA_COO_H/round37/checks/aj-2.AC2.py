"""HVST-aj-2 AC2 (issuer, read-only): the load monitor is back up and stays up (round-36 analysis ruling 2).

Reads `.runtime/harvest-backfill/load_monitor.json` twice, 600 s apart. PASS requires:
- the window opened at or after the restart (window_start >= 2026-10-02T06:50Z) and has no window_end (still open);
- the second read's snapshot_at is at least 540 s later than the first, with the same window_start (the log grows);
- `.runtime/harvest-backfill/runtimes.json` lists window1, window2 (preserved) and load_monitor.json.
"""
import datetime as dt
import json
import os
import subprocess
import sys
import time

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
H = os.path.join(ROOT, ".runtime/harvest-backfill")
RESTART = dt.datetime(2026, 10, 2, 6, 50, tzinfo=dt.timezone.utc)


def ts(s):
    t = dt.datetime.fromisoformat(str(s))
    return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)


def read():
    with open(os.path.join(H, "load_monitor.json"), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    failures = []
    a = read()
    print("READ 1 at %s: window_start %s snapshot_at %s window_end %s" % (
        dt.datetime.now(dt.timezone.utc).isoformat(), a.get("window_start"), a.get("snapshot_at"), a.get("window_end")))
    time.sleep(600)
    b = read()
    print("READ 2 at %s: window_start %s snapshot_at %s window_end %s" % (
        dt.datetime.now(dt.timezone.utc).isoformat(), b.get("window_start"), b.get("snapshot_at"), b.get("window_end")))
    if ts(a.get("window_start")) < RESTART:
        failures.append("window_start %s is before the restart" % a.get("window_start"))
    if b.get("window_end"):
        failures.append("window closed at %s" % b.get("window_end"))
    if a.get("window_start") != b.get("window_start"):
        failures.append("window_start changed between reads")
    gap = (ts(b.get("snapshot_at")) - ts(a.get("snapshot_at"))).total_seconds()
    print("SNAPSHOT ADVANCE %d s" % gap)
    if gap < 540:
        failures.append("snapshot advanced only %d s in 600 s" % gap)
    with open(os.path.join(H, "runtimes.json"), encoding="utf-8") as fh:
        wins = json.load(fh).get("monitor_windows") or []
    print("RUNTIMES monitor_windows %s" % wins)
    for w in ("load_monitor.window1.json", "load_monitor.window2.json", "load_monitor.json"):
        if not any(x.endswith(w) for x in wins):
            failures.append("runtimes.json does not list %s" % w)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
