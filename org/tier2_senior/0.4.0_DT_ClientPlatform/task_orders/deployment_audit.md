# Task Order: Deployment Audit

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-deployment-audit</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-02</date>
    <status>superseded</status>
  </metadata>

  <objective>
    Produce a deployment state audit mapping your pod's portal pages to the AWS
    infrastructure that serves them. Trace the data flow from Lambda/API Gateway
    endpoints through to the portal pages your RD agents build. This becomes your
    permanent deployment context for all future sessions.
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
  </scope>

  <requirements>
    <requirement id="1">For each page in your pod: identify which API endpoints it calls by reading the page's hooks and components (look for useQuery, useMutation, fetch calls with URL patterns like /api/scoped/ or /api/general/)</requirement>
    <requirement id="2">For each API endpoint found: trace it to the Lambda function that handles it using lambda-source-map.json and the Terraform lambdas.tf files</requirement>
    <requirement id="3">For each Lambda function serving your pages: document the function name, pipeline, trigger type, and last deployment date from lambda-source-map.json</requirement>
    <requirement id="4">Identify which data pipelines produce the data your pages consume -- trace S3 paths or database queries from Lambda source code back to pipeline scripts. Likely pipelines: bd-pipeline (advisor/client data from 49 Financial), portfolio-management</requirement>
    <requirement id="5">List all recent deployments (last_deployed_at in lambda-source-map.json) for functions in your scope</requirement>
    <requirement id="6">Identify any pages with NO clear data pipeline connection (potential gaps or hardcoded/mock data)</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Output is valid XML written to org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_audit.xml</criterion>
    <criterion id="2">Every page in your pod is mapped to at least one API endpoint or flagged as having no backend connection</criterion>
    <criterion id="3">Lambda function names match entries in lambda-source-map.json exactly</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify any source code or infrastructure -- this is a read-only audit</constraint>
    <constraint>Do NOT run terraform plan/apply or any AWS CLI commands</constraint>
    <constraint>Do NOT create or edit files outside your agent folder</constraint>
    <constraint>Use Glob, Grep, and Read tools only -- no Explore agent, no Task agent</constraint>
  </constraints>

  <deliverables>
    <deliverable type="document">
      org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/deployment_audit.xml
    </deliverable>
  </deliverables>
</task_order>

## Key Files to Read

- `infra/aws/lambda/ci/lambda-source-map.json` -- master Lambda registry
- Portal page directories for your pod's pages: ModelPortfolios, AdvisorIntelligence (list files, look for API calls)
- `infra/aws/terraform/bd-pipeline/lambdas.tf` -- advisor/client data functions (49 Financial)
- Any portfolio-management Terraform configs under `infra/aws/terraform/`
- Lambda function source code in `infra/aws/lambda/{function_name}/lambda_function.py`

## Deliverable XML Schema

Write your audit using this structure:

```xml
<deployment_audit>
  <metadata>
    <agent>0.4.0_DT_ClientPlatform</agent>
    <pod>ClientPlatform</pod>
    <date>2026-03-02</date>
  </metadata>

  <pages_served>
    <page name="ModelPortfolios" rd_agent="0.4.1_RD_ModelPortfolios">
      <api_endpoints>
        <endpoint url="/api/..." lambda="{function_name}" pipeline="{pipeline}" />
      </api_endpoints>
      <data_pipeline>
        Pipeline name, relevant scripts, S3 output paths
      </data_pipeline>
    </page>
    <page name="AdvisorIntelligence" rd_agent="0.4.2_RD_AdvisorIntelligence">
      <api_endpoints>
        <endpoint url="/api/..." lambda="{function_name}" pipeline="{pipeline}" />
      </api_endpoints>
      <data_pipeline>
        Pipeline name, relevant scripts, S3 output paths
      </data_pipeline>
    </page>
  </pages_served>

  <recent_deployments>
    <deployment function="{name}" commit="{sha}" date="{date}" />
  </recent_deployments>

  <terraform_resources>
    <resource pipeline="{name}" tf_file="{path}" type="{aws_resource_type}" />
  </terraform_resources>
</deployment_audit>
```
