<task_order>
  <metadata>
    <id>ADHC_CLCOMM.002.ae-feature-clb-integration</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-04-30</date>
    <status>staged</status>
    <project_code>ADHC_CLCOMM</project_code>
    <prd_ref>docs/architecture/ADHC_CLCOMM.md §4.5 + §4.6 (canonicalized from feature_clb 5eac1f09f)</prd_ref>
    <effort>0.5 day</effort>
    <gates_on>ADHC_CLCOMM.001 RAVC4 (CL MCP scripts shipped on CLOUD).</gates_on>
    <gates_for>ADHC_CLCOMM.003 (verification + close)</gates_for>
  </metadata>

  <objective>
    Wire up the feature_clb worktree to use the new isolated `complearns-agent-comms` MCP channel. Two file edits in feature_clb: `.mcp.json` (replace opal-agent-comms → complearns-agent-comms; correct the `cwd`) and `.claude/settings.local.json` (rename permission entries; update PostToolUse hook matcher).

    **CRITICAL LANE NOTE:** `feature_clb/.mcp.json` and `feature_clb/.claude/settings.local.json` are on the COMP branch (feature_clb is a worktree). AE 0.5's lane is SHARED_OPAL_ETL, not COMP_LEARNS. Owned-paths Phase 2 (fail-closed since 2026-04-30) will likely BLOCK these commits if those paths map to a lane the AE serial isn't in.

    **Three resolution options (AE judgment + flag to CTO if blocked):**
    1. **Cleanest:** route the COMP-side commits through 1.1.0_SA_CTO via MCP (they have COMP_LEARNS lane authority). AE prepares the exact file content + diff; CTO routes to 1.1.0 for commit.
    2. **Direct:** AE attempts the commit; if owned-paths BLOCKs, use `--force` escape hatch with audit entry citing this TO + Andrew GO. Acceptable for one-off infrastructure plumbing.
    3. **Workaround:** add a YAML exception widening `feature_clb/.mcp.json` and `feature_clb/.claude/settings.local.json` paths to `ANY_EXEC_OR_AE`. Ships in same commit as the wire-up. Sets a precedent for cross-worktree config edits.

    **AE picks based on what's pragmatic when reaching this TO. Document the choice in the session log + commit message.**
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_write>
      - Read current state of `C:/Users/AndrewBerman/Desktop/feature_clb/.mcp.json` and `C:/Users/AndrewBerman/Desktop/feature_clb/.claude/settings.local.json`.
      - Read PRD §4.5 and §4.6 for exact target content.
      - **Lane probe BEFORE editing:** dry-run a commit attempt with `git status` from feature_clb side; check whether owned-paths hook is active in the feature_clb worktree (it should be; same .git/hooks/ is shared between worktrees).
      - Decide which of the 3 resolution options applies. Document the decision rationale.
    </phase_1_before_write>
    <phase_2_before_commit>
      - JSON parse-validate `feature_clb/.mcp.json` post-edit: `python -m json.tool < feature_clb/.mcp.json > /dev/null`.
      - JSON parse-validate `feature_clb/.claude/settings.local.json` post-edit.
      - Confirm `mcp__opal-agent-comms__*` permission entries are FULLY replaced with `mcp__complearns-agent-comms__*` — no stale opal entries left.
      - Confirm PostToolUse hook matcher updated to `mcp__complearns-agent-comms__register_agent`.
    </phase_2_before_commit>
    <phase_3_after_commit>
      - **DO NOT smoke test yet** — that's TO-3 (a fresh feature_clb Claude Code session is needed to load the new MCP config; AE can't smoke-test from inside a session that already loaded the old one).
      - Document the COMP-branch commit hash + the resolution option chosen.
      - Append session-log entry to `org/compiler-tools-log.md`.
    </phase_3_after_commit>
  </compiler_tools_mandate>

  <scope>
    Two file edits, both in the feature_clb worktree (COMP branch):

    1. `feature_clb/.mcp.json` — replace entirely per PRD §4.5. Key changes from current state:
       - Remove `opal-agent-comms` entry (currently has wrong `cwd`)
       - Add `complearns-agent-comms` entry pointing to `org/mcp/complearns_server.py` with `cwd: feature_clb`
       - Remove `deck-generation` (not relevant to CL work)
       - Keep `playwright` if used by CL tooling (per PRD: remove if not — AE judgment)

    2. `feature_clb/.claude/settings.local.json` — two changes:
       - **A.** Replace all `mcp__opal-agent-comms__*` permission entries with `mcp__complearns-agent-comms__*` (full list of 13 in PRD §4.6.A)
       - **B.** Update the PostToolUse hook matcher from `mcp__opal-agent-comms__register_agent` to `mcp__complearns-agent-comms__register_agent`
       - Update `disabledMcpjsonServers` if it references opal-agent-comms (remove the entry; the server is no longer in .mcp.json)

    Pull the new MCP scripts (built in TO-1) into the feature_clb filesystem so the MCP server can find them. Two ways:
    - Git merge: from feature_clb worktree, `git merge origin/CLOUD` (or cherry-pick TO-1 commit). Brings TO-1's new files onto COMP branch.
    - Filesystem copy: cp the new files from ajb_workspace/org/mcp/ to feature_clb/org/mcp/, commit on COMP. Less clean; possible drift.

    Recommended: git merge (or cherry-pick) — keeps history coherent and avoids file-content drift. Document choice in commit message.

    Author: `0.5.0_AE_OpalETL <0.5.0_AE_OpalETL@opal.agent>` (or 1.1.0_SA_CTO if Option 1 routing). Use `.tools/safe-commit.sh` with explicit pathspec.
  </scope>

  <acceptance_criteria>
    1. `feature_clb/.mcp.json` post-edit matches PRD §4.5 spec exactly. JSON parses cleanly. `cwd` is `C:\\Users\\AndrewBerman\\Desktop\\feature_clb`. opal-agent-comms entry absent.
    2. `feature_clb/.claude/settings.local.json` post-edit: all 13 permission entries renamed to `mcp__complearns-agent-comms__*`; PostToolUse hook matcher updated; opal-agent-comms entries absent. JSON parses cleanly.
    3. New MCP scripts (TO-1 deliverables) exist on COMP branch in feature_clb's filesystem. Verify by listing `feature_clb/org/mcp/complearns_server.py`, `cl_broker.py`, `cl-inbox-watch.sh`, `cl-check-inbox.sh`.
    4. Lane resolution choice documented (1/2/3 from objective). If --force used, audit entry visible in `org/git-author-override-audit.log` with this TO ID cited.
    5. Commit on COMP branch (or CLOUD, depending on file scope). Pushed if remote tracking. RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT smoke-test the new channel from inside the current session — MCP config is loaded at session-start; testing requires a fresh Claude Code session. That's TO-3.</rule>
    <rule>Do NOT modify ajb_workspace/.mcp.json — only feature_clb. The org-wide channel stays exactly as is.</rule>
    <rule>Do NOT create new lane definitions in `.owned-paths.yaml` outside of Resolution Option 3 — preemptive widening was flagged by Andrew today (see `feedback_no_preemptive_cross_pipeline_widening.md`).</rule>
    <rule>Do NOT use bare `git commit`. Always `.tools/safe-commit.sh` with explicit pathspec; document any --force usage in commit message + audit log.</rule>
  </do_not>

  <deliverables>
    <deliverable type="config">feature_clb/.mcp.json (MODIFIED to complearns-agent-comms spec)</deliverable>
    <deliverable type="config">feature_clb/.claude/settings.local.json (MODIFIED)</deliverable>
    <deliverable type="code">feature_clb/org/mcp/* CL files present (via merge or copy)</deliverable>
    <deliverable type="document">Session log documenting lane-resolution choice + commit details</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC5 evidence + lane resolution rationale</deliverable>
  </deliverables>
</task_order>
