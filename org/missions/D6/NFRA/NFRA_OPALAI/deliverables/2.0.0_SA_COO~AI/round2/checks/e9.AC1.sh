#!/usr/bin/env bash
# OA-e-9 AC1 (the census's shape): E9_GATEWAY_UNRELEASED_CENSUS.md is COMMITTED at HEAD, names BASE and HEAD commits and a
# DENOMINATOR, carries exactly DENOMINATOR commit rows, and every row is classed released-elsewhere | unreleased |
# superseded and names an owning project code.
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~10/E9_GATEWAY_UNRELEASED_CENSUS.md"
git cat-file -e "HEAD:$F" 2>/dev/null || { echo "census not committed at HEAD"; echo "RESULT: FAIL"; exit 1; }
t=$(git show "HEAD:$F" | tr -d '\r')
den=$(printf '%s\n' "$t" | grep -m1 -oE '^DENOMINATOR: [0-9]+' | grep -oE '[0-9]+')
base=$(printf '%s\n' "$t" | grep -m1 -oE '^BASE: [0-9a-f]{10,40}' | awk '{print $2}')
head=$(printf '%s\n' "$t" | grep -m1 -oE '^HEAD: [0-9a-f]{10,40}' | awk '{print $2}')
rows=$(printf '%s\n' "$t" | grep -cE '^\| [0-9a-f]{10} \|')
classed=$(printf '%s\n' "$t" | grep -E '^\| [0-9a-f]{10} \|' | grep -cE '\| (released-elsewhere|unreleased|superseded) \|')
owned=$(printf '%s\n' "$t" | grep -E '^\| [0-9a-f]{10} \|' | grep -cE '\| [A-Z]{3,}_[A-Z0-9]+ ')
echo "base=${base:-NONE} head=${head:-NONE} denominator=${den:-NONE} rows=$rows classed=$classed with-project=$owned"
if [ -n "$den" ] && [ -n "$base" ] && [ -n "$head" ] && [ "$rows" = "$den" ] && [ "$classed" = "$den" ] && [ "$owned" = "$den" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
