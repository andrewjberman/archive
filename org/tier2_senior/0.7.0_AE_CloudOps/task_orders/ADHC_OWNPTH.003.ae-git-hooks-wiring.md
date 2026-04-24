<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-24-adhc-ownpth-003-ae-git-hooks-wiring</id>
  <project>ADHC_OWNPTH</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>0.7.0_AE_CloudOps</issued_to>
  <issued_date>2026-04-24</issued_date>
  <status>staged</status><!-- STAGED: gates on ADHC_OWNPTH.002 (DS hook script impl) completion -->

  <title>ADHC_OWNPTH TO 3 — Git hooks wiring + install bootstrap (AE CloudOps)</title>

  <references>
    <ref type="prd">docs/architecture/ADHC_OWNPTH.md</ref>
    <ref type="tooling">`.tools/git-hooks/owned-paths-check.sh` (TO 2 output)</ref>
    <ref type="config">`.owned-paths.yaml` (TO 1 output)</ref>
    <ref type="startup">org/XXX.md (Step 1b to be updated)</ref>
  </references>

  <context>
    TO 1 produced .owned-paths.yaml. TO 2 produced the hook script at
    .tools/git-hooks/owned-paths-check.sh + the validator .tools/owned-paths-validate.py.
    TO 3 wires the hook into .git/hooks/pre-commit via symlink so it fires on every commit.
    AE CloudOps owns infrastructure wiring — .git/hooks/ is shared infra for the repo.

    Phase 1 (warn-mode) begins when the hook is live. AE wires, then COO broadcasts to all
    agents that the hook is active. Default mode = warn (OWNED_PATHS_MODE not set = warn).
  </context>

  <scope>
    1. Check existing .git/hooks/pre-commit:
       - If absent: create symlink .git/hooks/pre-commit -> ../../.tools/git-hooks/owned-paths-check.sh
       - If present: chain the existing hook by creating a wrapper that calls both the
         existing hook and owned-paths-check.sh in sequence. Document chain in session log.

    2. Create `.tools/git-hooks/install-owned-paths.sh` (idempotent bootstrap):
       - Checks if .git/hooks/pre-commit exists as a symlink to owned-paths-check.sh
       - If not: creates/updates the symlink (or chain wrapper)
       - Safe to re-run: idempotent; no-ops if already wired correctly
       - Exits 0 on success; exits 1 with error message if .tools/git-hooks/owned-paths-check.sh
         is missing (TO 2 not yet shipped)

    3. Bootstrap `org/git-author-override-audit.log`:
       - Create file if absent (append-only; first line = bootstrap record)
       - Format: `{ISO8601} BOOTSTRAP  SYSTEM  0_files  (audit log initialized by ADHC_OWNPTH.003 AE wiring)`

    4. Add to `org/XXX.md` Step 1b (agent startup protocol) — after the existing
       register_agent + inbox-watch lines, add:
       ```
       test -L .git/hooks/pre-commit || bash .tools/git-hooks/install-owned-paths.sh
       ```
       Include a one-line comment: "# owned-paths hook — installs if absent (ADHC_OWNPTH)"

    5. Run canary test after wiring: stage a single file from an out-of-lane path with
       a known author; confirm WARN fires in warn-mode (exit 0). Document canary output
       in session log.

    Do NOT modify .owned-paths.yaml (TO 1) or hook script internals (TO 2).
    Do NOT change OWNED_PATHS_MODE — leave at default (warn/Phase 1).
  </scope>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_OWNPTH.002" status="staged"
                required=".tools/git-hooks/owned-paths-check.sh must exist before wiring. TO 2 must be complete."/>
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>ls -la .git/hooks/</run>
        <expect>List of existing hooks. Note any pre-commit hook already present — if so, must chain, not replace. Document in session log.</expect>
        <if_mismatch>NOTE only. Chain if pre-commit exists.</if_mismatch>
      </step>
      <step>
        <run>ls .tools/git-hooks/owned-paths-check.sh &amp;&amp; echo "TO 2 COMPLETE" || echo "TO 2 NOT YET SHIPPED"</run>
        <expect>"TO 2 COMPLETE". If not, STOP — TO 2 must ship first.</expect>
        <if_mismatch>STOP. Do not wire until TO 2 is complete.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>bash .tools/git-hooks/install-owned-paths.sh &amp;&amp; echo "INSTALL OK"</run>
        <expect>Exit 0 + "INSTALL OK". Symlink (or chain wrapper) created.</expect>
        <if_mismatch>STOP. Fix install script before committing.</if_mismatch>
      </step>
      <step>
        <run>ls -la .git/hooks/pre-commit</run>
        <expect>Symlink or wrapper file present. Symlink should resolve to ../../.tools/git-hooks/owned-paths-check.sh</expect>
        <if_mismatch>STOP. Hook not wired — install failed silently.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>canary test — run install-owned-paths.sh on at least one other agent's working directory (if accessible) or re-run on main repo to confirm idempotent behavior</run>
        <expect>Exit 0. No errors. Existing symlink not replaced (idempotent).</expect>
        <if_mismatch>NOTE to 2.0.0_SA_COO — agents will need to run install manually if worktrees differ.</if_mismatch>
      </step>
      <step>
        <run>tail -5 org/git-author-override-audit.log</run>
        <expect>Bootstrap line present. Canary test WARN line present (if canary was run). Confirms audit log is operational.</expect>
        <if_mismatch>STOP. Audit log must be populated before Phase 1 observation begins.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <coordination agent="2.0.0_SA_COO" note="MCP COO immediately on TO 3 completion. COO will broadcast Phase 1 start to all live agents (hook is live in warn-mode; any WARN means YAML adjustment needed; flag to COO). Do not signal AE trigger."/>
    <coordination agent="0.4.0_DS_ClientPlatform" note="DS hook script must be shipped (TO 2 complete) before AE begins. No concurrent edits to .tools/git-hooks/ during TO 3."/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `.git/hooks/pre-commit` symlinks (or chains) to `.tools/git-hooks/owned-paths-check.sh`.
    2. `.tools/git-hooks/install-owned-paths.sh` exists, is executable, is idempotent.
    3. `bash .tools/git-hooks/install-owned-paths.sh` exits 0 on fresh run + re-run.
    4. `org/git-author-override-audit.log` created with BOOTSTRAP entry.
    5. `org/XXX.md` Step 1b includes install-check line.
    6. Canary test executed and output documented in session log (WARN fires, exit 0).
    7. Session log includes Phase 1-3 compiler tools runs with pass/fail.
    8. MCP COO on completion with commit hash + audit log tail showing bootstrap + canary entries.
  </acceptance_criteria>

  <evidence>
    <!-- To be filled by AE on completion -->
  </evidence>
</task_order>
