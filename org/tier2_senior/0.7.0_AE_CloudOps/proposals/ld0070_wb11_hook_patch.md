# LD-0070 WB-1.1 hook patch — session-id-keyed serial resolution
**Status:** PROPOSAL — pre-positioned per ws CTO routing-verdict (c) of `[AUDIT-ABSORBED + ROUTING-VERDICT]` MCP 2026-05-26T~01:18Z
**Authority:** TELEMETRY_LIVENESS_FRAMEWORK.md v0.2 `4a0bb72d6` §7.2 + §7.4 (session-id-keyed pattern PRIMARY + fallback chain)
**Author:** 0.7.0_AE_CloudOps
**Date:** 2026-05-26
**Application gate:** MSTR ratification of LD-0070 WS-A spec + ws CVO independent review + ws CTO approves THIS patch shape pre-commit
**On gate-clear:** apply diff to `.tools/hooks/post-tool-telemetry.sh`; commit under AE author; CC ws CTO + ws COO on ship MCP

---

## §1 — Patch scope

Adds the session-id-keyed serial resolution as PRIMARY source per v0.2 §7.2. Preserves the legacy fallback chain transitionally. Adds `serial_source` tag to JSONL output. Adds fail-loud-to-audit-trail WARN entry when fallback used.

**Does NOT in this patch:**
- Wire `broker_record_tool_call` hot-path (WB-2; depends on broker code amendment landing)
- Change JSONL shape beyond adding `serial_source` field (preserves field names for dual-read compat per ws CTO §2 routing)
- Refine 2-class → 3-class kind taxonomy (WB-3 semantic refinement)
- Add `bg_task` lifecycle entries (WB-4; depends on Claude Code lifecycle hook coverage check)
- Modify `org/XXX.md` Step 1b session-start ritual (separate companion change; see §4 below)

Stays tightly scoped to §3.5 CRITICAL fix.

---

## §2 — File-level diff (`.tools/hooks/post-tool-telemetry.sh`)

