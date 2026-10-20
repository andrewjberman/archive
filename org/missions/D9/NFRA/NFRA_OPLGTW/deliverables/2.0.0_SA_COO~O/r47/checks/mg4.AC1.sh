#!/usr/bin/env bash
# OPLGTW OG-mg-4 AC1 (round 47, the CTO's C1 ruling): the in-flight cap is 26 and nothing else about the guard moved.
# app/inflight_guard.py: MAX_INFLIGHT == 26, QUEUE_WAIT_S == 20.0, the process-wide guard's snapshot limit == 26, Busy.code unchanged; against the pinned blob c7716b5398 the file differs by
# exactly one removed and one added line (the constant). tests/test_og_mg3.py against the pinned blob 0d62677122 differs by at most 3 lines, every added line names 26.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
res=$(python3 -I - "$(native "$G")" <<'PYEOF'
import difflib, subprocess, sys
G = sys.argv[1]
sys.path.insert(0, G)
from app import inflight_guard as ig
const_ok = ig.MAX_INFLIGHT == 26 and ig.QUEUE_WAIT_S == 20.0 and ig.guard.snapshot()["limit"] == 26 and getattr(ig.Busy, "code", None) == "gateway_busy"
print("module constants: MAX_INFLIGHT %r, QUEUE_WAIT_S %r, process-wide guard limit %r, Busy.code unchanged: %s" % (ig.MAX_INFLIGHT, ig.QUEUE_WAIT_S, ig.guard.snapshot()["limit"], "ok" if const_ok else "NO"))


def delta(path, pin):
    old = subprocess.run(["git", "show", pin], capture_output=True).stdout.decode("utf-8").splitlines()
    new = open(path, encoding="utf-8").read().splitlines()
    d = list(difflib.unified_diff(old, new, lineterm="", n=0))
    return [x[1:] for x in d if x.startswith("-") and not x.startswith("---")], [x[1:] for x in d if x.startswith("+") and not x.startswith("+++")]


r, a = delta(G + "/app/inflight_guard.py", "c7716b53980c742038e6b23f1f75f7bd66f2cc7b")
g_ok = len(r) == 1 and len(a) == 1 and "MAX_INFLIGHT" in a[0] and "26" in a[0]
print("inflight_guard.py against the pin: %d removed, %d added (want 1 and 1, the constant): %s" % (len(r), len(a), "ok" if g_ok else "NO"))
r, a = delta(G + "/tests/test_og_mg3.py", "0d6267712240be30441ce516528bb394a1340271")
t_ok = 1 <= len(a) <= 3 and len(r) == len(a) and all("26" in x for x in a)
print("test_og_mg3.py against the pin: %d removed, %d added (want equal, 1 to 3, each added names 26): %s" % (len(r), len(a), "ok" if t_ok else "NO"))
print("OK" if const_ok and g_ok and t_ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
