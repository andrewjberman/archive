<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_DSFLOW.005</id>
    <project>ADHC_DSFLOW</project>
    <title>safe-deploy gate extension — atomic commit + push + S3 deploy + comp-pipescript verify; structurally close the deployment-discipline gap that CLAUDE.md rule 13 currently leaves cultural; fold INF coverage gap into scope</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>~4-6h (design + implementation + INF coverage + tests + memory entry)</estimated_effort>
    <authorized_by>1.0.0_SA_CTO ratified 2026-05-11 (workspace-wide scope; AE 0.7 owner per .tools/ git-hooks precedent — safe-commit.sh OWNPTH.007, git-hooks install OWNPTH.003, ds-commit-gate.sh DSFLOW.001)</authorized_by>
  </metadata>

  <references>
    <ref type="parent_incident">DS~B discovery 2026-05-11 — DS~A's `c2a7a5967` (ACCOUNT-ID-COERCE) committed + pushed to CLOUD but NEVER deployed to `s3://opal-data-inf/code/gold/`. 5 of 6 affected gold scripts stale (2026-04-29 S3 timestamps); `lib/dtype_coerce.py` MISSING entirely. Severity HIGH (no incorrect data in PROD, but next PROD trigger would expose).</ref>
    <ref type="parent_rule">CLAUDE.md rule 13 — "DS owns the gold-script commit→QA-deploy cycle — including S3 upload." Today CULTURAL. This TO makes it STRUCTURAL.</ref>
    <ref type="related_ds_to">ADVI_INFNNA.ID-DTYPE-ENFORCEMENT (`ffd42171c`) — DS~B's AST detection rule extending `ds-precommit-check.py`. Detection layer; this TO is the wrapper-infrastructure layer. Different layers, same defense-in-depth philosophy.</ref>
    <ref type="precedent_safe_commit">.tools/safe-commit.sh — AE 0.7 ADHC_OWNPTH.007. Same architectural pattern: atomic wrapper enforcing structural-not-cultural discipline. `--force` audit-logged bypass is the model for `--allow-stale` here.</ref>
    <ref type="precedent_ds_gate">.tools/ds-commit-gate.sh — AE 0.7 ADHC_DSFLOW.001 (py_compile + ds-precommit-check + ruff). This TO extends the same pattern to S3-deploy.</ref>
    <ref type="ds_b_workaround">DS~B used manual `hashlib.sha256` for INF deploys since `comp-pipescript deployed` is hardcoded for BD paths only. Workaround works; structural fix preferred. Folded into this TO's scope.</ref>
  </references>

  <context>
    **The gap.** CLAUDE.md rule 13 mandates DS commit → push → `aws s3 cp` → `comp-pipescript deployed` MATCH → SSM dispatch. Today's `ds-commit-gate.sh` enforces the first half (py_compile + AST scan + ruff) but stops at commit. The S3 deploy + verify steps are cultural — agents must remember to execute them.

    On 2026-05-11 a DS agent shipped 6 gold script edits to CLOUD without S3 deploy, only caught when a downstream agent's SSM dispatch failed on `ModuleNotFoundError`. Empirical proof that cultural discipline alone is insufficient under heavy multi-agent MCP cycles — same incident class as 2026-04-27 commit-sweep cases that drove `safe-commit.sh`.

    **Structural solution.** Atomic `safe-deploy.sh` wrapper that does commit + push + S3 deploy + verify in one indivisible call. Agent can't accidentally push without deploying. Bypass via `--allow-stale` writes audit-log entry (same shape as `safe-commit.sh --force`).

    **Two implementation options (AE picks):**

    **Option A — wrapper script** (`.tools/safe-deploy.sh`): explicit invocation. Most discoverable; matches existing tools pattern. Easy to teach + audit.

    **Option B — pre-push git hook**: invisible. Fires on any `git push` if a `data/*/scripts/{gold,silver,bronze,lib}/*.py` is in the diff. More opaque but harder to forget. Bypass via `git push --no-verify` is audit-loggable.

    **Option C — hybrid**: pre-push hook calls `safe-deploy.sh` internally. Best of both — opaque enforcement, explicit named script for diagnostics.

    AE 0.7 picks based on existing pattern fit with `safe-commit.sh` + `owned-paths` infrastructure.

    **Workspace-wide scope intentional.** This is NOT INFNNA-specific. BD + INF + future Cottonwood all use the same DS commit→deploy cycle. The gap is in the rule-13 enforcement primitive, not in any pipeline-specific code. ADHC_DSFLOW family is the right home — continuing the .001-.004 surface.

    **INF coverage gap folded in.** DS~B flagged that `comp-pipescript deployed` is hardcoded for `s3://opal-data-bd/code/...` paths and ignores INF. They used manual `hashlib.sha256` as workaround. Since this TO's gate calls `comp-pipescript deployed`, the INF coverage must work or the gate is incomplete. Fold the comp-pipescript INF-coverage fix into scope (Step 5 below) so AE doesn't ship a half-working gate.
  </context>

  <scope>
    <step>
      **Design decision.** Pick A / B / C from context. Document rationale in design note before implementation. Match existing patterns (safe-commit.sh, ds-commit-gate.sh, owned-paths hook).
    </step>

    <step>
      **Diff detection — what triggers the gate.** Detect when a commit / push includes any of:
      - `data/*/scripts/gold/*.py`
      - `data/*/scripts/silver/*.py`
      - `data/*/scripts/bronze/*.py`
      - `data/*/scripts/{gold,silver,bronze}/lib/*.py` (shared helpers)
      - Any other `data/*/scripts/.../*.py` location surfaced by audit

      Output: file-glob list + corresponding S3 prefix mapping table baked into the gate.
    </step>

    <step>
      **S3 deploy phase.** For each matched file in the diff:
      - Resolve pipeline → S3 bucket (e.g., `bd-pipeline` → `opal-data-bd`, `inf-pipeline` → `opal-data-inf`)
      - `aws s3 cp` local → `s3://{bucket}/code/{layer}/{path}` (where layer ∈ {gold, silver, bronze}, and lib/ preserves the relative path)
      - SHA256 verify local file == downloaded S3 copy
      - Fail fast on any mismatch; do not partial-deploy

      Idempotent across re-runs (safe to retry on transient S3 errors).
    </step>

    <step>
      **`comp-pipescript deployed` verify phase.** Invoke `comp-pipescript deployed` for each affected script. Expect MATCH for all. Fail the gate if any STALE / MISSING / MISMATCH.
    </step>

    <step>
      **INF coverage fix in `comp-pipescript deployed` — folded into scope (CTO 2026-05-11).** DS~B finding: current implementation hardcoded for `s3://opal-data-bd/code/...`. Extend to:
      - Recognize INF pipeline → `s3://opal-data-inf/code/...`
      - Future-proof for additional pipelines (Cottonwood, etc.) — table-driven pipeline → S3 prefix mapping
      - Backward-compatible with current BD callers
      - Repro the original issue: `comp-pipescript deployed --pipeline inf-gold INF_D_04` should fetch from `s3://opal-data-inf/code/gold/`, not fall through to BD. V4.019 fixed UnboundLocalError on this exact command but the underlying path resolution may still be broken.
      - Verify via test: deploy a file to INF S3 → run `comp-pipescript deployed` → expect MATCH

      If scope expands materially, AE RAVC1 for split into separate `.006.ae-comp-pipescript-deployed-inf-coverage`.
    </step>

    <step>
      **`--allow-stale` bypass mechanism.** Same shape as `safe-commit.sh --force`:
      - Bypass requires explicit flag
      - Writes audit-log entry to `org/git-author-override-audit.log` (or new `org/safe-deploy-bypass-audit.log`) with timestamp + author + pathspec + commit SHA + bypass reason
      - Use cases: emergency hotfix when comp-pipescript is broken, intentional code-only changes (docstring updates, comment-only), multi-agent worktree contention.
    </step>

    <step>
      **Tests.** Synthetic fixture suite at `.tools/test_fixtures/safe-deploy/` covering:
      - **PASS:** gold script edit → deploy succeeds → verify MATCH
      - **FAIL (no deploy):** simulate push without S3 step → gate ERROR
      - **FAIL (deploy partial):** simulate one file deploy succeeded, another failed → gate ERROR + rollback / no partial-state
      - **FAIL (mismatch SHA):** simulate corrupted upload → SHA check catches
      - **BYPASS:** `--allow-stale` → gate WARN + audit-log entry written
      - **INF path:** explicit test exercising the path-resolution-not-BD-fallthrough fix from Step 5

      Test runner at `.tools/test_safe_deploy.py` (parallel to existing `.tools/test_ds_precommit_check.py` if it exists, or new).
    </step>

    <step>
      **CLAUDE.md rule update.** Coordinate with CTO on rule 13 + 14 wording. Likely:
      - Rule 13 sentence: "...via `.tools/safe-deploy.sh` (atomic commit + push + S3 + verify; see ADHC_DSFLOW.005)."
      - Rule 14 sentence: "Pre-commit gate via `.tools/ds-commit-gate.sh` runs py_compile + ds-precommit-check + ruff. For `data/*/scripts/.../*.py` edits, the deploy cycle is enforced by `.tools/safe-deploy.sh`."

      Surface draft wording to CTO before commit; expect minor tweaks.
    </step>

    <step>
      **Memory entry — author under AE 0.7 serial.** Path: `.../memory/feedback_safe_deploy_gate.md`. Documents:
      - The cultural-vs-structural-discipline pattern (regression-guard-alongside-correctness-fix dimension #3 — already being crystallized under COO serial; cross-reference)
      - When to bypass (audit-loggable cases)
      - Common failure modes + recovery

      Cross-link to COO's `feedback_regression_guard_alongside_correctness_fix.md` (drafting now).
    </step>

    <step>
      **Commit + push + RAVC.**
      - All edits under AE 0.7 author identity
      - Bundle: wrapper script + comp-pipescript fix + test fixtures + memory entry + CLAUDE.md rule edit (CTO-coordinated)
      - RAVC payload: design choice (A/B/C), test results, INF coverage repro before/after, CLAUDE.md rule edit outcome, bypass-log path
    </step>
  </scope>

  <acceptance_criteria>
    1. **Design decision** (A/B/C) documented with rationale.
    2. **Diff detection** correctly identifies all `data/*/scripts/.../*.py` triggers via test cases.
    3. **S3 deploy phase** idempotent; partial-deploy failure is safe (no half-state).
    4. **`comp-pipescript deployed` verify** integrated; gate fails on STALE/MISSING.
    5. **INF coverage fix** PASS — `comp-pipescript deployed --pipeline inf-gold INF_D_04` correctly fetches INF bucket; repro of DS~B's manual-hashlib workaround eliminated.
    6. **`--allow-stale` bypass** audit-logged; entry includes author + pathspec + commit SHA + reason.
    7. **6 synthetic fixtures** (PASS, FAIL-no-deploy, FAIL-partial, FAIL-mismatch, BYPASS, INF-path) all behave as designed.
    8. **100% PASS** validation against repo state post-DS~A 5-script deploy (today's incident state once cleaned).
    9. **CLAUDE.md rules 13+14 updated** (CTO-coordinated).
    10. **Memory entry** drafted at canonical path with cross-reference to COO's broader regression-guard-pattern entry.
    11. **RAVC delivered** with design rationale + test outcomes + INF coverage demonstration.
  </acceptance_criteria>

  <blocking>
    **Blocked by:** ADVI_INFNNA.ID-DTYPE-ENFORCEMENT (`ffd42171c`) — though different layers (AST detection vs deploy wrapper), the two TOs share the regression-guard-alongside-fix architectural pattern. CTO ratified sequencing: ID-DTYPE-ENFORCEMENT first (closes silver-builder code correctness via AST), then this TO (closes deploy correctness via wrapper). Different layers but same family.

    ID-DTYPE-ENFORCEMENT is itself blocked by SILVER-ID-DTYPE-UNIFY completion. So this TO is 2-deep in the dependency chain.

    Adjacent: today's incident in DS~A's S3 deploy gap is a workaround-resolved real-world test case. After this TO lands, that exact failure class becomes structurally impossible.
  </blocking>

  <notes>
    **Naming rationale (CTO directive 2026-05-11):** workspace-wide scope, not INFNNA-specific. ADHC_DSFLOW family continuation (.001 ds-commit-gate → .002 CLAUDE.md → .003/.004 backfills → **.005 safe-deploy**). The gap surfaced via INFNNA but applies to BD + future Cottonwood equally.

    **Owner rationale (CTO directive 2026-05-11):** AE 0.7 per `.tools/` git-hooks precedent. DS owns AST detection rules (ID-DTYPE-ENFORCEMENT); AE owns wrapper-infrastructure (safe-commit.sh, safe-deploy.sh, ds-commit-gate.sh original, owned-paths hook).

    **Connection to memory pattern (3 instances):** This is the deployment-layer instance of "ship regression guard alongside correctness fix":
    - V4.024 synthetic-workspace test fixture (code-correctness regression guard)
    - ID-DTYPE-ENFORCEMENT pre-commit AST gate (data-shape regression guard)
    - **safe-deploy gate (this TO) — deployment-state regression guard**

    Three dimensions: code / data / deployment. Stable architectural pattern, not coincidence.

    **Empirical test data ready-to-hand:** DS~A's `c2a7a5967` is the canonical "bad commit" — committed without S3 deploy. After this TO ships, re-pushing equivalent state should ERROR at the gate with clear actionable message.
  </notes>
</task_order>
