#!/usr/bin/env bash
# MP-pd-8 AC1 (FWD-21 DONE WHEN, the write half; decomposition PD.1, PD.6): the worker's run file
# deliverables/0.9.0_WK_NFRA_MCPORTAL~30/pd8_run.json carries {"principal":{"tid","oid"},"t0","t1","steps":[...]}; each step is
# {"op","store_after","history_row","effect"}. The six ops, in order, are: channel_off, channel_on, tool_off, tool_on, stop,
# restore. The checker requires, for every step: the grant store's record read AFTER the op shows the intended change
# (store_after_matches true); the change history holds a set_person_access row for the principal whose `after` equals the store
# read and whose `before` equals the prior step's store read (history_before_after true); and the step's effect on the
# principal's NEXT gateway call is the expected one (effect_ok true: off/stop deny, on/restore admit). 6 of 6 steps, each three
# ways, or it is not a pass.
. "$(dirname "$0")/_root.sh"
RUN="${MP_PD8_RUN:-$PDD/0.9.0_WK_NFRA_MCPORTAL~30/pd8_run.json}"
v=$(python - "$RUN" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("run=unreadable(%s)" % type(e).__name__); print("PASSCOND no"); sys.exit()
want = ["channel_off", "channel_on", "tool_off", "tool_on", "stop", "restore"]
st = d.get("steps") or []
ops = [s.get("op") for s in st if isinstance(s, dict)]
a = sum(1 for s in st if isinstance(s, dict) and s.get("store_after_matches") is True)
b = sum(1 for s in st if isinstance(s, dict) and s.get("history_before_after") is True)
c = sum(1 for s in st if isinstance(s, dict) and s.get("effect_ok") is True)
p = d.get("principal") or {}
good = ops == want and a == 6 and b == 6 and c == 6 and p.get("tid") and p.get("oid") and d.get("t0") and d.get("t1")
print("run=read ops=%s store_after_matches=%d of 6 history_before_after=%d of 6 effect_ok=%d of 6 window=%s..%s" % ("ordered" if ops == want else ",".join(map(str, ops)), a, b, c, d.get("t0"), d.get("t1")))
print("PASSCOND " + ("yes" if good else "no"))
PY
)
printf '%s\n' "$v" | grep -v '^PASSCOND'
if printf '%s' "$v" | grep -q '^PASSCOND yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
