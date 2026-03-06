#!/usr/bin/env bash
# run-ADVI_49FNV3-001-stacked-bar-data-contract.sh
#
# Pattern 0: F4 -- Top Ten Advisors stacked bar data contract
# Key question: are inflows/outflows tracked separately per advisor in source data,
# or only net NNA? Stacked bar requires them as distinct values.
# Participants: DS -> DE -> RD (round_robin, gpt-5.2, tools ON)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_49FNV3"
THREAD_ID=""              # auto-assigned (ADVI_49FNV3-001)
TOPIC="Pattern 0: stacked bar advisor inflow outflow"
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
      "label": "49FNV3 PRD (Section F4: Top Ten Advisors Stacked Bar)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md"
    }
  ],
  "inline": "DS must read script 10 before answering. The critical question for F4 is whether inflows and outflows are tracked as SEPARATE fields per advisor in the source parquet data, or whether only net NNA is available. The stacked bar (F4) requires: blue inflow bar (above zero), red outflow bar (below zero), and a gold horizontal dash showing NNA level. If inflows/outflows are not separate in source data, DS must flag this as a data gap and propose how to derive them from transaction data. M2: push back on any answer that does not cite the specific parquet column or script line that produces inflows vs outflows per advisor."
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

## Pattern 0 Alignment -- F4: Top Ten Advisors Stacked Bar

I am the COO convening this alignment thread for ADVI_49FNV3 (49Financial V3). The F4 fix requires redesigning the Top Ten Advisors panel in AdvisorsTab: replacing the current view with a stacked bar showing blue inflow bars (above zero), red outflow bars (below zero), and a gold horizontal dash showing the net NNA level for each advisor. This is analogous to the NNA bar in the main header panel and the triangle markers in ModelPortfolios Peer Performance.

DS, DE, and RD must agree on the data shape before any code is written.

**Turn order:** DS -> DE -> RD. Three turns per agent.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read script 10 (10_generate_advisor_rolling_flows.py in context) and data_contract.xml before answering. Name specific variable and column names from the file, not from memory.

1. What does script 10 currently compute per advisor? Name the specific parquet input columns. Does the source data track INFLOWS and OUTFLOWS as separate values per advisor per period, or only net NNA? Name the exact column names in the parquet source.

2. For the F4 stacked bar: can you produce, for each of the top N advisors, an inflow total and outflow total for the selected period (the current window or a fixed look-back)? If inflows/outflows are not separate in source data, flag this as a data gap and propose whether they can be derived from transaction-level data (e.g. summing positive vs negative NNA events per advisor).

3. What is the current output key in advisor_rolling_flows.json for the stacked bar data (Y13 per data_contract.xml)? Show the current shape so DE and RD know what exists vs what is new.

4. What is the sorting key for the top N selection? The PRD says sorted by NNA descending (or total AUA -- confirm with Andrew). Which field do you recommend as the sort key?

**DE (0.4.0_DE_ClientPlatform):** Read types.ts and AdvisorsTab.tsx before responding. Specify:
- TypeScript interface for a single advisor's stacked bar entry (inflow, outflow, nna_net, advisor_name, sort_key)
- How outflows should be encoded in the data (negative number? absolute value with sign flag?)
- What query key or data key maps to this stacked bar in the API response
- How the existing leaderboard data (architect_leaderboard.json) relates to or can be combined with advisor_rolling_flows.json

**RD (0.4.2_RD_AdvisorIntelligence):** Read AdvisorsTab.tsx before responding. Specify:
- How negative outflows should be rendered (bar below zero line, or absolute value with downward orientation?)
- Tooltip fields required: what numbers should appear on hover for each advisor bar
- How the gold NNA dash should be positioned (overlay on bar? separate reference line?)
- Any constraint from the charting library (Recharts/Nivo) on mixed positive/negative bars

**IMPORTANT (M2):** If any answer references a parquet column, S3 key, or interface field without citing a specific file in the repo, ask for the exact path or column name before accepting it as ground truth.

**Final turn must produce a structured contract block with:**
- advisor_rolling_flows.json stacked_bar entry shape (exact fields for a single advisor)
- How outflows are encoded (sign convention or separate field)
- Top N selection: how many advisors, what sort key
- TypeScript interface name DE will define
- Any data feasibility caveat (especially if inflows/outflows must be derived)
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
