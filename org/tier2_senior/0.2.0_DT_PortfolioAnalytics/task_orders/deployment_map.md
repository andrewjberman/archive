# Task Order — Deployment Map: PortfolioAnalytics

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-deployment-map-portfolio-analytics</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
    <date>2026-03-02</date>
    <status>complete</status><!-- completed: deliverable deployment_map.xml confirmed present at deliverables/ as of 2026-04-24 CTO startup audit -->
  </metadata>

  <objective>
    Produce a deployment_map.xml that is your permanent operational reference for
    the PortfolioAnalytics pod. All six pages are Yang-pipeline driven — your
    deployment map is a complete two-view reference to the yang-pipeline module:
    page-centric (which pages call which yang-generate-* endpoints) and
    Lambda-centric (deployment state, Step Functions position, module config).
    Consolidates and supersedes the earlier deployment_audit task order.
  </objective>

  <scope>
    <pod>PortfolioAnalytics</pod>
    <pages>
      <page>Positioning</page>
      <page>Attribution</page>
      <page>FactorTilts</page>
      <page>Valuation</page>
      <page>Macroeconomics</page>
      <page>Correlation</page>
    </pages>
    <rd_agents>
      <agent>0.2.1_RD_Positioning</agent>
      <agent>0.2.2_RD_Attribution</agent>
      <agent>0.2.3_RD_FactorTilts</agent>
      <agent>0.2.4_RD_Valuation</agent>
      <agent>0.2.5_RD_Macroeconomics</agent>
      <agent>0.2.6_RD_Correlation</agent>
    </rd_agents>
    <files>
      <!-- Wave outputs — start here -->
      <file action="read">org/tier2_senior/0.2.0_DS_PortfolioAnalytics/deliverables/data_contract.xml</file>
      <file action="read">org/tier2_senior/0.2.0_DE_PortfolioAnalytics/deliverables/pod_inventory.xml</file>
      <!-- Independent verification — read portal pages directly -->
      <file action="read">portal/src/pages/Positioning/</file>
      <file action="read">portal/src/pages/Attribution/</file>
      <file action="read">portal/src/pages/FactorTilts/</file>
      <file action="read">portal/src/pages/Valuation/</file>
      <file action="read">portal/src/pages/Macroeconomics/</file>
      <file action="read">portal/src/pages/Correlation/</file>
      <!-- Terraform -->
      <file action="read">infra/aws/terraform/yang-pipeline/lambdas.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/stepfunctions.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/eventbridge.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/iam.tf</file>
      <file action="read">infra/aws/terraform/yang-pipeline/CHANGELOG.json</file>
      <!-- Deployment state -->
      <file action="read">infra/aws/lambda/ci/lambda-source-map.json</file>
      <!-- Output -->
      <file action="create">org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/deployment_map.xml</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read data_contract.xml first — use it as your Lambda list and Yang pipeline
      overview (Step Functions execution order is documented there). Then
      independently verify by reading each portal page directory: look for useQuery,
      useMutation, and fetch calls. If direct reads reveal endpoints the wave
      documents missed, include them and note the gap.
    </requirement>
    <requirement id="2">
      For each portal page, document the API endpoint it calls, the URL pattern,
      the yang-generate-* Lambda that handles it, and its S3 output key pattern.
    </requirement>
    <requirement id="3">
      For each yang-generate-* Lambda, extract from lambda-source-map.json:
      source_path, memory_mb, timeout_s, layers[], last_deployed_commit,
      last_deployed_at. Also identify its position in the Step Functions
      execution (parallel batch, sequential, or terminal).
    </requirement>
    <requirement id="4">
      Read stepfunctions.tf. Document the full execution order: what runs in
      parallel, what runs sequentially, what the terminal states are. This is
      your primary diagnostic reference for a stalled Yang pipeline run.
    </requirement>
    <requirement id="5">
      Read eventbridge.tf. Document the trigger rule(s): schedule, target
      (state machine ARN or Lambda), and what this means for data freshness
      on your six pages.
    </requirement>
    <requirement id="6">
      Document the Yang versioning model from the data_contract: how the portal
      knows which S3 version to fetch after a pipeline run. Include the deployment
      implication — what happens to a portal session in-flight when a new Yang
      run completes and the manifest pointer updates.
    </requirement>
    <requirement id="7">
      Flag any pages with no clear data pipeline connection. Note any functions
      with lifecycle ignore_changes or non-standard deploy paths.
    </requirement>
    <requirement id="8">
      Mark task order status as "complete" when deliverable is written.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      deployment_map.xml exists at org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/deployment_map.xml
    </criterion>
    <criterion id="2">
      File follows this schema:
      &lt;deployment_map&gt;
        &lt;metadata&gt; agent, pod, rd_agents[], date &lt;/metadata&gt;

        &lt;pages_served&gt;
          One &lt;page&gt; per portal page:
            name, rd_agent,
            &lt;api_endpoints&gt;
              &lt;endpoint url="/api/..." lambda="{yang-generate-*}" s3_key="{pattern}" /&gt;
            &lt;/api_endpoints&gt;
            &lt;data_pipeline&gt; yang-pipeline, S3 key, versioning mechanism &lt;/data_pipeline&gt;
        &lt;/pages_served&gt;

        &lt;lambda_inventory&gt;
          One &lt;lambda&gt; per function:
            name, terraform_module, source_path, memory_mb, timeout_s,
            layers[], sfn_position (parallel|sequential|terminal),
            last_deployed_commit, last_deployed_at,
            &lt;serves_pages&gt; which pages &lt;/serves_pages&gt;
        &lt;/lambda_inventory&gt;

        &lt;step_functions&gt;
          State machine name, parallel stage Lambdas, sequential stages,
          terminal state, failure behavior
        &lt;/step_functions&gt;

        &lt;terraform_modules&gt;
          One &lt;module&gt;:
            path, current_tag, state_key,
            &lt;resources&gt; resource type + name &lt;/resources&gt;
        &lt;/terraform_modules&gt;

        &lt;eventbridge_schedules&gt;
          name, schedule, target, effect_on_pod
        &lt;/eventbridge_schedules&gt;

        &lt;versioning_model&gt;
          How portal fetches correct Yang version after each pipeline run
        &lt;/versioning_model&gt;

        &lt;recent_deployments&gt;
          One &lt;deployment&gt; per function: function, commit, date
        &lt;/recent_deployments&gt;

        &lt;deployment_sequence&gt;
          Ordered steps for deploying a Yang generator Lambda change
        &lt;/deployment_sequence&gt;

        &lt;known_gotchas&gt;
          S3 artifact upload required before apply, build-and-upload.sh,
          Windows zip behavior, any ignore_changes exceptions
        &lt;/known_gotchas&gt;
      &lt;/deployment_map&gt;
    </criterion>
    <criterion id="3">
      step_functions section must be complete — it is the primary reference
      for debugging a stalled Yang pipeline run.
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
      yang-pipeline is owned by 0.5.0_AE_OpalETL for pipeline-level changes.
      Lambda code changes are DT authority; Step Functions definition changes,
      new EventBridge rules, or new Lambda additions require AE coordination.
    </constraint>
    <constraint>
      yang-generate-cma belongs to MarketIntelligence pod. Include it only if
      data_contract.xml includes it. If excluded by DS, note it as out-of-scope.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.2.0_DS_PortfolioAnalytics" task="data_contract" status="complete"/>
    <dependency agent="0.2.0_DE_PortfolioAnalytics" task="pod_inventory" status="complete"/>
  </dependencies>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/deployment_map.xml
    </deliverable>
  </deliverables>
</task_order>
```
