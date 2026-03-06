#!/usr/bin/env bash
# run-ADVI_49FNV3-002-books-tab-design.sh
#
# Pattern 0: N1/N2 -- Books tab design brief (firm admin dashboard + advisor drilldown)
# CRITICAL: DE must write docs/architecture/advisor_intelligence/books_tab_design_brief.md
# on their final turn. If the file does not exist after the thread, the thread failed.
# Participants: DS -> RD -> DE (round_robin, gpt-5.2, tools ON)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_49FNV3"
THREAD_ID=""              # auto-assigned (ADVI_49FNV3-002)
TOPIC="Pattern 0: Books tab design brief N1 N2"
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
      "label": "49FNV3 PRD (Section 4: New Features -- Books Tab N1/N2)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md"
    }
  ],
  "inline": "This is the Books tab design alignment for ADVI_49FNV3. Focus on N1 (Firm Admin Dashboard) and N2 (Advisor Book View). The PRD confirms Phase 1 panel data exists today: clients_tab.json has tax breakdown, architect_leaderboard.json has AUA by advisor, clients_tab.json has account/client distributions and engagement. DS must verify this by reading the advisor-publisher Lambda. Per-advisor JSONs have tax, engagement, clients arrays per data_contract.xml. DE must write the design brief as their final turn -- this is a hard deliverable requirement, not optional. Anchor every answer to a specific function name, dict key, S3 path, or JSON field. Do not claim data exists without citing the source file and key."
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

## Pattern 0 Alignment -- N1/N2: Books Tab Design Brief

I am the COO convening this alignment thread for ADVI_49FNV3. The Books tab requires two layers: N1 (Firm Admin Dashboard -- top-down view of the entire book of business using existing data) and N2 (Advisor Book View -- drilldown to a selected advisor's relationships). Before DE wires an endpoint or RD builds a component, DS must surface what data currently flows from the advisor-publisher Lambda and confirm which N1/N2 fields are already available today vs which require publisher changes.

**DE has a hard deliverable on the final turn.** DE MUST write the file:
  docs/architecture/advisor_intelligence/books_tab_design_brief.md

If this file does not exist after the thread completes, the thread has failed.

**Turn order:** DS -> RD -> DE. Three turns per agent.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read the advisor-publisher lambda_function.py and data_contract.xml from context before answering. For N1 and N2, verify each data source by citing the specific dict key or S3 path in the publisher output.

**N1: Firm Admin Dashboard (Phase 1 panels -- data expected to exist today):**

1. Tax Status Breakdown: The PRD says clients_tab.json has a `tax` object with taxable/deferred/exempt breakdown. Confirm: read the publisher and name the exact output dict key. What are the fields (amounts, percentages, AUA)?

2. AUA by Advisor (top N): architect_leaderboard.json has AUA per advisor. Confirm: name the S3 key pattern and the specific field for AUA. Is it sorted? How many advisors are included?

3. Account and Client Distributions: clients_tab.json has total accounts, total clients (relationships), median AUA. Confirm: name the exact fields.

4. Engagement Summary: clients_tab.json has net flows TTM, average relationship tenure, active clients percentage. Confirm: name the exact fields.

**N2: Advisor Book View (data from per-advisor JSONs):**

5. Per-advisor JSONs have tax, engagement, clients arrays per the data contract. Confirm: name the S3 key pattern for per-advisor JSONs (e.g. advisors/{advisorKey}.json). What fields does a single advisor JSON contain? Show the top-level keys.

6. For each field the PRD says N2 needs (tax breakdown, client list with AUA, NNA, engagement): is it currently present in the per-advisor JSON output? If not, name it as a publisher gap.

**IMPORTANT (M2):** Every field you confirm must be cited to a specific dict key in the Lambda output or a specific variable name in the Lambda code. Do not say a field exists without reading the publisher to verify.

**RD (0.4.2_RD_AdvisorIntelligence) -- after DS:**

Propose visual layout for N1 and N2. For each panel the PRD specifies:
- What existing portal components (Panel, PanelContent, DataTable, donut chart from ClientsTab) can be reused?
- What new component structure is needed?
- Which DS-confirmed field goes in which visual element?
- Do NOT propose rendering a field DS did not confirm exists.

For N1, propose the dashboard grid layout: how are the four Phase 1 panels arranged?
For N2, propose how the advisor drilldown overlays or replaces the firm dashboard when an advisor is selected.

**DE (0.4.0_DE_ClientPlatform) -- final turn (CRITICAL DELIVERABLE):**

Review DS's confirmation of available fields and RD's layout proposal. Then WRITE the design brief to:
  docs/architecture/advisor_intelligence/books_tab_design_brief.md

The brief must cover:
1. N1 Firm Admin Dashboard: panel layout, data field mappings (DS-confirmed fields only), component reuse map
2. N2 Advisor Book View: drilldown interaction model, data field mappings, component reuse map
3. Publisher gaps: explicit list of fields DS could NOT confirm (what must be added before RD can implement them)
4. TypeScript interface additions needed for N1 and N2
5. A note on N3 (Relationship Detail): is the data available for Phase 2a? What would need to be added to the publisher?

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
