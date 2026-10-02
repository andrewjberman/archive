#!/usr/bin/env bash
# OPLGTW OG-au-1 AC2 (narrow): every gateway file the cell's worker commits touched is one of app/audit.py,
# app/tools.py, tests/test_audit_bytes_principal.py. Author anchored on "<serial> <" so sibling lanes do not match.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="0.9.0_WK_NFRA_OPLGTW~19 <"
files=$(git log --author="$W" --format= --name-only HEAD -- "$GW" | grep . | sort -u)
n=$(printf '%s\n' "$files" | grep -c .)
allowed=$(printf '%s\n' "$GW/app/audit.py" "$GW/app/tools.py" "$GW/tests/test_audit_bytes_principal.py" | sort -u)
out=$(comm -23 <(printf '%s\n' "$files" | grep .) <(printf '%s\n' "$allowed"))
no=$(printf '%s\n' "$out" | grep -c .)
echo "gateway files touched by the cell's commits: $n; outside the allowed three: $no"
[ "$no" = 0 ] || printf '  outside: %s\n' $out
if [ "$n" -ge 2 ] && [ "$no" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
