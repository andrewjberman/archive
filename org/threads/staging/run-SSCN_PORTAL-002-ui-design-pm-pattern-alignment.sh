#!/usr/bin/env bash
# run-SSCN_PORTAL-002-ui-design-pm-pattern-alignment.sh
#
# Pattern 0 (design): PortfolioManagement pattern alignment for SecurityScanner
# Goal: 0.3.1_RD_PortfolioManagement documents what is abstractable from PM;
#       0.3.4_RD_SecurityScanner maps those patterns to SSCN tab layout needs;
#       0.3.0_DE_TradingOperations arbitrates shared vs page-local and produces
#       an approved component reuse plan + DESIGN_SPEC skeleton.
#
# Rationale: The PM page is the most complete, production-quality page in the portal.
# SSCN should mirror its visual language (panels, tab nav, sortable tables, gradient
# coloring, factor ordering) rather than reinvent those patterns. Any component that
# can be extracted from PM and shared must be approved by DE before RD creates a
# page-local copy.
#
# Participants: 0.3.1_RD_PortfolioManagement -> 0.3.4_RD_SecurityScanner -> 0.3.0_DE_TradingOperations
# Deliverable: Approved component reuse list + SSCN DESIGN_SPEC.md skeleton authored by DE.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="SSCN_PORTAL"
TOPIC="Pattern 0 (design): SecurityScanner UI -- PortfolioManagement pattern alignment and component reuse plan"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.3.1_RD_PortfolioManagement,0.3.4_RD_SecurityScanner,0.3.0_DE_TradingOperations"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "PM main page -- tab layout, shared component imports, PageHeaderCleanBadge + TabNavigation usage pattern",
      "path": "portal/src/pages/PortfolioManagement/PortfolioManagement.tsx"
    },
    {
      "label": "PM colorUtils -- getGradientBackground (red/yellow/green gradient), getWhiteToGreenGradient. Primary candidate for SSCN quintile coloring on Universe Scanner tab.",
      "path": "portal/src/pages/PortfolioManagement/utils/colorUtils.ts"
    },
    {
      "label": "PM factorOrder -- CANONICAL_GROUP_ORDER (15 groups), canonicalGroupIndex(). Directly applicable to SSCN Factor Bank tab category ordering.",
      "path": "portal/src/pages/PortfolioManagement/utils/factorOrder.ts"
    },
    {
      "label": "PM AlphaTab -- factor table with 3-state sort (canonical / asc / desc), search filter, group display. Most directly analogous to SSCN Factor Bank tab.",
      "path": "portal/src/pages/PortfolioManagement/tabs/AlphaTab.tsx"
    }
  ],
  "documents": [
    {
      "label": "Security Scanner PRD -- full portal spec: 4 tabs, scoring algorithm, universes, ScannerHeaderPanel, requiresDev gate",
      "path": "docs/architecture/SECURITY_SCANNER_PRD.md"
    },
    {
      "label": "PM DESIGN_SPEC -- PortfolioManagement UI design spec: panel framework, tab layout, snapshot header, design token references. Use this as the visual template.",
      "path": "portal/src/pages/PortfolioManagement/DESIGN_SPEC.md"
    }
  ],
  "inline": "This is a Pattern 0 design-alignment thread for SSCN_PORTAL. The COO's directive is: SecurityScanner must mirror PortfolioManagement's visual language as closely as possible. PM is the most production-complete page in the portal. SSCN should reuse PM patterns rather than reinvent them.\n\nThe data architecture is already settled (SSCN_PORTAL-001):\n- Server-side precompute monthly: per-factor percentiles per universe\n- Client-side: composite score + rank (sum of pctls * weight / 100)\n- API: GET /api/scoped/security-scanner/factors, /universe/{universeId}/data, /universe/{universeId}/scanner\n- JSON row shape: { ticker, name, mktVal, sector, industryGroup, values: Record<FactorCode, number|null>, pctls: Record<FactorCode, number|null> }\n- 6 universes: sp500/r1000/r1000v/acwx/eafe/eafev\n- 284 scoring factor columns in source data\n\nThis thread resolves the DESIGN side:\n1. Which PM utilities/patterns can be imported directly by SSCN (zero copying)?\n2. Which PM patterns need abstraction to a shared location before SSCN uses them?\n3. What new SSCN-specific components are needed (no PM equivalent)?\n4. What does the SSCN DESIGN_SPEC.md skeleton look like?\n\nThe output is an approved component reuse plan that 0.3.4_RD_SecurityScanner can build against."
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

## Pattern 0 Design Alignment -- SecurityScanner UI

I am the COO convening this design-alignment thread. The SSCN data architecture is locked (SSCN_PORTAL-001). This thread resolves the implementation design: how SSCN's UI maps to PortfolioManagement's visual patterns.

**COO directive:** SSCN must mirror PM's visual language as closely as possible. We do not reinvent what PM already built. Any component that can be abstracted from PM to a shared location and reused by SSCN should be. Any component that cannot be abstracted should be copied with DE approval.

**Turn order:** 0.3.1_RD_PortfolioManagement → 0.3.4_RD_SecurityScanner → 0.3.0_DE_TradingOperations (round_robin, 3 turns)

