#!/usr/bin/env bash
# run-2026-03-03-advisors-stacked-bar-alignment.sh
#
# Pattern 0 pre-implementation alignment — Stream A3
# Stream: Advisors tab stacked bar + 1Y rolling line (replaces 30d/90d/1Y window charts)
# Participants: DS (knowledge source) -> DE (interface spec) -> RD (layout constraints)
#
# Run from repo root: bash org/threads/staging/run-2026-03-03-advisors-stacked-bar-alignment.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

THREAD_ID="2026-03-03-advisors-stacked-bar-alignment"
TOPIC="Pattern 0 alignment: Advisors tab stacked bar (Stream A3)"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.3-codex"

# ---------------------------------------------------------------------------
# Context (M1: current script 10 + portal consumer + types)
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Script 10 — current advisor rolling flows generator",
      "path": "data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py"
    },
    {
      "label": "AdvisorsTab component (current consumer)",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx"
    },
    {
      "label": "AdvisorIntelligence TypeScript types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "Advisor Intelligence API endpoints",
      "path": "portal/src/api/endpoints/advisor-intelligence.ts"
    }
  ],
  "documents": [
    {
      "label": "AdvisorIntelligence Completion PRD — Section 4C (Rolling Flows New Model)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md"
    }
  ],
  "inline": "This is a Pattern 0 pre-implementation alignment thread for Stream A3 of the AdvisorIntelligence completion PRD.\n\nStream A3: The Advisors tab currently shows rolling NNA with 30d/90d/1Y window toggles as line charts. This is being replaced with two views:\n  (1) Stacked bar chart: one bar per advisor showing inflows, outflows, NNA net — sorted by NNA — for period aggregations (QTD/YTD/1Y/3Y/Max).\n  (2) 1-year rolling line chart: daily 1Y trailing NNA per advisor, x-axis window controlled by period toggle (3Y/Max supported).\n\nScript 10 currently produces trailing rolling NNA at 30d/90d/1Y windows. It needs to be updated or supplemented to produce period-anchored aggregations and extended rolling series.\n\nKnowledge source: 0.4.0_DS_ClientPlatform (what script 10 currently computes, what nna_aua_by_advisor.parquet contains, what period-anchored aggregations are feasible).\nInterface specifier: 0.4.0_DE_ClientPlatform (TypeScript shape needed for both views).\nLayout specifier: 0.4.2_RD_AdvisorIntelligence (chart implementation constraints — Recharts vs Nivo, how negative outflows should be encoded in the bar data, what fields the tooltip needs).\n\nDeliverable: agreed JSON output schema for advisor_rolling_flows.json replacement/additions, agreed TypeScript interface names, agreed encoding for negative outflow values in the bar chart data. The final turn must contain this as a structured contract."
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

## Pattern 0 Alignment — Stream A3: Advisors Tab Stacked Bar + Rolling 1Y

I am the COO convening this alignment thread before script 10 is modified.
The Advisors tab rolling flows visualization is being redesigned: replacing
30d/90d/1Y window line charts with a stacked bar (period aggregations) primary
view and a fixed-1Y rolling line secondary view. DS, DE, and RD must agree
on the data shape before DS writes any code.

**Turn order:** DS -> DE -> RD. Three turns.

**DS (0.4.0_DS_ClientPlatform) — your turn first. Answer:**

1. What does script 10 currently compute? Name the specific parquet input files
   (e.g., nna_aua_by_advisor.parquet) and what columns carry inflows, outflows, NNA.
   Does the current output separate inflows from outflows, or only net NNA?

2. For the stacked bar: can you compute period-anchored totals (QTD, YTD, 1Y, 3Y, Max)
   for inflows, outflows, and nna_net per architect AND per implementor?
   How are inflows vs outflows currently tracked in the source data?
   What field distinguishes an inflow transaction from an outflow?

3. For the rolling 1Y line: script 10 already has a 1Y rolling window. Can it be
   extended to produce daily points across a 3Y+ lookback period?
   What is the realistic date history available in the source data?

4. What is the current output file/S3 key for script 10? What is the current JSON shape?
   Show the top-level keys so DE and RD know what already exists vs what is new.

**DE and RD:** After DS describes what is possible:
- DE: specify the TypeScript interface shape needed for both views (bar data per period,
  rolling series per advisor). Name the query key and how the toggle maps to data fields.
- RD: specify how negative outflows should be encoded in the bar chart data
  (e.g., as a negative number, as a separate field, as an absolute with a sign flag).
  Name the charting library (Recharts/Nivo/other) and any constraint it imposes
  on the data format. What tooltip fields are required?

**IMPORTANT (M2):** If any answer references a parquet column, S3 key, or interface
field without citing a specific file in the repo, ask for the exact path or column name
before accepting it as ground truth.

**Final turn must include a structured contract:**
- advisor_rolling_flows.json top-level structure (full key list, not just new keys)
- stacked_bar entry shape (exact fields for a single advisor/period entry)
- rolling_1y series shape (per-advisor structure, date+value format)
- How outflows are encoded (sign convention or separate field)
- TypeScript interface names DE will define
- Any risk or limitation DS wants to flag (e.g., limited history for Max period)
OPENING_EOF

# ---------------------------------------------------------------------------
# Scaffold and run
# ---------------------------------------------------------------------------

echo "Scaffolding thread: ${THREAD_ID}"
"${THREADS_DIR}/create-thread.sh" \
  --id              "$THREAD_ID" \
  --topic           "$TOPIC" \
  --created-by      "$CREATED_BY" \
  --participants    "$PARTICIPANTS" \
  --context-file    "$CONTEXT_FILE" \
  --opening-message "$OPENING_FILE" \
  --max-turns       "$MAX_TURNS" \
  --turn-order      round_robin

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

echo ""
echo "Running orchestrator..."
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
