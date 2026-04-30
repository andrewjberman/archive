<task_order>
  <metadata>
    <id>ADHC_COMPIL.015.ae-validate-resolver-and-noconfig-semantics</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-30</date>
    <status>complete</status>
    <project_code>ADHC_COMPIL</project_code>
    <theme>F-amendment (v3) — comp-validate UX + correctness fixes surfaced by 2026-04-30 ad-hoc analysis</theme>
    <prd_ref>docs/architecture/ADHC_COMPIL_V3.md (amendment — drafted post-PRD via comp-validate log analysis 2026-04-30 PM)</prd_ref>
    <effort>3–5 days</effort>
    <gates_on>ADHC_COMPIL.009 COMPLETE — .009 lands the Windows path translator on the same file (.tools/comp-validate); .015 builds on top to avoid merge churn.</gates_on>
    <gates_for>None</gates_for>
  </metadata>

  <objective>
    Two contained fixes to `comp-validate` surfaced by 2026-04-30 ad-hoc
    analysis of the past 2 weeks of validate invocations (~85 invocations,
    ~33% FAIL rate — high relative to other comp tools):

    Fix 1 (UX): script-id-as-alias resolver. The dominant FAIL pattern (~12
    FAIL→retry pairs in window) is operators passing the producer script-id
    when the validate config is keyed on artifact-id. Examples:
    - `comp-validate D_04 --artifact /tmp/cohort_a_summary.json` → FAIL
    - `comp-validate cohort_a_summary --artifact /tmp/cohort_a_summary.json` → PASS
    Same script (D_04) produces 17 distinct artifacts; agents reach for the
    script-id naturally. The tool should resolve script-id → artifact-id
    when the `--artifact` filename disambiguates, OR emit a precise error
    listing the script's artifact-ids.

    Fix 2 (correctness): missing-artifact / no-config exit semantics. Log
    lines 1776–1777 (2026-04-30 AE 0.7 sandbox testing) show:
    - `comp-validate nonexistent_script --artifact /tmp/nonexistent.json` → PASS
    - `comp-validate fee_earning_aua --artifact /tmp/missing_file_xyz.json` → PASS

    The tool returns exit 0 on a nonexistent script-id AND on a missing
    artifact file. In a CI/dispatcher context where exit 0 means "ship it,"
    this is unsafe: the gate has a hole big enough to ship blank or missing
    output past validation. Distinguish PASS from SKIP/NO-CONFIG/MISSING at
    the exit-code or status-line level.
  </objective>

  <scope>
    Fix 1 — Script-id-as-alias resolver:

    1. Walk `gold_validate_config.yaml` (BD + INF) at resolver init. Build
       a map: script-id → list of artifact-ids that script produces. The
       mapping is sourced from the existing config; no new declaration
       needed. (If a config doesn't already record producer-script per
       artifact, add a `producer_script: <id>` field to each config entry
       — minimal schema extension.)

    2. When invoked with `comp-validate <id> --artifact <path>`:
       a. First try `<id>` as artifact-id (current behavior).
       b. If miss, try `<id>` as script-id → look up artifact-ids that
          script produces.
          - If script produces exactly one artifact-id: silently use it.
            Emit one info line: `Resolved D_04 → cohort_a_summary` so the
            operator sees the alias.
          - If script produces multiple artifact-ids: try to disambiguate
            by matching the `--artifact <path>` basename against each
            artifact-id (e.g. `cohort_a_summary.json` → `cohort_a_summary`).
            On unique match: use it + emit the info line.
            On ambiguous or no filename match: exit 1 with error listing
            all candidate artifact-ids.
       c. If `<id>` is neither an artifact-id nor a script-id: exit 1
          with `difflib.get_close_matches` suggestion (matches the .008
          pattern).

    Example error output (multi-artifact, no filename match):
      `Error: 'D_04' is a script-id, not an artifact-id. D_04 produces 17 artifacts:`
      `  cohort_a_summary, cash_coverage_summary, leaderboard, fee_earning_aua, ...`
      `Pass one of these as the first arg, OR pass --artifact <path>`
      `with a filename matching one of them.`

    Fix 2 — Missing-artifact / no-config exit semantics:

    1. After resolver succeeds: check `--artifact <path>` exists.
       - If file does NOT exist → exit 1 with status line:
         `MISSING_ARTIFACT: <path> not found (post-translation: <translated_path>)`
         (the translated_path piece comes from .009's Windows translator —
         show both for parity with the .009 dual-path error pattern)
       - This is a hard FAIL. The current PASS-on-missing behavior is
         unsafe in CI/dispatcher contexts.

    2. After artifact exists: check the resolved id has a config entry.
       - If no config entry (the `nonexistent_script` case): exit 0 BUT
         emit status line `NO_CONFIG: no validation rules defined for <id>`.
         The exit code is 0 because there's nothing to fail; the status
         line distinguishes from genuine PASS.
       - For dispatcher/CI integration: the dispatcher checks the status
         line, not just the exit code. Add a `--strict` flag that
         escalates NO_CONFIG to exit 2 for callers that want
         no-config-is-an-error semantics.

    3. Distinguish status lines on stdout (machine-readable):
       - `PASS: all <N> checks passed for <artifact_id>` — exit 0
       - `NO_CONFIG: no validation rules defined for <id>` — exit 0 (or
         exit 2 with --strict)
       - `MISSING_ARTIFACT: <path> not found` — exit 1
       - `FAIL: <N>/<M> checks failed for <artifact_id>` — exit 1
       - `BLOCKED: <reason>` — exit 1 (existing semantics)

    4. Update COMP_VALIDATE_PROTOCOL.md (shipped under v1 .006) to
       document the four status lines + the --strict flag. Edit-only —
       no rewrite.

    Both fixes:
    - Single helper module `validate_resolver.py` (or extend existing) for
      the alias map + exit-status logic. Avoid duplicating the lookup
      across code paths.
    - Append one row per AC to `org/compiler-tools-log.md`.
  </scope>

  <acceptance_criteria>
    Fix 1 — Script-id-as-alias resolver:

    1. `comp-validate D_04 --artifact <path>/cohort_a_summary.json` resolves
       to `cohort_a_summary` config and runs checks. Exit 0 if checks pass.
       Stdout includes `Resolved D_04 → cohort_a_summary` info line.

    2. `comp-validate D_04 --artifact <path>/cash_coverage_summary.json`
       resolves to `cash_coverage_summary`. Same behavior.

    3. `comp-validate D_04 --artifact <path>/ambiguous_name.json` (filename
       doesn't match any of D_04's artifact-ids) → exit 1 with error listing
       all 17 D_04 artifact-ids.

    4. `comp-validate D_04` (no --artifact) → exit 1 with same multi-artifact
       error (cannot disambiguate without filename).

    5. `comp-validate cohort_a_summary --artifact ...` (existing behavior,
       direct artifact-id) → unchanged. No info line. Pure regression test.

    6. `comp-validate definitely_not_a_thing --artifact ...` → exit 1 with
       `Did you mean: <closest>?` (preserves .008's closest-match UX).

    Fix 2 — Missing-artifact / no-config:

    7. `comp-validate cohort_a_summary --artifact /tmp/does_not_exist.json`
       → exit 1, status line `MISSING_ARTIFACT: /tmp/does_not_exist.json
       not found` (with translated path from .009 if applicable).

    8. `comp-validate nonexistent_script --artifact <real-existing-file>` →
       exit 1 with the .008-style "Did you mean" error (this case is now
       caught at the resolver, not silently passing through to vacuous
       success).

    9. `comp-validate <real-id-with-no-config> --artifact <real-file>` →
       exit 0, status line `NO_CONFIG: no validation rules defined for <id>`.
       (Synthetic test: introduce a temporary script with no config entry,
       verify status line, revert.)

    10. `comp-validate <real-id-with-no-config> --strict --artifact <real-file>`
        → exit 2 with the same NO_CONFIG status line.

    11. Existing all-pass run: `comp-validate cohort_a_summary --artifact
        <good-cohort_a-output>` → exit 0, status line `PASS: all <N>
        checks passed for cohort_a_summary`.

    12. Existing FAIL run: synthetic bad artifact → exit 1, status line
        `FAIL: <N>/<M> checks failed for cohort_a_summary`.

    13. COMP_VALIDATE_PROTOCOL.md updated with §status-lines section + --strict
        flag documentation. Diff committed.

    14. Test fixture covering all 13 ACs above committed under
        `tests/comp_validate/test_resolver_and_status.sh`.

    15. Append one row per AC to `org/compiler-tools-log.md`.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT start before .009 COMPLETE — same file (.tools/comp-validate); want to avoid merge churn on the artifact-path handler.</rule>
    <rule>Do NOT change the existing PASS / FAIL exit code semantics (0 / 1). The new status lines are additive; the new MISSING_ARTIFACT case promotes from silent-PASS to FAIL (correctness fix, not breaking change).</rule>
    <rule>Do NOT silently auto-pick when D_04 produces multiple artifacts and no filename match — emit the explicit list. Silent auto-pick of "first artifact-id alphabetically" or any heuristic would mask real misuse.</rule>
    <rule>Do NOT make `--strict` the default — back-compat for existing dispatcher integrations. Operators opt in.</rule>
    <rule>Do NOT introduce a separate config schema file for the script-id → artifact-id map. Source it from the existing gold_validate_config.yaml entries (add `producer_script:` field if not already present).</rule>
    <rule>Do NOT use emoji in status lines — CLAUDE.md "Code Quality". Plain ASCII PASS/NO_CONFIG/MISSING_ARTIFACT/FAIL/BLOCKED.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">.tools/comp-validate with script-id alias resolver + exit-status differentiation + --strict flag</deliverable>
    <deliverable type="code">data/black_diamond/scripts/gold/gold_validate_config.yaml — `producer_script:` field added to each artifact entry (if not already present)</deliverable>
    <deliverable type="code">data/orion/scripts/gold/gold_validate_config.yaml — same</deliverable>
    <deliverable type="code">tests/comp_validate/test_resolver_and_status.sh fixture (15 ACs)</deliverable>
    <deliverable type="document">docs/architecture/COMP_VALIDATE_PROTOCOL.md — appended §status-lines + --strict</deliverable>
    <deliverable type="document">Session log with AC1–AC15 verification output</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1+AC2 stdout-diff (alias resolution), AC3+AC4 multi-artifact error excerpt, AC7 MISSING_ARTIFACT exit code, AC9+AC10 NO_CONFIG status differentiation, fixture pass count</deliverable>
  </deliverables>

  <compiler_tools_mandate>
    Phase 1 (before write):
    - Confirm .009 COMPLETE; pull the dual-path error pattern from .009's
      RAVC4 to reuse in MISSING_ARTIFACT formatting
    - Direct read of .tools/comp-validate post-.009 (artifact-path handler
      is the surface .015 extends)
    - Direct read of both gold_validate_config.yaml files to enumerate
      script-id → artifact-id pairs; identify whether `producer_script:`
      is already a field or needs adding

    Phase 2 (before commit):
    - Run all 15 fixture cases; capture exit codes + stdout/status lines
    - Reproduce the original 12 FAIL→retry pairs from log lines 429, 430,
      433, 937, 939, 941, 1108, 1425, 1445, 1496, 1534, 1623 against the
      new resolver — every one of those FAIL cases must now PASS (or
      emit the resolver info line + PASS) without retry
    - Verify the AC7+AC8 cases (line 1776+1777 phantom-pass) now correctly
      exit 1
    - `.tools/ds-commit-gate.sh` on every .py file in change set

    Phase 3 (after commit):
    - Append one row per AC to `org/compiler-tools-log.md`
    - Confirm in next session window that comp-validate FAIL rate drops
      from ~33% to <10% (most current FAILs are the script-id-as-alias
      pattern .015 fixes)
    - Notify DS 0.4 lanes (~A/~B/~C/~D/~E) via MCP that the alias resolver
      is live so they update their session habits
  </compiler_tools_mandate>
</task_order>
