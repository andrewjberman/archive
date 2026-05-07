<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.01</id>
    <project>ADVI_FIRMSEP</project>
    <title>Declare opal-data-inf as CF origin (TF reflection of runtime origin mutation) — ZERO data-path change</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-07</completed_date>
    <completed_by>0.7.0_AE_CloudOps~B</completed_by>
    <priority>high</priority>
    <estimated_effort>~0.25d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.1 + §6 Phase 1</ref>
    <ref type="cf_distribution_tf">infra/aws/terraform/portal-auth/cloudfront-distribution.tf:107-114 (opal-data-bd origin) + line 7 ("IMPORTED RESOURCE — do not terraform apply without verifying 0-diff first")</ref>
    <ref type="oai">E139998VWH0PD (shared OAI for opal-data-bd; runtime mutation requires same OAI for opal-data-inf)</ref>
    <ref type="risk_register">PRD Appendix C row 1 — origin declaration may trigger spurious replace; mitigate via low-traffic apply window + post-apply CW metric verification</ref>
  </references>

  <context>
    Today opal-data-inf is reached via runtime origin mutation in shared-advisor-router
    (request.origin.s3.domainName swap from opal-data-bd → opal-data-inf at origin-request
    time). Terraform has zero representation of the second tenant.

    Implications: (1) drift detection on the CF distribution doesn't validate the inf-bucket
    origin path; (2) CW per-origin metrics merge Inflection traffic under S3-opal-data-bd;
    (3) the OAI grant on opal-data-inf lives in inf-pipeline TF without cross-reference from
    portal-auth (separate concern — TO-FIRMSEP.02).

    THIS TO is purely declarative. Add an origin {} block for
    opal-data-inf.s3.us-east-1.amazonaws.com to aws_cloudfront_distribution.portal. Same OAI
    (E139998VWH0PD). NO modification to existing origins, behaviors, cache policies, or
    Lambda associations. The runtime origin mutation in shared-advisor-router still does the
    actual origin selection — declarations are for TF reflection + per-origin CW metrics
    + drift-detection coverage.

    Risk: terraform plan may surface a spurious "replace" on the existing distribution due to
    historical console drift (the file is marked IMPORTED RESOURCE). Mitigation: inspect plan
    carefully before apply; abort and escalate if anything beyond the single origin ADD shows.
  </context>

  <scope>
    <step>
      Edit infra/aws/terraform/portal-auth/cloudfront-distribution.tf — add origin block:
        origin {
          domain_name = "opal-data-inf.s3.us-east-1.amazonaws.com"
          origin_id   = "S3-opal-data-inf"
          s3_origin_config { origin_access_identity = "origin-access-identity/cloudfront/E139998VWH0PD" }
        }
      Mirror the structure of the existing opal-data-bd origin block exactly.
    </step>
    <step>
      terraform plan — REQUIRED outcome: 1 ADD (origin block), 0 modifications, 0 replaces.
      If plan shows any modifications to existing origins, behaviors, cache policies, or Lambda
      associations → ABORT, capture full plan output, RAVC1 to COO with anomaly. Do NOT apply.
    </step>
    <step>
      Apply during low-traffic window (off-peak — defer if dispatched mid-day; Andrew can
      authorize same-day if explicit). Capture pre-apply + post-apply 0-diff plan.
    </step>
    <step>
      Post-apply verification:
        a. Portal smoke test — Inflection user login + advisor-intelligence route hit
           (curl with Inflection JWT against /api/scoped/advisor-intelligence/{advisor}/book).
           Expect 200 + correct payload.
        b. CW metrics — within ~1h post-apply, S3-opal-data-inf metric should show non-zero
           Requests + BytesDownloaded. If still merged under S3-opal-data-bd after 1h,
           investigate.
    </step>
    <step>
      record-terraform-deploy.sh portal-auth + tag bump portal-auth-v1.X.Y (check current tag
      via git tag -l "portal-auth-v*" | sort -V | tail -3). Push --follow-tags.
    </step>
    <step>
      RAVC2 to COO: plan output before/after, apply log, smoke test result, CW metric snapshot
      ~1h post-apply, tag bump.
    </step>
  </scope>

  <compiler_mandate>
    <tool>terraform plan attached to RAVC — must show 1 ADD only</tool>
    <tool>comp-routes trace inflection-* (post-apply) — confirm route paths unchanged</tool>
    <tool>comp-routes trace 49financial-* (post-apply) — same, BD side regression check</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">terraform plan shows exactly 1 ADD (origin block); zero modifications.</criterion>
    <criterion id="AC2">terraform apply executes successfully; post-apply plan is 0-diff.</criterion>
    <criterion id="AC3">Portal smoke test green for Inflection AND 49Financial routes post-apply.</criterion>
    <criterion id="AC4">CW per-origin metric for S3-opal-data-inf populates with non-zero traffic count within 1h post-apply.</criterion>
    <criterion id="AC5">portal-auth-v1.X.Y tag bumped + push --follow-tags + record-terraform-deploy.sh ran.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent of Phase 0.</upstream>
    <downstream>TO-FIRMSEP.02 (cross-reference OAI) ships after; both are TF reflection.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. ZERO data-path change. Apply during off-peak window or coordinate same-day approval. RAVC2 with plan + apply + smoke + CW metric.</message>
  </go_signal>
</task_order>
