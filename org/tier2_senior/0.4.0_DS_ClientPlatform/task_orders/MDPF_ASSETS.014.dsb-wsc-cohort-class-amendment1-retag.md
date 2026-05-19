<task_order>
  <metadata>
    <id>MDPF_ASSETS.014</id>
    <slug>dsb-wsc-cohort-class-amendment1-retag</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO). Not gated. WS-C (.008) shipped around the WS-A-contract AMENDMENT-1 ratification and predates the cohort_class column; .013's end-to-end run CONFIRMED the gap on the live S3 parquet (inflection model_aua_positions, 399 rows, no cohort_class; non_model_aua lacks sma_aua_input). This is the small WS-C re-tag .013's cross_domain_coordination named as the clean follow-on.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P2 -- MDPF Phase-2 cleanup. NOT blocking: .013's normalize_amendment1() already surfaced-defaults the missing columns correctly (Inflection has no SMA, so cohort_class='model' for all rows; the §7 dual check PASSES inflection). This TO removes the surfaced-default dependency by making WS-C natively AMENDMENT-1-conformant -- structural cleanliness, not a correctness fix.</priority>
    <sla>0.5d wall -- a column add mirroring the shipped WS-B re-tag (commit 24251a794, registry v3 model_type).</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md AMENDMENT 1 -- §3.1 model_aua_positions carries cohort_class {model|sma} derived from the registry model_type via model_key; §4 the non_model_aua artifact carries sma_aua_input beside model_aua_input.</contract>
    <wsb_precedent>WS-B (.007) was re-tagged for cohort_class -- commit 24251a794, registry v3 (model_type). WS-C mirrors that exact pattern: read model_type from data/mdpf/scripts/gold/mdpf_model_registry.json via model_key, set cohort_class.</wsb_precedent>
    <wsc_feeder>The WS-C feeder (MDPF_ASSETS.008 deliverable, DS~B) -- emits model_aua_positions + model_composition + non_model_aua for firm_id=inflection to opal-data-mdpf.</wsc_feeder>
    <amendment1_consumer>.013 (mdpf_aggregate_aua.py, commits 1757fe364 + d2c751cfc) reads cohort_class and runs the §7 dual model_aua_input/sma_aua_input check. .013's normalize_amendment1() currently fills WS-C's missing columns with the surfaced default + records meta.feeds_pre_amendment1 -- this TO makes that normalization a no-op for WS-C.</amendment1_consumer>
  </references>

  <context>
    Inflection's advised book is all core-model today -- the Eclipse Opal models carry no SMA strategies (Eclipse models 9/10 carry zero per .013 cross_domain_coordination). So every WS-C model_aua_positions row is cohort_class='model' and inflection sma_aua=0. The column must nonetheless be PRESENT and natively emitted -- the AMENDMENT-1 contract requires it, and relying on the consumer-side surfaced-default is a latent fragility (a future Inflection SMA strategy would silently mis-bucket). This TO re-tags the WS-C feeder to emit cohort_class + sma_aua_input natively, mirroring the WS-B re-tag.
  </context>

  <scope>
    <step>Phase 1 -- re-tag the WS-C feeder:
      - model_aua_positions: add the cohort_class column, derived from the registry model_type via model_key (same lookup WS-B uses, mdpf_model_registry.json registry v3). For Inflection's 9 Eclipse Opal models this resolves to cohort_class='model' for all rows -- but it is DERIVED, not hardcoded, so a future SMA model resolves correctly. A model_key whose registry model_type is absent emits cohort_class per the registry rule WS-B established (do not silently default -- mirror WS-B).
      - non_model_aua: add the sma_aua_input audit field beside model_aua_input. For inflection sma_aua_input = 0.00 (no SMA), model_aua_input unchanged.
      - Rule 15 (from __future__ import annotations first) on any gold/silver/bronze script touched; ds-commit-gate exit 0 on every .py edit.</step>
    <step>Phase 2 -- re-run the WS-C feeder, re-land the two artifacts (model_aua_positions + non_model_aua) for firm_id=inflection to the opal-data-mdpf feeder prefix. Verify: cohort_class present on all 399 inflection model_aua_positions rows, all = 'model'; non_model_aua carries sma_aua_input = 0.00. model_aua(inflection) unchanged at $93,603,055.45 (re-tag is additive -- no value change).</step>
    <step>Phase 3 -- verify the consumer. Re-run mdpf_aggregate_aua.py against the re-tagged feed; confirm meta.feeds_pre_amendment1 NO LONGER lists WS-C / inflection (the feed is now natively conformant), and the §7 dual check still PASSES inflection. Record in the session log.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on the WS-C feeder script.</run>
        <expect>The registry read + model_aua_positions/non_model_aua write surface; no COLUMN GAP after cohort_class is added to the emit set.</expect>
        <if_mismatch>Reconcile the column surface before write.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast on the re-tagged feeder function.</run>
        <expect>Blast radius is the WS-C opal-data-mdpf feeder artifacts only -- no overlap with the live ADVI_ECLDAT INF_E_00 pipeline (WS-C reads it, does not modify it).</expect>
        <if_mismatch>If the re-tag touches an ADVI_ECLDAT artifact, STOP -- surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>The WS-C feeder re-runs and re-writes its two opal-data-mdpf artifacts (model_aua_positions + non_model_aua for inflection) with the added columns. No upstream producer modified; no ADVI_ECLDAT reprocessing. The values are unchanged -- only the schema gains cohort_class + sma_aua_input.</reprocess_required>
  </data_reprocess_scope>

  <cross_domain_coordination>
    WS-C feeder is DS~B's own (.008) -- single-owner, no concurrent-edit hazard. The re-tag must mirror the WS-B re-tag (24251a794) for consistency -- same registry lookup, same null-handling rule. .013 (mdpf_aggregate_aua.py) is the consumer; this TO makes WS-C natively conformant so .013's normalize_amendment1() no longer has to default it -- coordinate verification with DS~A only at the read-back (Phase 3), no concurrent edit.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">WS-C model_aua_positions emits cohort_class natively for firm_id=inflection -- derived from registry model_type via model_key (not hardcoded), all 399 rows resolve to 'model'. Conformant to AMENDMENT-1 §3.1.</ac>
    <ac id="AC2">WS-C non_model_aua emits sma_aua_input (= 0.00 for inflection) beside model_aua_input. Conformant to AMENDMENT-1 §4.</ac>
    <ac id="AC3">Both artifacts re-landed in opal-data-mdpf; model_aua(inflection) unchanged at $93,603,055.45. mdpf_aggregate_aua.py re-run confirms meta.feeds_pre_amendment1 no longer lists WS-C/inflection and the §7 dual check still PASSES inflection.</ac>
    <ac id="AC4">No emoji; ds-commit-gate exit 0 on every .py edit; Rule 15 where applicable; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The re-tagged WS-C feeder emitting cohort_class + sma_aua_input.
    - The two re-landed artifacts (model_aua_positions + non_model_aua, firm_id=inflection) in opal-data-mdpf.
    - Session log with the Compiler Tools section + the Phase-3 consumer verification. RAVC2 to COO.
  </deliverables>
</task_order>
