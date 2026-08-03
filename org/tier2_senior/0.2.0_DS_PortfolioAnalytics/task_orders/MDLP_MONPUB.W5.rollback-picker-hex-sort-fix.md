<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-08-03-monpub-w5</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics (code) + 0.2.0_DT_PortfolioAnalytics (deploy)</issued_to>
    <date>2026-08-03</date>
    <status>complete</status>
    <project_code>MDLP_MONPUB</project_code>
  </metadata>

  <objective>
    Fix the DataRefresh rollback picker's ordering blindness: handle_history queries
    opal-data-refresh-executions PK=EXECUTION with ScanIndexForward=False + limit 20, but the SK is
    exec-{random uuid hex} -- "newest first" is actually DESCENDING-HEX-ALPHABET, so only executions
    whose random id starts f/e/d ever surface. The 07-27 execution (exec-5a4149176fb6,
    canRollback=True) is structurally invisible; this is half of what Andrew fought on 07-31.
  </objective>

  <context>
    Source: CVO Andrew-direct audit @30a13b89b1
    (org/tier1_exec/3.0.0_SA_CVO/logs/2026-08-03/datarefresh_rollback_and_cloudfront_cache_audit_1530-1610Z.md)
    -- verified in the DEPLOYED zip, not just source. Fix shape (CVO rec, CTO-ratified): sort by
    startedAt -- paginate + sort in-Lambda, or a GSI if the table shape warrants it (DS's call, cite
    the tradeoff in the commit). Same Lambda as W3 (data_refresh); coordinate the deploys -- one
    data-refresh deploy carrying W3+W5 together is fine, ledger entry covers both.
  </context>

  <compiler_tools_mandate>
    Phase 1: read handle_history at current HEAD + cite the query call lines in your commit message.
    Phase 3 (after deploy):
      <run>invoke the history endpoint on the DEPLOYED Lambda</run>
      <expect>exec-5a4149176fb6 (07-27) PRESENT in the returned list, ordered by startedAt descending</expect>
      <if_mismatch>Fix did not reach the handler -- verify CodeSha256 changed + TF 0-diff</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: infra/aws/lambda/data_refresh/lambda_function.py
    also_in_to: MDLP_MONPUB.W3 (same file, both in your lane -- sequence the commits, deploy together allowed)
    required_action: single deploy-completion ledger entry may cover the joint deploy; say so in it.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. DIFFERENTIAL (the criterion that can fail): exec-5a4149176fb6 is ABSENT from the deployed
       pre-fix history response and PRESENT post-fix, with the list ordered by startedAt descending
       -- both responses captured as evidence.
    2. COMPLETENESS: the response denominator is cited -- N executions in the table vs M returned;
       if limit 20 still truncates, the truncation is by RECENCY (startedAt), never by hex.
    3. NO-REGRESSION: canRollback flags and payload shape unchanged for the entries both versions return.
    4. DEPLOY DISCIPLINE: Terraform-only, ledger entry, data-refresh-v* tag --follow-tags.
  </acceptance_criteria>

<completion date="2026-08-03" by="2.0.0_SA_COO">
W5 COMPLETE: code 5de42e3b7b, LIVE data-refresh-v2.5.0 16:29:56Z (0-diff, no override needed post-@ac778cbbcd, sweep-check clean). Differential: exec-5a4149176fb6 ABSENT on deployed v2.4.0 handler -> PRESENT post-fix, all 20 startedAt-desc, denominator 133-in-table vs 20-by-recency, no-regression on 3 co-returned entries.
Project closed Andrew-direct (COO terminal, 2026-08-03 ~1750Z): "WE can closeout this project, everything looks good for data refresh and the associated paths/lambdas/etc, visual smoke passes."
</completion>
</task_order>
