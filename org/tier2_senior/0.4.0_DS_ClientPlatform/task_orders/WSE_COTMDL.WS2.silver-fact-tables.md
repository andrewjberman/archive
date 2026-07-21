<task_order>
<id>WSE_COTMDL.WS2.silver-fact-tables</id>
<project>WSE_COTMDL</project>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>P1 (parallel to cutover; cutover precedence)</priority>
<date>2026-07-21</date>

<references>
  <ref type="prd">docs/architecture/WSE_COTTONWOOD_MDPF_FOLDIN_PRD.md (sec 3,5)</ref>
</references>

<objective>
Build the 3 silver fact_* parquet converters (bronze -> silver, EventBridge on the bronze complete-stamp),
dedup + dtype ONLY (Rule 17): fact_model_definition, fact_model_blend, fact_model_assignment under
s3://opal-data-assets/blackdiamond/cottonwood/silver/.
</objective>

<scope>
  <in>
    - fact_model_definition (one row per model x leaf-component: model_id, model_name, is_opal, rebalance_model_type, sleeve_name, symbol, asset_id, absolute_allocation, relative_allocation).
    - fact_model_blend (model_id -> child primary-model-id + relative_allocation -- the blend split).
    - fact_model_assignment (account_id/externalId -> strategyName -> model_id, Rebalancer-authoritative; strategyName '--' = unassigned).
    - The bronze-complete(meta/{date}-complete.json)->silver EventBridge TRIGGER (targets this silver lambda). OWNERSHIP RULED to WS-2 (COO 2026-07-21, build-where-target-lives): WS-5 cannot forward-reference this silver ARN, so this deploy builds its own inbound trigger. Coordinate the source stamp path with WS-1/WS-5.
    - COMPLETE tables (Rule 17: dedup + dtype standardization ONLY). Parquet begins at silver (Rule 17a).
  </in>
  <out>
    - NEVER slim fields / fillna / dropna / business-row-filter / drop bronze columns (Rule 17 -- that judgment is gold-tier). NO name-filter here (the strict-Opal filter is a GOLD business-logic step, WS-3). Firm-sep: only blackdiamond/cottonwood.
  </out>
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io (the mirrored bd/silver converter pattern)</run>
      <expect>Silver = dedup+dtype passthrough; all bronze columns preserved; parquet output. No business logic.</expect>
      <if_mismatch>STOP. If a transform needs field-relevance/null judgment, it is GOLD -- move it to WS-3.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh (py_compile + ds-precommit AST/silver-ids + ruff); `from __future__ import annotations`</run>
      <expect>PASS. silver-id checks clean.</expect>
      <if_mismatch>STOP. Fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after run">
    <step>
      <run>aws s3 ls blackdiamond/cottonwood/silver/ (ListObjectsV2) + row-count vs bronze</run>
      <expect>3 fact_* tables land; row counts preserve bronze (no silent slim/drop). 60 models in definition; blend children present; ~910 accounts in assignment.</expect>
      <if_mismatch>Surface to COO. A row-count shrink = a silver slim violation (Rule 17).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
  - WS-1 (0.6.2): produces the bronze this consumes; triggered on its complete-stamp.
  - WS-3 (DS, same lane): consumes these silver facts for the gold dim.
</cross_domain_coordination>

<acceptance_criteria>
  1. 3 fact_* parquet tables land under blackdiamond/cottonwood/silver/, dedup+dtype only, all bronze columns preserved (no slim/fillna/dropna).
  2. Row counts consistent with bronze (60 models, blend children, full account book).
  3. Session log Compiler Tools section reproduces every <run> + pass/fail.
</acceptance_criteria>

<dependencies>
  <dependency agent="0.6.2_AE_PartnerETL" task="WSE_COTMDL.WS1 (bronze land)" status="staged"/>
</dependencies>
</task_order>
