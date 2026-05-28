<task_order>
  <metadata>
    <id>ADVI_INFDEMO.003</id>
    <slug>rd-fee-sliced-flows-adapter-passthrough</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-28</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <finding note="FE side VERIFIED-READY, NO code change needed. (a) The Inflection leaderboard adapter does NOT drop fee_breakdown: all three leaderboard fetches (getFirmLeaderboard:1710, getEmployeeLeaderboard:805, getPlatinumFirmDashboard:894) are raw JSON.parse/cast passthroughs — no field selection. Inflection partner index (inflection/index.tsx:71) uses getFirmLeaderboard, the IDENTICAL fetch 49F uses (49financial/index.tsx:92). (b) End-to-end PROVEN on 49F through this exact path: getFirmLeaderboard -> employeeData -> rawEntry -> applyFeeBucket (feeBucket.ts:85-102 spreads ...entry, preserves fee_breakdown, tenant-agnostic no-op when absent) -> SummaryCard slice (AdvisorPublicProfile.tsx:332 entry.fee_breakdown?.[feeView], optional-chained, NO Inflection gating). Type declares fee_breakdown (types.ts:2050). So the consuming chain is complete + ready. IWM activation = DS F11 emitting fee_breakdown into Inflection's platinum/firm/leaderboard.json (the TRIMMED artifact getFirmLeaderboard reads — same field 49F's trimmed leaderboard includes). NO FE passthrough to add (the CTO's 'if it drops it' condition is false). Sister: DS ADVI_INFDEMO.F11. Verified by /work 2026-05-28."/>
    <project_code>ADVI_INFDEMO</project_code>
    <priority>P1 — IWM demo-prep (Andrew direct). Explore/confirm; likely POST-DEMO (gated on DS F11 emit).</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFDEMO.md Batch 3 / F11</ref>
    <ref type="cto_finding">NOT a regression. Fee-slice consuming logic is intact: AdvisorPublicProfile.tsx:329-335 (SummaryCard) reads entry.fee_breakdown[feeView] for inflows/outflows/nna when feeView!='all' (INFFIN.022 d7775170). Works on 49F. Inflection just lacks entry.fee_breakdown.</ref>
    <ref type="sister">DS ADVI_INFDEMO.F11 (emits the Inflection fee_breakdown data).</ref>
  </references>

  <objective>
    Confirm the Inflection path will activate the EXISTING fee-slice flow logic once DS emits fee_breakdown — i.e. ensure the Inflection leaderboard adapter threads entry.fee_breakdown through to where SummaryCard:332 reads it. No new slice logic (it already exists + works for 49F).
  </objective>

  <explore_and_do>
    <step1>Trace the Inflection leaderboard/advisor-entry adapter (advisor-intelligence.ts static-inflection path) and confirm whether it would pass a source `fee_breakdown` field through to the PlatinumLeaderboardEntry.fee_breakdown the frontend consumes. If the adapter drops/omits fee_breakdown (likely, since it's never been present for Inflection), ADD the passthrough so it threads when DS F11 emits it.</step1>
    <step2>Confirm there's no Inflection-specific gating that would suppress the slice even with fee_breakdown present (e.g. a tenant conditional). The SummaryCard logic is tenant-agnostic; verify the adapter is the only gap.</step2>
    <step3>VERIFY end-to-end: with fee_breakdown present (mock it locally, or test against 49F which already has it, or against DS's F11 emit once it lands), confirm switching Fees: All→Fee-Paying→No Fee re-slices Inflows/Outflows/NNA. This proves the consuming end is ready.</step3>
  </explore_and_do>

  <acceptance>
    Report: (a) does the Inflection adapter pass fee_breakdown through (or did you add it)? (b) end-to-end confirmation that the Fees toggle re-slices flows when fee_breakdown is present. If you add the adapter passthrough, commit portal DEV + RAVC2 to COO + CC CTO. Coordinate with DS F11 (the emit) — your passthrough + their emit together light up the toggle.
  </acceptance>

  <notes>Gated on DS F11 for the full end-to-end (no Inflection fee_breakdown data exists yet). You CAN do the adapter-passthrough + 49F verification now (proves the path); the IWM activation completes when DS emits. Likely post-demo. Not demo-blocking — current aggregate flows are correct.</notes>
</task_order>
