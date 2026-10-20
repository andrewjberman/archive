#!/usr/bin/env bash
# MP-zo-4 AC1 (FWD-24, 25, 27, 28, 29 close run; decomposition OGW1.7): the worker's run file
# deliverables/0.9.0_WK_NFRA_MCPORTAL~44/zo4_run.json carries {"principal":{"tid","oid"},"t0","t1","steps":[...]}; each step is
# {"op","store_after","history_row","effect"} plus the booleans below. The six ops, in order, are: channel_off, channel_on, tool_off,
# tool_on, stop, restore. For every step the checker requires: the grant store's record after the op shows the intended change
# (store_after_matches true); the change history holds a set_person_access row for the principal whose `after` equals that read and whose
# `before` equals the prior step's read (history_before_after true); that row names a writer (history_attributed true); and the served
# gateway's answer to the principal's NEXT call agrees with the switch the store state implies (effect_ok true: off/stop deny, on/restore
# admit). 6 of 6 steps, each four ways, or it is not a pass.
. "$(dirname "$0")/../../pd/checks/_root.sh"
RUN="${MP_ZO4_RUN:-$PDD/0.9.0_WK_NFRA_MCPORTAL~44/zo4_run.json}"
v=$(python - "$RUN" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("run=unreadable(%s)" % type(e).__name__); print("PASSCOND no"); sys.exit()
want = ["channel_off", "channel_on", "tool_off", "tool_on", "stop", "restore"]
st = d.get("steps") or []
ops = [s.get("op") for s in st if isinstance(s, dict)]
def n(key):
    return sum(1 for s in st if isinstance(s, dict) and s.get(key) is True)
a, b, h, c = n("store_after_matches"), n("history_before_after"), n("history_attributed"), n("effect_ok")
p = d.get("principal") or {}
good = ops == want and a == 6 and b == 6 and h == 6 and c == 6 and p.get("tid") and p.get("oid") and d.get("t0") and d.get("t1")
print("run=read ops=%s store_after_matches=%d of 6 history_before_after=%d of 6 history_attributed=%d of 6 effect_ok=%d of 6 window=%s..%s" % ("ordered" if ops == want else ",".join(map(str, ops)), a, b, h, c, d.get("t0"), d.get("t1")))
print("PASSCOND " + ("yes" if good else "no"))
PY
)
printf '%s\n' "$v" | grep -v '^PASSCOND'
if printf '%s' "$v" | grep -q '^PASSCOND yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
