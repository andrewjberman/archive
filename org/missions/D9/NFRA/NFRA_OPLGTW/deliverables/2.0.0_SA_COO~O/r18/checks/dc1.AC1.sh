#!/usr/bin/env bash
# OPLGTW OG-dc-1 AC1 (row Z-S55, CTO R18): .tools/m365-mcp-kit/ now tells a colleague the HOSTED-gateway reconnect --
# README.md (and BOOTSTRAP.md if kept) carry the exact command
#   claude mcp add --transport http -s user opalgateway https://mcp.opalinvest.dev/mcp
# and the work-account sign-in step; the OLD entry the worker named in DC1_RECORD.json (old_entry_marker) is absent
# from every kit file.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
K=".tools/m365-mcp-kit"; R="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~21/DC1_RECORD.json"
[ -f "$R" ] || { echo "$R absent"; echo "RESULT: FAIL"; exit 1; }
CMD='claude mcp add --transport http -s user opalgateway https://mcp.opalinvest.dev/mcp'
has=$(grep -lF "$CMD" "$K"/*.md 2>/dev/null | grep -c .)
mk=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('old_entry_marker',''))" "$(native "$R")" | tr -d '\r')
old=0; [ -n "$mk" ] && old=$(grep -lF "$mk" "$K"/* 2>/dev/null | grep -c .)
signin=$(grep -liE 'work account|opalinvest\.com account' "$K"/README.md 2>/dev/null | grep -c .)
echo "kit files carrying the hosted command $has; old entry marker '${mk:-<none>}' present in $old file(s); README names the work-account sign-in $signin"
[ "$has" -ge 1 ] && [ -n "$mk" ] && [ "$old" = 0 ] && [ "$signin" = 1 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
