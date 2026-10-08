"""OPLGTW OG-g5-1 AC1 (round 32 item 3, PRD v2.0 item 5(a)): the list-only run for master 08403355 beside its control.

Reads the worker's record and RE-READS each SSM invocation it names from AWS (the real neighbour, not the record):
  - both masters present, on the SI2 box, the same search window, the control (08335338) enumerating > 0 files;
  - each invocation terminal, started OUTSIDE [09:15, 11:05) and [21:15, 23:05) UTC (the two daily pulls and their
    50-minute deadlines);
  - the invocation's own output carries `mode=enumerate`, the master, the window line and an ENUMERATED count equal to
    the record's; where files were enumerated, the per-type lines equal the record's `by_type`;
  - the record's side-by-side type comparison equals one recomputed from its `by_type`.

  python g5.AC1.py <record.json>
"""
import datetime as dt
import json
import re
import sys

import boto3

BOX = "i-0f3d57a97f14727af"
MASTERS = ("08403355", "08335338")
FORBIDDEN = ((dt.time(9, 15), dt.time(11, 5)), (dt.time(21, 15), dt.time(23, 5)))


def fail(msg):
    print("FAIL: " + msg)
    return False


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        rec = json.load(open(argv[1], encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("record unreadable: %s (%s)" % (argv[1], type(exc).__name__))
        print("RESULT: FAIL")
        return 1
    ok = True
    if rec.get("instance_id") != BOX:
        ok = fail("instance_id %r is not the SI2 box %s" % (rec.get("instance_id"), BOX))
    runs = rec.get("runs") or {}
    win = rec.get("window") or {}
    ssm = boto3.client("ssm", region_name="us-east-1")
    seen_windows = set()
    for m in MASTERS:
        r = runs.get(m)
        if not isinstance(r, dict):
            ok = fail("no run recorded for master %s" % m)
            continue
        try:
            inv = ssm.get_command_invocation(CommandId=r.get("command_id", ""), InstanceId=BOX)
        except Exception as exc:  # the instrument's own failure is a FAIL, never a pass
            ok = fail("%s: cannot read SSM invocation %r (%s)" % (m, r.get("command_id"), type(exc).__name__))
            continue
        status = inv.get("Status")
        start = inv.get("ExecutionStartDateTime") or ""
        out = (inv.get("StandardOutputContent") or "").replace("\r", "")
        print("%s: invocation %s status=%s started=%s output=%d chars" % (m, r.get("command_id"), status, start,
                                                                          len(out)))
        if status not in ("Success", "Failed"):
            ok = fail("%s: invocation not terminal (%s)" % (m, status))
        try:
            t = dt.datetime.fromisoformat(start.replace("Z", "+00:00")).astimezone(dt.timezone.utc).time()
            if any(a <= t < b for a, b in FORBIDDEN):
                ok = fail("%s: started at %s UTC, inside a daily-pull window" % (m, t))
        except ValueError:
            ok = fail("%s: unparseable start time %r" % (m, start))
        if not re.search(r"master=%s mode=enumerate" % m, out):
            ok = fail("%s: output has no 'master=%s mode=enumerate' header" % (m, m))
        wm = re.search(r"SINGLE WIDE SEARCH (\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2}) -> ENUMERATED=(\d+)", out)
        if not wm:
            ok = fail("%s: output has no SINGLE WIDE SEARCH line" % m)
            continue
        seen_windows.add((wm.group(1), wm.group(2)))
        n = int(wm.group(3))
        if n != r.get("enumerated"):
            ok = fail("%s: output ENUMERATED=%d, record says %r" % (m, n, r.get("enumerated")))
        per_type = {k: int(v) for k, v in re.findall(r"/(\w+)\s+n=(\d+)", out)}
        if n > 0 and per_type != (r.get("by_type") or {}):
            ok = fail("%s: per-type lines %s differ from the record's by_type %s" % (m, per_type, r.get("by_type")))
        print("%s: ENUMERATED=%d over %s..%s; types %d" % (m, n, wm.group(1), wm.group(2), len(per_type)))
    if len(seen_windows) != 1:
        ok = fail("the two runs did not search one window: %s" % sorted(seen_windows))
    elif (win.get("from"), win.get("to")) not in seen_windows:
        ok = fail("record window %r is not the searched window %s" % (win, sorted(seen_windows)))
    ctl = runs.get("08335338") or {}
    if not isinstance(ctl.get("enumerated"), int) or ctl.get("enumerated") <= 0:
        ok = fail("positive control 08335338 enumerated %r files" % ctl.get("enumerated"))
    a = set((runs.get("08403355") or {}).get("by_type") or {})
    b = set(ctl.get("by_type") or {})
    sbs = rec.get("side_by_side") or {}
    if sorted(sbs.get("types_only_in_08403355", [])) != sorted(a - b) or \
            sorted(sbs.get("types_only_in_08335338", [])) != sorted(b - a):
        ok = fail("side_by_side type lists do not equal the by_type difference")
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
