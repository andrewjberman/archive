<task_order>
<to_id>OPAL_VENDORPROVENANCE.BR1-AE.infra-legs</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P1-staged (implementation leg 2 of the sovereign retire ruling @6f4ad98db; ACTIVATES AFTER your v3 apply completes -- nothing here competes with the 10:00 ET fire. THE PLAN @7538cbc5f IS THE SPEC.)</priority>

<title>BR1-AE: the infra legs -- two Lambdas (Eclipse puller + completion-emitter) TF, the NEW silver floor (~15:15Z), the gold-floor rule live-verify, and eventually the G3 stop + TF retirement</title>

<context>
DS's execution plan @7538cbc5f is the authoritative spec (CTO concurred + floors condition
folded). Your legs per its lane table: (1) TF for the two new Lambdas (puller writing
bronze/eclipse_qa/ staging until the cut; completion-emitter on cron ~14:45Z); (2) the NEW
inf-silver-chain schedule floor (~15:15Z idempotent skip-if-converted) -- G2 is NOT live until
both consumer floors are; (3) LIVE-VERIFY the cited existing gold floor (inf-canonical-prices-
daily cron 14:00Z -> inf-gold-trigger) on the primitive -- a cited-but-unverified floor is the
disabled-control class; (4) at G3 (both gates live + one full cycle + one floor exercise
observed): the stop (destructive-class -- Andrew/COO word required), 14-day STOPPED-not-
terminated rollback window, then TF retirement.
</context>

<scope>
Per the plan verbatim; deviations are plan amendments. Full deploy law on every leg (TF-only,
commit-before-apply, safe-apply/HALTGT, 0-diff, tags, integrator push, deploy-completion
ledgers, comp-iam + live simulate-principal-policy one-resource-per-call for every new grant --
the puller Lambda touches Eclipse egress (lifted scope) + staging S3; the emitter touches the
sentinel key). The inf-pipeline targeted-applies-only posture: verify current state at
activation; honor whatever stands.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before TF">
    <step>
      <run>plan re-read @7538cbc5f + comp-blast on touched fns + live verify of inf-canonical-prices-daily (rule state + target, primitives)</run>
      <expect>The cited gold floor EXISTS-ENABLED live; contract values match the plan doc.</expect>
      <if_mismatch>STOP -- a missing cited floor is a plan amendment + CTO note, not an improvisation.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="apply">
    <step>
      <run>safe-apply per deploy law; IAM simulates per pair; 0-diff; ledger per leg</run>
      <expect>Staging-only write posture confirmed in the applied policies (the puller CANNOT write production keys pre-cut -- enforce in IAM, not just code).</expect>
      <if_mismatch>STOP + report; an over-broad grant here rebuilds R-1's write surface.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="G3, later">
    <step>
      <run>the stop ONLY on the recorded Andrew/COO word + all G3 preconditions evidenced; 14-day stopped window; TF retirement last</run>
      <expect>NEVER#7 ledger closed per leg; the rollback path stays real for 14 days.</expect>
      <if_mismatch>No stop without the word -- there is no override path on destructive-class.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
DS's script legs (GO'd) produce the code your TF deploys -- contracts through the plan doc only.
Sequencing at your seat: v3 apply + its proof window outrank this; activate when your board
clears. The G3 stop is the program's first destructive-class act -- it gets its own fresh
COO/Andrew confirmation at the time, never carried forward from tonight.
</cross_domain_coordination>

<acceptance_criteria>
1. Both Lambdas live with staging-only IAM enforced; both consumer floors live (new silver floor
   + gold floor live-verified); G2 emitter exercised.
2. Every leg under deploy law with ledgers; the plan doc amended where reality diverged.
3. G3 executes only on its evidenced preconditions + the fresh destructive-class word.
Plus: session log Compiler Tools section reproduces every <run> with observed output and explicit
pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="plan">BR1_EXECUTION_PLAN_retire_inf_bronze_runner.md @7538cbc5f (THE SPEC)</ref>
  <ref type="ruling">Andrew @6f4ad98db; CTO 042600Z (re-source concur + floors condition)</ref>
</references>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="T2.C v3 apply + first-fire proof" status="pending (this TO activates on your board clearing)"/>
  <dependency agent="0.4.0_DS_ClientPlatform" task="OPAL_VENDORPROVENANCE.BR1-DS.script-legs" status="pending (contracts via the plan doc)"/>
</dependencies>
</task_order>
