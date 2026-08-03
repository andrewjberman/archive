<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-08-03-monpub-w3</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics (code) + 0.2.0_DT_PortfolioAnalytics (deploy)</issued_to>
    <date>2026-08-03</date>
    <status>pending</status>
    <project_code>MDLP_MONPUB</project_code>
  </metadata>

  <objective>
    Make Pass-type skip branches visible in the DataRefresh status/history UX. Today
    SkipDataPKL/SkipModelPKL/SkipBothPKLs (+ Excel skips) are structurally absent from the steps
    array, so an operator watching the page during the 2026-08-03 incident saw only SUCCEEDED runs.
  </objective>

  <context>
    Spec: docs/architecture/MDLP_MONPUB_MANIFEST_REGRESSION_FIX.md @d59fc15920 section 3 W3.
    infra/aws/lambda/data_refresh/lambda_function.py handle_status(): the history parser (~:862-880)
    checks only TaskStateEntered/TaskStateExited/TaskFailed/ExecutionFailed; STATE_LABELS (~:730-770)
    has no Skip* entries. Add PassStateEntered/PassStateExited handling + STATE_LABELS entries for
    every Skip* state. CVO ADDITION (same pass, cheap): Choice states (Check*) emit
    ChoiceStateEntered/Exited and are equally unparsed -- several existing STATE_LABELS entries are
    dead code because of it; add Choice-state handling too, or explicitly scope the delivered claim
    to Pass-states only. Scope is VISIBILITY ONLY -- no new alarm/notification machinery (moratorium).
    NOTE: an existing deploy-completion ledger for opal-data-refresh-api (07-17) lives in
    org/critical_paths/change_management/ -- open your own entry at deploy start per the NEVER rule.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
      <run>comp-blast data-refresh (under PYTHONIOENCODING=utf-8 -- the tool crashes on cp1252 rendering its HOLD banner otherwise)</run>
      <expect>No extracted downstream consumers (LOWER BOUND -- not provably zero); HOLD claims include the 07-17 deploy ledger</expect>
      <if_mismatch>New consumers appeared = re-scope with CTO</if_mismatch>
    Phase 3 (after deploy):
      <run>curl/invoke the status endpoint for execution ba852138 (2026-08-03 13:22Z, SkipBothPKLs)</run>
      <expect>steps array contains a labeled skip step</expect>
      <if_mismatch>Parser change did not reach the deployed handler -- verify CodeSha256 changed and TF applied 0-diff</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>  <!-- different Lambda from W1/W2/W4; no shared files or keys; same project only -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. DIFFERENTIAL: for the SAME real execution (ba852138), the pre-fix handler output lacks any
       skip step and the post-fix deployed handler output contains a labeled SkipBothPKLs step --
       verified against live execution history, not a fixture.
    2. COMPLETENESS: every Pass-type state name in the YangDataPipeline definition has a
       STATE_LABELS entry (enumerate the state machine definition; cite the denominator -- N states,
       N labels -- so a future Skip* addition is visibly out of contract rather than silently absent).
    3. NO-REGRESSION: an execution with NO skips renders the same steps as pre-fix (existing
       Task-state parsing untouched).
    4. DEPLOY DISCIPLINE: Terraform-only, deploy-completion ledger entry opened at start + closed at
       completion, data-refresh-v* tag bumped + pushed --follow-tags.
  </acceptance_criteria>
</task_order>
