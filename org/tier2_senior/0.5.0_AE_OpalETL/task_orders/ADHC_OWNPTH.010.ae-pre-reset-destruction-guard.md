<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_OWNPTH.010</id>
    <project>ADHC_OWNPTH</project>
    <title>Pre-reset destruction guard — gate destructive HEAD-move operations that discard local-only commits</title>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="cto_ruling">CTO ruling MCP 20260508T~PM — ship structural mitigation; design sketch authored verbatim by CTO</ref>
    <ref type="anchor_incident_3rd_class">2026-05-08 git-reset incident: AE 0.7 mid-FIRMSEP.07/.08 deploy. Reset to origin/CLOUD discarded 3 local commits (b2ebd19d6, c42105381, 2bd593627). 10 AWS resources destroyed by parallel TF apply on rolled-back .tf. Recovered cleanly but recurrence risk material.</ref>
    <ref type="prior_art_pattern">.tools/git-hooks/owned-paths-check.sh (ADHC_OWNPTH.002 — same lane; audit-log + install-script pattern)</ref>
    <ref type="prior_incident_1">2026-04-22 Andrew "this keeps happening" — feedback_structural_commit_hygiene.md</ref>
    <ref type="prior_incident_2">2026-04-27 base COO swept COMP_LEARNS files (`2b3bfcd4`) — feedback_base_coo_git_sweep_incident.md</ref>
    <ref type="prior_incident_3">2026-04-27/28 record-terraform-deploy.sh sweep × 3 → ADHC_OWNPTH.007 → safe-commit.sh wrapper</ref>
  </references>

  <context>
    Third-class git-incident occurrence: `git reset <ref>` (specifically reset to origin/CLOUD) during heavy multi-agent sessions discards local-only commits without warning. Existing `safe-commit.sh` (ADHC_OWNPTH.007) prevents commit-time contamination but doesn't gate destructive HEAD-move operations.

    **2026-05-08 incident severity:** 10 AWS resources destroyed by parallel TF apply running with rolled-back .tf state during AE 0.7's reset window. Recovery worked but each recovery is non-trivial (manifest reconciliation + audit + 0-diff verification). Next occurrence may not recover as cleanly.

    Same-domain structural mitigation as ADHC_OWNPTH.007 (safe-commit.sh wrapper). Reopens ADHC_OWNPTH at .010 with Phase 2 narrative: "git-workflow safety expanded to destructive HEAD-move operations."

    **Design pattern:** mirror safe-commit.sh — pre-action check + audit-log + force-flag escape hatch. Detects discarded-commit set, lists them to stderr, requires explicit override to proceed.
  </context>

  <scope>
    <step>
      **Phase 1 — author hook script.**

      File: `.tools/git-hooks/pre-reset-guard` (or extend existing pre-action hook surface; verify git supports `pre-reset` hook trigger — Git 2.34+ does; if older, fallback to wrapper-script invocation pattern).

      Hook trigger: pre-reset (git's `pre-reset` hook fires before `git reset` updates HEAD).

      Algorithm:
      1. Capture current HEAD SHA + reflog position
      2. Parse target ref from git's `--head-only` flag passed to hook (target SHA available via hook arg or `git rev-parse <target>`)
      3. Compute discarded-commit set: `git rev-list HEAD ^<target>` minus `git rev-list <target>`
      4. Special-case: ignore `git reset HEAD <path>` (unstage operation; HEAD unchanged) — detected via empty discard set
      5. Special-case: ignore `git reset HEAD~0` or `git reset HEAD` (no-op same SHA)
      6. If discarded set non-empty:
         - Print discarded commits (hash + author + subject + ago) to stderr
         - Check `$RESET_FORCE` env var (or `--force-reset` flag if argv parsed)
         - If neither set: exit 1 (abort)
         - If set: proceed + log to `org/git-author-override-audit.log`

      Audit log line format (mirrors safe-commit.sh):
      ```
      YYYY-MM-DDTHHMMSSZ FORCE-RESET <serial> <prior-HEAD-sha> -> <target-sha> (<N> discarded)
      ```
    </step>

    <step>
      **Phase 2 — author install script.**

      File: `.tools/git-hooks/install-pre-reset-guard.sh` (mirrors `install-owned-paths.sh` pattern).

      - Install hook into `.git/hooks/pre-reset` (and any necessary fallback wrapper if `pre-reset` not natively supported)
      - Idempotent: re-run safe; doesn't duplicate
      - Verify with `git hooks verify` post-install
      - Echo install location + verification result
    </step>

    <step>
      **Phase 3 — Windows Git Bash 3.6.7 compatibility check.**

      Per CLAUDE.md Rule 16 utility availability table: ensure script uses only utilities that ship with Git Bash 3.6.7 default install.
      - Available: bash 5.3.9, ps, awk, sed, grep, find, timeout, curl, xargs, mktemp, realpath, stdbuf, tee, jq (workspace-local), git, python/python3, aws
      - NOT available: pgrep, pkill, flock, pidof, setsid, wget — DO NOT USE without `command -v` guarded fallback

      Test on Andrew's Windows Git Bash environment (or equivalent dev env).
    </step>

    <step>
      **Phase 4 — empirical validation.**

      Test fixtures:
      - **AC1:** bare `git reset origin/CLOUD` from a position with local commits → aborts cleanly + lists discarded
      - **AC2:** `RESET_FORCE=1 git reset origin/CLOUD` → proceeds + logs FORCE-RESET line to audit log
      - **AC3:** `git reset HEAD path/to/file` (unstage) → unaffected — no false positive
      - **AC4:** `git reset HEAD~0` (no-op same SHA) → unaffected
      - **AC5:** `git reset HEAD~1` from position with no local commits ahead → aborts (1 discarded)
      - **AC6:** Hook idempotent — install script run twice doesn't duplicate

      Use synthetic test repo or feature_clb worktree for fixtures.
    </step>

    <step>
      Commit + push. Update `org/projects/REGISTRY.md` ADHC_OWNPTH row to reflect Phase 2 .010 ship.
    </step>
  </scope>

  <acceptance_criteria>
    1. `.tools/git-hooks/pre-reset-guard` ships; executable; correct shebang; Git Bash 3.6.7 compatible.
    2. `.tools/git-hooks/install-pre-reset-guard.sh` ships; idempotent; mirrors install-owned-paths.sh pattern.
    3. AC1: bare `git reset origin/CLOUD` from a position with local commits aborts (exit 1) + lists discarded commits to stderr.
    4. AC2: `RESET_FORCE=1 git reset origin/CLOUD` proceeds + appends FORCE-RESET line to `org/git-author-override-audit.log`.
    5. AC3: `git reset HEAD path/to/file` (unstage operation) is unaffected — no false positive abort.
    6. AC4: `git reset HEAD~0` (no-op) is unaffected.
    7. AC5: works on Windows Git Bash 3.6.7 (per CLAUDE.md Rule 16).
    8. AC6: install script idempotent; re-run safe.
    9. Audit log format: `YYYY-MM-DDTHHMMSSZ FORCE-RESET <serial> <prior-HEAD-sha> -> <target-sha> (<N> discarded)`.
    10. Out-of-scope (do NOT implement in this TO): rebase, force-push, force-checkout — separate hooks if those classes recur.
    11. Session log Compiler Tools section reproduces each `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail.
    12. RAVC2 to COO with: commit SHA, install script invocation result, all 6 AC test fixture outputs (pass/fail), Windows Git Bash 3.6.7 compatibility verification.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat .tools/git-hooks/owned-paths-check.sh | head -50</run>
        <expect>Existing hook pattern visible — audit log writes, override env-var pattern, error-exit semantics. Mirror this pattern.</expect>
        <if_mismatch>If hook missing, ADHC_OWNPTH.002 not properly shipped; surface to COO before authoring.</if_mismatch>
      </step>
      <step>
        <run>git --version</run>
        <expect>git version ≥ 2.34 for native `pre-reset` hook support; if older, fallback to wrapper-script pattern.</expect>
        <if_mismatch>If &lt;2.34, document fallback approach in TO ship notes.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>.tools/git-hooks/install-pre-reset-guard.sh; ls -la .git/hooks/pre-reset</run>
        <expect>Install script runs cleanly; pre-reset hook installed.</expect>
        <if_mismatch>Install failed; debug.</if_mismatch>
      </step>
      <step>
        <run>git rev-list HEAD ^origin/CLOUD | wc -l</run>
        <expect>Returns count of local-only commits; informational. If &gt;0, AC1 testable; if 0, fixture requires synthetic local commit creation first.</expect>
        <if_mismatch>n/a (informational)</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure git-workflow tooling; no S3/data side-effects; no reprocessing required.</no_reprocess_needed>
  </data_reprocess_scope>

  <dependencies>
    None. Parallel-dispatchable with INFLFE.006-data (DS~B) + COMPIL_V4.003 (AE 0.7).
  </dependencies>
</task_order>
