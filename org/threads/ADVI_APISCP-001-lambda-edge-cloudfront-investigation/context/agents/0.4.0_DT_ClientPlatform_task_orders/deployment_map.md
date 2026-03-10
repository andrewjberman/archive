# Task Order — Deployment Map: ClientPlatform

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-deployment-map-client-platform</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a deployment_map.xml that is your permanent operational reference for
    the ClientPlatform pod. This pod uniquely spans two entirely separate pipelines —
    yang (ModelPortfolios) and BD (AdvisorIntelligence). The map gives a page-centric
    view (endpoints per page), a Lambda-centric view (deployment state), and an
    explicit pipeline_split documenting exactly where your DT deployment authority
    ends and AE coordination begins.
    Consolidates and supersedes the earlier deployment_audit task order.
  </objective>

  <scope>
    <pod>ClientPlatform</pod>
    <pages>
      <page>ModelPortfolios</page>
      <page>AdvisorIntelligence</page>
    </pages>
    <rd_agents>
      <agent>0.4.1_RD_ModelPortfolios</agent>
      <agent>0.4.2_RD_AdvisorIntelligence</agent>
    </rd_agents>
    <files>
      <!-- Wave outputs — start here -->
      <file action="read">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</file>
      <file action="read">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/pod_inventory.xml</file>
      <!-- Independent verification — read portal pages directly -->
      <file action="read">portal/src/pages/ModelPortfolios/</file>
      <file action="read">portal/src/pages/AdvisorIntelligence/</file>
      <file action="read">portal/src/api/endpoints/advisor-intelligence.ts</file>
      <file action="read">portal/src/api/endpoints/aum.ts</file>
      <!-- Terraform modules -->
      <file action="read">infra/aws/terraform/yang-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/CHANGELOG.json</file>
      <file action="read">infra/aws/terraform/bd-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/s3-notifications.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/ec2.tf</file>
      <file action="read">infra/aws/terraform/bd-pipeline/CHANGELOG.json</file>
      <!-- Deployment state -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read data_contract.xml first — use the pipeline_split section as the
      primary organizer of your deployment map. Then independently verify by
      reading the portal page directories and endpoint files directly: look for
      useQuery, useMutation, and fetch calls. Note any endpoints the wave
      documents missed.
    </requirement>
    <requirement id="2">
      For each portal page, document which API endpoints it calls, the URL
      pattern, the Lambda handling each, and which pipeline owns it.
    </requirement>
    <requirement id="3">
      For each Lambda serving this pod, extract from lambda-source-map.json:
      source_path, memory_mb, timeout_s, layers[], last_deployed_commit,
      last_deployed_at. Identify which Terraform module owns it.
    </requirement>
    <requirement id="4">
      ModelPortfolios (Yang side): yang-model-portfolio-benchmarks is the single
      Lambda. Confirm from stepfunctions.tf whether it runs in the Step Functions
      state machine or independently. Document its S3 output key and the Yang
      versioning mechanism for the portal fetch.
    </requirement>
    <requirement id="5">
      AdvisorIntelligence (BD side): bd-portal-publisher, bd-portal-advisor-publisher,
      bd-client-detail, and opal-partners-data are your portal-facing Lambdas.
      Read s3-notifications.tf to confirm the trigger chain: gold layer completion
      sentinel → S3 notification → publisher Lambda. Document this chain explicitly.
    </requirement>
    <requirement id="6">
      From EC2_MANIFEST.json, document bd-gold-layer-runner and bd-gold-detail-generator
      as upstream EC2 dependencies. You do not own them (0.6.0_AE_PartnerETL does)
      but you need them as your diagnostic starting point when AdvisorIntelligence
      data is stale. Document instance IDs and last deployed commits.
    </requirement>
    <requirement id="7">
      Document the deployment authority boundary clearly: which Lambdas you can
      deploy independently vs what requires coordination with 0.6.0_AE_PartnerETL.
    </requirement>
    <requirement id="8">
      Flag any pages with no clear data pipeline connection. Note any functions
      with lifecycle ignore_changes or non-standard deploy paths.
    </requirement>
    <requirement id="9">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      deployment_map.xml exists at org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;deployment_map&gt;
        &lt;metadata&gt; agent, pod, rd_agents[], date &lt;/metadata&gt;

        &lt;pages_served&gt;
          One &lt;page&gt; per portal page:
            name, rd_agent, pipeline (yang|bd),
            &lt;api_endpoints&gt;
              &lt;endpoint url="/api/..." lambda="{name}" pipeline="{pipeline}" /&gt;
            &lt;/api_endpoints&gt;
            &lt;data_pipeline&gt; pipeline name, trigger chain, S3 output paths &lt;/data_pipeline&gt;
        &lt;/pages_served&gt;

        &lt;lambda_inventory&gt;
          One &lt;lambda&gt; per function — grouped by pipeline:
            name, pipeline (yang|bd), terraform_module, source_path,
            memory_mb, timeout_s, layers[], trigger,
            last_deployed_commit, last_deployed_at,
            &lt;serves_pages&gt; page and section &lt;/serves_pages&gt;
        &lt;/lambda_inventory&gt;

        &lt;pipeline_split&gt;
          &lt;yang_side&gt;
            Lambda, module, versioning model, DT deployment authority
          &lt;/yang_side&gt;
          &lt;bd_side&gt;
            Portal-facing Lambdas (DT authority) vs upstream EC2/gold layer (AE authority).
            S3 notification trigger chain from gold completion sentinel to publishers.
          &lt;/bd_side&gt;
        &lt;/pipeline_split&gt;

        &lt;terraform_modules&gt;
          One &lt;module&gt; per Terraform module:
            path, current_tag, state_key,
            &lt;resources&gt; resource type + name &lt;/resources&gt;
        &lt;/terraform_modules&gt;

        &lt;upstream_ec2_dependencies&gt;
          EC2 services owned by AE that feed this pod's Lambdas.
          name, instance_id, last_deployed_commit, owned_by (AE agent)
        &lt;/upstream_ec2_dependencies&gt;

        &lt;s3_triggers&gt;
          S3 notification rules that invoke pod Lambdas:
            bucket, prefix, event_type, target_lambda
        &lt;/s3_triggers&gt;

        &lt;recent_deployments&gt;
          One &lt;deployment&gt; per function: function, commit, date
        &lt;/recent_deployments&gt;

        &lt;deployment_sequence&gt;
          Separate sequences for Yang side and BD side
        &lt;/deployment_sequence&gt;

        &lt;known_gotchas&gt;
          AE coordination points, BD data lag, any ignore_changes exceptions
        &lt;/known_gotchas&gt;
      &lt;/deployment_map&gt;
    </criterion>
    <criterion id="3">
      pipeline_split section must be complete and unambiguous about deployment
      authority. This is the most operationally critical distinction for this pod.
    </criterion>
    <criterion id="4">
      Every Lambda name matches an entry in lambda-source-map.json exactly.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any source code or infrastructure. Read-and-document only.</constraint>
    <constraint>Do not run terraform plan, apply, or any AWS CLI commands.</constraint>
    <constraint>Use Glob, Grep, and Read tools only — no Explore agent, no Task agent.</constraint>
    <constraint>
      bd-pipeline infrastructure changes (EventBridge rules, S3 notifications,
      EC2 config) are owned by 0.6.0_AE_PartnerETL. Your DT authority covers
      portal-facing Lambda code only: bd-portal-publisher, bd-portal-advisor-publisher,
      bd-client-detail, opal-partners-data.
    </constraint>
    <constraint>
      yang-pipeline is shared across three pods. For yang-model-portfolio-benchmarks
      specifically, confirm with DS whether it runs in the Step Functions state machine.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="data_contract" status="complete"/>
    <dependency agent="0.4.0_DE_ClientPlatform" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_map.xml
    </deliverable>
  </deliverables>
</task_order>
```