```diff
@@ -1,11 +1,14 @@
 #!/usr/bin/env bash
 # post-tool-telemetry.sh -- Claude Code PostToolUse hook for agent telemetry.
 #
 # Ported from corporeal mcp_runner/hooks/post_tool_use.sh (2026-05-20).
-# Adapted to the ajb_workspace: serial is resolved from the workspace-native
-# .comp-graph/.agent_context file (written by org/XXX.md startup Step 1 E)
-# rather than corporeal's CORPOREAL_AGENT_SERIAL env var. An OPAL_AGENT_SERIAL
-# env var, if set, takes precedence (per-process attribution survives a shared
-# working directory).
+# Adapted to the ajb_workspace per LD-0070 WS-B §7.2 (TELEMETRY_LIVENESS_FRAMEWORK.md
+# v0.2): serial is resolved via SESSION-ID-KEYED FILE as PRIMARY source -- the
+# org/mcp/sessions/{session_id}.serial file written by org/XXX.md Step 1b on
+# session start. This is per-session deterministic + tilde-lane-safe + survives
+# broker outage. Legacy chain ($OPAL_AGENT_SERIAL env / .comp-graph/.agent_context)
+# preserved transitionally as fallback for sessions that haven't completed the
+# Step 1b ritual yet. Fallback usage flagged via `serial_source` JSONL field +
+# WARN entry to org/mcp/hook_errors.log per §3.6.
 #
 # Reads the hook event JSON from stdin, extracts tool_name, and appends a JSONL
 # record to a per-agent telemetry file under org/mcp/agent_telemetry/.
@@ -34,12 +37,44 @@ TELEMETRY_DIR="$REPO_ROOT/org/mcp/agent_telemetry"
 mkdir -p "$TELEMETRY_DIR" 2>/dev/null
 
-# Resolve agent serial: OPAL_AGENT_SERIAL env var wins; else the workspace-native
-# .comp-graph/.agent_context SERIAL= line; else _unknown (debugging signal).
-AGENT="${OPAL_AGENT_SERIAL:-}"
-if [ -z "$AGENT" ] && [ -f "$REPO_ROOT/.comp-graph/.agent_context" ]; then
-    AGENT=$(grep -m1 '^SERIAL=' "$REPO_ROOT/.comp-graph/.agent_context" 2>/dev/null | cut -d= -f2- | tr -d '\r' || echo "")
-fi
-AGENT="${AGENT:-_unknown}"
+# Read hook context from stdin EARLY -- need session_id for primary resolution.
+HOOK_INPUT="$(cat)"
+SESSION_ID=$(printf '%s' "$HOOK_INPUT" | jq -r '.session_id // ""' 2>/dev/null || echo "")
+TOOL=$(printf '%s' "$HOOK_INPUT" | jq -r '.tool_name // "?"' 2>/dev/null || echo "?")
+
+# Resolve agent serial per LD-0070 §7 fallback chain (priority order):
+#   1. session-id-keyed file at org/mcp/sessions/{session_id}.serial (PRIMARY)
+#   2. OPAL_AGENT_SERIAL env var
+#   3. .comp-graph/.agent_context SERIAL= line (legacy fallback)
+#   4. _unknown_lane_check_needed literal (fail-loud sentinel)
+SESSIONS_DIR="$REPO_ROOT/org/mcp/sessions"
+AGENT=""
+SERIAL_SOURCE=""
+
+if [ -n "$SESSION_ID" ] && [ -f "$SESSIONS_DIR/${SESSION_ID}.serial" ]; then
+    AGENT=$(head -1 "$SESSIONS_DIR/${SESSION_ID}.serial" 2>/dev/null | tr -d '\r\n')
+    SERIAL_SOURCE="session-keyed"
+fi
+
+if [ -z "$AGENT" ] && [ -n "${OPAL_AGENT_SERIAL:-}" ]; then
+    AGENT="$OPAL_AGENT_SERIAL"
+    SERIAL_SOURCE="env"
+fi
+
+if [ -z "$AGENT" ] && [ -f "$REPO_ROOT/.comp-graph/.agent_context" ]; then
+    AGENT=$(grep -m1 '^SERIAL=' "$REPO_ROOT/.comp-graph/.agent_context" 2>/dev/null | cut -d= -f2- | tr -d '\r' || echo "")
+    [ -n "$AGENT" ] && SERIAL_SOURCE="comp-graph-fallback"
+fi
+
+if [ -z "$AGENT" ]; then
+    AGENT="_unknown_lane_check_needed"
+    SERIAL_SOURCE="unresolved"
+fi
+
+# Fail-loud-to-audit-trail per §3.6 + §7.4: any fallback use logs WARN.
+if [ "$SERIAL_SOURCE" != "session-keyed" ] && [ "$AGENT" != "_unknown" ]; then
+    HOOK_ERRORS_LOG="$REPO_ROOT/org/mcp/hook_errors.log"
+    printf '{"ts":"%s","level":"WARN","session_id":"%s","fallback_source":"%s","serial_resolved":"%s","reason":"session-keyed file missing"}\n' \
+        "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$SESSION_ID" "$SERIAL_SOURCE" "$AGENT" >> "$HOOK_ERRORS_LOG" 2>/dev/null
+fi
 
 # Sanitize serial for use as a filename (tilde lanes -> safe chars).
 SAFE_AGENT=$(printf '%s' "$AGENT" | tr '/~ ' '___')
 TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
 
-# Read hook context from stdin. Extract tool_name + session_id; fall back to "?".
-HOOK_INPUT="$(cat)"
-TOOL=$(printf '%s' "$HOOK_INPUT" | jq -r '.tool_name // "?"' 2>/dev/null || echo "?")
-SESSION_ID=$(printf '%s' "$HOOK_INPUT" | jq -r '.session_id // "?"' 2>/dev/null || echo "?")
+# (HOOK_INPUT + TOOL + SESSION_ID already read above for serial resolution.)
 
 # Classify kind: loop (supervisor/infrastructure self-ping) vs work (real action).
 # Default work; flip to loop on known infrastructure patterns. Keep patterns tight.
@@ -74,8 +109,8 @@ esac
 # Append JSONL line. A single <4KB write is atomic per POSIX; per-agent files
 # (one per serial) have no cross-agent contention. Trailing newline is REQUIRED.
-LINE=$(printf '{"ts":"%s","agent":"%s","tool":"%s","kind":"%s","session_id":"%s"}' \
-  "$TS" "$AGENT" "$TOOL" "$KIND" "$SESSION_ID")
+LINE=$(printf '{"ts":"%s","agent":"%s","tool":"%s","kind":"%s","session_id":"%s","serial_source":"%s"}' \
+  "$TS" "$AGENT" "$TOOL" "$KIND" "$SESSION_ID" "$SERIAL_SOURCE")
 printf '%s\n' "$LINE" >> "$TELEMETRY_DIR/$SAFE_AGENT.jsonl" 2>/dev/null
 
 # Always exit 0 -- never disrupt the agent on hook failure.
 exit 0
```

---

## §3 — Behavior tests (manual smoke after WB-1 ratify)

Once applied, verify with synthetic tool calls from each lane state:

