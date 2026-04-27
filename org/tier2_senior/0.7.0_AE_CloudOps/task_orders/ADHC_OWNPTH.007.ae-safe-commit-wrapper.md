<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-27-adhc-ownpth-007-ae-safe-commit-wrapper</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>0.7.0_AE_CloudOps</issued_to>
  <issued_date>2026-04-27</issued_date>
  <status>open</status>

  <title>ADHC_OWNPTH TO 7 — safe-commit.sh wrapper + index-state pre-commit check (AE CloudOps)</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="rule">CLAUDE.md Rule 14a (--only mandate, to be updated post-ship to reference safe-commit.sh)</ref>
    <ref type="config">.owned-paths.yaml</ref>
    <ref type="hook">.tools/git-hooks/owned-paths-check.sh</ref>
    <ref type="audit">org/git-author-override-audit.log</ref>
    <ref type="prior_to">ADHC_OWNPTH.005 (flip-to-fail-closed, CTO scope), ADHC_OWNPTH.006 (commit-discipline yaml+claudemd, CTO scope)</ref>
  </references>

  <context>
    Three sweep incidents on 2026-04-27 (f84c2df4, 0ac97913, and a third) demonstrated that
    even explicit git add + git commit --only is insufficient when pre-staged ambient files
    exist in the index. Root cause: agents run git add &lt;explicit-path&gt; but then issue
    git commit with incomplete index isolation. The owned-paths hook fires but cannot abort
    the commit if the index already contains out-of-lane files before the hook runs.

    TO 7 closes the structural gap by providing a wrapper script (safe-commit.sh) that:
    1. Inspects the full staged index BEFORE committing.
    2. Aborts if staged files do not exactly match the declared pathspec.
    3. Wraps git commit --only &lt;pathspec&gt; so the safe path is the natural path.

    This is the structural complement to TO 5 (fail-closed mode) and TO 6 (YAML/CLAUDE.md rule).
    Gates: none — independent of TO 5 + TO 6.
  </context>

  <scope>
    1. Author `.tools/safe-commit.sh`:
       - Accepts: --author "..." -m "message" -- &lt;pathspec...&gt;
       - Step A: run `git diff --cached --name-only` to capture full staged set.
       - Step B: compare staged set against declared pathspec files.
         - If staged contains ANY file not in pathspec: print ERROR listing the extra files,
           exit 1 (abort — commit does not proceed).
         - If --force flag passed: log bypass to org/git-author-override-audit.log
           (format: {ISO8601} FORCE-BYPASS {agent} {N_files} ({details})) and proceed.
       - Step C: run `git commit --only &lt;pathspec&gt; --author "..." -m "..."` (pass-through
         remaining args after -- separator).
       - Script must be POSIX-compatible (bash, not zsh). Use /usr/bin/env bash shebang.
       - --help: print usage summary and exit 0.

    2. Ensure `.tools/safe-commit.sh` is executable (`chmod +x`).

    3. Update CLAUDE.md Rule 14a (post-ship):
       - Current: "Always constrain commit pathspec (--only flag)"
       - New: "Always use .tools/safe-commit.sh for commits. It wraps --only and aborts on
         index contamination. Direct git commit requires explicit justification and audit log
         entry."
       - Keep the existing -- or --only guidance as a fallback note for emergency use.

    4. Optional (bonus): Add a one-line hint in `.tools/git-hooks/owned-paths-check.sh`
       (after any VIOLATION lines) suggesting the agent use safe-commit.sh. Non-blocking
       if skipped — core deliverable is the wrapper script.

    Do NOT modify .owned-paths.yaml. Do NOT change OWNED_PATHS_MODE.
    Do NOT update org/XXX.md startup protocol (that is CTO scope if needed later).
  </scope>

  <dependencies>
    <!-- No hard dependencies. TO 5 + TO 6 are independent parallel tracks. -->
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>git diff --cached --name-only</run>
        <expect>Empty (clean index before starting). If not empty, abort and clear the index first.</expect>
        <if_mismatch>STOP. Clean index before authoring the script.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after write, before commit">
      <step>
        <run>bash .tools/safe-commit.sh --help</run>
        <expect>Exit 0. Usage summary printed.</expect>
        <if_mismatch>STOP. Script must be self-documenting before shipping.</if_mismatch>
      </step>
      <step>
        <run>Canary test A (match case): stage safe-commit.sh only; run safe-commit.sh
          with pathspec = .tools/safe-commit.sh; expect exit 0 + commit proceeds.</run>
        <expect>Exit 0. Commit created.</expect>
        <if_mismatch>STOP. Fix mismatch detection logic.</if_mismatch>
      </step>
      <step>
        <run>Canary test B (mismatch case): stage an extra file alongside pathspec;
          run safe-commit.sh with pathspec for original file only; expect exit 1 + abort.</run>
        <expect>Exit 1. ERROR message lists the extra staged file. No commit created.</expect>
        <if_mismatch>STOP. Abort logic is broken.</if_mismatch>
      </step>
      <step>
        <run>Canary test C (--force bypass): same as B but with --force; expect exit 0
          + audit log entry written.</run>
        <expect>Exit 0. org/git-author-override-audit.log contains FORCE-BYPASS line.</expect>
        <if_mismatch>STOP. Force-bypass audit log is required.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git show --stat HEAD</run>
        <expect>Only safe-commit.sh (and optionally CLAUDE.md update) in the commit.
          No out-of-lane files.</expect>
        <if_mismatch>STOP. Commit is contaminated. Escalate to CTO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <coordination agent="2.0.0_SA_COO" note="MCP COO on completion with commit hash. COO will broadcast safe-commit.sh availability to all live agents and update CLAUDE.md Rule 14a note."/>
    <coordination agent="1.0.0_SA_CTO" note="CTO authored TO spec (ADHC_OWNPTH.006 message 20260427T18XXXX). AE ships; CTO notified on completion."/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `.tools/safe-commit.sh` exists, is executable, has --help output.
    2. Canary A (match): exit 0, commit succeeds.
    3. Canary B (mismatch): exit 1, commit aborted, extra files listed in ERROR.
    4. Canary C (--force): exit 0, audit log FORCE-BYPASS entry written.
    5. CLAUDE.md Rule 14a updated to mandate safe-commit.sh as primary path.
    6. Session log includes all 3 canary runs with output.
    7. MCP COO + MCP CTO on completion with commit hash.
  </acceptance_criteria>
</task_order>
