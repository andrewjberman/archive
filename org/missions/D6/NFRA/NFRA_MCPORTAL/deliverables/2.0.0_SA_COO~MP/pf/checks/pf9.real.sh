#!/usr/bin/env bash
# MP-pf-9, the issuer's REAL RUN of the outcome (not a worker criterion): after the bundle release, the SERVED breakdown body (read over SSM, holders redacted) is rendered through the real GatewayView
# and the CSS of mcportal c66ca82952 (the deployed bundle's sha256 equals a build of it, pf9.AC2.sh) and measured in a real browser at 390 and 1280 px.
# usage: pf9.real.sh [keep]   -- with `keep` the rendered html is left at $RENDER_OUT for the issuer to screenshot and READ before anything is committed; it is never committed.
# Prints counts and widths only: no index name, no holder, no account number.
. "$(dirname "$0")/../../pc/checks/_root.sh"
MC="${MP_PF9_MC:-C:/tmp/mp-pf-render}"
[ -f "$MC/src/pages/gateway/GatewayView.tsx" ] || { echo "$MC/src/pages/gateway/GatewayView.tsx absent"; echo "RESULT: FAIL"; exit 1; }
head=$(git -C "$MC" rev-parse HEAD 2>&1 | tr -d '\r')
[ "$head" = c66ca82952c01575968d16cc736cdabe36606572 ] || { echo "render checkout at $head, want c66ca82952c0..."; echo "RESULT: FAIL"; exit 1; }
PW="$(git worktree list --porcelain | sed -n '1s/^worktree //p')/portal/node_modules/playwright-core"
[ -d "$PW" ] || { echo "playwright-core absent at $PW"; echo "RESULT: FAIL"; exit 1; }
BUN="$(command -v bun || ls "$HOME"/AppData/Local/Microsoft/WinGet/Packages/Oven-sh.Bun_*/bun-windows-x64/bun.exe 2>/dev/null | head -1)"
[ -n "$BUN" ] || { echo "bun not found"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_pf9real_$$"; mkdir -p "$T"; Tw="$(cygpath -m "$T")"
CK="org/missions/D6/NFRA/NFRA_MCPORTAL/deliverables/2.0.0_SA_COO~MP/pf/checks"
bl=$(bash "$CK/s1_served_body.sh" "$Tw/body.json" 2>&1 | grep -E '^(body:|RESULT)' | tr '\n' ' ')
echo "$bl"
printf '%s' "$bl" | grep -q 'RESULT: READ' || { rm -rf "$T"; echo "RESULT: FAIL"; exit 1; }
cp "$CK/_gw_render_body.tsx" "$MC/.pf9_render.tsx"
r=$(cd "$MC" && timeout 90 "$BUN" run .pf9_render.tsx "$Tw/page.html" "$Tw/body.json" 2>&1 | tail -1); rm -f "$MC/.pf9_render.tsx"
echo "$r"
m390=$(timeout 90 node "$CK/_gw_measure.cjs" "$(cygpath -m "$PW")" "$Tw/page.html" 390 2>&1 | tail -1)
m1280=$(timeout 90 node "$CK/_gw_measure.cjs" "$(cygpath -m "$PW")" "$Tw/page.html" 1280 2>&1 | tail -1)
echo "served body at 390: $m390"; echo "served body at 1280: $m1280"
if [ "$1" = keep ]; then mkdir -p /c/tmp/mp-pf9-real && cp "$T/page.html" /c/tmp/mp-pf9-real/page.html && echo "kept: C:/tmp/mp-pf9-real/page.html (NOT to be committed)"; fi
rm -rf "$T"
ok() { printf '%s' "$1" | grep -q 'ok=yes' && printf '%s' "$1" | grep -q 'offenders=0'; }
if printf '%s' "$r" | grep -q '^rendered served body' && ok "$m390" && ok "$m1280"; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
