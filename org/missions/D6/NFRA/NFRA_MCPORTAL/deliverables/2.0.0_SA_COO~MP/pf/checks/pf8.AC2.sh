#!/usr/bin/env bash
# MP-pf-8 AC2 (the page does not scroll sideways at 390 px with REAL-LENGTH index names; CTO msg 34947, row Z-S64): in a real browser the Gateway page, rendered from the worker's mcportal tree with the checked-in fixture
# PLUS one 65-character unbroken index name planted in every channel and tool index list (the check plants it, so the worker's own fixture cannot make the check pass), reads
#   at 390 px: documentElement.scrollWidth <= innerWidth (390)  and  offenders=0 (no element outside a .gateway-scroll box has content wider than its own box);
#   at 1280 px: the same (the control: the page that passes at 390 also passes at 1280);
#   and the SHORT-name control (the fixture as checked in) at 390 px is ok too (so a pass is not the check failing to render anything: the page rendered with bytes > 0 and `rendered long` printed).
# The base reads FAIL: p.gateway-indexes holds the long name wider than its column.
. "$(dirname "$0")/../../pc/checks/_root.sh"
MC="${MP_PF8_MC:-$(pwd)/mcportal}"
[ -f "$MC/src/pages/gateway/GatewayView.tsx" ] || { echo "$MC/src/pages/gateway/GatewayView.tsx absent"; echo "RESULT: FAIL"; exit 1; }
PW="$(git worktree list --porcelain | sed -n '1s/^worktree //p')/portal/node_modules/playwright-core"
[ -d "$PW" ] || { echo "playwright-core absent at $PW"; echo "RESULT: FAIL"; exit 1; }
BUN="$(command -v bun || ls "$HOME"/AppData/Local/Microsoft/WinGet/Packages/Oven-sh.Bun_*/bun-windows-x64/bun.exe 2>/dev/null | head -1)"
[ -n "$BUN" ] || { echo "bun not found"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_pf8_$$"; mkdir -p "$T"
CK="org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks"
cp "$CK/_gw_render_long.tsx" "$MC/.pf8_render.tsx"
render() { (cd "$MC" && timeout 90 "$BUN" run .pf8_render.tsx "$(cygpath -m "$T")/$1.html" "$2" 2>&1 | tail -1); }
r_long=$(render long long); r_short=$(render short short)
rm -f "$MC/.pf8_render.tsx"
echo "$r_long; $r_short"
m390=$(timeout 90 node "$CK/_gw_measure.cjs" "$(cygpath -m "$PW")" "$(cygpath -m "$T")/long.html" 390 2>&1 | tail -1)
m1280=$(timeout 90 node "$CK/_gw_measure.cjs" "$(cygpath -m "$PW")" "$(cygpath -m "$T")/long.html" 1280 2>&1 | tail -1)
s390=$(timeout 90 node "$CK/_gw_measure.cjs" "$(cygpath -m "$PW")" "$(cygpath -m "$T")/short.html" 390 2>&1 | tail -1)
rm -rf "$T"
echo "long names at 390: $m390"; echo "long names at 1280: $m1280"; echo "short names at 390 (control): $s390"
ok() { printf '%s' "$1" | grep -q 'ok=yes' && printf '%s' "$1" | grep -q 'offenders=0'; }
if printf '%s' "$r_long" | grep -q '^rendered long' && ok "$m390" && ok "$m1280" && ok "$s390"; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
