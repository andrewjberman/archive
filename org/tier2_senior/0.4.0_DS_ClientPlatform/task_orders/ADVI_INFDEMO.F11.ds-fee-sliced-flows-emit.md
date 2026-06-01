<task_order>
  <metadata>
    <id>ADVI_INFDEMO.F11</id>
    <slug>ds-fee-sliced-flows-emit</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-28</date>
    <status>superseded</status>
    <reconcile_2026_06_01>SUPERSEDED by ADVI_INFMVP -- fee-split + canonical-NNA + flows shipped via ADVI_INFMVP.F4/F5 (f5ac50af1, bcc29881c) + F11-B leg-1 LIVE (982394f01). Fee-sliced-flows subsumed. (was: dispatched)</reconcile_2026_06_01>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFDEMO</project_code>
    <priority>P1 — IWM demo-prep (Andrew direct). Likely POST-DEMO (real data-emit work); explore-first.</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFDEMO.md Batch 3 / F11</ref>
    <ref type="andrew_direct">Andrew 2026-05-28 ~1105 PT: Fees: toggle doesn't change Inflows/Outflows/NNA — explore (suspected regression).</ref>
    <ref type="cto_finding">NOT a frontend regression — frontend fee-slice (AdvisorPublicProfile.tsx:329-335, INFFIN.022 d7775170) is intact + works on 49F. Root cause = Inflection leaderboard entry lacks fee_breakdown. 49F has it; IWM doesn't.</ref>
    <ref type="frontend_contract">PlatinumFeeBreakdown shape (types.ts:1989): {aua, account_count, client_count, nna, inflows, outflows, period_start_aua?, aua_growth_pct?, new_clients?}; entry.fee_breakdown = {fee_paying: PlatinumFeeBreakdown, no_fee: PlatinumFeeBreakdown} (types.ts:2035-2051).</ref>
  </references>

  <objective>
    EXPLORE then (if feasible) EMIT: produce the per-fee-status flow breakdown for Inflection advisors so the existing frontend Fees: toggle re-slices Inflows/Outflows/NNA. The consuming frontend already exists + works for 49F — this is purely the missing data emit on the Inflection side.
  </objective>

  <explore>
    <q1>Does the Inflection source (per-account flows + per-account fee status) carry enough to compute, per advisor + per window (QTD/YTD/MAX), the fee_paying vs no_fee split of inflows / outflows / nna / aua / account_count / client_count? Per-account fee_bps>0 = fee_paying (the FeeSummaryPanel already partitions fee-paying AUA this way), and per-account flows should be aggregable into the two buckets.</q1>
    <q2>Where in the Inflection leaderboard/headline gold + adapter pipeline would fee_breakdown be emitted onto the advisor entry? (Mirror how 49F's fee_breakdown is produced — find the 49F emit + replicate the shape for Inflection.)</q2>
    <q3>Windowing: the frontend reads fee_breakdown per the active window. Confirm whether fee_breakdown is per-window or single — match whatever 49F does so the QTD/YTD/MAX toggle + Fees toggle compose correctly.</q3>
  </explore>

  <do>
    If the source supports it: emit entry.fee_breakdown.{fee_paying,no_fee} with the PlatinumFeeBreakdown fields (at minimum inflows/outflows/nna; aua/account_count/client_count if cheap) for Inflection advisors, matching the 49F shape + windowing. If the source does NOT support it (e.g. flows aren't fee-attributable per account at the needed granularity): report exactly what's missing + what it would take. Do NOT fabricate a split.
  </do>

  <acceptance>
    Inflection advisor leaderboard entry carries fee_breakdown.{fee_paying,no_fee} flows that sum to the aggregate (fee_paying + no_fee == all, per metric), verified by CVO /verify-channel against live S3. RAVC2 to COO + CC CTO. Once emitted, coordinate with RD (ADVI_INFDEMO.003) to confirm the toggle re-slices end-to-end.
  </acceptance>

  <notes>Likely post-demo (real data work). Not demo-blocking — the current aggregate flows are correct (= the "All" view). Sister to RD ADVI_INFDEMO.003 (adapter passthrough). If you can produce a quick emit that verifies before the early-PM demo, flag CTO for a ship decision; otherwise post-demo.</notes>
</task_order>
