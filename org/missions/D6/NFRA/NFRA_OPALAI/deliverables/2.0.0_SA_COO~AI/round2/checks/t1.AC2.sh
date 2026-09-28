#!/usr/bin/env bash
# ROUND-2 RE-CUT COPY of round 1 t1.AC2.sh (2.0.0_SA_COO~AI). ONE amendment: the catalog one-line diff is read against the ROUND-2 cut $OA_R2_BASE, because NFRA_MCPINDEX
# moved the catalog 61/3 lines after round 1's cut (bc0cde67f0, 2c25c4c831); the re-point itself is unchanged. It reads no nested file.
# OA-t-1 AC2 (the move, parent side): the 10 moved parent paths are ABSENT at this worktree's HEAD, the 4 census files
# are KEPT, the gateway catalog differs from the cut by exactly ONE line (the guardrails_ref re-point), and no code/config
# file at HEAD still references a moved path (C1: move, never copy; every consumer re-pointed in the same change).
# Amended per the CTO's ruling I-4 (D-1): refs/census/ stays with the index; its 30 census_ref lines stay byte-unchanged.
# Census scope (printed): code/config pathspecs; the fence hook and its test are OA-t-3's and are excluded here.
. "$(dirname "$0")/_root.sh"
S="org/tier0_utility/0.0.3_BG_BBGTerminal"
C="infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml"
OLD="$S/prompt.md $S/refs/BLOOMBERG_GUARDRAILS.md $S/refs/BUCKET_ALLOWLIST.yaml $S/refs/PORTAL_RETRIEVAL.md $S/refs/RELAUNCH.md
$S/refs/REQUEST_CATALOG.md $S/refs/TEAMS_DUTY.md $S/refs/THREAD_MEMORY.md $S/tools/portal_lookup.py .claude/skills/bbg-teams-assist/SKILL.md"
KEEP="$S/refs/census/ARTIFACT_CENSUS_MACRO.yaml $S/refs/census/ARTIFACT_CENSUS_MP.yaml $S/refs/census/ARTIFACT_CENSUS_NEWS.yaml
$S/refs/census/ARTIFACT_CENSUS_POD2.yaml"
n=0; gone=0; still=""
for f in $OLD; do n=$((n+1)); if git cat-file -e "HEAD:$f" 2>/dev/null; then still="$still $f"; else gone=$((gone+1)); fi; done
k=0; kept=0; lost=""
for f in $KEEP; do k=$((k+1)); if [ "$(git rev-parse -q --verify "HEAD:$f")" = "$(git rev-parse -q --verify "$OA_BASE:$f")" ]; then kept=$((kept+1)); else lost="$lost $f"; fi; done
ns=$(git diff --numstat "$OA_R2_BASE" HEAD -- "$C" | awk '{print $1" "$2}')
[ -z "$ns" ] && ns="0 0"
gr=no; git show "HEAD:$C" | grep -q 'guardrails_ref: opal_ai/opal/agent/refs/BLOOMBERG_GUARDRAILS.md' && gr=yes
PAT='0\.0\.3_BG_BBGTerminal/(refs/(BLOOMBERG_GUARDRAILS|BUCKET_ALLOWLIST|PORTAL_RETRIEVAL|RELAUNCH|REQUEST_CATALOG|TEAMS_DUTY|THREAD_MEMORY)|prompt\.md|tools/portal_lookup)|skills/bbg-teams-assist'
SCOPE=".claude/ .tools/ org/mcp/ infra/ integrations/ lib/ *.ps1"
hits=$(git grep -l -E "$PAT" HEAD -- .claude/ .tools/ org/mcp/ infra/ integrations/ lib/ '*.ps1' \
  ':!.tools/hooks/bg-concierge-gate.sh' ':!.tools/hooks/tests/test_bg_concierge_gate.sh' | sed 's/^HEAD://')
nh=$(printf '%s' "$hits" | grep -c . )
echo "moved paths absent at HEAD: $gone of $n; census files kept at HEAD: $kept of $k; catalog lines added/removed vs cut: $ns (guardrails_ref re-pointed=$gr); code/config files still referencing moved paths: $nh (scope: $SCOPE)"
[ -n "$still" ] && echo "still present:$still"
[ -n "$lost" ] && echo "census not byte-equal to the cut:$lost"
[ "$nh" != 0 ] && printf '%s\n' "$hits" | sed 's/^/  ref: /'
if [ "$gone" = "$n" ] && [ "$kept" = "$k" ] && [ "$ns" = "1 1" ] && [ "$gr" = yes ] && [ "$nh" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
