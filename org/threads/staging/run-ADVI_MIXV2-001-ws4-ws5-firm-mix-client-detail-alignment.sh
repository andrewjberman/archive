#!/usr/bin/env bash
# Pattern 0 thread: ADVI_MIXV2-001
# Participants: DS + DE + RD (3-party, round_robin)
# Scope: WS4 firm-level mix chart redesign + WS5 client detail page wiring
#
# Context trimmed to stay under rate limit:
#   Pre-loaded: task orders + types.ts + ClientDetailPage.tsx (small/essential)
#   Tool-read:  PartnerAnalytics.tsx, advisor-intelligence.ts, 06b, Lambda
#               (agents will grep/read these during the thread)
#
# Run from repo root: bash org/threads/staging/run-ADVI_MIXV2-001-ws4-ws5-firm-mix-client-detail-alignment.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

PROJECT="ADVI_MIXV2"
THREAD_ID=""
TOPIC="WS4+WS5 firm mix chart and client detail alignment"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Context -- small files only; large files read via tools during thread
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "AdvisorIntelligence types.ts -- existing type definitions",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "ClientDetailPage.tsx -- setTimeout stub to replace (WS5)",
      "path": "portal/src/pages/AdvisorIntelligence/ClientDetail/ClientDetailPage.tsx"
    }
  ],
  "documents": [
    {
      "label": "DS task order 002 -- 06b firm+advisor aggregation + Lambda endpoints (WS3+WS6 spec)",
      "path": "org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_MIXV2.002.gold-firm-advisor-aggregation-and-lambda.md"
    },
    {
      "label": "DE task order 005 -- frontend firm mix chart + client detail wiring (WS4+WS5 spec)",
      "path": "org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_MIXV2.005.frontend-firm-mix-and-client-detail.md"
    }
  ],
  "inline": "This is a 3-party Pattern 0 alignment thread for ADVI_MIXV2 WS4 and WS5. Task orders 002 (DS) and 005 (DE) are pre-loaded as the spec. Large source files are NOT pre-loaded -- use tool calls to read them during the thread. Key files to read: PartnerAnalytics.tsx at portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx (for getPeriodInfo, ASSET_CLASS_COLORS, firmMixData useMemo, chart container layout), advisor-intelligence.ts at portal/src/api/endpoints/advisor-intelligence.ts (for LAMBDA_FIRM_ID and existing API pattern), 06b at data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py (for DS to confirm period label derivation logic). ClientDetailPage.tsx is pre-loaded. DS is the knowledge source for gold output shape and Lambda endpoints. DE is the receiver who will type and wire. RD is the receiver who will implement the chart and panel layout. Deliverable: a binding contract containing confirmed period label format, confirmed granularity key names, confirmed asset class color map, confirmed clientKey == relationship_id resolution, and RD layout constraints for the dollar stacked bar and panel mounting."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message
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

## ADVI_MIXV2 WS4 + WS5: Pre-Implementation Alignment

