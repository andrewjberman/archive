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
    <revised>2026-03-10 -- REVISED post agent review. Critical correction: bd-capture-output-versions
    cannot be an additional S3 event destination on pipeline-complete.json -- S3 does not allow two
    notification rules with the same prefix+suffix filter. Use Lambda-to-Lambda fan-out from
    bd-portal-publisher (same pattern as bd-portal-advisor-publisher). Terraform scope updated
    accordingly. New dedicated IAM roles confirmed (Option A). Publisher source path is env-var
    backed -- no time_machine flag needed. Go-ahead: start Phase A now.</revised>
  </metadata>

  <objective>
    Build bd-capture-output-versions and bd-time-machine Lambdas (Layer 2 of Portal Time Machine).
    S3 versioning is already enabled on opal-data-bd (confirmed 2026-03-10). No snapshot archive
    approach needed -- use version-restore identical in pattern to Layer 1 (yang). PartnerETL owns
    all IAM for BD Lambda roles in bd-pipeline. CloudOps P1 is NOT a gate for BD IAM.
    The only CloudOps dependency is the CloudFront invalidation path for /api/scoped/* (needed
    by bd-time-machine to invalidate after restore).
  </objective>

  <scope>
    <files>
      <file action="create">infra/aws/lambda/bd-pipeline/bd-capture-output-versions/lambda_function.py</file>
      <file action="create">infra/aws/lambda/bd-pipeline/bd-time-machine/lambda_function.py</file>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/main.tf</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/lambdas.tf</file>
      <file action="modify">infra/aws/terraform/bd-pipeline/iam.tf</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="create">org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      bd-capture-output-versions Lambda -- trigger via Lambda-to-Lambda fan-out (NOT S3 event):
      CRITICAL CORRECTION from original task order: S3 does not allow two notification rules
      with the same prefix+suffix filter on the same bucket+event type. bd-portal-publisher
      already holds the exclusive S3 notification rule on gold/pipeline-complete.json.
      bd-capture-output-versions must be invoked by bd-portal-publisher async at completion --
      identical pattern to how bd-portal-publisher invokes bd-portal-advisor-publisher
      (line ~1694 in publisher source: lam.invoke(... InvocationType='Event')).

      Implementation:
        - Add CAPTURE_VERSIONS_FUNCTION env var to bd-portal-publisher Terraform module
        - Add one async invoke call at the end of bd-portal-publisher's success path
          (after all publish writes complete, same location as advisor-publisher invoke)
        - aws_lambda_permission for bd-portal-publisher to invoke bd-capture-output-versions
          (Principal: lambda.amazonaws.com, SourceArn: bd-portal-publisher ARN)
        - Do NOT modify aws_s3_bucket_notification.bd_data_bucket -- S3 wiring stays untouched

      bd-capture-output-versions Lambda logic:
        1. List all objects under opal-data-bd/gold/ (recursive, paginated).
        2. For each object key, call head_object to get current VersionId.
        3. Assemble manifest: { "rebuild_date": "YYYY-MM-DD", "rebuild_completed_at": ISO8601,
           "source": "bd-portal-publisher-fanout",
           "outputs": { "gold/{key}": { "versionId": "...", "size": N } } }
           Use rebuild_completed_at = datetime.utcnow().isoformat() + "Z".
           Derive rebuild_date from the gold/ timeseries_chart.json data_as_of field if available,
           otherwise use UTC date.
        4. Write manifest to: opal-data-bd/snapshots/manifests/{YYYYMMDD-HHMMSS}.json
           (timestamped, never overwritten -- permanent rebuild audit log).
    </requirement>

    <requirement id="2">
      bd-time-machine Lambda:
      Path: infra/aws/lambda/bd-pipeline/bd-time-machine/lambda_function.py
      Input: { "target_date": "YYYY-MM-DD" }
      Logic:
        1. List opal-data-bd/snapshots/manifests/ (paginated). Select latest manifest where
           rebuild_date <= target_date AND rebuild_completed_at <= 17:00 ET on target_date.
        2. If no manifest exists (pre-deploy history): fallback to s3.list_object_versions
           on each gold/ key to find the version current at 5pm ET on target_date.
           This is slower but handles dates before bd-capture-output-versions was deployed.
           Return 404 with { "error": "no_restore_point", "earliest_available": date } if
           no versions predate target_date.
        3. For each key/versionId: s3.copy_object(CopySource={Bucket=opal-data-bd, Key, VersionId},
           Bucket=opal-data-bd, Key=key). Collect failures, continue on error.
        4. Publisher source path is env-var backed (INPUT_BUCKET / OUTPUT_BUCKET from lambdas.tf).
           NO time_machine flag needed. Trigger bd-portal-publisher by writing sentinel:
           s3.put_object(Bucket="opal-data-bd", Key="gold/pipeline-complete.json",
                         Body=json.dumps({"time_machine": True, "target_date": target_date}))
           This fires the existing S3 event notification and triggers the publisher to regenerate
           portal JSON from the restored gold/ files.
        5. CloudFront invalidation: use the /api/scoped/advisor-intelligence/* path (confirmed
           by DT's Lambda@Edge v4 deploy log showing the behavior path pattern is
           /api/scoped/advisor-intelligence/*.json). Verify against CloudOps P1 findings doc
           when available -- but this path is already known from ADVI_APISCP work.
        6. Return { "restored_manifest": key, "rebuild_date": date,
                    "files_restored": N, "files_failed": [key, ...] }.
    </requirement>

    <requirement id="3">
      IAM -- new dedicated roles (Option A confirmed):
      Add to infra/aws/terraform/bd-pipeline/iam.tf:

      bd-capture-versions-lambda-role:
        - s3:GetObjectVersion on opal-data-bd/*
        - s3:ListBucket + s3:ListObjectVersions on opal-data-bd
        - s3:PutObject on opal-data-bd/snapshots/manifests/*

      bd-time-machine-lambda-role:
        - s3:ListObjectVersions + s3:ListBucket on opal-data-bd
        - s3:GetObjectVersion on opal-data-bd/*
        - s3:CopyObject on opal-data-bd/*
        - s3:PutObject on opal-data-bd/gold/* (for sentinel write)
        - cloudfront:CreateInvalidation on arn:aws:cloudfront::313476888478:distribution/EVTSA9VEHNZVH

      PartnerETL owns bd-pipeline/iam.tf. Add these directly. No CloudOps involvement needed for IAM.

      Also add aws_lambda_permission for bd-portal-publisher to invoke bd-capture-output-versions.
    </requirement>

    <requirement id="4">
      Earliest available date -- run before writing findings doc:
      export MSYS_NO_PATHCONV=1
      aws s3api list-object-versions \
        --bucket opal-data-bd \
        --prefix gold/timeseries_chart.json \
        --query "Versions[*].{LastModified:LastModified,VersionId:VersionId}" \
        --max-items 5
      Report the earliest version date. This is the Time Machine earliest available date
      for BD data (fallback path handles dates before manifests exist).
    </requirement>

    <requirement id="5">
      Terraform wiring (lambdas.tf / main.tf):
        - bd-capture-output-versions: new Lambda module, role = bd-capture-versions-lambda-role,
          memory 256MB, timeout 120s.
        - bd-time-machine: new Lambda module, role = bd-time-machine-lambda-role,
          memory 256MB, timeout 300s.
        - bd-portal-publisher module: add CAPTURE_VERSIONS_FUNCTION env var.
        - s3-notifications.tf: add comment documenting the three-way fan-out chain:
          "S3 event: pipeline-complete.json -> bd-portal-publisher -> [bd-portal-advisor-publisher (async), bd-capture-output-versions (async)]"
        - lambda-source-map.json: add both new Lambdas.
    </requirement>

    <requirement id="6">
      FINDINGS DOCUMENT:
      Write org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md
      covering:
        - Versioning status: ENABLED on opal-data-bd (confirmed 2026-03-10 CLI)
        - PRD snapshot approach: SUPERSEDED -- versioning already on; using version-restore + manifests
        - Trigger correction: Lambda-to-Lambda fan-out (not S3 event) -- S3 constraint documented
        - bd-portal-publisher source path: env-var backed (INPUT_BUCKET, OUTPUT_BUCKET)
        - No time_machine flag needed in publisher -- sentinel fires existing S3 event
        - Earliest available BD date from req 4 CLI output
        - New dedicated roles (bd-capture-versions-lambda-role, bd-time-machine-lambda-role)
        - bd-portal-advisor-publisher: no change needed (publisher invokes it, restore covers gold/)
        - Deployment tag: bd-v2.18.0
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      After next BD gold rebuild, bd-capture-output-versions fires (invoked by bd-portal-publisher)
      and writes a manifest to opal-data-bd/snapshots/manifests/. Manifest contains non-null
      versionIds for all gold/ files.
    </criterion>
    <criterion id="2">
      bd-time-machine invoked with a historical target_date (from req 4 version history)
      restores gold/ files, fires publisher sentinel, publisher regenerates portal JSONs,
      CloudFront invalidation fires for /api/scoped/advisor-intelligence/*.
    </criterion>
    <criterion id="3">
      Terraform 0-diff after apply. lambda-source-map.json updated. pipeline_inventory.xml updated.
      record-terraform-deploy.sh run. Tag bd-v2.18.0 pushed.
    </criterion>
    <criterion id="4">Findings doc complete. States clearly: "Snapshot archive approach superseded."</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>CRITICAL: Do NOT add a second S3 event notification for pipeline-complete.json.
    S3 rejects two rules with identical prefix+suffix. Use Lambda-to-Lambda fan-out only.</constraint>
    <constraint>Do NOT modify aws_s3_bucket_notification.bd_data_bucket -- S3 wiring stays untouched.</constraint>
    <constraint>Do NOT write advisor-intelligence data to opal-data-portal-v2. BD data stays in opal-data-bd.</constraint>
    <constraint>Standard deployment protocol: terraform apply only. No aws lambda update-function-code.</constraint>
    <constraint>IAM is fully owned by PartnerETL in bd-pipeline/iam.tf. Do not coordinate with CloudOps for IAM.</constraint>
  </constraints>

  <go_ahead>
    PROCEED IMMEDIATELY on Phase A (all code development):
      - Req 1 (bd-capture-output-versions code + bd-portal-publisher fan-out addition)
      - Req 2 (bd-time-machine code)
      - Req 3 (IAM new roles in iam.tf)
      - Req 4 (CLI: earliest version date)
      - Req 5 (Terraform modules, stub role ARNs, env vars)
      - Req 6 (findings doc)
    HOLD terraform apply (Phase B) until CloudOps P1 delivers findings doc confirming CF paths.
    CF path for /api/scoped/advisor-intelligence/* is already known from ADVI_APISCP work --
    you may hardcode this and note it is pre-confirmed pending CloudOps P1 final table.
  </go_ahead>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="DRFR_PTMCH.P1.lifecycle-iam-cloudfront.md"
      status="pending" scope="CloudFront path confirmation only"
      note="CloudOps P1 is NOT a gate for IAM (PartnerETL owns BD IAM). Gate is CF path table
      from CloudOps P1 req 3. CF path for /api/scoped/advisor-intelligence/* is already
      known from ADVI_APISCP -- can pre-hardcode and validate against CloudOps P1 output."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">bd-capture-output-versions Lambda source</deliverable>
    <deliverable type="commit">bd-time-machine Lambda source</deliverable>
    <deliverable type="commit">bd-portal-publisher fan-out addition + CAPTURE_VERSIONS_FUNCTION env var</deliverable>
    <deliverable type="commit">bd-pipeline/iam.tf new dedicated roles</deliverable>
    <deliverable type="commit">bd-pipeline Terraform modules + lambda-source-map.json update. Tag: bd-v2.18.0.</deliverable>
    <deliverable type="document">org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/DRFR_PTMCH.001.bd-pipeline-findings.md</deliverable>
  </deliverables>
</task_order>
```
