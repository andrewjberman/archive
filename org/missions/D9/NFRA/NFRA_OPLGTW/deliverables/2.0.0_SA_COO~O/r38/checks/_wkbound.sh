#!/usr/bin/env bash
# OPLGTW round-38 write-set bound: every file touched by commits authored by the worker serial $1 matches the allowed-path regex $2
# (plus the standing record paths: the task orders, the surprise channel, and the serial's own deliverables folder); at least one file was touched.
# Usage: _wkbound.sh <worker serial> <extended regex of allowed product paths>
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
serial="$1"; allow="$2"
[ -n "$serial" ] && [ -n "$allow" ] || { echo "usage: _wkbound.sh <serial> <allowed regex>"; echo "RESULT: FAIL"; exit 2; }
std="^org/missions/D9/NFRA/NFRA_OPLGTW/(task-orders/|surprise-channel/|deliverables/${serial}/)"
files=$(git log --author="${serial} <" --name-only --format= | sort -u | grep -v '^$')
n=$(printf '%s\n' "$files" | grep -c .)
outside=$(printf '%s\n' "$files" | grep -Ev "${allow}|${std}" | grep -c .)
product=$(printf '%s\n' "$files" | grep -Ev "${std}" | grep -c .)
echo "write-set bound for ${serial}: files touched ${n}; product files ${product}; outside the allowed set ${outside} (want 0)"
[ "$n" -ge 1 ] && [ "$product" -ge 1 ] && [ "$outside" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
