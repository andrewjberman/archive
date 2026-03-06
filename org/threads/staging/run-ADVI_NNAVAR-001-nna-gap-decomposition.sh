#!/usr/bin/env bash
# run-ADVI_NNAVAR-001-nna-gap-decomposition.sh
#
# Pattern 2 (Technical Gap Investigation): DS + DT NNA gap decomposition alignment
# Goal: DS analyzes param grid v2 results (correlation plateau at r=0.175), proposes
#       gap decomposition framework for the remaining -$119.8M gap. DT confirms
#       EC2 execution feasibility and script execution sequence.
# Output: Agreed diagnostic sequence + optimal ACAT param recommendation.
#         DS will write a gap decomposition design brief from the receipt.
# Participants: DS -> DT (round_robin, gpt-5.2, tools ON)
# M1: script 05 (target modification), param grid script, correlation summary script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_NNAVAR"
THREAD_ID=""              # auto-assigned (ADVI_NNAVAR-001)
TOPIC="NNA gap decomposition: param grid analysis and diagnostic sequence planning"
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
      "label": "Script 05 -- gold layer client performance builder (target for parameter modifications: velocity cap, outflow cap, dedup, JNL/sweep filter, ACAT integration)",
      "path": "data/black_diamond/scripts/gold/05_build_client_performance.py"
    },
    {
      "label": "ACAT param grid engine -- the 24-combo grid script already executed; v2 baseline uses gold parquet not raw silver",
      "path": "data/black_diamond/scripts/diagnostics/diag_acat_param_grid.py"
    },
    {
      "label": "Correlation summary analysis script -- written but NOT YET RUN; reads s3://opal-data-bd/diagnostics/acat_param_grid_results.csv",
      "path": "data/black_diamond/scripts/diagnostics/diag_acat_correlation_summary.py"
    }
  ],
  "documents": [
    {
      "label": "NNAVAR PRD -- full optimization scope: ACAT params, gap decomposition, diagnostic framework, production implementation",
      "path": "docs/architecture/NNA_VARIANCE_OPTIMIZATION_PRD.md"
    },
    {
      "label": "Existing ACAT v3 production design brief -- 30d/3-burst methodology, $45.98M recovery, current param recommendation",
      "path": "docs/briefs/data-scientist-acat-inkind-nna-production-design.md"
    }
  ],
  "inline": "This is an ADVI_NNAVAR-001 gap decomposition alignment thread between DS and DT.\n\nContext: The ACAT param grid v2 (24 combos, ONBOARDING_DAYS x BURST_THRESHOLD) was executed on 2026-03-05. Critical finding: ALL ACAT combos return Pearson r = 0.175 -- identical to the no-ACAT baseline. ACAT adds $12-22M gap closure but does NOT improve correlation. The remaining -$119.8M 13-month gap vs Schwab is driven by factors OUTSIDE the ACAT scope.\n\nThe NNAVAR PRD identifies candidate explanatory variables: JNL/sweep exclusion calibration, velocity cap tuning (90-day/1.0x AUA), AUA-based outflow cap, transaction deduplication aggressiveness, account coverage gaps (43 accounts = $9.1M), timing misalignment.\n\nNote: The JNL/sweep exclusion fix was ALREADY committed to script 05 + 05b (canonical_nna_logic.md session, 2026-03-05). It is committed but NOT yet rebuilt into gold layer (awaiting CEO go/no-go). This is NOT in the NNAVAR PRD prior art table -- DS should be aware of it.\n\nDS is the knowledge source: they know the script logic, the filter parameters, and what diagnostic framework is needed. DT is the execution source: they know EC2 feasibility, runtime estimates, and S3 artifact management.\n\nPurpose of this thread:\n1. DS proposes the gap decomposition diagnostic framework (which filters to test, in what order)\n2. DS recommends optimal ACAT params from the v2 grid (even though ACAT alone doesn't move r)\n3. DT confirms EC2 feasibility and execution sequence for each proposed diagnostic\n4. Thread receipt = agreed diagnostic plan that COO will convert to DS+DT task orders\n\nDeliverable: DS closes with a concrete decomposition plan block: which diagnostics to run, what each measures, expected EC2 runtime, and the recommended ACAT params. DT confirms or adjusts the execution plan."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message (COO voice, DS goes first)
