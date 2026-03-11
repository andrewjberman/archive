```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-apiscp-007-ae-dynamo-cf</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>ADVI_APISCP-007</thread_serial>
  </metadata>

  <objective>
    Two-part task. (A) Run the DynamoDB patch script to set firmId='opal-capital' on all
    Opal employee records in opal-users-v2. This unblocks Opal users from the 403 caused
    by firmId='null' being routed to opal-data-null. (B) Add the 'firm' query string
    parameter to the CloudFront cache key for /api/scoped/advisor-intelligence/* so that
    Opal users switching between partner firms get isolated cache entries.
  </objective>

  <scope>
    <files>
      <file action="run">infra/aws/auth/migration/004_patch_opal_firmid.py</file>
      <file action="modify">infra/aws/terraform/{cf-owner-pipeline}/... (wherever CF behavior is managed)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      PART A — DynamoDB patch (must run FIRST).

      The patch script is at: infra/aws/auth/migration/004_patch_opal_firmid.py

      Follow EC2 Code Deployment Standard:
        1. Upload script to S3 artifact bucket: opal-313476888478-lambda-artifacts/migrations/004_patch_opal_firmid.py
        2. Run via SSM on the appropriate EC2 instance (or run directly from local if
           the machine has DynamoDB access with AWS_EC2_METADATA_DISABLED=true set).
        3. Dry run first: python3 004_patch_opal_firmid.py --dry-run
        4. Verify output looks correct (all @opalinvest.com emails listed).
        5. Execute: python3 004_patch_opal_firmid.py
        6. Confirm VERIFICATION section passes: "OK: All N Opal employees have firmId='opal-capital'"
    </requirement>
    <requirement id="2">
      PART A — Session token note. Existing Opal user JWTs were signed with the OLD
      firmId value. The JWT is valid for 15 minutes (access) or 7 days (refresh).
      After the patch, Opal users must re-login or wait for token expiry. The /auth/refresh
      endpoint generates a new access token from the refresh token — which re-reads
      DynamoDB — so hitting /auth/refresh will pick up the new firmId immediately.
      Document this in your session log. No additional action required from AE.
    </requirement>
    <requirement id="3">
      PART B — CloudFront cache key update.

      PREFLIGHT: Determine which Terraform pipeline manages distribution EVTSA9VEHNZVH
      and the cache policy for /api/scoped/advisor-intelligence/*. Run:
        aws cloudfront get-distribution-config --id EVTSA9VEHNZVH
      Identify the CachePolicyId for that path pattern.

      Add query string parameter 'firm' to the cache key for /api/scoped/advisor-intelligence/*.
      The cache key after this change includes both:
        - Headers: X-Firm-Id (partner users set this; Opal users have 'opal-capital')
        - Query strings: 'firm' (Opal users send ?firm=bd; partner users send nothing)
      This prevents two Opal users selecting different partner firms from sharing a cache entry.
    </requirement>
    <requirement id="4">
      PART B — After Terraform apply reaches 0-diff, issue CloudFront cache invalidation:
        /api/scoped/advisor-intelligence/*
      Confirm invalidation reaches Completed status.
    </requirement>
    <requirement id="5">
      After both parts complete, update pipeline_inventory.xml, commit, tag, push.
      Deliver a handoff note to 0.4.0_DT_ClientPlatform: DynamoDB patched, CF cache key
      updated, Opal users can be tested.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Patch script verification section output: "OK: All N Opal employees have firmId='opal-capital'"
      with N greater than 0 (confirms at least one record was found and patched).
    </criterion>
    <criterion id="2">
      aws dynamodb get-item on any known Opal employee PK returns firmId='opal-capital'.
      passwordHash field is present and unchanged (spot-check one record).
    </criterion>
    <criterion id="3">
      aws cloudfront get-distribution-config --id EVTSA9VEHNZVH shows 'firm' in the
      query string allowlist for the /api/scoped/advisor-intelligence/* cache policy.
    </criterion>
    <criterion id="4">
      Terraform plan shows 0 changes after apply (0-diff confirmed).
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      DynamoDB UpdateItem is safe — only firmId is touched. Do NOT use put_item or
      batch_write_item (those would overwrite the entire record). The script uses
      update_item with SET firmId = :fid. Verify this before running.
    </constraint>
    <constraint>
      Run --dry-run FIRST. Confirm all @opalinvest.com emails appear in the output.
      If any unexpected emails appear or the count seems wrong, stop and escalate.
    </constraint>
    <constraint>
      Terraform is the only mechanism for CloudFront changes. Do NOT use the AWS console
      or aws CLI to modify the distribution directly.
    </constraint>
    <constraint>
      Do NOT alter the X-Firm-Id header cache key inclusion — it must remain. Only ADD
      the 'firm' query string parameter to the existing cache policy.
    </constraint>
  </constraints>

  <dependencies>
    <!-- No blocking dependencies. Begin immediately. -->
  </dependencies>

  <deliverables>
    <deliverable type="commit">
      Terraform config updated for CF cache key. 0-diff plan confirmed.
      Invalidation complete. pipeline_inventory.xml updated. Tagged and pushed.
    </deliverable>
    <deliverable type="document">
      Session log confirming: (a) DynamoDB patch ran + verified, (b) CF cache key
      updated + 0-diff + invalidated. Handoff note to DT in their task_orders/.
    </deliverable>
  </deliverables>
</task_order>
```
