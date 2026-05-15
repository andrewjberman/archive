<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_OWNPTH.010</id>
    <project>ADHC_OWNPTH</project>
    <title>Unified destructive-HEAD-move guard -- gate reset/rebase/amend operations that discard or rewrite local-only commits</title>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <revised>2026-05-15 -- scope-step-1 + AC10 rewritten by COO per the CTO Option-(a) ruling (20260515T193433Z). Mechanism corrected: git has no pre-reset hook; the guard hooks reference-transaction. Reframed from a reset-only guard to a unified destructive-HEAD-move guard (reset + rebase + amend). No new design -- this encodes AE 0.5.0's Phase-1-probe Option-A, CTO-ratified. The install-step + Phase-4 fixtures + the dependent ACs were threaded for coherence with the corrected mechanism.</revised>
    <status>pending</status>
    <priority>medium</priority>
    <estimated_effort>~0.5d (unchanged -- AE 0.5.0 corrected-design estimate)</estimated_effort>
  </metadata>

  <references>
    <ref type="cto_ruling_original">CTO ruling MCP 20260508T~PM -- ship a structural mitigation for the destructive-HEAD-move incident class. The original design sketch (a "pre-reset" hook) was empirically wrong -- see cto_ruling_corrected.</ref>
    <ref type="ae_phase1_probe">0.5.0_AE_OpalETL Phase-1 synthetic-repo probe 20260515T183713Z. FINDING 1 -- git has NO pre-reset hook (any version); installed .git/hooks/pre-reset (exit 1) in a synthetic repo, ran git reset --hard, the hook never fired. FINDING 2 -- reference-transaction is the only structural hook that fires on git reset; exit 1 at state=prepared cleanly aborts the update (HEAD verified unmoved). FINDING 3 -- the hook is command-blind (GIT_REFLOG_ACTION unset; a commit and a reset present identical refs/heads/* transactions) -- topology is the only discriminator.</ref>
    <ref type="cto_ruling_corrected">CTO ruling 20260515T193433Z -- Option (a) ACCEPT: reframe .010 as a unified destructive-HEAD-move guard. The topology discriminator necessarily also catches rebase + commit --amend; that coverage is CORRECT (same risk class -- destructive HEAD-moves that discard/rewrite local commits), not a scope violation. Option (b) allowlist-heuristic rejected (amend is topologically identical to reset; leaky by mechanism). Option (c) wrapper-script rejected (cultural, fails AC3/AC6, contradicts ADHC_OWNPTH's structural-over-cultural thesis). Load-bearing scoping: state=prepared + refs/heads/* + non-zero-old.</ref>
    <ref type="anchor_incident_3rd_class">2026-05-08 git-reset incident: AE 0.7 mid-FIRMSEP.07/.08 deploy. Reset to origin/CLOUD discarded 3 local commits (b2ebd19d6, c42105381, 2bd593627). 10 AWS resources destroyed by a parallel TF apply on rolled-back .tf. Recovered cleanly but recurrence risk material.</ref>
    <ref type="prior_art_pattern">.tools/git-hooks/owned-paths-check.sh (ADHC_OWNPTH.002 -- same lane; audit-log + install-script + override-env pattern to mirror).</ref>
    <ref type="prior_incident_1">2026-04-22 Andrew "this keeps happening" -- feedback_structural_commit_hygiene.md</ref>
    <ref type="prior_incident_2">2026-04-27 base COO swept COMP_LEARNS files (2b3bfcd4) -- feedback_base_coo_git_sweep_incident.md</ref>
    <ref type="prior_incident_3">2026-04-27/28 record-terraform-deploy.sh sweep x3 -> ADHC_OWNPTH.007 -> safe-commit.sh wrapper</ref>
  </references>

  <context>
    Third-class git-incident occurrence: a destructive HEAD-move during heavy multi-agent sessions discards or rewrites local-only commits without warning. The incident class spans `git reset <ref>` (the 2026-05-08 reset to origin/CLOUD) and -- by the same mechanism -- `git rebase` and `git commit --amend`. Existing safe-commit.sh (ADHC_OWNPTH.007) prevents commit-time contamination but does not gate destructive HEAD-move operations.

    2026-05-08 incident severity: 10 AWS resources destroyed by a parallel TF apply running with rolled-back .tf state during AE 0.7's reset window. Recovery worked but each recovery is non-trivial (manifest reconciliation + audit + 0-diff verification). Next occurrence may not recover as cleanly.

    MECHANISM CORRECTION (AE 0.5.0 Phase-1 probe, CTO-ratified 2026-05-15). The original TO premised a git `pre-reset` hook. No such hook exists at any git version. The only structural hook that fires on `git reset` -- and aborts it cleanly -- is `reference-transaction`. That hook is command-blind, so the guard discriminates by TOPOLOGY (does the HEAD-move discard commits), which by mechanism also covers `git rebase` and `git commit --amend`. Per the CTO ruling that coverage is correct: rebase and amend are the same risk class. .010 is therefore a UNIFIED destructive-HEAD-move guard, not a reset-only guard -- it reopens ADHC_OWNPTH with a Phase-2 narrative: "git-workflow safety expanded to destructive HEAD-move operations."

    Design pattern: mirror safe-commit.sh / owned-paths-check.sh -- a structural hook + an audit log + a force-flag escape hatch. Detect the discarded/rewritten-commit set, list it to stderr, require an explicit override to proceed.
  </context>

  <scope>
    <step>
      Phase 1 -- author the hook script (CORRECTED MECHANISM).

      File: `.tools/git-hooks/headmove-guard` (the hook logic; AE may choose a different coherent name -- NOT "pre-reset", which is a non-existent git hook).

      Hook type: git's `reference-transaction` hook. It fires per ref-transaction with a `state` argument (preparing / prepared / committed / aborted) and stdin lines `<old-sha> <new-sha> <ref-name>`. Exit 1 at `state=prepared` cleanly aborts the transaction (`fatal: ... update aborted by the reference-transaction hook`; HEAD unmoved). This is the only hook that gates `git reset` -- there is no `pre-reset` hook.

      Algorithm (per stdin transaction line):
      1. Act ONLY when the hook's `state` argument is `prepared`. Ignore preparing / committed / aborted.
      2. Act ONLY on `ref-name` matching `refs/heads/*`. IGNORE: HEAD, ORIG_HEAD, AUTO_MERGE, FETCH_HEAD, MERGE_HEAD, `refs/remotes/*`, `refs/stash`, `refs/tags/*`.
      3. Act ONLY when `old-sha` is non-zero (an all-zero `old-sha` is branch creation -- ignore).
      4. Topology discriminator: `git merge-base --is-ancestor <old-sha> <new-sha>`.
         - PASSES (old IS an ancestor of new) -- a normal commit or a fast-forward merge -- NOT destructive -- allow silently.
         - FAILS (old is NOT an ancestor of new) -- commits reachable from old are being discarded or rewritten -- DESTRUCTIVE HEAD-move (covers reset-to-divergent-ref, rebase, and commit --amend by mechanism).
      5. On a destructive move:
         - Compute the discarded/rewritten set: `git rev-list <new-sha>..<old-sha>`.
         - Print it (hash + author + subject + relative-age) to stderr with a clear "ABORTED: destructive HEAD-move would discard N local commit(s)" banner.
         - Check the override env var (`FORCE_HEADMOVE=1`; `RESET_FORCE=1` MAY be retained as an accepted alias for continuity -- AE's call).
         - If not set: exit 1 (aborts the transaction at `prepared`).
         - If set: exit 0 (allow) + append a FORCE-HEADMOVE line to `org/git-author-override-audit.log`.

      The `state=prepared` + `refs/heads/*` + non-zero-old scoping is LOAD-BEARING (CTO note). It must NOT flag normal commits, fast-forward merges (old is an ancestor of new, so --is-ancestor passes), fetches (`refs/remotes/*`, filtered out), or branch creation (`old-sha` all-zero, filtered out). This is the correctness boundary -- a false positive here blocks every ordinary commit.

      Audit log line format (mirrors safe-commit.sh / owned-paths-check.sh):
      ```
      YYYY-MM-DDTHHMMSSZ FORCE-HEADMOVE <serial> <prior-HEAD-sha> -> <target-sha> (<N> discarded)
      ```
    </step>

    <step>
      Phase 2 -- author the install script.

      File: `.tools/git-hooks/install-headmove-guard.sh` (mirrors install-owned-paths.sh).

      - Install the hook script as `.git/hooks/reference-transaction` (the real git hook name -- non-negotiable).
      - If a `reference-transaction` hook already exists (e.g. from another lane), chain/append rather than clobber, or surface the conflict -- do NOT silently overwrite.
      - Idempotent: re-run safe; does not duplicate.
      - Echo the install location + a verification result (hook present + executable).
    </step>

    <step>
      Phase 3 -- Windows Git Bash 3.6.7 compatibility.

      Per CLAUDE.md Rule 16, use only utilities that ship with the Git Bash 3.6.7 default install.
      - Available: bash 5.3.9, ps, awk, sed, grep, find, timeout, curl, xargs, mktemp, realpath, stdbuf, tee, jq (workspace-local), git, python/python3, aws.
      - NOT available: pgrep, pkill, flock, pidof, setsid, wget -- do NOT use without a `command -v` guarded fallback.
      Test on Andrew's Windows Git Bash environment (or an equivalent dev env).
    </step>

    <step>
      Phase 4 -- empirical validation. Use a synthetic test repo (or a throwaway worktree) for fixtures. Cover both the topology discriminator AND the load-bearing scoping:
      - F1 (reset, destructive): `git reset --hard origin/CLOUD` from a position with local commits ahead -- aborts (exit 1) + lists the discarded commits to stderr.
      - F2 (force override): `FORCE_HEADMOVE=1 git reset --hard origin/CLOUD` -- proceeds + appends a FORCE-HEADMOVE line to `org/git-author-override-audit.log`.
      - F3 (rebase, destructive): a `git rebase` that drops or rewrites a local commit -- aborts unless forced (covered by the unified design).
      - F4 (amend, destructive): `git commit --amend` -- aborts unless forced (covered by the unified design).
      - F5 (normal commit -- MUST NOT flag): an ordinary `git commit` (old IS an ancestor of new) -- proceeds silently. Correctness boundary.
      - F6 (fast-forward -- MUST NOT flag): a fast-forward `git merge` / `git pull` -- proceeds silently.
      - F7 (unstage -- MUST NOT flag): `git reset HEAD <path>` (HEAD SHA unchanged) -- proceeds silently, no false positive.
      - F8 (branch creation -- MUST NOT flag): `git checkout -b <new>` / `git branch <new>` (`old-sha` all-zero) -- proceeds silently.
      - F9 (idempotent install): the install script run twice does not duplicate the hook.
    </step>

    <step>
      Commit + push. Update `org/projects/REGISTRY.md` ADHC_OWNPTH row to reflect the .010 unified-HEAD-move-guard ship.
    </step>
  </scope>

  <acceptance_criteria>
    1. `.tools/git-hooks/headmove-guard` (or AE's coherent equivalent name) ships; executable; correct shebang; Git Bash 3.6.7 compatible.
    2. `.tools/git-hooks/install-headmove-guard.sh` ships; idempotent; installs the guard as `.git/hooks/reference-transaction`; does not silently clobber a pre-existing reference-transaction hook.
    3. F1: a destructive `git reset --hard origin/CLOUD` from a position with local commits aborts (exit 1) + lists the discarded commits to stderr.
    4. F2: `FORCE_HEADMOVE=1` (override) proceeds + appends a FORCE-HEADMOVE line to `org/git-author-override-audit.log`.
    5. F3 + F4: a destructive `git rebase` and a `git commit --amend` are both gated by the same guard (abort unless forced) -- the unified-guard coverage.
    6. F5 + F6 + F7 + F8: a normal commit, a fast-forward merge, a `git reset HEAD <path>` unstage, and a branch creation are all UNAFFECTED -- no false-positive abort. This is the load-bearing correctness boundary.
    7. Works on Windows Git Bash 3.6.7 (CLAUDE.md Rule 16).
    8. F9: the install script is idempotent; re-run is safe.
    9. Audit log format: `YYYY-MM-DDTHHMMSSZ FORCE-HEADMOVE <serial> <prior-HEAD-sha> -> <target-sha> (<N> discarded)`.
    10. SCOPE: the guard covers `git reset`, `git rebase`, and `git commit --amend` BY DESIGN -- a unified destructive-HEAD-move guard. This is CORRECT coverage (one mechanism, one risk class -- destructive HEAD-moves that discard or rewrite local commits), per the CTO Option-(a) ruling 2026-05-15; it is NOT a scope overreach, and rebase/amend must not be excluded (they are topologically indistinguishable from a destructive reset). OUT OF SCOPE -- do NOT implement here; different mechanisms, separate hooks if they recur: force-push (a `pre-push` hook concern) and force-checkout / detached-HEAD discards.
    11. Session log Compiler Tools section reproduces each `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail.
    12. RAVC2 to COO with: commit SHA, install-script invocation result, all F1-F9 fixture outputs (pass/fail), and the Windows Git Bash 3.6.7 compatibility verification.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>cat .tools/git-hooks/owned-paths-check.sh | head -50</run>
        <expect>The existing hook pattern is visible -- audit-log writes, override env-var pattern, error-exit semantics. Mirror it.</expect>
        <if_mismatch>If the hook is missing, ADHC_OWNPTH.002 did not ship properly; surface to COO before authoring.</if_mismatch>
      </step>
      <step>
        <run>git --version</run>
        <expect>Informational. The reference-transaction hook is present in all modern git -- AE 0.5.0 verified the abort behavior empirically on git 2.54.0.windows.1. There is no pre-reset hook at any version; do not look for one.</expect>
        <if_mismatch>n/a (informational)</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>.tools/git-hooks/install-headmove-guard.sh; ls -la .git/hooks/reference-transaction</run>
        <expect>The install script runs cleanly; the reference-transaction hook is installed + executable.</expect>
        <if_mismatch>Install failed; debug.</if_mismatch>
      </step>
      <step>
        <run>git rev-list HEAD ^origin/CLOUD | wc -l</run>
        <expect>The count of local-only commits; informational. If &gt;0, the F1 fixture is testable directly; if 0, the fixture needs a synthetic local commit created first.</expect>
        <if_mismatch>n/a (informational)</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure git-workflow tooling; no S3/data side-effects; no reprocessing required.</no_reprocess_needed>
  </data_reprocess_scope>

  <dependencies>
    None. AE 0.5.0's Phase-1 probe is complete and the corrected design is fully scoped. SXPL_RESTIN.002 was AE 0.5.0's P1 and has shipped -- .010 is clear to execute.
  </dependencies>
</task_order>
