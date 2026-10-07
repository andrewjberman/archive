#!/usr/bin/env bash
# OPLGTW OG-fl-1 AC1 (row Z-W15-S58, CTO round-19 analysis s.4 item 3): test_ogx2_ac01 is DETERMINISTIC -- 20 runs of
# tests/test_schwab_export_stream.py::test_ogx2_ac01, each in its own process, pass 20 of 20; and FL1_CAUSE.md names the
# job_failed cause (one of: timing, shared path, engine deadline, other -- stated) with the fix's commit.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
R="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~26/FL1_CAUSE.md"
export AUDIT_PATH="${TMP:-/tmp}/og_r20_fl1_audit_$$.jsonl"
p=0; for i in $(seq 1 20); do
  ( cd "$GW" && timeout 120 python -m pytest "tests/test_schwab_export_stream.py::test_ogx2_ac01" -q -p no:cacheprovider --color=no >/dev/null 2>&1 ) && p=$((p+1))
done
restore_audit; rm -f "$AUDIT_PATH"
cause=no; [ -f "$R" ] && grep -qiE '^cause: *(timing|shared path|engine deadline|other)' "$R" && grep -qiE 'commit [0-9a-f]{7,}' "$R" && cause=yes
echo "test_ogx2_ac01 passed $p of 20 own-process runs; FL1_CAUSE.md names the cause and the fix commit: $cause"
[ "$p" = 20 ] && [ "$cause" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
