# Task Order — Data Contract: PortfolioAnalytics

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-data-contract-portfolio-analytics</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a data_contract.xml mapping what each PortfolioAnalytics page
    consumes, which Yang pipeline Lambda produces it, what S3 key it lives at,
    and what shape the JSON has. All six pages in this pod (Positioning,
    Attribution, FactorTilts, Valuation, Macroeconomics, Correlation) are
    driven entirely by the Yang pipeline — your data contract is effectively
    a full map of Yang's analytical output layer.
  </objective>

  <scope>
    <files>
      <!-- Primary input -->
      <file action="read">org/tier2_senior/0.2.0_DE_PortfolioAnalytics/deliverables/pod_inventory.xml</file>

      <!-- Yang generator Lambdas — one per page -->
      <file action="read">infra/aws/lambda/yang_generate_positioning/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_holdings_attribution/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_factor_tilts/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_valuation/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_macro/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_macro_timeseries/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_correlation/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_risk_premium/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_benchmark_returns/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_etf_returns/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_peer_performance/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_volatility/lambda_function.py</file>

      <!-- Yang pipeline orchestration — understand trigger chain -->
      <file action="read">infra/aws/lambda/yang_pipeline_trigger/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_manifest/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_generate_latest/lambda_function.py</file>
      <file action="read">infra/aws/terraform/yang-pipeline/stepfunctions.tf</file>

      <!-- Portal endpoint files -->
      <file action="read">portal/src/api/endpoints/portfolio.ts</file>
      <file action="read">portal/src/api/endpoints/benchmarks.ts</file>
      <file action="read">portal/src/api/endpoints/valuation.ts</file>
      <file action="read">portal/src/api/endpoints/macro.ts</file>
      <file action="read">portal/src/hooks/useYangData.ts</file>

      <!-- Lambda source map -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.2.0_DS_PortfolioAnalytics/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read pod_inventory.xml first. All six pages share the Yang pipeline as their
      upstream. Use the api_endpoints section to confirm which yang-generate-*
      Lambda maps to which page.
    </requirement>
    <requirement id="2">
      Read the Yang Step Functions definition (stepfunctions.tf or yang-pipeline-definition.json)
      to understand the full orchestration sequence: trigger → validate → ingest →
      generate-* (parallel) → manifest → latest → invalidate. Document which
      generator Lambdas run in parallel and which run in sequence.
    </requirement>
    <requirement id="3">
      For each generator Lambda, extract:
      (a) which PKL or DynamoDB data it reads as input (the Yang workspace),
      (b) the S3 output key pattern (e.g., yang/{version}/{output_name}.json),
      (c) the top-level JSON keys of its output,
      (d) how the portal fetches it (versioned S3 key via manifest, or direct).
    </requirement>
    <requirement id="4">
      Document the Yang versioning model: how the portal knows which version
      to fetch (manifest.json, latest pointer, or CloudFront-cached path).
      This is critical context for any DS working on Yang output correctness.
    </requirement>
    <requirement id="5">
      For Attribution specifically: document the alpha factor calculation method
      found in yang_generate_holdings_attribution — the permid join vs company_name
      join distinction was a root cause of a prior data bug. Capture this in
      data_quality_notes.
    </requirement>
    <requirement id="6">
      For Macroeconomics: yang_generate_macro and yang_generate_macro_timeseries
      are separate Lambdas. Document what each produces and which portal tab/section
      consumes which.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      data_contract.xml exists at org/tier2_senior/0.2.0_DS_PortfolioAnalytics/deliverables/data_contract.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;data_contract&gt;
        &lt;metadata&gt; agent, pod, date &lt;/metadata&gt;

        &lt;yang_pipeline_overview&gt;
          Step Functions execution order, trigger mechanism, versioning model
        &lt;/yang_pipeline_overview&gt;

        &lt;page_contracts&gt;
          One &lt;page&gt; per pod page:
            name,
            &lt;data_sources&gt;
              One &lt;source&gt; per distinct data feed:
                lambda_function, s3_output_key_pattern,
                &lt;input_data&gt; what the Lambda reads (PKL workspace path, DynamoDB table) &lt;/input_data&gt;
                &lt;response_shape&gt; top-level keys and value types &lt;/response_shape&gt;
                &lt;portal_endpoint&gt; which endpoint.ts function fetches this &lt;/portal_endpoint&gt;
            &lt;/data_sources&gt;
            &lt;data_freshness&gt; triggered per Yang run — document run frequency &lt;/data_freshness&gt;
        &lt;/page_contracts&gt;

        &lt;shared_data_sources&gt;
          Yang outputs consumed by more than one page (e.g., benchmark data)
        &lt;/shared_data_sources&gt;

        &lt;upstream_dependencies&gt;
          What feeds the Yang pipeline: PKL upload, FRED data, ETF classification
          DynamoDB, peer performance Excel — document each with its S3 or API source
        &lt;/upstream_dependencies&gt;

        &lt;data_quality_notes&gt;
          Known issues: alpha factor join bug (permid vs company_name), sector
          remapping history, any other data correctness notes from code comments
        &lt;/data_quality_notes&gt;

        &lt;gaps&gt;
          Any generator Lambdas whose output shape could not be determined
        &lt;/gaps&gt;
      &lt;/data_contract&gt;
    </criterion>
    <criterion id="3">
      yang_pipeline_overview must document the Step Functions execution order.
      This is the single most important piece of context for a DS working on Yang.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Lambda source files or portal files.</constraint>
    <constraint>Do not run any Lambda functions or AWS CLI commands.</constraint>
    <constraint>
      If a Lambda file path is not found using the underscore variant, try the
      hyphen variant. Both naming conventions exist in this codebase.
    </constraint>
    <constraint>
      yang-generate-cma belongs to the CapitalMarketAssumptions page (Pod 1 /
      MarketIntelligence). Do not include it in this data contract — it is owned
      by DS_MarketIntelligence. If you encounter it, note that it is out of scope.
    </constraint>
    <constraint>
      Focus on output shape, not implementation details. The DS role is concerned
      with data contracts — what flows between Lambda and portal — not the
      mathematical implementation of the models themselves.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.2.0_DE_PortfolioAnalytics" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.2.0_DS_PortfolioAnalytics/deliverables/data_contract.xml
    </deliverable>
  </deliverables>
</task_order>
```
