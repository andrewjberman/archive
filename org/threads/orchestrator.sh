#!/usr/bin/env bash
# orchestrator.sh -- Round-robin agent conversation driver
#
# Usage:
#   ./org/threads/orchestrator.sh [options]
#
# Options:
#   --thread <id>       Run a specific thread (default: run all active threads)
#   --concurrency <n>   Max threads to run in parallel (default: 1)
#   --dry-run           Show what would be invoked without running
#   --verbose           Print agent prompts and responses to stdout

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
THREADS_DIR="$SCRIPT_DIR"
JQ="${REPO_ROOT}/.tools/jq.exe"

# --- Defaults ---
THREAD_ID=""
CONCURRENCY=1
DRY_RUN=false
VERBOSE=false

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --thread) THREAD_ID="$2"; shift 2 ;;
    --concurrency) CONCURRENCY="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --verbose) VERBOSE=true; shift ;;
    *) echo "ERROR: Unknown argument: $1"; exit 1 ;;
  esac
done

# --- resolve_agent() ---
resolve_agent() {
  local serial="$1"
  _ROLE_CODE=$(echo "$serial" | cut -d'_' -f2)

  local x=$(echo "$serial" | cut -d'.' -f1)
  local y=$(echo "$serial" | cut -d'.' -f2)
  local z=$(echo "$serial" | cut -d'.' -f3 | cut -d'_' -f1)

  if [ "$x" != "0" ]; then
    _TIER_FOLDER="tier1_exec"
  elif [ "$y" != "0" ]; then
    _TIER_FOLDER="tier2_senior"
  else
    _TIER_FOLDER="tier3_junior"
  fi

  _AGENT_DIR="$REPO_ROOT/org/$_TIER_FOLDER/$serial"
  _AGENT_PROMPT="$_AGENT_DIR/prompt.md"
  _AGENT_README="$_AGENT_DIR/README.md"

  case "$_ROLE_CODE" in
    SA) _BASE_PROMPT="$REPO_ROOT/org/ref/prompts/systems_architect.md" ;;
    DE) _BASE_PROMPT="$REPO_ROOT/org/ref/prompts/dashboard_engineer.md" ;;
    DT) _BASE_PROMPT="$REPO_ROOT/org/ref/prompts/devops_technician.md" ;;
    DS) _BASE_PROMPT="$REPO_ROOT/org/ref/prompts/data_scientist.md" ;;
    AE) _BASE_PROMPT="$REPO_ROOT/org/ref/prompts/aws_engineer.md" ;;
    RD) _BASE_PROMPT="$REPO_ROOT/org/ref/prompts/react_designer.md" ;;
    *)  _BASE_PROMPT="" ;;
  esac
}

# --- get_next_agent() ---
# For round_robin and alternating: deterministic from participant list and turn number
get_next_agent() {
  local thread_dir="$1"
  local turn_order=$("$JQ" -r '.turn_order' "$thread_dir/THREAD.json")
  local next=$("$JQ" -r '.next_agent' "$thread_dir/TURN.json")
  echo "$next"
}

