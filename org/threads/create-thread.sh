#!/usr/bin/env bash
# create-thread.sh -- Scaffold a new agent conversation thread
#
# Usage:
#   ./org/threads/create-thread.sh \
#     --id "2026-03-02-etl-migration-review" \
#     --topic "Review seeking-alpha ETL migration approach" \
#     --created-by "1.0.0_SA_CTO" \
#     --participants "1.0.0_SA_CTO,0.5.0_AE_OpalETL" \
#     --context-file path/to/CONTEXT.json \
#     --opening-message path/to/opening.md \
#     [--max-turns 3] \
#     [--turn-order alternating]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
THREADS_DIR="$SCRIPT_DIR"
JQ="${REPO_ROOT}/.tools/jq.exe"

# --- Defaults ---
MAX_TURNS=3
TURN_ORDER="alternating"
CONTEXT_FILE=""
OPENING_MESSAGE=""

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --id) THREAD_ID="$2"; shift 2 ;;
    --topic) TOPIC="$2"; shift 2 ;;
    --created-by) CREATED_BY="$2"; shift 2 ;;
    --participants) PARTICIPANTS_RAW="$2"; shift 2 ;;
    --context-file) CONTEXT_FILE="$2"; shift 2 ;;
    --opening-message) OPENING_MESSAGE="$2"; shift 2 ;;
    --max-turns) MAX_TURNS="$2"; shift 2 ;;
    --turn-order) TURN_ORDER="$2"; shift 2 ;;
    *) echo "ERROR: Unknown argument: $1"; exit 1 ;;
  esac
done

# --- Validate required args ---
for var in THREAD_ID TOPIC CREATED_BY PARTICIPANTS_RAW; do
  if [ -z "${!var:-}" ]; then
    echo "ERROR: --$(echo $var | tr '[:upper:]' '[:lower:]' | tr '_' '-') is required"
    exit 1
  fi
done

# --- Parse participants into array ---
IFS=',' read -ra PARTICIPANTS <<< "$PARTICIPANTS_RAW"
if [ ${#PARTICIPANTS[@]} -lt 2 ]; then
  echo "ERROR: At least 2 participants required"
  exit 1
fi

# --- resolve_agent() ---
# Maps a serial number to its folder path, prompt files, and role info.
# Sets: AGENT_DIR, AGENT_PROMPT, AGENT_README, BASE_PROMPT, AGENT_LOGS, AGENT_TASKS, ROLE_CODE, TIER_FOLDER
resolve_agent() {
  local serial="$1"
  ROLE_CODE=$(echo "$serial" | cut -d'_' -f2)

  local x=$(echo "$serial" | cut -d'.' -f1)
  local y=$(echo "$serial" | cut -d'.' -f2)
  local z=$(echo "$serial" | cut -d'.' -f3 | cut -d'_' -f1)

  if [ "$x" != "0" ]; then
    TIER_FOLDER="tier1_exec"
  elif [ "$z" != "0" ]; then
    TIER_FOLDER="tier3_junior"
  elif [ "$y" != "0" ]; then
    TIER_FOLDER="tier2_senior"
  else
    TIER_FOLDER="tier3_junior"
  fi

  AGENT_DIR="$REPO_ROOT/org/$TIER_FOLDER/$serial"
  AGENT_PROMPT="$AGENT_DIR/prompt.md"
  AGENT_README="$AGENT_DIR/README.md"
  AGENT_LOGS="$AGENT_DIR/logs"
  AGENT_TASKS="$AGENT_DIR/task_orders"

  # Map role code to base prompt filename
  case "$ROLE_CODE" in
    SA) BASE_PROMPT="$REPO_ROOT/org/ref/prompts/systems_architect.md" ;;
    DE) BASE_PROMPT="$REPO_ROOT/org/ref/prompts/dashboard_engineer.md" ;;
    DT) BASE_PROMPT="$REPO_ROOT/org/ref/prompts/devops_technician.md" ;;
    DS) BASE_PROMPT="$REPO_ROOT/org/ref/prompts/data_scientist.md" ;;
    AE) BASE_PROMPT="$REPO_ROOT/org/ref/prompts/aws_engineer.md" ;;
    RD) BASE_PROMPT="$REPO_ROOT/org/ref/prompts/react_designer.md" ;;
    *)  echo "WARN: Unknown role code '$ROLE_CODE' for serial '$serial'"; BASE_PROMPT="" ;;
  esac
}

