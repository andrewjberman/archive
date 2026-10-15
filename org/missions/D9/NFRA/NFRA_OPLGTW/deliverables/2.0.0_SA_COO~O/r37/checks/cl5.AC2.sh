#!/usr/bin/env bash
# OPLGTW OG-cl-5 AC2 (round-37, FWD-22): the worker's probe, RE-RUN here, reads the real silver with the box's credentials and an Opal stand-in principal and asserts
# the envelope, a count equal to an independent read, the fence negative arm and that no account number was printed. The probe prints counts and booleans only.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~107"
P="$W/probe_smartx.py"
[ -f "$P" ] || { echo "$P absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 115 python "$P" 2>&1 | tr -d '\r'); rc=$?
echo "$out" | grep -E "^probe smartx:" | tail -n 3
leak=$(printf '%s\n' "$out" | grep -cE '[0-9]{8,}')
echo "probe rc $rc; digit runs of 8 or more in the output $leak (want 0)"
printf '%s\n' "$out" | grep -qE "^probe smartx: envelope_ok True; independent_count_equal True; fence_negative_arm True; account_numbers_printed 0" && [ "$rc" = 0 ] && [ "$leak" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
