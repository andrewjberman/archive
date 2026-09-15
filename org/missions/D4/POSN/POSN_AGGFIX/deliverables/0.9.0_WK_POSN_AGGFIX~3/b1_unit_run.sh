#!/usr/bin/env bash
# POSN_AGGFIX.TO-B1-1 (slot ~3) -- <UNIT_RUN_B1>: the B1-AC4 unit control, run with the portal's resolver.
# Writes the edf85ce503 copy of shared/bookSet.ts into the workspace scratch with ONE line rewritten (its '@/lib/chartColors'
# alias import pointed at this portal's file, printed below), then runs b1_unit_control.ts from portal/ with bun, the runner
# POSN_ASTTAX round 6 recorded for the same kind of control (~26: `cd portal && bun <deliverables>/w3_presence_unit_control.ts`).
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(git -C "$HERE" rev-parse --show-toplevel)"
PORTAL="$ROOT/portal"
BASE=edf85ce503
SCR="$ROOT/.scratch/unit"
mkdir -p "$SCR"
echo "PORTAL: $PORTAL  HEAD $(git -C "$PORTAL" rev-parse HEAD)  branch $(git -C "$PORTAL" rev-parse --abbrev-ref HEAD)"
echo "src working-tree changes vs HEAD: $(git -C "$PORTAL" status --porcelain -- src | wc -l)"
git -C "$PORTAL" show "$BASE:src/pages/Positioning/shared/bookSet.ts" > "$SCR/bookSet.base.ts"
rc=$?
lines=$(wc -l < "$SCR/bookSet.base.ts")
echo "BASE COPY: $BASE:src/pages/Positioning/shared/bookSet.ts -> .scratch/unit/bookSet.base.ts  rc=$rc  lines=$lines"
if [ "$rc" != 0 ] || [ "$lines" -lt 100 ]; then echo "BLOCKED: the base copy did not resolve"; exit 1; fi
python - "$SCR/bookSet.base.ts" "$PORTAL/src/lib/chartColors.ts" <<'PY'
import sys
p, chart = sys.argv[1], sys.argv[2]
src = open(p, encoding='utf-8').read()
old = "import { PALETTE } from '@/lib/chartColors'"
new = "import { PALETTE } from '" + chart.replace(chr(92), '/') + "'"
n = src.count(old)
print('REWRITE (the only change to the base copy): ' + str(n) + ' occurrence(s)')
print('  - ' + old)
print('  + ' + new)
if n != 1:
    print('BLOCKED: expected exactly one alias import')
    sys.exit(1)
open(p, 'w', encoding='utf-8', newline='\n').write(src.replace(old, new))
PY
[ $? = 0 ] || exit 1
echo "RUNNER: bun $(bun --version)  (cwd portal/)"
echo "---"
cd "$PORTAL" && bun "$HERE/b1_unit_control.ts" "$SCR/bookSet.base.ts"
rc=$?
echo "---"
echo "EXIT=$rc"
exit $rc
