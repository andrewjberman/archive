<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-bdpl-astdim-w6</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>BDPL_ASTDIM</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/BD_ASSET_DIM_PIPELINE.md</ref>
    <ref type="analogs">
      infra/aws/ssm/opal-bd-fees-download.json,
      infra/aws/lambda/bd-pipeline/bd-fees-trigger/,
      infra/aws/terraform/bd-pipeline/eventbridge.tf
    </ref>
  </references>

  <objective>
    Stand up the scheduling stack for asset-dim:
    - SSM document `opal-bd-asset-dim-download.json` (clone of fees doc; runs TS downloader + DS silver converter; shutdown +2; logs to s3://opal-data-bd/logs/asset-dim-download-$TODAY.log)
    - Lambda `bd-asset-dim-trigger` (clone of bd-fees-trigger; same IAM pattern: SSM SendCommand + EC2 StartInstances on bd-exporter)
    - EventBridge rule `bd_asset_dim_pipeline` cron: ~22:10 UTC Mon-Fri (AE confirms exact slot has no SSM-run collision on bd-exporter)
    - `infra/aws/lambda/ci/lambda-source-map.json` entry added for bd-asset-dim-trigger
    - Terraform apply via bd-pipeline stack, 0-diff verified, tag `bd-v2.24.0` (or next per memory rule), pushed --follow-tags
  </objective>

  <acceptance_criteria>
    1. SSM doc + Lambda + EventBridge rule live
    2. Terraform plan = 0-diff after apply
    3. Source map entry committed
    4. Git tag pushed (next bd-v* per `git tag -l "bd-v*" | sort -V | tail -5`)
    5. MCP COMPLETE message to COO with tag + plan output snippet
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-iam service bd-asset-dim-trigger` — verify SSM SendCommand + EC2 StartInstances permissions before terraform apply.
    Phase 2: `comp-iam gaps` after iam.tf change.
    Phase 3: `comp-pipescript deployed` on referenced silver scripts (DS W3 must be MATCH on S3).
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="BDPL_ASTDIM.W5" status="staged" description="TS downloader must exist on bd-exporter"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="BDPL_ASTDIM.W3" status="staged" description="Silver converter must be on S3 for SSM doc to invoke"/>
  </dependencies>

  <next>
    On COMPLETE: COO sends GO for W7 (first prod-run verification).
  </next>
</task_order>
