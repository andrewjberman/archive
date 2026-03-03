#!/usr/bin/env bash
# BESPOKE_TEMPLATE.sh -- Template for generated bespoke thread run scripts
#
# Claude Code generates one of these when you describe a thread in natural language.
# Everything is self-contained: CONTEXT.json and opening message are embedded as
# heredocs. Run it once from the repo root and the thread scaffolds and executes.
#
# Generated scripts are named: staging/run-YYYY-MM-DD-{slug}.sh
# Run from repo root: bash org/threads/staging/run-YYYY-MM-DD-{slug}.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
THREADS_DIR="$REPO_ROOT/org/threads"

# ---------------------------------------------------------------------------
# Configuration -- edit these when generating a new script
# ---------------------------------------------------------------------------

THREAD_ID="YYYY-MM-DD-{slug}"
TOPIC="{Human-readable topic}"
CREATED_BY="{opening-agent-serial}"
PARTICIPANTS="{agent1-serial},{agent2-serial}"
MAX_TURNS=3               # bespoke default; use 2 for shorter exchanges
MODEL="gpt-4o"            # bespoke default; gpt-4o-mini for lighter threads

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
  --turn-order      alternating

rm -f "$CONTEXT_FILE" "$OPENING_FILE"

echo ""
echo "Running orchestrator..."
/c/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe \
  "${THREADS_DIR}/orchestrator.py" \
  --thread  "$THREAD_ID" \
  --model   "$MODEL" \
  --verbose
