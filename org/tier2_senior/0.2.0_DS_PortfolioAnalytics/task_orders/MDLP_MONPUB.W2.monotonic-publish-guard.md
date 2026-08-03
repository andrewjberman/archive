<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-08-03-monpub-w2</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics (code) + 0.2.0_DT_PortfolioAnalytics (deploy)</issued_to>
    <date>2026-08-03</date>
    <status>pending</status>
    <project_code>MDLP_MONPUB</project_code>
  </metadata>

  <objective>
    Two halves, both required: (a) a monotonic date-guard on yang-model-portfolio-benchmarks'
    publish path so a reprocess of an older upload can never silently overwrite a newer served
    vintage (the 2026-08-03 last-writer-wins regression class); (b) CVO-REQUIRED build-before-publish
    reorder -- FAILED executions currently PUBLISH (upload_json :316/:319 runs BEFORE
    build_rfr_daily :324 throws; the four FAILED 07-31 runs each wrote defective 07-31 data the
    portal SERVED 12:09Z-13:12Z, timeseries key never landing = mixed-vintage serve). All three
    payloads must be FULLY CONSTRUCTED before the first upload_json. The guard alone cannot close
    this half: 07-31 was NEWER than served, so monotonicity passes it.
  </objective>

  <context>
    Spec: docs/architecture/MDLP_MONPUB_MANIFEST_REGRESSION_FIX.md @d59fc15920 section 3 W2.
    Source at vintage b8874661fe: three outputs (:47-49) published unconditionally via upload_json
    at :316/:319/:351; data_as_of derives from end_date = term_returns.index.max() (:187).
    GUARD SEMANTICS (CVO-validated): before the FIRST upload, read currently-served
    OUTPUT_KEY_COMPREHENSIVE data_as_of. Incoming OLDER -> abort ALL THREE writes, raise loudly
    (FAILED execution -- an error, NOT an alarm/SNS/monitor; the moratorium stands). Equal -> allow.
    Served object missing/unreadable -> allow with loud log (first-publish case). Event flag
    force_publish=true bypasses the guard with a loud log (deliberate rollback stays possible).
    DOCTRINE: memory/reference_yang_datapkl_return_daily_total_return_basis_custom_indices.md if
    you touch anything near return computation (you should not need to).
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
      <run>comp-blast yang-model-portfolio-benchmarks</run>
      <expect>31-node yang-family radius (as measured 2026-08-03); guard is additive, radius must not grow</expect>
      <if_mismatch>New downstream nodes = the graph moved since spec; flag to CTO before writing</if_mismatch>
    Phase 2 (before committing):
      <run>.tools/comp-surface-check check</run>
      <expect>SEV1 model_portfolios.benchmark named; confirm+justify per gate (this TO IS the justification -- cite it)</expect>
      <if_mismatch>A SEV1 you did not expect = STOP, not a note</if_mismatch>
    Phase 3 (after deploy):
      <run>aws iam simulate-principal-policy --policy-source-arn &lt;lambda role&gt; --action-names s3:GetObject --resource-arns arn:aws:s3:::opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json</run>
      <expect>allowed. ONE --resource-arns per call; positive control (a key the role is KNOWN to read) as a SEPARATE invocation. comp-iam alone is NOT sufficient -- it fails green on new resources (Rule 22a).</expect>
      <if_mismatch>implicitDeny may be a missing grant OR a condition block OR an action-name typo -- discriminate per Rule 22a before adding policy</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: yang-model-portfolio-benchmarks lambda_function.py + opal-data-portal-v2/json/benchmarks/*
    also_in_to: MDLP_MONPUB.W1 (fires first), MDLP_MONPUB.W4 (re-upload waits for this guard to be LIVE)
    required_action: confirm W1 closed before deploying; message W4 owner when the guard is live-verified.
  </cross_domain_coordination>

  <acceptance_criteria>
    <!-- ACCEPTANCE STATE AS EXERCISED (CTO amendment 2026-08-03T1636Z, per the 155100Z ruling +
         CVO witness @ff496d7621 -- the record matches what was ACTUALLY exercised, no over-claim):
         Criterion 1 (older-date):      EXERCISED-LIVE PASS (direct-invoke per CVO method ruling
                                        162224Z; PublishGuardError at deployed :354; S3 version-gap
                                        proof: zero new versions on all three keys, battery window).
         Criterion 2 (passing):         CLOSED via W4's recovery publish (CVO witness @b16913d35e)
                                        + a second organic exercise: 16:21:45Z execution 3796f456,
                                        real user pull, equal-date guard pass by design.
         Criterion 2b (mid-build-crash):EXERCISED-LIVE PASS -- the REAL defective 07-31 pkl (the
                                        byte-identical input that wrote the serve 4x on 08-03
                                        morning) crashed at :325 BEFORE any upload; zero writes.
         Criterion 3 (force_publish):   PENDING SCRATCH-ONLY (CVO ruling: never rewrite the healed
                                        SEV1 serve to prove a bypass; two-invocation design --
                                        refusal control then bypass -- on a seeded scratch serve).
         W2 is LIVE-and-WITNESSED on legs 1/2/2b; formal close issues on CVO's leg-3 verdict. -->

    1. EXERCISED-FAILING (the criterion that can fail): on the DEPLOYED Lambda, a mutant invocation
       carrying data_as_of OLDER than served -> execution FAILS AND all three served ETags are
       byte-identical before/after (record all six ETags). A guard never exercised in the failing
       direction is UNEXERCISED != PASSED.
    2. EXERCISED-PASSING: a publish with data_as_of &gt;= served succeeds end-to-end.
    2b. EXERCISED-CRASH (CVO-required): a mid-build-crash mutant -- the real defective 07-31 pkl
       is a ready fixture -- leaves ALL THREE served ETags byte-unchanged; the execution FAILS
       loudly and publishes NOTHING. This is the acceptance for the build-before-publish reorder.
    3. BYPASS: force_publish=true with an older date publishes AND emits the loud log line.
    4. IAM: Phase-3 simulate-principal-policy allowed on the exact key ARN + separate positive control.
    5. DEPLOY DISCIPLINE: Terraform-only via .tools/safe-apply.sh, commit-before-apply, 0-diff
       post-apply, tag yang-v* bumped + pushed --follow-tags, lambda-source-map entry current.
       Forbidden shortcut: aws lambda update-function-code (NEVER-rule).
    6. THIRD STATE: if the guard's served-read errors at runtime, the publish is BLOCKED-LOUD (fail
       closed), not silently allowed -- demonstrated in the mutant battery or by cited code path.
  </acceptance_criteria>
</task_order>
