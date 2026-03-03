# Task Order: Deployment Audit

<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-02-deployment-audit</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
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
  </scope>

  <requirements>
    <requirement id="1">For each page in your pod: identify which API endpoints it calls by reading the page's hooks and components (look for useQuery, useMutation, fetch calls with URL patterns like /api/scoped/ or /api/general/)</requirement>
    <requirement id="2">For each API endpoint found: trace it to the Lambda function that handles it using lambda-source-map.json and the Terraform lambdas.tf files</requirement>
    <requirement id="3">For each Lambda function serving your pages: document the function name, pipeline, trigger type, and last deployment date from lambda-source-map.json</requirement>
    <requirement id="4">Identify which data pipelines produce the data your pages consume -- trace S3 paths or database queries from Lambda source code back to pipeline scripts. Likely pipelines: yang-pipeline (factor/attribution data), smartx-pipeline (strategy data)</requirement>
    <requirement id="5">List all recent deployments (last_deployed_at in lambda-source-map.json) for functions in your scope</requirement>
    <requirement id="6">Identify any pages with NO clear data pipeline connection (potential gaps or hardcoded/mock data)</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Output is valid XML written to org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/deployment_audit.xml</criterion>
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
      org/tier2_senior/0.2.0_DT_PortfolioAnalytics/deliverables/deployment_audit.xml
    </deliverable>
  </deliverables>
</task_order>

## Key Files to Read

- `infra/aws/lambda/ci/lambda-source-map.json` -- master Lambda registry
- Portal page directories for your pod's pages: Positioning, Attribution, FactorTilts, Valuation, Macroeconomics, Correlation (list files, look for API calls)
- `infra/aws/terraform/yang-pipeline/lambdas.tf` -- factor/attribution data functions
- `infra/aws/terraform/smartx-pipeline/lambdas.tf` -- strategy data functions
- Lambda function source code in `infra/aws/lambda/{function_name}/lambda_function.py`

## Deliverable XML Schema

Write your audit using this structure:

```xml
<deployment_audit>
  <metadata>
    <agent>0.2.0_DT_PortfolioAnalytics</agent>
    <pod>PortfolioAnalytics</pod>
    <date>2026-03-02</date>
  </metadata>

  <pages_served>
    <page name="Positioning" rd_agent="0.2.1_RD_Positioning">
      <api_endpoints>
        <endpoint url="/api/..." lambda="{function_name}" pipeline="{pipeline}" />
      </api_endpoints>
      <data_pipeline>
        Pipeline name, relevant scripts, S3 output paths
      </data_pipeline>
    </page>
    <page name="Attribution" rd_agent="0.2.2_RD_Attribution">
      <api_endpoints>
        <endpoint url="/api/..." lambda="{function_name}" pipeline="{pipeline}" />
      </api_endpoints>
      <data_pipeline>
        Pipeline name, relevant scripts, S3 output paths
      </data_pipeline>
    </page>
    <page name="FactorTilts" rd_agent="0.2.3_RD_FactorTilts">
      <api_endpoints>
        <endpoint url="/api/..." lambda="{function_name}" pipeline="{pipeline}" />
      </api_endpoints>
      <data_pipeline>
        Pipeline name, relevant scripts, S3 output paths
      </data_pipeline>
    </page>
    <page name="Valuation" rd_agent="0.2.4_RD_Valuation">
      <api_endpoints>
        <endpoint url="/api/..." lambda="{function_name}" pipeline="{pipeline}" />
      </api_endpoints>
      <data_pipeline>
        Pipeline name, relevant scripts, S3 output paths
      </data_pipeline>
    </page>
    <page name="Macroeconomics" rd_agent="0.2.5_RD_Macroeconomics">
      <api_endpoints>
        <endpoint url="/api/..." lambda="{function_name}" pipeline="{pipeline}" />
      </api_endpoints>
      <data_pipeline>
        Pipeline name, relevant scripts, S3 output paths
      </data_pipeline>
    </page>
    <page name="Correlation" rd_agent="0.2.6_RD_Correlation">
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
