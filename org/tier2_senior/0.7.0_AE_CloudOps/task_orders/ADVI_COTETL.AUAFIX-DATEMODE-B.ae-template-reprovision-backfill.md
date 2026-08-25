<to_id>ADVI_COTETL.AUAFIX-DATEMODE-B</to_id>
<project>ADVI_COTETL</project>
<title>AUAFIX DATEMODE-B (AE infra-leg) -- re-provision 3 BD templates (holdings/alloc/unrealized) CurrentDay -> Custom + backfill 06-09..latest</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<consult>0.4.0_DS_ClientPlatform (DATEMODE-A code commit-leg -- the cot_bronze_ingest.py edit must deploy MATCH before the backfill pull)</consult>
<issued_by>2.0.0_SA_COO (COTETL AUAFIX re-scope; CTO L2 ruling 135603Z; off your decisive probe)</issued_by>
<issued_date>2026-06-22</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_COTETL, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: REOPENED -- REGRESSION 2026-07-07T18:34Z. My earlier same-day flip to "complete" (based on served firm-AUA data_as_of=07-02 ALONE) was PREMATURE + is RETRACTED: it did not check the allocations/holdings TABLES this TO re-provisioned. Live-grounded incident (COO URGENT 182432Z, DS-found): silver/allocations EMPTY (0 rows) since ~07-01, silver/holdings stale + DROPPED from the 07-07 bronze pull. ROOT CAUSE = this TO's own CurrentDay->Custom flip: templates/allocations.json(qt5)+holdings.json(qt1) set to Custom on 06-22; the bronze producer's OWN comment (cot_bronze_ingest.py:334-336) documents that runtime Custom-date-stamping ZEROS qt5 allocations + NULLS qt1 holdings -- the exact two query-types + mode this TO set. holdings.json is also a 547-byte stub (no query body). AUA (holdings-snapshot path) masked it initially, but 2 of the 3 re-provisioned tables silently broke. FIX needs a CTO per-table date-mode ruling (real tension: CurrentDay froze AUA -> this TO switched to Custom -> Custom zeros these snapshots; the code implies CurrentDay-no-stamp is proven-good for qt1/qt5) + restore holdings.json body. Reported to COO+DS; awaiting the mode ruling before I re-provision (unilateral flips are the change-class that caused this).</status>
<!-- GO 2026-06-22 (COO /drive cycle-5): your probe resolved this internal. You diagnosed it; you own the BD template re-provision + the date-window + the backfill orchestration. -->

<objective>
Eliminate the CurrentDay date-mislabel at the SOURCE: re-provision the 3 BD DataMining export templates (holdings, allocations, unrealized) from CurrentDay to Custom mode (mirror the working transactions Custom-14 template; end = latest COMPLETE business day). Then backfill 06-09..latest so silver/gold catch up. Supply DS the exact ("Custom-N", end) tuple + per-table mapping for the DATEMODE-A code edit (cross-tool: you diagnose, DS commits).
</objective>

<the_fix>
HARD SEQUENCE GATE (CTO 135924Z): AE goes FIRST -- the DS code edit (DATEMODE-A) is inert until you re-provision + update the persisted templateId. Order: (1) you re-provision templates -> (2) hand DS per-table windows -> (3) DS commits matching code -> (4) you backfill -> (5) nightly-verify.

1. Re-provision holdings/alloc/unrealized BD templates to Custom + UPDATE templates/{table}.json templateId (the runner reuses the PERSISTED templateId -- a runtime-param change alone is ignored; banked reference_bd_datamining_blank_selection_template_status_error).
2. PER-TABLE windows, NOT blind Custom-14 (CTO 135924Z): holdings/alloc/unrealized are point-in-time SNAPSHOTS (the AUA basis), not transactions' 14d restatement log -- pick each table's EXACT minimal Custom window (end = latest COMPLETE business day; per-table lookback). Verify a fresh pull returns the CORRECT per-date asOfDate (not 06-08).
3. Hand DS the exact per-table ("Custom-N", end) tuple for cot_bronze_ingest.py TABLE_DATE_MODE (DATEMODE-A) -- DS takes YOUR windows, does not mirror Custom-14.
4. After DATEMODE-A deploys MATCH: run the BACKFILL pull holdings/alloc/unrealized 06-09..latest -> bronze (source pull via the normal bronze ingest, NOT ad-hoc inline). Confirm bronze gains 06-09..latest partitions with correct asOfDate stamps; silver/gold follow on the chain.
</the_fix>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service / comp-freshness (cot bronze pull path)</run>
      <expect>The cot-exporter/bronze pull has the IAM + the BD session is live (you started i-0643a5bee8a8feabf); no new perm gap for the backfill.</expect>
      <if_mismatch>comp-iam gaps; close any gap before the backfill pull.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after backfill">
    <step>
      <run>aws s3 ls cot bronze holdings/alloc/unrealized (partition check) + comp-freshness</run>
      <expect>Bronze gains 06-09..latest partitions with CORRECT per-date asOfDate stamps (not all 06-08); MVs advance ($397.7M-area at latest).</expect>
      <if_mismatch>Templates still mis-stamping -> re-check the Custom re-provision (persisted-template override).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
REPROCESS REQUIRED (this TO IS the reprocess leg for DATEMODE-A). Backfill 06-09..latest holdings/alloc/unrealized bronze -> silver -> gold. Validate the chain advances on the SCHEDULED nightly (no ad-hoc gold run -- c6i cost + manufactured-run ban).
</data_reprocess_scope>

<acceptance_criteria>
1. 3 BD templates re-provisioned to Custom (verified: a fresh pull returns CORRECT per-date asOfDate, not 06-08).
2. DS handed the exact ("Custom-N", end) tuple for DATEMODE-A.
3. Backfill 06-09..latest landed in bronze (partition + asOfDate check).
4. Session-log Compiler Tools section reproduces every <run> + result + pass/fail.
5. BINDING VERIFICATION GATE (project-level, shared with DATEMODE-A): served cot firm-AUA data_as_of advances PAST 06-09 AND total_aua ~$397.7M on the NEXT SCHEDULED NIGHTLY. NOT accepted until the nightly confirms. (Pairs with the L4 serve-time vintage alert so a future stamp-drift surfaces day-1.)
</acceptance_criteria>
