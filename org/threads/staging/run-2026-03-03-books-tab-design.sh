#!/usr/bin/env bash
# run-2026-03-03-books-tab-design.sh
#
# Pattern 0 pre-implementation alignment — Stream D (Books tab)
# L2 (advisor book) / L3 (relationship) / L4 (account + holdings + tax) design brief
# Participants: DS (knowledge source) -> RD (layout proposals) -> DE (wiring + component gaps)
#
# Run from repo root: bash org/threads/staging/run-2026-03-03-books-tab-design.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

THREAD_ID="2026-03-03-books-tab-design"
TOPIC="Pattern 0 alignment: Books tab L2/L3/L4 design brief"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.2_RD_AdvisorIntelligence,0.4.0_DE_ClientPlatform"
MAX_TURNS=3
MODEL="gpt-5.3-codex"

# ---------------------------------------------------------------------------
# Context (M1: advisor publisher + gold scripts + current portal consumer files)
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "BD advisor publisher Lambda (current S3 output producer)",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py"
    },
    {
      "label": "Script 03 — holdings lots builder (L4 source)",
      "path": "data/black_diamond/scripts/gold/03_build_holdings_lots.py"
    },
    {
      "label": "Script 05b — account performance builder (L4 source)",
      "path": "data/black_diamond/scripts/gold/05b_build_account_performance.py"
    },
    {
      "label": "Script 06 — client tax liability builder (L4 source)",
      "path": "data/black_diamond/scripts/gold/06_build_client_tax_liability.py"
    },
    {
      "label": "ClientsTab component (current L2/L3 entry point)",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx"
    },
    {
      "label": "ClientDetailPage (current L3/L4 entry point)",
      "path": "portal/src/pages/AdvisorIntelligence/ClientDetail/ClientDetailPage.tsx"
    },
    {
      "label": "ClientDetail types (current portal types for detail view)",
      "path": "portal/src/pages/AdvisorIntelligence/ClientDetail/types.ts"
    },
    {
      "label": "AdvisorIntelligence TypeScript types (main page types)",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    }
  ],
  "documents": [
    {
      "label": "AdvisorIntelligence Completion PRD — Section 5 (Books Tab)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md"
    }
  ],
  "inline": "This is a Pattern 0 pre-implementation alignment thread for the Books tab (Stream D) of the AdvisorIntelligence completion PRD.\n\nThe Books tab has four levels:\n  L2: Advisor book (all of this advisor's relationships — default landing for non-admin users)\n  L3: Relationship/client view (one client's full detail)\n  L4: Account + holdings + lots + performance + tax (deepest view, with lot-level drill-down)\n\nKnowledge source: 0.4.0_DS_ClientPlatform — describes WHAT data currently flows out of the advisor-publisher Lambda and what L4 data exists in the gold layer (scripts 03, 05b, 06) but is NOT yet published. DS must surface the gap between what is available in gold vs what is currently in the S3 publisher output.\n\nLayout proposer: 0.4.2_RD_AdvisorIntelligence — proposes the visual layout for each level (L2/L3/L4), identifies component reuse opportunities, flags any layout constraint that affects what fields DS needs to add to the publisher.\n\nWiring specifier: 0.4.0_DE_ClientPlatform — reviews DS's gap list and RD's layout, identifies TypeScript interface additions needed, confirms component reuse opportunities, and flags any API endpoint changes required.\n\nDeliverable: a markdown design brief at docs/architecture/advisor_intelligence/books_tab_design_brief.md covering:\n  1. L2 advisor book layout (sections with data field mappings)\n  2. L3 relationship view layout\n  3. L4 account + holdings view with tax summary and lot drill-down\n  4. Component reuse opportunities\n  5. Publisher data gaps DS must close before RD implements\nThe final agent turn (DE) must write the design brief path and a structured summary of what changed in the agreed contract."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message (COO sets agenda, DS goes first as knowledge source)
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

## Pattern 0 Alignment — Books Tab Design Brief (L2/L3/L4)

I am the COO convening this alignment thread before any Books tab implementation begins.
The Books tab is the deepest, most data-intensive part of AdvisorIntelligence.
Before DE wires an endpoint or RD builds a component, DS must surface what data
currently flows out of the advisor-publisher Lambda and what gold layer data
(scripts 03, 05b, 06) is available but not yet published. RD proposes layout
per level. DE identifies wiring gaps. We emerge with a precise design brief.

**Turn order:** DS -> RD -> DE. Three turns. DE writes the final design brief.

**DS (0.4.0_DS_ClientPlatform) — your turn first. For each level, describe:**

**L2 (Advisor Book — aggregate of all advisor's relationships):**
- What fields currently appear in the advisor S3 output (clients_tab.json or book.json)?
  Name the actual S3 key pattern for this file.
- What summary metrics are currently published (AUA total, client count, NNA)?
- What is MISSING that the PRD requires: AUA composition (NMNC/NMEC breakdown),
  geography, account type, tax exposure summary, income/fees, portfolio composition?
  For each missing field, name the gold layer source (which script or parquet file).

**L3 (Relationship/Client View):**
- What currently flows in clients/{clientKey}.json?
  Name the S3 key pattern. List the top-level fields currently present.
- What is missing for L3: performance time series for the relationship's total AUA,
  full account list, deeper client segment data?

**L4 (Account + Holdings + Tax):**
- Script 03 (holdings_lots): what output does it produce? What fields per lot?
  Does it currently flow into the publisher Lambda output, or is it gold-layer only?
- Script 05b (account_performance): what fields does it produce?
  Is account-level AUA, returns, and account type currently in the publisher output?
- Script 06 (tax_liability): what output structure does it produce?
  Is it currently in the publisher output? What fields for the tax summary view?
- What L4 fields are COMPLETELY ABSENT from the current publisher output?

**IMPORTANT (M2):** Anchor every answer to a specific file, S3 key, or parquet column.
If a field is in the gold layer but not in the publisher output, name both:
the gold source script AND the missing publisher field. Do not say "this data is available"
without naming where it currently lives.

**RD (0.4.2_RD_AdvisorIntelligence) — after DS:** Propose visual layout for L2, L3, L4.
For each level: what sections exist on the page, what data field goes in each section,
what existing portal components can be reused (check the Panel/PanelContent/DataTable
primitives). Flag any layout constraint that changes what DS needs to publish.

**DE (0.4.0_DE_ClientPlatform) — final turn:** Review DS's gap list and RD's layout.
Identify TypeScript interface additions needed (new fields in ClientDetailPageData or
equivalent). Confirm component reuse. Flag any API endpoint changes (new endpoint,
new query key, new response field). Finalize and write the design brief to:
  docs/architecture/advisor_intelligence/books_tab_design_brief.md
The brief must list DS data gaps explicitly — this is what blocks RD from implementing.
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
