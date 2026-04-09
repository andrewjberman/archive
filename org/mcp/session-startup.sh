#!/usr/bin/env bash
# session-startup.sh — PostToolUse hook for register_agent
#
# Triggered automatically after any agent calls register_agent via MCP.
# Reads the hook JSON payload from stdin, extracts agent_serial,
# and launches agent-poller.py in background.
#
# NOTE: inbox-watch.sh is NOT launched here. It must be launched by the
# agent via Bash(run_in_background: true) so that Claude Code manages
# the process and fires a <task-notification> when a message arrives.
# Async hooks run as detached OS processes -- their exit is invisible
# to the conversation.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
JQ="$SCRIPT_DIR/../../.tools/jq.exe"

# Read JSON payload from stdin
HOOK_JSON="$(cat)"

# Extract agent_serial from tool_input
SERIAL="$("$JQ" -r '.tool_input.agent_serial // empty' <<< "$HOOK_JSON")"

if [ -z "$SERIAL" ]; then
    exit 0
fi

# Guard: don't double-launch if poller is already running for this serial
if tasklist 2>/dev/null | grep -q "python" && \
   wmic process where "name='python.exe'" get commandline 2>/dev/null | grep -q "agent-poller.py $SERIAL"; then
    exit 0
fi

# Launch heartbeat poller (background, detached)
python "$SCRIPT_DIR/agent-poller.py" "$SERIAL" &

echo "OK: session-startup launched poller for $SERIAL (inbox-watch must be launched in-conversation)"
