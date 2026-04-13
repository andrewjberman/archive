<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-06-debt-1strun-005-ae</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-04-06</date>
    <status>pending</status>
    <project_code>DEBT_1STRUN</project_code>
  </metadata>

  <objective>
    Import remaining non-auth, non-trade DynamoDB tables and IAM roles into
    their appropriate TF pipelines. Clean up test Lambdas and migrate local-state
    TF directories to S3 backend.
  </objective>

  <scope>
    <files>
      <file action="edit">infra/aws/terraform/market-overview/*.tf</file>
      <file action="edit">infra/aws/terraform/shared-infra/*.tf</file>
      <file action="edit">infra/aws/terraform/bd-pipeline/*.tf</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="dynamo-imports">
      **DynamoDB Imports (4 tables)**

      Non-auth, non-trade tables from the audit:
      - `causality-generations` -> causality pipeline (create if needed, or shared-infra)
      - `causality-saved-analyses` -> causality pipeline
      - `market-updates` -> market-overview
      - `opal-pii-lookup` -> shared-infra (schwab anonymizer)

      Auth tables (opal-firms, sessions, permissions, offices, users, users-v2,
      invitations) already handled by AUTH_TFIMPT.
      Trade tables (recon-jobs, security-identifiers, trade-users) handled by .003.

      For each: describe, write TF resource, import, 0-drift.
    </deliverable>

    <deliverable id="iam-imports">
      **IAM Role Imports (13 roles)**

      Triage each role from the audit:

      **Import:**
      - `ec2-auto-shutdown-enforcer-role` -> shared-infra (migrate from local TF state)
      - `ec2-ssm-role` -> shared-infra
      - `infrastructure-ops-lambda-role` -> shared-infra
      - `infrastructure-snapshot-role` -> shared-infra
      - `market-data-generator-lambda-role` -> market-overview
      - `market-update-lambda-role` -> market-overview
      - `opal-layer3-ec2-role` -> news-pipeline
      - `MoltbotEC2Role` -> shared-infra (legacy but active)

      **Flag for audit (possibly stale):**
      - `bd-merge-daily-lambda-role` (legacy BD merge?)
      - `bd-pipeline-task-role` (legacy?)
      - `opal-smartx-lambda-role` (legacy SmartX)
      - `security-sweep-dedicated-role` (one-time scan?)

      For stale candidates: check last used date via
      `aws iam get-role --role-name X` (RoleLastUsed field).
      If unused >90 days, flag as delete candidate. Do NOT delete.

      `portal-auth-lambda-role` handled by AUTH_TFIMPT.003 assessment.
      Trade roles handled by .003.
    </deliverable>

    <deliverable id="cleanup">
      **Cleanup Items**

      1. **Delete test Lambdas** (after Andrew confirms):
         - `test-yfinance-simple`
         - `yfinance-aapl-test` (runtime=None, broken)
         Document the deletion command but do NOT execute without approval.

      2. **Migrate local-state TF to S3 backend:**
         - `infra/aws/lambda/ec2-auto-shutdown-enforcer/main.tf` (local state)
         - `infra/aws/terraform/causality/` (local state)
         - `infra/aws/terraform/seeking-alpha/` (local state)
         For each: add S3 backend block, run `terraform init -migrate-state`.

      3. **Sync EC2 manifest:**
         Run `./infra/aws/ec2/sync-ec2-manifest.sh` to populate null instance_ids
         for bd-gold-detail-generator and seeking-alpha-scraper.
    </deliverable>
  </deliverables>

  <tooling>
    1. **crossref_graph** -- Scope: all TF pipeline dirs + Lambda source dirs.
       Maps which IAM roles are referenced by which Lambdas/TF resources.
       Prevents importing a role into the wrong pipeline.

    2. **coverage_auditor** -- Run after all imports.
       Source = live AWS IAM roles + DynamoDB tables.
       Registry = all TF-managed resources.
       Final gap check -- should show significant coverage improvement.
  </tooling>

  <references>
    <ref type="audit">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/DEBT_1STRUN.001_infrastructure_audit.md</ref>
  </references>

  <dependencies>
    <dependency agent="0.5.0_AE_OpalETL" task="DEBT_1STRUN.002" status="pending"/>
    <dependency agent="0.5.0_AE_OpalETL" task="DEBT_1STRUN.003" status="pending"/>
  </dependencies>
</task_order>
