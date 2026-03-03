# Task Order — Pipeline Inventory: OpalETL

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-pipeline-inventory-opal-etl</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a pipeline_inventory.xml covering all six Opal-owned pipelines:
    yang, news, market-overview, smartx, causality, and seeking-alpha.
    This is your permanent activation document — a complete map of every Lambda,
    EC2 service, EventBridge rule, S3 artifact path, IAM role, and Terraform
    module you own. Read it at session start to orient without re-exploring
    the codebase each time.
  </objective>

  <scope>
    <files>
      <!-- Terraform modules — read all .tf files in each pipeline -->
      <file action="read">infra/aws/terraform/yang-pipeline/main.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/iam.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/stepfunctions.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/etf-classifications.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/CHANGELOG.json</file>

      <file action="read">infra/aws/terraform/news-pipeline/main.tf</file>
      <file action="read">infra/aws/terraform/news-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/news-pipeline/iam.tf</file>
      <file action="read">infra/aws/terraform/news-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/news-pipeline/CHANGELOG.json</file>

      <file action="read">infra/aws/terraform/market-overview/main.tf</file>
      <file action="read">infra/aws/terraform/market-overview/lambdas.tf</file>
      <file action="read">infra/aws/terraform/market-overview/iam.tf</file>
      <file action="read">infra/aws/terraform/market-overview/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/market-overview/CHANGELOG.json</file>

      <file action="read">infra/aws/terraform/smartx-pipeline/main.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/iam.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/ec2.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/CHANGELOG.json</file>

      <file action="read">infra/aws/terraform/causality/main.tf</file>

      <file action="read">infra/aws/terraform/seeking-alpha/main.tf</file>

      <!-- Lambda source map — filter to your functions -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- EC2 manifest — filter to your services -->
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.5.0_AE_OpalETL/deliverables/pipeline_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read every .tf file listed above in full. Extract every aws_lambda_function,
      aws_lambda_layer_version, aws_cloudwatch_event_rule (EventBridge), aws_sfn_state_machine
      (Step Functions), and aws_instance (EC2) resource defined across all six pipelines.
    </requirement>
    <requirement id="2">
      From lambda-source-map.json, extract the source_path, memory_mb, timeout_s,
      and last_deployed_commit for every function you own. Your functions are those
      prefixed with: yang-, news-, causality-, opal-market-, opal-news-,
      opal-trending-, opal-keyword-, opal-portal-fear-greed, opal-portal-volatility,
      opal-precompute-, opal-smartx-, smartx-, seeking-alpha-, finbert-, fred-,
      semantic-, keyword-.
    </requirement>
    <requirement id="3">
      From EC2_MANIFEST.json, identify any EC2 services under your ownership.
      SmartX exporter (smartx-exporter), seeking-alpha scraper, and historical-prices
      scheduler EC2 are likely yours — confirm from the manifest.
    </requirement>
    <requirement id="4">
      For each pipeline, note its current Terraform tag from CHANGELOG.json
      (the last deployed version). This is the version baseline.
    </requirement>
    <requirement id="5">
      Produce pipeline_inventory.xml following the schema in acceptance criteria.
      All values must be read from actual files — no inference.
    </requirement>
    <requirement id="6">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      pipeline_inventory.xml exists at org/tier2_senior/0.5.0_AE_OpalETL/deliverables/pipeline_inventory.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;pipeline_inventory&gt;
        &lt;metadata&gt; agent, pipelines_owned[], date &lt;/metadata&gt;

        &lt;pipeline name="yang-pipeline" terraform_module="infra/aws/terraform/yang-pipeline/" current_tag="yang-vX.Y.Z"&gt;
          &lt;lambdas&gt;
            One &lt;lambda&gt; per function:
              name, source_path, memory_mb, timeout_s, layers[], trigger (EventBridge|StepFunctions|S3|manual)
          &lt;/lambdas&gt;
          &lt;step_functions&gt; state machine name and definition summary &lt;/step_functions&gt;
          &lt;eventbridge_rules&gt; rule name, schedule, target &lt;/eventbridge_rules&gt;
          &lt;s3_artifacts&gt; key patterns used (input/output) &lt;/s3_artifacts&gt;
          &lt;iam_roles&gt; role names owned &lt;/iam_roles&gt;
        &lt;/pipeline&gt;

        Repeat &lt;pipeline&gt; block for: news-pipeline, market-overview,
        smartx-pipeline, causality, seeking-alpha

        &lt;ec2_services&gt;
          One &lt;service&gt; per EC2 instance:
            name, instance_id, source_path, last_deployed_commit, trigger
        &lt;/ec2_services&gt;

        &lt;layers&gt;
          Lambda layers owned, with S3 key and Python version
        &lt;/layers&gt;

        &lt;known_issues&gt;
          Any drift, missing Terraform coverage, or deprecated resources noted
        &lt;/known_issues&gt;
      &lt;/pipeline_inventory&gt;
    </criterion>
    <criterion id="3">
      Every function name, resource name, and tag value is verbatim from source files.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Terraform files. This is a read-and-document task only.</constraint>
    <constraint>Do not run terraform plan or apply.</constraint>
    <constraint>Do not run any AWS CLI commands.</constraint>
    <constraint>
      causality and seeking-alpha Terraform modules may be minimal stubs.
      Document what exists, note what is missing as a gap in known_issues.
    </constraint>
    <constraint>
      seeking-alpha and portfolio pipelines have no S3 backend yet (per memory).
      Note this explicitly under each pipeline's metadata.
    </constraint>
  </constraints>

  <dependencies>
    <!-- No pod wave dependencies — AE pipelines are independent of pod inventories -->
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.5.0_AE_OpalETL/deliverables/pipeline_inventory.xml
    </deliverable>
  </deliverables>
</task_order>
```
