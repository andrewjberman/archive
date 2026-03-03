# Task Order — Data Contract: ClientPlatform

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-data-contract-client-platform</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a data_contract.xml mapping the data layer for the ClientPlatform pod.
    This pod is architecturally unique: its two pages draw from entirely different
    pipelines. ModelPortfolios is Yang-driven (yang-model-portfolio-benchmarks).
    AdvisorIntelligence is BD-driven (opal-partners-data, bd-portal-publisher,
    bd-portal-advisor-publisher, bd-client-detail). Document both sides clearly,
    including the BD gold layer stages that produce the publisher inputs.
  </objective>

  <scope>
    <files>
      <!-- Primary input -->
      <file action="read">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>

      <!-- ModelPortfolios Lambda -->
      <file action="read">infra/aws/lambda/yang_model_portfolio_benchmarks/lambda_function.py</file>

      <!-- AdvisorIntelligence Lambdas -->
      <file action="read">infra/aws/lambda/opal_partners_data/lambda_function.py</file>
      <file action="read">infra/aws/lambda/bd_portal_publisher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/bd_portal_advisor_publisher/lambda_function.py</file>
      <file action="read">infra/aws/lambda/bd_client_detail/lambda_function.py</file>

      <!-- BD gold layer scripts that produce publisher inputs -->
      <file action="read">infra/aws/ec2/bd-gold-layer-runner/scripts/</file>

      <!-- Portal endpoint files -->
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">portal/src/api/endpoints/aum.ts</file>

      <!-- Lambda source map -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read pod_inventory.xml first. Use the api_endpoints section to understand
      which endpoints serve ModelPortfolios vs AdvisorIntelligence and what
      data shapes the portal expects.
    </requirement>
    <requirement id="2">
      For ModelPortfolios: read yang_model_portfolio_benchmarks/lambda_function.py.
      Extract what Yang outputs it reads (S3 key patterns), what it produces,
      and how the portal fetches it via the Yang versioning system.
    </requirement>
    <requirement id="3">
      For AdvisorIntelligence: trace the BD publisher chain.
      Read opal_partners_data, bd_portal_publisher, and bd_portal_advisor_publisher.
      Document what S3 keys each Lambda writes (portal-ready JSON paths) and what
      shape each JSON has at its top level.
    </requirement>
    <requirement id="4">
      For bd_client_detail: document what it reads (per-client detail from gold tables),
      the S3 key pattern it writes to, and the response shape. This Lambda produces
      the drill-down data for advisor/client detail views in AdvisorIntelligence.
    </requirement>
    <requirement id="5">
      List the BD gold layer scripts (from infra/aws/ec2/bd-gold-layer-runner/scripts/)
      that feed the publisher Lambdas. Use Glob or ls to enumerate the scripts directory.
      Document which gold scripts produce the input that bd-portal-publisher and
      bd-portal-advisor-publisher consume. You do not need to document every script's
      internals — just which ones produce publisher-input data and what files they write.
    </requirement>
    <requirement id="6">
      Document the GEO/ADV cohort split in the AdvisorIntelligence data model.
      The portal has a GEO (geographic/city drill-down) and ADV (advisor/client
      drill-down) dimension. Document how these are reflected in the publisher
      output shape.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      data_contract.xml exists at org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;data_contract&gt;
        &lt;metadata&gt; agent, pod, date &lt;/metadata&gt;

        &lt;page_contracts&gt;
          One &lt;page&gt; per pod page:
            name,
            &lt;data_sources&gt;
              One &lt;source&gt; per distinct data feed:
                lambda_function, trigger, s3_output_key_pattern,
                &lt;response_shape&gt; top-level keys and value types &lt;/response_shape&gt;
                &lt;portal_endpoint&gt; endpoint function &lt;/portal_endpoint&gt;
            &lt;/data_sources&gt;
            &lt;data_freshness&gt; how often data is updated &lt;/data_freshness&gt;
        &lt;/page_contracts&gt;

        &lt;pipeline_split&gt;
          Explicit documentation of the Yang vs BD pipeline boundary:
            ModelPortfolios: yang-pipeline source, trigger, versioning
            AdvisorIntelligence: bd-pipeline source, gold stage inputs, publisher outputs
        &lt;/pipeline_split&gt;

        &lt;bd_gold_inputs&gt;
          Which BD gold scripts produce data consumed by the portal publishers.
          One entry per gold script that feeds publisher input.
        &lt;/bd_gold_inputs&gt;

        &lt;upstream_dependencies&gt;
          For Yang side: Yang PKL workspace, benchmark data
          For BD side: 49 Financial allocation/transaction raw files, BD gold tables
        &lt;/upstream_dependencies&gt;

        &lt;data_quality_notes&gt;
          Known issues: AUA undercount history, data shape mismatches, fallback
          behaviors found in code comments
        &lt;/data_quality_notes&gt;

        &lt;gaps&gt;
          Any data sources where the contract could not be determined from code
        &lt;/gaps&gt;
      &lt;/data_contract&gt;
    </criterion>
    <criterion id="3">
      pipeline_split section must be complete and unambiguous. The Yang/BD split
      is the most important architectural fact about this pod.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Lambda source files or portal files.</constraint>
    <constraint>Do not run any Lambda functions or AWS CLI commands.</constraint>
    <constraint>
      infra/aws/ec2/bd-gold-layer-runner/scripts/ is a directory.
      Use Glob or Bash ls to enumerate its contents before reading individual scripts.
      You only need to identify which scripts produce publisher-input data —
      do not read every gold script in full.
    </constraint>
    <constraint>
      If a Lambda file path is not found at the underscore path, try hyphen variants.
      Document the actual path found.
    </constraint>
    <constraint>
      The BD pipeline had a significant AUA undercount incident resolved in the
      Feb 23-27 sprint. Code comments or recent edits in the publisher Lambdas
      may reference this. Note any such context in data_quality_notes.
    </constraint>
    <constraint>
      The full BD pipeline infrastructure (allocation trigger, transaction processing,
      gold layer runner) is owned by DS_PartnerETL (0.6.0_AE_PartnerETL). Your scope
      is the portal-facing output layer only: publisher Lambdas + opal-partners-data.
      Reference the BD pipeline as an upstream dependency, do not re-document its
      full internals.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml
    </deliverable>
  </deliverables>
</task_order>
```
