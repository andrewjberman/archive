#!/usr/bin/env bash
# run-ADVI_BKSCMP-001-task-order-cross-validation.sh
#
# Pattern: Bespoke -- 4-party task order cross-validation (tools enabled)
# Goal:    DS / RD / DT / AE each verify their task order against actual code
#          before implementation starts. Each agent reads the files they own,
#          confirms structural alignment, and flags any discrepancy.
# Run from repo root: bash org/threads/staging/run-ADVI_BKSCMP-001-task-order-cross-validation.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT="ADVI_BKSCMP"
THREAD_ID=""               # auto-assigned from project serial
TOPIC="ADVI_BKSCMP task order cross-validation -- DS, RD, DT, AE verify alignment with current code"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="0.4.0_DS_ClientPlatform,0.4.2_RD_AdvisorIntelligence,0.4.0_DT_ClientPlatform,0.6.0_AE_PartnerETL"
MAX_TURNS=1                # 1 turn per agent -- validate, report, converge
MODEL="claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "run_gold_layer.sh -- full script (DS and AE: verify 08b->12->06b insertion point and upload paths)",
      "path": "data/black_diamond/scripts/gold/run_gold_layer.sh"
    }
  ],
  "documents": [
    {
      "label": "PRD -- ADVI_BKSCMP (canonical schema, algorithm, workstreams, acceptance criteria)",
      "path": "docs/architecture/ADVI_BKSCMP_PRD.md"
    },
    {
      "label": "Task order 001 -- DS: script 12 + Lambda v2.8 routes",
      "path": "org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_BKSCMP.001.ds-script12-lambda-routes.md"
    },
    {
      "label": "Task order 002 -- RD: types.ts + holdings adapter",
      "path": "org/tier3_junior/0.4.2_RD_AdvisorIntelligence/task_orders/ADVI_BKSCMP.002.rd-types-holdings-adapter.md"
    },
    {
      "label": "Task order 003 -- DT: partners-api-v1.5.0 Lambda deploy",
      "path": "org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/ADVI_BKSCMP.003.dt-lambda-deploy.md"
    },
    {
      "label": "Task order 004 -- AE: EC2 gold run + artifact verification",
      "path": "org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/ADVI_BKSCMP.004.ae-ec2-gold-run.md"
    }
  ],
  "inline": "ADVI_BKSCMP cross-validation thread. Each of the four participants validates their own task order against the current state of the files they own. This is not a design discussion -- it is a read-verify-report exercise. Each agent reads the relevant source files, checks the task order requirements against what the code actually contains, and outputs CONFIRMED or DISCREPANCY for each requirement. COO reads the receipts and applies any corrections before implementation starts. All four agents are knowledge sources for their own domain; COO is the receiver of the validation report."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message (COO voice, turn 0)
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

## ADVI_BKSCMP Task Order Cross-Validation

COO has written four task orders for ADVI_BKSCMP. Before implementation starts, each of you
must validate your own task order against the actual files in the repo. The goal is to catch
any mismatch between what the task order says and what the code actually looks like today.

This is a read-verify-report session, not a design discussion. One turn each. Use your tool
access to read the files your task order references. Report CONFIRMED or DISCREPANCY per
requirement. Signal converge when done.

---

## What each agent must verify

### 0.4.0_DS_ClientPlatform (task order ADVI_BKSCMP.001)

Read these files (use tool access):

1. `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py`
   - Verify: line 1222 currently reads `elif action == 'composition': return handle_books_composition(bucket, entity_type, entity_id)`
   - Verify: entity_type validation at line 1212 already includes 'firm' and 'advisor'
   - Verify: `cors_response` function exists around line 106 (your req 3 adds cors_response_nocache after it)
   - Verify: `handle_advisor_mix_views` function exists around line 1055 (your req 4 inserts new handlers after it)

2. `data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py`
   - Verify: `ETF_CLASSIFICATIONS` exists (around line 146)
   - Verify: `ASSET_NAME_TO_TICKER` exists (around line 218)
   - Verify: `_OPAL_ETF_OVERRIDES` exists (search for it -- was added in commit b69d1ae6)
   - Verify: `classify_series()` function exists (around line 307)
   - All four must be present for your req 1 (inline from 06b)

