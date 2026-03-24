#!/usr/bin/env bash
# ADVI_MVPLVL-006 -- 4-party E2E trace: Mix + Composition views broken at all drill levels
# Pattern 0 alignment thread: DS + AE + DE + RD
# Diagnose where the chain breaks: gold layer -> Lambda -> TypeScript -> frontend component
#
# Run from repo root: bash org/threads/staging/run-ADVI_MVPLVL-006-mix-composition-e2e-trace.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_MVPLVL"
THREAD_ID=""              # auto-assigned from project serial
TOPIC="Mix and Composition E2E trace -- broken views diagnosis"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.6.0_AE_PartnerETL,0.4.0_DE_ClientPlatform,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="gpt-5.2"

# ---------------------------------------------------------------------------
# Context -- M1 compliant: actual source files for all knowledge-bearing agents
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Gold script 06b -- builds firm_mix_views.json + per-advisor mix.json + client_mix_timeseries parquet (4-class taxonomy via ETFClassifier)",
      "path": "data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py"
    },
    {
      "label": "Gold script 12 -- builds firm_composition.json + per-advisor composition.json (asset mix radial + top holdings per class, ETFClassifier)",
      "path": "data/black_diamond/scripts/gold/12_build_composition_artifacts.py"
    },
    {
      "label": "Lambda function -- opal-partners-data (partners-api-v1.8.0). Contains ALL routes: mix-views, advisor mix, firm composition, advisor composition, relationship composition",
      "path": "infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py"
    },
    {
      "label": "Portal API endpoints -- advisor-intelligence.ts. All fetch functions for AdvisorIntelligence page",
      "path": "portal/src/api/endpoints/advisor-intelligence.ts"
    },
    {
      "label": "Portal TypeScript types -- types.ts. FirmMixViewsResponse, BooksCompositionResponse, AuaMixView, MixAssetClass, MixItem, etc.",
      "path": "portal/src/pages/AdvisorIntelligence/types.ts"
    },
    {
      "label": "PartnerAnalytics.tsx -- Assets Overview header panel (AUA / Clients / Mix toggles). The 'Mix' toggle is broken.",
      "path": "portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx"
    },
    {
      "label": "ClientsTab.tsx -- Books tab with Overview panels (Asset Mix radial + Top Holdings bars). Both are broken at all drill levels.",
      "path": "portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx"
    },
    {
      "label": "AUACompositionChart.tsx -- composition chart rendering component",
      "path": "portal/src/pages/AdvisorIntelligence/components/AUACompositionChart.tsx"
    },
    {
      "label": "MixTimeseriesPanel.tsx -- ClientDetail mix timeseries panel (recently fixed by DT for 4-class taxonomy)",
      "path": "portal/src/pages/AdvisorIntelligence/ClientDetail/panels/MixTimeseriesPanel.tsx"
    }
  ],
  "documents": [
    {
      "label": "ADVI_MVPLVL.009 task order -- full problem statement, data sources, Lambda routes, TypeScript types, acceptance criteria",
      "path": "org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_MVPLVL.009.mix-composition-e2e.md"
    }
  ],
  "inline": "GOAL: Two views in AdvisorIntelligence are completely non-functional despite all upstream projects being marked complete. (1) Assets Overview 'Mix' toggle does not display -- should show asset class stacked bar (equity, fixed income, alternatives, other) in same format as NMEC/NMNC in Clients toggle. (2) Books tab 'Asset Mix' radial + 'Top Holdings' bars do not load at any drill level (firm, advisor, relationship). This thread is a diagnostic -- each agent traces their segment of the chain and identifies exactly where the break is.\n\nROLES:\n- DS (knowledge source): Describes gold layer outputs -- what 06b and 12 produce, JSON shapes, S3 paths, field names\n- AE (knowledge source): Confirms Lambda routes serve the data correctly -- HTTP status, response shape, S3 key mapping\n- DE (knowledge receiver + fixer): Traces API fetch chain through TypeScript types to components, identifies wiring gaps\n- RD (knowledge receiver + fixer): Identifies rendering expectations and what the components need from the data\n\nDELIVERABLE: Thread receipt containing (1) confirmed data path from gold -> Lambda -> portal for each view, (2) exact location of every break in the chain, (3) agreed fix plan per agent.\n\nDEFINITIONS:\n- 'Mix' = breakdown by ASSET CLASS (equity, fixed income, alternatives, other)\n- 'Concentration' = breakdown by SECURITY (individual holdings ranked by market value)\n- 'Other' in Mix context = residual AUA not in equity/fixed_income/alternatives (primarily cash). Do NOT add 'Cash' as a separate label.\n\nCRITICAL CONSTRAINT: Do NOT assume data is missing. The gold rerun completed 2026-03-20 evening. Scripts 06b + 12 ran successfully. Lambda partners-api-v1.8.0 is deployed with all routes. The break is MOST LIKELY in the frontend wiring or a shape mismatch between Lambda response and TypeScript types. Verify before declaring anything missing."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- DS leads the chain trace
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

