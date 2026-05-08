<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.023</id>
    <project>ADHC_COMPIL_V4</project>
    <title>BD Lambda permission-gap remediation — investigate + patch the 9 gaps surfaced by V4.022 Cat 6.1 IAM backfill</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>0.7.0_AE_CloudOps (self-author per Andrew direct 2026-05-08T~PM "sure yeah do it")</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- Closed 2026-05-08T~PM by AE 0.7.0 per Andrew direct "sure yeah do it". 1 of 9 gaps was real (bd-time-machine s3:CopyObject; 2 line refs same fix); 7 false positives documented per gap_classification table. terraform apply on bd-pipeline added s3:CopyObject statement (CopyVersionedRestore Sid) on opal-data-bd/gold/* — 1 to change, 0 add/destroy; post-apply 0-diff verified. comp-iam gaps post-apply: 9 → 7 (bd-time-machine cleared from list; ops show [GRANTED]). 7 remaining gaps are EC2-shipped-shell or AWS-managed-policy false positives — surfaced as comp-iam follow-on improvement candidates per Phase 4 step (ADHC_COMPIL_V5 candidates: managed-policy parsing + EC2-shipped-shell distinction). -->
    <priority>normal</priority>
    <estimated_effort>~0.5d (mostly investigation; few real bugs)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md (V4 family)</ref>
    <ref type="parent_to">ADHC_COMPIL_V4.022 Cat 6.1 — IAM backfill surfaced 9 gaps</ref>
    <ref type="andrew_direct">2026-05-08T~PM: CTO queued "tonight or tomorrow?"; Andrew → "sure yeah do it"</ref>
  </references>

  <context>
    V4.022 Cat 6.1 backfilled lambda-source-map iam_role mappings for 95+ BD Lambdas.
    Post-backfill, comp-iam gaps surfaced 9 permission gaps that were previously
    silently skipped due to missing role mappings. Per V4.022 out-of-scope ruling,
    REMEDIATION was queued separately. This TO scopes that remediation.
  </context>

  <gap_classification>

  Investigation per gap (read each Lambda source + iam.tf + classify):

  | Gap | Service | Action | Classification | Reason |
  |---|---|---|---|---|
  | 1 | bd-time-machine | s3:CopyObject (line 139) | **REAL BUG** | boto3 s3.copy_object on opal-data-bd/gold/* versioned objects; iam.tf has GetObjectVersion + PutObject but missing CopyObject |
  | 2 | bd-time-machine | s3:CopyObject (line 184) | **REAL BUG** | Same — second call site, same fix |
  | 3 | historical-prices-scheduler | s3:GetObject | FALSE POSITIVE (comp-iam scope) | `aws s3 cp` in USER_DATA_SCRIPT for ephemeral EC2 spawn; runs on EC2 with bd-exporter-profile, NOT Lambda IAM |
  | 4 | historical-prices-scheduler | s3:PutObject | FALSE POSITIVE | Same as #3 |
  | 5 | historical-prices-scheduler | s3:GetObject (line 58) | FALSE POSITIVE | Same EC2-shipped script |
  | 6 | historical-prices-scheduler | s3:PutObject (line 58) | FALSE POSITIVE | Same |
  | 7 | inf-assets-trigger | s3:GetObject | FALSE POSITIVE | `aws s3 cp` in `_ASSETS_CHAIN_CMD` shipped via ssm.send_command to inf-gold-layer-runner EC2; runs with inf-gold-layer-ec2-role |
  | 8 | inf-assets-trigger | s3:PutObject | FALSE POSITIVE | Same |
  | 9 | opal-news-layer3-curation | s3:GetObject | FALSE POSITIVE (comp-iam scope) | iam.tf attaches AWS-managed `AmazonS3ReadOnlyAccess` policy via `aws_iam_role_policy_attachment`; comp-iam scans inline statements only, doesn't infer managed-policy actions |

  **Net: 1 real bug (counted as 2 due to call-site duplication; same fix), 7 false positives.**

  </gap_classification>

  <scope>
    <step>
      <run>**Real fix #1: bd-time-machine** — patch `infra/aws/terraform/bd-pipeline/iam.tf` `aws_iam_role_policy.bd_time_machine_s3` to add `s3:CopyObject` action on the existing `arn:aws:s3:::opal-data-bd/gold/*` resource scope. Either expand the existing `RestoreAndSentinel` PutObject statement to include CopyObject, or add a new `CopyVersionedRestore` statement.</run>
      <expect>Statement landed; bd-pipeline terraform plan shows in-place IAM policy update; apply 0-diff post.</expect>
    </step>
    <step>
      <run>terraform apply bd-pipeline; verify 0-diff plan; tag `bd-pipeline-v{X.Y.Z}` per CLAUDE.md tag protocol; push --follow-tags.</run>
      <expect>Clean apply; tag pushed.</expect>
    </step>
    <step>
      <run>Re-run `comp-iam gaps` post-apply; verify gap count drops by 2 (the bd-time-machine line 139 + 184 entries should disappear). Remaining 7 gaps are documented false-positives per gap_classification table.</run>
      <expect>9 gaps → 7 gaps (or fewer if comp-iam consolidates duplicates).</expect>
    </step>
    <step>
      <run>**Document false-positives**: append to V4.OPS test matrix doc + standing-backlog observations. The 7 false positives reveal 2 comp-iam improvement opportunities for follow-on TO (.024+):
        (a) Distinguish boto3 calls from shell-shipped commands (aws s3 cp inside USER_DATA_SCRIPT or SSM-send_command body should not flag the Lambda's role).
        (b) Track AWS-managed policy attachments (aws_iam_role_policy_attachment with policy_arn = arn:aws:iam::aws:policy/...) and infer actions covered.</run>
      <expect>Standing-backlog candidates documented for CTO triage (improvement TO authoring).</expect>
    </step>
    <step>
      <run>safe-commit.sh + RAVC2 to CTO + COO with full classification table + before/after gap count.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">bd-time-machine-lambda-role IAM policy adds s3:CopyObject on opal-data-bd/gold/* (real fix landed via terraform apply).</ac>
    <ac id="2">terraform apply 0-diff post; bd-pipeline tag bumped + pushed.</ac>
    <ac id="3">comp-iam gaps post-apply reduces by ≥2 (the bd-time-machine entries cleared).</ac>
    <ac id="4">Remaining 7 false-positives explicitly documented in classification table; not silently dismissed.</ac>
    <ac id="5">comp-iam follow-on improvement candidates surfaced (managed-policy parsing + EC2-shipped-shell distinction) for CTO triage.</ac>
    <ac id="6">No regression on bd-time-machine actual behavior (additive grant, not restriction).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Pre-edit: re-run comp-iam gaps; classify each per code inspection.</phase>
    <phase id="2">Post-apply: re-run comp-iam gaps + comp-iam service bd-time-machine; verify GRANTED.</phase>
    <phase id="3">Append rows to compiler-tools-log.md per usual cadence.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Classification table + terraform plan/apply output + before/after gap count + comp-iam follow-on improvement candidates surfaced</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>comp-iam improvement TOs (managed-policy parsing, EC2-shell distinction) — surface as follow-on candidates only.</item>
    <item>EC2-side IAM audit for the 7 false-positive Lambdas — separate scope (would scope bd-exporter-profile + inf-gold-layer-ec2-role for the actual S3 actions used in shell-shipped commands).</item>
    <item>AmazonS3ReadOnlyAccess audit — managed-policy attachments to ALL roles is a separate audit surface.</item>
  </out_of_scope>
</task_order>
