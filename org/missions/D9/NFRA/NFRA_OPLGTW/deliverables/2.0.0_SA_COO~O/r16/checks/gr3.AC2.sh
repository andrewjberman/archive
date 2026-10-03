#!/usr/bin/env bash
# OPLGTW OG-gr-3 AC2 (narrow): every gateway file the cell's worker commits touched is one of
# app/integrations/schwab/query.py, app/integrations/schwab/datasets.json, tests/test_schwab_grain_r9.py.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="0.9.0_WK_NFRA_OPLGTW~22 <"; S="$GW/app/integrations/schwab"
files=$(git log --author="$W" --format= --name-only 8e0fed682a..HEAD -- "$GW" | grep . | sort -u)
n=$(printf '%s\n' "$files" | grep -c .)
allowed=$(printf '%s\n' "$S/query.py" "$S/datasets.json" "$GW/tests/test_schwab_grain_r9.py" | sort -u)
no=$(comm -23 <(printf '%s\n' "$files" | grep .) <(printf '%s\n' "$allowed") | grep -c .)
echo "gateway files touched by the cell's commits since the issuance: $n; outside the allowed three: $no"
[ "$n" -ge 2 ] && [ "$no" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
