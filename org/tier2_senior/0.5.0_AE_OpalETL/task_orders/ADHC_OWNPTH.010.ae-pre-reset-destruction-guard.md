<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_OWNPTH.010</id>
    <project>ADHC_OWNPTH</project>
    <title>Unified destructive-HEAD-move guard -- a git() shell-shadow function gating reset/rebase/amend operations that discard or rewrite local-only commits</title>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <revised>2026-05-18 -- MECHANISM RE-RULED by CTO (Option A, 20260518T~14:00Z). The reference-transaction hook mechanism is WITHDRAWN: AE 0.5.0's Phase-4 fixtures empirically proved that installing ANY reference-transaction hook -- including a trivial exit-0 no-op -- deterministically hangs `git rebase` on git 2.54.0/Windows Git Bash (7/7 hang WITH hook, 4/4 OK WITHOUT). The guard is now a `git()` shell-shadow FUNCTION auto-loaded from `~/.bashrc`. COO rewrote scope (Phases 1-5) + acceptance criteria for the new mechanism. The Phase-1 headmove-guard topology engine AE already built (merge-base --is-ancestor discriminator, discarded-set reporting, FORCE-HEADMOVE audit) is preserved as the function body -- only the install vector changed. This is the second empirical mechanism correction in the .010 arc (the pre-reset-hook premise fell in Phase 1; the reference-transaction install-side-effect premise falls now) -- the probe process working, not a scoping failure.</revised>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-18 on the CTO Option-A re-ruling. AE 0.5.0 was held at Phase 2 commit pending this rewrite; resume now. No external gate.</dispatch_unblock_condition>
    <priority>medium</priority>
    <estimated_effort>~0.5d -- the topology engine is built (Phase 1 reusable); the new work is the git()-function wrapper shell, the ~/.bashrc installer, and the re-run fixtures.</estimated_effort>
  </metadata>

  <references>
    <ref type="cto_ruling_original">CTO ruling MCP 20260508T~PM -- ship a structural mitigation for the destructive-HEAD-move incident class. The original "pre-reset" hook sketch was empirically wrong (no such hook exists).</ref>
    <ref type="ae_phase1_probe">0.5.0_AE_OpalETL Phase-1 synthetic-repo probe 20260515T183713Z -- git has NO pre-reset hook at any version; reference-transaction fires on git reset and exit 1 at state=prepared aborts it cleanly; the hook is command-blind so topology is the only discriminator.</ref>
    <ref type="ae_phase4_hang_finding">0.5.0_AE_OpalETL Phase-4 finding 2026-05-18 -- NEW EMPIRICAL EVIDENCE. Installing ANY reference-transaction hook deterministically hangs `git rebase` on git 2.54.0.windows.1/Windows Git Bash: rebase WITH hook 7/7 HANG (trivial exit-0 no-op, cat-then-exit0, the headmove-guard -- all identical), WITHOUT hook 4/4 OK; merge --ff WITH hook flaky-hangs 1/4; reset/commit/amend/cherry-pick/branch-create WITH hook all OK. The hang is caused by the hook's PRESENCE, not its logic. Reproducible: .runtmp/hook_isolation.sh + op_matrix.sh + confirm_determinism.sh.</ref>
    <ref type="cto_ruling_optionA">CTO re-ruling 20260518 -- Option A ACCEPT, Option-(a) reference-transaction hook WITHDRAWN. The mechanism is a `~/.bashrc`-autoloaded `git()` shell-shadow function. This resolves the CTO session-25 Option-(c) rejection: that rejection characterized a wrapper as a discretionary "remember-to-invoke" tool (the safe-commit.sh shape) and was premised on a working reference-transaction hook as the real structural alternative. A shell function that SHADOWS the `git` command itself, auto-loads into every Bash-tool shell, and intercepts every git reset/rebase/commit --amend with zero agent action is categorically structural -- typing `git` IS the trigger. On a platform with no usable pre-reset hook, a .bashrc git-shadow is as structural as achievable. Five implementation constraints (install vector / recursion guard / subcommand precision / coverage boundary / escape hatch) are baked into the scope + ACs below.</ref>
    <ref type="anchor_incident_3rd_class">2026-05-08 git-reset incident: AE 0.7 mid-FIRMSEP.07/.08 deploy. Reset to origin/CLOUD discarded 3 local commits (b2ebd19d6, c42105381, 2bd593627). 10 AWS resources destroyed by a parallel TF apply on rolled-back .tf. Recovered cleanly but recurrence risk material.</ref>
    <ref type="prior_art_pattern">.tools/git-hooks/owned-paths-check.sh + install-owned-paths.sh (ADHC_OWNPTH.002 -- same lane; audit-log + idempotent-installer + override-env pattern to mirror) and .tools/safe-commit.sh (ADHC_OWNPTH.007 -- the --force / FORCE-BYPASS audit-log escape-hatch pattern to mirror).</ref>
    <ref type="prior_incident_1">2026-04-22 Andrew "this keeps happening" -- feedback_structural_commit_hygiene.md</ref>
    <ref type="prior_incident_3">2026-04-27/28 record-terraform-deploy.sh sweep x3 -> ADHC_OWNPTH.007 -> safe-commit.sh wrapper</ref>
  </references>

  <context>
    Third-class git-incident occurrence: a destructive HEAD-move during heavy multi-agent sessions discards or rewrites local-only commits without warning. The incident class spans `git reset <ref>` (the 2026-05-08 reset to origin/CLOUD) and -- by the same topology mechanism -- `git rebase` and `git commit --amend`. Existing safe-commit.sh (ADHC_OWNPTH.007) prevents commit-time index contamination but does not gate destructive HEAD-move operations.

    2026-05-08 incident severity: 10 AWS resources destroyed by a parallel TF apply running on rolled-back .tf state during AE 0.7's reset window. Recovery worked but each recovery is non-trivial; the next occurrence may not recover cleanly.

    MECHANISM -- TWO empirical corrections, now final (CTO Option A, 2026-05-18):
    - Correction 1 (Phase 1): git has no `pre-reset` hook at any version.
    - Correction 2 (Phase 4): the `reference-transaction` hook -- the only hook that fires on `git reset` -- cannot be used: its mere installation deterministically hangs `git rebase` on Windows Git Bash. AC2-as-hook-install is dead.
    - FINAL MECHANISM: a `git()` shell-shadow function, auto-loaded from `~/.bashrc`. It shadows the `git` command in every Bash-tool shell, dispatches on the subcommand, runs the topology pre-check for the destructive subcommands (reset / rebase / commit --amend), and aborts-or-proceeds. It hangs nothing -- it is ordinary shell code, not a git-internal hook. The Phase-1 headmove-guard topology engine (merge-base --is-ancestor discriminator + discarded-set rev-list + FORCE-HEADMOVE audit) is the function body; only the install/dispatch vector is new.

    Design pattern: mirror owned-paths-check.sh + safe-commit.sh -- a structural intercept + an audit log + a force-flag escape hatch. Detect the discarded/rewritten-commit set, list it to stderr, require an explicit override to proceed.
  </context>

  <scope>
    <step>
      Phase 1 -- author the git() shell-shadow function (CORRECTED MECHANISM -- Option A).

      File: `.tools/git-hooks/headmove-guard.sh` (the guard logic + the `git()` function definition; AE may pick a coherent name -- NOT a `.git/hooks/` hook name, this is shell code sourced into the environment, not a git hook).

      The function shadows `git`. Required behavior:
      1. SUBCOMMAND DISPATCH. Inspect the subcommand ($1) and args. Run the topology pre-check ONLY for: `git reset`, `git rebase`, `git commit --amend`. Every other invocation (including plain `git commit`, `git merge`, `git pull`, `git fetch`, `git checkout`, `git branch`, `git status`, ...) passes straight through to `command git` untouched.
      2. SUBCOMMAND PRECISION (CTO constraint 3). For `rebase`, gate ONLY a fresh rebase start. `git rebase --continue`, `git rebase --abort`, `git rebase --skip`, `git rebase --edit-todo` are continuations of an in-progress rebase, NOT fresh HEAD-move starts -- they pass straight through ungated. (This is a precision improvement over the command-blind hook.)
      3. RECURSION GUARD (CTO constraint 2). EVERY git call inside the function body -- the topology check, rev-list, merge-base, the final pass-through invocation -- MUST use `command git`, never bare `git`. Bare `git` re-enters the function = infinite recursion. This is load-bearing.
      4. TOPOLOGY DISCRIMINATOR (the Phase-1 engine, reused). For the gated subcommand, derive the would-be (old-HEAD, new-HEAD) pair and apply: `command git merge-base --is-ancestor <old> <new>` -- if old IS an ancestor of new (fast-forward / ordinary advance) it is NOT destructive, proceed silently; if old is NOT an ancestor of new, commits reachable from old are discarded or rewritten = DESTRUCTIVE. The per-subcommand derivation of the (old,new) pair (reset: old=HEAD, new=resolved target ref; commit --amend: old=HEAD, new=the rewritten commit; rebase: the pre-start determination of whether the rebase drops/rewrites local commits) is AE's design -- the Phase-1 headmove-guard Pass-1/Pass-2 logic AE confirmed reusable. If pre-execution determination for `rebase` proves genuinely undecidable, surface to COO rather than silently degrading to "gate-all-rebases."
      5. ON A DESTRUCTIVE MOVE: compute the discarded/rewritten set (`command git rev-list <new>..<old>`), print it (hash + author + subject + relative-age) to stderr under a clear "ABORTED: destructive HEAD-move would discard N local commit(s)" banner, then check the escape hatch (CTO constraint 5): if `FORCE_HEADMOVE=1` is set, proceed (`command git "$@"`) AND append a FORCE-HEADMOVE line to `org/git-author-override-audit.log`; if not set, return non-zero WITHOUT calling `command git` (the destructive op never runs).

      The reset / rebase-fresh-start / amend gating + the must-NOT-flag boundary (ordinary commit, fast-forward, unstage, branch creation -- see Phase 4) is the correctness boundary; a false positive blocks ordinary work.

      Audit log line format (mirrors safe-commit.sh / owned-paths-check.sh):
      `YYYY-MM-DDTHHMMSSZ FORCE-HEADMOVE <serial> <prior-HEAD-sha> -> <target-sha> (<N> discarded)`
    </step>

    <step>
      Phase 2 -- author the idempotent ~/.bashrc installer (CTO constraint 1).

      File: `.tools/git-hooks/install-headmove-guard.sh` (mirrors install-owned-paths.sh).
      - `~/.bashrc` is user-local, NOT repo-tracked -- the installer appends a guarded block to `~/.bashrc` that sources `.tools/git-hooks/headmove-guard.sh` (or inlines the git() function -- AE's call; sourcing the tracked file is preferred so updates flow without re-install).
      - Double-append guard: a sentinel comment marker; re-run must NOT duplicate the block. Idempotent.
      - Echo install location + a verification result (the git() function is defined in a fresh `bash -lic` shell).
      - Also add a one-line entry to `org/XXX.md` Step-1b (the owned-paths-hook-install precedent -- ADHC_OWNPTH.002 added its line there) so every agent runs the installer on startup. If the owned-paths pre-commit hook blocks the XXX.md edit as out-of-lane, surface to COO -- do not force past it.
    </step>

    <step>
      Phase 3 -- Windows Git Bash 3.6.7 compatibility (CLAUDE.md Rule 16).
      Use only utilities in the Git Bash 3.6.7 default install -- available: bash 5.3.9, ps, awk, sed, grep, find, timeout, curl, xargs, mktemp, realpath, stdbuf, tee, jq, git, python/python3, aws. NOT available without a `command -v` guarded fallback: pgrep, pkill, flock, pidof, setsid, wget. Test on Windows Git Bash (or an equivalent dev env).
    </step>

    <step>
      Phase 4 -- empirical validation (synthetic test repo / throwaway worktree). Cover the topology discriminator, the must-NOT-flag boundary, the new subcommand-precision cases, AND the regression that killed the old mechanism:
      - F1 (reset, destructive): `git reset --hard origin/CLOUD` from a position with local commits ahead -- aborts (non-zero) + lists the discarded commits to stderr; the reset does NOT run.
      - F2 (force override): `FORCE_HEADMOVE=1 git reset --hard origin/CLOUD` -- proceeds + appends a FORCE-HEADMOVE line to `org/git-author-override-audit.log`.
      - F3 (rebase, destructive): a `git rebase` that drops/rewrites a local commit -- aborts unless forced.
      - F4 (amend, destructive): `git commit --amend` -- aborts unless forced.
      - F5 (normal commit -- MUST NOT flag): an ordinary `git commit` (old IS an ancestor of new) -- proceeds silently.
      - F6 (fast-forward -- MUST NOT flag): a fast-forward `git merge` / `git pull` -- proceeds silently.
      - F7 (unstage -- MUST NOT flag): `git reset HEAD <path>` (HEAD SHA unchanged) -- proceeds silently, no false positive.
      - F8 (branch creation -- MUST NOT flag): `git checkout -b <new>` / `git branch <new>` -- proceeds silently.
      - F9 (idempotent install): the installer run twice does not duplicate the ~/.bashrc block.
      - F10 (rebase continuation -- MUST NOT gate): `git rebase --continue` / `--abort` / `--skip` pass straight through ungated (CTO constraint 3).
      - F11 (NO HANG -- the regression test): with the git() guard active, `git rebase` COMPLETES and does not hang. This is the explicit regression gate against the withdrawn reference-transaction mechanism -- run it under a `timeout` and assert completion, mirroring AE's Phase-4 matrix. `git merge --ff` / `git pull` likewise complete (no flaky hang).
      - F12 (recursion guard): the git() function's internal git calls use `command git` -- a gated invocation completes and does not stack-overflow / infinite-loop.
    </step>

    <step>
      Phase 5 -- commit + push. Update `org/projects/REGISTRY.md` ADHC_OWNPTH row to reflect the .010 git()-shadow unified-HEAD-move-guard ship. (The ADHC_OWNPTH PRD .010 mechanism-description correction is handled by COO -- do not edit the PRD in this TO.)
    </step>
  </scope>

  <coverage_boundary note="CTO constraint 4 -- accepted + documented, NOT hidden">
    The git() shell-shadow protects Bash-tool shells that source `~/.bashrc`. It does NOT protect: PowerShell-tool git invocations; explicit `command git ...`; absolute-path git invocations; or any shell that does not source `~/.bashrc`. This residual is ACCEPTED -- a working narrow guard beats a hanging complete one, and agents run destructive git in the Bash tool, not PowerShell. The TO documents it explicitly here and the boundary must be stated plainly in the ADHC_OWNPTH PRD (COO) -- it must NOT be presented or logged as full coverage.
  </coverage_boundary>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>sed -n '1,60p' .tools/safe-commit.sh</run>
        <expect>The safe-commit.sh --force / FORCE-BYPASS audit-log escape-hatch pattern is visible -- mirror it for FORCE_HEADMOVE + the org/git-author-override-audit.log append.</expect>
        <if_mismatch>If safe-commit.sh is absent, ADHC_OWNPTH.007 did not ship; surface to COO before authoring.</if_mismatch>
      </step>
      <step>
        <run>sed -n '1,40p' .tools/git-hooks/install-owned-paths.sh</run>
        <expect>The idempotent-installer + sentinel-marker pattern is visible -- mirror it for the ~/.bashrc append guard.</expect>
        <if_mismatch>If install-owned-paths.sh is absent, ADHC_OWNPTH.002 did not ship; surface to COO.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>bash .tools/git-hooks/install-headmove-guard.sh; bash -lic 'type git'</run>
        <expect>The installer runs cleanly; in a fresh login shell `type git` reports `git is a function` -- the shadow is active.</expect>
        <if_mismatch>The ~/.bashrc append or the function definition failed; debug before closing.</if_mismatch>
      </step>
      <step>
        <run>command git rev-list HEAD ^origin/CLOUD | wc -l</run>
        <expect>The count of local-only commits; informational -- if &gt;0 the F1 fixture is testable directly, if 0 create a synthetic local commit first. Note `command git` is used so the count is not itself gated.</expect>
        <if_mismatch>n/a (informational)</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    1. `.tools/git-hooks/headmove-guard.sh` ships -- defines the `git()` shell-shadow function; executable/sourceable; correct shebang; Git Bash 3.6.7 compatible.
    2. `.tools/git-hooks/install-headmove-guard.sh` ships -- idempotent; appends a sentinel-guarded block to `~/.bashrc` that activates the git() shadow; re-run does not duplicate; adds the `org/XXX.md` Step-1b install line. (AC2 is rewritten from the withdrawn "install as .git/hooks/reference-transaction" -- the install vector is `~/.bashrc`, per CTO Option A.)
    3. F1: a destructive `git reset --hard origin/CLOUD` from a position with local commits aborts (non-zero) + lists the discarded commits to stderr + the reset does not run. (AC3 re-examined vs the new mechanism: PASSES -- the git() function intercepts pre-execution and returns non-zero without calling `command git`.)
    4. F2: `FORCE_HEADMOVE=1` proceeds + appends a FORCE-HEADMOVE line to `org/git-author-override-audit.log`.
    5. F3 + F4: a destructive `git rebase` and a `git commit --amend` are both gated by the same git() guard (abort unless forced).
    6. F5 + F6 + F7 + F8: a normal commit, a fast-forward merge, a `git reset HEAD <path>` unstage, and a branch creation are all UNAFFECTED -- no false-positive abort. (AC6 re-examined vs the new mechanism: PASSES -- subcommand dispatch + the topology discriminator only gate genuine destructive moves; the must-not-flag set passes straight to `command git`.)
    7. F10: `git rebase --continue` / `--abort` / `--skip` pass through ungated (subcommand precision -- CTO constraint 3).
    8. F11: with the guard active, `git rebase` and `git merge --ff` / `git pull` COMPLETE and do not hang -- the explicit regression gate against the withdrawn reference-transaction mechanism (run under `timeout`, assert completion).
    9. F12: the recursion guard holds -- the git() function's internal git calls use `command git`; a gated invocation completes without infinite recursion.
    10. Works on Windows Git Bash 3.6.7 (CLAUDE.md Rule 16).
    11. F9: the installer is idempotent; re-run is safe.
    12. Audit log format: `YYYY-MM-DDTHHMMSSZ FORCE-HEADMOVE <serial> <prior-HEAD-sha> -> <target-sha> (<N> discarded)`.
    13. SCOPE + COVERAGE BOUNDARY: the guard covers `git reset`, fresh `git rebase`, and `git commit --amend` via the git() shadow -- one mechanism, one risk class. The coverage_boundary block (PowerShell / `command git` / absolute-path / non-~/.bashrc shells are NOT protected) is documented in the session log + RAVC2 and NOT presented as full coverage. OUT OF SCOPE: force-push (pre-push concern), force-checkout / detached-HEAD discards.
    14. Session log Compiler Tools section reproduces each `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail.
    15. RAVC2 to COO with: commit SHA, installer invocation result, all F1-F12 fixture outputs (pass/fail), the no-hang (F11) evidence explicitly, and the Windows Git Bash 3.6.7 compatibility verification.
  </acceptance_criteria>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure git-workflow tooling; no S3/data side-effects; no reprocessing required.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    <none/> -- .010 ships shell tooling under `.tools/git-hooks/` + an `~/.bashrc` installer + a REGISTRY row. No overlap with the active INFGRO / INFETL / INFINC / TXNAMG TOs (none touch `.tools/git-hooks/`). The `org/XXX.md` Step-1b edit is the only shared file; it is an append of one line, the ADHC_OWNPTH.002 precedent.
  </cross_domain_coordination>

  <dependencies>
    None. AE 0.5.0's Phase-1 topology engine + Phase-4 hang-matrix are complete; the CTO Option-A re-ruling is final. Clear to execute.
  </dependencies>
</task_order>
