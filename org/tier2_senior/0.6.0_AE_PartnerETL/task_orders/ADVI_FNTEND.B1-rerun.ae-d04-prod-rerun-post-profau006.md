<task_order>
  <metadata>
    <id>0.6.0_AE_PartnerETL-2026-04-14-advi-fntend-b1-rerun</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_FNTEND</project_code>
    <type>coordination</type>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (B1 AE re-run section)</ref>
    <ref type="upstream">ADVI_PROFAU.006 (Capital Gains TTM + Cost Basis by Year)</ref>
  </references>

  <objective>
    Trigger PROD D_04 gold re-run once ADVI_PROFAU.006 deploys to the PROD runner.
    Reuses the existing nightly gold-rerun pattern — no new infrastructure.
    This is a coordination ticket so the ownership is tracked per RD audit 2026-04-14 (CTO ratified).
  </objective>

  <acceptance_criteria>
    1. ADVI_PROFAU.006 confirmed live on PROD runner (bd-gold-layer-runner)
    2. D_04 PROD re-run completes cleanly (nightly EventBridge is the canonical trigger; no manual PROD-runner trigger — see MEMORY.md `feedback_no_prod_gold_trigger`)
    3. platinum/advisors/{id}/summary.json populated with `capital_gains_ttm` + `cost_basis_by_year` on client L3
    4. Top Gain Positions visible on client L3 drill after cache refresh
    5. MCP COMPLETE to COO confirming L3 population + linking to ADVI_PROFAU.006 deploy tag
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 3: Spot-check platinum output via `aws s3 cp ... summary.json` on 3 advisors — confirm new tax_exposure fields populate.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_PROFAU.006" status="complete" description="PROFAU.006 DE wiring already COMPLETE per registry; gates on PROD D_04 refresh to land the L3 data"/>
  </dependencies>

  <next>
    On COMPLETE: unblocks ADVI_FNTEND.B4 FE L3 acceptance criterion.
  </next>
</task_order>
