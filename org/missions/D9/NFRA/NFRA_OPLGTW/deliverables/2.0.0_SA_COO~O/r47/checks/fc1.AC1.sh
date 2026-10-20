#!/usr/bin/env bash
# OPLGTW OG-fc-1 AC1 (round 47, D1 / Z-S409): the client core's fence kinds hold orion, eclipse and commonwealth, so firm_segments()
# is no longer empty for the three served pairs, and the fence did not widen (control pairs unchanged).
# Real Ctx over the repo's DATA_CATALOG (no network). Expected segments: orion/inflection -> [inflection], eclipse/inflection -> [inflection],
# commonwealth/cottonwood -> [cottonwood]; controls: blackdiamond/cottonwood -> [cottonwood] (unchanged), orion/cottonwood -> [], eclipse/49financial -> [],
# commonwealth/inflection -> [], schwab/49financial -> non-empty (unchanged).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 100 python3 -I - <<'EOF'
import sys
sys.path.insert(0, ".")
from app import client_core as core
ctx = core.Ctx()
n = core._names()
k49, kct, kinf = n["canonical"]
def seg(v, f):
    return list(ctx.firm_segments(v, f))
want = [("orion", kinf, ["inflection"]), ("eclipse", kinf, ["inflection"]), ("commonwealth", kct, ["cottonwood"])]
ctl = [("blackdiamond", kct, ["cottonwood"]), ("orion", kct, []), ("eclipse", k49, []), ("commonwealth", kinf, [])]
ok = True
served = 0
for v, f, w in want:
    got = seg(v, f)
    served += 1 if got == w else 0
    print("served pair %s/%s: segments %s (want %s): %s" % (v, f, got, w, "ok" if got == w else "NO"))
    ok = ok and got == w
held = 0
for v, f, w in ctl:
    got = seg(v, f)
    held += 1 if got == w else 0
    print("control pair %s/%s: segments %s (want %s): %s" % (v, f, got, w, "ok" if got == w else "NO"))
    ok = ok and got == w
sw = seg("schwab", k49)
print("control pair schwab/%s: %d segment(s) (want >= 1): %s" % (k49, len(sw), "ok" if sw else "NO"))
ok = ok and bool(sw)
print("served pairs %d of 3; controls held %d of 4" % (served, held))
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
