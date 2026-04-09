# ADVI_GLDOPS.005 — DS: Bulk Vectorize All Gold Scripts

<task_order>
  <issuer>0.4.0_DS_ClientPlatform</issuer>
  <issued>2026-04-07</issued>
  <agent>0.4.0_DS_ClientPlatform</agent>
  <status>cancelled</status>
  <!-- GLDOPS archived 2026-04-07. This TO is orphaned. Cancelled by COO 2026-04-08. -->
  <priority>medium</priority>
  <project>ADVI_GLDOPS</project>
  <depends_on>GLDOPS.004 (in progress)</depends_on>
</task_order>

## Problem

Gold scripts process dates sequentially on a c6i.16xlarge (64 cores, 128GB RAM).
Total dataset fits in ~10GB memory. Scripts are I/O-bound on S3 round-trips,
not CPU or memory. This wastes 95%+ of the machine's capacity.

## Pattern (established in GLDOPS.004)

Every gold script should follow this pattern:

1. **Bulk load**: parallel S3 reads (256 workers) into in-memory dicts/DataFrames
2. **Vectorized compute**: one big pandas operation (groupby, cumsum, merge, shift)
   instead of per-date loops. Use the full 128GB — no reason to partition.
3. **Parallel write**: ThreadPoolExecutor(256) for S3 puts

No per-date S3 reads during compute. No sequential loops over dates.
No manual cumulative state dicts — use groupby().cumsum().

## Scripts already converted (GLDOPS.004)

- 02b_build_canonical_holdings.py
- 03b_build_canonical_lots.py
- 03c_build_account_gains.py
- 04a_build_canonical_performance.py
- 04b_validate_nna.py
- 05_build_client_performance.py (reads at 256 workers)

## Scripts to convert

- 05b_build_account_performance.py (ProcessPoolExecutor, already parallel but per-partition)
- 06_build_client_tax_liability.py
- 06b_build_client_mix_timeseries.py (ProcessPoolExecutor, already parallel but per-partition)
- 07_build_nna_aua_by_geography.py
- 08_build_nna_aua_by_advisor.py
- 08b_build_architect_attribution.py
- 08c_build_advisor_fee_efficiency.py
- 09_generate_partner_analytics.py
- 10_generate_advisor_rolling_flows.py
- 11a_publish_portal_aggregates.py
- 11b_publish_advisor_client_detail.py
- 12_build_composition_artifacts.py

## Acceptance Criteria

- [ ] All 12 downstream scripts use bulk load + vectorized compute + parallel write
- [ ] No sequential S3 I/O in any date processing path
- [ ] Full pipeline (00 through 11b) completes in under 10 minutes on c6i.16xlarge
- [ ] run_gold_layer.sh updated with new timing expectations
