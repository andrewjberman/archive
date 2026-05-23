<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-22-demov1-to5-iam-ec2-grant</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~C</issued_to>
    <date>2026-05-22</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_DEMOV1</project_code>
    <priority>P1 -- TO-4 transform run + R5 PII-leak scan (the closure gate for ADVI_DEMOV1) is gated on this grant. DS~C cannot execute --apply without it.</priority>
    <sla>~1d wall (IAM TF write + apply + smoke + verify + EC2_MANIFEST entry).</sla>
    <!-- GO ON AUTHOR by 2.0.0_SA_COO base 2026-05-22T23:30Z. Spawned per MSTR LD-0008
         (commit 743133a4a) to unblock the DS~C ADVI_DEMOV1.004 --apply chain. -->
    <!-- CLOSURE 2026-05-23T07:40Z (2.0.0_SA_COO base): RAVC2-ACCEPTED. All 9 ACs MET per AE~C RAVC2 + COO independent verification. DEPLOY CHAIN: 206cd4483 (IAM role + EC2 source) -> 611926658 (EC2_MANIFEST entry) -> 5e32c0f1d (source_path) -> f17ee0fb2 (record-deploy + shared-infra-v1.17.0 tag). Role ARN: arn:aws:iam::313476888478:role/demo-transform-runner-ec2-role. Instance: i-03343a6072834f77d (t3.large, AL2023, running, SSM Online). Smoke verify (SSM cmd d128878f) 4/4 PASS including 2 negative-test ACL checks (DELETE on demo bucket = AccessDenied; WRITE on opal-data-bd = AccessDenied). DS~C unblocked + MCP'd by AE~C this turn. 3 findings in AE~C session log: CVO P1 timing-claim bug (-3h 53m UTC/EST conversion error in their audit); pre-existing comp-iam gaps on mdpf-daily-trigger-lambda-role (separate AE PartnerETL lane); TO-delivery-discoverability gap (codified by CTO 041a3d366 as Author+GO pairing rule). MSTR LD-0008 SPAWN -> COO TO -> AE~C EXECUTE chain delivered end-to-end. -->

  </metadata>

  <references>
    <prd>docs/architecture/ADVI_DEMOV1.md (v0.1.3)</prd>
    <project_json>org/projects/ADVI_DEMOV1.json</project_json>
    <predecessor_to>org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADVI_DEMOV1.001.aec-infra-demo-bucket-and-routing.md (COMPLETE -- shared-infra-v1.16.0 + portal-auth-v1.16.0)</predecessor_to>
    <downstream_consumer_to>org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_DEMOV1.004.dsc-run-and-verify-pii-leak-scan.md (PENDING; --apply gates on this grant)</downstream_consumer_to>
    <claude_md_rules>CLAUDE.md Rules 7-12 (EC2 deployment + S3 artifact model + EC2_MANIFEST.json)</claude_md_rules>
    <protocols>docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md (S3 artifact model -- code never written on VM, never inline in SSM)</protocols>
  </references>

  <objective>
    Stand up the scoped IAM role + EC2 access that the DS~C ADVI_DEMOV1.004 EC2 one-shot transform requires to populate opal-data-demo/platinum/** from opal-data-bd/platinum/**. End-state: a least-privilege IAM role + instance profile, EC2 service registered in EC2_MANIFEST.json, transform script deployable via safe-ec2-deploy.sh, smoke-test write to opal-data-demo verified, DS~C unblocked to proceed with --apply.
  </objective>

  <context>
    ADVI_DEMOV1 TO-1 (commit `0b12664d1` + shared-infra-v1.16.0 + portal-auth-v1.16.0) created the opal-data-demo S3 bucket + CloudFront-OAI policy (serving-side; read-only). It did NOT grant any write principal on the bucket -- that was deliberate: the only writer is the demo-population transform job, which runs once + then the demo dataset is static.

    DS~C's TO-4 transform engine (commit `2ea34ba81` + register_demo_tenant.py) reads opal-data-bd/platinum/** (the source 49F book) and writes the pseudonymized clone to opal-data-demo/platinum/**. The transform's runtime needs:
    1. A scoped IAM role with READ on opal-data-bd/platinum/** + WRITE on opal-data-demo/platinum/**.
    2. An EC2 instance + instance profile to assume that role (OR an existing EC2 service registered for this purpose -- check the manifest first; do not create a new instance if an existing demo-class service can carry this with a manifest extension).
    3. The transform script deployed via safe-ec2-deploy.sh (S3 artifact model; CLAUDE.md Rules 7, 10, 12).
    4. EC2_MANIFEST.json registration for the new (or extended) service.

    HARD CONSTRAINT: this is a ONE-SHOT, not a daily pipeline. The transform runs once to seed the demo bucket, then DS~C executes the R5 PII-leak scan, then the demo dataset is static. The IAM grant should be auditable + minimal -- no broad opal-data-* wildcards, no s3:DeleteObject, no role-assumption to other roles.
  </context>

  <scope>
    <in_scope>
      DELIVERABLE A -- IAM TF authoring + apply.
        - Add a scoped IAM role + instance profile (or extend an existing demo-class role if one exists) under the appropriate infra/aws/terraform/ pipeline (likely `shared-infra` since opal-data-demo is shared-infra-managed; verify the project boundary before writing).
        - Policy attached: READ-only on opal-data-bd/platinum/** (s3:GetObject + s3:ListBucket scoped to the platinum/ prefix) + WRITE on opal-data-demo/platinum/** (s3:PutObject + s3:ListBucket + s3:GetObject [for transform-state reads]; NO s3:DeleteObject).
        - NO IAM admin grants. NO STS:AssumeRole to other roles. NO broad opal-data-* wildcards (use the explicit bucket ARNs).
        - Terraform 0-diff verified post-apply.
        - shared-infra (or alternate pipeline) tag bumped + record-terraform-deploy.sh + CHANGELOG.json entry per CLAUDE.md Rule 6.

      DELIVERABLE B -- EC2 service registration.
        - Decide between (a) reusing an existing EC2 service (preferred; lower blast radius) by extending its IAM role + manifest entry, OR (b) standing up a new instance for the demo transform. Document the decision in the session log.
        - If (a): extend the role + add a manifest sub-entry naming the demo-transform script path.
        - If (b): register new service in EC2_MANIFEST.json with the IAM role, instance ID, instance profile, S3 deploy path, and the transform script path.

      DELIVERABLE C -- Transform script deployable via safe-ec2-deploy.sh.
        - Confirm DS~C's transform script path (likely under `data/orion/scripts/` or `infra/aws/ec2/{service}/`; coordinate with DS~C if ambiguous).
        - Verify safe-ec2-deploy.sh recognizes the service via EC2_MANIFEST.json -- do a deploy-dry-run.

      DELIVERABLE D -- Smoke verify.
        - From the EC2 service running the new role, write a 1-byte dummy artifact to `opal-data-demo/platinum/_smoke_test/heartbeat_$(date).txt` + `aws s3 ls` confirm + immediately clean up the dummy.
        - Also smoke-read 1 artifact from opal-data-bd/platinum/** to confirm the READ grant works.
        - Both smokes run from the EC2 service's perspective (via SSM invocation if needed), NOT from a local CLI session.

      DELIVERABLE E -- RAVC2 to COO with evidence.
        - Commit hashes, tag, terraform 0-diff, EC2_MANIFEST diff, smoke output, role ARN.
        - Hand-off signal to DS~C: "grant live, manifest registered, script deployable, smoke PASS -- you may proceed with --apply."
    </in_scope>
    <out_of_scope>
      - The transform code itself (DS~C lane; already authored).
      - The R5 PII-leak scan (DS~C lane; runs after the transform completes).
      - Any production-pipeline IAM (this is a one-shot demo-transform grant, not a daily-job grant).
      - Adding write-roles to opal-data-bd (the source is read-only; do NOT extend writes back to the source).
      - Cleanup-after-transform IAM (the demo dataset stays static; nothing to clean).
    </out_of_scope>
  </scope>

  <cross_domain_coordination>
    Lead: 0.7.0_AE_CloudOps~C (IAM + EC2 + Terraform + safe-ec2-deploy.sh).
    Downstream consumer: 0.4.0_DS_ClientPlatform~C (executes --apply on the EC2 service once the grant is live + smoke-passes).
    MCP DS~C with the role ARN + manifest entry + smoke-pass signal as the RAVC2 hand-off; DS~C re-runs check_inbox to pick up.
    NO INFGRO coordination needed (different lane).
    NO portal coordination needed (serving-side already shipped under TO-1).
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam service {{the_service_name}}</run>
        <expect>If reusing an existing service: zero MISSING permissions vs the target operations (GetObject on opal-data-bd/platinum/**, PutObject on opal-data-demo/platinum/**). If new service: comp-iam returns "service unknown" -- proceed to author.</expect>
        <if_mismatch>STOP. If MISSING permissions surface on a reuse path, the policy attachment is incorrect -- fix iam.tf before deploying.</if_mismatch>
      </step>
      <step>
        <run>aws s3api get-bucket-policy --bucket opal-data-demo</run>
        <expect>Returns the TO-1-installed CloudFront-OAI policy (AllowCloudFrontOACReadPlatinum + AllowScopedAdvisorOAI). Confirms no conflicting write-deny statement exists.</expect>
        <if_mismatch>STOP. If a write-deny statement exists on the bucket policy, surface to COO -- the IAM grant + bucket policy must be reconciled before WRITE permissions are usable.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-iam gaps</run>
        <expect>Exit 0. No new IAM gaps introduced.</expect>
        <if_mismatch>STOP. Do not commit if comp-iam gaps fails.</if_mismatch>
      </step>
      <step>
        <run>terraform plan (post-apply)</run>
        <expect>0-diff -- "No changes. Your infrastructure matches the configuration."</expect>
        <if_mismatch>STOP. Drift detected -- diagnose before tagging or committing record-deploy.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>aws s3 cp /tmp/heartbeat.txt s3://opal-data-demo/platinum/_smoke_test/heartbeat_$(date +%Y%m%d_%H%M%S).txt (from EC2 service via SSM)</run>
        <expect>Exit 0; aws s3 ls confirms object EXISTS; then immediately aws s3 rm to clean.</expect>
        <if_mismatch>STOP. IAM grant doesn't permit the write -- diagnose role/policy/bucket-policy.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-bd/platinum/{one-known-file}.json /tmp/source_smoke.json (from EC2 service via SSM)</run>
        <expect>Exit 0; file pulled. Confirms READ grant works.</expect>
        <if_mismatch>STOP. IAM grant doesn't permit the source read -- diagnose.</if_mismatch>
      </step>
      <step>
        <run>comp-blast (the new role / IAM resource)</run>
        <expect>No unexpected downstream consumers -- the grant is scoped to the demo-transform service alone.</expect>
        <if_mismatch>Surface to COO. Likely indicates another agent extended the role mid-flight.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <ac id="AC1">Scoped IAM role + instance profile live with explicit ARN; policy text grants ONLY GetObject/ListBucket on opal-data-bd/platinum/** + PutObject/ListBucket/GetObject on opal-data-demo/platinum/**. No s3:DeleteObject, no STS:AssumeRole to other roles, no broad opal-data-* wildcards.</ac>
    <ac id="AC2">EC2 service registered in EC2_MANIFEST.json (new entry OR extension of existing entry); safe-ec2-deploy.sh recognizes the service.</ac>
    <ac id="AC3">Transform script deployable via safe-ec2-deploy.sh dry-run (no errors).</ac>
    <ac id="AC4">Smoke-test write PASS: 1-byte dummy artifact written to opal-data-demo/platinum/_smoke_test/ via the EC2 service's IAM role + verified via aws s3 ls + cleaned up. Smoke-test read PASS: source artifact pullable from opal-data-bd/platinum/** via same role.</ac>
    <ac id="AC5">Terraform 0-diff post-apply (replan shows "No changes").</ac>
    <ac id="AC6">Shared-infra (or alternate pipeline) tag bumped + record-terraform-deploy.sh + CHANGELOG.json entry committed + pushed to origin/CLOUD with --follow-tags.</ac>
    <ac id="AC7">comp-iam gaps exits 0 (no new gaps); comp-iam service shows the new permissions matching the policy.</ac>
    <ac id="AC8">Session log includes Compiler Tools section reproducing every &lt;run&gt; from &lt;compiler_tools_mandate&gt; with observed output + explicit pass/fail vs. &lt;expect&gt;. Missing rows = REWORK.</ac>
    <ac id="AC9">RAVC2 to COO with all 8 ACs evidence + role ARN + hand-off signal to DS~C ("grant live -- proceed with --apply"); DS~C MCP'd in the same wake.</ac>
  </acceptance_criteria>

  <not_authorized>
    - Granting s3:DeleteObject (the demo dataset must be immutable post-transform).
    - Using broad opal-data-* wildcards (explicit bucket ARNs only).
    - Adding write-back to opal-data-bd (the source is read-only-from-the-demo-lane).
    - Standing up a new EC2 instance without first checking whether an existing demo-class service can absorb this via manifest extension.
    - Authoring this as a daily-pipeline IAM (this is one-shot).
    - Cutting acceptance flex on AC4 (smoke verify) -- the grant must be empirically confirmed from the EC2 service's perspective, not asserted from policy text alone.
  </not_authorized>
</task_order>
