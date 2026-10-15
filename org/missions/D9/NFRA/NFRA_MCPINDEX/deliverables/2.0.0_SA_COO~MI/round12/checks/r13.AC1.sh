#!/usr/bin/env bash
# MX-r-13 AC1: the NEVER-2 ledger nfra-mcpindex-r12-catalog-release-v2 is CLOSED (entry at HEAD, no sentinel, not listed OPEN/HELD).
. "$(dirname "$0")/_root.sh"
S=nfra-mcpindex-r12-catalog-release-v2   # the re-cut's ledger: the first attempt (nfra-mcpindex-r12-catalog-release) closed ROLLED-BACK on r13.AC2
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${S}_deploy_completion.md$")
sn=$(git ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/ | grep -c "/${S}.json$")
lst=$(timeout 60 python .tools/deploy_ledger.py list 2>&1 | tr -d '\r' | sed 's/\x1b\[[0-9;]*m//g')
op=$(printf '%s\n' "$lst" | grep -E "$S" | grep -cE 'OPEN|HELD')
den=$(printf '%s\n' "$lst" | grep -E 'SCAN DENOMINATOR' | tail -1)
echo "entry files at HEAD=$e; sentinel at HEAD=$([ "$sn" = 0 ] && echo no || echo yes); listed OPEN/HELD=$op; $den"
rc=1; [ "$e" -ge 1 ] && [ "$sn" = 0 ] && [ "$op" = 0 ] && [ -n "$den" ] && rc=0
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
