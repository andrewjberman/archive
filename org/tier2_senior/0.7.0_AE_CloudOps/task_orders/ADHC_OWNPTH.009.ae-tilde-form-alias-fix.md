<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-28-ownpth-009-tilde-form-alias-fix</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-28</date>
    <status>complete</status>
    <project_code>ADHC_OWNPTH</project_code>
    <to_serial>009</to_serial>
    <priority>LOW</priority>
    <prd>docs/architecture/ADHC_OWNPTH.md (Phase 1 hook hardening)</prd>
  </metadata>

  <objective>
    Fix the owned-paths pre-commit hook so it correctly recognizes both the
    underscore form (`{pod}.{tier}.{role}_{lane}`) and the tilde form
    (`{pod}.{tier}.{role}~{lane}`) as the same agent identity for tilde-lane
    agents. Currently the hook flags every commit by tilde-lane agents (DS~B,
    AE~B, etc.) as "agent not in permitted_agents" because the YAML config
    lists tilde form but git author MUST use underscore form per
    `feedback_author_serial_no_tilde.md`.
  </objective>

  <context>
    DS~B reported during ADVI_INFLV2.012 cross-ref commit `f603e915`:

      "POD4 owned-paths WARN. The pre-commit hook flagged
       `0.4.0_DS_ClientPlatform_B` not in POD4 permitted_agents list.
       Likely the lane config has `~B` tilde-form literally and the
       underscore-vs-tilde mismatch (per memory
       `feedback_author_serial_no_tilde.md` — git author MUST be
       underscore form, but hook membership is on tilde form). WARN
       mode so commit proceeded. Flagging for COO follow-up — hook
       config may need to alias both forms for tilde-lane agents."

    AE~B confirmed same issue during ORIAPI.001 ship. Both tilde-lane
    agents have committed multiple times this session with the WARN
    message firing each time.

    WARN mode currently masks this — every tilde-lane commit fires a
    spurious WARN that someone has to mentally filter. Once Phase 2
    flips to fail-closed (ADHC_OWNPTH.005, gates on TO 4 observe-week),
    every tilde-lane commit will BLOCK without this fix.

    Therefore: fix MUST land before TO 5 (Phase 2 flip-closed) ships.
    Easy way to enforce: TO 5 dependency check verifies TO 9 commit ref
    in audit log before flipping the rollout_phase.
  </context>

  <files_to_modify>
    <file>.tools/git-hooks/owned-paths-check.sh</file>
    <file action="modify">.owned-paths.yaml (only if hook reads from a separate alias config; otherwise leave alone — hook does the normalization)</file>
  </files_to_modify>

  <spec_summary>
    The hook currently extracts the git author serial (e.g.,
    `0.4.0_DS_ClientPlatform_B`) and compares it directly against the
    `permitted_agents` list in `.owned-paths.yaml`, which lists agents
    by tilde form (e.g., `0.4.0_DS_ClientPlatform~B`).

    Add a normalization step in the hook before the membership check:

    ```bash
    # Normalize tilde-form -> underscore-form for membership comparison
    # Both forms refer to the same agent identity per
    # feedback_author_serial_no_tilde.md
    normalize_serial() {
      # Replace ~ with _ in the lane suffix
      # Pattern: {pod}.{tier}.{role}~{X} -> {pod}.{tier}.{role}_{X}
      echo "$1" | sed 's/~\([A-Za-z0-9]\+\)$/_\1/'
    }

    AUTHOR_NORMALIZED=$(normalize_serial "$AUTHOR_SERIAL")
    PERMITTED_NORMALIZED=$(printf '%s\n' "${PERMITTED[@]}" | while read p; do normalize_serial "$p"; done)

    if printf '%s\n' "$PERMITTED_NORMALIZED" | grep -q "^${AUTHOR_NORMALIZED}$"; then
      # match
    fi
    ```

    Both lookup directions normalized to the same form before comparison.
    Author keeps writing in underscore form (no change to author convention);
    YAML keeps using tilde form (no churn on existing config); hook bridges.

    Audit log entries should LOG THE ORIGINAL author form (underscore), not
    the normalized form, for forensic clarity.
  </spec_summary>

  <acceptance_criteria>
    <ac>1. Hook normalizes tilde form to underscore form before membership
        check. Both `0.4.0_DS_ClientPlatform_B` (git author) and
        `0.4.0_DS_ClientPlatform~B` (YAML config) resolve to the same
        permitted-agent identity.</ac>
    <ac>2. Canary tests: tilde-lane agent committing to a permitted path
        produces NO warn/block (currently produces spurious WARN).
        Tilde-lane agent committing to NON-permitted path STILL produces
        warn/block as expected.</ac>
    <ac>3. Base-lane agents (no tilde, no underscore lane suffix) still
        match correctly (no regression).</ac>
    <ac>4. Audit log entries continue to record the ORIGINAL git author
        serial (underscore form), not the normalized form.</ac>
    <ac>5. 5-line update to `.tools/git-hooks/owned-paths-check.sh` per
        spec above; commit via safe-commit.sh; tag inf-pipeline if
        applicable (likely no TF tag — pure script change).</ac>
  </acceptance_criteria>

  <gates_and_dependencies>
    <gates>None — runs anytime AE 0.7.0 has bandwidth.</gates>
    <unblocks>ADHC_OWNPTH.005 (Phase 2 fail-closed flip — must land before
        the flip or every tilde-lane commit will block).</unblocks>
  </gates_and_dependencies>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 with hook commit ref + canary test output showing
        tilde-lane agents pass without WARN.</on_complete>
  </ravc_target>

  <estimated_effort>30-60 minutes (5-line hook patch + canary verification + commit).</estimated_effort>
</task_order>
