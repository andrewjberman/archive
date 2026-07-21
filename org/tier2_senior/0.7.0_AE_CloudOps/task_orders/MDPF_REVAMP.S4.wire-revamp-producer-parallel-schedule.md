<task_order>
<id>MDPF_REVAMP.S4.wire-revamp-producer-parallel-schedule</id>
<project>MDPF_REVAMP</project>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>P0</priority>
<date>2026-07-21</date>

<references>
  <ref type="prd">docs/architecture/MDPF_REVAMP (S4: D publishers PARALLEL-NOT-SERVING -> parity streak)</ref>
  <ref type="ruling">CTO S4 DEPLOY route 20260721T162218Z + S4 spec RULING (A) 20260721T162832Z (arm PRODUCER schedule ONLY; publisher OFF until cutover)</ref>
  <ref type="ground">infra/aws/ec2/EC2_MANIFEST.json (mdpf-daily-runner; trigger mdpf-daily-trigger; EventBridge mdpf-daily-refresh-trigger); infra/aws/lambda/ci/lambda-source-map.json (opal-assets-mdpf-portal-publisher: build-alongside, schedule DEFERRED); infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf</ref>
</references>

<objective>
Wire the MDPF revamp PRODUCER to run PARALLEL on the existing MDPF nightly schedule so the N=3 parity
streak can accrue on CONSECUTIVE SCHEDULED cycles (currently hand-staged -> streak cannot accrue, and
hand-running trips the "validate on scheduled artifacts, not ad-hoc" NEVER rule). Build-alongside, zero
prod risk. Cycle 1 = the first scheduled parallel run.
</objective>

