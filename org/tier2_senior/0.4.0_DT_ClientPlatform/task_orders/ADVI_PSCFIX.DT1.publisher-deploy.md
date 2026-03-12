# Task Order: ADVI_PSCFIX DT1 — Publisher Lambda Deploy + Portal Push

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-11-advi-pscfix-dt1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-11</date>
    <status>pending</status>
    <!-- UPDATED 2026-03-11 by 0.4.0_DS_ClientPlatform: added commit c3c8d072
         (GRO nna_start fix) and portal DEV commit 67090a4 (GRO aggregation fix).
         Both must go out with ea832f51. Deadline: 4PM DT. -->
  </metadata>

  <objective>
    Deploy the updated bd-portal-publisher Lambda (three CLOUD commits: ea832f51,
    c3c8d072) and push the portal DEV commit 67090a4 to PROD.
    Together these fix: (1) static NMNC/NMEC AUA chart, (2) certified_aua overrides
    on all total_aua fields, and (3) GRO vs NNA numerical consistency — the bug
    causing GRO to show $227M where NNA shows $353M for 2023 on the 3Y time window.
  </objective>

  <scope>
    <files>
      <!-- Lambda: two commits, one file -->
      <file action="deploy">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/CHANGELOG.json</file>
      <!-- Portal: one DEV commit to push to PROD -->
      <file action="push">portal/ (DEV -> PROD merge)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      LAMBDA DEPLOY — bd-portal-publisher (commits ea832f51 + c3c8d072 on CLOUD).

      What ea832f51 does:
        - Replaces rolling daily NMNC/NMEC with static period-bound classification
        - timeseries_chart.json aua key is now {quarterly, monthly, annually} sub-keys
          (old flat aua.data array is gone)
        - Adds _load_aua_certification() and _build_static_aua_periods() helpers
        - Applies certified_aua override to timeseries aua (proportional scale on
          current-period NMNC/NMEC) and simple replacement on header_metrics.json
          total.aua and all four snapshots/aua_by_{dim}.json total_aua

      What c3c8d072 does:
        - Fixes growth_decomposition monthly nna_net to use last-of-prior-month as
          start instead of first-of-current-month
        - This makes the sum of monthly nna values telescope to the same number as
          the NNA view's year-endpoint diff (eliminates a systematic ~$9M/year gap)

      Both commits touch only lambda_function.py. Build and deploy as a single artifact.

      Deploy sequence:
        1. build-and-upload.sh bd-pipeline bd-portal-publisher
           (head of CLOUD includes both commits)
        2. Commit updated lambda-source-map.json
        3. terraform plan bd-pipeline
           Expected: only bd-portal-publisher source_code_hash changes
        4. terraform apply bd-pipeline
        5. Verify 0-diff plan
        6. record-terraform-deploy.sh + git tag bd-vX.Y.Z + push --follow-tags

      Tag: check current tags first:
        git tag -l "bd-v*" | sort -V | tail -5
      Use the next patch increment on whatever is current.
    </requirement>

    <requirement id="2">
      PORTAL PUSH — portal DEV commit 67090a4 to PROD.

      What 67090a4 does:
        - Fixes GRO aggregation: aggregates all 12 months first, then filters which
          period labels to display based on time window
        - Prevents the bug where 3Y window showed only Apr-Dec 2023 ($227M) instead
          of the full Jan-Dec ($343M) in the GRO chart
        - Adds explanatory comment documenting the fix approach

      This is a frontend-only change in PartnerAnalytics.tsx.
      No Terraform involved. Standard DEV -> PROD merge and CloudFront invalidation.

      Push sequence:
        1. git checkout PROD (portal submodule)
        2. git merge DEV
        3. git push origin PROD
        4. CloudFront invalidation on /api/timeseries_chart* and portal assets
           (or full /* invalidation if easier)

      Verify: on 3Y window, GRO "2023" bar shows ~$343M NNA (not $227M).
      NNA view "2023" shows $353M. The ~$10M residual gap is the pre-fix
      backend data still in S3 — it disappears after the Lambda reruns.
    </requirement>

    <requirement id="3">
      After Lambda deploy, trigger a publisher rerun (or wait for nightly).
      After rerun, verify:
        - timeseries_chart.json has aua.quarterly / aua.monthly / aua.annually keys
        - growth_decomposition annual NNA sum matches NNA view year-endpoint diffs
          (expected: within $1 rounding, no $9M gap)
        - summary/header_metrics.json total.aua matches certified_aua when
          gold/aua_certification/{today}.json exists on S3
          (if cert file not yet present from A1, falls back gracefully -- that is OK)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Terraform 0-diff after apply. Only bd-portal-publisher updated.</criterion>
    <criterion id="2">bd-pipeline tag pushed. CHANGELOG.json updated.</criterion>
    <criterion id="3">Portal DEV merged to PROD and pushed. CloudFront invalidated.</criterion>
    <criterion id="4">On 3Y window: GRO 2023 shows full-year NNA (~$343M post-nightly-rerun,
      or ~$227M until next Lambda run — the frontend fix is visible immediately in how
      existing data is aggregated, but the backend nna_start fix requires a Lambda rerun).</criterion>
    <criterion id="5">Lambda memory/timeout unchanged. No layer changes needed.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Terraform is the only Lambda deploy mechanism. No aws lambda update-function-code.</constraint>
    <constraint>Portal PROD is merge-only from DEV. No direct commits to PROD.</constraint>
    <constraint>No emojis in commits or logs.</constraint>
    <constraint>Check current bd tag before tagging -- do not assume version number.</constraint>
    <constraint>A1 (certified_aua S3 JSONs from 0.6.0_AE_PartnerETL) is NOT required for
      this deploy. The publisher falls back gracefully when cert file is absent.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_PSCFIX.A2.publisher-restructure.md"
                status="complete"
                note="DS commits ea832f51 + c3c8d072 on CLOUD HEAD. Ready to build and deploy."/>
    <dependency agent="0.4.0_DE_ClientPlatform"
                task="ADVI_PSCFIX.B1.portal-schema-update.md"
                status="pending -- check DE logs"
                note="DE portal DEV commit 67090a4 also needs to go to PROD with this deploy."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">lambda-source-map.json + CHANGELOG.json updated (CLOUD)</deliverable>
    <deliverable type="deploy">bd-portal-publisher Lambda live (ea832f51 + c3c8d072)</deliverable>
    <deliverable type="tag">bd-vX.Y.Z pushed with --follow-tags</deliverable>
    <deliverable type="push">portal DEV 67090a4 merged to PROD and pushed</deliverable>
    <deliverable type="invalidation">CloudFront invalidation issued</deliverable>
  </deliverables>

  <references>
    <ref type="commit">ea832f51 -- ADVI_PSCFIX A2: static NMNC/NMEC + certified_aua override</ref>
    <ref type="commit">c3c8d072 -- GRO nna_start fix (last-of-prior-month, telescoping sum)</ref>
    <ref type="portal_commit">67090a4 (portal DEV) -- GRO aggregation: full-history sum then period filter</ref>
    <ref type="log">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-11/assets_overview_math_audit.md</ref>
    <ref type="prd">docs/architecture/ADVI_PSCFIX_PRD.md</ref>
  </references>
</task_order>
```
