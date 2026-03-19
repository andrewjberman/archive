#!/usr/bin/env bash
# BESPOKE_TEMPLATE.sh -- Template for generated bespoke thread run scripts
#
# Claude Code generates one of these when you describe a thread in natural language.
# Everything is self-contained: CONTEXT.json and opening message are embedded as
# heredocs. Run it once from the repo root and the thread scaffolds and executes.
#
# Generated scripts are named: staging/run-{PROJECT_CODE}-{NNN}-{slug}.sh  (project threads)
#                          or: staging/run-YYYY-MM-DD-{slug}.sh             (non-project threads)
# Run from repo root: bash org/threads/staging/run-{name}.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration -- edit these when generating a new script
# ---------------------------------------------------------------------------

PROJECT="{CODE}"          # project code from org/projects/REGISTRY.md (e.g. AI, PEB)
                          # leave blank and set THREAD_ID manually for non-project threads
THREAD_ID=""              # auto-assigned from project serial if PROJECT is set
TOPIC="{Human-readable topic}"
CREATED_BY="{opening-agent-serial}"
PARTICIPANTS="{agent1-serial},{agent2-serial}"
MAX_TURNS=3               # bespoke default; use 2 for shorter exchanges
MODEL="claude-sonnet-4-6"  # current standard model

# ---------------------------------------------------------------------------
# Context -- files and briefing injected into CONTEXT_COMPILED.md
# ---------------------------------------------------------------------------

CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << 'CONTEXT_EOF'
{
  "code": [
    {
      "label": "{Descriptive label}",
      "path": "relative/path/to/file.ts"
    }
  ],
  "documents": [
    {
      "label": "{Doc label}",
      "path": "docs/path/to/doc.md"
    }
  ],
  "inline": "Briefing paragraph: state the goal of the conversation, which agent is the knowledge source, which is the receiver, and what deliverable the receiver will produce."
}
CONTEXT_EOF

# ---------------------------------------------------------------------------
# Opening message -- written in the voice of CREATED_BY
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

## {Opening section title}

{Who I am and why we are having this conversation. Be specific about what I need
and what deliverable I will produce from this conversation.}

## Questions

{Structured, specific questions. Reference files or endpoints by name where possible.
If asking AE/DT about pipeline behavior, ask for: Lambda function name, S3 key pattern,
EventBridge schedule, known issues. Do not ask vague questions.}

If any answer references a resource name without citing a specific file or config,
ask for the exact location before accepting it as ground truth.

## Self-unblock requirement (applies to all participants)

If you are uncertain about a data field, date range, output shape, or script
behavior: use your tool access to read the relevant file and resolve the question
before your final turn. Do not close the thread with a caveat that file inspection
would answer. Acceptable blockers are things that do not exist yet or require a
live data query outside the repo. An unresolved question about a file in this repo
is not an acceptable receipt caveat.
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
