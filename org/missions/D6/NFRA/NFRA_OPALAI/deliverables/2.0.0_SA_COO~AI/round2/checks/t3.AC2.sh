#!/usr/bin/env bash
# ROUND-2 RE-CUT COPY of round 1 t3.AC2.sh (2.0.0_SA_COO~AI). ONE amendment: the runtime files are read from a detached opal_ai worktree at $OA_NESTED_PIN (_pin.sh);
# the parent-fence read stays at the parent HEAD.
# OA-t-3 AC2 (the runtime setup's shape): mcp.json.example lists exactly one server, opal-gateway-bbg; CLAUDE.md imports
# ../agent/prompt.md and names Opal_Agent; .claude/settings.json registers concierge-gate.sh as a PreToolUse hook;
# launcher.ps1 fetches --ff-only; nothing under opal/runtime names ajb_workspace, AWS_PROFILE or a fabric serial; and
# the parent's .tools/hooks/bg-concierge-gate.sh is gone at HEAD (moved, never copied).
. "$(dirname "$0")/_root.sh"
. "$(dirname "$0")/_pin.sh"
D="$PT/opal/runtime"
servers=$(python -c "import json,sys;print(','.join(sorted(json.load(open(sys.argv[1],encoding='utf-8')).get('mcpServers',{}).keys())))" "$D/mcp.json.example" 2>/dev/null || echo PARSE-FAIL)
imp=$(grep -c '@\.\./agent/prompt\.md' "$D/CLAUDE.md" 2>/dev/null || echo 0)
nm=$(grep -c 'Opal_Agent' "$D/CLAUDE.md" 2>/dev/null || echo 0)
hook=$(python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print(sum(1 for m in d.get('hooks',{}).get('PreToolUse',[]) for h in m.get('hooks',[]) if 'concierge-gate.sh' in h.get('command','')))" "$D/.claude/settings.json" 2>/dev/null || echo 0)
ff=$(grep -c -- '--ff-only' "$D/launcher.ps1" 2>/dev/null || echo 0)
# The one exempt line is the config key workspace_probe_file: the face REQUIRES it to name a workspace file (the launch
# gate proves that read is DENIED), so its value is the spec, not a leak. Every other line under opal/runtime is scanned
# (row NFRA_OPALAI-Z-W3-S2).
bad=$(grep -rnE 'ajb_workspace|AWS_PROFILE|[0-9]\.[0-9]\.[0-9]_[A-Z]{2}_' "$D" 2>/dev/null | grep -v '"workspace_probe_file"[[:space:]]*:' | cut -d: -f1 | sort -u | grep -c .)
gone=yes; git cat-file -e "HEAD:.tools/hooks/bg-concierge-gate.sh" 2>/dev/null && gone=no
echo "mcp servers=[$servers]; CLAUDE.md import=$imp name=$nm; fence registrations=$hook; launcher --ff-only=$ff; runtime files naming workspace/AWS/serial=$bad; parent fence gone=$gone"
if [ "$servers" = "opal-gateway-bbg" ] && [ "$imp" -ge 1 ] && [ "$nm" -ge 1 ] && [ "$hook" -ge 1 ] && [ "$ff" -ge 1 ] && [ "$bad" = 0 ] && [ "$gone" = yes ]; then
  echo "RESULT: PASS"; exit 0
fi
echo "RESULT: FAIL"; exit 1