# --- compute_next_after() ---
# Given the current agent and thread config, determine who goes next
compute_next_after() {
  local thread_dir="$1"
  local current_agent="$2"
  local turn_order=$("$JQ" -r '.turn_order' "$thread_dir/THREAD.json")
  local participants=$("$JQ" -r '.participants[]' "$thread_dir/THREAD.json")

  IFS=$'\n' read -rd '' -a PARTS <<< "$participants" || true

  local count=${#PARTS[@]}
  local current_idx=-1

  for ((i=0; i<count; i++)); do
    if [ "${PARTS[$i]}" = "$current_agent" ]; then
      current_idx=$i
      break
    fi
  done

  if [ "$turn_order" = "alternating" ] || [ "$turn_order" = "round_robin" ]; then
    local next_idx=$(( (current_idx + 1) % count ))
    echo "${PARTS[$next_idx]}"
  else
    # directed: default to next in sequence (agent can override via signal)
    local next_idx=$(( (current_idx + 1) % count ))
    echo "${PARTS[$next_idx]}"
  fi
}

# --- parse_signal() ---
# Extract signal from YAML frontmatter of a message file
parse_signal() {
  local msg_file="$1"
  # Read the frontmatter between --- markers
  local signal=$(sed -n '/^---$/,/^---$/{ /^signal:/s/^signal: *//p }' "$msg_file" | tr -d '[:space:]')
  echo "${signal:-continue}"
}

# --- check_convergence() ---
# Check if last two messages both signal converge
check_convergence() {
  local thread_dir="$1"
  local messages_dir="$thread_dir/messages"
  local msg_files=($(ls -1 "$messages_dir"/*.md 2>/dev/null | sort))
  local count=${#msg_files[@]}

  if [ "$count" -lt 2 ]; then
    echo "false"
    return
  fi

  local last_signal=$(parse_signal "${msg_files[$((count-1))]}")
  local prev_signal=$(parse_signal "${msg_files[$((count-2))]}")

  if [ "$last_signal" = "converge" ] && [ "$prev_signal" = "converge" ]; then
    echo "true"
  else
    echo "false"
  fi
}

# --- check_max_turns() ---
# Check if all agents have exhausted their max turns
check_max_turns() {
  local thread_dir="$1"
  local max_turns=$("$JQ" -r '.max_turns_per_agent' "$thread_dir/THREAD.json")
  local participants=$("$JQ" -r '.participants[]' "$thread_dir/THREAD.json")

  while IFS= read -r serial; do
    local taken=$("$JQ" -r --arg s "$serial" '.turns_taken[$s] // 0' "$thread_dir/TURN.json")
    if [ "$taken" -lt "$max_turns" ]; then
      echo "false"
      return
    fi
  done <<< "$participants"

  echo "true"
}

# --- build_system_prompt() ---
build_system_prompt() {
  local serial="$1"
  resolve_agent "$serial"

  local prompt=""

  # Base persona prompt
  if [ -n "$_BASE_PROMPT" ] && [ -f "$_BASE_PROMPT" ]; then
    prompt+="$(cat "$_BASE_PROMPT")"
    prompt+=$'\n\n'
  fi

  # Scoped agent prompt
  if [ -f "$_AGENT_PROMPT" ]; then
    prompt+="$(cat "$_AGENT_PROMPT")"
    prompt+=$'\n\n'
  fi

  echo "$prompt"
}

# --- build_user_prompt() ---
build_user_prompt() {
  local thread_dir="$1"
  local serial="$2"
  local turn_number="$3"
  local msg_number="$4"

  local topic=$("$JQ" -r '.topic' "$thread_dir/THREAD.json")
  local max_per_agent=$("$JQ" -r '.max_turns_per_agent' "$thread_dir/THREAD.json")
  local thread_id=$("$JQ" -r '.id' "$thread_dir/THREAD.json")
  local num_participants=$("$JQ" -r '.participants | length' "$thread_dir/THREAD.json")
  local max_total=$((max_per_agent * num_participants))
  local taken=$("$JQ" -r --arg s "$serial" '.turns_taken[$s] // 0' "$thread_dir/TURN.json")
  local remaining=$((max_per_agent - taken))

  resolve_agent "$serial"
  local role_name=""
  case "$_ROLE_CODE" in
    SA) role_name="Systems Architect" ;;
    DE) role_name="Dashboard Engineer" ;;
    DT) role_name="DevOps Technician" ;;
    DS) role_name="Data Scientist" ;;
    AE) role_name="AWS Engineer" ;;
    RD) role_name="React Designer" ;;
  esac

  local prompt=""

  # Turn instructions
  prompt+="## YOUR TURN -- Thread Protocol"
  prompt+=$'\n\n'
  prompt+="You are participating in a structured conversation thread."
  prompt+=$'\n\n'
  prompt+="**Your identity:** $serial ($role_name)"
  prompt+=$'\n'
  prompt+="**Thread topic:** $topic"
  prompt+=$'\n'
  prompt+="**Turn:** $turn_number of max $max_total"
  prompt+=$'\n'
  prompt+="**Your turns remaining:** $remaining"
  prompt+=$'\n\n'

  prompt+="### Instructions"
  prompt+=$'\n\n'
  prompt+="1. Read the CONTEXT section below -- this is your shared briefing material."
  prompt+=$'\n'
  prompt+="2. Read all previous messages in order."
  prompt+=$'\n'
  prompt+="3. Write your response to: org/threads/$thread_id/messages/$(printf '%03d' "$msg_number").md"
  prompt+=$'\n'
  prompt+="4. Use the message template (YAML frontmatter with agent, turn, timestamp, signal)."
  prompt+=$'\n'
  prompt+="5. Set your signal:"
  prompt+=$'\n'
  prompt+="   - \`continue\` -- you have more to discuss or questions remain"
  prompt+=$'\n'
  prompt+="   - \`converge\` -- you believe the conversation has reached resolution"
  prompt+=$'\n'
  prompt+="   - \`escalate\` -- you need human input (explain why in your message)"
  prompt+=$'\n\n'

  prompt+="### Constraints"
  prompt+=$'\n'
  prompt+="- Stay in your role. Do not impersonate other agents."
  prompt+=$'\n'
  prompt+="- Do not modify THREAD.json, TURN.json, CONTEXT.json, or other agents' messages."
  prompt+=$'\n'
  prompt+="- Only write your own message file."
  prompt+=$'\n'
  prompt+="- Reference context documents by their label (e.g., \"per the Architecture Spec...\")."
  prompt+=$'\n'
  prompt+="- Be concrete. Name files, functions, resource names. Avoid vague summaries."
  prompt+=$'\n'

  if [ "$remaining" -le 1 ]; then
    prompt+="- **THIS IS YOUR LAST TURN. Your signal MUST be \`converge\` (forced convergence).**"
    prompt+=$'\n'
  fi

  prompt+=$'\n'

  # CONTEXT_COMPILED.md
  prompt+="---"
  prompt+=$'\n\n'
  prompt+="## CONTEXT"
  prompt+=$'\n\n'
  if [ -f "$thread_dir/CONTEXT_COMPILED.md" ]; then
    prompt+="$(cat "$thread_dir/CONTEXT_COMPILED.md")"
    prompt+=$'\n\n'
  fi

  # Previous messages
  prompt+="---"
  prompt+=$'\n\n'
  prompt+="## PREVIOUS MESSAGES"
  prompt+=$'\n\n'

  local msg_files=($(ls -1 "$thread_dir/messages"/*.md 2>/dev/null | sort))
  if [ ${#msg_files[@]} -eq 0 ]; then
    prompt+="(No previous messages)"
    prompt+=$'\n'
  else
    for mf in "${msg_files[@]}"; do
      prompt+="### Message: $(basename "$mf")"
      prompt+=$'\n\n'
      prompt+="$(cat "$mf")"
      prompt+=$'\n\n'
    done
  fi

  echo "$prompt"
}

# --- write_receipts() ---
# Compile thread into receipt files for each participant
write_receipts() {
  local thread_dir="$1"
  local thread_id=$("$JQ" -r '.id' "$thread_dir/THREAD.json")
  local topic=$("$JQ" -r '.topic' "$thread_dir/THREAD.json")
  local status=$("$JQ" -r '.status' "$thread_dir/THREAD.json")
  local created_by=$("$JQ" -r '.created_by' "$thread_dir/THREAD.json")
  local created_at=$("$JQ" -r '.created_at' "$thread_dir/THREAD.json")
  local participants=$("$JQ" -r '.participants[]' "$thread_dir/THREAD.json")

  IFS=$'\n' read -rd '' -a PARTS <<< "$participants" || true

  # Extract date from thread ID (first 10 chars = YYYY-MM-DD)
  local date_prefix="${thread_id:0:10}"
  # Extract slug (everything after YYYY-MM-DD-)
  local slug="${thread_id:11}"

  # Build receipt content
  local receipt=""
  receipt+="# Thread Receipt: $topic"
  receipt+=$'\n\n'
  receipt+="**Thread ID:** $thread_id"
  receipt+=$'\n'
  receipt+="**Created by:** $created_by"
  receipt+=$'\n'
  receipt+="**Created at:** $created_at"
  receipt+=$'\n'
  receipt+="**Status:** $status"
  receipt+=$'\n'
  receipt+="**Participants:** $(IFS=', '; echo "${PARTS[*]}")"
  receipt+=$'\n\n'
  receipt+="---"
  receipt+=$'\n\n'

  # Append all messages
  local msg_files=($(ls -1 "$thread_dir/messages"/*.md 2>/dev/null | sort))
  for mf in "${msg_files[@]}"; do
    receipt+="## $(basename "$mf")"
    receipt+=$'\n\n'
    receipt+="$(cat "$mf")"
    receipt+=$'\n\n'
    receipt+="---"
    receipt+=$'\n\n'
  done

  # Write receipt to each participant's threads/ folder
  for serial in "${PARTS[@]}"; do
    resolve_agent "$serial"

    # Build other_serials (all participants except current)
    local others=()
    for other in "${PARTS[@]}"; do
      if [ "$other" != "$serial" ]; then
        others+=("$other")
      fi
    done
    local others_str=$(IFS='+'; echo "${others[*]}")

    local receipt_file="$_AGENT_DIR/threads/${date_prefix}_${others_str}_${slug}.md"
    echo "$receipt" > "$receipt_file"
    echo "OK: Receipt written to $receipt_file"
  done
}

# --- run_thread() ---
# Execute one thread to completion (or until blocked/escalated)
run_thread() {
  local thread_dir="$1"
  local thread_id=$("$JQ" -r '.id' "$thread_dir/THREAD.json")
  local status=$("$JQ" -r '.status' "$thread_dir/THREAD.json")

  if [ "$status" != "active" ]; then
    echo "SKIP: Thread '$thread_id' is not active (status: $status)"
    return 0
  fi

  echo ""
  echo "========================================"
  echo "THREAD: $thread_id"
  echo "========================================"
  echo ""

  while true; do
    # Re-read state each iteration
    status=$("$JQ" -r '.status' "$thread_dir/TURN.json")
    if [ "$status" != "active" ]; then
      echo "HALT: Thread status is '$status'"
      break
    fi

    # Check max turns
    if [ "$(check_max_turns "$thread_dir")" = "true" ]; then
      echo "COMPLETE: All agents have exhausted their max turns"
      "$JQ" '.status = "complete"' "$thread_dir/THREAD.json" > "$thread_dir/THREAD.json.tmp" && mv "$thread_dir/THREAD.json.tmp" "$thread_dir/THREAD.json"
      "$JQ" '.status = "complete"' "$thread_dir/TURN.json" > "$thread_dir/TURN.json.tmp" && mv "$thread_dir/TURN.json.tmp" "$thread_dir/TURN.json"
      write_receipts "$thread_dir"
      break
    fi

    # Check convergence
    if [ "$(check_convergence "$thread_dir")" = "true" ]; then
      echo "COMPLETE: Both agents signaled converge"
      "$JQ" '.status = "complete"' "$thread_dir/THREAD.json" > "$thread_dir/THREAD.json.tmp" && mv "$thread_dir/THREAD.json.tmp" "$thread_dir/THREAD.json"
      "$JQ" '.status = "complete"' "$thread_dir/TURN.json" > "$thread_dir/TURN.json.tmp" && mv "$thread_dir/TURN.json.tmp" "$thread_dir/TURN.json"
      write_receipts "$thread_dir"
      break
    fi

    # Determine current agent
    local current_agent=$(get_next_agent "$thread_dir")
    local turn_number=$("$JQ" -r '.turn_number' "$thread_dir/TURN.json")
    local msg_number=$turn_number

    echo "TURN $turn_number: Agent $current_agent"

    # Check if this agent has turns remaining
    local max_per=$("$JQ" -r '.max_turns_per_agent' "$thread_dir/THREAD.json")
    local taken=$("$JQ" -r --arg s "$current_agent" '.turns_taken[$s] // 0' "$thread_dir/TURN.json")
    if [ "$taken" -ge "$max_per" ]; then
      echo "SKIP: Agent $current_agent has exhausted their turns ($taken/$max_per)"
      # Move to next agent
      local next=$(compute_next_after "$thread_dir" "$current_agent")
      "$JQ" --arg a "$next" '.next_agent = $a' "$thread_dir/TURN.json" > "$thread_dir/TURN.json.tmp" && mv "$thread_dir/TURN.json.tmp" "$thread_dir/TURN.json"
      continue
    fi

    # Build prompts
    local system_prompt=$(build_system_prompt "$current_agent")
    local user_prompt=$(build_user_prompt "$thread_dir" "$current_agent" "$turn_number" "$msg_number")

    local msg_file="$thread_dir/messages/$(printf '%03d' "$msg_number").md"

    if [ "$DRY_RUN" = "true" ]; then
      echo "DRY RUN: Would invoke claude for agent $current_agent"
      echo "  System prompt length: $(echo "$system_prompt" | wc -c) chars"
      echo "  User prompt length: $(echo "$user_prompt" | wc -c) chars"
      echo "  Expected output: $msg_file"

      if [ "$VERBOSE" = "true" ]; then
        echo ""
        echo "--- SYSTEM PROMPT (first 500 chars) ---"
        echo "$system_prompt" | head -c 500
        echo ""
        echo "--- USER PROMPT (first 1000 chars) ---"
        echo "$user_prompt" | head -c 1000
        echo ""
      fi

      break
    fi

    # Write prompts to temp files (avoid shell quoting issues with large prompts)
    local sys_tmp=$(mktemp)
    local usr_tmp=$(mktemp)
    echo "$system_prompt" > "$sys_tmp"
    echo "$user_prompt" > "$usr_tmp"

    if [ "$VERBOSE" = "true" ]; then
      echo "--- Invoking claude for $current_agent ---"
    fi

    # Invoke claude
    claude -p "$(cat "$usr_tmp")" \
      --system-prompt "$(cat "$sys_tmp")" \
      --allowedTools "Read,Write,Edit,Glob,Grep" \
      --output-format text \
      --print 2>/dev/null || true

    rm -f "$sys_tmp" "$usr_tmp"

    # Validate message was written
    if [ ! -f "$msg_file" ]; then
      echo "ERROR: Agent $current_agent did not write expected message: $msg_file"
      echo "HALT: Thread requires manual intervention"
      "$JQ" '.status = "blocked"' "$thread_dir/TURN.json" > "$thread_dir/TURN.json.tmp" && mv "$thread_dir/TURN.json.tmp" "$thread_dir/TURN.json"
      "$JQ" '.status = "blocked"' "$thread_dir/THREAD.json" > "$thread_dir/THREAD.json.tmp" && mv "$thread_dir/THREAD.json.tmp" "$thread_dir/THREAD.json"
      break
    fi

    if [ "$VERBOSE" = "true" ]; then
      echo ""
      echo "--- Message from $current_agent ---"
      cat "$msg_file"
      echo ""
      echo "--- End message ---"
      echo ""
    fi

    # Parse signal
    local signal=$(parse_signal "$msg_file")
    echo "  Signal: $signal"

    # Handle escalate
    if [ "$signal" = "escalate" ]; then
      echo "ESCALATE: Agent $current_agent requests human input"
      "$JQ" '.status = "needs_human"' "$thread_dir/TURN.json" > "$thread_dir/TURN.json.tmp" && mv "$thread_dir/TURN.json.tmp" "$thread_dir/TURN.json"
      "$JQ" '.status = "needs_human"' "$thread_dir/THREAD.json" > "$thread_dir/THREAD.json.tmp" && mv "$thread_dir/THREAD.json.tmp" "$thread_dir/THREAD.json"
      break
    fi

    # Update TURN.json
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local new_taken=$((taken + 1))
    local next_turn=$((turn_number + 1))
    local next_agent=$(compute_next_after "$thread_dir" "$current_agent")

    "$JQ" \
      --argjson tn "$next_turn" \
      --arg na "$next_agent" \
      --arg s "$current_agent" \
      --argjson nt "$new_taken" \
      --arg lu "$now" \
      '.turn_number = $tn | .next_agent = $na | .turns_taken[$s] = $nt | .last_updated = $lu' \
      "$thread_dir/TURN.json" > "$thread_dir/TURN.json.tmp" && mv "$thread_dir/TURN.json.tmp" "$thread_dir/TURN.json"

    echo "  Next: $next_agent (turn $next_turn)"
    echo ""
  done
}

# --- Main ---

# Collect threads to run
THREAD_DIRS=()

if [ -n "$THREAD_ID" ]; then
  TD="$THREADS_DIR/$THREAD_ID"
  if [ ! -d "$TD" ] || [ ! -f "$TD/THREAD.json" ]; then
    echo "ERROR: Thread not found: $TD"
    exit 1
  fi
  THREAD_DIRS+=("$TD")
else
  # Find all active threads
  for td in "$THREADS_DIR"/*/THREAD.json; do
    [ -f "$td" ] || continue
    dir=$(dirname "$td")
    s=$("$JQ" -r '.status' "$td")
    if [ "$s" = "active" ]; then
      THREAD_DIRS+=("$dir")
    fi
  done

  if [ ${#THREAD_DIRS[@]} -eq 0 ]; then
    echo "No active threads found."
    exit 0
  fi

  echo "Found ${#THREAD_DIRS[@]} active thread(s)"
fi

# Run threads
if [ "$CONCURRENCY" -le 1 ] || [ ${#THREAD_DIRS[@]} -le 1 ]; then
  # Sequential
  for td in "${THREAD_DIRS[@]}"; do
    run_thread "$td"
  done
else
  # Parallel
  PIDS=()
  RUNNING=0

  for td in "${THREAD_DIRS[@]}"; do
    if [ "$RUNNING" -ge "$CONCURRENCY" ]; then
      # Wait for one to finish
      wait -n
      RUNNING=$((RUNNING - 1))
    fi

    run_thread "$td" &
    PIDS+=($!)
    RUNNING=$((RUNNING + 1))
  done

  # Wait for all remaining
  for pid in "${PIDS[@]}"; do
    wait "$pid" || true
  done
fi

echo ""
echo "Orchestrator complete."
