#!/usr/bin/env bash
# REVIEW_TEMPLATE.sh -- Template for CTO task order review threads (Pattern R)
#
# Run AFTER COO writes draft task orders, BEFORE committing them.
# CTO reads drafts + receipts + source files with full tool access.
# Outputs corrections list or APPROVED. Record saved in thread folder.
#
# Generated scripts are named: staging/run-YYYY-MM-DD-{CODE}-{NNN}-review.sh
# Run from repo root: bash org/threads/staging/run-{name}.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# No --project flag for review threads. Name explicitly.
THREAD_ID="YYYY-MM-DD-{CODE}-{NNN}-review"
TOPIC="Pattern R: CTO task order review -- {CODE}-{NNN} post-receipt"
CREATED_BY="2.0.0_SA_COO"
PARTICIPANTS="1.0.0_SA_CTO"
MAX_TURNS=2
MODEL="claude-sonnet-4-6"

# ---------------------------------------------------------------------------
# Context -- inject drafts + receipts + source files
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "Draft task order: {agent} -- {stream}",
      "path": "org/{tier}/{serial}/task_orders/{CODE}-{NNN}-{slug}.md"
    },
    {
      "label": "Source file cited in task order: {description}",
      "path": "data/black_diamond/scripts/gold/{script}.py"
    }
  ],
  "documents": [
    {
      "label": "Thread receipt: {CODE}-{NNN}",
      "path": "org/threads/{thread-id}/messages/00{N}.md"
    },
    {
      "label": "PRD section for {stream}",
      "path": "docs/architecture/{feature}.md"
    }
  ],
  "inline": "CTO review of draft task orders derived from {CODE}-{NNN} receipt. Review all drafts for correctness before COO commits them. Corrections will be applied; record of this review is permanent."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- COO hands off to CTO for review
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

## Pattern R: CTO Task Order Review -- {CODE}-{NNN}

COO has written {N} draft task orders derived from the {CODE}-{NNN} thread receipt.
The drafts are injected as context above. Before I commit them, review each one for
correctness using your tool access. Do not accept any claim at face value -- read
the cited files and verify.

## Receipts reviewed

- {CODE}-{NNN}: {topic} (receipt: org/threads/{thread-id}/messages/00{N}.md)

## Draft task orders under review

- {agent}: org/{tier}/{serial}/task_orders/{CODE}-{NNN}-{slug}.md (status: draft)

## Review checklist -- apply to every draft

For each task order:

1. BLOCKED items: read the cited source file. Confirm the blocker is real.
   If a file contains the field the agent claimed was missing, flag it as a
   false block and provide the correct implementation path.

2. Data source references: verify every parquet file, Lambda, or script named
   in the task order appears in the receipt and exists in the repo.
   If a file name does not match the receipt or does not exist, flag it.

3. JSON shapes: verify the structure matches both the receipt and the PRD.
   If nesting, key names, or sign conventions differ between task order and
   receipt, flag the discrepancy with the correct version.

4. TypeScript interface names: confirm each interface name matches what DE
   agreed in the receipt. Flag any invented names not present in the receipt.

## Output format

For each task order, output one of:
  APPROVED: {filename} -- no corrections needed
  CORRECTIONS: {filename}
    - [{requirement id}] {description of issue} -> {correct value or action}

If all task orders are approved, output: ALL APPROVED -- COO may commit.
If any corrections are needed, list them all. COO will apply and re-run if needed.

## Self-unblock requirement

If uncertain whether a file exists, a field is present, or a shape is correct:
use your tool access to read the file and resolve the question. Do not output
a caveat -- output a definitive finding.
OPENING_EOF

# ---------------------------------------------------------------------------
# Scaffold and run
# ---------------------------------------------------------------------------

CREATE_ARGS=(
  --id              "$THREAD_ID"
  --topic           "$TOPIC"
  --created-by      "$CREATED_BY"
  --participants    "$PARTICIPANTS"
  --context-file    "$CONTEXT_FILE"
  --opening-message "$OPENING_FILE"
  --max-turns       "$MAX_TURNS"
  --turn-order      sequential
)

echo "Scaffolding Pattern R review thread..."
"${THREADS_DIR}/create-thread.sh" "${CREATE_ARGS[@]}"

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

echo ""
echo "Running CTO review on: ${THREAD_ID}"
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
