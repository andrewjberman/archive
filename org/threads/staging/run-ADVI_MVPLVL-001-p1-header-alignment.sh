#!/usr/bin/env bash
# P1 Header Alignment Thread — ADVI_MVPLVL
#
# Pattern 0 (DS + RD, 2-party). DS investigates Mix data lineage, NNA Oct
# anomaly, GRO formula. RD confirms rendering requirements and data shape
# expectations for GRO summary container and any Mix fixes.
#
# Run from repo root: bash org/threads/staging/run-ADVI_MVPLVL-001-p1-header-alignment.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_MVPLVL"
THREAD_ID=""
TOPIC="P1 Header Assets Overview alignment"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context -- M1 compliance: actual source files for knowledge-bearing agents
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "PartnerAnalytics.tsx — Assets Overview panel (AUA/NNA/GRO charts, Mix sub-mode, summary container, time window state)",
      "path": "portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx"
    },
    {
      "label": "AdvisorIntelligence types — AuaMixView, GrowthDecompositionView, NNA types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "bd-portal-publisher Lambda — builds timeseries_chart.json including aua_mix, growth_decomposition, nna",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "05_build_client_performance.py — relationship-level AUA/NNA daily time series",
      "path": "data/black_diamond/scripts/gold/05_build_client_performance.py"
    },
    {
      "label": "02_build_positions_cube.py — daily holdings per account (potential Mix data source)",
      "path": "data/black_diamond/scripts/gold/02_build_positions_cube.py"
    },
    {
      "label": "03_build_holdings_lots.py — lot-level holdings with cost basis (potential Mix data source)",
      "path": "data/black_diamond/scripts/gold/03_build_holdings_lots.py"
    }
  ],
  "documents": [
    {
      "label": "ADVI_MVPLVL PRD — Part 1 (Header) is the scope for this thread",
      "path": "docs/architecture/ADVI_MVPLVL_PRD.md"
    }
  ],
  "inline": "Goal: Align DS and RD on the 5 Header work items (1a-i, 1a-ii, 1b-i, 1c-i, 1c-ii) before task orders are written. DS is the knowledge source — they must investigate the publisher Lambda to trace Mix data lineage (1a-ii), inspect NNA data around Oct 2025 for sign anomaly (1b-i), and verify the GRO decomposition formula (1c-i). RD is the knowledge receiver — they need confirmed data shapes and field names before building the GRO summary container (1c-ii) and any Mix rendering fixes. Deliverable: a concrete data contract for each work item — what DS will produce/fix and what shape RD should expect. DS must use tool access to read actual data and resolve questions during the thread, not defer to post-thread investigation."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- DS goes first (knowledge source)
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$OPENING_FILE" << OPENING_EOF
---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: ${TS}
signal: continue
---

## P1 Header — Assets Overview Panel Alignment

I am DS for Pod 4 (ClientPlatform). This thread covers the 5 Header work items from the ADVI_MVPLVL PRD. My job is to investigate the data layer and provide RD with confirmed shapes and findings so task orders can be written with zero ambiguity.

The PRD (docs/architecture/ADVI_MVPLVL_PRD.md) Part 1 defines these items:

### Items I own (RESEARCH):

**1a-ii. AUA Mix sub-mode** — The Mix view shows wrong data (only 2 months, wrong AUA numbers). I need to:
- Trace how \`aua_mix\` is built in \`bd-portal-publisher/lambda_function.py\`
- Identify what gold layer data feeds it (positions cube? holdings lots? something else?)
- Determine why only Feb/Mar 2026 are showing
- Report the correct methodology and what the JSON shape should look like

**1b-i. NNA October 2025 stacking anomaly** — The outflow bar for Oct 2025 renders above zero (stacked with inflows). I need to:
- Inspect the raw \`timeseries_chart.json -> nna -> data\` for daily values around Sep-Nov 2025
- Determine if the \`outflow\` value for October is positive (data bug) or if the frontend differencing logic produces a sign error
- Report whether the fix is backend (publisher) or frontend (PartnerAnalytics.tsx)

**1c-i. GRO number audit** — Growth decomposition shows market + NNA = total AUA change. I need to:
- Trace \`growth_decomposition\` computation in the publisher Lambda
- Verify the formula: is market = total_aua_change - nna, or independently computed?
- Cross-check Feb 2026, Jun 2025, Feb 2023 against known market conditions
- Report whether the numbers are correct or need formula changes

### Items RD owns (ACTION, but depends on my findings):

**1a-i. AUA default window** — Change TimeWindow default from '3Y' to '1Y' (PartnerAnalytics.tsx:203). This is independent — RD can do it without waiting for me.

**1c-ii. GRO summary container** — RD needs to build the GRO summary section (currently excluded at line 1826). But they need confirmed data shapes from my 1c-i audit before building it. I need to tell RD: what fields are in growth_decomposition, are the numbers correct, and what should the summary display.

### What I need from RD:

For 1c-ii: What specific data fields does the summary container pattern expect? I see AUA and NNA summaries already exist — what is the exact shape RD needs from GRO data to build the matching container? (period-over-period deltas, absolute values, etc.)

For 1a-ii Mix: If I find the Mix data source is fundamentally broken, does RD have a fallback rendering pattern, or do we defer Mix entirely until the data pipeline is fixed?

## Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer. Acceptable blockers are things that do not exist yet or require a live data query outside the repo.
OPENING_EOF

# ---------------------------------------------------------------------------
# Scaffold and run
# ---------------------------------------------------------------------------

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

# Resolve the actual thread ID (auto-assigned if project was set)
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
