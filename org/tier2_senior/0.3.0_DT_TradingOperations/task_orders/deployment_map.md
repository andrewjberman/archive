# Task Order — Deployment Map: TradingOperations

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-deployment-map-trading-operations</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.3.0_DT_TradingOperations</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
  </metadata>

  <objective>
    Produce a deployment_map.xml that is your permanent operational reference for
    the TradingOperations pod. This is the most infrastructure-complex pod: three
    Terraform modules (portfolio-management, yang-pipeline upload side, smartx-pipeline)
    and one EC2 service. The map gives a page-centric view (endpoints per page) and
    a Lambda-centric view (deployment state per function), plus critical_flows
    documenting the multi-Lambda sequences that are the pod's primary failure modes.
    Consolidates and supersedes the earlier deployment_audit task order.
  </objective>

  <scope>
    <pod>TradingOperations</pod>
    <pages>
      <page>PortfolioManagement</page>
      <page>TradeSubmission</page>
      <page>DataRefresh</page>
    </pages>
    <rd_agents>
      <agent>0.3.1_RD_PortfolioManagement</agent>
      <agent>0.3.2_RD_TradeSubmission</agent>
      <agent>0.3.3_RD_DataRefresh</agent>
    </rd_agents>
    <files>
      <!-- Wave outputs — start here -->
      <file action="read">org/tier2_senior/0.3.0_DS_TradingOperations/deliverables/data_contract.xml</file>
      <file action="read">org/tier2_senior/0.3.0_DE_TradingOperations/deliverables/pod_inventory.xml</file>
      <!-- Independent verification — read portal pages directly -->
      <file action="read">portal/src/pages/PortfolioManagement/</file>
      <file action="read">portal/src/pages/TradeSubmission/</file>
      <file action="read">portal/src/pages/DataRefresh/</file>
      <!-- Terraform modules -->
      <file action="read">infra/aws/terraform/portfolio-management/main.tf</file>
      <file action="read">infra/aws/terraform/portfolio-management/CHANGELOG.json</file>
      <file action="read">infra/aws/terraform/yang-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/stepfunctions.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/CHANGELOG.json</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/ec2.tf</file>
      <file action="read">infra/aws/terraform/smartx-pipeline/CHANGELOG.json</file>
      <!-- Deployment state -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.3.0_DT_TradingOperations/deliverables/deployment_map.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read data_contract.xml first — use critical_flows section as the backbone
      of your deployment map. The PM upload-to-optimization and trade-export-to-submission
      flows documented by DS map directly to your deployment concerns.
      Then independently verify by reading portal page directories: look for useQuery,
      useMutation, and fetch calls with /api/ patterns. Note any endpoints the
      wave documents missed.
    </requirement>
    <requirement id="2">
      For each portal page, document which API endpoints it calls (both GET read
      paths and POST/PUT write paths), the URL pattern, the Lambda handling each,
      and which Terraform module owns that Lambda.
    </requirement>
    <requirement id="3">
      For each Lambda serving this pod, extract from lambda-source-map.json:
      source_path, memory_mb, timeout_s, layers[], last_deployed_commit,
      last_deployed_at. Note the HTTP method (GET/POST/PUT) for API Gateway Lambdas.
    </requirement>
    <requirement id="4">
      Document the yang upload chain as a distinct deployment unit: yang-pipeline-trigger,
      yang-validate-files, yang-ingest-dynamodb, yang-move-to-processed. These
      are invoked via S3 upload event (PM uploads Excel), not EventBridge schedule.
      Note that the Terraform module is yang-pipeline (shared with PortfolioAnalytics)
      but the trigger path is entirely different.
    </requirement>
    <requirement id="5">
      SmartX: document opal-smartx-ingestion-pipeline Lambda and the smartx-exporter
      EC2 from EC2_MANIFEST.json (instance_id, source_path, last_deployed_commit).
      The EC2 feeds the fund universe for PM's funds-list dropdown.
    </requirement>
    <requirement id="6">
      Document the deployment sequence with explicit ordering constraints:
      SmartX EC2 must be current before PM can load the funds list;
      yang upload chain must be current for optimization results to appear.
    </requirement>
    <requirement id="7">
      Flag any pages with no clear data pipeline connection. Note any functions
      with lifecycle ignore_changes or non-standard deploy paths (smartx-exporter
      uses safe-ec2-deploy.sh, not terraform apply).
    </requirement>
    <requirement id="8">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      deployment_map.xml exists at org/tier2_senior/0.3.0_DT_TradingOperations/deliverables/deployment_map.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;deployment_map&gt;
        &lt;metadata&gt; agent, pod, rd_agents[], date &lt;/metadata&gt;

        &lt;pages_served&gt;
          One &lt;page&gt; per portal page:
            name, rd_agent,
            &lt;api_endpoints&gt;
              &lt;endpoint url="/api/..." method="GET|POST|PUT" lambda="{name}" pipeline="{module}" /&gt;
            &lt;/api_endpoints&gt;
            &lt;data_pipeline&gt; module name, S3 paths for reads and writes &lt;/data_pipeline&gt;
        &lt;/pages_served&gt;

        &lt;lambda_inventory&gt;
          One &lt;lambda&gt; per function:
            name, terraform_module, source_path, memory_mb, timeout_s,
            layers[], trigger, http_method (for API-Gateway functions),
            last_deployed_commit, last_deployed_at,
            &lt;serves_pages&gt; page and action &lt;/serves_pages&gt;
        &lt;/lambda_inventory&gt;

        &lt;critical_flows&gt;
          &lt;flow name="pm-upload-to-optimization"&gt;
            Ordered Lambda sequence: trigger, each step's module and trigger type
          &lt;/flow&gt;
          &lt;flow name="trade-export-to-submission"&gt;
            Ordered Lambda sequence: trigger, each step's module and trigger type
          &lt;/flow&gt;
        &lt;/critical_flows&gt;

        &lt;terraform_modules&gt;
          One &lt;module&gt; per Terraform module:
            path, current_tag, state_key,
            &lt;resources&gt; resource type + name &lt;/resources&gt;
        &lt;/terraform_modules&gt;

        &lt;ec2_services&gt;
          name, instance_id, source_path, last_deployed_commit,
          deploy_mechanism (safe-ec2-deploy.sh), feeds_pages[]
        &lt;/ec2_services&gt;

        &lt;recent_deployments&gt;
          One &lt;deployment&gt; per function: function, commit, date
        &lt;/recent_deployments&gt;

        &lt;deployment_sequence&gt;
          Ordered steps with dependency constraints noted
        &lt;/deployment_sequence&gt;

        &lt;known_gotchas&gt;
          EC2 uses safe-ec2-deploy.sh not terraform; yang-pipeline module is shared
          with PortfolioAnalytics; any ignore_changes exceptions
        &lt;/known_gotchas&gt;
      &lt;/deployment_map&gt;
    </criterion>
    <criterion id="3">
      critical_flows section must be complete — these are the primary failure
      modes for this pod. The DT must be able to diagnose and redeploy any
      step in these flows without looking elsewhere.
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
      yang-pipeline is shared with PortfolioAnalytics. You own the upload/ingest
      side (trigger, validate, ingest, move). yang-generate-* functions are
      PortfolioAnalytics DT territory. Document the boundary explicitly.
    </constraint>
    <constraint>
      smartx-exporter EC2 uses safe-ec2-deploy.sh, not terraform apply.
      Document this in known_gotchas — the deploy path is different from all
      other resources in this pod.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.3.0_DS_TradingOperations" task="data_contract" status="complete"/>
    <dependency agent="0.3.0_DE_TradingOperations" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.3.0_DT_TradingOperations/deliverables/deployment_map.xml
    </deliverable>
  </deliverables>
</task_order>
```
