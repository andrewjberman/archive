#!/usr/bin/env bash
# OPLGTW OG-gt-8 AC2 (round-37, FWD-22): deploy-to-ec2.sh stages lib/trading_calendar.py into the artifact root as lib/,
# the tar names `lib`, the script still parses, and the staged source is the repo's own file (not a copy kept in the gateway dir).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
S="$GW/deploy-to-ec2.sh"
bash -n "$S"; syn=$?
stage=$(grep -cE 'cp .*lib/trading_calendar\.py.*\$TMP/bundle/lib' "$S" | tr -d '\r')
tarlib=$(sed -n '/^tar -czf/,/^echo "INFO: built artifact/p' "$S" | grep -cE '^\s+-C "\$TMP/bundle" .*\blib\b|^\s+lib( |$)|"\$TMP/bundle" lib' | tr -d '\r')
copy_in_gw=$(git ls-files "$GW" | grep -c '/lib/trading_calendar\.py$' | tr -d '\r')
echo "bash -n rc $syn; stage line $stage (want 1); tar names lib $tarlib (want 1+); a second copy of the calendar under the gateway dir $copy_in_gw (want 0)"
[ "$syn" = 0 ] && [ "$stage" = 1 ] && [ "$tarlib" -ge 1 ] && [ "$copy_in_gw" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