# ---------------------------------------------------------------------------

OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
printf -- '---\nagent: %s\nturn: 0\ntimestamp: %s\nsignal: continue\n---\n\n' "$CREATED_BY" "$TS" > "$OPENING_FILE"
cat >> "$OPENING_FILE" << 'OPENING_EOF'
## ADVI_NNAVAR-001: NNA Gap Decomposition Planning

I am 2.0.0_SA_COO opening this thread for project ADVI_NNAVAR. The NNAVAR PRD has been issued. Both DS and DT have extensive prior art on the ACAT diagnostic work. This thread produces the agreed diagnostic plan that I will convert to task orders.

## Situation Summary (COO context for both agents)

The param grid v2 (24 combos) ran on 2026-03-05. Key finding: Pearson r = 0.175 for ALL combos, including the no-ACAT baseline. ACAT adds $12-22M in gap closure dollar terms, which is real and should be integrated -- but correlation vs Schwab does not improve. The -$119.8M total 13-month gap is driven by something outside ACAT detection scope.

The NNAVAR PRD (docs/architecture/NNA_VARIANCE_OPTIMIZATION_PRD.md) defines the target: Pearson r >= 0.50, sign agreement >= 10/13 months. Six candidate explanatory variables are listed: JNL/sweep exclusion calibration, velocity cap tuning, AUA-based outflow cap, dedup aggressiveness, account coverage, timing misalignment.

Additional context DS should be aware of: the JNL/sweep exclusion fix was already committed to scripts 05 and 05b in the canonical_nna_logic session (2026-03-05), but has NOT been rebuilt into the gold layer yet (awaiting CEO go/no-go). This is a potential correlation improvement that needs to be quantified in this diagnostic plan.

## Questions for DS (goes first)

1. **Param recommendation**: Given the v2 grid results (r=0.175 flat across all ACAT combos), what ACAT parameters do you recommend integrating into script 05? Even if ACAT does not move correlation, the $45.98M gap closure from the Phase 3 analysis is real. Read diag_acat_param_grid.py and the correlation summary script to confirm the winning combo.

2. **Gap decomposition framework**: Script 05 has multiple filter stages. For each candidate variable in the PRD (velocity cap, outflow cap, JNL exclusion, dedup, account coverage, timing), what diagnostic would you run to attribute monthly NNA impact? What script(s) would need to be written or modified?

3. **JNL/sweep exclusion**: The fix is committed but not rebuilt. Read script 05 to confirm exactly what was changed (action field filter + description exclusions). What does the expected correlation impact look like when this runs?

4. **Diagnostic sequence**: In what order should the diagnostics run to avoid confounding variables? (e.g., does the JNL fix need to be rebuilt before velocity cap testing is meaningful?)

## Questions for DT (goes second)

1. **EC2 feasibility**: For each diagnostic DS proposes, confirm: is the data available on EC2? What is the expected runtime (order of magnitude)? Any S3 path issues?

2. **Rebuild sequencing**: After the diagnostic phase, script 05 + 05b need to be rebuilt with the winning parameter set. What is the EC2 runtime for a full gold layer rebuild? Are scripts 09/10 re-runs included in the same session?

3. **Correlation summary script**: diag_acat_correlation_summary.py is written but not run. Can DT run it immediately (reads from S3, no heavy compute) to surface the ranked param table before the next diagnostic round?

## Self-unblock requirement (applies to both agents)

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer. Acceptable blockers are things that do not exist yet or require a live data query. An unresolved question about a file in this repo is not an acceptable receipt caveat.

If any answer references a parameter, filter condition, or S3 key without citing the specific script line or variable name, the other agent must ask for the exact location before accepting it as ground truth.

## Expected Receipt Format (final turn)

DS closes with a structured block:
- Recommended ACAT params (ONBOARDING_DAYS, BURST_THRESHOLD, MIN_ACAT_ESTIMATE) with rationale
- Gap decomposition diagnostic sequence: ordered list of diagnostics, what each measures, script needed
- Estimated correlation impact of JNL/sweep fix (if readable from committed code)
- Any hard blockers that require a live data query (acceptable caveats only)

DT confirms or amends the execution plan with EC2 feasibility notes.
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

echo "Scaffolding thread ADVI_NNAVAR-001..."
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
