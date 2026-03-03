# Task Order — Deployment Map: MarketIntelligence

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-deployment-map-market-intelligence</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.1.0_DT_MarketIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
  </metadata>

  <objective>
    Produce a deployment_map.xml that is your permanent operational reference for
    the MarketIntelligence pod. It gives you two complementary views: a page-centric
    view (which endpoints each page calls and which Lambda handles them) and a
    Lambda-centric view (deployment state, module ownership, trigger, config).
    Together these let you orient instantly at session start and diagnose failures
    without re-reading infrastructure files each time.
    Consolidates and supersedes the earlier deployment_audit task order.
  </objective>

  <scope>
    <pod>MarketIntelligence</pod>
    <pages>
      <page>MarketPerformance</page>
      <page>CausalityEngine</page>
      <page>MarketUpdate</page>
      <page>CapitalMarketAssumptions</page>
    </pages>
    <rd_agents>
      <agent>0.1.1_RD_MarketPerformance</agent>
      <agent>0.1.2_RD_CausalityEngine</agent>
      <agent>0.1.3_RD_CapitalMarketAssumptions</agent>
    </rd_agents>
    <files>
      <!-- Wave outputs — start here -->
      <file action="read">org/tier2_senior/0.1.0_DS_MarketIntelligence/deliverables/data_contract.xml</file>
      <file action="read">org/tier2_senior/0.1.0_DE_MarketIntelligence/deliverables/pod_inventory.xml</file>
      <!-- Independent verification — read portal pages directly -->
      <file action="read">portal/src/pages/MarketPerformance/hooks.ts</file>
      <file action="read">portal/src/pages/CausalityEngine/</file>
      <file action="read">portal/src/pages/CapitalMarketAssumptions/</file>
      <!-- Terraform modules -->
      <file action="read">infra/aws/terraform/market-overview/lambdas.tf</file>
      <file action="read">infra/aws/terraform/market-overview/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/market-overview/iam.tf</file>
      <file action="read">infra/aws/terraform/market-overview/CHANGELOG.json</file>
      <file action="read">infra/aws/terraform/causality/main.tf</file>
      <file action="read">infra/aws/terraform/news-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/news-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/news-pipeline/CHANGELOG.json</file>
      <!-- Deployment state -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="read">infra/aws/ec2/EC2_MANIFEST.json</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.1.0_DT_MarketIntelligence/deliverables/deployment_map.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read data_contract.xml and pod_inventory.xml first — use them as your
      primary Lambda list and endpoint mapping. Then independently verify by
      reading the portal page hook files directly (look for useQuery, useMutation,
      and fetch calls with /api/scoped/ or /api/general/ URL patterns). If direct
      reads reveal endpoints the wave documents missed, include them and note the gap.
    </requirement>
    <requirement id="2">
      For each portal page, document which API endpoints it calls, the URL pattern,
      the Lambda that handles it, and which pipeline owns that Lambda.
    </requirement>
    <requirement id="3">
      For each Lambda serving this pod, extract from lambda-source-map.json:
      source_path, memory_mb, timeout_s, layers[], last_deployed_commit,
      last_deployed_at. Identify which Terraform module owns it.
    </requirement>
    <requirement id="4">
      From the Terraform eventbridge.tf files, extract all scheduled rules:
      name, cron/rate schedule, target Lambda. These are the automated data
      refresh triggers your pages depend on — knowing the schedule is knowing
      when stale data is expected to clear.
    </requirement>
    <requirement id="5">
      Check EC2_MANIFEST.json for any EC2 services in this pod's data path
      (seeking-alpha scraper may feed the news pipeline that feeds SentimentPanel).
    </requirement>
    <requirement id="6">
      Document the deployment sequence: which modules to deploy in what order
      for a full pod refresh, and why the order matters.
    </requirement>
    <requirement id="7">
      Flag any pages with no clear data pipeline connection as gaps.
      Flag any functions with lifecycle ignore_changes or non-standard deploy paths.
    </requirement>
    <requirement id="8">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      deployment_map.xml exists at org/tier2_senior/0.1.0_DT_MarketIntelligence/deliverables/deployment_map.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;deployment_map&gt;
        &lt;metadata&gt; agent, pod, rd_agents[], date &lt;/metadata&gt;

        &lt;pages_served&gt;
          One &lt;page&gt; per portal page:
            name, rd_agent,
            &lt;api_endpoints&gt;
              &lt;endpoint url="/api/..." lambda="{name}" pipeline="{pipeline}" /&gt;
            &lt;/api_endpoints&gt;
            &lt;data_pipeline&gt; pipeline name, S3 output paths &lt;/data_pipeline&gt;
        &lt;/pages_served&gt;

        &lt;lambda_inventory&gt;
          One &lt;lambda&gt; per function serving this pod:
            name, terraform_module, source_path, memory_mb, timeout_s,
            layers[], trigger, last_deployed_commit, last_deployed_at,
            &lt;serves_pages&gt; which pages &lt;/serves_pages&gt;
        &lt;/lambda_inventory&gt;

        &lt;terraform_modules&gt;
          One &lt;module&gt; per Terraform module:
            path, current_tag, state_key,
            &lt;resources&gt; resource type + name for each owned resource &lt;/resources&gt;
        &lt;/terraform_modules&gt;

        &lt;eventbridge_schedules&gt;
          One &lt;rule&gt; per scheduled trigger:
            name, schedule, target_lambda, effect_on_pod
        &lt;/eventbridge_schedules&gt;

        &lt;ec2_services&gt; any EC2 in the data path &lt;/ec2_services&gt;

        &lt;recent_deployments&gt;
          One &lt;deployment&gt; per function:
            function, commit, date
        &lt;/recent_deployments&gt;

        &lt;deployment_sequence&gt;
          Ordered steps for a full pod refresh, with dependency rationale
        &lt;/deployment_sequence&gt;

        &lt;known_gotchas&gt;
          Deployment warnings, ignore_changes exceptions, cross-module boundaries
        &lt;/known_gotchas&gt;
      &lt;/deployment_map&gt;
    </criterion>
    <criterion id="3">
      Every page is mapped to at least one endpoint, or explicitly flagged as
      having no backend connection.
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
      market-overview, news-pipeline, and causality Terraform modules are owned
      by 0.5.0_AE_OpalETL for pipeline-level changes. Document the boundary:
      Lambda code changes are DT authority; new resources or EventBridge changes
      require AE coordination.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.1.0_DS_MarketIntelligence" task="data_contract" status="complete"/>
    <dependency agent="0.1.0_DE_MarketIntelligence" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.1.0_DT_MarketIntelligence/deliverables/deployment_map.xml
    </deliverable>
  </deliverables>
</task_order>
```
