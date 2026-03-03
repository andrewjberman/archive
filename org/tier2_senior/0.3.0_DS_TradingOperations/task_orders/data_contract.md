# Task Order — Data Contract: TradingOperations

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-data-contract-trading-operations</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.3.0_DS_TradingOperations</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a data_contract.xml mapping the full data layer for the TradingOperations
    pod. Unlike other pods, TradingOperations has bidirectional data flows — not just
    read paths but also write paths (PM uploads, autosave, trade submission). Document
    both directions. This pod's data layer is the most operationally sensitive in the
    portal: it handles PM-uploaded Excel files, Yang optimization outputs, trade
    approval state, and the SmartX fund universe.
  </objective>

  <scope>
    <files>
      <!-- Primary input -->
      <file action="read">org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml</file>

      <!-- PM optimization Lambdas -->
      <file action="read">infra/aws/lambda/opal_pm_optimization_loader/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_pm_optimization_autosave_put/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_pm_snapshot_handler/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_pm_upload_urls/lambda_function.py</file>

      <!-- Portfolio/version Lambdas -->
      <file action="read">infra/aws/lambda/opal_portfolio_pickle_parser/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portfolio_excel_generator/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portfolio_export_download/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portfolio_funds_list/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portfolio_autosave_get/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portfolio_autosave_put/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portfolio_version_get/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_portfolio_versions_list/lambda_function.py</file>

      <!-- Data refresh and SmartX ingestion -->
      <file action="read">infra/aws/lambda/opal_data_refresh_api/lambda_function.py</file>
      <file action="read">infra/aws/lambda/opal_smartx_ingestion_pipeline/lambda_function.py</file>

      <!-- Yang upload pipeline (PM uploads feed Yang) -->
      <file action="read">infra/aws/lambda/yang_pipeline_trigger/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_validate_files/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_ingest_dynamodb/lambda_function.py</file>
      <file action="read">infra/aws/lambda/yang_move_to_processed/lambda_function.py</file>

      <!-- Portal endpoint files -->
      <file action="read">portal/src/api/endpoints/portfolio-optimization.ts</file>
      <file action="read">portal/src/api/endpoints/trade-submission.ts</file>
      <file action="read">portal/src/api/endpoints/portfolio.ts</file>

      <!-- Lambda source map -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read pod_inventory.xml first. Pay close attention to PortfolioManagement's
      extensive Lambda list — this pod has the most complex bidirectional data flow.
    </requirement>
    <requirement id="2">
      Document the PM upload-to-optimization flow:
      PM uploads Excel → opal-pm-upload-urls (presigned URLs) →
      S3 upload → yang-pipeline-trigger → yang-validate-files →
      yang-ingest-dynamodb → yang-move-to-processed →
      opal-pm-optimization-loader (loads result for portal display).
      This is the critical data path for the PM workflow.
    </requirement>
    <requirement id="3">
      Document the autosave data contract: what opal-pm-optimization-autosave-put
      writes (S3 key, JSON shape) and what opal-portfolio-autosave-get/put
      handle (separate from PM optimization autosave). These are distinct systems.
    </requirement>
    <requirement id="4">
      Document the snapshot system: what opal-pm-snapshot-handler stores,
      what S3 key pattern, and how opal-portfolio-version-get/versions-list
      serve version history to the portal.
    </requirement>
    <requirement id="5">
      For TradeSubmission: trace what data the trade submission page reads
      (pending approvals state) and what it writes (approval/rejection actions).
      Identify where this state lives (DynamoDB table or S3) from the Lambda code.
    </requirement>
    <requirement id="6">
      For DataRefresh: document what opal-data-refresh-api and opal-smartx-ingestion-pipeline
      trigger and what they affect. DataRefresh is an ops page — document its
      side effects on other pod data sources.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      data_contract.xml exists at org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;data_contract&gt;
        &lt;metadata&gt; agent, pod, date &lt;/metadata&gt;

        &lt;page_contracts&gt;
          One &lt;page&gt; per pod page:
            name,
            &lt;read_paths&gt;
              One &lt;source&gt; per data feed the page reads:
                lambda_function, trigger, s3_key_or_dynamodb_table,
                &lt;response_shape&gt; top-level keys and value types &lt;/response_shape&gt;
                &lt;portal_endpoint&gt; endpoint function &lt;/portal_endpoint&gt;
            &lt;/read_paths&gt;
            &lt;write_paths&gt;
              One &lt;sink&gt; per data write the page performs:
                lambda_function, trigger (user action), s3_key_or_dynamodb_table,
                &lt;payload_shape&gt; what the portal sends &lt;/payload_shape&gt;
            &lt;/write_paths&gt;
        &lt;/page_contracts&gt;

        &lt;critical_flows&gt;
          Named end-to-end flows that span multiple Lambdas:
            &lt;flow name="pm-upload-to-optimization"&gt;ordered Lambda sequence&lt;/flow&gt;
            &lt;flow name="trade-export-to-submission"&gt;ordered steps&lt;/flow&gt;
        &lt;/critical_flows&gt;

        &lt;upstream_dependencies&gt;
          External inputs: Yang PKL Excel upload, SmartX fund universe,
          any external data APIs
        &lt;/upstream_dependencies&gt;

        &lt;data_quality_notes&gt;
          Known issues, edge cases, or failure modes observed in code or comments
        &lt;/data_quality_notes&gt;

        &lt;gaps&gt;
          Any flows where the data contract could not be determined from code
        &lt;/gaps&gt;
      &lt;/data_contract&gt;
    </criterion>
    <criterion id="3">
      critical_flows section must be complete. The PM upload and trade export flows
      are the primary operational paths for the trading workflow — they must be
      fully traced and documented.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Lambda source files or portal files.</constraint>
    <constraint>Do not run any Lambda functions or AWS CLI commands.</constraint>
    <constraint>
      If a Lambda file path is not found at the underscore path, try hyphen variants
      or search with Glob. Document the actual path used.
    </constraint>
    <constraint>
      opal-portfolio-autosave-* and opal-pm-optimization-autosave-put are DIFFERENT
      systems. Do not conflate them. The PM optimization autosave is scoped to the
      optimization session; the portfolio autosave is for general portfolio state.
    </constraint>
    <constraint>
      The yang-generate-* Lambdas (positioning, attribution, etc.) are owned by
      DS_PortfolioAnalytics. Do not re-document their output shapes here — reference
      them as upstream dependencies via the yang-pipeline-trigger entry point only.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.0_DE_TradingOperations" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml
    </deliverable>
  </deliverables>
</task_order>
```
