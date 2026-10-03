#!/usr/bin/env bash
# OPLGTW OG-sr-1 AC2 (narrow): every gateway file the cell's worker commits touched is one of app/mail_route.py,
# app/transcript_route.py, tests/test_mail_route.py, tests/test_transcript_route.py. Author anchored on "<serial> <".
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="0.9.0_WK_NFRA_OPLGTW~24 <"
files=$(git log --author="$W" --format= --name-only HEAD -- "$GW" | grep . | sort -u)
n=$(printf '%s\n' "$files" | grep -c .)
allowed=$(printf '%s\n' "$GW/app/mail_route.py" "$GW/app/transcript_route.py" "$GW/tests/test_mail_route.py" "$GW/tests/test_transcript_route.py" | sort -u)
out=$(comm -23 <(printf '%s\n' "$files" | grep .) <(printf '%s\n' "$allowed"))
no=$(printf '%s\n' "$out" | grep -c .)
echo "gateway files touched by the cell's commits: $n; outside the allowed four: $no"
[ "$no" = 0 ] || printf '  outside: %s\n' $out
if [ "$n" -ge 4 ] && [ "$no" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
