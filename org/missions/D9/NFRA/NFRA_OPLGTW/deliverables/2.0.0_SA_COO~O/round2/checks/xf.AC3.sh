#!/usr/bin/env bash
# OPLGTW OG-x-4 AC3 (CTO ruling msg 26488 (3)): OG-x-2's local flatness proof re-run at FULL WIDTH -- the named test
# test_ogx4_ac03 (OG-x-2's test_ogx2_ac01 harness at the 11 exportable columns of dim_position, through the REAL engine
# and export.generate_csv) passes its flatness bar. Interpreter: the worktree's .venv-og, else python.
. "$(dirname "$0")/_root.sh"
PY=".venv-og/Scripts/python"; [ -x "$PY" ] || PY="python"
T="$GW/tests/test_schwab_export_stream.py"
[ -f "$T" ] || { echo "$T absent"; echo "RESULT: FAIL"; exit 1; }
grep -q '^def test_ogx4_ac03' "$T" || { echo "test_ogx4_ac03 absent in $T; named tests passed 0 of 1"; echo "RESULT: FAIL"; exit 1; }
export AUDIT_PATH="$(mktemp)"
out=$(timeout 110 "$PY" -m pytest "$T::test_ogx4_ac03" -q -s -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
rm -f "$AUDIT_PATH"; restore_audit
printf '%s\n' "$out" | grep -E 'columns|peak|ratio' | tail -6
p=$(printf '%s\n' "$out" | grep -cE '^1 passed')
echo "pytest rc=$rc; named tests passed $p of 1"
[ "$rc" = 0 ] && [ "$p" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
