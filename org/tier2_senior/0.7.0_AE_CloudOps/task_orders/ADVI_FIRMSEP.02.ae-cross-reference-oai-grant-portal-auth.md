<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.02</id>
    <project>ADVI_FIRMSEP</project>
    <title>Cross-reference OAI grant from portal-auth — surface a one-sided OAI change as a TF diff</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-07</completed_date>
    <completed_by>0.7.0_AE_CloudOps~B</completed_by>
    <priority>medium</priority>
    <estimated_effort>~0.25d</estimated_effort>
    <implementation_path>Path B (data.aws_s3_bucket_policy + check{}) per RAVC1 21:00Z + COO default-path-with-time-bound at 21:18Z. Path A (TF import of bucket policies) remains a separate ADHC concern; both bucket policies are CONSOLE-MANAGED with zero TF source ownership pre-FIRMSEP.02 — TO §4 step 1+2's data.terraform_remote_state.{X}.outputs.{X}_bucket_oai_arn approach was structurally impossible.</implementation_path>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.2 + §6 Phase 1</ref>
    <ref type="oq4">PRD §7 OQ4 — TF cross-reference pattern: data "terraform_remote_state" vs consolidated firm-buckets module. Default approved: data "terraform_remote_state" (less restructure, lower blast radius).</ref>
    <ref type="modules">inf-pipeline/iam.tf or s3.tf (OAI grant on opal-data-inf), bd-pipeline (analogous), portal-auth/ (consumer)</ref>
  </references>

  <context>
    OAI grants on opal-data-bd and opal-data-inf both reference E139998VWH0PD but live in their
    respective pipeline modules — invisible to the portal-auth CF distribution module. A
    one-sided change to either bucket policy could silently break CF access without a TF
    plan diff in portal-auth.

    Fix: each pipeline module exposes an output (bucket name + OAI ARN). portal-auth consumes
    via data "terraform_remote_state" + asserts the granted OAI matches the CF distribution's
    expected OAI. A change in either side now triggers a portal-auth plan diff.

    Per OQ4: SAME OAI E139998VWH0PD across all firms (the runtime origin-mutation pattern in
    shared-advisor-router requires consistent OAI auth context). Per-firm OAI is OUT OF
    SCOPE — would require per-firm CF behaviors or router restructure.
  </context>

  <scope>
    <step>
      Audit current OAI grant locations:
        grep -rE "E139998VWH0PD|origin-access-identity" infra/aws/terraform/inf-pipeline/
        grep -rE "E139998VWH0PD|origin-access-identity" infra/aws/terraform/bd-pipeline/
      Confirm both grants exist + reference the same OAI.
    </step>
    <step>
      Add Terraform output to inf-pipeline/outputs.tf (create if absent):
        output "inf_bucket_oai_arn" { value = aws_s3_bucket_policy.inf_oai_grant.id }
        output "inf_bucket_name"   { value = aws_s3_bucket.opal_data_inf.id }
      (Adjust resource names per actual TF.) Same pattern for bd-pipeline outputs (additive —
      may already exist; verify and add if missing).
    </step>
    <step>
      In portal-auth (a new file e.g. firm-bucket-cross-ref.tf or appended to an existing TF):
        data "terraform_remote_state" "inf_pipeline" {
          backend = "s3"
          config  = { bucket = "opal-313476888478-terraform-state", key = "inf-pipeline/tfstate", region = "us-east-1" }
        }
        data "terraform_remote_state" "bd_pipeline" {
          backend = "s3"
          config  = { bucket = "opal-313476888478-terraform-state", key = "bd-pipeline/tfstate", region = "us-east-1" }
        }
        # Assertion via locals + check {} block:
        locals {
          expected_oai_arn = "origin-access-identity/cloudfront/E139998VWH0PD"
        }
        check "inf_oai_matches" {
          assert {
            condition     = data.terraform_remote_state.inf_pipeline.outputs.inf_bucket_oai_arn == local.expected_oai_arn
            error_message = "inf-pipeline OAI ARN drifted from expected"
          }
        }
    </step>
    <step>
      terraform plan in portal-auth — should show data lookups + check resources only;
      no resource ADDs or MODs to existing infra. Capture plan.
    </step>
    <step>
      apply portal-auth — 0-diff post; check assertions pass.
    </step>
    <step>
      Plan in inf-pipeline + bd-pipeline if outputs added — also additive only.
    </step>
    <step>
      Empirical test: temporarily simulate a mismatched OAI in a branch (do NOT push — local
      sed in a test workspace — terraform plan in portal-auth should surface a check failure).
      Revert. Document evidence in RAVC.
    </step>
    <step>
      record-terraform-deploy.sh per pipeline touched + tag bumps. Push --follow-tags.
    </step>
    <step>
      RAVC2 to COO with plan outputs + check assertion evidence + simulated-mismatch test result.
    </step>
  </scope>

  <compiler_mandate>
    <tool>terraform plan ×3 (inf-pipeline, bd-pipeline, portal-auth) — ADD-only</tool>
    <tool>comp-iam service auth-validator-edge — verify scope unchanged post-apply</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">inf-pipeline + bd-pipeline expose bucket name + OAI ARN as TF outputs.</criterion>
    <criterion id="AC2">portal-auth consumes both via data "terraform_remote_state" + check {} assertion blocks.</criterion>
    <criterion id="AC3">All three TF modules apply 0-diff post-change.</criterion>
    <criterion id="AC4">Empirical: simulated OAI mismatch in test workspace surfaces check failure on portal-auth plan (evidence attached to RAVC; revert before commit).</criterion>
    <criterion id="AC5">Tag bumps per pipeline + push --follow-tags + record-terraform-deploy.sh.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>TO-FIRMSEP.01 ships first (origin declaration before cross-reference) — preferred ordering, not strict.</upstream>
    <downstream>None.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Per OQ4 default: data "terraform_remote_state" pattern. Single OAI E139998VWH0PD across all firms (per OQ2 default).</message>
  </go_signal>
</task_order>
