#!/usr/bin/env bash
# OPLGTW OG-gw-1 AC2 (narrow): every infra file the cell's worker commits touched is one of the grant writer's
# build_package.py, tests/test_build_input_pinned.py, .gitignore. Author anchored on "<serial> <".
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
L="infra/aws/lambda/mcportal/mcportal-grant-writer-lambda"; W="0.9.0_WK_NFRA_OPLGTW~25 <"
files=$(git log --author="$W" --format= --name-only HEAD -- infra/aws | grep . | sort -u)
n=$(printf '%s\n' "$files" | grep -c .)
allowed=$(printf '%s\n' "$L/build_package.py" "$L/tests/test_build_input_pinned.py" "$L/.gitignore" | sort -u)
no=$(comm -23 <(printf '%s\n' "$files" | grep .) <(printf '%s\n' "$allowed") | grep -c .)
echo "infra files touched by the cell's commits: $n; outside the allowed three: $no"
[ "$n" -ge 2 ] && [ "$no" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
