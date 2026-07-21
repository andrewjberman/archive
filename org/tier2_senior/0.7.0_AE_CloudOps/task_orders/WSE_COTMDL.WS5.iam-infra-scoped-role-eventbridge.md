<task_order>
<id>WSE_COTMDL.WS5.iam-infra-scoped-role-eventbridge</id>
<project>WSE_COTMDL</project>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>
<priority>P1 (infra scaffolding -- can proceed ahead of the standing-egress GO; the daily SCHEDULE arms only after WS-1 egress)</priority>
<date>2026-07-21</date>

<references>
  <ref type="prd">docs/architecture/WSE_COTTONWOOD_MDPF_FOLDIN_PRD.md (sec 7,9,10,11)</ref>
</references>

<objective>
Stand up the scoped IAM role + EventBridge schedule/stamp-triggers + Terraform for the WS-E producer chain,
mirroring the opal-assets-bd49f infra. Terraform-only (Rule 1/2/4/18). NO new alarm (07-17 suspend).
</objective>

<scope>
  <in>
    - Scoped {resource}-role: PutObject blackdiamond/cottonwood/{bronze,silver,gold,meta}/**, read blackdiamond/cot/session secret, read cot holdings silver, DDB PutItem on the MDPF table (WS-4 fold-in) -- EXACT-ARN grants, PAB-on, firm-sep DENY to blackdiamond/49f.
    - EventBridge: the daily schedule for opal-assets-bd-rebalancer-daily-pull (bronze) + stamp-triggers bronze-complete->silver, silver->gold (mirror the bd49f/estate trigger pattern). The daily SCHEDULE is armed but the producer's live pull is gated on WS-1's standing egress -- coordinate the arm-timing with WS-1.
    - Terraform + source-map entry (Rule 4); safe-apply (Rule 18); tag after 0-diff.
  </in>
  <out>
    - NO new SNS/CloudWatch alarm/twin (07-17 suspend; the absence-twin is DEFERRED target-state). NO modification to other firms' infra (new-territory: pure-add TF only). Never grant blackdiamond/49f.
  </out>
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam gaps + comp-blast (the bd49f infra pattern being mirrored)</run>
      <expect>The scoped role's grants match the pull's needs; firm-sep deny present; no gaps. Mirror the estate pattern, don't improvise.</expect>
      <if_mismatch>STOP. Ground the pattern.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>For EACH new grant: aws iam simulate-principal-policy --resource-arns &lt;exact ARN&gt; --action-names &lt;action&gt; (ONE arn/call; SEPARATE positive control) -- S3 PutObject on cottonwood prefixes + DDB PutItem on the MDPF table + a NEGATIVE control on blackdiamond/49f (must DENY)</run>
      <expect>Each cottonwood/MDPF grant GRANTED; the blackdiamond/49f negative control DENIED (firm-sep). comp-iam alone is NOT sufficient for the new resources.</expect>
      <if_mismatch>STOP. Do not apply until the exact-ARN grants + firm-sep deny verify on the live primitive.</if_mismatch>
    </step>
    <step>
      <run>.tools/safe-apply.sh (0-diff verify); source-map updated</run>
      <expect>0-diff; pure-add (new-territory); tag pushed --follow-tags.</expect>
      <if_mismatch>STOP. A non-pure-add plan is out of scope.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
  - WS-1 (0.6.2): runs under this role/schedule -- coordinate the schedule arm-timing with WS-1's standing egress.
  - WS-4 (self-lane): the fold-in role's DDB grant lives here.
</cross_domain_coordination>

<acceptance_criteria>
  1. Scoped role live with EXACT-ARN grants (S3 cottonwood prefixes + DDB MDPF table + secret/holdings reads), PAB-on, firm-sep DENY to blackdiamond/49f -- each verified on the live primitive (simulate-principal-policy, isolated positive control, negative control on 49f).
  2. EventBridge schedule + stamp-triggers live (mirror estate); daily pull SCHEDULE arm-timed to WS-1 standing egress.
  3. Terraform 0-diff, pure-add, source-map updated, tag pushed. NO new alarm.
  4. Session log Compiler Tools section reproduces every <run> incl the per-ARN simulate + the 49f negative control.
</acceptance_criteria>

<dependencies>
  <dependency agent="none" task="infra scaffolding can start; daily schedule arm coordinated with WS-1 egress" status="ready"/>
</dependencies>
</task_order>
