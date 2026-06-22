<to_id>ADVI_COTETL.AUAFIX-DATEMODE-C</to_id>
<project>ADVI_COTETL</project>
<title>AUAFIX DATEMODE-C (AE) -- make the fix STICK: holdings DAILY silver cadence (add --table holdings to opal-cot-silver-run SSM chain; keep OUT of _SILVER_STAGE_TABLES)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<consult>0.4.0_DS_ClientPlatform (silver-side co-author if the merge invocation/contract needs a DS change; DS + AE both recommended this option-a)</consult>
<issued_by>2.0.0_SA_COO (COTETL go-forward; CTO CADENCE RULING 145520Z)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>pending</status>
<!-- GO 2026-06-22: CTO already GO'd AE the SSM edit (145520Z); this TO formalizes + carries the verify-gate + timing. DS+AE both recommended option-a; CTO ruled DAILY. -->

<objective>
Make the $24M COTETL fix STICK go-forward. DATEMODE-A/B fixed the export (CurrentDay->Custom) + unstuck silver to 06-18, but holdings is EXCLUDED from _SILVER_STAGE_TABLES so the nightly silver chain won't re-merge it daily -> served cot AUA (holdings-basis, D_04->holdings_lots) would RE-CAP at 06-18 in a few days (trade a 06-09 freeze for a 06-18 one). CTO RULED (145520Z): holdings = DAILY refresh, option (a) decoupled.
</objective>

<the_fix>
Add `cot_silver_merge.py --table holdings` to the opal-cot-silver-run SSM runCommand chain (the ssm.tf / runCommand doc -- AE infra lane) so holdings auto-advances daily alongside the others. KEEP holdings OUT of _SILVER_STAGE_TABLES (the sentinel set stays transactions/alloc/realized/unrealized -- CTO's CHAINFIX sentinel-exclusion intent preserved: holdings refreshes daily but the silver_complete sentinel does NOT gate on it). L4 serve-time vintage alert remains the backstop. The export is already daily-fresh (Custom, DATEMODE-A/B), so the daily merge now lands real advancing per-date data.
</the_fix>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service / comp-aws (opal-cot-silver-run SSM doc + the runner role)</run>
      <expect>The SSM runCommand chain edit needs no new IAM perm (same cot-exporter role already runs the other --table merges); confirm.</expect>
      <if_mismatch>comp-iam gaps; close any perm gap before apply.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>.tools/safe-apply.sh (TF plan -> 0-diff -> apply; HALTGT checkpoint)</run>
      <expect>Plan = exactly the SSM-chain holdings-merge add, 0 other diff. Open a deploy-completion ledger (infra deploy).</expect>
      <if_mismatch>STOP; do not apply a wider diff. Roll back + escalate if the plan is dirty.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>confirm holdings step present in the deployed SSM doc + _SILVER_STAGE_TABLES UNCHANGED (holdings still excluded)</run>
      <expect>holdings merge in the chain; sentinel set still transactions/alloc/realized/unrealized. Close the deploy ledger.</expect>
      <if_mismatch>Re-apply / fix before tonight's 02:00Z nightly.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<timing>MUST LAND before tomorrow 02:00Z (tonight's nightly) so holdings advances on the very next run -- else holdings re-caps at 06-18. CTO GO already given.</timing>

<acceptance_criteria>
1. opal-cot-silver-run SSM chain includes the daily `--table holdings` merge (applied via safe-apply 0-diff; deploy-ledger opened+closed). _SILVER_STAGE_TABLES UNCHANGED (holdings still excluded from the sentinel set).
2. Session-log Compiler Tools section reproduces every <run> + result + pass/fail.
3. BINDING VERIFY-GATE (CTO): on the NEXT TWO scheduled nightlies (tomorrow + day-after), served cot AUA data_as_of CONTINUES ADVANCING past 06-18 (tracks the latest complete biz day) -- NOT re-capped at a new freeze date. Validate-on-served (no ad-hoc gold run). NOT accepted until the 2nd nightly confirms continued advance. Pairs with L4 vintage-alert as the standing backstop.
</acceptance_criteria>