# --- Validate all participants resolve ---
for serial in "${PARTICIPANTS[@]}"; do
  resolve_agent "$serial"
  if [ ! -d "$AGENT_DIR" ]; then
    echo "ERROR: Agent directory not found: $AGENT_DIR (serial: $serial)"
    exit 1
  fi
done

# --- Create thread directory ---
THREAD_DIR="$THREADS_DIR/$THREAD_ID"
if [ -d "$THREAD_DIR" ]; then
  echo "ERROR: Thread already exists: $THREAD_DIR"
  exit 1
fi

mkdir -p "$THREAD_DIR/messages"
mkdir -p "$THREAD_DIR/context/agents"
mkdir -p "$THREAD_DIR/context/refs"
mkdir -p "$THREAD_DIR/context/commits"

echo "OK: Created thread directory: $THREAD_DIR"

# --- Write THREAD.json ---
CREATED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
PARTICIPANTS_JSON=$(printf '%s\n' "${PARTICIPANTS[@]}" | "$JQ" -R . | "$JQ" -s .)

"$JQ" -n \
  --arg id "$THREAD_ID" \
  --arg created_by "$CREATED_BY" \
  --arg created_at "$CREATED_AT" \
  --arg topic "$TOPIC" \
  --argjson participants "$PARTICIPANTS_JSON" \
  --arg turn_order "$TURN_ORDER" \
  --argjson max_turns "$MAX_TURNS" \
  '{
    id: $id,
    created_by: $created_by,
    created_at: $created_at,
    topic: $topic,
    participants: $participants,
    turn_order: $turn_order,
    max_turns_per_agent: $max_turns,
    status: "active"
  }' > "$THREAD_DIR/THREAD.json"

echo "OK: Wrote THREAD.json"

# --- Auto-inject participant context ---
TODAY=$(date +"%Y-%m-%d")

