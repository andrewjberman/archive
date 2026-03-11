# Task Order: ADVI_PSCFIX DT1 — Publisher Lambda Deploy

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-advi-pscfix-dt1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-11</date>
    <status>pending</status>
  </metadata>

  <objective>
    Deploy the updated bd-portal-publisher Lambda (DS commit ea832f51). This commit
    implements static NMNC/NMEC period-bound classification, restructures timeseries_chart.json
    aua to quarterly/monthly/annually sub-keys, and applies certified_aua overrides to
    all total_aua fields when gold/aua_certification/{today}.json is present.
    After deploy, notify DE to validate integration against live data.
  </objective>

  <scope>
    <files>
      <file action="deploy">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/CHANGELOG.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Deploy bd-portal-publisher Lambda using standard bd-pipeline deployment protocol:
        1. build-and-upload.sh bd-pipeline bd-portal-publisher
        2. Commit updated lambda-source-map.json
        3. terraform plan bd-pipeline — confirm only bd-portal-publisher source_code_hash changes
        4. terraform apply bd-pipeline
        5. Verify 0-diff plan
        6. record-terraform-deploy.sh + git tag bd-vX.Y.Z + push --follow-tags

      Source commit to deploy: ea832f51
      (0.4.0_DS_ClientPlatform: bd-portal-publisher -- static NMNC/NMEC + certified_aua override)

      Tag version: check current bd-pipeline tags first:
        git tag -l "bd-v*" | sort -V | tail -5
      Next tag should be a patch increment on current latest.
    </requirement>

    <requirement id="2">
      After 0-diff verified, notify 0.4.0_DE_ClientPlatform to validate integration.
      DE needs to confirm:
        - AUA chart in AdvisorIntelligence Assets Overview renders with the new
          quarterly/monthly/annually granularity structure (no mock data fallback)
        - Granularity toggle switches between sub-keys correctly
        - Time window filter applies to end_date correctly
      DE's portal commit 8c51aaf (PSCFIX.B1) already wires the new schema.
      The validation is portal-side only — no code changes expected.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Terraform 0-diff after apply. Only bd-portal-publisher function updated.</criterion>
    <criterion id="2">bd-pipeline tag pushed. CHANGELOG.json updated.</criterion>
    <criterion id="3">Lambda invoked manually or via next nightly run produces
      timeseries_chart.json with aua.quarterly, aua.monthly, aua.annually sub-keys
      (not flat aua.data array).</criterion>
    <criterion id="4">DE notified to validate integration.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Terraform is the only deploy mechanism. No aws lambda update-function-code.</constraint>
    <constraint>No emojis in commits or logs.</constraint>
    <constraint>Check current bd tag before tagging — do not assume version number.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_PSCFIX.A2.publisher-restructure.md"
                status="complete"
                note="DS commit ea832f51 is on CLOUD and ready to deploy."/>
    <dependency agent="infra/aws/lambda/ci/lambda-source-map.json"
                task="build-and-upload must complete before plan"
                status="pending"/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">lambda-source-map.json + CHANGELOG.json updated</deliverable>
    <deliverable type="deploy">bd-portal-publisher Lambda live with PSCFIX schema</deliverable>
    <deliverable type="tag">bd-vX.Y.Z pushed with --follow-tags</deliverable>
    <deliverable type="handoff">DE notified to validate AUA chart integration</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_PSCFIX_PRD.md</ref>
    <ref type="commit">ea832f51 — DS publisher restructure (source to deploy)</ref>
    <ref type="task">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_PSCFIX.B1.portal-schema-update.md</ref>
  </references>
</task_order>
```
