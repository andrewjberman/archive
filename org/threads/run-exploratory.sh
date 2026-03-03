#!/usr/bin/env bash
# run-exploratory.sh -- Spin up a baseline context-sync thread between two agents
#
# No configuration required. Logs and READMEs are auto-injected.
# The opening message is written in the voice of AGENT1.
#
# Usage:
#   ./org/threads/run-exploratory.sh <agent1-serial> <agent2-serial> [--model <model>] [--max-turns <n>] [--dry-run]
#
# Examples:
#   ./org/threads/run-exploratory.sh 0.4.0_DS_ClientPlatform 0.6.0_AE_PartnerETL
#   ./org/threads/run-exploratory.sh 0.1.0_DS_MarketIntelligence 0.5.0_AE_OpalETL --model gpt-4o

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
JQ="${REPO_ROOT}/.tools/jq.exe"

# --- Defaults ---
MODEL="gpt-5.2"
MAX_TURNS=2
DRY_RUN=false

# --- Parse args ---
AGENT1="${1:-}"
AGENT2="${2:-}"
shift 2 2>/dev/null || true

if [ -z "$AGENT1" ] || [ -z "$AGENT2" ]; then
  echo "Usage: $0 <agent1-serial> <agent2-serial> [--model <m>] [--max-turns <n>] [--dry-run]"
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)     MODEL="$2";     shift 2 ;;
    --max-turns) MAX_TURNS="$2"; shift 2 ;;
    --dry-run)   DRY_RUN=true;   shift ;;
    *) echo "ERROR: Unknown argument: $1"; exit 1 ;;
  esac
done

# --- Thread ID ---
DATE=$(date +"%Y-%m-%d")
# Shorten serials for slug: take the role+name part (e.g. DS_ClientPlatform)
A1_SLUG=$(echo "$AGENT1" | cut -d'.' -f3 | tr '[:upper:]' '[:lower:]' | tr '_' '-')
A2_SLUG=$(echo "$AGENT2" | cut -d'.' -f3 | tr '[:upper:]' '[:lower:]' | tr '_' '-')
THREAD_ID="${DATE}-${A1_SLUG}+${A2_SLUG}-sync"

# --- Resolve agent role names for the opening message ---
get_role_name() {
  local serial="$1"
  local code
  code=$(echo "$serial" | cut -d'.' -f3 | cut -d'_' -f2)
  case "$code" in
    SA) echo "Systems Architect" ;;
    DE) echo "Dashboard Engineer" ;;
    DT) echo "DevOps Technician" ;;
    DS) echo "Data Scientist" ;;
    AE) echo "AWS Engineer" ;;
    RD) echo "React Designer" ;;
    *)  echo "$code" ;;
  esac
}

A1_ROLE=$(get_role_name "$AGENT1")
A2_ROLE=$(get_role_name "$AGENT2")

# --- Write opening message (in voice of AGENT1) ---
OPENING_FILE=$(mktemp /tmp/thread-opening-XXXXXX.md)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

cat > "$OPENING_FILE" << EOF
---
agent: ${AGENT1}
turn: 0
timestamp: ${TS}
signal: continue
---

## Context Sync

I am ${AGENT1} (${A1_ROLE}). I am initiating this sync to share recent context and understand what you have been focused on.

My README and any recent session logs are provided in context -- read them to understand my role and current state. If my logs are sparse or absent I am a recently activated agent and this sync is part of establishing shared awareness.

## What I would like from you

1. **Recent work summary** -- based on your session logs and deployment tags in context, what have you been focused on? What decisions were made or outputs shipped?

2. **Cross-dependencies** -- is there anything from your recent work that has downstream implications for my domain? New data shapes, changed endpoints, schema changes, deployment decisions?

3. **Open questions** -- do you have any questions or dependencies on my end that I should be aware of?

After your response I will follow up with anything from my side that affects you.
EOF

# --- Write inline context briefing ---
CONTEXT_FILE=$(mktemp /tmp/thread-context-XXXXXX.json)
cat > "$CONTEXT_FILE" << EOF
{
  "inline": "This is a baseline context-sync thread between ${AGENT1} (${A1_ROLE}) and ${AGENT2} (${A2_ROLE}). Both agents should reference their auto-injected session logs and READMEs. The goal is to surface recent work, cross-dependencies, and any open questions between their domains. Keep responses concrete -- name files, functions, resource names, and decisions."
}
EOF

# --- Scaffold thread ---
echo "Scaffolding thread: ${THREAD_ID}"
"${SCRIPT_DIR}/create-thread.sh" \
  --id          "$THREAD_ID" \
  --topic       "Context sync: ${AGENT1} + ${AGENT2}" \
  --created-by  "$AGENT1" \
  --participants "${AGENT1},${AGENT2}" \
  --context-file "$CONTEXT_FILE" \
  --opening-message "$OPENING_FILE" \
  --max-turns   "$MAX_TURNS" \
  --turn-order  alternating

rm -f "$OPENING_FILE" "$CONTEXT_FILE"

# --- Run orchestrator ---
DRY_FLAG=""
if [ "$DRY_RUN" = "true" ]; then
  DRY_FLAG="--dry-run"
fi

echo ""
echo "Running orchestrator..."
python "${SCRIPT_DIR}/orchestrator.py" \
  --thread    "$THREAD_ID" \
  --model     "$MODEL" \
  --no-tools \
  --verbose \
  $DRY_FLAG
