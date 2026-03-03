#!/usr/bin/env bash
# run-ADVI-006-books-tab-design.sh
#
# Pattern 0: Books tab design brief (re-run of ADVI-003)
# Critical: DE must write docs/architecture/advisor_intelligence/books_tab_design_brief.md
# on their final turn. If the file does not exist after the thread, the thread failed.
# Participants: DS -> RD -> DE (round_robin, gpt-5.2, tools ON)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI"
THREAD_ID=""              # auto-assigned (ADVI-006)
TOPIC="Pattern 0: Books tab design brief L2 L3 L4"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.2_RD_AdvisorIntelligence,0.4.0_DE_ClientPlatform"
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
      "label": "BD advisor publisher Lambda",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py"
    },
    {
      "label": "ClientsTab component",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx"
    },
    {
      "label": "AdvisorIntelligence TypeScript types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "Script 03 -- holdings lots builder",
      "path": "data/black_diamond/scripts/gold/03_build_holdings_lots.py"
    },
    {
      "label": "Script 05b -- account performance builder",
      "path": "data/black_diamond/scripts/gold/05b_build_account_performance.py"
    },
    {
      "label": "Script 06 -- client tax liability builder",
      "path": "data/black_diamond/scripts/gold/06_build_client_tax_liability.py"
    },
    {
      "label": "DS data contract",
      "path": "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml"
    }
  ],
  "documents": [
    {
      "label": "AdvisorIntelligence Completion PRD (Section 5 Books Tab)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md"
    }
  ],
  "inline": "This is a Books tab design alignment. The previous run (ADVI-003) failed to produce its required deliverable: docs/architecture/advisor_intelligence/books_tab_design_brief.md. The DE must write this file as their final turn. It is not optional.\nDS: read lambda_function.py before describing what currently flows through the advisor-publisher. Anchor every answer to a function name and output dict key. Distinguish between what is currently in the published JSON vs what is gold-layer only. The gap list (what is missing from publisher output) is the core deliverable."
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

## Pattern 0 Alignment -- Books Tab Design Brief (L2/L3/L4)

I am the COO convening this alignment thread. The Books tab is the deepest, most data-intensive part of AdvisorIntelligence. Before DE wires an endpoint or RD builds a component, DS must surface what data currently flows from the advisor-publisher Lambda and what gold layer data (scripts 03, 05b, 06) is available but NOT yet published.

**This is a re-run.** The previous thread (ADVI-003) failed to produce its required deliverable: the Books design brief. This time, DE MUST write the file docs/architecture/advisor_intelligence/books_tab_design_brief.md on their final turn. If it does not exist after this thread completes, the thread has failed.

**Turn order:** DS -> RD -> DE. Three turns per agent. DE writes the design brief as their final deliverable.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read the advisor-publisher lambda_function.py, scripts 03/05b/06, and data_contract.xml from context. For each level, describe:

**L2 (Advisor Book -- aggregate of all advisor's relationships):**
- What fields currently appear in the advisor S3 output? Name the actual S3 key pattern and the specific dict keys in the publisher output.
- What summary metrics are currently published (AUA total, client count, NNA)?
- What is MISSING that the PRD requires: NMNC/NMEC breakdown, geography, account type, tax exposure, income/fees, portfolio composition? For each missing field, name the gold layer source file and the specific function or variable that produces it.

**L3 (Relationship/Client View):**
- What currently flows in clients/{clientKey}.json? Name the S3 key pattern. List the top-level dict keys currently present.
- What is missing: performance time series, full account list, client segment data?

**L4 (Account + Holdings + Tax):**
- Script 03: what output does it produce? What fields per lot? Does it currently flow into the publisher output, or is it gold-layer only? Name the specific function and output variable.
- Script 05b: what fields does it produce? Is it in the publisher output?
- Script 06: what output structure does it produce? Is it in the publisher output?
- What L4 fields are COMPLETELY ABSENT from the current publisher output?

**IMPORTANT (M2):** Anchor every answer to a specific function name, dict key, S3 path, or parquet column. If you say "this data is available," name where it currently lives (which file, which variable). Do not say a field exists without citing the source.

**RD (0.4.2_RD_AdvisorIntelligence) -- after DS:**
Propose visual layout for L2, L3, L4. For each level: what sections exist on the page, what data field from DS's description goes in each section, what existing portal components (Panel/PanelContent/DataTable/etc.) can be reused. Do NOT propose fields that DS did not confirm exist.

**DE (0.4.0_DE_ClientPlatform) -- final turn (CRITICAL):**
Review DS's gap list and RD's layout. Then WRITE the design brief to:
  docs/architecture/advisor_intelligence/books_tab_design_brief.md

The brief must cover:
1. L2 advisor book layout with data field mappings (DS confirmed fields only)
2. L3 relationship view layout
3. L4 account + holdings view with tax summary and lot drill-down
4. Component reuse opportunities
5. DS data gaps: explicit list of what must be added to the publisher before RD can implement
6. TypeScript interface additions needed (new types or extensions to existing types)
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
