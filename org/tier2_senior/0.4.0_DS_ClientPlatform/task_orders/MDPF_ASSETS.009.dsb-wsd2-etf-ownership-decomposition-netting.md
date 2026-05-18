<task_order>
  <metadata>
    <id>MDPF_ASSETS.009</id>
    <slug>dsb-wsd2-etf-ownership-decomposition-netting</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED 2026-05-18 (COO) to DS~B. Phase 2 -- sequenced behind MDPF_ASSETS.008 (WS-C): WS-D.2's held_partner needs the partner model_composition feeds (WS-B + WS-C) for real numbers. COO flips to pending + fires GO when .008 closes (DS~B's lane frees). The Phase-0 scope-reconciliation can begin earlier if DS~B has slack -- it is read-only analysis.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF Phase 2. WS-D.2 produces Cohort 0 (the non-partner Opal-ETF public residual) and the §3.3 ETF ownership decomposition.</priority>
    <sla>1-2d wall -- mechanism-dependent on the Phase-0 scope finding; likely smaller than a full feeder build (much of the decomposition logic is already in the WS-A aggregation script).</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md (RATIFIED) -- §3.3 (no-double-count: held_partner is derived from model_composition is_opal_etf x model_aua_positions, the ETF slice is INSIDE model_aua, never standalone), §5 (the etf_net_assets feeder contract -- row per (ticker, as_of_date) with net_assets/nav/shares_outstanding; matches the ETFS_NETAST silver/netassets_daily.parquet schema), §6 (the platinum etf_decomposition[] block), §7 identity 2 (etf_total == Σ held_partner + public_residual; negative public_residual = ERROR) + identity 3 (no-double-count).</contract>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.4) -- section 3.0 (Cohort 0 = non-partner Opal-ETF public residual, tracked but NOT advised AUA), section 3.3, section 4 WS-D.2.</prd>
    <structural_note>The WS-A aggregation gold script (data/mdpf/scripts/gold/mdpf_aggregate_aua.py, shipped MDPF_ASSETS.004) ALREADY contains §3.3 ETF-decomposition + §7 reconciliation logic and emits the platinum etf_decomposition[] block -- fixture-verified (4/4 tests, incl. the negative-public_residual ERROR test). Contract §5 says "the §3.3 decomposition is built by WS-D.2, not WS-A" while §3.3/§6/§7 describe the WS-A script computing held_partner + public_residual. This apparent overlap is real and is WS-D.2's Phase-0 question -- see scope.</structural_note>
    <inputs>
      - ETF net-assets + holdings: shipped by WS-D.1 (MDPF_ASSETS.005) -- s3://opal-data-etfs/ silver/netassets_daily.parquet (all 4 ETFs) + silver/holdings/{date}.parquet (PFDE/PFOE line items).
      - Partner ETF exposure: from WS-B (.007) + WS-C (.008) model_composition (is_opal_etf rows) x model_aua_positions. .003 §4.3: PFDE/PFOE are line-item positions in 7 of 9 Opal models; DIVZ/IDVZ are held by NO Opal model (so held_partner(DIVZ)=held_partner(IDVZ)=0 for Inflection).
    </inputs>
  </references>

  <context>
    WS-D.2 produces Cohort 0 -- the non-partner Opal-ETF public residual -- and the §3.3 ETF ownership decomposition: for each Opal ETF, ETF_total_net_assets = Σ_partner held_partner + public_residual. held_partner is the partner-advised slice (already inside that partner's model_aua); public_residual (Cohort 0) is the measured plug -- ETF float held outside Opal's advised base. The §3.5 no-double-count rule is load-bearing: a partner-held ETF position is counted ONCE, inside model_aua, never also as standalone AUA.

    STRUCTURAL REALITY (Phase 0 resolves the exact scope). The WS-A aggregation script already computes the decomposition + runs the §7 identity-2/3 gates on fixtures. So WS-D.2 is NOT a from-scratch decomposition build. Its real scope is most likely: (a) wire the WS-D.1 etf_net_assets feed into the convergent feeder location/shape the WS-A script reads (WS-D.1 writes opal-data-etfs; the contract §5 etf_net_assets artifact must be available to the MDPF aggregation -- in opal-data-mdpf/feeds/etf_net_assets/ or referenced); (b) verify the end-to-end decomposition produces correct held_49F / held_inflection / public_residual once the WS-B + WS-C model_composition feeds exist; (c) close any gap the Phase-0 reconciliation finds between what the WS-A script does and what §3.3/§5 require. Phase 0 settles this before building -- do not duplicate logic the WS-A script already owns.
  </context>

  <scope>
    <step>Phase 0 -- scope reconciliation (read-only; can start before the GO). Read mdpf_aggregate_aua.py + the WS-A contract §3.3/§5/§6/§7. Establish precisely: what the WS-A script ALREADY computes (held_partner, public_residual, etf_decomposition[], the identity-2/3 gates) vs what WS-D.2 must still add. Determine the etf_net_assets feeder wiring: WS-D.1 writes opal-data-etfs -- decide with AE whether the MDPF aggregation reads it there or whether WS-D.2 lands a conformed etf_net_assets artifact in opal-data-mdpf/feeds/. Produce a short scope-decision note: WS-D.2's confirmed deliverable set. If Phase 0 finds WS-D.2 is purely a feeder-wiring + verification task (no new decomposition code), that is a valid and good finding -- record it and proceed accordingly.</step>
    <step>Phase 1 -- build to the Phase-0-confirmed scope. At minimum: the etf_net_assets feed is wired so the WS-A aggregation script reads all 4 Opal ETFs' net-assets in the contract §5 shape. If Phase 0 finds genuine decomposition logic missing from the WS-A script, build it there or as a WS-D.2 module -- but do NOT fork/duplicate the held_partner / public_residual computation the WS-A script already owns. Honor the no-double-count rule: held_partner derives from model_composition (is_opal_etf) x model_aua_positions; the ETF slice is never added as standalone AUA.</step>
    <step>Phase 2 -- end-to-end verification. With the WS-B + WS-C model_composition feeds present (or fixtures standing in for an absent feeder), verify the §7 identities on real/near-real data: identity 2 (etf_total == Σ held_partner + public_residual per ETF; public_residual >= 0 -- a negative is ERROR-class, partner over-attribution); identity 3 (no double-count). Confirm DIVZ/IDVZ public_residual = full net-assets (no Opal model holds them) and PFDE/PFOE carry a real held_inflection slice. Carry honestly the ruling-iii caveat: v1 held_partner is target-weight-based -- public_residual is an ESTIMATE, not exact; label it so. Record the verified per-ETF decomposition.</step>
  </scope>

  <gate_verdict_policy>WS-D.2's public_residual feeds the §7 identity-2 gate already in the WS-A script -- a negative public_residual is ERROR-class (the script exits non-zero). WS-D.2 adds no new gate; it ensures the existing gate runs on the real ETF feed.</gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on mdpf_aggregate_aua.py + the WS-D.1 etf probe; comp-trace on the etf_net_assets artifact path.</run>
        <expect>What the WS-A script reads/computes for ETFs + where WS-D.1's net-assets output lives -- grounds the Phase-0 scope reconciliation.</expect>
        <if_mismatch>If comp graph does not register the new data/mdpf/ or etf_netassets_watch/ nodes, fall back to direct script inspection; note which.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast on any WS-D.2 function added</run>
        <expect>Blast radius is the etf_net_assets feeder wiring + the MDPF platinum artifact only -- no overlap with the live ETFS_NETAST probe's canonical output or the INF chain.</expect>
        <if_mismatch>Reconcile before close.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>WS-D.2 wires an existing feed (WS-D.1's etf_net_assets) into the MDPF aggregation and verifies the decomposition; it modifies no producer and rewrites no artifact. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    WS-D.2 ↔ ETFS_NETAST / WS-D.1: WS-D.2 READS the WS-D.1 etf_net_assets + holdings output (opal-data-etfs) -- it does not modify the etf_probe.py probe. WS-D.2 ↔ WS-A: WS-D.2 must NOT fork the decomposition logic already in mdpf_aggregate_aua.py -- the Phase-0 reconciliation exists precisely to avoid duplication; if decomposition code must change, it changes in the WS-A script (one owner). WS-D.2 ↔ WS-B/WS-C: held_partner depends on their model_composition feeds -- WS-D.2's real-data verification gates on .007 + .008; fixtures stand in until they land. AE finalizes the opal-data-mdpf bucket + the etf_net_assets feed location -- coordinate.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A Phase-0 scope-decision note: what the WS-A aggregation script already owns vs WS-D.2's confirmed deliverable set; the etf_net_assets feeder-wiring decision. No duplication of the WS-A decomposition logic.</ac>
    <ac id="AC2">The etf_net_assets feed (all 4 Opal ETFs, contract §5 shape) is wired so the WS-A aggregation script consumes it -- the §3.3 decomposition runs on the real ETF net-assets, not a fixture.</ac>
    <ac id="AC3">End-to-end verified: per-ETF etf_total == Σ held_partner + public_residual; DIVZ/IDVZ public_residual = full net-assets (no Opal model holds them); PFDE/PFOE carry a real held_inflection slice; no double-count (identity 3). The target-weight v1 caveat (public_residual is an estimate) is labelled honestly.</ac>
    <ac id="AC4">No emoji; ds-commit-gate exit 0; Rule 15 where applicable; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Phase-0 scope-decision note.
    - The etf_net_assets feeder wiring + any Phase-0-confirmed decomposition work (no WS-A duplication).
    - The verified per-ETF decomposition (held_partner / public_residual / Cohort 0).
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
