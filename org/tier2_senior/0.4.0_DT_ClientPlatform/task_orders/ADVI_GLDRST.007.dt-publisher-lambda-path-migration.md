<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-gldrst-007-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
    <revised_by>1.0.0_SA_CTO</revised_by>
    <revised_date>2026-03-26</revised_date>
    <revision_reason>CTO audit found task order understated scope (24 key refs in partners vs "~15"), missing explicit key migration map, missing multi-bucket concern, and missing shared-advisor-router dependency.</revision_reason>
  </metadata>

  <objective>
    Update the 3 Lambda handlers (opal-partners-data, bd-portal-publisher,
    bd-portal-advisor-publisher) to read/write from the new GLDRST S3 key
    layout. Also apply the TX snapshot date anchor fix specified by DS in .005.

    This is the Lambda-side of the copy-then-switch migration. Scripts
    (.004 Phase A) must have already dual-written to new paths before
    this TO begins.
  </objective>

  <context>
    After .004 Phase A completes, both old and new S3 keys exist in every
    firm bucket. This TO switches Lambda reads from old to new paths and
    adds dual-write for Lambda outputs (writing to both old and new paths
    until .008 cuts over CloudFront).

    Three Lambdas need updates:

    1. opal-partners-data (infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/)
       - 24 S3 key read references (see migration map below)
       - Zero writes (read-only API server)
       - Reads from FIRM-SPECIFIC buckets (opal-data-{firmId}), NOT just opal-data-bd

    2. bd-portal-publisher (infra/aws/lambda/bd-pipeline/bd-portal-publisher/)
       - 10 S3 key read references (parquets + JSONs + prefix listing)
       - 8 S3 key write references (portal-ready JSONs)

    3. bd-portal-advisor-publisher (infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/)
       - 8 S3 key read references
       - 5 S3 key write patterns (per-entity, hundreds of actual objects)

    MULTI-BUCKET: opal-partners-data resolves the target bucket dynamically
    from JWT claims via X-Firm-Id header. Every partner firm bucket
    (opal-data-{firmId}) must have the same key layout. The gold scripts
    (.004) write to opal-data-bd only. The publisher Lambdas write to
    opal-data-bd. Partner buckets get their data via a separate sync
    mechanism — verify that partner bucket key layouts are consistent
    with the migration map.
  </context>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      COMPLETE KEY MIGRATION MAP — every S3 key reference in all 3 Lambdas
      must be updated per this map. Lambda code cannot import lib/s3_layout.py
      (packaged separately), so create a LAMBDA_S3_KEYS dict at the top of
      each Lambda mirroring the layout.

      READS that MOVE (parquets — dimensions + timeseries):
        gold/client_performance.parquet         -> gold/timeseries/client_performance.parquet
        gold/account_performance.parquet         -> gold/timeseries/account_performance.parquet
        gold/holdings_lots/{date}.parquet        -> gold/timeseries/holdings_lots/{date}.parquet
        gold/holdings_lots/ (prefix listing)     -> gold/timeseries/holdings_lots/
        gold/client_dimension.parquet            -> gold/dimensions/client_dimension.parquet
        gold/accounts_dimension_latest.parquet   -> gold/dimensions/accounts_dimension_latest.parquet
        gold/aua_certification/{date}.json       -> gold/validation/aua_certification/{date}.json

      READS that MOVE (portal-ready JSONs — artifacts):
        gold/summary/header_metrics.json         -> gold/artifacts/summary/header_metrics.json
        gold/partner_analytics/header_metrics.json -> gold/artifacts/partner_analytics/header_metrics.json
        gold/filters/dimensions.json             -> gold/artifacts/filters/dimensions.json
        gold/snapshots/aua_by_{dim}.json         -> gold/artifacts/snapshots/aua_by_{dim}.json
        gold/clients/growth_timeseries.json      -> gold/artifacts/clients/growth_timeseries.json
        gold/clients/tax_basis_breakdown.json    -> gold/artifacts/clients/tax_basis_breakdown.json
        gold/clients/tax_deferred_candidates.json -> gold/artifacts/clients/tax_deferred_candidates.json
        gold/firm_mix_views.json                 -> gold/artifacts/firm_mix_views.json
        gold/architect_leaderboard.json          -> gold/artifacts/architect_leaderboard.json
        gold/implementor_leaderboard.json        -> gold/artifacts/implementor_leaderboard.json
        gold/timeseries_chart.json               -> gold/artifacts/timeseries_chart.json
        gold/clients_tab.json                    -> gold/artifacts/clients_tab.json

      READS that MOVE (per-entity JSONs):
        gold/advisors/{id}/book.json             -> gold/entities/advisors/{id}/book.json
        gold/advisors/{id}/timeseries.json       -> gold/entities/advisors/{id}/timeseries.json
        gold/advisors/{id}/mix_timeseries.json   -> gold/entities/advisors/{id}/mix_timeseries.json
        gold/advisors/{id}/mix.json              -> gold/entities/advisors/{id}/mix.json
        gold/advisors/{id}/composition.json      -> gold/entities/advisors/{id}/composition.json
        gold/client_timeseries/{rel_id}.json     -> gold/entities/clients/{rel_id}/timeseries.json
        gold/clients/{rel_id}.json               -> gold/entities/clients/{rel_id}/detail.json

      READS that STAY (already subcategorized under gold/views/ and gold/timeseries/):
        gold/views/nna_aua_by_advisor.parquet    (no change)
        gold/views/nna_aua_by_geography.parquet  (no change)
        gold/views/nna_aua_by_geography_city.parquet (no change)
        gold/views/client_tax_liability.parquet  (no change)
        gold/views/rel_architect_lookup.parquet   (no change)
        gold/views/firm_composition.json         (no change)
        gold/timeseries/nna_total.json           (no change)
        gold/timeseries/nna_by_{dim}.json        (no change)

      WRITES (publisher outputs — DUAL-WRITE old + new until .008 completes):
        gold/summary/header_metrics.json         + gold/artifacts/summary/header_metrics.json
        gold/filters/dimensions.json             + gold/artifacts/filters/dimensions.json
        gold/snapshots/aua_by_{dim}.json         + gold/artifacts/snapshots/aua_by_{dim}.json
        gold/architect_leaderboard.json          + gold/artifacts/architect_leaderboard.json
        gold/implementor_leaderboard.json        + gold/artifacts/implementor_leaderboard.json
        gold/timeseries_chart.json               + gold/artifacts/timeseries_chart.json
        gold/clients_tab.json                    + gold/artifacts/clients_tab.json
        gold/advisors/{id}/book.json             + gold/entities/advisors/{id}/book.json
        gold/advisors/{id}/timeseries.json       + gold/entities/advisors/{id}/timeseries.json
        gold/advisors/{id}/mix_timeseries.json   + gold/entities/advisors/{id}/mix_timeseries.json
        gold/client_timeseries/{rel_id}.json     + gold/entities/clients/{rel_id}/timeseries.json
        gold/clients/{rel_id}.json               + gold/entities/clients/{rel_id}/detail.json
    </requirement>

    <requirement id="2">
      Apply TX snapshot date anchor fix to bd-portal-publisher:
      Use US-only max date for both snapshot and continuous views
      (per DS .005 specification).
    </requirement>

    <requirement id="3">
      Dual-write ALL publisher outputs to both old and new paths.
      CloudFront (.008) still reads via the old gold/ prefix until
      the shared-advisor-router is updated. Removing dual-write happens
      in .010 (cleanup) after .008 is verified.
    </requirement>

    <requirement id="4">
      Terraform deploy for both bd-pipeline and partners-api.
      Update lambda-source-map.json. Follow LAMBDA_DEPLOYMENT_PROTOCOL.md.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All 3 Lambdas read from new GLDRST S3 key paths per migration map</criterion>
    <criterion id="2">All publisher writes dual-write to old + new paths</criterion>
    <criterion id="3">TX snapshot date anchor uses US-only max date</criterion>
    <criterion id="4">Terraform plan shows 0-diff after apply for both bd-pipeline and partners-api</criterion>
    <criterion id="5">Portal loads all tabs without errors (old CloudFront paths still work via dual-write)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Requires .004 Phase A (dual-write in gold scripts) to be complete and verified</constraint>
    <constraint>Requires .009 (migration gold rerun) to have populated new keys</constraint>
    <constraint>Must follow LAMBDA_DEPLOYMENT_PROTOCOL.md (commit -> plan -> apply -> tag)</constraint>
    <constraint>Dual-write old paths until .008 + .010 complete — do NOT remove old writes</constraint>
    <constraint>opal-partners-data reads from firm-specific buckets — verify partner bucket key layout matches</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.004" status="pending">
      Phase A (dual-write) must be complete so new S3 keys exist
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_GLDRST.005" status="pending">
      TX date anchor fix specification needed
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_GLDRST.009" status="pending">
      Gold rerun with .004 Phase A to populate new keys
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Lambda S3 path updates (all 3 handlers) + TX date anchor fix</deliverable>
    <deliverable type="deploy">bd-pipeline Terraform deploy (publisher + advisor-publisher)</deliverable>
    <deliverable type="deploy">partners-api Terraform deploy (opal-partners-data)</deliverable>
  </deliverables>
  <tooling>
    <tool module="interpret.crossref_graph" when="before_coding">
      Run against infra/aws/lambda/ to map references between the 3 Lambda handlers
      and gold script outputs. Identify every S3 path literal in the Lambda source.
      The graph shows which Lambda reads which gold output — every path must be
      updated to the new layout.
    </tool>

    <tool module="interpret.ast_extractor" when="before_coding">
      Parse all 3 Lambda handlers (opal-partners-data, bd-portal-publisher,
      bd-portal-advisor-publisher). Extract function signatures, S3 client calls,
      and key construction patterns. This is the migration surface for Lambda paths.
    </tool>

    <tool module="adapt.coverage_auditor" when="after_coding">
      Compare: S3 path literals found in pre-analysis vs paths now routed through
      the new layout. Any old-format path literal remaining in Lambda source is a
      migration gap that will break after .010 (old key cleanup).
    </tool>
  </tooling>
</task_order>
