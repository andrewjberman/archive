<task_order>
  <metadata>
    <id>2.0.0_SA_COO~C-2026-05-21-demov1-to1-infra</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~C</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <project_code>ADVI_DEMOV1</project_code>
    <!-- GO issued by 2.0.0_SA_COO~C 2026-05-22: the sole gate (Andrew standing up
         the 0.7.0_AE_CloudOps~C infra lane) is cleared — AE~C registered LIVE on
         the broker. Flipped staged -> pending. -->
  </metadata>

  <objective>
    Phase 1 of ADVI_DEMOV1 — stand up the demo tenant's infrastructure: create the
    `opal-data-demo` S3 bucket via Terraform with the CloudFront OAI bucket policy,
    grant the IAM reads needed by the serving roles, add the `demo` firm entry to
    the edge `FIRM_CONFIG` single-source module, flip the routing CI sentinel, and
    rebuild/redeploy both Lambda@Edge functions. End state: bucket + routing live
    and empty, ready for the Phase-4 transform run to populate it.
  </objective>

  <context>
    ADVI_DEMOV1 PRD: docs/architecture/ADVI_DEMOV1.md (v0.1, committed 2e1321f79).
    Read §3 (serving architecture), §4 (CTO rulings R1-R7), §6 TO-1, §7 risks.

    Project goal: a self-contained demo tenant — clone s3://opal-data-bd/platinum/**
    into opal-data-demo with all PII faked, served to a demo Cognito login.

    SERVING-PATH VERDICT (TO-0 Phase-0 probe, §3.2 linchpin — RESOLVED, evidenced,
    source-cited by DS~C 2026-05-21T16:12Z):
    - Static-platinum routes are served by CloudFront distribution
      `EVTSA9VEHNZVH`, behavior `/api/scoped/advisor-intelligence/*` -> S3 origin,
      via two Lambda@Edge functions:
        * `auth-validator-edge` (viewer-request) — validates the JWT, injects the
          `X-Firm-Id` header. Source: infra/aws/lambda-edge/auth-validator-edge/index.mjs
        * `shared-advisor-router` (origin-request) — reads `X-Firm-Id`, resolves
          the target bucket, mutates `request.origin.s3.domainName` in place
          (runtime origin-mutation; preserves OAI auth). Source:
          infra/aws/lambda-edge/shared-advisor-router/index.mjs
    - Bucket selection (shared-advisor-router/index.mjs lines ~183-205): partner
      `firmId` resolves via `FIRM_BUCKET_MAP`; that map is the single-source
      module `infra/aws/lambda-edge/_shared/firm-config.mjs` (`FIRM_CONFIG`),
      consumed by BOTH edge functions. Today: 49financial->opal-data-bd,
      inflection->opal-data-inf, mockadv->opal-data-bd. `mockadv` is an existing
      test-account firm — direct precedent for a non-real firm entry.
    - The routing was purpose-built for firm onboarding (project ADVI_FIRMSEP).
      The documented path is the ADVI_FIRMSEP_ONBOARDING_PLAYBOOK; FIRMSEP.10
      (Cottonwood onboarding) is the working template — follow it.
    - DUAL SERVING PATH: shared-advisor-router v9 BLOCKS
      platinum/{advisors,clients}/{id}/summary.json from S3-direct (returns 401) —
      those route through the `opal-partners-data` Lambda for pseudonymization. So
      the demo needs BOTH the edge `FIRM_CONFIG` entry (static platinum/*) AND a
      DynamoDB `FIRM#demo` record (dynamic Lambda path). The DynamoDB record is
      TO-3's scope, not yours — but be aware the edge entry alone is not the whole
      serving story.

    GATING — this TO is staged. It does NOT get a GO until:
      (a) Andrew stands up the `~C` AE infra lane (COO~C flags this to CTO +
          Andrew alongside the §3.2 verdict). This is the SOLE remaining gate.

    CTO ruling R3 — STATUS: RESTATED + CONFIRMED by CTO 2026-05-21. R3 as
    originally worded ("declared CF origin; runtime origin-mutation = debt") was
    built on a half-understanding of the ADVI_FIRMSEP finding. The §3.2 verdict
    (source-cited) proved runtime origin-mutation via the shared firm-config map
    IS the designed universal partner-routing mechanism (49F/INF/mockadv all
    route this way), purpose-built by FIRMSEP — not debt. CTO confirmed the
    restatement. R3's binding intent, now concrete:
      1. opal-data-demo bucket + its bucket POLICY (the OAI grant — principal
         E139998VWH0PD + EVTSA9VEHNZVH SourceArn, per-bucket, NO wildcard) are
         Terraform-managed. The bucket policy is the non-skippable part.
      2. The FIRM_CONFIG `demo -> opal-data-demo` entry + the firm-routing.spec.mjs
         CI sentinel flip land in the SAME commit, version-controlled.
      3. Both edge fns rebuild/redeploy via the standard Lambda@Edge cycle (the
         ADVI_FIRMSEP_ONBOARDING_PLAYBOOK; FIRMSEP.10 Cottonwood is the template).
    Nothing is created out-of-band; everything is in the TF graph or version
    control. R3 is settled — no further wording question.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing iam.tf / Terraform:
      <run>comp-iam service shared-advisor-router</run>
      <expect>Current IAM grants for the edge router role; identify what (if
      anything) an opal-data-demo read grant must add. Note: edge S3 reads are
      OAI-mediated via the bucket policy, not necessarily the role — confirm
      which mechanism applies.</expect>
      <if_mismatch>If the edge role is not resolved by comp-iam, inspect the role
      + the existing opal-data-bd / opal-data-inf bucket policies directly
      (firm-bucket-cross-ref.tf) and mirror the pattern.</if_mismatch>

      <run>comp-iam service opal-partners-data</run>
      <expect>Current IAM grants for the partners Lambda role; opal-data-demo
      needs the same s3:GetObject/ListBucket pattern the role holds for
      opal-data-bd / opal-data-inf.</expect>
      <if_mismatch>Surface any gap before writing iam.tf — fix it in the same
      change.</if_mismatch>

    Phase 2 — before commit (after iam.tf + Terraform + firm-config changes):
      <run>comp-iam gaps</run>
      <expect>No new permission gaps — every S3 op against opal-data-demo is
      covered by a Terraform policy statement or the bucket-policy OAI grant.</expect>
      <if_mismatch>Fix iam.tf before deploy — a missing grant surfaces as a
      runtime 403/AccessDenied (the F2 yield-curve incident pattern).</if_mismatch>

      <run>comp-routes behaviors</run>
      <expect>The CloudFront behavior table for EVTSA9VEHNZVH is intact; the
      advisor-intelligence behavior + its two edge functions are unchanged.</expect>
      <if_mismatch>The routing change is in FIRM_CONFIG, not the CF behavior — if
      the behavior table shows unexpected drift, stop and flag to COO~C.</if_mismatch>

    Phase 3 — after deploy (terraform apply 0-diff + both edge fns redeployed):
      <run>comp-routes trace getPlatinumFirmDashboard</run>
      <expect>For a `?firm=demo` / X-Firm-Id=demo request the path resolves
      CF EVTSA9VEHNZVH -> shared-advisor-router -> origin opal-data-demo. Bucket
      empty at this stage — the routing path is what is verified.</expect>
      <if_mismatch>If the path does not resolve to opal-data-demo, the
      FIRM_CONFIG entry, the edge redeploy, or the bucket policy is wrong — fix
      before signaling complete.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: infra/aws/lambda-edge/_shared/firm-config.mjs (FIRM_CONFIG)
      — the single-source firm map consumed by BOTH edge functions
      (auth-validator-edge + shared-advisor-router). Editing it touches the
      routing of 49F + INF + mockadv.
    - shared_resource: both Lambda@Edge functions (auth-validator-edge,
      shared-advisor-router) — both must be rebuilt/redeployed because both
      import firm-config.mjs.
    - shared_resource: the CI sentinel shared-advisor-router/test/firm-routing.spec.mjs.
    - also_in_to: none currently active. Any concurrent Inflection/49F edge or
      onboarding TO is a hard collision.
    - required_action: before committing the FIRM_CONFIG `demo` entry, re-confirm
      via get_live_agents / broker that no other agent is editing the edge
      functions or firm-config.mjs; pull latest. The `demo` entry is purely
      additive — it must NOT alter the 49financial / inflection / mockadv entries.
      Verify existing firm routes still resolve in the Phase-3 trace.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `opal-data-demo` S3 bucket created via Terraform (new `demo` module OR
       under shared-infra — AE's call, documented), with versioning + encryption +
       public-access-block consistent with opal-data-bd. NOT created via the AWS
       console or `aws s3 mb`.
    2. The opal-data-demo BUCKET POLICY grants the CloudFront OAI principal
       `E139998VWH0PD` + the `EVTSA9VEHNZVH` distribution SourceArn, per-bucket
       (no wildcard) — mirroring the firm-bucket-cross-ref.tf pattern for
       opal-data-bd / opal-data-inf. This is a HARD requirement: without it every
       demo static fetch 403s.
    3. iam.tf: the `opal-partners-data` role holds s3:GetObject + s3:ListBucket on
       opal-data-demo (the dynamic path). `comp-iam gaps` shows no new gap.
    4. The `demo` firm entry is added to infra/aws/lambda-edge/_shared/firm-config.mjs
       (`FIRM_CONFIG`): `demo -> { bucket: 'opal-data-demo', ... }` following the
       mockadv / FIRMSEP.10 Cottonwood template. The 49financial / inflection /
       mockadv entries are unchanged.
    5. The routing CI sentinel shared-advisor-router/test/firm-routing.spec.mjs is
       updated to cover the `demo` firm IN THE SAME COMMIT as the firm-config
       change, and the sentinel passes.
    6. BOTH Lambda@Edge functions (auth-validator-edge + shared-advisor-router)
       are rebuilt and redeployed (both import firm-config.mjs). Deployed via the
       standard Lambda@Edge deploy cycle.
    7. `terraform apply` reaches a verified 0-diff replan; recorded via
       record-terraform-deploy.sh; pipeline git-tagged per CLAUDE.md Rule 6.
       lambda-source-map.json updated for the edge source changes (Rule 4).
    8. Phase-3 `comp-routes trace` confirms an X-Firm-Id=demo platinum request
       resolves CF -> shared-advisor-router -> opal-data-demo (bucket empty OK).
    9. Existing 49F (opal-data-bd), Inflection (opal-data-inf), and mockadv
       routes still resolve correctly — additive change, zero regression.
    10. Session log with Compiler Tools section committed.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create | modify">infra/aws/terraform/** — opal-data-demo bucket + bucket policy (OAI grant) + iam.tf grants (exact module path is AE's call per criterion 1)</file>
      <file action="modify">infra/aws/lambda-edge/_shared/firm-config.mjs — additive `demo` FIRM_CONFIG entry</file>
      <file action="modify">infra/aws/lambda-edge/shared-advisor-router/test/firm-routing.spec.mjs — CI sentinel covering `demo`</file>
      <file action="modify">infra/aws/lambda-edge/auth-validator-edge/ + infra/aws/lambda-edge/shared-advisor-router/ — rebuild/redeploy artifacts</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json — edge source changes (Rule 4)</file>
      <file action="reference">docs/architecture/ADVI_DEMOV1.md; the ADVI_FIRMSEP_ONBOARDING_PLAYBOOK; the FIRMSEP.10 Cottonwood onboarding TO/commits</file>
      <file action="reference">the TO-0 probe brief (docs/briefs/advi-demov1-phase0-...)</file>
      <file action="reference">firm-bucket-cross-ref.tf (the OAI bucket-policy pattern)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Create opal-data-demo strictly via Terraform — CLAUDE.md
    Rule 1. Commit before apply (Rule 2); 0-diff replan; tag after deploy (Rule 6).</requirement>
    <requirement id="2">The OAI bucket policy (criterion 2) is mandatory and must
    land with the bucket — it is the documented requirement for any new partner
    bucket; omitting it 403s every demo static fetch.</requirement>
    <requirement id="3">Follow the ADVI_FIRMSEP onboarding playbook — the
    FIRM_CONFIG entry + CI sentinel flip in one commit + both edge fns redeployed.
    Use FIRMSEP.10 Cottonwood as the working template.</requirement>
    <requirement id="4">The FIRM_CONFIG `demo` entry is purely additive — zero
    change to 49financial / inflection / mockadv routing.</requirement>
    <requirement id="5">IAM least-privilege: opal-data-demo read grants only.
    No write grants to serving roles — the transform run (TO-4) gets its own
    scoped EC2 role.</requirement>
    <requirement id="6">Zero regression — verify existing firm routes in the
    Phase-3 comp-routes trace.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Terraform (bucket + OAI policy + iam.tf) + firm-config.mjs + CI sentinel, committed to CLOUD, pushed --follow-tags after a 0-diff apply</deliverable>
    <deliverable type="commit">Both Lambda@Edge functions rebuilt + redeployed; lambda-source-map.json updated</deliverable>
    <deliverable type="document">record-terraform-deploy.sh CHANGELOG entry + pipeline git tag</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT create opal-data-demo via the AWS console or `aws s3 mb` —
    Terraform only (Rule 1).</rule>
    <rule>Do NOT omit the OAI bucket policy — it is a hard requirement, not a
    follow-up; the bucket and its policy land together.</rule>
    <rule>Do NOT modify the 49financial / inflection / mockadv FIRM_CONFIG
    entries — the `demo` entry is additive only.</rule>
    <rule>Do NOT redeploy only one edge function — both import firm-config.mjs;
    both must be rebuilt/redeployed or the routing is half-applied.</rule>
    <rule>Do NOT grant write/PutObject on opal-data-demo to the serving roles.</rule>
    <rule>Do NOT begin before Andrew has stood up the ~C AE lane and COO~C
    issues the GO. This TO is staged. (R3 is settled — CTO-confirmed 2026-05-21.)</rule>
  </do_not>
</task_order>
