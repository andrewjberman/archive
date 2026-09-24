#!/usr/bin/env bash
# OA-t-3 AC2 (the runtime setup's shape): mcp.json.example lists exactly one server, opal-gateway-bbg; CLAUDE.md imports
# ../agent/prompt.md and names Opal_Agent; .claude/settings.json registers concierge-gate.sh as a PreToolUse hook;
# launcher.ps1 fetches --ff-only; nothing under opal/runtime names ajb_workspace, AWS_PROFILE or a fabric serial; and
# the parent's .tools/hooks/bg-concierge-gate.sh is gone at HEAD (moved, never copied).
. "$(dirname "$0")/_root.sh"
D="opal_ai/opal/runtime"
servers=$(python -c "import json,sys;print(','.join(sorted(json.load(open(sys.argv[1],encoding='utf-8')).get('mcpServers',{}).keys())))" "$D/mcp.json.example" 2>/dev/null || echo PARSE-FAIL)
imp=$(grep -c '@\.\./agent/prompt\.md' "$D/CLAUDE.md" 2>/dev/null || echo 0)
nm=$(grep -c 'Opal_Agent' "$D/CLAUDE.md" 2>/dev/null || echo 0)
hook=$(python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print(sum(1 for m in d.get('hooks',{}).get('PreToolUse',[]) for h in m.get('hooks',[]) if 'concierge-gate.sh' in h.get('command','')))" "$D/.claude/settings.json" 2>/dev/null || echo 0)
ff=$(grep -c -- '--ff-only' "$D/launcher.ps1" 2>/dev/null || echo 0)
bad=$(grep -rlE 'ajb_workspace|AWS_PROFILE|[0-9]\.[0-9]\.[0-9]_[A-Z]{2}_' "$D" 2>/dev/null | wc -l | tr -d ' ')
gone=yes; git cat-file -e "HEAD:.tools/hooks/bg-concierge-gate.sh" 2>/dev/null && gone=no
echo "mcp servers=[$servers]; CLAUDE.md import=$imp name=$nm; fence registrations=$hook; launcher --ff-only=$ff; runtime files naming workspace/AWS/serial=$bad; parent fence gone=$gone"
if [ "$servers" = "opal-gateway-bbg" ] && [ "$imp" -ge 1 ] && [ "$nm" -ge 1 ] && [ "$hook" -ge 1 ] && [ "$ff" -ge 1 ] && [ "$bad" = 0 ] && [ "$gone" = yes ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
