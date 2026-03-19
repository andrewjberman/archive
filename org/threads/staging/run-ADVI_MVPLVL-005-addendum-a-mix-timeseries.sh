#!/usr/bin/env bash
# ADVI_MVPLVL-005: Addendum A — Mix Timeseries Gold Script + Endpoints + Frontend Alignment
#
# Pattern 0: Pre-implementation alignment (DS + AE + RD)
# CONTEXT SLIMMED: only run_all.sh injected as code. Agents use tools for larger files.
# PRD Addendum A key specs embedded in the inline briefing + opening message.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_MVPLVL"
THREAD_ID=""
TOPIC="Addendum A mix timeseries alignment"
CREATED_BY="0.4.0_DS_ClientPlatform"
PARTICIPANTS="0.6.0_AE_PartnerETL,0.4.2_RD_AdvisorIntelligence"
MAX_TURNS=3
MODEL="claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Context -- lightweight: only small files injected, agents use tools for rest
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "run_all.sh (EC2 gold runner pipeline order -- 06b goes after 06)",
      "path": "data/black_diamond/scripts/gold/run_all.sh"
    }
  ],
  "inline": "ALIGNMENT THREAD: DS + AE + RD must agree on the interface contract for Addendum A of ADVI_MVPLVL before task orders are written.\n\nDS (0.4.0_DS_ClientPlatform) is the knowledge source -- built the classification pipeline and point-in-time composition endpoints. AE (0.6.0_AE_PartnerETL) owns the EC2 gold runner and will deploy the new gold script. RD (0.4.2_RD_AdvisorIntelligence) will wire Mix + Concentration timeseries charts into Books Tab L3/L4.\n\nKEY FILES (use tools to read as needed):\n- data/black_diamond/scripts/gold/05b_build_account_performance.py -- pattern for 06b (positions_cube x prices join, ThreadPoolExecutor)\n- data/black_diamond/scripts/gold/06_build_client_tax_liability.py -- 06b goes after this\n- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py -- existing endpoints + where new ones go\n- infra/aws/lambda/v2_portal/_shared/etf_classification.py -- _classify_holding pipeline\n- portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx -- Books Tab L3/L4 drill\n- docs/architecture/ADVI_MVPLVL_PRD.md -- full PRD (Addendum A starts at line 796)\n\nGOLD ARTIFACTS (from PRD Addendum A2):\n1. gold/client_mix_timeseries.parquet: (date, relationship_id, asset_class, market_value, pct) -- 5 classes: equity, fixed_income, structured_notes, cash, other\n2. gold/client_concentration_timeseries.parquet: (date, relationship_id, asset_name, ticker, asset_class, market_value)\n\nLAMBDA ENDPOINTS (from PRD A3):\n- GET /api/scoped/partners/books/relationship/{id}/mix-timeseries?firmId=xxx -- returns wide-format {date, equity, fixed_income, ...} as pct\n- GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries?firmId=xxx -- returns top-N holdings per date\n\nFRONTEND (from PRD A4):\n- Stacked area chart for Mix timeseries at L3 (relationship) and L4 (account)\n- Concentration chart linked to Mix: clicking asset class in Mix filters Concentration\n- Same time window (1Y/3Y/Max) and granularity as AUA/NNA charts\n\nDELIVERABLE: Agreed contract covering (1) gold artifact schema, (2) endpoint response shape, (3) chart data consumption pattern."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- DS describes the design and asks targeted questions
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

## Addendum A: Mix Timeseries Pipeline -- Alignment Thread

I am DS (0.4.0_DS_ClientPlatform). I built the point-in-time composition endpoints
and the classification pipeline (\`_classify_holding\` in \`etf_classification.py\`)
that classifies holdings into \`equity | fixed_income | structured_notes | cash | other\`
with 96.9% MV coverage. I need alignment with AE (EC2 deployment) and RD (frontend
chart consumption) before writing the gold script and timeseries Lambda endpoints.

### What I plan to build

**Gold script: \`06b_build_client_mix_timeseries.py\`**

Position after \`06_build_client_tax_liability.py\` in run_all.sh. Same join pattern
as \`05b_build_account_performance.py\`: positions_cube x canonical_prices x
accounts_dimension, ThreadPoolExecutor parallelism, pre-forward-filled prices.

Two output artifacts per date partition:
1. \`gold/client_mix_timeseries.parquet\` -- (date, relationship_id, asset_class, market_value, pct)
2. \`gold/client_concentration_timeseries.parquet\` -- (date, relationship_id, asset_name, ticker, asset_class, market_value)

Both include an AP active gate (45-day account_performance filter) to prevent the
\$371M stale-holdings inflation from contaminating totals.

Full rebuild: ~2,081 daily positions_cube files, estimated 30-45 min on EC2.
Incremental mode: watermark-based, processes only new dates.

**Lambda endpoints (opal-partners-data):**

\`\`\`
GET /api/scoped/partners/books/relationship/{id}/mix-timeseries?firmId=xxx
GET /api/scoped/partners/books/relationship/{id}/concentration-timeseries?firmId=xxx
\`\`\`

Mix returns wide-format: \`{date, equity: 0.72, fixed_income: 0.24, ...}\` as pct values.
Concentration returns top-N per date with an Other bucket.

### Questions for AE (0.6.0_AE_PartnerETL)

1. **run_all.sh wiring:** Read \`data/black_diamond/scripts/gold/run_all.sh\` -- where exactly
   should 06b slot in? After 06 and before which script?
2. **Incremental mode:** The existing gold runner does full rebuild nightly. Should 06b support
   \`--incremental\` from day one, or full-rebuild-only first?
3. **EC2 resource concerns:** 05b runs with ThreadPoolExecutor on the r6i.xlarge. 06b has
   similar workload. Any memory or runtime concerns?
4. **S3 output keys:** Confirm: \`s3://opal-data-bd/gold/client_mix_timeseries.parquet\` and
   \`s3://opal-data-bd/gold/client_concentration_timeseries.parquet\`. Single-file or Hive-partitioned?

### Questions for RD (0.4.2_RD_AdvisorIntelligence)

1. **Chart type:** PRD specifies stacked area. Is 100% stacked area (always sums to 100%)
   better for showing allocation shifts over time?
2. **Time window controls:** Reuse the lifted time window from AdvisorIntelligence.tsx (2i),
   or does L3 need its own independent controls?
3. **Granularity:** Should Mix respect Monthly/Quarterly/Annually toggle, or use daily data?
4. **Mix-to-Concentration linkage:** When user clicks an asset class in Mix chart, Concentration
   filters to that class. What click interaction pattern fits the Books Tab drill UX?
   Read \`portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx\` to ground your answer.
5. **L4 (Account level):** Show relationship-level data at L4, or filter by account_id
   (requires adding account_id column to concentration artifact)?

### Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior:
use your tool access to read the relevant file and resolve it before your final turn.
Do not close the thread with a caveat that file inspection would answer. Acceptable
blockers are things that do not exist yet or require a live data query.
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
