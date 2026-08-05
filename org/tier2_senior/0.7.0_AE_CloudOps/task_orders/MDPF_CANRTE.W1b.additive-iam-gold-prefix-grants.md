<task_order>
<id>MDPF_CANRTE.W1b</id>
<title>ADDITIVE IAM: grant gold-bucket GetObject + ListBucket alongside the existing platinum grants, so W-1a's source re-point cannot fail at runtime</title>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-05</issued>
<status>staged</status>
<priority>P1 -- blocks W-1a</priority>
<arch_gate>1.0.0_SA_CTO, re-gate ruling 183006Z</arch_gate>

<context>
W-1 SPLIT a/b because the consumer set closed at FIVE and the prefix is pinned in IAM in three places
-- and gold is a DIFFERENT BUCKET (opal-data-portal-v2 -> opal-data-assets), so no IAM follows a
source re-point. One seat in one window became impossible; CTO ruled the split.

W-1b LANDS FIRST AND IS PURELY ADDITIVE. W-1a (DS, source, five consumer legs) lands second.
WHY THIS ORDER: an additive IAM change is independently reversible and CANNOT break the running
chain. A source re-point without IAM fails at runtime. Sequencing the reversible, non-breaking half
first is free -- DO NOT INVERT IT.

NOT THE VETOED SHADOW/DUAL-READ CLASS: adding a permission is not adding a data path. Only ONE write
target exists at any moment. This is PERMISSION, not ROUTING. (CTO ruling, verbatim reasoning.)
</context>

<the_three_pins>
  <pin file="infra/aws/terraform/opal-assets/emitter.tf" line="59" action="s3:GetObject"
       resource="arn:aws:s3:::${local.platinum_bucket}/platinum/mdpf/aggregate_aua/*"/>
  <pin file="infra/aws/terraform/opal-assets/emitter.tf" line="63-68" action="s3:ListBucket"
       resource="arn:aws:s3:::${local.platinum_bucket}"
       condition="StringLike s3:prefix = [platinum/mdpf/aggregate_aua/*]"
       note="*** THE TRAP. See below. ***"/>
  <pin file="infra/aws/terraform/mdpf-pipeline/iam.tf" line="753" action="s3:GetObject"
       resource="arn:aws:s3:::opal-data-portal-v2/platinum/mdpf/aggregate_aua/*"/>
</the_three_pins>

<scope>
  ADD gold-bucket GetObject + ListBucket to all three statements.
  *** KEEP THE EXISTING PLATINUM GRANTS. *** They are removed LATER, with the teardown -- NOT in this
  window. Removing them here would break the running chain, which is the exact thing this ordering
  exists to prevent.
  The ListBucket statement needs its CONDITION extended to cover the gold prefix, not just its Resource.
</scope>

<the_listbucket_trap>
  `StringLike s3:prefix` IS A SECOND, INDEPENDENT PIN THAT A BUCKET-ARN EDIT DOES NOT TOUCH.
  Add the gold bucket to the Resource and leave the condition alone, and the grant still DENIES --
  and it denies the **LIST**, not the GET. The caller is `_latest_key()` -> `list_objects_v2`, so the
  symptom is an AccessDenied on a list operation, which is NOT what anyone debugging a re-pointed
  READ would be looking for. Found by 0.4.0_DS outside their own lane.
</the_listbucket_trap>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service opal-assets-daily-emitter</run>
      <expect>Current modeled grants enumerated. *** NECESSARY BUT NOT SUFFICIENT -- comp-iam models (action), NEVER (action, resource), and reports [GRANTED] off ANY bucket. It will tell you nothing about the gold bucket. Its default view is DESIRED (parsed TF), not APPLIED. ***</expect>
      <if_mismatch>Do not treat a comp-iam GREEN as evidence of anything here. Proceed to the live primitive.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/terraform.exe plan (via safe-apply path)</run>
      <expect>Diff is ADDITIVE ONLY -- new gold statements/resources/condition values. ZERO removals of any platinum grant.</expect>
      <if_mismatch>STOP. Any platinum removal in this window is out of scope and breaks the running chain.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>aws iam simulate-principal-policy --policy-source-arn &lt;emitter role&gt; --action-names s3:ListBucket --resource-arns arn:aws:s3:::opal-data-assets --context-entries ContextKeyName=s3:prefix,ContextKeyValues=&lt;gold prefix&gt;,ContextKeyType=string</run>
      <expect>allowed. *** --context-entries IS MANDATORY: the statement is CONDITIONED, and with no context an unsatisfied condition returns implicitDeny BYTE-IDENTICAL TO A REAL DENY. *** ONE --resource-arns per call -- 2+ ARNs flips held ones to implicitDeny.</expect>
      <if_mismatch>The condition was not extended. Fix the condition, not the Resource.</if_mismatch>
    </step>
    <step>
      <run>aws iam simulate-principal-policy ... s3:GetObject --resource-arns &lt;one exact gold key&gt;</run>
      <expect>allowed.</expect>
      <if_mismatch>Resource pin not extended for GetObject.</if_mismatch>
    </step>
    <step>
      <run>POSITIVE CONTROL, AS A SEPARATE INVOCATION: the same two calls against the EXISTING platinum ARNs</run>
      <expect>still allowed -- proves the additive change did not disturb the running path. *** RUN IT IN ISOLATION. A control batched with the target is corrupted by its own presence (Rule 22a, mode 1). ***</expect>
      <if_mismatch>STOP -- you have altered a live grant. Roll back.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
  <criterion>All three pins carry gold-bucket grants AND retain their platinum grants. Plan diff additive-only, quoted.</criterion>
  <criterion>ListBucket CONDITION extended to the gold prefix -- verified by a simulate call carrying --context-entries. A Resource-only edit is NOT acceptance.</criterion>
  <criterion>Positive control on the platinum path run in a SEPARATE invocation and still allowed.</criterion>
  <criterion>Session log reproduces every run with observed output and pass/fail vs expect. Missing rows = REWORK.</criterion>
  <criterion>NO alarm/monitor/checker built (standing moratorium).</criterion>
</acceptance_criteria>

<dependencies>
  <blocks id="MDPF_CANRTE.W1a" note="DS source re-point across five consumer legs. MUST NOT begin until W-1b is applied and verified."/>
</dependencies>

<explicitly_out_of_scope>
  Removing platinum grants (rides the teardown). The 439-partition copy (W-1a). Any source edit.
  Any teardown -- see the W-3 note: THE EC2 RUNS TEN SCRIPTS INCLUDING THE CANONICAL SPINE, so the
  chain SURVIVES this wave and nothing may be decommissioned on the old assumption.
</explicitly_out_of_scope>
</task_order>