3. `data/black_diamond/scripts/gold/run_gold_layer.sh` (injected in context)
   - Verify: line 114 is 08b, line 115 is 06b (incremental section)
   - Verify: line 158 is 08b, line 159 is 06b (full section)
   - These are your req 2 insertion points

### 0.4.2_RD_AdvisorIntelligence (task order ADVI_BKSCMP.002)

Read these files:

1. `portal/src/pages/AdvisorIntelligence/types.ts`
   - Verify: `MixItem` interface exists and does NOT currently have `top_holdings` or `other` fields
   - Verify: `BooksCompositionResponse` exists and scope does NOT currently have `advisor_id` or `firm_id`
   - Verify: `ConcentrationItem` type is present (your changes reference it but do not modify it)

2. `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx`
   - Verify: lines 875-884 match the block described in req 2 exactly (allItems, filteredItems, MAX_ITEMS, cappedItems, showOther, showFilteredOther, maxPct)
   - Verify: `showFilteredOther` render block is at lines 1039-1050 (your req 3 replaces it)
   - Verify: `showOther` render block is at lines 1055-1068, referencing `composition.concentration.other.pct`
   - Verify: empty state at line 1073 reads `allItems.length === 0 ? 'No holdings data at this level'`
   - Verify: `handleSelectAdvisor` at line 382-383 uses the sanitization pattern in req context

### 0.4.0_DT_ClientPlatform (task order ADVI_BKSCMP.003)

Read these files:

1. `infra/aws/lambda/ci/lambda-source-map.json`
   - Verify: an entry for `opal-partners-data` exists under the `partners-api` pipeline
   - Note the current s3_key and artifact_sha256 -- your req 2 updates these after upload

2. Run in bash (use grep_content or glob_files):
   - Confirm current partners-api tags: check `infra/aws/terraform/partners-api/CHANGELOG.json` for the latest deployed version
   - The task order targets partners-api-v1.5.0 -- verify v1.4.0 is currently the latest so v1.5.0 is the correct next tag

3. Verify the partners-api terraform directory structure exists:
   - `infra/aws/terraform/partners-api/` contains the relevant .tf files
   - `infra/aws/lambda/ci/record-terraform-deploy.sh` exists (req 5 calls it)

### 0.6.0_AE_PartnerETL (task order ADVI_BKSCMP.004)

Read these files:

1. `data/black_diamond/scripts/gold/run_gold_layer.sh` (injected in context)
   - Verify: incremental mode is invoked with `./run_gold_layer.sh --incremental` (req 4 command)
   - Verify: the script performs `aws s3 sync s3://${S3_BUCKET}/code/gold/ SCRIPTS_DIR/` at startup (line ~71)
     so script 12 will be pulled automatically from S3 after upload
   - Verify: `run_gold_layer.sh` itself must be re-pulled separately (it is NOT in the gold/ prefix)
   - Confirm the S3 bucket variable name used in the script (S3_BUCKET) so req 2 upload paths are consistent

2. `infra/aws/ec2/EC2_MANIFEST.json`
   - Verify: bd-gold-layer-runner is already registered with at least one existing deployment record
   - Confirm the manifest format so req 6 (registration) can follow the correct structure

---

## Output format

For each requirement in your task order, output:
  CONFIRMED [req N]: <one-line description of what you verified>
  DISCREPANCY [req N]: <what the task order says vs what you actually found>

If a requirement cannot be verified without a live AWS call (e.g., checking actual S3 file content), mark it:
  LIVE-ONLY [req N]: requires live EC2/S3 access -- cannot verify from repo alone

Flag any discrepancy. Minor line-number drift (±5 lines due to other commits) is fine to note
but does not block. A wrong function name, missing dictionary, or incorrect routing logic
is a real discrepancy and must be flagged.

## Self-unblock requirement (M11)

If you are uncertain about a field name, line number, function name, or S3 path: read the
relevant file using your tool access and resolve the question before your final turn.
Do not close with a caveat that a file read would answer. An unresolved question about
a file in this repo is not an acceptable receipt caveat. Use tools -- that is what they
are for.

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