| Test | Setup | Expected |
|---|---|---|
| Base session, session-keyed file present | `mkdir -p org/mcp/sessions; echo "0.7.0_AE_CloudOps" > org/mcp/sessions/${CLAUDE_CODE_SESSION_ID}.serial` then fire any tool call | JSONL entry has `serial_source: "session-keyed"` + agent `0.7.0_AE_CloudOps`; no hook_errors.log entry |
| Tilde lane, session-keyed file present | `~B` session writes own session file with `0.X.0_..~B`; fires any tool call | JSONL entry has correct `~B` suffix; no leak to base-serial file |
| Session-keyed file MISSING, env set | `rm org/mcp/sessions/${CLAUDE_CODE_SESSION_ID}.serial; export OPAL_AGENT_SERIAL=test_agent; fire tool` | JSONL entry has `serial_source: "env"` + agent `test_agent`; WARN entry in `org/mcp/hook_errors.log` |
| Session-keyed file MISSING, no env, .comp-graph present | (default state for legacy sessions) | JSONL entry has `serial_source: "comp-graph-fallback"`; WARN entry in `org/mcp/hook_errors.log` |
| All sources missing | (catastrophic) | JSONL entry has `serial_source: "unresolved"` + agent `_unknown_lane_check_needed`; WARN entry |

---

## §4 — Companion change to `org/XXX.md` Step 1b (separate patch)

The session-id-keyed pattern requires `org/XXX.md` Step 1b to write the session file at session start. Companion change:

```diff
@@ Step 1b - MCP Startup @@
 **A. Register — use your FULL serial, including ~suffix:**
 ```python
 register_agent("{your_serial}", summary="Starting session")
 ```
 Makes you visible. Starts broker. Enables message push. Also auto-launches `agent-poller.py`.
+
+**A.1 — Write session-id-keyed serial file (LD-0070 §7.2):**
+```bash
+mkdir -p org/mcp/sessions
+# CLAUDE_CODE_SESSION_ID is set per-session by Claude Code (empirically verified by ws CTO 2026-05-26).
+# The PostToolUse hook will fall back to env/.comp-graph chain with WARN entry.
+if [ -n "${CLAUDE_CODE_SESSION_ID:-}" ]; then
+    echo "{your_full_suffixed_serial}" > "org/mcp/sessions/${CLAUDE_CODE_SESSION_ID}.serial"
+fi
+```
+This enables the PostToolUse hook to resolve serial via session-id-keyed file (per-session deterministic, tilde-lane-safe, broker-outage-resilient).
```

**ENV VAR NAME RESOLVED (2026-05-26 by ws CTO empirical verification per MCP `20260526T~0130Z`):** Claude Code DOES export the session ID at shell level — variable name is **`$CLAUDE_CODE_SESSION_ID`** (with the `_CODE_` infix; NOT `$CLAUDE_SESSION_ID`). Value matches the `session_id` field in PostToolUse hook stdin (confirmed identical UUID). The Step 1b ritual above works directly with no back-fill complexity needed. Locally verified in AE 0.7 session 2026-05-26: `CLAUDE_CODE_SESSION_ID=deac8e65-c5a9-4c2a-bd91-dacf55b4d0d8`. Spec v0.3 `566647bfd` §7.2 anchors this empirical name explicitly for future implementers.

---

## §5 — Gitignore companion (separate small change)

Add `org/mcp/sessions/*.serial` to `.gitignore` — session-state files are per-machine ephemeral, not source-of-truth. GC sweep removes them at 24h post-last-activity per spec §7.4.

```diff
+# LD-0070 session-id-keyed serial files (per-session ephemeral; GC'd 24h post-activity)
+org/mcp/sessions/*.serial
```

---

## §6 — Application sequence (post WB-1 ratify)

1. MSTR ratifies LD-0070 spec v0.2 (or v0.3 if further refinements land)
2. ws CVO independent review passes
3. ws CTO approves THIS patch shape (post-§7.2 confirmation that session-id-keyed is the path)
4. AE 0.7 applies the §2 diff to `.tools/hooks/post-tool-telemetry.sh`
5. AE 0.7 commits with author `0.7.0_AE_CloudOps`; .gitignore companion in same commit
6. AE 0.7 separately surfaces companion `org/XXX.md` Step 1b change to ws CTO (org/XXX.md edits are in CTO lane)
7. AE 0.7 runs §3 behavior smoke tests + MCPs ws CTO + ws COO with results
8. Phase 1 dual-read observation begins per spec §5.1

---

## §7 — Cross-references

- `docs/architecture/TELEMETRY_LIVENESS_FRAMEWORK.md` v0.2 `4a0bb72d6` §7
- `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-05-26/ld0070_postpostuse_hook_audit.md` (the audit findings)
- `.tools/hooks/post-tool-telemetry.sh` (current implementation; target file)
- `.claude/settings.local.json` (PostToolUse hook config; no change to this file required for WB-1.1)
- `org/mcp/INBOX_WATCH_DESIGN.md` (companion fabric infra)

---

## §8 — Sign-off lane

- ws CTO ratify on this patch shape: STANDING
- MSTR ratify on LD-0070 WS-A spec v0.2: STANDING (upstream gate)
- ws CVO independent review on LD-0070 WS-A spec v0.2: STANDING (upstream gate)
- AE 0.7 application + smoke test: BLOCKED on the three above

Once all three clear, application is ~30min wall (apply diff + commit + smoke test + RAVC2-Request to ws COO).
