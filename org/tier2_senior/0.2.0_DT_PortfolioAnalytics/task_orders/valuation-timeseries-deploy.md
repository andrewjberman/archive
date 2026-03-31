<task_order>
  <metadata>
    <id>adhc-valuation-timeseries-monthly-dt</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DT_PortfolioAnalytics</issued_to>
    <date>2026-03-31</date>
    <status>complete</status>
  </metadata>

  <objective>
    Deploy the yang-generate-valuation Lambda after DS commits the monthly data
    change, then deploy the portal frontend after RD commits the label change.
    Two sequential deploys.
  </objective>

  <scope>
    <files>
      <file action="deploy">infra/aws/lambda/v2_portal/yang_pipeline/valuation/yang-generate-valuation/lambda_function.py</file>
      <file action="deploy">portal/src/pages/Valuation/tabs/ValuationTimeSeriesTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      BLOCKED until DS (0.2.0_DS_PortfolioAnalytics) commits the sample_months
      change to lambda_function.py on CLOUD.

      Once committed, deploy the yang-generate-valuation Lambda following the
      standard Lambda deployment protocol:
      1. Build zip via build-and-upload.sh
      2. terraform plan (yang-pipeline)
      3. terraform apply
      4. terraform plan (verify 0-diff)
      5. git tag yang-v{next} and push --follow-tags

      After deploy, trigger the Lambda manually or wait for the next scheduled run
      to regenerate valuation_data.json with monthly data points.
    </requirement>

    <requirement id="2">
      BLOCKED until RD (0.2.4_RD_Valuation) commits the frontend label change
      to portal DEV.

      Once committed, follow the standard portal deploy workflow:
      1. Merge DEV -> PROD
      2. Push PROD (CI deploys)
      3. Verify the Valuation page shows monthly labels
    </requirement>

    <requirement id="3">
      The Lambda deploy (req 1) should happen BEFORE the portal deploy (req 2)
      so that by the time the frontend renders monthly labels, the backend is
      already serving monthly data. If the frontend deploys first, it will
      still work (the formatter handles any data density), but the labels will
      show monthly format with semi-annual data points until the Lambda runs.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">yang-generate-valuation Lambda deployed with monthly data output</criterion>
    <criterion id="2">valuation_data.json on S3 contains monthly data points (~12/year per metric)</criterion>
    <criterion id="3">Portal Valuation page shows monthly x-axis labels on the time series chart</criterion>
    <criterion id="4">Yang pipeline tag incremented (yang-v{next})</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Follow Lambda Deployment Protocol exactly -- commit before apply, tag after 0-diff.</constraint>
    <constraint>Check current yang tag before tagging: `git tag -l "yang-v*" | sort -V | tail -5`</constraint>
    <constraint>Do not modify the Lambda code or portal code -- only deploy what DS and RD committed.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.2.0_DS_PortfolioAnalytics" task="backend-monthly-data" status="complete">Lambda code change committed to CLOUD — commit 7ee774e0</dependency>
    <dependency agent="0.2.4_RD_Valuation" task="frontend-monthly-labels" status="complete">Frontend code change committed to portal DEV -- commits 38527e2, ac35d66</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="deploy">yang-generate-valuation Lambda redeployed (yang-v{next})</deliverable>
    <deliverable type="deploy">Portal PROD with monthly valuation labels (portal-v{next})</deliverable>
  </deliverables>
</task_order>
