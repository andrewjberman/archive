#!/usr/bin/env bash
# run-ADVI_AUAVAR-001-aua-gap-segment-alignment.sh
#
# Pattern 2 (Technical Gap Investigation): DS + DT AUA gap segment decomposition alignment
# Goal: DS proposes date-aligned comparison approach and segment decomposition framework
#       for the ~$55M gap between BD allocations ($1.605B) and our gold layer (~$1.545B).
#       DT confirms EC2 data availability and execution feasibility.
# Output: Agreed segment decomposition design that COO converts to DS+DT task orders.
# Participants: DS -> DT (round_robin, gpt-5.2, tools ON)
# M1: phase1 diagnostic script, script 05 (AUA computation logic), AUAVAR PRD

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_AUAVAR"
THREAD_ID=""              # auto-assigned (ADVI_AUAVAR-001)
TOPIC='AUA gap segment decomposition: BD allocations vs gold layer $55M variance'
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.0_DT_ClientPlatform"
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
      "label": "Phase 1 AUA data collection script -- prior investigation: reads BD allocation snapshots and gold layer parquets, extracts AUA numbers",
      "path": "data/black_diamond/scripts/diagnostics/phase1_data_collection_20260304.py"
    },
    {
      "label": "Script 05 -- gold layer client performance builder: AUA computation from positions_cube + canonical_prices + accounts_dimension; contains velocity cap, outflow cap, dedup, exclusion filters",
      "path": "data/black_diamond/scripts/gold/05_build_client_performance.py"
    }
  ],
  "documents": [
    {
      "label": "AUAVAR PRD -- full decomposition scope: date-aligned comparison, segment breakdown (account coverage, asset class, pricing, household aggregation, cash treatment), waterfall chart data, recommendation memo",
      "path": "docs/architecture/AUA_VARIANCE_ANALYSIS_PRD.md"
    }
  ],
  "inline": "This is an ADVI_AUAVAR-001 AUA gap segment decomposition alignment thread between DS and DT.\n\nContext: As of 2026-03-02, our BD gold layer reports ~$1.545B non-cash AUA while BD's own allocation snapshot shows ~$1.605B. The gap is ~$55M (3.4%). 49Financial leadership uses BD numbers as their source of truth, so understanding where this gap lives is a business priority.\n\nPrior DS investigation (2026-03-05) established:\n- Root cause: fundamental data source difference (BD = point-in-time allocation snapshot; our model = reconstructed from transactions + positions + canonical_prices)\n- Known account coverage gap: 43 accounts in BD but missing from accounts_dimension = $9.1M\n- Deduplication: $0 impact. Settlement/pending trades: $0 impact.\n- Pricing variance: INCONCLUSIVE (BD allocations lack symbol-level data for direct comparison)\n- CRITICAL: The DS Phase 1 investigation showed our model at $1.236B (2026-03-02) vs Andrew's $1.545B. This discrepancy -- $309M difference -- must be explained before any gap decomposition is meaningful. It likely reflects a different date (2026-03-02 vs a later date) or a different AUA definition (non-cash filter, relationship aggregation vs account-level, etc.).\n\nDS is the knowledge source: they know the script logic, prior investigation findings, and what segment decomposition approach will work. DT is the execution source: they know EC2 data availability (are BD allocation snapshots for matching dates on S3?), runtime feasibility, and S3 artifact management.\n\nPurpose of this thread:\n1. DS resolves the $1.236B vs $1.545B discrepancy (by reading script 05 and phase1 script)\n2. DS proposes the segment decomposition approach for the ~$55M gap (once metric is reconciled)\n3. DT confirms data availability: are BD allocation snapshots available at matching dates? What parquets are accessible?\n4. Thread receipt = agreed decomposition plan that COO converts to DS+DT task orders\n\nDeliverable: DS closes with a structured block: reconciled AUA definition, segment list with proposed measurement approach, data requirements per segment, which are addressable vs explainable. DT confirms data availability and EC2 execution path."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message (COO voice, DS goes first)
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
printf -- '---\nagent: %s\nturn: 0\ntimestamp: %s\nsignal: continue\n---\n\n' "$CREATED_BY" "$TS" > "$OPENING_FILE"
cat >> "$OPENING_FILE" << 'OPENING_EOF'
## ADVI_AUAVAR-001: AUA Gap Segment Decomposition Planning

