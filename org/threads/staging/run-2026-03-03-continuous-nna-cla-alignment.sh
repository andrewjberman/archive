#!/usr/bin/env bash
# run-2026-03-03-continuous-nna-cla-alignment.sh
#
# Pattern 0 pre-implementation alignment — Streams A1 + A2
# Streams: adv_drill (Continuous NNA ADV) + cla_timeseries (Continuous CLA)
# Participants: DS (knowledge source) -> DE (interface spec) -> RD (layout constraints)
#
# Run from repo root: bash org/threads/staging/run-2026-03-03-continuous-nna-cla-alignment.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

THREAD_ID="2026-03-03-continuous-nna-cla-alignment"
TOPIC="Pattern 0 alignment: adv_drill (Continuous NNA ADV) + cla_timeseries (Continuous CLA)"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.3-codex"

# ---------------------------------------------------------------------------
# Context (M1 compliance: DS knowledge source files + portal consumer files)
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "BD portal publisher Lambda (current output producer)",
      "path": "infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py"
    },
    {
      "label": "AdvisorIntelligence TypeScript types (current portal types)",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "DistributionTab component (current consumer)",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx"
    },
    {
      "label": "Advisor Intelligence API endpoints (current endpoint contract)",
      "path": "portal/src/api/endpoints/advisor-intelligence.ts"
    }
  ],
  "documents": [
    {
      "label": "AdvisorIntelligence Completion PRD — Section 3 (Distribution Tab)",
      "path": "docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md"
    }
  ],
  "inline": "This is a Pattern 0 pre-implementation alignment thread for two interface-dependent work streams in the AdvisorIntelligence completion PRD.\n\nStream A1: adv_drill — The publisher Lambda needs to generate per-architect NNA time series (analogous to the existing geo_drill per-city series). This does NOT yet exist. DS must describe what advisor/client-level NNA data is currently available in the gold layer and what an adv_drill output can realistically look like.\n\nStream A2: cla_timeseries — A new time-series view showing NMNC (new client) vs NMEC (existing client) AUM composition over time. This data does NOT exist anywhere in the current pipeline. DS must describe what classification data (NMNC vs NMEC) is available in the gold layer and what a realistic cla_timeseries output looks like.\n\nKnowledge source: 0.4.0_DS_ClientPlatform (what the gold layer can produce).\nInterface specifier: 0.4.0_DE_ClientPlatform (what TypeScript shape the portal needs).\nLayout specifier: 0.4.2_RD_AdvisorIntelligence (what the chart component requires from the data).\n\nDeliverable of this thread: agreed JSON output schemas for adv_drill and cla_timeseries, agreed TypeScript interface names and shapes, agreed S3 key patterns. The final turn must contain this as a structured contract. The COO will embed this receipt in the DS and RD task orders as the binding specification."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message (COO sets agenda, DS goes first)
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

## Pattern 0 Alignment — Streams A1 (adv_drill) and A2 (cla_timeseries)

I am the COO convening this alignment thread before any code is written.
Two new publisher outputs are needed for the AdvisorIntelligence Distribution tab:
adv_drill (per-architect NNA time series for the ADV continuous view) and
cla_timeseries (NMNC/NMEC AUM composition over time for the Continuous CLA view).
Neither exists today. Before DS writes a line of code, DS, DE, and RD must agree
on the exact JSON shapes, TypeScript interfaces, and chart constraints.

**Turn order:** DS -> DE -> RD. Three turns, then this thread is done.

**DS (0.4.0_DS_ClientPlatform) — your turn first. Answer:**

1. For adv_drill: what advisor/client-level NNA data currently exists in the gold layer?
   Name the specific parquet files or tables (e.g., nna_aua_by_advisor.parquet,
   rel_architect_lookup.parquet). Can you produce a per-architect -> per-client
   cumulative NNA time series? What is the realistic cardinality (clients per architect)?
   What date range and density can you commit to?

2. For cla_timeseries: what NMNC/NMEC classification data exists today?
   How is a relationship classified as NMNC vs NMEC (new vs existing client)?
   What is the source field or derivation logic? Which gold layer table carries it?
   Can you produce daily NMNC AUM and NMEC AUM aggregated by state, city, and architect?
   What is missing from current gold output that would need to be added?

3. For both: describe the output shape you CAN produce — specific field names,
   nesting structure, value types (dollars? cumulative?), and how it relates to
   the existing geo/geo_drill structure already in timeseries_chart.json.

**DE and RD:** After DS describes what is possible, respond with what you need:
- DE: the TypeScript interface name, shape, and query key the portal will use
- RD: any chart-level constraint that affects the data model
  (e.g., "the cumulative chart needs a colorMap field per series for consistent coloring")

**IMPORTANT (M2):** If any answer references a parquet file, S3 key, Lambda field,
or interface name without citing a specific file in the repo, ask for the exact path
before treating it as ground truth. Do not converge on a contract that is not anchored
to real, existing data in the gold layer.

**Final turn must include:** A structured contract block with:
- adv_drill JSON schema (exact field names, types, nesting)
- cla_timeseries JSON schema
- TypeScript interface names (DE confirms)
- S3 key / output location for each
- Any open caveats or risks DS wants to flag
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
