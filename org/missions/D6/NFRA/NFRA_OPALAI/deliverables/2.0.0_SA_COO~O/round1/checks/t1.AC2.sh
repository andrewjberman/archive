#!/usr/bin/env bash
# OA-t-1 AC2 (the move, parent side): the 14 moved parent paths are ABSENT at this worktree's HEAD, and no code/config
# file at HEAD still references them (C1: move, never copy; every consumer re-pointed in the same change).
# Census scope (printed): code/config pathspecs; the fence hook and its test are OA-t-3's and are excluded here.
. "$(dirname "$0")/_root.sh"
S="org/tier0_utility/0.0.3_BG_BBGTerminal"
OLD="$S/prompt.md $S/refs/BLOOMBERG_GUARDRAILS.md $S/refs/BUCKET_ALLOWLIST.yaml $S/refs/PORTAL_RETRIEVAL.md $S/refs/RELAUNCH.md
$S/refs/REQUEST_CATALOG.md $S/refs/TEAMS_DUTY.md $S/refs/THREAD_MEMORY.md $S/refs/census/ARTIFACT_CENSUS_MACRO.yaml
$S/refs/census/ARTIFACT_CENSUS_MP.yaml $S/refs/census/ARTIFACT_CENSUS_NEWS.yaml $S/refs/census/ARTIFACT_CENSUS_POD2.yaml
$S/tools/portal_lookup.py .claude/skills/bbg-teams-assist/SKILL.md"
n=0; gone=0; still=""
for f in $OLD; do n=$((n+1)); if git cat-file -e "HEAD:$f" 2>/dev/null; then still="$still $f"; else gone=$((gone+1)); fi; done
PAT='0\.0\.3_BG_BBGTerminal/(refs/|prompt\.md|tools/portal_lookup)|skills/bbg-teams-assist'
SCOPE=".claude/ .tools/ org/mcp/ infra/ integrations/ lib/ *.ps1"
hits=$(git grep -l -E "$PAT" HEAD -- .claude/ .tools/ org/mcp/ infra/ integrations/ lib/ '*.ps1' \
  ':!.tools/hooks/bg-concierge-gate.sh' ':!.tools/hooks/tests/test_bg_concierge_gate.sh' 2>/dev/null | sed 's/^HEAD://')
nh=$(printf '%s' "$hits" | grep -c . )
echo "moved paths absent at HEAD: $gone of $n; code/config files still referencing them: $nh (scope: $SCOPE)"
[ -n "$still" ] && echo "still present:$still"
[ "$nh" != 0 ] && printf '%s\n' "$hits" | sed 's/^/  ref: /'
if [ "$gone" = "$n" ] && [ "$nh" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