I am 2.0.0_SA_COO opening this thread for project ADVI_AUAVAR. The AUAVAR PRD has been issued by CTO. DS has prior investigation findings from the 2026-03-05 BD model reconciliation. This thread produces the agreed decomposition plan that I will convert to task orders.

## Situation Summary (COO context for both agents)

Business context: 49Financial leadership relies on Black Diamond AUA numbers as their source of truth. BD reports ~$1.605B non-cash AUA (2026-03-03). Our gold layer model reports ~$1.545B. The ~$55M gap (3.4%) needs to be explained at a segment level.

Prior DS investigation established the root cause is a fundamental methodology difference: BD provides a point-in-time allocation snapshot while our model reconstructs AUA from transaction history + daily positions + canonical_prices. This is a legitimate methodology difference, NOT a data quality error -- our model is actually closer to Schwab ($1.51B) than BD is.

**Critical unresolved discrepancy:** DS Phase 1 showed our model at $1.236B (2026-03-02) while Andrew reports $1.545B. This is a $309M difference that must be explained before any segment decomposition can be meaningful. Options: different date (model was run on 2026-03-02, BD was on 2026-03-03 -- market movement?), different AUA definition (cash included/excluded, relationship vs account aggregation), or different script output vs what the portal reads.

## Questions for DS (goes first)

1. **AUA definition reconciliation**: Read phase1_data_collection_20260304.py and script 05. What does the $1.236B figure represent exactly? Which script path, which filters, which date? What does the $1.545B Andrew cites represent? Can you reconcile these two numbers by reading the scripts now?

2. **Segment decomposition approach**: Assuming the AUA definition is reconciled, which of the PRD's six segments (account coverage, asset class variance, pricing variance, household aggregation, cash treatment, closed/pending accounts) are measurable with data we currently have? For each measurable segment, what comparison approach would you use?

3. **Pricing variance path**: The Phase 1 investigation found BD allocations lack symbol/price data. Can symbol-level pricing comparison be done from our end (match BD account-level totals to our canonical_prices + positions_cube at account level)?

4. **Recommendation memo structure**: What classification (Addressable / Explainable / Investigate) do you expect for each segment based on prior findings?

## Questions for DT (goes second)

1. **BD allocation data availability**: Are BD allocation snapshots available on S3 at `s3://opal-data-bd/allocations/`? For what date range? Is a 2026-03-04 snapshot available for date-aligned comparison?

2. **accounts_dimension freshness**: The prior investigation found 43 accounts in BD missing from accounts_dimension. Is accounts_dimension rebuilt frequently? What is the current gap likely to be at a more recent date?

3. **EC2 execution**: For a date-aligned AUA comparison script (loading BD allocations + gold layer parquets for the same date), what is the expected runtime? What S3 paths would the script need to read?

4. **Waterfall output**: Can the EC2 execution produce a structured JSON waterfall (BD Total -> segment adjustments -> Our Total) that DS can then interpret and classify?

## Self-unblock requirement (applies to both agents)

If you are uncertain about a data field, date range, S3 path, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer. The $1.236B vs $1.545B discrepancy must be resolved IN THIS THREAD by reading the scripts -- it is not an acceptable open item.

If any answer references an S3 path, column name, or filter logic without citing the specific script line, the other agent must ask for the exact location before accepting it as ground truth.

## Expected Receipt Format (final turn)

DS closes with a structured block:
- Reconciled AUA definition and explanation of $1.236B vs $1.545B discrepancy
- Segment decomposition plan: ordered list of segments, measurement approach, data needed
- Addressable / Explainable / Investigate classification (preliminary, based on prior findings)
- Any hard blockers (data that genuinely does not exist on S3 -- not a script reading question)

DT confirms or amends with data availability and EC2 execution notes.
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

echo "Scaffolding thread ADVI_AUAVAR-001..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

# Resolve the actual thread ID (auto-assigned from project serial)
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
