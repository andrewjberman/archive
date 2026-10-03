#!/usr/bin/env bash
# OA-f-13 AC1 (built): opal_ai/opal/runtime/provision/wall-dapi-8194-wfp.ps1 at ${OA_F13_REF:-HEAD} grades its sublayer
# read-back on name + the PERSISTENT flag and PRINTS the engine-assigned weight, instead of demanding weight == 0xFFFF
# (row Z-S54: on this box the engine holds the sublayer at 0xFFE2 under 29 EDR sublayers). Arms, all non-elevated:
#   lines  the C# compiled alone (no WFP engine opened); [OpalWfp]::SubLayerLine(name, weight, flags) returns
#          seam  (wall name, 0xFFE2, 1) -> 'VERIFY: opal_runtime_dapi_8194_wall WEIGHT 0xFFE2 OK'
#          top   (wall name, 0xFFFF, 1) -> 'VERIFY: opal_runtime_dapi_8194_wall WEIGHT 0xFFFF OK'
#          flag  (wall name, 0xFFE2, 0) -> 'VERIFY: opal_runtime_dapi_8194_wall WEIGHT 0xFFE2 FAIL'
#          name  ('x', 0xFFE2, 1)       -> 'VERIFY: opal_runtime_dapi_8194_wall WEIGHT 0xFFE2 FAIL'
#   wire   Verify()'s body calls SubLayerLine( and no longer compares '== SUBLAYER_WEIGHT'
#   plan   the script's own -Plan mode prints 'COMPILE: OK', exit 0
#   bound  parses; vs r2-dev bd7cd5d the only file changed is wall-dapi-8194-wfp.ps1
. "$(dirname "$0")/_root.sh"
REF="${OA_F13_REF:-HEAD}"; BASE="bd7cd5d1ce"; F="opal/runtime/provision/wall-dapi-8194-wfp.ps1"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/f13ac1_$$")"; mkdir -p "$T"
git -C opal_ai show "$REF:$F" > "$T/w.ps1" 2>/dev/null || { echo "wall-dapi-8194-wfp.ps1 absent at $REF"; rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
WT="$(cygpath -w "$T" 2>/dev/null || echo "$T")"
wire=$(python - "$T" <<'PY'
import sys, os, re
t = sys.argv[1]
src = open(os.path.join(t, "w.ps1"), encoding="utf-8").read().split("\n")
try:
    a = next(i for i, l in enumerate(src) if l.rstrip("\r") == "$cs = @'")
    b = next(i for i in range(a + 1, len(src)) if src[i].rstrip("\r") == "'@")
except StopIteration:
    print("NO-CS"); sys.exit(0)
cs = "\n".join(src[a + 1:b])
open(os.path.join(t, "cs.txt"), "w", encoding="utf-8").write(cs)
m = re.search(r"public static string\[\] Verify\(\)(.*?)\n    (public |static |//)", cs, re.S)
body = m.group(1) if m else ""
print("calls=%d compares=%d" % (body.count("SubLayerLine("), body.count("== SUBLAYER_WEIGHT")))
PY
)
lines=$(timeout 90 powershell -NoProfile -ExecutionPolicy Bypass -Command "Add-Type -TypeDefinition (Get-Content -Raw -LiteralPath '$WT\\cs.txt') -Language CSharp; \$n='opal_runtime_dapi_8194_wall'; [OpalWfp]::SubLayerLine(\$n, 0xFFE2, 1); [OpalWfp]::SubLayerLine(\$n, 0xFFFF, 1); [OpalWfp]::SubLayerLine(\$n, 0xFFE2, 0); [OpalWfp]::SubLayerLine('x', 0xFFE2, 1)" 2>&1 | tr -d '\r')
l1=$(printf '%s\n' "$lines" | sed -n 1p); l2=$(printf '%s\n' "$lines" | sed -n 2p); l3=$(printf '%s\n' "$lines" | sed -n 3p); l4=$(printf '%s\n' "$lines" | sed -n 4p)
planout=$(timeout 90 powershell -NoProfile -ExecutionPolicy Bypass -File "$WT\\w.ps1" -Plan 2>&1 | tr -d '\r'); prc=$?
pcomp=$(printf '%s\n' "$planout" | grep -c '^COMPILE: OK$')
pe=$(timeout 40 powershell -NoProfile -Command "\$e=\$null; [void][System.Management.Automation.Language.Parser]::ParseFile('$WT\\w.ps1',[ref]\$null,[ref]\$e); \$e.Count" 2>&1 | tr -d '\r' | tail -1)
others=$(git -C opal_ai diff --name-only "$BASE" "$REF" 2>/dev/null | grep -v -x -F -e "$F" | grep -c .)
rm -rf "$T"
P="VERIFY: opal_runtime_dapi_8194_wall WEIGHT"
echo "opal_ai $REF: seam '${l1:-none}'; top '${l2:-none}'; flag '${l3:-none}'; name '${l4:-none}'; wire ${wire:-none}; plan COMPILE:OK=$pcomp rc=$prc; parse errors=$pe; other files changed vs $BASE=$others"
if [ "$l1" = "$P 0xFFE2 OK" ] && [ "$l2" = "$P 0xFFFF OK" ] && [ "$l3" = "$P 0xFFE2 FAIL" ] && [ "$l4" = "$P 0xFFE2 FAIL" ] \
   && printf '%s' "$wire" | grep -Eq '^calls=[1-9][0-9]* compares=0$' &&[ "$pcomp" = 1 ] && [ "$prc" = 0 ] && [ "$pe" = 0 ] && [ "$others" = 0 ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
