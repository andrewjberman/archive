# Task Order: ADVI_TICKID.007 — Account-Level Silver AUA Override

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-26-silver-aua-override</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>complete</status>
  </metadata>

  <objective>
    Add account-level silver AUA override in scripts 05 and 05b. For any account where
    gold AUA diverges from silver account_market_value by more than 20%, use silver as
    the authoritative AUA. This catches non-traded instruments (insurance annuities,
    donor advised funds) where gold's units * price is unreliable. $94M gross impact.
    CTO endorsed account-level approach over position-level overrides.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/05_build_client_performance.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05b_build_account_performance.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">In scripts 05 and 05b, after computing gold AUA per account
      (units * canonical_price, summed): (a) load silver allocations for the same date
      from silver/allocations/{date}.parquet (same read pattern as 05c),
      (b) join on account_id, (c) compute divergence = abs(gold_aua - silver_aua) / silver_aua,
      (d) if divergence > 0.20 (OVERRIDE_THRESHOLD) and silver_aua > $1,000 (MINIMUM_AUA):
      replace gold_aua with silver_aua for that account, tag source as 'silver_override',
      log account_id + gold_aua + silver_aua + divergence_pct.</requirement>
    <requirement id="2">Silver load goes inside the date loop — one parquet read per date,
      no memory impact. Graceful fallback: if silver parquet missing for a date, skip
      override for that date and log a warning.</requirement>
    <requirement id="3">Ghost accounts in aua_overrides.json must remain excluded before
      override logic runs — the override does NOT replace the ghost account exclusion.</requirement>
    <requirement id="4">Log summary per gold run: total accounts overridden, total dollar
      impact of overrides, largest individual override.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Accounts with non-traded instruments report AUA within 20% of silver's reported value</criterion>
    <criterion id="2">Script 05c overall gap decreases from ~1.6% to target less than 0.5%</criterion>
    <criterion id="3">Override count and dollar impact logged per gold run</criterion>
    <criterion id="4">Money market accounts remain unaffected (gold already matches silver at $1.00 NAV)</criterion>
    <criterion id="5">Ghost accounts in aua_overrides.json remain excluded</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Scripts 05 and 05b do NOT currently load silver allocations. This is a new dependency — use the same read pattern as 05c: silver/allocations/{date}.parquet.</constraint>
    <constraint>Money markets priced at $1.00 NAV are correct (units * $1.00 = market value). They will not trigger the override because silver also reports units * $1.00. No special handling needed.</constraint>
    <constraint>This TO can be developed in parallel with Phase A (.005/.006) — different scripts, no overlap.</constraint>
  </constraints>

  <dependencies>
    <!-- Independent of Phase A; can run in parallel with .005/.006 -->
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_TICKID_PRICING_DIVERGENCE_ADDENDUM.md</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Modified scripts 05 and 05b with silver AUA override logic</deliverable>
  </deliverables>
</task_order>
