<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-debt-1strun-004-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    Import the 18 non-trade S3 buckets into their appropriate TF pipelines.
    5 trade buckets are handled by .003. This covers the remaining 18 buckets
    identified in the infrastructure audit.
  </objective>

  <scope>
    <files>
      <file action="edit">infra/aws/terraform/shared-infra/*.tf</file>
      <file action="edit">infra/aws/terraform/bd-pipeline/*.tf</file>
      <file action="edit">infra/aws/terraform/market-overview/*.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="s3-imports">
      **S3 Bucket TF Imports**

      Triage all 18 non-trade buckets into 4 categories, then act:

      **Import (active, critical):**
      - `opalinvest-portal` -> shared-infra (portal static hosting)
      - `opal-data-schwab` -> bd-pipeline or shared-infra (Schwab data, critical)
      - `opal-data-trade-submissions` -> trade-pipeline (if .003 done) or shared-infra
      - `opal-cloudfront-logs-313476888478` -> shared-infra (logging)
      - `opal-cloudtrail-logs-313476888478` -> shared-infra (audit)
      - `opal-market-data-v2` -> market-overview
      - `opal-market-update` -> market-overview
      - `opal-analytics-dashboard` -> shared-infra
      - `opal-ci-staging` -> shared-infra

      For each: describe via AWS CLI, write TF resource in the appropriate pipeline,
      import into state, achieve 0-drift.

      **Flag for deletion (legacy/superseded):**
      - `opal-code-factorscanner-v2` (superseded by lambda-artifacts)
      - `opal-code-smartx-v2` (superseded by lambda-artifacts)
      - `opal-lambda-code-archive` (superseded by lambda-artifacts)
      - `smartx-exports-ajb327-20250118` (one-time export)
      - `opal-infrastructure-snapshots` (empty per audit)

      Do NOT delete -- just document as delete candidates in the deliverable.
      Andrew approves deletions.

      **Investigate (unclear):**
      - `opal-data-aaii-sentiment` vs `opal-data-aaii-v2` (duplicate?)
      - `ajb-workflow` (personal?)
      - `opal-313476888478-wyncht` (HTML report hosting -- active?)

      For each: check last modified date, object count, size. Report findings.

      **Already handled:**
      - 5 trade buckets -> DEBT_1STRUN.003
      - 3 shared-infra buckets (terraform-state, lambda-layers, lambda-artifacts) -> already in TF
    </deliverable>
  </deliverables>

  <tooling>
    1. **coverage_auditor** -- Source = all S3 buckets (aws s3 ls).
       Registry = all aws_s3_bucket resources across all TF pipeline dirs.
       Confirms gap count matches audit and catches new buckets.
  </tooling>

  <references>
    <ref type="audit">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DEBT_1STRUN.001_infrastructure_audit.md</ref>
  </references>

  <dependencies>
    None. Can run in parallel with .002 and .003.
  </dependencies>
</task_order>