---

**0.3.1_RD_PortfolioManagement -- your turn first.**

You are the pattern source. You built PM and know every component. Your job this thread:

**1. PM pattern audit (abstractability)**

For each of the following PM patterns, state whether it is: (A) already shared/importable directly, (B) page-local but abstractable to shared (candidate for extraction), or (C) too PM-specific to generalize.

Anchor every answer to the exact file path and component/function name:

- \`colorUtils.ts\` → \`getGradientBackground\` / \`getWhiteToGreenGradient\`
- \`factorOrder.ts\` → \`CANONICAL_GROUP_ORDER\` / \`canonicalGroupIndex()\`
- \`AlphaTab.tsx\` → 3-state sort logic (canonical/asc/desc)
- \`AlphaTab.tsx\` → factor search/filter UI pattern
- \`OptimizationSummaryHeader.tsx\` → sticky always-visible header panel pattern
- \`PortfolioManagement.tsx\` → \`PageHeaderCleanBadge\` + \`useTabNavigation\` + \`TabNavigation\` usage
- AG Grid (PortfolioGrid.tsx) → Is this the right table primitive for SSCN, or is a simpler HTML table/Tanstack Table a better fit for a 3000-row read-only dataset?

**2. Reuse prescription**

For each item in the list above, write one concrete recommendation:
- "SSCN can import from \`portal/src/pages/PortfolioManagement/utils/colorUtils.ts\` directly" (if PM-local but stable)
- OR "This should be extracted to \`portal/src/utils/colorUtils.ts\` before SSCN uses it" (if shared)
- OR "SSCN should write its own version" (if PM-specific)

**3. Identify the 2-3 most important PM patterns for SSCN's Universe Scanner tab**

Universe Scanner (Tab 4) is the primary interactive tab: weight inputs (must sum to 100%), 3000-row security table with quintile gradient coloring, composite score column, per-factor percentile columns, auto-sort by rank. Name the PM components that most directly map to this tab.

**IMPORTANT (M2):** Cite exact file paths and function/component names. Do not describe a pattern without naming its source.

---

**0.3.4_RD_SecurityScanner -- after 0.3.1:**

You are the design receiver. Your job:

**1. SSCN tab → PM pattern mapping**

For each of the 4 SSCN tabs, list the PM components/patterns you will reuse or adapt:
- Factor Bank tab (factor selection, IC display, add/remove toggle, category grouping)
- Universe Data tab (large sortable table, identity + raw factor columns)
- Factor Data tab (static reference table, same shape as PM's AlphaTab factor list)
- Universe Scanner tab (weight inputs, composite score, quintile coloring, auto-sort by rank)

**2. ScannerHeaderPanel design**

The PRD specifies an always-visible \`ScannerHeaderPanel\` above the tab content with: universe dropdown, selected factor chips, weight controls. Does PM have an equivalent (e.g., \`OptimizationSummaryHeader.tsx\`)? Propose the component structure and what PM components/patterns it borrows.

**3. DESIGN_SPEC.md skeleton (ASCII layout)**

Produce a draft ASCII layout for each of the 4 tabs. Use PM's DESIGN_SPEC.md layout boxes as your format template. Show exactly where reused PM components appear.

**4. New components (no PM equivalent)**

List any components you will need to write from scratch with no PM equivalent. Be minimal -- every "new" component not in PM should be justified.

---

**0.3.0_DE_TradingOperations -- final turn (CRITICAL):**

You are the arbiter. Your job:

**1. Abstraction decisions**

For each component 0.3.1 flagged as (B) "abstractable to shared":
- Approve or reject moving it to a shared location
- If approved: name the target path (e.g., \`portal/src/utils/colorUtils.ts\`)
- If rejected: explain why page-local is correct

**2. AG Grid vs alternative**

Rule on the table primitive for SSCN's 3000-row tabs. AG Grid is a heavy dependency. For a read-only, monthly-refreshed dataset, is a lighter table sufficient (Tanstack Table, virtualized HTML table)? State what SSCN must use and why.

**3. Approved component reuse plan (deliverable)**

Produce a structured list in this exact format:

\`\`\`
SSCN COMPONENT REUSE PLAN -- SSCN_PORTAL-002

IMPORT DIRECTLY (no changes):
  - portal/src/pages/PortfolioManagement/utils/colorUtils.ts (getGradientBackground)
  - ...

EXTRACT TO SHARED BEFORE USE (DE approves, DT task):
  - [source] portal/src/pages/PortfolioManagement/utils/... -> [target] portal/src/utils/...
  - ...

SSCN-LOCAL COPY (approved, no abstraction):
  - ...

NEW (no PM equivalent, justify):
  - ScannerHeaderPanel -- universe dropdown + factor chips + weight controls (no PM analog)
  - ...

TABLE PRIMITIVE: [AG Grid | Tanstack Table | other] -- reason

DESIGN_SPEC target: portal/src/pages/SecurityScanner/DESIGN_SPEC.md
  0.3.4_RD_SecurityScanner authors it using 0.3.4's ASCII layout from this thread as the base.
\`\`\`

This plan is what 0.3.4_RD_SecurityScanner builds against. Vague answers are not acceptable.
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
