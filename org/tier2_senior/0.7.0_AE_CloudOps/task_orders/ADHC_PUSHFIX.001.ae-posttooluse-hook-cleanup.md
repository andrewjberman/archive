<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_PUSHFIX.001</id>
    <project>ADHC_PUSHFIX</project>
    <title>PostToolUse hook auto-runs kill-orphans --stale --force after register_agent</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>30-60 min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_PUSHFIX.md</ref>
    <ref type="prd_section">§4.1 Phase 1: PostToolUse hook auto-cleanup</ref>
    <ref type="current_hook">.claude/settings.local.json (PostToolUse.register_agent)</ref>
    <ref type="tool">.tools/kill-orphans (existing tool, --stale --force mode)</ref>
  </references>

  <context>
    Workspace-global inbox-watch orphan accumulation bug: prior-session watchers survive with
    PPID=1 after Bash-tool wrappers die on session cleanup. The single-watcher guard in
    inbox-watch.sh detects these orphans and exits, leaving the new session deaf to real-time
    inbox pushes. kill-orphans --stale --force already exists and does the right cleanup; it
    just has no auto-trigger. This TO wires the auto-trigger.

    Current hook state (.claude/settings.local.json PostToolUse):
      matcher: mcp__opal-agent-comms__register_agent
      command: python org/mcp/hook_launch_poller.py (async: true)

    Required change: add kill-orphans --stale --force to the same hook, running after (or
    in parallel with) the existing poller launch. Order does not matter; both are safe to run
    concurrently. AE picks the cleanest insertion: second command in the hooks array, or a
    wrapper script that runs both.
  </context>

  <scope>
    Modify .claude/settings.local.json to add kill-orphans --stale --force to the
    PostToolUse hook for mcp__opal-agent-comms__register_agent. The tool must run
    AFTER register_agent returns successfully (hook fires post-tool-use).

    The kill-orphans call must be non-blocking and must not fail the hook on tool error
    (exit 0 regardless of kill-orphans result).
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="before write — inspection">
      <step>
        <run>cat .claude/settings.local.json | python3 -c "import json,sys; h=json.load(sys.stdin)['hooks']['PostToolUse']; print(json.dumps(h, indent=2))"</run>
        <expect>Single matcher for mcp__opal-agent-comms__register_agent with one command: python org/mcp/hook_launch_poller.py. async: true.</expect>
        <if_mismatch>STOP. If multiple matchers or a different structure exists, surface to COO before editing. The hook structure may have changed.</if_mismatch>
      </step>
      <step>
        <run>ls -la .tools/kill-orphans</run>
        <expect>File exists and is executable.</expect>
        <if_mismatch>STOP. Tool missing or non-executable. Surface to COO — ADHC_PUSHFIX Phase 1 depends on this tool.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="before write">
      <step>
        <run>N/A — no comp-* tool covers Claude Code hook configurations or shell-script workspace MCP infrastructure. Documented as out-of-scope per ADHC_PUSHFIX PRD §5.1 and ADHC_COMPIL.003 §5.3 protocol.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python3 -c "import json; json.load(open('.claude/settings.local.json'))" &amp;&amp; echo VALID_JSON</run>
        <expect>VALID_JSON. File must be syntactically valid after edit.</expect>
        <if_mismatch>STOP. Fix JSON syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "import json; h=json.load(open('.claude/settings.local.json'))['hooks']['PostToolUse']; cmds=[c['command'] for m in h for c in m['hooks']]; print(cmds)"</run>
        <expect>List includes both 'python org/mcp/hook_launch_poller.py' AND a kill-orphans command. Both present.</expect>
        <if_mismatch>STOP. kill-orphans command was not added correctly to the hook.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>N/A — no comp-blast surface for hook configuration. Canary test is the acceptance criterion.</run>
        <expect>Absence acknowledged.</expect>
        <if_mismatch>N/A</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      After register_agent MCP tool returns successfully in any session, kill-orphans
      --stale --force runs automatically (in addition to the existing agent-poller.py launch).
      Evidence: .claude/settings.local.json PostToolUse.register_agent hook contains a
      kill-orphans command entry.
    </criterion>
    <criterion id="2">
      Tool failure does not block agent registration. The hook command must be async: true
      (or equivalent non-blocking pattern). Evidence: hook entry has async: true.
    </criterion>
    <criterion id="3">
      Canary test: with at least one orphan watcher running for any serial (verify via
      ps -ef | grep inbox-watch | grep -v grep showing PPID=1 for that serial), call
      register_agent for any serial. Within ~10s, the orphan PID is gone (confirm via
      ps -ef). Evidence: ps -ef output before + after in session log.
    </criterion>
    <criterion id="4">
      .claude/settings.local.json is valid JSON after edit. Evidence: python3 -c
      "import json; json.load(open('.claude/settings.local.json'))" exits 0.
    </criterion>
    <criterion id="5">
      Session log includes Compiler Tools section reproducing every phase-0+2 check
      with observed output and explicit pass/fail vs expect. Missing rows = REWORK.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="none" status="none"/>
  </dependencies>

  <cross_domain_coordination>
    <none/>
    Parallelizable with ADHC_PUSHFIX.002 (inbox-watch.sh PPID check). Both touch
    different files (.claude/settings.local.json vs org/mcp/inbox-watch.sh).
    No shared files. No coordination needed between the two TOs.
  </cross_domain_coordination>

  <commit_identity>
    .tools/safe-commit.sh --author "0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" \
      -m "fix(ADHC_PUSHFIX.001): PostToolUse hook auto-runs kill-orphans --stale --force post register_agent" \
      -- .claude/settings.local.json
  </commit_identity>

  <notes>
    No git tag required. This is workspace MCP tooling, not a pipeline.
    ADHC_OWNPTH.009 (tilde-form alias fix) is also pending for AE 0.7.0. Both are
    independent — can be run in parallel or in sequence per your bandwidth.
    ADHC_PUSHFIX.001 is higher priority (time-sensitive: active orphan accumulation).
  </notes>
</task_order>
