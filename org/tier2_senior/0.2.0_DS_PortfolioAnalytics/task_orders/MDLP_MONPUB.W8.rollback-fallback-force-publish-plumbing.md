<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-08-03-monpub-w8</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics (code) + 0.2.0_DT_PortfolioAnalytics (deploy)</issued_to>
    <date>2026-08-03</date>
    <status>complete</status>
    <project_code>MDLP_MONPUB</project_code>
  </metadata>

  <objective>
    Restore the DataRefresh RE-PROCESSING FALLBACK rollback path, which the W2 guard now
    structurally blocks: handle_rollback's fallback (:1407/:1411 -> :1433-1441) re-runs the full
    pipeline from archived older inputs, the benchmarks Lambda sees incoming data_as_of older than
    served, and PublishGuardError fails the execution -- force_publish appears ZERO times in
    data_refresh/lambda_function.py, so the feature has no bypass. Plumb force_publish through the
    fallback path ONLY: handle_rollback fallback -> the SFN/manifest input -> yang Lambda event,
    with the guard's loud bypass log carrying the rollback execution id.
  </objective>

  <context>
    Grounding: DT report 163640Z at vintage 5de42e3b7b (deployed Z3rt+Opu...), line cites therein.
    Spec: docs/architecture/MDLP_MONPUB_MANIFEST_REGRESSION_FIX.md section 5b.

    INTENDED SEMANTICS (CTO ruling, write it into the code comment at the plumbing site): a
    fallback rollback INTENTIONALLY regenerates the estate from older inputs -- a coherent older
    vintage across all ~40 keys is the DEFINITION of rolling back, not collateral damage. The R1
    unguarded siblings rebuilding from the same older inputs is therefore in-spec for this path.
    force_publish exists to tell the ONE guarded Lambda "this older date is deliberate"; it is
    set by the rollback path only, never defaulted, never exposed to normal publishes.

    CLAIM BOUNDARY (explicit, per DT's suggestion): PATH 1 (version-based restore, :1318-1328 raw
    copy_object per key) is OUT OF SCOPE and UNGUARDABLE by W2 -- it never invokes the Lambda.
    Its controls today are the ROLLBACK DDB record (:1377-1391, method='version-based') and
    fabric law (verify-live-before-mutation). This TO does not claim to cover it; the residual
    R2 recording in the spec is the honest register of that exposure.
  </context>

  <compiler_tools_mandate>
    Phase 1: comp-blast data-refresh (PYTHONIOENCODING=utf-8) -- radius must not grow beyond the
      known set; cite the handle_rollback fallback lines at your working vintage.
    Phase 3 (exercise, scratch-first per the CVO method precedent): a fallback rollback against a
      SEEDED SCRATCH serve (older archived inputs, scratch keys) completes end-to-end -- guard
      logs the loud bypass WITH the rollback execution id, all scratch keys land at the older
      vintage coherently. The LIVE end-to-end rides the next genuine rollback occasion (shared
      with W6's live leg -- one real occasion closes both).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/data_refresh/lambda_function.py (W3+W5 landed; sequence on HEAD)
      + yang-model-portfolio-benchmarks lambda_function.py (W2's guard event parsing)
    also_in_to: MDLP_MONPUB.W6 (its live-occasion exercise is the same event as this TO's)
    required_action: coordinate the two-Lambda change as one reviewed pair; deploys may ride
      separate cycles but the EVENT CONTRACT (field name, default-absent semantics) is one commit's
      decision, cited in both.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. EXERCISED-SCRATCH: the fallback rollback completes on the seeded scratch serve; the bypass
       log line carries the rollback execution id; scratch keys coherently at the older vintage.
       ENTRY POINT REQUIRED (CVO witness condition 164003Z): BOTH W8 legs -- the plumbed bypass
       AND criterion 2's negative control -- enter through data_refresh handle_rollback
       END-TO-END, never direct-invoke of the benchmarks Lambda. A direct-invoke pass proves the
       FLAG works while proving nothing about the PLUMBING this TO exists to add (entry-point
       substitution -- same class as citing W4's publish for the bypass). The witness checks
       which entry point each request-id came through; DT designs the scratch scoping
       (BUCKET env on a test instance or event-level override, their call).
    2. NEGATIVE CONTROL (separate invocation): a NORMAL publish event (no force_publish field)
       against the scratch serve with an older date still FAILS with PublishGuardError -- the
       plumbing must not widen the guard's default posture. A bypass that leaks into normal
       publishes re-commits the original defect wearing a fix's name.
    3. GREP GATE: force_publish is set at exactly ONE call site (the rollback fallback); cite the
       grep count in evidence.
    4. CLAIM BOUNDARY: the RAVC close names Path 1 as out-of-scope/unguardable with its DDB-record
       control -- UNCOVERED stated, not implied covered.
    5. DEPLOY DISCIPLINE: TF-only, fresh ledger entries, tags bumped per pipeline.
  </acceptance_criteria>

<completion date="2026-08-03" by="2.0.0_SA_COO">
W8 COMPLETE: code 4024664d71 (both Lambdas, one event-contract commit; grep gate: force_publish at exactly ONE call site, the rollback-fallback manifest stamp; Path-1 ruled OUT-OF-SCOPE/unguardable w/ DDB record as control). LIVE 0-diff: data-refresh-v2.6.0 + yang-v2.4.18. Scratch exercise per CVO ruling (option b + :146 manifest-arm condition): leg 1 end-to-end exec-fdf49e30710f manifest-landed-LAST, leg 2 manifest-arm bypass ed35ec26, leg 3 negative control 030ed212 refused/seed-unchanged. Package delivered to CVO for witness; closed on Andrew-direct closeout ruling 2026-08-03 ~1750Z (visual smoke passes) -- CVO witness appends to this record if/when it lands. Live-occasion traversal leg stays PENDING-LIVE-OCCASION, non-blocking per spec 5c.
Project closed Andrew-direct (COO terminal, 2026-08-03 ~1750Z): "WE can closeout this project, everything looks good for data refresh and the associated paths/lambdas/etc, visual smoke passes."
</completion>
</task_order>
