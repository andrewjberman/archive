#!/usr/bin/env bash
# OPLGTW OG-ev-7 AC1 (round 43): the peers call measured in the running service, to explain Z-S389 (etfs_compare_peers took 17.9 s through the probe listener against 4.5 s in a fresh process; one reading, one arming).
# It is a MEASUREMENT, not a fix. Everything below is fixed BEFORE the run:
#  - the run: ONE armed lease of 25 minutes or less that pins the firm (OG-pr-4 is live), then three etfs_compare_peers calls through the listener, back to back, in one service process: calls 1 and 2 with the heap signal ON, call 3 with the heap signal OFF
#    (no SIGUSR2 sent for that call); the same call once in a FRESH guarded process on the host (fresh_process_wall_s); then the lease is deleted (ParameterNotFound) and the listener read closed.
#  - SAFETY bounds (a failure is a STOP, not a finding): VmRSS after each call at most 1200 MB (CT3), one service PID throughout, NRestarts 0, armings 1.
#  - the VERDICT is computed from the numbers by the rule below, in this order, and the check recomputes it:
#      COLD              call 1 wall is at least 2 times call 2 wall;
#      SLOW_IN_SERVICE   else, every one of the three walls is more than 2 times fresh_process_wall_s;
#      SIGNAL_COST       else, call 3 (signal off) wall is at least 20 percent below call 2 wall;
#      INCONCLUSIVE      otherwise.
# Record W/PEERS_MEASURE.json = {"body": {"lease_minutes": n, "armings": 1, "firm_pinned": true, "calls": [{"n": 1, "wall_s": x, "vmrss_mb": x, "hwm_mb": x, "service_pid": n, "heap_signal": "on"}, {"n": 2, ... "on"}, {"n": 3, ... "off"}],
#   "fresh_process_wall_s": x, "verdict": "COLD|SLOW_IN_SERVICE|SIGNAL_COST|INCONCLUSIVE", "parameter_not_found_after_delete": true, "listener_closed_at_rest": true, "nrestarts_after": 0}}
# Override (dry-run controls only): EV7_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV7_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/PEERS_MEASURE.json}"
[ -f "$REC" ] || { echo "PEERS_MEASURE.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python -I - "$(native "$REC")" <<'PYEOF'
import json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
isn = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0
calls = b.get("calls") or []
fresh = b.get("fresh_process_wall_s")
shape = (len(calls) == 3 and [c.get("n") for c in calls] == [1, 2, 3] and [c.get("heap_signal") for c in calls] == ["on", "on", "off"]
         and all(isn(c.get("wall_s")) and isn(c.get("vmrss_mb")) and isn(c.get("service_pid")) for c in calls) and isn(fresh))
safe = shape and all(c["vmrss_mb"] <= 1200 for c in calls) and len({c["service_pid"] for c in calls}) == 1
w = [c["wall_s"] for c in calls] if shape else [0, 0, 0]
if shape and w[0] >= 2 * w[1]:
    want = "COLD"
elif shape and all(x > 2 * fresh for x in w):
    want = "SLOW_IN_SERVICE"
elif shape and w[2] <= 0.8 * w[1]:
    want = "SIGNAL_COST"
else:
    want = "INCONCLUSIVE"
frame = (isn(b.get("lease_minutes")) and b["lease_minutes"] <= 25 and b.get("armings") == 1 and b.get("firm_pinned") is True
         and b.get("parameter_not_found_after_delete") is True and b.get("listener_closed_at_rest") is True and b.get("nrestarts_after") == 0)
bignums = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", re.sub(r'"[0-9a-f]{40,64}"', '""', raw))
verdict_ok = b.get("verdict") == want
ok = shape and safe and frame and verdict_ok and not bignums
print("three calls in the order on/on/off with walls %s s, VmRSS %s MB (at most 1200), one PID %s; fresh-process wall %s s" % (w, [c.get("vmrss_mb") for c in calls], "yes" if safe else "NO", fresh))
print("lease %s minutes (25 or fewer), armings %s (want 1), firm pinned %s, ParameterNotFound after the delete %s, listener closed at rest %s, restarts after %s: %s" % (
      b.get("lease_minutes"), b.get("armings"), b.get("firm_pinned"), b.get("parameter_not_found_after_delete"), b.get("listener_closed_at_rest"), b.get("nrestarts_after"), "ok" if frame else "NOT OK"))
print("verdict by the rule fixed before the run: %s; the record says %s: %s; digit runs of 9 or more %d (want 0)" % (want, b.get("verdict"), "consistent" if verdict_ok else "INCONSISTENT", len(bignums)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
