<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.10</id>
    <project>ADVI_FIRMSEP</project>
    <title>Phase 3 — Cottonwood live ship via the FIRMSEP onboarding playbook (3rd partner)</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>gated</status>
    <priority>high (when ungated)</priority>
    <estimated_effort>~1d (per playbook target)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4 + §6 Phase 3.10</ref>
    <ref type="playbook">docs/architecture/ADVI_FIRMSEP_ONBOARDING_PLAYBOOK.md (CTO authors v1; this TO is the first real-test execution)</ref>
    <ref type="defaults_pending_andrew">
      OQ1 default: firm-id slug = "cottonwood", bucket = "opal-data-cot" (3-letter slug pattern matching bd, inf)
      OQ2 default: SAME OAI E139998VWH0PD as opal-data-{bd,inf} (mutation pattern requires consistent OAI)
      OQ3 default: SAME opal/auth/jwt-public-key Secrets Manager (current single-Opal-issued JWT pattern)
    </ref>
    <ref type="ds_dependency">DS pod for ownership_map.json publication (platinum/cottonwood/ownership_map.json)</ref>
  </references>

  <context>
    GATED on:
      1. Andrew confirmation of OQ1+OQ2+OQ3 defaults (forwarded to him 2026-05-07).
      2. Cottonwood credentials + bucket creation (AE 0.7 ops; coordinate with Andrew on
         go-time).
      3. Phase 1 (FIRMSEP.01-05) shipped — playbook + shared-module pattern + CI gate must
         exist before first real-test.

    Once ungated: the playbook turns this into mechanical execution. Time-to-onboard target:
    1 day, 1 PR-batch, 1 verified deploy.

    DS coordination: AE 0.7~B authors the AE TO body; sibling DS TO (drafted under this TO's
    "DS handoff" section, dispatched to DS at the right phase moment) covers ownership_map
    publication.
  </context>

  <scope>
    <step>
      WAIT for ungating signals:
        a. Andrew confirmation OQ1+OQ2+OQ3 (notify COO when received; COO updates this TO).
        b. AE 0.7 ops: opal-data-cot bucket exists in account 313476888478; OAI grant applied.
        c. Phase 1 ships (FIRMSEP.01-05 RAVCs accepted by COO).

      DO NOT begin steps below until all 3 ungating conditions are met.
    </step>
    <step>
      [POST UNGATE] Read docs/architecture/ADVI_FIRMSEP_ONBOARDING_PLAYBOOK.md for the
      canonical sequence. If playbook doesn't exist yet (CTO Phase 1 deliverable): notify
      COO; CTO authors v1 before this TO begins.
    </step>
    <step>
      [POST UNGATE] FIRM_BUCKET_MAP edit:
        Edit infra/aws/lambda-edge/_shared/firm-bucket-map.mjs (post FIRMSEP.03 extraction):
        Add: 'cottonwood': 'opal-data-cot',
        Single edit, single source. (Pre-FIRMSEP.03 fallback: edit BOTH inline maps in
        auth-validator-edge + shared-advisor-router. Surface to COO if Phase 1 not complete.)
    </step>
    <step>
      [POST UNGATE] CF origin declaration (mirror FIRMSEP.01 pattern):
        Add origin block for opal-data-cot to portal-auth/cloudfront-distribution.tf:
        origin {
          domain_name = "opal-data-cot.s3.us-east-1.amazonaws.com"
          origin_id   = "S3-opal-data-cot"
          s3_origin_config {
            origin_access_identity = "origin-access-identity/cloudfront/E139998VWH0PD"
          }
        }
    </step>
    <step>
      [POST UNGATE] OAI cross-reference (mirror FIRMSEP.02 pattern):
        Author cot-pipeline outputs (bucket_name + oai_arn).
        Add data "terraform_remote_state" "cot_pipeline" block in portal-auth.
        Apply assertion (null_resource precondition or output reference).
    </step>
    <step>
      [POST UNGATE] FIRMSEP.04 CI test sentinel flip:
        Per FIRMSEP.04 author's documented mechanism, remove cottonwood from the pendingFirms
        array (or unskip the test). Run test → must PASS now (cottonwood mapping exists in
        FIRM_BUCKET_MAP after step 3).
        If test fails: cottonwood mapping was missed in step 3 — fix before continuing.
    </step>
    <step>
      [POST UNGATE] Lambda@Edge rebuild + publish + version pin:
        bash infra/aws/lambda/ci/build-nodejs-lambda.sh portal-auth auth-validator-edge
        bash infra/aws/lambda/ci/build-nodejs-lambda.sh portal-auth shared-advisor-router
        # Verify zip parity (FIRMSEP.03's _shared/firm-bucket-map.mjs has cottonwood entry).
        # CF distribution re-pin to new Lambda@Edge versions in portal-auth TF.
        # terraform plan: ADD origin block (cot) + ADD data block + Lambda@Edge version pin
        # diffs only. ZERO modifications to existing behaviors / cache policies / advisor-intelligence routes.
        # terraform apply.
    </step>
    <step>
      [POST UNGATE] FIRMSEP.09 alarm bucket-list update:
        Add "opal-data-cot" to the EventBridge rule's bucketName list in shared-infra
        (or wherever FIRMSEP.09 alarm lives). terraform plan + apply. Verify alarm coverage
        extends to cot bucket via aws s3 cp test from non-CF context.
    </step>
    <step>
      [POST UNGATE — DS COORDINATION] Issue sibling TO to DS pod for ownership_map publication:
        TO scope: DS publishes platinum/cottonwood/ownership_map.json with Cottonwood
        advisor → account / household ownership relationships per ADVI_PROFIL.004c spec.
        Schema: mirror platinum/{bd,inf}/ownership_map.json. Publish via inf-portal-publisher
        OR direct S3 cp (sibling to DS~C work for inflection).
        Acceptance for sibling DS TO:
          AC1: ownership_map.json published at s3://opal-data-cot/platinum/cottonwood/ownership_map.json
          AC2: schema matches BD + INF reference (jq diff clean structurally)
          AC3: comp-pii audit clean (pseudonymized identifiers only)
        DS sibling TO ID: ADVI_FIRMSEP.10.DS — author concurrent with this TO ungate.
    </step>
    <step>
      [POST UNGATE] Smoke test:
        a. Cottonwood JWT (test JWT issued via Opal auth flow) → curl /api/scoped/advisor-intelligence/...?firm=cot
           Expected: 200 from S3-opal-data-cot.
        b. 49F JWT requesting cot path → 403 (firm scoping).
        c. Inflection JWT requesting cot path → 403.
        d. Missing X-Firm-Id with cot path → 403.
    </step>
    <step>
      [POST UNGATE] CW per-origin metric:
        Confirm S3-opal-data-cot CW metric populates within 1h post-deploy with non-zero
        traffic count (proves origin declaration is live + receiving CF traffic).
    </step>
    <step>
      [POST UNGATE] Tag bump portal-auth-vX.Y.Z + cot-pipeline-vX.Y.Z. record-terraform-deploy.
    </step>
    <step>
      [POST UNGATE] RAVC to COO: full end-to-end empirical evidence — smoke test responses,
      CW per-origin metric, alarm coverage extension, FIRMSEP.04 cottonwood test flipped to
      PASS, DS ownership_map RAVC, time-to-onboard total (target <1d).
    </step>
    <step>
      [POST RAVC] Playbook v0.2 update: capture any onboarding-step that the playbook
      missed during this first real-test. CTO ratchets v0.2.
    </step>
  </scope>

  <compiler_mandate>
    <tool>FIRMSEP.04 CI test on cottonwood case — must PASS post-step-3</tool>
    <tool>comp-routes trace cottonwood-* — confirm route maps to opal-data-cot</tool>
    <tool>comp-iam service auth-validator-edge / shared-advisor-router — verify scope unchanged</tool>
    <tool>terraform plan portal-auth post-apply 0-diff</tool>
    <tool>aws cloudwatch get-metric-statistics S3-opal-data-cot — non-zero post-deploy</tool>
    <tool>comp-pii audit on platinum/cottonwood/* — DS sibling TO's responsibility</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">cottonwood-firm-id JWT successfully reads opal-data-cot/platinum/firm/header_metrics.json (or equivalent) via portal CF route → 200.</criterion>
    <criterion id="AC2">49F JWT requesting cot path → 403 (firm scoping enforced).</criterion>
    <criterion id="AC3">Inflection JWT requesting cot path → 403.</criterion>
    <criterion id="AC4">CW per-origin metric S3-opal-data-cot populates within 1h with non-zero traffic.</criterion>
    <criterion id="AC5">FIRMSEP.04 cottonwood test flipped from SKIP/pending → PASS.</criterion>
    <criterion id="AC6">FIRMSEP.09 alarm bucket-list extended; coverage verified via empirical bypass test on cot.</criterion>
    <criterion id="AC7">DS sibling TO (ADVI_FIRMSEP.10.DS) RAVCs ownership_map.json publication.</criterion>
    <criterion id="AC8">Tag bumps + record-terraform-deploy.</criterion>
    <criterion id="AC9">Time-to-onboard end-to-end ≤ 1 effort-day (per playbook target).</criterion>
    <criterion id="AC10">Playbook v0.2 ratchet with any missed-step corrections (CTO ownership).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>HARD GATES (all 3): Andrew OQ1+OQ2+OQ3 confirmation, Cottonwood credentials + bucket creation, Phase 1 (FIRMSEP.01-05) shipped + playbook v1 authored.</upstream>
    <downstream>Playbook v0.2 ratchet (CTO). Phase 4 carry-over considerations (per-firm CF distribution evaluation post-Cottonwood empirical).</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GATED. Three hard gates: Andrew OQ-confirm + cot bucket creation + Phase 1 ship. COO ungates explicitly when all 3 met. DS sibling TO authored at ungate moment (do not pre-author). Playbook-driven; report time-to-onboard.</message>
  </go_signal>
</task_order>
