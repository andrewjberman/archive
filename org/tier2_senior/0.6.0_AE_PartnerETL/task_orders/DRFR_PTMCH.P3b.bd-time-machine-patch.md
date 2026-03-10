```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-10-drfr-ptmch-partneretl-p3b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-10</date>
    <status>complete</status>
    <thread_serial>DRFR_PTMCH-001</thread_serial>
    <thread_ref>org/threads/DRFR_PTMCH-001-portal-time-machine-ae-infrastructure-di/</thread_ref>
  </metadata>

  <objective>
    Patch and redeploy bd-time-machine to fix two bugs found during COO audit of bd-v2.18.0.
    The fixes are already committed at 233da228 -- this task is build + upload + terraform apply
    only. No code changes required.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      CONFIRM BUG FIXES ARE PRESENT:
      Read infra/aws/lambda/bd-pipeline/bd-time-machine/lambda_function.py at commit 233da228.
      Verify both fixes are in the current working copy:
        (a) _restore_from_manifest: has try/except around s3.copy_object() and returns
            tuple[int, list] (restored_count, failed_keys)
        (b) _restore_fallback: has try/except around s3.copy_object() and returns
            tuple[int, list, str] (restored_count, failed_keys, 'fallback')
        (c) Neither function uses MetadataDirective='REPLACE' or CacheControl= in copy_object
        (d) lambda_handler correctly unpacks the new return signatures and includes
            files_failed in the response body
      Do NOT proceed to build if any of these are absent.
    </requirement>

    <requirement id="2">
      BUILD AND UPLOAD bd-time-machine:
      Use the PowerShell PS1 temp file workaround (build-and-upload.sh fails on this machine
      due to bun/MSYS2 /tmp/ path issue -- see AE5 log drfr_ptmch_p2_phase_b_deploy.md for
      the exact workaround pattern).
      Upload to: s3://opal-313476888478-lambda-artifacts/bd-pipeline/bd-time-machine.zip
      Update SHA256 in infra/aws/lambda/ci/lambda-source-map.json.
      Commit the source map update with [skip ci].
    </requirement>

    <requirement id="3">
      TERRAFORM APPLY bd-pipeline:
      Run terraform plan and apply for bd-pipeline.
      Expected: 0 to add, 1 to change (bd-time-machine Lambda code update), 0 to destroy.
      Confirm 0-diff plan after apply.
      Update pipeline_inventory.xml with bd-v2.18.1.
      Run record-terraform-deploy.sh.
      Tag: bd-v2.18.1
      Push with --follow-tags.
    </requirement>

    <requirement id="4">
      MARK TASK ORDERS:
      Mark DRFR_PTMCH.P3 status back to complete (patch resolves the open issue).
      Mark this task order (DRFR_PTMCH.P3b) complete.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      bd-time-machine Lambda in AWS reflects commit 233da228 (verify via
      aws lambda get-function --function-name bd-time-machine --query
      "Configuration.{CodeSha256:CodeSha256,LastModified:LastModified}").
    </criterion>
    <criterion id="2">
      Terraform 0-diff after apply. Tag bd-v2.18.1 pushed.
    </criterion>
    <criterion id="3">
      Quick smoke test: invoke bd-time-machine with a historical date and confirm
      statusCode 200 in the response body and files_failed key present (even if empty).
      A single successful invocation is sufficient -- full acceptance testing follows
      in docs/testing/DRFR_PTMCH_acceptance_test_plan.md.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Code changes are already committed at 233da228. Do NOT modify the Lambda
    source -- this is a deploy-only task.</constraint>
    <constraint>Only bd-time-machine needs rebuilding. bd-capture-output-versions and
    bd-portal-publisher are unchanged and do not need new artifacts.</constraint>
    <constraint>Standard deployment protocol: terraform apply only. No aws lambda
    update-function-code.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="2.0.0_SA_COO" task="audit-commit-233da228" status="complete"
      note="Fixes committed by COO at 233da228. Source is correct in working copy."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">lambda-source-map.json updated with new bd-time-machine SHA256</deliverable>
    <deliverable type="commit">bd-v2.18.1 deployed via terraform apply, tag pushed</deliverable>
  </deliverables>
</task_order>
```
