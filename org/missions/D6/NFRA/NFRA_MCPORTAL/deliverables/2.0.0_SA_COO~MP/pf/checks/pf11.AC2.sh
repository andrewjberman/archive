#!/usr/bin/env bash
# MP-pf-11 AC2 (the Indexes box shows the same scroll cue as a tools table; CTO round analysis b6efe81187, CVO v10 enrichment): in a real browser the Gateway page, rendered from the worker's mcportal tree
# with the checked-in fixture PLUS one 65-character unbroken index name planted in every channel and tool index list (the check plants it), reads at 390 px:
#   every p.gateway-indexes carries four linear-gradient layers with background-attachment `local, local, scroll, scroll`, the same background-image as the `.gateway-scroll` box, and at least one of them really scrolls (content wider than its box).
# The base reads FAIL: the paragraph scrolls but carries no cue (cued=0).
. "$(dirname "$0")/../../pc/checks/_root.sh"
MC="${MP_PF8_MC:-$(pwd)/mcportal}"
[ -f "$MC/src/pages/gateway/GatewayView.tsx" ] || { echo "$MC/src/pages/gateway/GatewayView.tsx absent"; echo "RESULT: FAIL"; exit 1; }
PW="$(git worktree list --porcelain | sed -n '1s/^worktree //p')/portal/node_modules/playwright-core"
[ -d "$PW" ] || { echo "playwright-core absent at $PW"; echo "RESULT: FAIL"; exit 1; }
BUN="$(command -v bun || ls "$HOME"/AppData/Local/Microsoft/WinGet/Packages/Oven-sh.Bun_*/bun-windows-x64/bun.exe 2>/dev/null | head -1)"
[ -n "$BUN" ] || { echo "bun not found"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_pf11_$$"; mkdir -p "$T"
CK="org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks"
cp "$CK/_gw_render_long.tsx" "$MC/.pf8_render.tsx"
r_long=$(cd "$MC" && timeout 90 "$BUN" run .pf8_render.tsx "$(cygpath -m "$T")/long.html" long 2>&1 | tail -1)
rm -f "$MC/.pf8_render.tsx"
echo "$r_long"
m390=$(timeout 90 node "$CK/_gw_cue.cjs" "$(cygpath -m "$PW")" "$(cygpath -m "$T")/long.html" 390 2>&1 | tail -1)
rm -rf "$T"
echo "cue at 390: $m390"
if printf '%s' "$r_long" | grep -q 'rendered long' && printf '%s' "$m390" | grep -q 'ok=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
