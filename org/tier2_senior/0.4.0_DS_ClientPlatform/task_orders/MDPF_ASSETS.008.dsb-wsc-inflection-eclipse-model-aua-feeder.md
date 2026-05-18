<task_order>
  <metadata>
    <id>MDPF_ASSETS.008</id>
    <slug>dsb-wsc-inflection-eclipse-model-aua-feeder</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-18 (COO) to DS~B -- MDPF Phase 2. WS-A contract ratified; the WS-C feasibility (.003, authored by DS~B) and the .006 coverage audit are both complete -- WS-C is fully scoped and unblocked. DS~B authored the .003 build spec, so this is its lane.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF Phase 2. WS-C is Cohort 2a (Inflection model AUA) + Cohort 2b (Inflection non-model). It is the largest genuinely-new feeder; the holdings[] pull is the substance.</priority>
    <sla>2-3d wall -- the model-AUA rollup is largely a conform of the shipped INF_E_00 output; the net-new work is the Orion Trading/Models items[] holdings pull (.003 §6 estimate: moderate, well-precedented).</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md (RATIFIED) -- THE SPEC. WS-C emits model_aua_positions (§3.1, firm_id=inflection) + model_composition (§3.2) + the non_model_aua row for inflection (§4). model_key per the §2 registry -- Eclipse ids [3,5,6,7,8,9,10,28,29] / Orion ids [83,84,85,86,87,88,89,152,153] are the authoritative columns (the .003 brief's Eclipse↔Orion map). model_value = account-decomposable Eclipse total_value, NOT the cached model_aum headline (ruling ii -- model_aum drifts 3.4%). target_weight basis v1 (ruling iii). Feeder parquet -> opal-data-mdpf (ruling vi).</contract>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.4) -- section 3.0 (Inflection = Cohort 2; 2a model, 2b non-model), section 4 WS-C, section 7-Q3 RESOLVED (Cohort 2b IS tracked Opal AUA).</prd>
    <build_spec>docs/briefs/mdpf-eclipse-inflection-model-aua-feasibility-20260518.md (MDPF_ASSETS.003, DS~B) -- THE WS-C BUILD SPEC. WS-C is GO; the model-AUA rollup mostly exists in the shipped INF_E_00 gold; the one convergent-schema gap is holdings[]. §6 lists the concrete paths. The ticker-level composition is the Orion GET /api/v1/Trading/Models/{id}.items[] endpoint (proven 2026-05-14, snapshot .runtmp/orion_model_probe/opal_models_with_items.json) -- the shipped Eclipse bronze puller does NOT call it; WS-C adds that pull.</build_spec>
    <coverage_audit>docs/briefs/mdpf-assets-006-eclipse-inflection-model-tracking-coverage-20260518.md (MDPF_ASSETS.006, DS~C) -- the coverage map. Recommendation 1: WS-C stays .003-scoped (model-AUA rollup + holdings[]); do NOT widen it to absorb transactions -- transaction-model attribution is a separate workstream (WS-H), product-gated. WS-C honors that boundary.</coverage_audit>
    <shipped_pipeline>data/orion/scripts/{bronze/pull_eclipse_portfolios.py, silver/convert_eclipse_portfolios_to_silver.py, gold/INF_E_00.eclipse_model_portfolios.py} (ADVI_ECLDAT) -- INF_E_00 already emits gold/eclipse/{date}/model_portfolio_accounts.parquet (399 rows, account grain) + _households + _summary. WS-C conforms this to the convergent schema; it does not re-build the rollup.</shipped_pipeline>
  </references>

  <context>
    WS-C feeds Cohort 2a (Inflection model AUA) and Cohort 2b (Inflection non-model AUA) into the MDPF canonical schema, firm_id=inflection. The .003 feasibility (which DS~B authored) confirmed the shipped ADVI_ECLDAT Eclipse pipeline already carries the partner identity, model assignment, account/household grain, and model values. Two pieces of genuine build work:

    1. model_composition -- the holdings[] gap. The shipped Eclipse model_composition artifact stops at the opaque Security-Set level; the ticker-level composition is the Orion Trading/Models/{id}.items[] endpoint. WS-C adds a bronze pull of the 9 Opal models' items[], a silver dim, and the gold expansion to (model_key, ticker) rows with target_weight + is_opal_etf. .003 §4.3 confirmed PFDE/PFOE are clean line-item positions in 7 of 9 Opal models -- this is what makes the §3.3 ETF decomposition (WS-D.2) work for Inflection.

    2. Cohort 2b -- Inflection non-model. PRD §7-Q3 is RESOLVED: Inflection non-model AUA IS tracked Opal AUA (a real interim quantity shrinking as Inflection migrates onto Opal models). .003 §5 found ~$106M of non-Opal-model advised assets (IWM models $87.9M + unassigned $18.2M) in the SAME Eclipse portfolios_full feed INF_E_00 currently filters out. WS-C populates the non_model_aua row for inflection per contract §4 -- the same residual shape as 49F (partner_custody_total − model_aua), with Inflection's custody scope.
  </context>

  <scope>
    <step>Phase 1 -- model_composition (the holdings[] gap, .003 §6). Add a bronze pull of Orion GET /api/v1/Trading/Models/{id} for the 9 Opal Orion-ids; silver-convert items[] to a composition dim; gold-emit model_composition rows -- (firm_id=inflection, model_key, as_of_date, ticker, security_name, product_class, target_weight as decimal 0-1, is_opal_etf for DIVZ/IDVZ/PFDE/PFOE, source_pipeline=eclipse). model_key via the §2 registry (Eclipse/Orion id columns). Reuse the existing JWT machinery (the Orion JWT in Secrets Manager orion/jwt/current) -- no new auth.</step>
    <step>Phase 2 -- model_aua_positions (conform the shipped rollup). Conform INF_E_00's model_portfolio_accounts.parquet (399 account rows) to the convergent §3.1 schema: firm_id=inflection, model_key via the registry, account_id=eclipse_account_id, household_id, model_value = the account-decomposable total_value (NOT model_aum -- ruling ii), custodian from Eclipse, source_pipeline=eclipse. This is a conform-and-tag, not a re-build.</step>
    <step>Phase 3 -- non_model_aua for inflection (Cohort 2b). Per contract §4: emit the non_model_aua row for firm_id=inflection -- the residual partner_custody_total(inflection) − model_aua(inflection). The ~$106M IWM + unassigned book (.003 §5) is in the portfolios_full feed already pulled. Determine partner_custody_total(inflection)'s scope -- the contract notes Inflection custody is Fidelity and the exact scope is a per-partner determination; populate method + custody_scope provenance fields honestly and, if the scope needs an Andrew call, surface it (do NOT block -- the contract's reserved-slot design treats an unresolved scope cleanly). Verify against .003 §5 ($93.6M model / $199.7M full book; the 5/15 ref had Inflection-Fidelity $203.87M -- reconcile the views).</step>
    <step>Land all three artifacts to the opal-data-mdpf feeder prefix (coordinate the bucket with AE -- ruling vi). Fixture/verify: model_composition target_weights sum to 1.0 per model_key; model_aua(inflection) reconciles to the INF_E_00 firm headline. Record the verified numbers. Rule 15 where applicable; ds-commit-gate exit 0.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam service on the bronze puller (the new Orion Trading/Models call) -- and comp-pipescript io on the shipped INF_E_00 + Eclipse silver scripts WS-C conforms.</run>
        <expect>The Orion Trading/Models call uses the existing orion/jwt/current auth -- if no new AWS surface, state N/A. The INF_E_00 column surface grounds the conform.</expect>
        <if_mismatch>Fix the IAM gap before deploy; reconcile the conform against the live INF_E_00 artifact.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast on the WS-C feeder functions</run>
        <expect>Blast radius is the new opal-data-mdpf feeder artifacts + the new Orion Trading/Models bronze pull -- no modification of the shipped ADVI_ECLDAT INF_E_00 pipeline (WS-C READS it).</expect>
        <if_mismatch>If WS-C modifies an ADVI_ECLDAT artifact, STOP -- coordinate with the ADVI_ECLDAT lane; WS-C reads, does not re-author.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>WS-C is a NEW feeder. It adds a new Orion Trading/Models bronze pull + conforms the shipped INF_E_00 gold output to the convergent schema -- it modifies no ADVI_ECLDAT producer and rewrites no existing artifact. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    WS-C ↔ ADVI_ECLDAT: WS-C READS the shipped Eclipse pipeline (bronze/silver/INF_E_00 gold) and ADDS a new Orion Trading/Models bronze pull; it does not modify any ADVI_ECLDAT script or artifact. The new puller reuses the existing orion/jwt/current JWT -- no new auth provisioning. Transaction-model attribution is explicitly OUT of WS-C scope (.006 recommendation 1 -- it is the proposed WS-H, product-gated); WS-C does not touch transactions. AE finalizes the opal-data-mdpf bucket -- coordinate. The Inflection-custody-scope question (Phase 3) is a per-partner determination -- surface to COO if it needs an Andrew call; do not block.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">model_composition ships for the 9 Opal models, firm_id=inflection -- ticker-grain via the Orion Trading/Models items[] pull, target_weight decimal summing to 1.0 per model_key, is_opal_etf flagged. Conformant to contract §3.2.</ac>
    <ac id="AC2">model_aua_positions ships for firm_id=inflection -- the conformed INF_E_00 account rollup, account-decomposable model_value (not model_aum), model_key via the registry. Conformant to contract §3.1.</ac>
    <ac id="AC3">non_model_aua ships for firm_id=inflection (Cohort 2b) per contract §4 -- the residual with partner_custody_total + model_aua_input + method + custody_scope provenance. The IWM/unassigned ~$106M is accounted; any custody-scope ambiguity is surfaced to COO, not silently resolved.</ac>
    <ac id="AC4">Verified: model_composition weights sum to 1.0 per model; model_aua(inflection) reconciles to the INF_E_00 headline (~$93.6M) and the .003 / 5-15 reference views. All three artifacts in the opal-data-mdpf feeder prefix.</ac>
    <ac id="AC5">No emoji; ds-commit-gate exit 0; Rule 15 where applicable; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The WS-C feeder: model_aua_positions + model_composition + non_model_aua for firm_id=inflection.
    - The new Orion Trading/Models items[] bronze pull + silver composition dim.
    - Session log with the Compiler Tools section + verified numbers. RAVC2 to COO.
  </deliverables>
</task_order>
