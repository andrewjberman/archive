#!/usr/bin/env bash
# OA-e-9 AC2 (an independent recount, not the census's own word): the non-merge commits touching infra/aws/ec2/opal-gateway
# in BASE..HEAD, recounted here from the two commits the census names, equal its DENOMINATOR; and the census records that
# BASE is what the live host serves ("LIVE-MATCH: yes", its md5 read over SSM at the census's cut).
. "$(dirname "$0")/_root.sh"
F="org/missions/D6/NFRA/NFRA_OPALAI/deliverables/0.9.0_WK_NFRA_OPALAI~10/E9_GATEWAY_UNRELEASED_CENSUS.md"
git cat-file -e "HEAD:$F" 2>/dev/null || { echo "census not committed at HEAD"; echo "RESULT: FAIL"; exit 1; }
t=$(git show "HEAD:$F" | tr -d '\r')
den=$(printf '%s\n' "$t" | grep -m1 -oE '^DENOMINATOR: [0-9]+' | grep -oE '[0-9]+')
base=$(printf '%s\n' "$t" | grep -m1 -oE '^BASE: [0-9a-f]{10,40}' | awk '{print $2}')
head=$(printf '%s\n' "$t" | grep -m1 -oE '^HEAD: [0-9a-f]{10,40}' | awk '{print $2}')
live=$(printf '%s\n' "$t" | grep -m1 -oE '^LIVE-MATCH: (yes|no)' | awk '{print $2}')
n=""; [ -n "$base" ] && [ -n "$head" ] && n=$(timeout 60 git rev-list --no-merges --count "$base..$head" -- infra/aws/ec2/opal-gateway 2>&1)
echo "recount=${n:-NONE} denominator=${den:-NONE} live-match=${live:-NONE}"
if [ -n "$n" ] && [ "$n" = "$den" ] && [ "$live" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
