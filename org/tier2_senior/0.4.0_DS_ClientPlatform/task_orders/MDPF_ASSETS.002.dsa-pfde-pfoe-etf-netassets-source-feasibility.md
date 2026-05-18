<task_order>
  <metadata>
    <id>MDPF_ASSETS.002</id>
    <slug>dsa-pfde-pfoe-etf-netassets-source-feasibility</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18. Phase 0 investigation, read-only, no gate. DS~A runs this after MDPF_ASSETS.001 (same lane, sequential) -- or in either order; they are independent.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF_ASSETS Phase 0 (WS-D.1). The ETF ownership decomposition needs net-assets for all four Opal ETFs; only DIVZ/IDVZ are sourced today. Phase 0 feasibility probe; ends in a finding brief, NO implementation.</priority>
    <sla>~3-4h wall -- a source-feasibility probe + the brief. Lighter than MDPF_ASSETS.001.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.1, 3406a2edd) -- section 3.3 (ETF ownership decomposition), section 4 WS-D.1, section 6.3 seed MDPF_ASSETS.002, section 7 Q4 (ETF total source for PFDE/PFOE).</prd>
    <existing_feeder>ETFS_NETAST -- TrueShares daily net-assets probe for DIVZ + IDVZ; live, s3://opal-data-etfs/ (silver/ + snapshots/ + etf_history.csv present). The Phase-0-pilot probe structure to assess for replication.</existing_feeder>
    <etf_inventory>ETFS_SECIDX -- Phase 0 complete 2026-04 (102 securities / 138 tickers audited; DIVZ/IDVZ/PFOE/PFDE in scope). Reference for the ETF inventory.</etf_inventory>
  </references>

  <context>
    The four Opal ETFs are DIVZ, IDVZ, PFDE, PFOE. The MDPF_ASSETS ETF ownership decomposition (PRD section 3.3) needs each ETF's total net assets to compute `public_residual = ETF_total - Σ_partner held`. ETFS_NETAST sources DIVZ + IDVZ from TrueShares daily. PFDE + PFOE are NOT sourced. This TO is the Phase-0 feasibility probe: confirm the right source for PFDE/PFOE net-assets and whether the ETFS_NETAST probe structure replicates. Investigation only -- a finding brief, no ingestion built.
  </context>

  <scope>
    <in_scope>
      - Confirm whether TrueShares is the issuer / administrator / data-source for PFDE and PFOE (it supplies DIVZ/IDVZ). If TrueShares covers PFDE/PFOE, confirm the same daily-probe endpoint/mechanism returns their net-assets (NAV, market price, shares outstanding, net assets).
      - If TrueShares does NOT cover PFDE/PFOE: identify the correct issuer/administrator and the available net-assets data source (and its access mechanism + cadence).
      - Assess feasibility of replicating the ETFS_NETAST daily-probe structure for PFDE/PFOE -- same shape, or a different mechanism needed.
      - Document the concrete source + access path so the WS-D.1 Phase-1 build TO can be scoped off it.
    </in_scope>
    <out_of_scope>
      - Building the PFDE/PFOE ingestion -- that is the WS-D.1 Phase-1 build TO, authored after this brief.
      - The ownership decomposition itself (held_partner / public_residual) -- that is WS-D.2.
      - The broader ETF Operations portal surface (PRD section 1.4 -- future macro work).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="grounding the probe">
      <step>
        <run>aws s3 ls s3://opal-data-etfs/snapshots/ | tail -5 ; aws s3 ls s3://opal-data-etfs/silver/</run>
        <expect>The ETFS_NETAST DIVZ/IDVZ daily-probe artifact structure -- the template to assess for PFDE/PFOE replication.</expect>
        <if_mismatch>If the paths are empty/stale, note the ETFS_NETAST probe state in the brief -- it bears on the replication assessment.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Read-only feasibility probe; produces a finding brief, no script modified, no artifact written.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    Read-only assessment of the ETFS_NETAST probe structure -- no edit. The WS-D.1 Phase-1 build TO (authored after this brief) carries the cross_domain_coordination block vs ETFS_NETAST per PRD section 6.4. ETFS_NETAST keeps its own project code (PRD section 6.1 boundary ruling) -- this TO does not re-parent it.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">PFDE and PFOE net-assets source CONFIRMED -- either TrueShares (with the verified endpoint/mechanism that returns their NAV/price/shares/net-assets) or a named alternative source with its access mechanism + cadence.</ac>
    <ac id="AC2">Feasibility verdict: does the ETFS_NETAST daily-probe structure replicate for PFDE/PFOE as-is, or is a different mechanism required? Stated with the basis.</ac>
    <ac id="AC3">A finding brief committed under docs/briefs/ presenting AC1-AC2 + the concrete source/path for the WS-D.1 Phase-1 build TO.</ac>
    <ac id="AC4">Session log with the Compiler Tools section. RAVC2 to COO. "Complete" = the feasibility is determined, not that ingestion is built.</ac>
  </acceptance_criteria>

  <deliverables>
    - docs/briefs/mdpf-pfde-pfoe-etf-netassets-feasibility-20260518.md -- the WS-D.1 Phase-0 finding brief.
    - Session log with the Compiler Tools section.
    - RAVC2 to COO -- the brief is the input to the WS-D.1 Phase-1 build TO.
  </deliverables>
</task_order>