for serial in "${PARTICIPANTS[@]}"; do
  resolve_agent "$serial"

  # Copy README (identity)
  if [ -f "$AGENT_README" ]; then
    cp "$AGENT_README" "$THREAD_DIR/context/agents/${serial}_README.md"
  fi

  # Copy logs from the 3 most recent date folders (more context, same cost)
  if [ -d "$AGENT_LOGS" ]; then
    LOG_DATES=$(ls -1 "$AGENT_LOGS" 2>/dev/null | sort -r | head -3)
    if [ -n "${LOG_DATES}" ]; then
      mkdir -p "$THREAD_DIR/context/agents/${serial}_logs"
      while IFS= read -r log_date; do
        if [ -d "$AGENT_LOGS/$log_date" ]; then
          cp "$AGENT_LOGS/$log_date"/*.md "$THREAD_DIR/context/agents/${serial}_logs/" 2>/dev/null || true
        fi
      done <<< "$LOG_DATES"
    fi
  fi

  # Copy pending task orders
  if [ -d "$AGENT_TASKS" ]; then
    TASK_FILES=$(find "$AGENT_TASKS" -name "*.md" -type f 2>/dev/null)
    if [ -n "$TASK_FILES" ]; then
      mkdir -p "$THREAD_DIR/context/agents/${serial}_task_orders"
      for tf in $TASK_FILES; do
        # Only copy pending task orders (grep for status>pending)
        if grep -q '<status>pending</status>' "$tf" 2>/dev/null; then
          cp "$tf" "$THREAD_DIR/context/agents/${serial}_task_orders/"
        fi
      done
    fi
  fi

  # Inject recent commits authored by this agent (matched by serial in commit message)
  AGENT_COMMITS=$(git -C "$REPO_ROOT" log --oneline --grep="$serial" -20 2>/dev/null)
  if [ -n "$AGENT_COMMITS" ]; then
    {
      echo "# Recent commits by $serial"
      echo ""
      echo "$AGENT_COMMITS"
    } > "$THREAD_DIR/context/agents/${serial}_commits.txt"
    echo "OK: Injected commit history for $serial"
  fi

  # For AE and DT agents: inject recent deployment tags as deployment history
  if [ "$ROLE_CODE" = "AE" ] || [ "$ROLE_CODE" = "DT" ]; then
    RECENT_TAGS=$(git -C "$REPO_ROOT" tag --sort=-creatordate | grep -E "^[a-z].*-v[0-9]" 2>/dev/null | head -20)
    if [ -n "$RECENT_TAGS" ]; then
      {
        echo "# Recent deployment tags (all pipelines, newest first)"
        echo ""
        echo "$RECENT_TAGS"
      } > "$THREAD_DIR/context/agents/${serial}_deployment_tags.txt"
      echo "OK: Injected deployment tags for $serial"
    fi
  fi
done

echo "OK: Auto-injected participant context"

# --- Resolve explicit CONTEXT.json ---
if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
  cp "$CONTEXT_FILE" "$THREAD_DIR/CONTEXT.json"

  # Resolve documents
  DOC_COUNT=$("$JQ" '.documents | length' "$CONTEXT_FILE")
  for ((i=0; i<DOC_COUNT; i++)); do
    LABEL=$("$JQ" -r ".documents[$i].label" "$CONTEXT_FILE")
    DOC_PATH=$("$JQ" -r ".documents[$i].path" "$CONTEXT_FILE")
    SLUG=$(echo "$LABEL" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
    FULL_PATH="$REPO_ROOT/$DOC_PATH"
    if [ -f "$FULL_PATH" ]; then
      cp "$FULL_PATH" "$THREAD_DIR/context/refs/${SLUG}.md"
      echo "OK: Copied document '$LABEL' -> context/refs/${SLUG}.md"
    else
      echo "WARN: Document not found: $FULL_PATH (label: $LABEL)"
    fi
  done

  # Resolve code
  CODE_COUNT=$("$JQ" '.code | length' "$CONTEXT_FILE")
  for ((i=0; i<CODE_COUNT; i++)); do
    LABEL=$("$JQ" -r ".code[$i].label" "$CONTEXT_FILE")
    CODE_PATH=$("$JQ" -r ".code[$i].path" "$CONTEXT_FILE")
    LINES=$("$JQ" -r ".code[$i].lines // empty" "$CONTEXT_FILE")
    SLUG=$(echo "$LABEL" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-.')
    FULL_PATH="$REPO_ROOT/$CODE_PATH"
    EXT="${CODE_PATH##*.}"
    if [ -f "$FULL_PATH" ]; then
      if [ -n "$LINES" ]; then
        START=$(echo "$LINES" | cut -d'-' -f1)
        END=$(echo "$LINES" | cut -d'-' -f2)
        sed -n "${START},${END}p" "$FULL_PATH" > "$THREAD_DIR/context/refs/${SLUG}.${EXT}"
      else
        cp "$FULL_PATH" "$THREAD_DIR/context/refs/${SLUG}.${EXT}"
      fi
      echo "OK: Copied code '$LABEL' -> context/refs/${SLUG}.${EXT}"
    else
      echo "WARN: Code file not found: $FULL_PATH (label: $LABEL)"
    fi
  done

  # Resolve commits
  COMMIT_COUNT=$("$JQ" '.commits | length' "$CONTEXT_FILE")
  for ((i=0; i<COMMIT_COUNT; i++)); do
    LABEL=$("$JQ" -r ".commits[$i].label" "$CONTEXT_FILE")
    RANGE=$("$JQ" -r ".commits[$i].range" "$CONTEXT_FILE")
    SLUG=$(echo "$LABEL" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

    # Build path filter
    PATH_COUNT=$("$JQ" ".commits[$i].paths | length" "$CONTEXT_FILE")
    PATH_ARGS=""
    for ((j=0; j<PATH_COUNT; j++)); do
      P=$("$JQ" -r ".commits[$i].paths[$j]" "$CONTEXT_FILE")
      PATH_ARGS="$PATH_ARGS -- $REPO_ROOT/$P"
    done

    {
      echo "# Commits: $LABEL"
      echo "# Range: $RANGE"
      echo ""
      echo "## Log"
      echo ""
      git -C "$REPO_ROOT" log --oneline "$RANGE" $PATH_ARGS 2>/dev/null || echo "(no commits in range)"
      echo ""
      echo "## Diff Stats"
      echo ""
      git -C "$REPO_ROOT" diff --stat "$RANGE" $PATH_ARGS 2>/dev/null || echo "(no diff)"
    } > "$THREAD_DIR/context/commits/${SLUG}.txt"
    echo "OK: Generated commit context '$LABEL' -> context/commits/${SLUG}.txt"
  done

  # Resolve log entries
  LOG_COUNT=$("$JQ" '.logs | length' "$CONTEXT_FILE")
  for ((i=0; i<LOG_COUNT; i++)); do
    LABEL=$("$JQ" -r ".logs[$i].label" "$CONTEXT_FILE")
    LOG_AGENT=$("$JQ" -r ".logs[$i].agent // empty" "$CONTEXT_FILE")
    LOG_DATE=$("$JQ" -r ".logs[$i].date // empty" "$CONTEXT_FILE")
    LOG_PATH=$("$JQ" -r ".logs[$i].path // empty" "$CONTEXT_FILE")
    SLUG=$(echo "$LABEL" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

    if [ -n "$LOG_AGENT" ] && [ -n "$LOG_DATE" ]; then
      resolve_agent "$LOG_AGENT"
      SRC_DIR="$AGENT_LOGS/$LOG_DATE"
      if [ -d "$SRC_DIR" ]; then
        mkdir -p "$THREAD_DIR/context/refs/${SLUG}"
        cp "$SRC_DIR"/*.md "$THREAD_DIR/context/refs/${SLUG}/" 2>/dev/null || true
        echo "OK: Copied agent logs '$LABEL' -> context/refs/${SLUG}/"
      else
        echo "WARN: No logs found for $LOG_AGENT on $LOG_DATE"
      fi
    elif [ -n "$LOG_PATH" ]; then
      FULL_PATH="$REPO_ROOT/$LOG_PATH"
      if [ -f "$FULL_PATH" ]; then
        cp "$FULL_PATH" "$THREAD_DIR/context/refs/${SLUG}.md"
        echo "OK: Copied log '$LABEL' -> context/refs/${SLUG}.md"
      else
        echo "WARN: Log path not found: $FULL_PATH (label: $LABEL)"
      fi
    fi
  done

  # Resolve inline notes
  INLINE=$("$JQ" -r '.inline // empty' "$CONTEXT_FILE")
  if [ -n "$INLINE" ]; then
    echo "$INLINE" > "$THREAD_DIR/context/inline_notes.md"
    echo "OK: Wrote inline notes"
  fi
else
  # Write empty CONTEXT.json from template
  cp "$THREADS_DIR/templates/CONTEXT.json" "$THREAD_DIR/CONTEXT.json"
fi

# --- Generate CONTEXT_COMPILED.md ---
{
  echo "# Thread Context -- $TOPIC"
  echo ""
  echo "**Thread ID:** $THREAD_ID"
  echo "**Created by:** $CREATED_BY"
  echo "**Created at:** $CREATED_AT"
  echo ""

  # Section 1: Participant roster
  echo "---"
  echo ""
  echo "## Participants"
  echo ""
  for serial in "${PARTICIPANTS[@]}"; do
    resolve_agent "$serial"
    echo "### $serial"
    echo ""
    if [ -f "$THREAD_DIR/context/agents/${serial}_README.md" ]; then
      cat "$THREAD_DIR/context/agents/${serial}_README.md"
      echo ""
    fi
    echo ""
  done

  # Section 2: Explicit context
  echo "---"
  echo ""
  echo "## Reference Material"
  echo ""

  # Inline notes
  if [ -f "$THREAD_DIR/context/inline_notes.md" ]; then
    echo "### Briefing Notes"
    echo ""
    cat "$THREAD_DIR/context/inline_notes.md"
    echo ""
    echo ""
  fi

  # Refs (documents + code)
  if [ -d "$THREAD_DIR/context/refs" ]; then
    for ref in "$THREAD_DIR/context/refs"/*; do
      [ -e "$ref" ] || continue
      BASENAME=$(basename "$ref")
      if [ -d "$ref" ]; then
        echo "### $BASENAME"
        echo ""
        for subfile in "$ref"/*; do
          [ -e "$subfile" ] || continue
          echo "#### $(basename "$subfile")"
          echo ""
          echo '```'
          cat "$subfile"
          echo '```'
          echo ""
        done
      else
        echo "### $BASENAME"
        echo ""
        echo '```'
        cat "$ref"
        echo '```'
        echo ""
      fi
    done
  fi

  # Commits
  if [ -d "$THREAD_DIR/context/commits" ]; then
    for commit_file in "$THREAD_DIR/context/commits"/*; do
      [ -e "$commit_file" ] || continue
      echo "### Commits: $(basename "$commit_file" .txt)"
      echo ""
      echo '```'
      cat "$commit_file"
      echo '```'
      echo ""
    done
  fi

  # Section 3: Per-participant background
  echo "---"
  echo ""
  echo "## Participant Background"
  echo ""

  for serial in "${PARTICIPANTS[@]}"; do
    # Logs
    if [ -d "$THREAD_DIR/context/agents/${serial}_logs" ]; then
      echo "### ${serial} -- Recent Session Logs"
      echo ""
      for logfile in "$THREAD_DIR/context/agents/${serial}_logs"/*; do
        [ -e "$logfile" ] || continue
        echo "#### $(basename "$logfile")"
        echo ""
        cat "$logfile"
        echo ""
      done
      echo ""
    fi

    # Task orders
    if [ -d "$THREAD_DIR/context/agents/${serial}_task_orders" ]; then
      TASK_COUNT=$(find "$THREAD_DIR/context/agents/${serial}_task_orders" -name "*.md" 2>/dev/null | wc -l)
      if [ "$TASK_COUNT" -gt 0 ]; then
        echo "### ${serial} -- Pending Task Orders"
        echo ""
        for taskfile in "$THREAD_DIR/context/agents/${serial}_task_orders"/*.md; do
          [ -e "$taskfile" ] || continue
          echo "#### $(basename "$taskfile")"
          echo ""
          cat "$taskfile"
          echo ""
        done
        echo ""
      fi
    fi

    # Recent commits by this agent
    if [ -f "$THREAD_DIR/context/agents/${serial}_commits.txt" ]; then
      echo "### ${serial} -- Recent Commits"
      echo ""
      cat "$THREAD_DIR/context/agents/${serial}_commits.txt"
      echo ""
    fi

    # Deployment tags (AE/DT only)
    if [ -f "$THREAD_DIR/context/agents/${serial}_deployment_tags.txt" ]; then
      echo "### ${serial} -- Recent Deployments"
      echo ""
      cat "$THREAD_DIR/context/agents/${serial}_deployment_tags.txt"
      echo ""
    fi
  done

} > "$THREAD_DIR/CONTEXT_COMPILED.md"

echo "OK: Generated CONTEXT_COMPILED.md"

# --- Copy opening message ---
if [ -n "$OPENING_MESSAGE" ] && [ -f "$OPENING_MESSAGE" ]; then
  cp "$OPENING_MESSAGE" "$THREAD_DIR/messages/000.md"
  echo "OK: Copied opening message as messages/000.md"
elif [ -n "$OPENING_MESSAGE" ]; then
  echo "WARN: Opening message file not found: $OPENING_MESSAGE"
  echo "SKIP: No opening message -- creator must write messages/000.md manually"
fi

# --- Write initial TURN.json ---
# If creator is a participant, they wrote message 000 (their first turn),
# so the next agent is PARTICIPANTS[1]. If creator is NOT a participant
# (e.g., COO opens a thread they don't participate in), PARTICIPANTS[0]
# goes first -- the opening message is not a participant turn.
CREATOR_IS_PARTICIPANT=false
for serial in "${PARTICIPANTS[@]}"; do
  if [ "$serial" = "$CREATED_BY" ]; then
    CREATOR_IS_PARTICIPANT=true
    break
  fi
done

if [ "$CREATOR_IS_PARTICIPANT" = "true" ]; then
  FIRST_TURN_AGENT="${PARTICIPANTS[1]}"
else
  FIRST_TURN_AGENT="${PARTICIPANTS[0]}"
fi

# Build turns_taken: creator (if participant) has 1 turn, everyone else has 0
TURNS_TAKEN=$("$JQ" -n '{}')
for serial in "${PARTICIPANTS[@]}"; do
  if [ "$serial" = "$CREATED_BY" ]; then
    TURNS_TAKEN=$(echo "$TURNS_TAKEN" | "$JQ" --arg s "$serial" '. + {($s): 1}')
  else
    TURNS_TAKEN=$(echo "$TURNS_TAKEN" | "$JQ" --arg s "$serial" '. + {($s): 0}')
  fi
done

"$JQ" -n \
  --argjson turn_number 1 \
  --arg next_agent "$FIRST_TURN_AGENT" \
  --argjson turns_taken "$TURNS_TAKEN" \
  --arg last_updated "$CREATED_AT" \
  '{
    turn_number: $turn_number,
    next_agent: $next_agent,
    turns_taken: $turns_taken,
    status: "active",
    last_updated: $last_updated
  }' > "$THREAD_DIR/TURN.json"

echo "OK: Wrote TURN.json (next agent: $FIRST_TURN_AGENT)"
echo ""
echo "Thread '$THREAD_ID' is ready."
echo "  Directory: $THREAD_DIR"
echo "  Run: ./org/threads/orchestrator.sh --thread $THREAD_ID"
