<task_order>
<id>WSE_COTMDL.WS3.gold-dim-model-portfolio</id>
<project>WSE_COTMDL</project>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>P1 (parallel to cutover; cutover precedence)</priority>
<date>2026-07-21</date>

<references>
  <ref type="prd">docs/architecture/WSE_COTTONWOOD_MDPF_FOLDIN_PRD.md (sec 2,5,6)</ref>
</references>

<objective>
Build the gold dim_model_portfolio producer (silver -> gold; gold = the one business-logic/parse-down point):
per in-scope Opal model {account_count, dollar_value} via the count-vs-dollar mechanism (sec 6), with the
sec-5 count-reconciliation self-gate. Land under blackdiamond/cottonwood/gold/ (currently empty = target).
</objective>

<scope>
  <in>
    - STRICT Opal name filter (Andrew-direct): name ILIKE '%opal%' -> the 17 in-scope models; the 43 non-Opal OUT. (This filter is the gold business-logic step, not silver.)
    - Count-vs-dollar (sec 6): for account assigned strategy M with value V=Sum(holdings market_value): if M's children are primary Opal models (blend) -> count[c.name]+=1, dollars[c.name]+=V*c.relativeAllocation (nested blends recurse); if single/flat -> count[M]+=1, dollars[M]+=V. Aggregate across the 296 assigned accounts.
    - MDPF row set = UNION of {assignable Opal strategies that aren't pure primary-model blends} U {primary Opal building-block models the blends decompose into}.
    - Value join: accounts externalId (z09+8-digit, 11-char) === cot holdings silver account_id; sum market_value per account.
  </in>
  <out>
    - No SMA/UMA sleeve handling needed (all sleeve flags zero for cot Opal, grounded). Firm-clean: value join reads ONLY cot holdings silver, never blackdiamond/49f.
  </out>
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io (the mirrored gold dim producer)</run>
      <expect>READS the 3 fact_* silver + cot holdings silver; WRITES gold/dim_model_portfolio. No column gaps.</expect>
      <if_mismatch>STOP. Fix the load list.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit / producer self-gate">
    <step>
      <run>The sec-5 COUNT-RECONCILIATION self-gate (in the producer): full-sweep per-strategy account counts == roster accountCount for every Opal model</run>
      <expect>296 across 14 assigned Opal models (Sat50=82, Sat60=79, Sat80=54, Sat70=39, Sat40=16, Sat98=12, Sat30=4, UltraShort=3, Income=2, + 5 singletons). 0 orphan strategyNames.</expect>
      <if_mismatch>STOP -- HARD GATE. A count mismatch = the assignment pull is wrong; do NOT emit the gold dim. Surface to COO+CTO.</if_mismatch>
    </step>
    <step>
      <run>.tools/commit-gate.sh; `from __future__ import annotations`</run>
      <expect>PASS.</expect>
      <if_mismatch>STOP.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after run">
    <step>
      <run>Inspect gold/dim_model_portfolio (ListObjectsV2 + spot-check): per-Opal-model {account_count, dollar_value}; count sums tie to 296; dollars tie to Sum(account values)</run>
      <expect>Rows for the union primary-model set; account_count total == 296 (blend +1s expand it correctly); dollar_value total == portfolio total. Sane magnitude (cot AUA ~$437M).</expect>
      <if_mismatch>Surface to COO+CTO. This feeds MDPF -- must be correct before WS-4 folds it in.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
  - WS-2 (same lane): provides the silver facts.
  - WS-4 (AE/DT): folds this gold dim into the MDPF DDB -- gate a QA/verify on the first dim_model_portfolio (PRD sec 11f) before it serves.
</cross_domain_coordination>

<acceptance_criteria>
  1. gold/dim_model_portfolio lands with per in-scope Opal model {account_count, dollar_value}; strict-Opal filter applied; union primary-model set built.
  2. The sec-5 count-reconciliation gate PASSES (296 across 14) -- machine-checked in the producer; a mismatch blocks emission.
  3. Dollar/count totals tie (count->296 via blend expansion; dollars->portfolio total); sane magnitude.
  4. Session log Compiler Tools section reproduces every <run> incl the reconciliation gate result.
</acceptance_criteria>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="WSE_COTMDL.WS2 (silver facts)" status="staged"/>
</dependencies>
</task_order>
