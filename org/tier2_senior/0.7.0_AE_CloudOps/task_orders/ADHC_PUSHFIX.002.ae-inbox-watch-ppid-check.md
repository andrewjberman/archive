<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_PUSHFIX.002</id>
    <project>ADHC_PUSHFIX</project>
    <title>inbox-watch.sh PPID-liveness check — defense-in-depth against orphan watchers</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_PUSHFIX.md</ref>
    <ref type="prd_section">§4.2 Phase 2: inbox-watch.sh PPID-liveness check</ref>
    <ref type="target_file">org/mcp/inbox-watch.sh</ref>
    <ref type="target_lines">L27-42 (single-watcher guard)</ref>
    <ref type="predecessor">ADHC_BASHFIX.002 (045296b18) — hardened single-watcher guard; this TO extends that guard</ref>
  </references>

  <context>
    The current single-watcher guard (L27-42, shipped ADHC_BASHFIX.002 `045296b18`) detects
    existing inbox-watch.sh PIDs for the same serial and exits. It does NOT distinguish:
      - Live parent (genuine duplicate: PPID is an alive process) → should exit (correct today)
      - Orphan parent (PPID == 1 or PPID is dead) → should kill + proceed (does not happen today)

    PPID=1 orphans accumulate because Bash-tool wrappers die on session cleanup while the inner
    `bash inbox-watch.sh` survives. ADHC_PUSHFIX.001 handles the root cause (auto-cleanup at
    startup). This TO adds defense-in-depth so the watcher self-heals even if Phase 1 runs late
    or misses an edge case.

    PRD §4.2 specifies the exact logic (reproduced in scope below).
  </context>

  <scope>
    Modify org/mcp/inbox-watch.sh L27-42 to add PPID-liveness check.

    After the guard detects existing PIDs in $existing, loop through each PID and check its
    parent process:

    EXACT IMPLEMENTATION (from PRD §4.2):
    ---
    for pid in $existing; do
        ppid=$(ps -p "$pid" -o ppid= 2>/dev/null | tr -d ' ')
        if [ -z "$ppid" ] || [ "$ppid" -eq 1 ] || ! kill -0 "$ppid" 2>/dev/null; then
            # Orphan: PPID is 1 (init) or PPID is dead
            echo "inbox-watch: reaping orphan watcher pid $pid (parent dead)" >&gt;&amp;2
            kill "$pid" 2>/dev/null || true
            # Continue checking other PIDs
        else
            # Live parent: genuine duplicate launch from a sibling session
            echo "inbox-watch already running for $SERIAL (pid $pid, parent $ppid alive). Exiting." >&gt;&amp;2
            exit 0
        fi
    done
    # Falls through to launch poll loop (orphans reaped, no live duplicate)
    ---

    Replace the current "if [ -n '$existing' ]; then echo ... exit 0; fi" block at L39-42
    with the loop above. The loop preserves the original single-watcher guarantee while
    adding orphan-reaping.

    Compatibility note: ps -p $pid -o ppid= is Git Bash 3.6.7 compatible (standard ps
    fields). kill -0 $ppid is universal.
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="before write — inspection">
      <step>
        <run>sed -n '27,55p' org/mcp/inbox-watch.sh</run>
        <expect>Single-watcher guard at L27-42 checks $existing, exits if non-empty.
        No PPID check present. pgrep + ps fallback for Git Bash 3.6.7.</expect>
        <if_mismatch>STOP. If the guard structure differs from expected (e.g. different line numbers,
        already has PPID logic), surface to COO before editing.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="before write">
      <step>
        <run>N/A — no comp-* tool covers shell-script MCP internals. Documented as out-of-scope
        per ADHC_PUSHFIX PRD §5.1 and ADHC_COMPIL.003 §5.3 protocol.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash -n org/mcp/inbox-watch.sh</run>
        <expect>Exit 0. No syntax errors.</expect>
        <if_mismatch>STOP. Fix bash syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>grep -n "ppid" org/mcp/inbox-watch.sh | head -10</run>
        <expect>PPID check present: lines matching ps -p ... -o ppid= and kill -0 pattern.
        At minimum 2-3 lines with ppid variable.</expect>
        <if_mismatch>STOP. PPID check was not inserted correctly.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>N/A — no comp-blast surface for shell scripts.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      inbox-watch.sh launched when one or more orphan PIDs (PPID=1) exist for the same
      serial: orphans are killed via kill &lt;pid&gt;, stderr logs
      "inbox-watch: reaping orphan watcher pid NNN (parent dead)", watcher proceeds to
      launch its own poll loop. Evidence: test run output in session log.
    </criterion>
    <criterion id="2">
      inbox-watch.sh launched when a live-parent watcher is already running (PPID is alive
      non-1): script exits 0 with message
      "inbox-watch already running for SERIAL (pid NNN, parent PPP alive). Exiting."
      Evidence: test run output in session log.
    </criterion>
    <criterion id="3">
      Mixed case (multiple PIDs, some orphan + one live-parent): all orphans are killed,
      then exit on the live-parent. Evidence: constructed test or description of expected
      behavior in session log.
    </criterion>
    <criterion id="4">
      PPID lookup failure (transient ps error): graceful fallback to current behavior
      (exit on detection). Evidence: code review in session log showing the
      [ -z "$ppid" ] fallback path.
    </criterion>
    <criterion id="5">
      Two-launch self-test passes (ADHC_BASHFIX.002 acceptance pattern): launch
      inbox-watch twice in same session via Bash tool. Second launch detects first as
      live-parent and exits cleanly. Evidence: two Bash tool invocations + outputs
      in session log.
    </criterion>
    <criterion id="6">
      bash -n org/mcp/inbox-watch.sh exits 0 (no syntax errors). Evidence: command
      output in session log.
    </criterion>
    <criterion id="7">
      Session log includes Compiler Tools section reproducing every phase-0+2 check
      with observed output and explicit pass/fail vs expect. Missing rows = REWORK.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="none"/>
    Parallelizable with ADHC_PUSHFIX.001. Different files, no dependency.
  </dependencies>

  <cross_domain_coordination>
    <none/>
    org/mcp/inbox-watch.sh is owned by 0.7.0_AE_CloudOps (MCP infrastructure).
    No other agents are modifying this file concurrently.
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" \
      -m "fix(ADHC_PUSHFIX.002): inbox-watch.sh PPID liveness check — reap orphan watchers" \
      -- org/mcp/inbox-watch.sh
  </commit_identity>

  <notes>
    No git tag required. This is workspace MCP tooling, not a pipeline.
    Implementation spec is exact per PRD §4.2 — no design decisions needed.
    The guard extension is ~10 lines replacing the 4-line current exit block.
    ADHC_BASHFIX.002 shipped today (045296b18) is the predecessor this extends.
  </notes>
</task_order>
