#!/usr/bin/env bash
# MP-zb-1 AC2 (decomposition OGB1.1) -- DRAFT, NOT DRY-RUN: the type check of the page bundle is clean. `tsc --noEmit -p tsconfig.app.json` in the nested
# mcportal worktree, run as bun runs the local package (npx does not find it here).
. "$(dirname "$0")/../../pc/checks/_root.sh"
[ -d mcportal/node_modules/typescript ] || { echo "mcportal/node_modules/typescript absent"; echo "RESULT: FAIL"; exit 1; }
T=$(mktemp); trap 'rm -f "$T"' EXIT
(cd mcportal && timeout 110 bun node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json > "$T" 2>&1); rc=$?
tr -d '\r' < "$T" | tail -3
echo "tsc rc=$rc"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
