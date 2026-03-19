#!/usr/bin/env bash
# P4 Books Tab Alignment Thread — ADVI_MVPLVL
#
# Pattern 0 (DS + DE + RD, 3-party round robin). DS audits gold table data
# availability (4a), drives Mix/Concentration design (4e/4f). DE owns
# publisher endpoint wiring for time series (4g). RD needs data shapes for
# all Books Tab enhancements.
#
# Run from repo root: bash org/threads/staging/run-ADVI_MVPLVL-004-p4-books-alignment.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

PROJECT="ADVI_MVPLVL"
THREAD_ID=""
TOPIC="P4 Books Tab alignment"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.2"

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "ClientsTab.tsx — Books Tab (4-level drill: N1/L2/L3/L4)",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx"
    },
    {
      "label": "AdvisorIntelligence types — BookResponse types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "bd-portal-publisher Lambda — builds clients_tab.json, advisor book endpoints",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "03_build_holdings_lots.py — lot-level holdings with cost basis and market value",
      "path": "data/black_diamond/scripts/gold/03_build_holdings_lots.py"
    },
    {
      "label": "05_build_client_performance.py — relationship-level daily AUA/NNA",
      "path": "data/black_diamond/scripts/gold/05_build_client_performance.py"
    },
    {
      "label": "05b_build_account_performance.py — account-level daily AUA/NNA",
      "path": "data/black_diamond/scripts/gold/05b_build_account_performance.py"
    },
    {
      "label": "06_build_client_tax_liability.py — tax liability view",
      "path": "data/black_diamond/scripts/gold/06_build_client_tax_liability.py"
    },
    {
      "label": "ETF classification — canonical asset class mapping for Mix/Concentration",
      "path": "infra/aws/lambda/v2_portal/_shared/etf_classification.py"
    },
    {
      "label": "00_build_accounts_dimension.py — account metadata including tax_status",
      "path": "data/black_diamond/scripts/gold/00_build_accounts_dimension.py"
    }
  ],
  "documents": [
    {
      "label": "ADVI_MVPLVL PRD — Part 4 (Books Tab) is the scope",
      "path": "docs/architecture/ADVI_MVPLVL_PRD.md"
    }
  ],
  "inline": "Goal: Align DS, DE, and RD on the 8 Books Tab items (4a-4h) before task orders. This is the heaviest phase — 4a (gold table data audit) gates all downstream views. DS must determine what data exists at each drill level (firm/advisor/relationship/account) and what gaps require new builders. DE owns endpoint wiring for AUA/NNA time series at L3/L4 (4g). RD needs confirmed data shapes and endpoint contracts for Mix (4e), Concentration (4f), and time series (4g) views. DS must use tool access to read gold scripts, publisher Lambda, and ETF classification to resolve data questions. Deliverable: agreed data contract for each Books Tab view — what exists, what needs building, and what shapes RD will consume."
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

## P4 Books Tab — Alignment

I am DS for Pod 4. This thread covers the 8 Books Tab items from ADVI_MVPLVL PRD Part 4. The Books Tab is the deepest section — most items require understanding what gold layer data exists at each drill level before views can be designed.

### 4a. Gold Table Data Audit — RESEARCH (DS-owned, gates everything)

The PRD lists 6 gold scripts that produce data the Books Tab could consume. I need to determine for each:
- What grain level the data is at (firm/advisor/relationship/account)
- Whether the publisher already surfaces it via an endpoint
- What additional aggregations are needed for Mix, Concentration, and time series

I will read the publisher Lambda and gold scripts to answer these questions during this thread.

### 4b. Drill Hierarchy — ACTION (existing, needs enhancement)

The 4-level drill already exists in \`ClientsTab.tsx\`:
- N1 (Global): aggregate KPIs + advisor summary
- L2 (Advisor Book): advisor AUA, clients, accounts, tax
- L3 (Relationship): client AUA, accounts table, tax intelligence
- L4 (Account): inline expansion with account-scoped lots

### 4c/4d. Tax Status + Tax Liability — ACTION (already functional)

Both exist at L2/L3/L4. Minor refinements will come from Mix/Concentration work.

### 4e. Mix (Asset Class Breakdown) — RESEARCH + ACTION

Requires mapping each position to an asset class. The ETF Classification system (\`etf_classification.py\`) covers ~160 ETFs. Key questions:
- Does the publisher already expose \`portfolio_composition\` at L2?
- What coverage does ETF classification achieve against actual holdings?
- Should Mix be computed backend (publisher/gold script) or frontend (from lots data)?

### 4f. Concentration (Security-Level Breakdown) — RESEARCH + ACTION

Linked to Mix — when user clicks an asset class in Mix, Concentration filters to show securities in that class. Data comes from holdings lots or positions cube.

### 4g. AUA/NNA Time Series at L3/L4 — ACTION (data exists)

\`client_performance.parquet\` (relationship) and \`account_performance.parquet\` (account) have daily AUA/NNA. These need to be surfaced via publisher endpoints and rendered with existing chart components. DE: what is the endpoint plan for serving relationship/account-level time series?

### 4h. Advisor Listing UI Consistency — ACTION (blocked on 3d)

The N1 advisor summary table should match the leaderboard design from 3d.

### Questions for DE and RD:

1. **DE:** For 4g, does the publisher already have \`getAdvisorBook\` or \`getBooksClientDetail\` endpoints? If so, do they currently include time series data, or would we need new fields?
2. **RD:** For 4e/4f, do you envision Mix and Concentration as separate panels side-by-side, or as a stacked layout with Mix on top and Concentration below?
3. **RD:** For 4g time series at L3/L4, do you want the same chart components as the Header panel (PartnerAnalytics), or a more compact inline chart?

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