Task orders 002 (DS) and 005 (DE) are in context. Large source files are NOT pre-loaded
-- read them with tools. Key files to read:
- \`portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx\` (DE + RD)
- \`portal/src/api/endpoints/advisor-intelligence.ts\` (DE)
- \`data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py\` (DS)

ClientDetailPage.tsx is pre-loaded (WS5 gate: clientKey type).

---

## DS Commits (WS4): What I will produce from 06b

**\`gold/firm_mix_views.json\`** S3 key: \`opal-data-bd/gold/firm_mix_views.json\`

Shape per task order 002:
\`\`\`json
{
  "generated_at": "ISO",
  "data_as_of": "YYYY-MM-DD",
  "firm_id": "49financial",
  "views": {
    "quarterly": [
      {
        "period": "2024-Q4",
        "label": "Q4 '24",
        "end_date": "2024-12-31",
        "total_aua": 1620000000.0,
        "equity":           {"value": 1004400000.0, "pct": 0.62},
        "fixed_income":     {"value":  388800000.0, "pct": 0.24},
        "structured_notes": {"value":   97200000.0, "pct": 0.06},
        "cash":             {"value":   81000000.0, "pct": 0.05},
        "other":            {"value":   48600000.0, "pct": 0.03}
      }
    ],
    "monthly": [...],
    "annually": [...]
  }
}
\`\`\`

**Period label format (open question for DE to resolve):**
I plan to produce \`"label": "Q4 '24"\` for quarterly and \`"label": "Oct '24"\` for monthly.
Read PartnerAnalytics.tsx and find \`getPeriodInfo()\` -- confirm the exact string format
it produces today. If my proposed labels do not match, I will adjust 06b to match.
Cite the exact line(s) from PartnerAnalytics.tsx.

**Granularity keys (open question for DE to resolve):**
My views object uses keys: \`quarterly\`, \`monthly\`, \`annually\`.
Read PartnerAnalytics.tsx and find how the granularity state maps to period key names
in the current firmMixData useMemo. Cite exact string literals used. I will use the
same keys.

**Asset class keys:** equity, fixed_income, structured_notes, cash, other (5 classes).
These match the existing per-relationship mix-timeseries shape.

---

## Questions for DE

1. **getPeriodInfo() labels**: Read PartnerAnalytics.tsx, find getPeriodInfo().
   What is the exact string format for quarterly (e.g., "Q4 '24") and monthly
   (e.g., "Oct '24") periods? Cite the line.

2. **ASSET_CLASS_COLORS**: Read PartnerAnalytics.tsx. Does it already define colors
   for all 5 keys: equity, fixed_income, structured_notes, cash, other?
   List the color values and confirm all 5 are covered.

3. **Granularity mapping**: In the current firmMixData useMemo or chart data source,
   what string values does the granularity state hold? Confirm they match:
   quarterly / monthly / annually.

4. **WS5 clientKey type**: Read ClientDetailPage.tsx (pre-loaded). Trace how
   clientKey is set when navigating from the Books tab. Is it a relationship_id?
   An account_id? Cite the relevant prop or route param.

5. **getFirmMixViews query key**: Confirm the React Query key pattern you will use.
   For consistency with the other queries in PartnerAnalytics.tsx, what should it be?

---

## Questions for RD

6. **Dollar stacked bar layout in PartnerAnalytics.tsx**: Read PartnerAnalytics.tsx.
   What is the current chart container element and dimensions for the mix bar chart
   (the one we are replacing)? Fixed height? Responsive? What className or style?

7. **MixTimeseriesPanel + ConcentrationPanel mount in ClientDetailPage**: Read
   ClientDetailPage.tsx (pre-loaded). Where should these panels be mounted?
   After which existing panel? In what grid structure? Any existing empty slots?

8. **Empty state component pattern**: What component does the portal use for empty
   states in panels (e.g., a dedicated EmptyState component, a centered text div)?
   Read one existing panel in ClientDetailPage and cite the pattern.

---

## Self-unblock requirement

Read files with tools to answer questions 1-8. Do not surface an unresolved question
in the final turn if the answer is in a file in this repo. If an answer references
a field, line, or component name -- cite the file path and line number.

If any answer references a data field or interface name without citing a specific file,
ask for the exact location before accepting it as ground truth.

---

## Convergence deliverable

Final turn must produce a receipt block with:
1. Confirmed period label format (exact strings DS will produce in 06b)
2. Confirmed granularity key names (views object top-level keys)
3. Confirmed ASSET_CLASS_COLORS coverage (all 5 or gap + proposed addition)
4. Confirmed clientKey type (relationship_id or mapping needed)
5. RD chart layout constraints (container, height, className)
6. RD panel mount position in ClientDetailPage
7. Agreed TypeScript interface names (FirmMixViewsResponse, FirmMixPeriodPoint, FirmMixClassValue)
8. Agreed React Query key for getFirmMixViews
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

echo "Scaffolding ADVI_MIXV2-001 Pattern 0 thread (trimmed context)..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

# Resolve thread ID
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