## E2E Chain Trace: Mix + Composition Views Broken

I am 0.4.0_DS_ClientPlatform. We have two completely non-functional views in AdvisorIntelligence despite all upstream projects (GLDPRE, BKSCMP, CLSPT2, MIXV2) being marked complete. Andrew confirmed on 2026-03-23 that neither loads at any drill level. This thread is a 4-party diagnostic to trace the full chain and find every break.

### The two broken views

**View 1: Assets Overview "Mix" toggle** -- The AUA stacked bar in the header panel (PartnerAnalytics.tsx) has AUA / Clients / Mix toggles. Mix does not display. It should show asset class breakdown (equity, fixed income, alternatives, other) in the EXACT SAME stacked bar format as NMEC/NMNC in the Clients toggle.

**View 2: Books tab "Asset Mix" + "Top Holdings"** -- The Overview panels at the top of /books route (ClientsTab.tsx) do not load at any drill level (firm, advisor, relationship). Expected: (a) Asset Mix radial/donut showing class breakdown, (b) Top Holdings horizontal bars showing top 9 + Other. Critical interaction: clicking a class segment in the radial must filter Top Holdings to top 9 within THAT CLASS.

### My trace: Gold Layer outputs

I will now read scripts 06b and 12 to confirm exactly what they produce and in what shape. AE_PartnerETL -- please confirm the Lambda routes that serve these files and verify they return data (not 404/500). DE_ClientPlatform -- please trace the API fetch chain from the portal endpoint functions through TypeScript types to the components. RD_AdvisorIntelligence -- please identify what each component expects to receive and render.

### Data source chain (from .009 task order)

| Layer | Source | Output |
|-------|--------|--------|
| Gold 06b | 06b_build_client_mix_timeseries.py | firm_mix_views.json, per-advisor mix.json, client_mix_timeseries parquet |
| Gold 12 | 12_build_composition_artifacts.py | firm_composition.json, per-advisor composition.json |
| Lambda | opal-partners-data (partners-api-v1.8.0) | Routes: /books/firm/mix-views, /books/advisor/{id}/mix, /books/firm/all/composition, /books/advisor/{id}/composition, /books/relationship/{id}/composition |
| Portal types | types.ts | FirmMixViewsResponse, BooksCompositionResponse, AuaMixView, MixItem |
| Portal UI | PartnerAnalytics.tsx (View 1), ClientsTab.tsx (View 2), AUACompositionChart.tsx |

### Questions for each agent

**AE_PartnerETL:**
1. Read the Lambda function and confirm each route listed above exists and correctly maps to the S3 key. Specifically: does handle_firm_mix_views() read from gold/firm_mix_views.json? Does handle_firm_composition() read from gold/views/firm_composition.json?
2. Are there any route handler bugs (wrong S3 key, missing handler, exception path)?

**DE_ClientPlatform:**
1. Read advisor-intelligence.ts API endpoints. Is there a fetch function for firm mix-views? For firm composition? For advisor-level composition?
2. Read PartnerAnalytics.tsx -- how does the Mix toggle get its data? Is there a useQuery call? Does it call the right endpoint?
3. Read ClientsTab.tsx -- how do the Overview panels (Asset Mix radial, Top Holdings) get their data? Is there a fetch at each drill level (firm, advisor, relationship)?

**RD_AdvisorIntelligence:**
1. Read AUACompositionChart.tsx -- what props does it expect? What data shape?
2. Read the relevant rendering sections of PartnerAnalytics.tsx and ClientsTab.tsx -- is the component actually rendered when the Mix toggle is active? Is the composition panel actually rendered in the Books overview?

## Self-unblock requirement (applies to all participants)

If you are uncertain about a data field, S3 path, route handler, fetch function, or component prop: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer. Acceptable blockers are things that do not exist yet or require a live S3 query. An unresolved question about a file in this repo is not acceptable.

If any answer references a resource name, S3 path, or interface without citing a specific file and line number, ask for the exact location before accepting it as ground truth.
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

echo "Scaffolding thread..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

# Resolve the actual thread ID (auto-assigned if project was set)
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
