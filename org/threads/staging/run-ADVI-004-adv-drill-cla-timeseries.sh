#!/usr/bin/env bash
# run-ADVI-004-adv-drill-cla-timeseries.sh
#
# Pattern 0: adv_drill + cla_timeseries alignment (re-run of ADVI-001)
# Fixes from ADVI-001: missing geo_drill in cla, placeholder colorMap, unverified NMNC/NMEC logic
# Participants: DS -> DE -> RD (round_robin, gpt-5.2, tools ON)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI"
THREAD_ID=""              # auto-assigned from project serial (ADVI-004)
TOPIC="Pattern 0: adv_drill + cla_timeseries data contract"
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
      "label": "BD portal publisher Lambda",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "AdvisorIntelligence TypeScript types",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "DistributionTab component",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx"
    },
    {
      "label": "DS data contract",
      "path": "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml"
    }
  ],
  "documents": [
    {
      "label": "AdvisorIntelligence Completion PRD (Section 3 Distribution Tab)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md"
    }
  ],
  "inline": "This is a re-run of a previous alignment thread that produced low-quality contracts. Three specific gaps must be resolved this time:\n(1) cla_timeseries must include geo_drill (city-level drill within each state) -- it was missing from ADVI-001 despite being required by the PRD.\n(2) colorMap values must be actual portal color token names or hex values from the existing portal color system -- not placeholder strings like '#green'. RD: read DistributionTab.tsx to confirm what color tokens are in use.\n(3) The NMNC/NMEC 12-month window rule proposed in ADVI-001 was not verified against the existing header_metrics.json CLA structure. DS must confirm how NMNC/NMEC is defined in the current gold layer output, not assume it."
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

## Pattern 0 Alignment -- adv_drill + cla_timeseries

I am the COO convening this alignment thread. Two publisher outputs are needed for the Distribution tab: adv_drill (per-architect NNA time series for ADV continuous view) and cla_timeseries (NMNC/NMEC AUM composition over time for continuous CLA view). Neither exists today. Before any code is written, DS, DE, and RD must agree on exact JSON shapes, TypeScript interfaces, and chart constraints.

This is a re-run. The previous thread produced contracts with three critical gaps: (1) cla_timeseries was missing geo_drill for city-level drill-down, (2) colorMap values were placeholders not real portal tokens, (3) NMNC/NMEC classification logic was assumed without verification. Fix all three this time.

**Turn order:** DS -> DE -> RD. Three turns per agent.

**DS (0.4.0_DS_ClientPlatform) -- your turn first.**

Read lambda_function.py (the publisher Lambda in context) and data_contract.xml before answering. Cite specific function names and field names from those files.

1. For adv_drill: what per-architect and per-client NNA data currently exists? Name specific parquet files, column names, and cardinality. What cumulative NNA time series can you produce per architect -> per client? What date range and density?

2. For cla_timeseries: how is NMNC vs NMEC CURRENTLY defined in the gold layer output? Read data_contract.xml and the publisher Lambda to find the existing definition -- do not assume a 12-month first_seen_date rule. Name the specific field, table, or derivation logic. Can you produce daily NMNC AUM and NMEC AUM at total, geo (state), geo_drill (city within state), and adv (architect) grains?

3. For both: describe the exact output shape you will produce -- field names, nesting, value types (dollars, cumulative, absolute). Show how it relates to existing geo/geo_drill structure in timeseries_chart.json. Include a colorMap field per series with values that reference the existing portal color system (RD will confirm the exact tokens).

**DE (0.4.0_DE_ClientPlatform):** Read types.ts before responding. Specify the exact TypeScript interface names and shapes the portal needs. Name the query key and endpoint path for each.

**RD (0.4.2_RD_AdvisorIntelligence):** Read DistributionTab.tsx before responding. Identify what color tokens are currently in use and specify the exact colorMap values (portal tokens or hex). Flag any chart constraint that affects the data model.

**IMPORTANT (M2):** If any agent cites a field, S3 path, or interface name without naming the file it came from, the next agent must ask for the exact path before treating it as ground truth.

**Final turn must produce a structured contract block with:**
- adv_drill JSON schema (exact field names, types, nesting)
- cla_timeseries JSON schema (including geo_drill for city-level drill)
- colorMap spec with actual portal token names or hex values
- TypeScript interface names (DE confirms)
- S3 key / output location for each
- NMNC/NMEC classification logic (agreed definition verified against existing code, not assumed)
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

# Resolve the actual thread ID (auto-assigned by project)
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
