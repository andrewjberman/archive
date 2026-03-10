```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-partneretl-p3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-10</date>
    <status>pending</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
  </metadata>

  <objective>
    Build the bd-time-machine Lambda (Layer 2 of the Portal Time Machine). The PRD
    proposed a snapshot archive approach (copy gold/ to snapshots/{date}/ after each rebuild).
    This approach is UNNECESSARY. CLI audit confirmed S3 versioning is already enabled on
    opal-data-bd (confirmed 2026-03-10). Every gold/ file that gets overwritten by bd-portal-publisher
    already has its previous versions preserved in S3. The time machine can restore BD data
    by finding the version of each gold/ file that was current at 5:00 PM ET on the target date,
    using s3.list_object_versions() with a date cutoff. No new snapshot pipeline needed.
    Also add a bd-capture-output-versions Lambda that runs after bd-portal-publisher completes
    to record versionIds at each rebuild -- this gives faster restore (no need to scan version
    history) and a clean audit trail parallel to the yang archive pattern.
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/bd-pipeline/bd-capture-output-versions/lambda_function.py</file>
      <file action="create">infra/aws/lambda/bd-pipeline/bd-time-machine/lambda_function.py</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/main.tf</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="create">org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      bd-capture-output-versions Lambda:
      New Lambda at infra/aws/lambda/bd-pipeline/bd-capture-output-versions/lambda_function.py.
      Triggered by: S3 event on opal-data-bd/gold/pipeline-complete.json (same trigger as
      bd-portal-publisher, added as an additional destination -- NOT replacing it).
      Logic:
        1. List all objects under opal-data-bd/gold/ (recursive).
        2. For each object key, call head_object to get the current VersionId.
        3. Assemble a manifest: { "rebuild_date": "YYYY-MM-DD", "rebuild_completed_at": ISO8601,
           "outputs": { "gold/{key}": { "versionId": "...", "size": N } } }
        4. Write manifest to: opal-data-bd/snapshots/manifests/{YYYYMMDD-HHMMSS}.json
           (one manifest per rebuild, timestamped, never overwritten).
      This gives bd-time-machine a fast lookup path (scan manifests/, find latest before
      target_date) rather than calling list_object_versions on every file individually.
      The manifests/ prefix is also a permanent audit log of every BD rebuild.
    </requirement>

    <requirement id="2">
      bd-time-machine Lambda:
      New Lambda at infra/aws/lambda/bd-pipeline/bd-time-machine/lambda_function.py.
      Input event: { "target_date": "YYYY-MM-DD" }
      Logic:
        1. List all objects under opal-data-bd/snapshots/manifests/.
        2. Select the latest manifest whose rebuild_date <= target_date AND
           rebuild_completed_at <= 17:00 ET on target_date.
           If no manifest exists: fallback to list_object_versions on gold/ keys
           (slower but works even before manifests exist). Return 404 with earliest_available
           if no versions predate target_date.
        3. For each key/versionId in the selected manifest:
           call s3.copy_object(CopySource={Bucket=opal-data-bd, Key=key, VersionId=versionId},
           Bucket=opal-data-bd, Key=key) to restore that exact version to current.
        4. Trigger bd-portal-publisher by writing a sentinel to opal-data-bd/gold/pipeline-complete.json
           (this fires the S3 event trigger and runs the publisher to regenerate portal outputs
           from the restored gold/ files). Note: the publisher writes to the gold/ prefix --
           this is acceptable because the restored gold/ files are the source of truth and
           the publisher just generates derived outputs from them.
           ALTERNATIVE if publisher triggers a full gold rebuild (not just publishing): write
           a new sentinel format { "time_machine": true, "target_date": "YYYY-MM-DD" } and
           modify bd-portal-publisher to skip gold rebuild when time_machine flag is set.
           Read bd-portal-publisher source to determine which path applies.
        5. Invalidate CloudFront for /api/scoped/advisor-intelligence/* (this is the BD data path,
           confirmed from DT's Lambda@Edge v4 deploy log showing path pattern *.json behavior).
        6. Return { "restored_manifest": manifest_key, "rebuild_date": date, "files_restored": N }.
    </requirement>

    <requirement id="3">
      Terraform wiring:
        - Add bd-capture-output-versions Lambda to bd-pipeline Terraform.
        - Add S3 event notification for opal-data-bd/gold/pipeline-complete.json triggering
          bd-capture-output-versions (in ADDITION to existing bd-portal-publisher trigger).
        - Add bd-time-machine Lambda to bd-pipeline Terraform (256MB, 300s timeout).
        - Update lambda-source-map.json for both new Lambdas.
        - Note: bd-capture-output-versions needs s3:ListBucket + s3:GetObjectVersion +
          s3:PutObject on opal-data-bd. Coordinate with CloudOps (DRFR_PTMCH.P1) which
          is adding IAM for bd-time-machine; add capture Lambda permissions in the same PR.
    </requirement>

    <requirement id="4">
      Earliest available date determination:
      Since opal-data-bd versioning was already enabled BEFORE this project, historical
      versions of gold/ files may exist going back some time. Run:
        aws s3api list-object-versions --bucket opal-data-bd --prefix gold/timeseries_chart.json
          --query "Versions[*].{LastModified:LastModified,VersionId:VersionId}" --max-items 5
      Report the earliest version date in the findings doc. This is the earliest date
      the Time Machine can serve for BD data (before manifests existed, the fallback
      list_object_versions path handles restore).
    </requirement>

    <requirement id="5">
      FINDINGS DOCUMENT:
      Write org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md
      covering:
        - Versioning status: ENABLED on opal-data-bd (confirmed via CLI 2026-03-10)
        - PRD snapshot approach: SUPERSEDED -- versioning already on, using version-restore instead
        - bd-portal-publisher source path analysis (hardcoded or env var)
        - bd-portal-advisor-publisher scope (separate handling needed or covered by publisher)
        - Earliest available historical date from req 4 CLI output
        - Snapshot cost analysis: NOT NEEDED (versioning + lifecycle rule is the approach)
        - bd-capture-output-versions + bd-time-machine deployment notes
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      bd-capture-output-versions fires after next BD gold rebuild and writes a manifest
      to opal-data-bd/snapshots/manifests/. Manifest contains non-null versionIds for
      all gold/ files.
    </criterion>
    <criterion id="2">
      bd-time-machine invoked with a historical target_date (from the version history
      found in req 4) successfully restores gold/ files and triggers publisher.
      CloudFront invalidation fires for /api/scoped/advisor-intelligence/*.
    </criterion>
    <criterion id="3">
      Terraform 0-diff after apply. Source map updated. Git tag pushed.
    </criterion>
    <criterion id="4">
      Findings document complete. Clearly states: "Snapshot archive approach from PRD
      superseded -- S3 versioning already enabled on opal-data-bd."
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT create the snapshots/{YYYYMMDD}/ pattern from the PRD -- it is
    unnecessary and wasteful given versioning is already on. Use manifests/ instead.</constraint>
    <constraint>bd-capture-output-versions must NOT replace bd-portal-publisher as the
    S3 event target -- add it as an ADDITIONAL destination.</constraint>
    <constraint>Do NOT write to opal-data-portal-v2 for any BD advisor-intelligence data.
    BD data lives exclusively in opal-data-bd.</constraint>
    <constraint>Standard deployment protocol: terraform apply only. No aws lambda
    update-function-code.</constraint>
    <constraint>Coordinate with CloudOps on IAM (DRFR_PTMCH.P1) before deploying --
    bd-capture-output-versions needs s3:GetObjectVersion which may not be in the current
    bd-pipeline Lambda role.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="DRFR_PTMCH.P1.lifecycle-iam-cloudfront.md"
      status="pending"
      note="CloudOps P1 adds IAM permissions for cross-version operations on opal-data-bd.
      bd-capture-output-versions and bd-time-machine both need these permissions.
      Can develop in parallel but must coordinate on IAM before deploy."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">bd-capture-output-versions Lambda source + Terraform + S3 event wiring</deliverable>
    <deliverable type="commit">bd-time-machine Lambda source + Terraform</deliverable>
    <deliverable type="commit">lambda-source-map.json updated for both Lambdas</deliverable>
    <deliverable type="document">org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md</deliverable>
  </deliverables>
</task_order>
```
