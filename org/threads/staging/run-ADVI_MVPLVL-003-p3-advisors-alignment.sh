#!/usr/bin/env bash
# P3 Advisors Tab Alignment Thread — ADVI_MVPLVL
#
# Pattern 0 (DS + RD, 2-party). DS investigates portfolio_group + architect
# data quality (3a). RD needs data findings before implementing leaderboard
# redesign (3d) and hierarchy changes.
#
# Run from repo root: bash org/threads/staging/run-ADVI_MVPLVL-003-p3-advisors-alignment.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

PROJECT="ADVI_MVPLVL"
THREAD_ID=""
TOPIC="P3 Advisors Tab alignment"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.2"

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "AdvisorsTab.tsx — Top 3, stacked bar, rolling flows, leaderboard",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx"
    },
    {
      "label": "AdvisorIntelligence types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "00_build_accounts_dimension.py — contains portfolio_group, architect, implementor fields",
      "path": "data/black_diamond/scripts/gold/00_build_accounts_dimension.py"
    },
    {
      "label": "08_build_nna_aua_by_advisor.py — advisor-level time series builder",
      "path": "data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py"
    },
    {
      "label": "10_generate_advisor_rolling_flows.py — rolling flows + stacked bar data",
      "path": "data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py"
    },
    {
      "label": "bd-portal-publisher Lambda — builds advisor_leaderboard.json",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "SecurityScanner page (design reference for leaderboard visual polish)",
      "path": "portal/src/pages/SecurityScanner/SecurityScanner.tsx"
    },
    {
      "label": "FactorTilts page (design reference for rich data presentation)",
      "path": "portal/src/pages/FactorTilts/FactorTilts.tsx"
    }
  ],
  "documents": [
    {
      "label": "ADVI_MVPLVL PRD — Part 3 (Advisors Tab) is the scope",
      "path": "docs/architecture/ADVI_MVPLVL_PRD.md"
    }
  ],
  "inline": "Goal: Align DS and RD on the 4 Advisors Tab items (3a-3d) before task orders. DS is the knowledge source for 3a (portfolio_group + architect data quality investigation). DS must run diagnostic queries against accounts_dimension to determine: what distinct portfolio_group values exist, how many true architects vs noise entries, and propose a filtering/mapping strategy. RD needs these findings before designing the leaderboard (3d) and understanding what drill hierarchy the tab should support. DS must use tool access to read scripts and resolve data questions during the thread."
}
CONTEXT_EOF

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$OPENING_FILE" << OPENING_EOF
---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: ${TS}
signal: continue
---

## P3 Advisors Tab — Alignment

I am DS for Pod 4. This thread covers the 4 Advisors Tab items from ADVI_MVPLVL PRD Part 3. My primary research task is 3a (portfolio group + architect data quality), which gates RD's leaderboard redesign.

### 3a. Portfolio Group + Architect Data Quality — RESEARCH (DS-owned)

The PRD states 49 Financial has 53 architect entries but likely fewer than 15 true architects. I need to investigate:

1. **Portfolio group field analysis** — What distinct \`portfolio_group\` values exist in \`accounts_dimension_latest.parquet\`? Is it a proxy for regional offices? How many unique groups? I will read \`00_build_accounts_dimension.py\` to understand how this field is populated, then query the actual data.

2. **True architect identification** — Develop filtering logic to separate real architects from noise. Proposed heuristics:
   - Cross-reference with portfolio group consistency
   - Temporal activity (trailing 12M transactions)
   - AUA threshold (top N by managed AUA)
   - Account count threshold (multiple relationships, not just 1-2)

3. **Default tab hierarchy** — Once portfolio groups are understood, propose whether the Advisors Tab should support: Portfolio Group (default) -> Architect -> Implementor instead of the current binary toggle.

### 3b. Top 3 Panel Overwritten by Stacked Bar — ACTION (RD-owned)

The \`TopTenStackedBar\` is conditionally rendered in Panel 1 (where Top3Highlights should always be). When \`flowsData\` loads, Top 3 disappears. Fix: move \`TopTenStackedBar\` to Panel 2, keep Panel 1 as always-\`Top3Highlights\`.

### 3c. Stacked Bar NNA Sort Order — ACTION (RD-owned)

Bars display in inconsistent order. The sort in data prep looks correct (\`b.nna_net - a.nna_net\`), but Recharts may re-sort. RD needs to debug the rendering order.

### 3d. Leaderboard Visual Polish — ACTION (RD-owned)

Complete visual redesign of the leaderboard table. Design refs: SecurityScanner, FactorTilts, KI modal. Blocked on 3a findings — if we discover portfolio groups are meaningful, the leaderboard may need a grouping/hierarchy dimension.

### Questions for RD:

1. For 3d: if 3a reveals that portfolio groups are clean regional office labels, would you want the leaderboard to support a "group by portfolio group" view? Or keep it flat with a filter?
2. For 3b: is it a simple component swap (move TopTenStackedBar from Panel 1 conditional to Panel 2), or are there layout/sizing implications you foresee?
3. For 3c: have you observed the sort issue yourself? Is it consistent across all period selections or only certain ones?

## Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.
OPENING_EOF

CREATE_ARGS=(
  --topic           "$TOPIC"
  --created-by      "$CREATED_BY"
  --participants    "$PARTICIPANTS"
  --context-file    "$CONTEXT_FILE"
  --opening-message "$OPENING_FILE"
  --max-turns       "$MAX_TURNS"
  --turn-order      round_robin
)
[ -n "$PROJECT" ]   && CREATE_ARGS+=(--project "$PROJECT")
[ -n "$THREAD_ID" ] && CREATE_ARGS+=(--id "$THREAD_ID")

echo "Scaffolding thread..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

if [ -z "$THREAD_ID" ] && [ -n "$PROJECT" ]; then
  JQ="${REPO_ROOT}/.tools/jq.exe"
  PROJECT_FILE="${REPO_ROOT}/org/projects/${PROJECT}.json"
  COUNTER=$("$JQ" -r '.thread_counter' "$PROJECT_FILE")
  SERIAL="${PROJECT}-$(printf '%03d' $COUNTER)"
  TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-40 | sed 's/-$//')
  THREAD_ID="${SERIAL}-${TOPIC_SLUG}"
fi

echo ""
echo "Running orchestrator on: ${THREAD_ID}"
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
