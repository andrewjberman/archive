<task_order>
  <metadata>
    <id>MDPF_ASSETS.013</id>
    <slug>dsa-wsa-aggregation-cohort1c-amendment1-update</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO) to DS~A. Not gated -- the WS-A contract AMENDMENT 1 is the spec and is ratified. Sequence: DS~A self-sequences on its own lane AFTER WS-E (MDPF_ASSETS.010) -- both are DS~A's; the aggregation-script update consumes the §4 non_model_aua artifact shape WS-E emits, so WS-E first is the natural order. Carved out as its own TO (not folded into .007/.010) because it is a CONSUMER-layer change to a shipped script, distinct from the feeder TOs.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF Phase 2. The aggregation script is the script that produces the platinum artifact + runs the §7 reconciliation gates; it must be AMENDMENT-1-correct before the platinum aggregate is correct.</priority>
    <sla>1d wall -- a bounded update to one shipped script + its fixtures; the contract AMENDMENT 1 fully specs the deltas.</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md -- AMENDMENT 1 (CTO-ratified 2026-05-18, commit 7d8934ff2) IS THE SPEC. The three contract deltas, verbatim scope:
      (1) §3.1 model_aua_positions gains a cohort_class column {model|sma} -- derived from the registry model_type via model_key.
      (2) §4 non-model residual: non_model_aua = partner_custody_total − model_aua − sma_aua (subtracts BOTH; subtracting only model_aua double-counts SMA dollars). The non_model_aua artifact gains a sma_aua_input audit field beside model_aua_input.
      (3) §7 identity 1 extends: opal_aggregate_aua == Σ_partner (model_aua + sma_aua + non_model_aua); the residual-input consistency check becomes DUAL -- model_aua_input == Σ model_aua_positions.model_value WHERE cohort_class='model' AND sma_aua_input == Σ ... WHERE cohort_class='sma'.
      §3.1/§4/§7 inline contract text is already updated to match. Cohort 1a = core models, Cohort 1c = SMAs, Cohort 1b = non-model -- a clean three-way partition of advised AUA (no excluded category).</contract>
    <prd>docs/architecture/MDPF_ASSETS.md v0.5 -- §3.0 cohort taxonomy with Cohort Nc (SMA) as a first-class sub-cohort.</prd>
    <target_script>data/mdpf/scripts/gold/mdpf_aggregate_aua.py + mdpf_aggregate_aua_fixtures.py -- shipped under MDPF_ASSETS.004 (closed) BEFORE AMENDMENT 1. The script currently does the two-way (model + non_model) decomposition; this TO brings it to the ratified three-way. Same script, same DS~A authorship -- a contract-amendment update, not a rewrite.</target_script>
    <feeder_state>WS-B (.007) re-tagged for cohort_class -- commit 24251a794, registry v3 (model_type). Cohort 1a $1,335.95M / 6,755 accts + Cohort 1c $24.79M / 94 accts emitted as distinct cohort_class line items. WS-E (.010) finalizes its residual on the AMENDMENT-1 formula (subtracts both 1a + 1c).</feeder_state>
  </references>

  <context>
    AMENDMENT 1 (Andrew-directed, CTO-ratified) makes a partner's advised book a THREE-way sub-classification: core models (Cohort Na, model_aua) + SMA strategies (Cohort Nc, sma_aua) + non-model (Cohort Nb, non_model_aua). The MDPF aggregation gold script (mdpf_aggregate_aua.py) shipped under the now-closed MDPF_ASSETS.004 predates the amendment -- it computes a two-way (model + non_model) decomposition and a two-term reconciliation. It must be updated to the ratified three-way before the platinum aggregate artifact and the §7 reconciliation gates are correct.

    This is carved out as its own TO -- not folded into WS-B (.007, a near-closed feeder) or WS-E (.010, also a feeder) -- because it is a consumer/aggregator-layer change to a specific shipped script. It is DS~A's code (DS~A authored .004); DS~A self-sequences it after WS-E on its own lane (the §7 dual-input check the script asserts must match the sma_aua_input field WS-E's non_model_aua artifact emits).
  </context>

  <scope>
    <step>Phase 1 -- update mdpf_aggregate_aua.py to the AMENDMENT-1 three-way:
      - Read cohort_class from model_aua_positions. Compute, per partner: model_aua = Σ model_value WHERE cohort_class='model'; sma_aua = Σ model_value WHERE cohort_class='sma'. (Handle a feed missing cohort_class deliberately -- see cross_domain_coordination -- do not silently mis-bucket.)
      - The platinum artifact partners[] entries carry model_aua + sma_aua + non_model_aua + total_aua (= the three summed); the aggregate block sums all three across partners. by_model breakdown reflects cohort_class.
      - §7 identity 1: opal_aggregate_aua == Σ_partner (model_aua + sma_aua + non_model_aua), $0.01 tolerance, ERROR outside.
      - §7 residual-input check becomes DUAL: assert non_model_aua.model_aua_input == Σ model_aua_positions.model_value WHERE cohort_class='model' AND non_model_aua.sma_aua_input == Σ ... WHERE cohort_class='sma', per (firm_id, as_of_date). A mismatch on EITHER → identity_1 model_aua_input_check: ERROR.
      Rule 15 (from __future__ import annotations first); ds-commit-gate exit 0.</step>
    <step>Phase 2 -- update mdpf_aggregate_aua_fixtures.py for the three-way: the existing 4 tests adapted (valid 3-way fixtures with the 3 identities; the negative-public_residual fixture still raises ERROR); ADD a fixture that breaks the sma_aua_input consistency check and verify it raises ERROR (the new dual-check half). Target: all tests pass; the two ERROR fixtures (negative-residual + sma-input-mismatch) raise, not pass.</step>
    <step>Phase 3 -- end-to-end verify on real feeders. Run mdpf_aggregate_aua.py --source s3 against the live opal-data-mdpf feeds (WS-B re-tagged 1a/1c; WS-C; etc.). Confirm: 49F shows model_aua (1a) ~$1,336M + sma_aua (1c) ~$24.8M as distinct terms (never a lumped $1,360M); the §7 dual check passes; reconciliation overall PASS. Record the verified three-way breakdown.</step>
  </scope>

  <gate_verdict_policy>The script's §7 reconciliation block is ERROR-gated (exits non-zero on any identity ERROR) -- unchanged by AMENDMENT 1 except that identity 1 + the input check now cover three sub-cohorts. The negative-public_residual ERROR fixture remains mandatory.</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on mdpf_aggregate_aua.py -- confirm the cohort_class column is in the load set once added.</run>
        <expect>No COLUMN GAP after the update -- cohort_class is read from model_aua_positions.</expect>
        <if_mismatch>Reconcile the load set.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast on the updated aggregation function + the fixture run end-to-end.</run>
        <expect>Blast radius unchanged from .004 (the new data/mdpf/ home, standalone -- no INF/SmartX/ETFS chain overlap); fixtures pass, the two ERROR fixtures raise.</expect>
        <if_mismatch>Debug before close.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>An update to one shipped gold script + its fixtures; the script runs ad-hoc / fixture-driven at Phase 2. No data pipeline producer modified beyond this script, no artifact backfill. The platinum artifact is regenerated on the next run -- forward, not a reprocess.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    The script is DS~A's own (.004) -- single-owner, no concurrent-edit hazard. COHORT_CLASS ON THE FEEDS: WS-B (.007) re-tagged and emits cohort_class (commit 24251a794). VERIFY WS-C's (.008, closed) model_aua_positions also carries cohort_class -- WS-C shipped around the AMENDMENT-1 ratification; if its feed lacks cohort_class, the aggregation script cannot bucket Inflection positions. If WS-C's feed is missing cohort_class, do NOT silently default it -- surface to COO; a small WS-C re-tag (mirroring WS-B's) is the fix, a separate follow-on. (Inflection has no SMA assets today -- Eclipse models 9/10 carry zero -- so Inflection's positions are all cohort_class='model', but the column must still be present.) WS-E (.010) emits the non_model_aua artifact with sma_aua_input -- the script's §7 dual check reads it; sequence WS-E before this so the check runs against the real field.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">mdpf_aggregate_aua.py computes the three-way decomposition -- model_aua (cohort_class='model') + sma_aua (cohort_class='sma') + non_model_aua -- per partner; the platinum artifact carries all three + total_aua.</ac>
    <ac id="AC2">§7 identity 1 covers all three sub-cohorts; the residual-input check is dual (model_aua_input + sma_aua_input), each asserted against the matching cohort_class subset. A mismatch on either raises ERROR.</ac>
    <ac id="AC3">mdpf_aggregate_aua_fixtures.py updated for the three-way -- all tests pass; the negative-public_residual fixture AND a new sma_aua_input-mismatch fixture both raise ERROR.</ac>
    <ac id="AC4">End-to-end on the live opal-data-mdpf feeds: 49F reports 1a and 1c as distinct terms (no lumped $1,360M), the §7 dual check passes, reconciliation overall PASS. WS-C cohort_class presence confirmed (or its absence surfaced to COO).</ac>
    <ac id="AC5">No emoji; ds-commit-gate exit 0; Rule 15; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - Updated mdpf_aggregate_aua.py (three-way decomposition + the §7 AMENDMENT-1 reconciliation).
    - Updated mdpf_aggregate_aua_fixtures.py (three-way; the two ERROR fixtures).
    - The verified end-to-end three-way breakdown. Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
