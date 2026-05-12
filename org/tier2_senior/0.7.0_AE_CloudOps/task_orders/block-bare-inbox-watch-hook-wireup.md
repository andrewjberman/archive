<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-05-12-block-bare-inbox-watch-hook-wireup</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to><!-- CTO direct authorization from Andrew 2026-05-12 13:55Z: "have 0.7.0 do it" — hook script + settings wireup is AE infra lane (settings.local.json + .tools/hooks/). -->
    <date>2026-05-12</date>
    <status>pending</status>
    <project_code>ad-hoc</project_code>
    <priority>P1 — small lift (~15 min). Deterministic prevention of the silent watcher-deafness failure mode Andrew empirically hit 2026-05-12 (zombie PID 443027 short-circuit + misleading exit 143).</priority>
  </metadata>

  <references>
    <ref type="trigger">Andrew empirical 2026-05-12: bare-path inbox-watch.sh launches create PPID=1 auto-respawn zombies that short-circuit future tracked launches via single-watcher guard; Claude Code surfaces guard-exit-0 as misleading exit 143 in task output.</ref>
    <ref type="doc_change">org/XXX.md line 92 (canonical launch form mandate, shipped `ddf654141`)</ref>
    <ref type="doc_change">org/mcp/INBOX_WATCH_DESIGN.md § "Failure mode: 143 / zombie short-circuit" (shipped `81b97d753`)</ref>
    <ref type="hook_script">.tools/hooks/block-bare-inbox-watch.sh (CTO-authored, untracked — AE owns commit)</ref>
  </references>

  <objective>
    Deterministically prevent bare-path inbox-watch.sh launches. Doc-level mandate
    (org/XXX.md + INBOX_WATCH_DESIGN.md) is awareness-only; agents skim. A
    PreToolUse hook blocking the relative-path form at tool-call time is the
    only mechanism that survives skim.

    Two steps:
    1. Commit the hook script `.tools/hooks/block-bare-inbox-watch.sh` (already
       authored + smoke-tested 5/5 cases by CTO; sits in working tree).
    2. Wire it via PreToolUse hook in `.claude/settings.local.json` (and
       optionally project-shared `.claude/settings.json` if the wire-up should
       apply org-wide, not just this user — AE judgment call).
  </objective>

  <deliverables>
    <item>
      <path>.tools/hooks/block-bare-inbox-watch.sh</path>
      <action>commit (already authored + tested; `chmod +x` already applied)</action>
      <notes>Reject input: `bash org/mcp/inbox-watch.sh <serial>` and `sh` variants, including chained forms. Accept: `inbox-watch <serial>` (PATH wrapper) and `bash /absolute/path/...` (absolute). Smoke tests run 2026-05-12 13:48Z passed all 5 cases.</notes>
    </item>
    <item>
      <path>.claude/settings.local.json</path>
      <action>add PreToolUse hook block as sibling to existing PostToolUse block</action>
      <snippet><![CDATA["PreToolUse": [
  {
    "matcher": "Bash|PowerShell",
    "hooks": [
      {
        "type": "command",
        "command": "bash .tools/hooks/block-bare-inbox-watch.sh",
        "timeout": 5
      }
    ]
  }
]]]></snippet>
    </item>
  </deliverables>

  <acceptance_criteria>
    1. `.tools/hooks/block-bare-inbox-watch.sh` committed to CLOUD with `chmod +x` preserved (verify: `git ls-files -s .tools/hooks/block-bare-inbox-watch.sh` shows mode `100755`).
    2. PreToolUse hook entry added to `.claude/settings.local.json` (or shared `.claude/settings.json` per AE judgment) — JSON validates.
    3. Empirical post-wire-up test in a fresh Bash tool call: attempting `bash org/mcp/inbox-watch.sh <any_serial>` returns the hook's BLOCKED stderr message and the command does NOT execute. Capture transcript in session log.
    4. Empirical positive test: `inbox-watch <serial>` (PATH wrapper) and `bash /c/Users/AndrewBerman/Desktop/ajb_workspace/org/mcp/inbox-watch.sh <serial>` both PASS through the hook and reach the underlying script normally.
    5. No regression of the existing PostToolUse hook (`mcp__opal-agent-comms__register_agent` matcher with `hook_launch_poller.py` + `kill-orphans` chain) — verify a register-agent call still fires both.
    6. Session log entry under `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-05-12/` with the four test transcripts + commit hash.
    7. MCP COMPLETE to 1.0.0_SA_CTO with commit hash + settings.json delta.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <none reason="Hook wireup touches .tools/hooks/ + .claude/settings.local.json. Neither is modeled in the compiler graph. No comp-* check applies. Smoke-test transcripts are the validation surface (acceptance criteria 3+4)."/>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none reason="settings.local.json is user-local; .tools/hooks/ is an AE-owned tool directory. No shared S3 artifacts, no shared Lambda, no other agent's lane touched. CTO authored the hook script in the working tree but explicitly hands ownership to AE for commit + wireup per Andrew 2026-05-12 directive."/>
  </cross_domain_coordination>

  <notes>
    - Choice between `.claude/settings.local.json` (this machine only) vs project-shared `.claude/settings.json` is AE's call. The local file already has PostToolUse hooks for this user; the shared file is committed and would apply to all users of the repo. Recommend shared for org-wide coverage, but local is faster to ship and proves the mechanism.
    - If you find the hook needs a tweak (e.g., the PowerShell tool wraps commands differently and the regex misses a case), surface back to CTO before shipping — the regex was tested only against the Bash-tool eval-wrapper form. CTO can adjust + re-test.
    - Live bare-path zombies in the org as of 2026-05-12 13:00Z: PID 442015 (0.6.1_AE_PartnerETL), PID 446579 (0.4.0_DS_ClientPlatform~C if still alive), and 1.0.0_SA_CTO's own 439200 (tracked but bare-form). Hook only prevents NEW bare-path launches; existing zombies stay until killed. Cleanup is independent.
  </notes>
</task_order>
