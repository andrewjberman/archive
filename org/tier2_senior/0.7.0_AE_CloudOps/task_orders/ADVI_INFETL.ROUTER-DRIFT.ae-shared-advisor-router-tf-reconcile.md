<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.ROUTER-DRIFT</id>
    <project>ADVI_INFETL</project>
    <title>shared-advisor-router Lambda@Edge — recover deployed source, reconcile to local + Terraform, CloudTrail audit drift</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>folded</status>
    <completed_date>2026-05-11</completed_date>
    <completed_note>Absorbed into FIRMSEP.05 cleanup per COO REGISTRY 2026-05-11. Not a standalone deliverable.</completed_note>
    <priority>high</priority>
    <estimated_effort>~0.25-0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="finding">RD INFETL.007 audit (df0b18942) — Risk R3: shared-advisor-router LOCAL is STALE. Deployed Lambda@Edge has ?firm= origin-routing logic not in local index.mjs.</ref>
    <ref type="andrew_directive">2026-05-07 — "we need to fix that drift issue, definitely want to keep everything organized in tf"</ref>
    <ref type="claude_md_rule_1">CLAUDE.md rule 1 — "Terraform is the only Lambda deployment mechanism. Never use aws lambda update-function-code, deploy.sh, or the AWS console to deploy code. All Lambda code is deployed via terraform apply."</ref>
    <ref type="target_lambda">infra/aws/lambda/edge/shared-advisor-router/index.mjs (local)</ref>
    <ref type="target_terraform">infra/aws/terraform/<pipeline>/ — find the resource that defines aws_lambda_function for shared-advisor-router</ref>
  </references>

  <context>
    Lambda@Edge `shared-advisor-router` has out-of-band code in production. Deployed
    version has ?firm= origin-routing logic that does not appear in local source.
    This violates CLAUDE.md rule 1 (Terraform-only deploy) and means any local-side
    change would silently revert the deployed routing logic.

    Andrew direct 2026-05-07: "we need to fix that drift issue, definitely want to
    keep everything organized in tf."

    Plan: recover deployed source as the source-of-truth (since it has the working
    routing logic), diff vs local, commit the reconciled version to local + Terraform,
    re-apply to confirm 0-diff. CloudTrail audit identifies who/when the drift was
    introduced so we can prevent recurrence.
  </context>

  <scope>
    <step>
      Pull deployed source. Lambda@Edge requires us-east-1 region:
        aws lambda get-function --function-name shared-advisor-router --region us-east-1 \
          --query 'Code.Location' --output text
        # Returns a presigned S3 URL — download the zip, extract.
      OR fetch via Lambda console export. Capture deployed-source-of-truth.
    </step>
    <step>
      Diff deployed vs local:
        diff -u infra/aws/lambda/edge/shared-advisor-router/index.mjs deployed/index.mjs
      Capture full diff. Document the ?firm= routing logic (or any other deltas).
    </step>
    <step>
      RECONCILE direction = deployed → local. Treat deployed as canonical because it
      has the live routing behavior portal users depend on.

      Update local index.mjs to match deployed. Preserve any local-only changes only
      if they're forward-fixes that haven't been deployed yet (rare; verify with COO
      before keeping any local-only logic).
    </step>
    <step>
      Verify Terraform manages the deployment cleanly:
        - Confirm aws_lambda_function resource exists for shared-advisor-router in
          infra/aws/terraform/<pipeline>/
        - Confirm filename / source_code_hash references local source via build-and-upload.sh
          (per S3-backed Lambda pattern, post-yang-v2.0.0 migration)
        - If any source_code reference points to a stale S3 zip or in-line archive that
          doesn't match local: fix it
        - Lambda layer references (if any) should be canonical
    </step>
    <step>
      Build + upload via canonical pattern:
        bash infra/aws/lambda/build-and-upload.sh shared-advisor-router
        (or equivalent — follow the canonical pattern used by other Lambdas in the same pipeline)
      Verify S3 zip hash matches local source hash.
    </step>
    <step>
      Pre-commit gate (if applicable for .mjs):
        bash -n / node --check on the JS file
      Then commit via .tools/safe-commit.sh:
        --author "0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;"
        -m "fix(ADVI_INFETL.ROUTER-DRIFT): reconcile shared-advisor-router local to deployed (recover ?firm= routing). Restore TF as source-of-truth per CLAUDE.md rule 1."
        -- infra/aws/lambda/edge/shared-advisor-router/index.mjs
        [+ any TF files modified]
    </step>
    <step>git push origin CLOUD.</step>
    <step>
      terraform plan in pipeline directory:
        - Expected diff: only the source_code_hash / s3_object update (since we're now uploading the deployed-equivalent local version)
        - If no diff: Terraform was already pointing to a current zip and the deployed-but-out-of-band version was identical. Investigate further.
        - If non-trivial diff: review carefully before apply.
    </step>
    <step>terraform apply (verify 0-diff post).</step>
    <step>
      Empirical: invoke shared-advisor-router with a sample request including ?firm=inflection
      (or whatever the routing param is). Verify routing works as expected post-deploy.
    </step>
    <step>
      CloudTrail audit:
        aws cloudtrail lookup-events \
          --lookup-attributes AttributeKey=ResourceName,AttributeValue=shared-advisor-router \
          --region us-east-1 \
          --start-time YYYY-MM-DDTHH:MM:SSZ \
          --max-results 50
      Identify UpdateFunctionCode events outside the Terraform deploy account.
      Document the actor + timestamp + scope of change. Output to RAVC.
    </step>
    <step>
      Tag bump (if pipeline tag pattern applies): {pipeline}-v{X.Y.Z}.
      record-terraform-deploy.sh.
    </step>
    <step>
      RAVC to COO: deployed-vs-local diff summary + reconciled commit hash + Terraform
      0-diff confirmation + CloudTrail audit findings + empirical invoke proof + new
      tag.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-pipescript deployed shared-advisor-router — required MATCH post-reconcile</tool>
    <tool>comp-routes trace shared-advisor-router — confirm full path including ?firm= origin-routing logic preserved</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Deployed source recovered + diff captured + documented in RAVC.</criterion>
    <criterion id="AC2">Local index.mjs reconciled to match deployed (with any local-only forward-fix preserved + flagged).</criterion>
    <criterion id="AC3">Terraform manages the deployment cleanly via build-and-upload.sh + s3_object pattern (no inline archive_file or stale references).</criterion>
    <criterion id="AC4">terraform apply: 0-diff post-apply.</criterion>
    <criterion id="AC5">comp-pipescript deployed MATCH.</criterion>
    <criterion id="AC6">Empirical invoke proves ?firm= routing still works.</criterion>
    <criterion id="AC7">CloudTrail audit identifies actor + timestamp of drift introduction.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent fix.</upstream>
    <downstream>TO-8 (gold→platinum read-path migration) tranches that touch shared-advisor-router are gated on this TO completing per RD R3 finding.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:35Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Andrew direct: "fix that drift issue, definitely want to keep everything organized in tf." Priority HIGH; should ship before any further router-touching TO-8 tranches.</message>
  </go_signal>
</task_order>
