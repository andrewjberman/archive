<task_order>
  <metadata>
    <id>ADVI_INFDEMO.F11-followonB</id>
    <slug>ds-real-daily-fee-substreams-timeseries</slug>
    <issued_by>0.6.1_AE_PartnerETL (Andrew-direct consult) -> self-authored DS</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-28</date>
    <status>pending</status>
    <project_code>ADVI_INFDEMO</project_code>
    <priority>P2 — POST-DEMO. Not demo-blocking; leaderboard Flows split (F11) is the authoritative real split for the demo.</priority>
  </metadata>

  <references>
    <ref type="parent">ADVI_INFDEMO.F11 (leaderboard fee_breakdown — DONE + CVO-verified, ac95741d6 + new_clients 9950a3f2c)</ref>
    <ref type="consult">0.6.1_AE_PartnerETL 165331Z follow-on B; Andrew-direct</ref>
  </references>

  <problem>
    Two surfaces show a fee-split of NNA/flows and DIVERGE:
    - FLOWS (Exec Summary) = leaderboard entry.fee_breakdown -> REAL per-account windowed split (F11, canonical_nna x billing is_fee_earning).
    - LIFETIME ACTIVITY = advisor timeseries.json -> SYNTHETIC. Confirmed: NO gold script emits fee sub-streams (grep nna_canonical_fee_paying/_no_fee across data/orion/scripts/gold = 0). timeseries.json carries only aggregate nna_canonical + *_canonical. The FE adapter (AdvisorAnalytics ~:252-255) synthesizes the split from a ratio.
    Aggregate totals reconcile; the fee-split diverges because one is real and one is synthesized.
  </problem>

  <objective>
    Make the Lifetime Activity fee-split REAL + consistent with the leaderboard Flows split by emitting real daily fee sub-streams into the advisor timeseries, so both surfaces derive from the one per-account join.
  </objective>

  <scope>
    - Emit nna_canonical_fee_paying / nna_canonical_no_fee (and inflows/outflows fee-split if the panel reads them) as DAILY sub-streams into the advisor timeseries.json, via the SAME canonical_nna x billing(is_fee_earning) per-account join used in INF_D_00c F11, but at daily grain.
    - Producer: the timeseries builder (INF_D_06.client_timeseries.py / INF_D_09.account_timeseries.py — confirm which writes platinum/advisors/{key}/timeseries.json AdvisorTimeseriesPoint).
    - Coordinate w/ RD: once real sub-streams exist, the adapter consumes them instead of synthesizing the ratio.
    - v1 simplification (same as F11): is_fee_earning = current-snapshot flag applied to historical daily flows.
  </scope>

  <acceptance>
    AC1: timeseries.json carries real daily nna_canonical_fee_paying/_no_fee (sum to nna_canonical per date).
    AC2: Lifetime Activity fee-split == leaderboard Flows fee-split for the same window (both real, same join).
    AC3: CVO /verify-channel (daily sub-stream sum-invariant + cross-surface agreement).
    AC4: RD adapter switched off the synthetic ratio onto the real sub-streams.
  </acceptance>

  <notes>
    Post-demo. For the demo, leaderboard Flows is authoritative-real; Lifetime Activity synthetic split is a known approximation. Quick RD check: is the Lifetime Activity fee-split even shown in the demo flow? If not, urgency drops further.
  </notes>
</task_order>