<spec authority="CTO RULING (A), verbatim-binding">
Arm ONLY the PRODUCER schedule: the parallel gold-runner (dim_mdpf_aggregate_aua_timeseries --firm all +
dim_mdpf_non_model_assets [A4]) runs on the existing MDPF nightly schedule, writing gold/mdpf_revamp/* ONLY.
The PUBLISHER (opal-assets-mdpf-portal-publisher, gold/mdpf_revamp/* -> portal/*) STAYS OFF / on-demand:
its EventBridge schedule is NOT armed here -- that happens at CUTOVER (S5), gated on the never-widen
CTO+COO co-sign. "publish HELD" = publisher NOT scheduled, portal/* UNTOUCHED. The streak accrues on the
PRODUCER (CTO per-cycle S3-verify + DT per-cycle parity + CVO independent each cycle); the publisher /
portal-copy is NOT needed to accrue the streak and is OUT OF SCOPE for this TO.
</spec>

<scope>
  <in>
    - Schedule the parallel revamp gold-runner on the existing MDPF nightly cadence (AE chooses the
      mechanism + grounds it: an added entry in the mdpf-daily-runner EC2 dispatch [s3://opal-data-mdpf/code/mdpf-daily-dispatch.sh]
      reusing the current convergence-gate trigger, OR a dedicated scheduled runner/Lambda -- whichever is
      lower-blast and least-privilege; justify via comp-blast + comp-iam).
    - Produce gold/mdpf_revamp/* each scheduled cycle (dim_mdpf_aggregate_aua_timeseries --firm all + A4 dim_mdpf_non_model_assets).
    - Terraform for any new/changed EventBridge rule, IAM, EC2 entry, or Lambda. source-map update. Tag after 0-diff.
  </in>
  <out>
    - The publisher (opal-assets-mdpf-portal-publisher). DO NOT arm its schedule, DO NOT invoke it, DO NOT
      touch portal/*. That is S5/cutover, co-sign-gated.
    - The LEGACY producer + current MDPF serving: UNCHANGED. This is build-ALONGSIDE.
    - gold/meta/pipeline-complete.json (Door-6): NEVER hand-written / never emitted by this runner (forged
      completion signal). The parallel run builds gold/mdpf_revamp/* only.
  </out>
</scope>

<guardrails>
  - NEVER move served output without never-widen CTO+COO sign-off -- publisher/portal-copy stays OFF (this TO cannot widen serve).
  - Terraform is the ONLY deploy mechanism (safe-apply, never bare apply; never aws lambda update-function-code). Commit before apply. 0-diff verify. Tag + push --follow-tags.
  - Door-6 gold/meta/pipeline-complete.json is NEVER hand-written.
  - Deploy-completion ledger (NEVER-rule): OPEN an entry in org/critical_paths/change_management/ at deploy-START, CLOSE it at completion. A begun deploy FINISHES in-session (every prefix/leg/activation) or rolls back + escalates to COO. Unclosed at session end = COO alarm.
  - Bronze/silver/serving untouched; this adds a parallel gold write only.
</guardrails>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-blast mdpf-daily-runner</run>
      <expect>Blast radius = the MDPF nightly chain (trigger -> runner -> legacy producer -> publisher). Enumerate every node the parallel-runner change touches; confirm the publisher + portal/* are NOT in the write path of the new runner.</expect>
      <if_mismatch>STOP. If the parallel runner would write anything under portal/* or invoke the publisher, the mechanism is wrong -- re-scope to gold/mdpf_revamp/* only. Surface to COO.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service &lt;the runner role for the parallel gold-runner&gt;</run>
      <expect>Role can PutObject to s3://&lt;mdpf gold bucket&gt;/gold/mdpf_revamp/* and READ its inputs. NO write grant to portal/* needed or added.</expect>
      <if_mismatch>STOP. comp-iam models (action) not (action,resource): for the exact gold/mdpf_revamp/* key run `aws iam simulate-principal-policy --policy-source-arn &lt;role&gt; --action-names s3:PutObject --resource-arns &lt;exact key&gt;` (ONE resource-arn/call; positive control as a SEPARATE invocation). Ground on live get-role-policy for any fresh IAM.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-iam gaps</run>
      <expect>If iam.tf changed: no new permission gaps introduced. If no iam.tf change: N/A (document).</expect>
      <if_mismatch>STOP. Close the gap before commit.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript deployed dim_mdpf_aggregate_aua_timeseries.py (+ dim_mdpf_non_model_assets.py)</run>
      <expect>MATCH -- the scheduled runner will execute the SAME committed/parity-clean revamp code DS shipped (DEPLOYED == imported), not a stale copy.</expect>
      <if_mismatch>STOP. Reconcile the deployed code to DS's committed revamp code before arming the schedule.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit/apply">
    <step>
      <run>aws s3 ls s3://&lt;mdpf gold bucket&gt;/gold/mdpf_revamp/ (post first scheduled fire) via ListObjectsV2 (key+ETag+Size)</run>
      <expect>gold/mdpf_revamp/* lands on the SCHEDULE (cycle 1 = first scheduled parallel run), mtime &gt; deploy-commit-time. HeadObject is NOT the acceptance instrument (it is s3:GetObject) -- use LISTING.</expect>
      <if_mismatch>Surface to COO + CTO. A missing/empty gold/mdpf_revamp/* on the schedule = the wiring did not take; do not report the streak as accruing.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on the new runner + confirm portal/* + legacy serving unchanged (ListObjectsV2 on portal/* mtime pre==post)</run>
      <expect>NO new serving consumer appeared; portal/* untouched (mtime unchanged); legacy producer output unchanged.</expect>
      <if_mismatch>STOP + RED-ALERT to COO. Any portal/* change is an un-co-signed serve-widen -- roll back.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
  - DS (0.4.0_DS_ClientPlatform / ~A): owns the revamp gold code (committed, parity-clean). Do NOT modify the producer logic -- deploy it as-is. MCP DS if the deployed code needs a change.
  - DT (0.2.0_DT_PortfolioAnalytics): owns the per-cycle PARITY re-verify (date-joined harness). Notify DT when cycle-1 gold/mdpf_revamp/* lands.
  - CTO (1.0.0_SA_CTO): owns the per-cycle S3 re-verify + the S4 gate + the S5 cutover co-sign. CTO gates the apply.
  - CVO (3.0.0_SA_CVO): independent each cycle.
  - Publisher (portal-copy): NOT this TO. S5/cutover, CTO+COO co-sign.
</cross_domain_coordination>

<acceptance_criteria>
  1. gold/mdpf_revamp/* is produced ON THE SCHEDULE (not hand-run) -- verified by ListObjectsV2 (key+ETag+Size, mtime &gt; deploy-commit-time); cycle 1 = first scheduled parallel run.
  2. The publisher (opal-assets-mdpf-portal-publisher) is NOT scheduled and NOT invoked; portal/* mtime UNCHANGED pre/post (machine-checked).
  3. Legacy producer output + current MDPF serving UNCHANGED (build-alongside).
  4. gold/meta/pipeline-complete.json NOT emitted by the new runner.
  5. Terraform 0-diff verified; source-map updated; tag pushed --follow-tags.
  6. Deploy-completion ledger entry OPENED at start + CLOSED at completion in org/critical_paths/change_management/.
  7. Session log includes a Compiler Tools section reproducing EVERY &lt;run&gt; above with observed output + explicit pass/fail vs &lt;expect&gt;. Missing rows = REWORK.
</acceptance_criteria>

<notes>
Sequencing: this S4 TO is P0 and takes precedence over the AE's pending DATA_PLATFORM.DC1/DC2 (Orion/Eclipse
recon) + NFRA_COMPLEARN.AMD-P3a TOs -- those stay staged behind it. Report cycle-1 landing to COO + CTO +
DT the moment gold/mdpf_revamp/* appears on the schedule.
</notes>
</task_order>
