<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-FEEDEXP</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-22</date>
    <scope_expanded>2026-04-24 (COO 2.0.0_SA_COO) — added Cohort B (ORPHRELID 4 structural accounts, ~$670K AUA) per ORPHRELID closure `e28e0f5d` H1-A classification. Same BD data-ops inquiry pattern applies to both cohorts.</scope_expanded>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P4 — informational; no portal gate. Combined residual ~$6.68M (Cohort A $6.013M + Cohort B $670K) within Gate 2 band. Not blocking any active TO.</priority>
    <predecessors>
      <predecessor id="ADVI_ROLLUP.CP-RES20" status="complete" closeout_date="2026-04-22"
        note="Path C chosen — silver-invisible cohort (20 accts) documented as feed-boundary residual"/>
      <predecessor id="ADVI_ROLLUP.ORPHRELID" status="complete" closeout_date="2026-04-24"
        note="Orphan rel_id upstream trace; H1-A classification identified 4 structural accounts absent from accounts_dimension — same feed-gap pattern as CP-RES20 Cohort A; folded into this TO as Cohort B"/>
    </predecessors>
  </metadata>

  <cohort_b_orphrelid>
    Added 2026-04-24 per ORPHRELID RAVC (commit `e28e0f5d`, trace doc `data/black_diamond/diagnostics/ROLLUP/orphan_rel_id_trace.md`).

    4 accounts structurally absent from BD accounts_dimension since EOP2025:
      - z0819052671 ($35K)
      - z0819070781 ($29K)
      - z0819926011 ($280K)
      - z0820769131 ($326K)
      Combined: ~$670K AUA persistent; never linked in BD dimension export.

    Pattern: same class as Cohort A — BD feed gap (accounts_dimension missing entries). Distinct from Cohort A in that (a) these are IN silver/allocations, (b) they're not specifically UGL-absent like Cohort A, (c) they're missing from accounts_dimension itself. But the vendor inquiry pattern is identical: "these accounts appear in some BD feeds but not others — please confirm or correct."

    Consolidation rationale: single BD data-ops inquiry covering both cohorts is more efficient than two separate vendor asks; AE 0.6 handles as one engagement cycle.
  </cohort_b_orphrelid>

  <context>
    During CP-RES20 (2026-04-22), a 20-account cohort was identified as silver-invisible at the
    custody-feed level:

    Cohort characteristics:
      - 20 accounts (z0820721041, z0820721031, z0814308771, z0814292981, z0814308781,
        z0820682621, z0820930841, z0814317801, z0820682641, z0820682611, and 10 others)
      - All alloc_billable with alloc_noncash > $1,000
      - gold_mv = $0 (chronic-zero) — NOT a gold script bug; no upstream silver input
      - ZERO rows in silver/unrealized for any of these accounts (phase checked 2026-04-20 data)
      - No Schwab-RPS mapping (distinct from the 472 CP-MAP cohort which has unrealized rows
        but lacks Schwab-RPS mapping)
      - Only authority signal: silver/allocations per-account market_value (portfolio-aggregated,
        not lot-level)
      - Aggregate missing non-cash: $6,013,161 (0.36% of firm non-cash $1,660,263,546)

    Phase 1 empirical investigation (CP-RES20):
      1. silver/positions_cube: ABSENT from s3://opal-data-bd/silver/ — prefix does not exist.
         Path B (lot-level records from positions_cube) eliminated.
      2. Path A (synthetic stub emission with price_quality='allocation_stub'): technically feasible
         but distorts lot-level downstream consumers (B_01b classify, C_02 canonical_lots,
         C_05 client_tax_liability) without providing real cost basis, acquisition_date, or term.
         Bias cost-benefit at 0.36% gap: not justified.
      3. Path C selected: document silver-invisibility as feed-boundary residual; author this
         feed-expansion TO for the partner-ETL pod.

    Root cause hypothesis: these 20 accounts exist in BD's allocation feed
    (silver/allocations) but are absent from BD's unrealized/positions feed. They may be:
      (a) Accounts with only cash holdings (no securities position rows emitted by BD)
      (b) Newly onboarded accounts not yet appearing in BD's position snapshot
      (c) Accounts excluded from BD's UGL export for a custodian-specific reason
      (d) BD data-ops issue (same class as the CP-MASTERFEED coverage gap from 2026-03)
  </context>

  <objective>
    Investigate and expand the silver custody feed to cover the 20-account cohort, so that
    silver/unrealized (or an equivalent silver artifact) provides lot-level or at minimum
    position-level data for these accounts.

    Two parallel tracks recommended:

    Track 1 — BD data-ops inquiry:
      Work with BD / Schwab data team to understand why these 20 accounts appear in
      silver/allocations but not in the unrealized/positions snapshot. Request explicit
      inclusion or a separate feed file for these accounts.

    Track 2 — Silver ingestion expansion (if BD confirms a parallel feed exists):
      If BD emits a supplemental positions file (e.g., a "cash accounts" snapshot or
      accounts-with-no-positions export), extend the silver ingestion pipeline to ingest it
      and populate silver/unrealized rows for these accounts.

    Track 3 — If accounts are cash-only (no securities):
      If BD confirms these are cash-only accounts (no security positions), coordinate with
      DS to determine whether the alloc_noncash field in silver/allocations for cash-type
      accounts is a BD data quality issue (reporting non-zero alloc_noncash for cash-only)
      or a legitimate MV that should appear in gold via a cash-lot path.

    Success: silver/unrealized has rows for at least 15 of the 20 accounts, allowing B_01
    to produce gold MV entries and recover the $6,013,161 aggregate gap.
  </objective>

  <wire_contract>
    No immediate code change required from DS side. DS will add silver/unrealized rows for
    these accounts once AE confirms silver ingestion covers them.

    If Track 2 lands: AE updates silver ingestion Lambda/script to ingest supplemental BD file.
    DS re-runs B_00 → B_01 for the affected accounts to propagate to gold.

    Residual: if BD confirms accounts are legitimately cash-only with no security positions,
    DS will update gold_validate_config.yaml to document the known exclusion pattern.
  </wire_contract>

  <acceptance_criteria>
    1. BD data-ops inquiry initiated: AE sends formal inquiry to BD/Schwab data team citing
       (a) Cohort A — 20 account IDs + silver/unrealized absence, AND (b) Cohort B — 4
       account IDs + accounts_dimension absence (z0819052671 / z0819070781 / z0819926011 /
       z0820769131).
    2. Root cause determined for EACH cohort (one of a/b/c/d for Cohort A; analogous
       categories for Cohort B).
    3. If feed expansion feasible: silver ingestion updated + silver/unrealized or
       accounts_dimension populated for the respective cohorts + DS notified to re-run
       B_00 → B_01 or chain cascade as appropriate.
    4. If cash-only or by-design confirmed for any account: DS notified with BD confirmation;
       DS updates gold_validate_config.yaml known-exclusion block.
    5. MCP DS (0.4.0_DS_ClientPlatform) + COO (2.0.0_SA_COO) with outcome when resolved —
       cohort-separated report (Cohort A outcome + Cohort B outcome).
  </acceptance_criteria>

  <dependencies>
    <dependency task="ADVI_ROLLUP.CP-RES20" status="complete"
      note="Path C closeout is the trigger for this TO"/>
    <dependency task="BD data-ops access" status="external"
      note="BD/Schwab vendor coordination; no internal gate"/>
  </dependencies>

  <risk>
    External vendor dependency (BD data team) — timeline unknown. This TO is P4 and does
    not block any active portal feature or nightly run. The $6M residual is documented and
    within Gate 2 band. AE should pursue as capacity allows, not as a blocking item.
  </risk>

  <cohort_reference>
    Account IDs (20 accounts, measured against 2026-04-20 snapshot):
      z0820721041 — $2,000,000
      z0820721031 — $1,750,000
      z0814308771 —   $519,815
      z0814292981 —   $469,032
      z0814308781 —   $298,973
      z0820682621 —   $181,562
      z0820930841 —   $166,276
      z0814317801 —   $152,358
      z0820682641 —   $149,961
      z0820682611 —    $60,392
      (10 additional accounts with smaller allocations — full list in CP-RES20 session log
       2026-04-22: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-22/advi_rollup_cp_res20_path_c_closeout.md)

    S3 evidence snapshot:
      silver/allocations: accounts present with alloc_noncash > $1,000 (alloc_billable=True)
      silver/unrealized: 0 rows for any of these 20 accounts (2026-04-20 snapshot)
      gold/timeseries/holdings_lots/2026-04-20.parquet: gold_mv = $0 for all 20 accounts
  </cohort_reference>
</task_order>
