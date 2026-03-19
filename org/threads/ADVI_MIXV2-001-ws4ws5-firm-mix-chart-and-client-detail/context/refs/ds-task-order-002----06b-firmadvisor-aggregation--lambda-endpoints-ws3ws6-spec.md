<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-002-firm-advisor-gold-lambda</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
    <project_code>ADVI_MIXV2</project_code>
  </metadata>

  <objective>
    Extend 06b_build_client_mix_timeseries.py to produce two new pre-computed artifacts:
    (1) firm-level period-aggregated mix views with dollar amounts, and (2) per-advisor
    period-aggregated mix views. Add two new Lambda passthrough endpoints to serve them.
    This is WS3 + WS6 from ADVI_MIXV2_PRD.md.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      DEPENDENCY: This task order must not begin until ADVI_MIXV2.001 is committed. The AP gate
      fix must be in place before the firm-level pre-computed views are built — otherwise the
      $60M insurance volatility gets baked into the quarterly snapshots.
    </requirement>

    <requirement id="2">
      Extend 06b per-date processing to also track firm-level market value by asset class.
      In process_date(), the function already returns {rel_id: {mix: {equity: pct, ...}, conc: [...]}}
      per relationship. Modify to ALSO return total_mv per relationship:
        result[rel_id] = {'mix': mix, 'conc': holdings, 'total_mv': total_mv}
      This allows the caller to back-compute dollar amounts: dollar[ac] = pct[ac] * total_mv.
    </requirement>

    <requirement id="3">
      In the full-build and incremental-build paths, accumulate a firm_daily dict:
        firm_daily[date_str] = {equity: $, fixed_income: $, structured_notes: $, cash: $, other: $, total: $}
      Computed as sum across all relationships: for each rel, dollar[ac] = mix[ac] * total_mv.
      Also accumulate advisor_daily in the same loop:
        advisor_daily[advisor_id][date_str] = {same shape as firm_daily entry}
      The advisor→relationship mapping comes from rel_architect_lookup.parquet at
      gold/views/rel_architect_lookup.parquet. Load this at startup alongside static tables.
      If the file does not exist, skip advisor aggregation and log a warning (do not crash).
    </requirement>

    <requirement id="4">
      Implement compute_period_views(daily_dict, data_as_of) function that:
        - Accepts {date_str: {equity: $, ..., total: $}}
        - For each granularity (quarterly, monthly, annually):
          - Groups dates by period key using the same period logic as PartnerAnalytics.tsx
            (quarterly: YYYY-Q#, monthly: YYYY-MM, annually: YYYY)
          - Takes the LAST date in each period as the end-of-period snapshot
          - Computes pct = asset_mv / total for that snapshot
        - Returns {"quarterly": [...], "monthly": [...], "annually": [...]}
      Each period entry shape:
        {period, label, end_date, total_aua, equity: {value, pct}, fixed_income: {value, pct},
         structured_notes: {value, pct}, cash: {value, pct}, other: {value, pct}}
      All pct values are 0-1. Values are floats rounded to 2 decimal places.
      Period labels follow the same format as PartnerAnalytics.tsx getPeriodInfo():
        quarterly: "Q4 '24", monthly: "Oct '24", annually: "2024"
    </requirement>

    <requirement id="5">
      Write firm mix views to S3:
        gold/firm_mix_views.json
      Shape:
        {generated_at, data_as_of, firm_id: "49financial", views: {quarterly, monthly, annually}}
      Write this at the end of the build (full or incremental), after the watermark.
    </requirement>

    <requirement id="6">
      Write per-advisor mix views to S3:
        gold/advisors/{advisor_id}/mix.json  (one per advisor)
      Shape:
        {generated_at, data_as_of, advisor_id, advisor_name, views: {quarterly, monthly, annually}}
      advisor_name comes from the rel_architect_lookup.parquet canonical_name column (or advisor_id
      reformatted if canonical_name is absent). Write in parallel using the existing WRITE_WORKERS pool.
      Only write advisors that have at least one period entry in the annual view (skip advisors
      with no funded relationship data).
    </requirement>

    <requirement id="7">
      Add two Lambda endpoints to opal-partners-data:

      (a) GET /api/scoped/partners/books/firm/mix-views?firmId=xxx
          -> serve_s3_json(bucket, 'gold/firm_mix_views.json')
          Route: entity_type == 'firm', action == 'mix-views'
          Validator: entity_type == 'firm' and entity_id == 'all' (same as composition endpoint)

      (b) GET /api/shared/advisor-intelligence/advisors/{id}/mix-views?firmId=xxx
          -> serve_s3_json(bucket, f'gold/advisors/{advisor_id}/mix.json')
          Route: add elif for this path in the shared/advisor-intelligence branch
          Validator: reuse existing _validate_advisor_id check from handle_advisor_book
    </requirement>

    <requirement id="8">
      Update data_contract.xml with new output artifacts:
        - gold/firm_mix_views.json: schema, written_by 06b, served_by new Lambda endpoint
        - gold/advisors/{id}/mix.json: schema, written_by 06b, served_by new Lambda endpoint
    </requirement>

    <requirement id="9">
      Commit to CLOUD with:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"
      Two commits:
        (a) "0.4.0_DS_ClientPlatform: 06b firm + advisor mix period views (WS3+WS6)"
        (b) "0.4.0_DS_ClientPlatform: opal-partners-data -- firm/mix-views + advisor/mix-views endpoints"
      Update data_contract.xml in commit (a).
      Write DevOps brief at docs/briefs/devops-brief-mixv2-002.md:
        - 06b: run sequence (incremental is sufficient after 001 full run), expected output sizes
        - Lambda: endpoints to add, Terraform plan expected (no new resources, code change only)
        - Verification steps: check S3 for firm_mix_views.json, curl test both endpoints
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">gold/firm_mix_views.json exists in S3 with correct shape after 06b run</criterion>
    <criterion id="2">gold/advisors/{id}/mix.json exists for all 19 active advisors</criterion>
    <criterion id="3">Each period entry pct values sum to 1.0 ± 0.001</criterion>
    <criterion id="4">Lambda endpoint GET /api/scoped/partners/books/firm/mix-views returns 200 with views.quarterly populated</criterion>
    <criterion id="5">Lambda endpoint GET /api/shared/advisor-intelligence/advisors/{id}/mix-views returns 200</criterion>
    <criterion id="6">data_contract.xml updated with new artifacts</criterion>
    <criterion id="7">DevOps brief at docs/briefs/devops-brief-mixv2-002.md is actionable for AE + DT</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT begin until ADVI_MIXV2.001 is committed (AP gate fix must be in place)</constraint>
    <constraint>Do NOT deploy — AE deploys 06b (task order 003), DT deploys Lambda (task order 004)</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
    <constraint>Period label format MUST match PartnerAnalytics.tsx getPeriodInfo() output exactly — DE relies on this for direct rendering without transformation</constraint>
    <constraint>If rel_architect_lookup.parquet is missing, skip advisor aggregation with a warning — do not crash the entire 06b run</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MIXV2.001" status="pending">
      AP gate fix must be committed before this task order begins
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">06b extended with firm + advisor aggregation, committed to CLOUD</deliverable>
    <deliverable type="commit">Lambda endpoints committed to CLOUD</deliverable>
    <deliverable type="commit">data_contract.xml updated</deliverable>
    <deliverable type="document">docs/briefs/devops-brief-mixv2-002.md</deliverable>
  </deliverables>
</task_order>
