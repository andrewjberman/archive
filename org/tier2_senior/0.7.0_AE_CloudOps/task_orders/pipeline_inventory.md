# Task Order — Pipeline Inventory: CloudOps

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-pipeline-inventory-cloudops</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a pipeline_inventory.xml covering all shared infrastructure:
    shared-infra (S3 artifact buckets, Lambda layers), portal-notifications
    (all S3 triggers on opal-data-portal-v2), CloudFront distribution and
    behaviors (auth, routing, Lambda@Edge), and cross-cutting IAM/security
    resources. Unlike OpalETL and PartnerETL, you own infrastructure — not
    a data pipeline. Your deliverable maps every shared resource that other
    pipelines and the portal depend on.
  </objective>

  <scope>
    <files>
      <!-- Shared infra Terraform -->
      <file action="read">infra/aws/terraform/shared-infra/main.tf</file>

      <!-- Portal notifications — owns ALL S3 triggers on opal-data-portal-v2 -->
      <file action="read">infra/aws/terraform/portal-notifications/main.tf</file>
      <file action="read">infra/aws/terraform/portal-notifications/outputs.tf</file>

      <!-- Lambda@Edge and auth functions — in lambda-source-map -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>

      <!-- EC2 manifest — for any CloudOps-owned infrastructure EC2s -->
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>

      <!-- Lambda layer manifests — shared layers owned by shared-infra -->
      <file action="read">infra/aws/lambda/layers/</file>

      <!-- Output -->
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/pipeline_inventory.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read shared-infra/main.tf and portal-notifications/main.tf in full.
      shared-infra owns the three core S3 buckets (terraform-state,
      lambda-layers, lambda-artifacts) and the Lambda layer versions.
      portal-notifications owns all S3 event triggers on opal-data-portal-v2
      — every pipeline that publishes to that bucket registers its trigger here.
    </requirement>
    <requirement id="2">
      From lambda-source-map.json, identify Lambda@Edge and auth-related functions:
      opal-portal-authorizer, opalinvest-auth-handler, and any functions with
      "edge", "auth", "validator", or "router" in their name. These are CloudOps assets.
      Also include: opal-infrastructure-monitor, security-sweep-comprehensive,
      ec2-auto-shutdown-enforcer, cost-anomaly-scanner, access-anomaly-scanner,
      daily-agenda-generator.
    </requirement>
    <requirement id="3">
      Document the CloudFront architecture from what you can infer from the
      portal-proxy.ts endpoint naming and Lambda@Edge functions found in the
      source map. Three behavioral layers exist: viewer-request (auth gate),
      origin-request (routing), and origin (data). Map what you can find.
    </requirement>
    <requirement id="4">
      From infra/aws/lambda/layers/, list every Lambda layer with its requirements.txt
      path, S3 key, and which pipelines use it. Layers are shared infrastructure.
    </requirement>
    <requirement id="5">
      Document the S3 bucket structure: which bucket serves which purpose,
      what key patterns each pipeline uses for artifacts vs state vs portal data.
    </requirement>
    <requirement id="6">
      Note the Terraform backend for shared-infra (state key: shared-infra/tfstate)
      and the current tag from memory (shared-infra-v1.2.0). If a CHANGELOG.json
      exists, read it; if not, note it as missing.
    </requirement>
    <requirement id="7">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      pipeline_inventory.xml exists at org/tier2_senior/0.7.0_AE_CloudOps/deliverables/pipeline_inventory.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;pipeline_inventory&gt;
        &lt;metadata&gt; agent, scope="shared-infrastructure", date &lt;/metadata&gt;

        &lt;s3_buckets&gt;
          One &lt;bucket&gt; per S3 bucket owned or managed:
            name, purpose, key_patterns[], consumers[]
        &lt;/s3_buckets&gt;

        &lt;lambda_layers&gt;
          One &lt;layer&gt; per layer:
            name, s3_key, python_version, requirements_file, used_by_pipelines[]
        &lt;/lambda_layers&gt;

        &lt;portal_notifications&gt;
          One &lt;trigger&gt; per S3 event registered in portal-notifications/:
            bucket, prefix, event_type, target_lambda, owning_pipeline
        &lt;/portal_notifications&gt;

        &lt;cloudfront&gt;
          &lt;distribution&gt; ID or logical name &lt;/distribution&gt;
          &lt;behaviors&gt;
            One &lt;behavior&gt; per path pattern:
              path_pattern, viewer_request_fn, origin_request_fn, origin
          &lt;/behaviors&gt;
          &lt;lambda_at_edge&gt;
            One &lt;function&gt; per Lambda@Edge:
              name, event_type (viewer-request|origin-request), role
          &lt;/lambda_at_edge&gt;
        &lt;/cloudfront&gt;

        &lt;auth_infrastructure&gt;
          Auth Lambda names, Cognito pool (if discoverable), JWT flow summary
        &lt;/auth_infrastructure&gt;

        &lt;monitoring_lambdas&gt;
          Operational Lambdas not in any product pipeline:
            name, trigger, purpose
        &lt;/monitoring_lambdas&gt;

        &lt;terraform_modules&gt;
          One &lt;module&gt; per Terraform module owned:
            path, state_key, current_tag
        &lt;/terraform_modules&gt;

        &lt;known_issues&gt;
          Any unmanaged resources, missing Terraform coverage, or gaps
        &lt;/known_issues&gt;
      &lt;/pipeline_inventory&gt;
    </criterion>
    <criterion id="3">
      portal_notifications section must be complete — it is the authoritative
      record of how pipeline outputs trigger downstream portal refreshes.
    </criterion>
    <criterion id="4">
      All resource names, bucket names, and key patterns are verbatim from source files.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any Terraform files. Read-and-document only.</constraint>
    <constraint>Do not run terraform plan, apply, or any AWS CLI commands.</constraint>
    <constraint>
      The CloudFront distribution config is not fully in Terraform (behaviors were
      partially managed via console historically). Document what you can find in
      source files; note gaps in known_issues rather than fabricating resource names.
    </constraint>
    <constraint>
      infra/aws/lambda/layers/ is a directory — use Glob or ls to enumerate its
      contents, then read each requirements.txt found.
    </constraint>
    <constraint>
      You own shared infrastructure — not application logic. Do not document
      application-level Lambda functions (those belong to OpalETL or PartnerETL).
      Focus on cross-cutting resources that multiple pipelines depend on.
    </constraint>
  </constraints>

  <dependencies>
    <!-- No pod wave dependencies — CloudOps is independent -->
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.7.0_AE_CloudOps/deliverables/pipeline_inventory.xml
    </deliverable>
  </deliverables>
</task_order>
```
