# Task Order — Pipeline Inventory: PartnerETL

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-pipeline-inventory-partner-etl</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a pipeline_inventory.xml covering the entire BD pipeline — the
    partner ETL that processes 49 Financial's allocation, transaction, and
    portfolio data into gold-layer outputs consumed by AdvisorIntelligence
    and other client-facing portal views. This is your permanent activation
    document. The BD pipeline is the most operationally complex in the system
    (multi-stage gold layer, EC2 runner, ephemeral EC2 for historical prices,
    multiple publisher chains). Thorough documentation is critical.
  </objective>

  <scope>
    <files>
      <!-- Terraform module — read all .tf files -->
      <file action="read">infra/aws/terraform/bd-pipeline/main.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/iam.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/layers.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/ec2.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/s3-notifications.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/CHANGELOG.json</file>

      <!-- Gold layer scripts (EC2 runner) — document what each script does -->
      <file action="read">infra/aws/ec2/bd-gold-layer-runner/run_gold_layer.sh</file>

      <!-- Lambda source map — filter to bd- prefixed functions -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- EC2 manifest — bd services -->
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read all .tf files in infra/aws/terraform/bd-pipeline/ in full. Extract every
      aws_lambda_function, aws_lambda_layer_version, aws_cloudwatch_event_rule,
      aws_instance, aws_s3_bucket_notification, and aws_iam_role resource.
    </requirement>
    <requirement id="2">
      From lambda-source-map.json, extract source_path, memory_mb, timeout_s,
      and last_deployed_commit for all bd- prefixed functions:
      bd-allocation-processor, bd-allocation-trigger, bd-client-detail,
      bd-gold-detail-checker, bd-gold-foundation, bd-gold-layer, bd-gold-trigger,
      bd-portal-advisor-publisher, bd-portal-publisher, bd-price-update,
      bd-transactions-trigger. Also include historical-prices-scheduler (BD-owned).
    </requirement>
    <requirement id="3">
      Read run_gold_layer.sh to document the gold layer execution stages.
      The BD gold layer runs in numbered stages (01 through 10+) on an EC2 runner.
      Document each stage: script name, what it produces, dependencies, whether
      it runs in the full or incremental path.
    </requirement>
    <requirement id="4">
      From EC2_MANIFEST.json, identify all BD EC2 services: bd-gold-layer-runner
      (persistent), bd-gold-detail-generator (ephemeral), historical-prices EC2.
      Document instance IDs, source paths, and last deployed commits.
    </requirement>
    <requirement id="5">
      Document the full pipeline trigger chain:
      S3 drop (raw allocation/transaction file) → EventBridge or S3 notification →
      trigger Lambda → processor Lambda → gold layer stages → publisher Lambdas →
      portal S3 output. This chain is the operational heart of the BD pipeline.
    </requirement>
    <requirement id="6">
      Note the current Terraform tag from CHANGELOG.json as the version baseline.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      pipeline_inventory.xml exists at org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;pipeline_inventory&gt;
        &lt;metadata&gt; agent, pipeline="bd-pipeline", current_tag, date &lt;/metadata&gt;

        &lt;pipeline name="bd-pipeline" terraform_module="infra/aws/terraform/bd-pipeline/" current_tag="bd-vX.Y.Z"&gt;
          &lt;trigger_chain&gt;
            Ordered description of how a raw data file becomes portal output.
            Name every Lambda in sequence, every S3 key written, every EC2 stage.
          &lt;/trigger_chain&gt;

          &lt;lambdas&gt;
            One &lt;lambda&gt; per function:
              name, source_path, memory_mb, timeout_s, layers[], trigger, role_in_pipeline
          &lt;/lambdas&gt;

          &lt;gold_layer_stages&gt;
            One &lt;stage&gt; per gold script:
              script_name, stage_number, produces, depends_on, runs_in (full|incremental|both)
          &lt;/gold_layer_stages&gt;

          &lt;ec2_services&gt;
            One &lt;service&gt; per EC2:
              name, type (persistent|ephemeral), instance_id, source_path, last_deployed_commit
          &lt;/ec2_services&gt;

          &lt;eventbridge_rules&gt; rule name, schedule_or_trigger, target &lt;/eventbridge_rules&gt;
          &lt;s3_notifications&gt; bucket, prefix filter, target Lambda &lt;/s3_notifications&gt;
          &lt;layers&gt; layer name, S3 key, Python packages &lt;/layers&gt;
          &lt;iam_roles&gt; role names owned &lt;/iam_roles&gt;
        &lt;/pipeline&gt;

        &lt;known_issues&gt;
          Operational notes, known drift, gotchas from recent incidents
        &lt;/known_issues&gt;
      &lt;/pipeline_inventory&gt;
    </criterion>
    <criterion id="3">
      trigger_chain section must be complete — it is the primary operational reference
      for anyone debugging a data delivery failure.
    </criterion>
    <criterion id="4">
      All function names, instance IDs, script names, and tag values are verbatim
      from source files.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Terraform files or EC2 scripts. Read-and-document only.</constraint>
    <constraint>Do not run terraform plan, apply, or any AWS CLI commands.</constraint>
    <constraint>
      The BD pipeline has had several recent operational incidents (AUA undercount,
      triple-bug fix, EC2 gold runner expansion to scripts 09+10). Document known
      operational complexity in known_issues rather than trying to resolve it.
    </constraint>
    <constraint>
      historical-prices-scheduler is technically a BD pipeline asset (it feeds
      bd-price-update). Include it in the BD pipeline inventory even though its
      Lambda prefix is not bd-.
    </constraint>
  </constraints>

  <dependencies>
    <!-- No pod wave dependencies — AE pipelines are independent -->
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/pipeline_inventory.xml
    </deliverable>
  </deliverables>
</task_order>
```
