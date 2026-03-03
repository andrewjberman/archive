#!/usr/bin/env bash
# run-ADVI-005-stacked-bar-rolling-flows.sh
#
# Pattern 0: Advisors tab stacked bar + 1Y rolling (re-run of ADVI-002)
# Key question: are inflows/outflows tracked separately in source data or only net NNA?
# Participants: DS -> DE -> RD (round_robin, gpt-5.2, tools ON)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI"
THREAD_ID=""              # auto-assigned (ADVI-005)
TOPIC="Pattern 0: stacked bar + rolling flows data contract"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context (M1 + M4)
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Script 10 -- advisor rolling flows generator",
      "path": "data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py"
    },
    {
      "label": "AdvisorsTab component",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx"
    },
    {
      "label": "AdvisorIntelligence TypeScript types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "DS data contract",
      "path": "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml"
    }
  ],
  "documents": [
    {
      "label": "AdvisorIntelligence Completion PRD (Section 4C Rolling Flows)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md"
    }
  ],
  "inline": "DS must read script 10 before answering. The critical open question is whether inflows and outflows are tracked as SEPARATE fields in the source parquet data, or whether only net NNA is available and inflows/outflows must be derived. The stacked bar chart requires inflows and outflows as distinct values per advisor per period. If only net NNA exists, DS must flag this as a data gap and propose a derivation approach -- do not silently agree to produce a field that does not exist in source data. M2: push back on any answer that does not cite the specific parquet column or script line that produces inflows vs outflows."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$OPENING_FILE" << OPENING_EOF
---
agent: ${CREATED_BY}
turn: 0
timestamp: ${TS}
signal: continue
---

## Pattern 0 Alignment -- Advisors Tab Stacked Bar + Rolling 1Y

I am the COO convening this alignment thread. The Advisors tab rolling flows visualization is being redesigned: replacing 30d/90d/1Y window line charts with a stacked bar (period aggregations) primary view and a fixed-1Y rolling line secondary view. DS, DE, and RD must agree on the data shape before any code is modified.

**Turn order:** DS -> DE -> RD. Three turns per agent.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read script 10 (10_generate_advisor_rolling_flows.py in context) and data_contract.xml before answering. Name specific variable and column names from the file, not from memory.

1. What does script 10 currently compute? Name the specific parquet input files and their columns. Does the source data have inflows and outflows as SEPARATE columns, or only net NNA? Name the exact column names.

2. For the stacked bar: can you compute period-anchored totals (QTD, YTD, 1Y, 3Y, Max) for inflows, outflows, and nna_net per architect AND per implementor? If inflows and outflows are not separate in the source data, flag this as a data gap and propose how to derive them.

3. For the rolling 1Y line: script 10 already has rolling windows. Can it produce daily points across a 3Y+ lookback? What date range does the source data actually cover?

4. What is the current output file and its S3 key? Show the current top-level JSON keys so DE and RD know what already exists vs what is new.

**DE (0.4.0_DE_ClientPlatform):** Read types.ts and AdvisorsTab.tsx before responding. Specify:
- TypeScript interface for the stacked bar data per period
- TypeScript interface for the rolling 1Y series
- How the period toggle maps to data keys
- Outflow encoding requirement from a portal typing perspective

**RD (0.4.2_RD_AdvisorIntelligence):** Read AdvisorsTab.tsx before responding. Specify:
- How negative outflows should be encoded in the data (negative number? separate field? absolute with sign flag?)
- Which charting library (Recharts/Nivo/other) and any constraint it imposes on the data format
- What tooltip fields are required for both views

**IMPORTANT (M2):** If any answer references a parquet column, S3 key, or interface field without citing a specific file in the repo, ask for the exact path or column name before accepting it as ground truth.

**Final turn must produce a structured contract block with:**
- advisor_rolling_flows.json top-level structure (full key list, not just new keys)
- stacked_bar entry shape (exact fields for a single advisor per period)
- rolling_1y series shape (per-advisor structure, date+value format)
- How outflows are encoded (sign convention or separate field)
- TypeScript interface names DE will define
- Period key names (exactly: qtd/ytd/1y/3y/max or confirmed equivalents)
- Any data feasibility caveat (especially if inflows/outflows are derived, not native)
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
  --project         "$PROJECT"
)

echo "Scaffolding thread..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

# Resolve the actual thread ID
JQ="${REPO_ROOT}/.tools/jq.exe"
PROJECT_FILE="${REPO_ROOT}/org/projects/${PROJECT}.json"
COUNTER=$("$JQ" -r '.thread_counter' "$PROJECT_FILE")
SERIAL="${PROJECT}-$(printf '%03d' $COUNTER)"
TOPIC_SLUG=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-40 | sed 's/-$//')
THREAD_ID="${SERIAL}-${TOPIC_SLUG}"

echo ""
echo "Running orchestrator on: ${THREAD_ID}"
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
