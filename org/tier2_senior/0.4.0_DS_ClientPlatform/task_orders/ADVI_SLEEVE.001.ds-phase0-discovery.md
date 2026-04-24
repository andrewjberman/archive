<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-24-advi-sleeve-001-ds-phase0-discovery</id>
  <project>ADVI_SLEEVE</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>0.4.0_DS_ClientPlatform</issued_to>
  <issued_date>2026-04-24</issued_date>
  <status>cancelled</status><!-- CANCELLED 2026-04-24 by 2.0.0_SA_COO. Work already complete: SL-P0 decision memo (Path 3 selected — cost-basis apportionment) + SL-P1 shadow emit code at 28818eaf (2026-04-16, DS 0.4.0). ADVI_SLEEVE.json was stale at Phase 0 pending; actual state is Phase 0 COMPLETE / Phase 1 STAGED (blocked on nightly re-enable post-INFLEC W4.13b). COO dispatched this TO without verifying SL-P0 commit history. Same pattern as CANNNA.P2 redundant TO. No DS action required; disregard. -->

  <title>ADVI_SLEEVE Phase 0 — Discovery + cohort sizing + quantity source recommendation</title>

  <references>
    <ref type="prd">docs/architecture/ADVI_SLEEVE_PLAN.md</ref>
    <ref type="prd">docs/architecture/ADVI_ROLLUP_MASTER_WAVE.md</ref>
  </references>

  <context>
    BD sub-custody sleeve accounts (PCRA Trust, SWTC TTEE, retirement sleeves) carry
    ~$35-50M of real positions that never appear at gold grain because FIFO replay
    receives no Transfer In. Diagnostic case: Jones z0817905851 — silver/allocations
    $2.4M, gold/holdings_lots $82K, delta $2.31M.

    Fix concept: for sleeve accounts, seed opening lots from silver/unrealized before
    applying incremental FIFO. Same pattern as B_01's existing RPS synthetic lot
    injection. Extends _build_rps_synthetic_lots → _build_uln_sleeve_lots.

    Critical open question blocking Phase 1: silver/unrealized carries open_date,
    unit_cost, asset_id, cusip — but NOT quantity. Three candidate quantity sources
    (see PRD §"Critical open question"). Phase 0 must determine which is viable.

    Note on bandwidth: pick this up in your queue after DSFLOW.004 backfill +
    ADVI_STAUDT.COHORT-A + BDPL_CNPRCS.WP-10b are complete. Estimated: S (half day).
  </context>

  <scope>
    Phase 0 is a discovery + recommendation task. NO changes to gold scripts in this phase.
    Output is a brief findings doc + recommendation. Implementation begins in Phase 1.

    1. BD unrealized export audit — quantity source investigation:
       - Inspect the actual BD UGL unrealized export source upstream of silver/unrealized.
         Check: does BD's source workbook (or Silver ingest at C_* scripts) carry a Units
         column that is currently being dropped? Path: data/black_diamond/scripts/silver/
         or bronze — find the ingest for silver/unrealized.
       - If Units column is present in source but dropped on ingest: recommend Path (1)
         (add units to ingestion mapping — hours of work).
       - If BD source genuinely omits units: check adjacent BD feeds (ULT Taxable
         Unrealized, positions API if available). Document what's accessible.
       - If neither (1) nor (2) are viable: recommend Path (3) (inferred quantity from
         account_market_value / current_price apportionment, with quantity_source='inferred'
         flag). Document accuracy limits (breaks on rebalanced sleeves, CASH rows).

    2. `lib/sleeve_detect.py` — sleeve account classifier:
       - Build `is_sleeve_account(acct_row) -> bool` (requires ≥2 signals from):
           account_type IN ('IRA', '401K', '403B', 'ROTH_IRA')
           account_registration_type IN ('INVESTMENT_IRA', 'SIMPLE_IRA', 'PENSION_TRUST')
           account_number prefix: 'PCRA Trust', 'SWTC TTEE', or known sleeve codes
           portfolio_group: 'No Advisor' (supplementary, not required)
       - Conservative default: ≥2 signals = sleeve. Single-signal = non-sleeve.
       - Unit test: Jones z0817905851 must classify as sleeve.
       - Must begin with `from __future__ import annotations`.

    3. Cohort sizing — run classifier on latest allocations partition:
       - Load latest silver/allocations partition.
       - Apply `is_sleeve_account` to all accounts.
       - Compute: N_sleeve_accounts, aggregate_sleeve_AUA (from allocations), sum of
         (silver_AUA - gold_holdings_AUA) within sleeve cohort (the actionable gap).
       - Acceptance gate: sleeve cohort delta AUA between $30M and $60M (confirms
         match to observed ~$35-50M silver-gold recon gap from 2026-04-13 study).
       - Log result as a brief findings summary (markdown or JSON, either is fine).

    4. Recommendation document — MCP-ready summary:
       - State: which quantity source (1/2/3) is recommended and why.
       - If Path (1): cite which bronze/silver ingest script drops the Units column and
         what the fix scope is.
       - If Path (2): identify which adjacent BD feed and what new ingest project is required.
       - If Path (3): document accuracy limits + flag approach.
       - Cohort sizing result: N accounts, AUA delta, vs acceptance gate.
       - Any new sleeve registration types discovered beyond the four listed above.

    Do NOT touch B_01 gold script (Phase 1 scope).
    Do NOT build _build_uln_sleeve_lots (Phase 1 scope).
    Do NOT commit lib/sleeve_detect.py unless the unit test passes gate.
  </scope>

  <dependencies>
    <dependency agent="None" status="none" required="No upstream TOs for Phase 0."/>
  </dependencies>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Phase 0 is read-only analysis + lib file authoring. No gold/silver/bronze script
      changes in this phase. No reprocess required.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io B_01</run>
        <expect>READS list shows current B_01 inputs. silver/unrealized NOT yet in READS (expected — Phase 1 adds it). Confirms Phase 0 does not touch B_01. Document in session log.</expect>
        <if_mismatch>NOTE only. Phase 1 will add silver/unrealized read.</if_mismatch>
      </step>
      <step>
        <run>find data/black_diamond/scripts -name "*.py" | xargs grep -l "unrealized" 2>/dev/null</run>
        <expect>List of scripts that handle silver/unrealized. Identifies the ingest/bronze scripts to audit for Units column presence.</expect>
        <if_mismatch>NOTE only — expand search to silver/ and bronze/ if needed.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit (lib/sleeve_detect.py only)">
      <step>
        <run>python -m py_compile lib/sleeve_detect.py</run>
        <expect>Exit 0. No syntax errors.</expect>
        <if_mismatch>STOP. Fix syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh lib/sleeve_detect.py</run>
        <expect>Exit 0. py_compile + AST scan + ruff check all pass.</expect>
        <if_mismatch>STOP. Fix gate failures before committing.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>python -c "from lib.sleeve_detect import is_sleeve_account; print('IMPORT OK')"</run>
        <expect>Exit 0 + "IMPORT OK". Module importable from repo root.</expect>
        <if_mismatch>STOP. Fix import path before signaling.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <coordination agent="2.0.0_SA_COO" note="MCP COO on Phase 0 completion with: (a) quantity source recommendation (Path 1/2/3) + evidence, (b) cohort sizing result (N accounts + AUA delta), (c) commit hash for lib/sleeve_detect.py. COO relays recommendation to Andrew for Path decision. DO NOT begin Phase 1 implementation without explicit COO GO after Andrew confirms Path selection."/>
    <coordination agent="0.7.0_AE_CloudOps" note="If Path (2) is recommended (new BD feed ingestion), AE must be looped in to assess ingestion pipeline scope before Phase 1 begins. COO will route AE coordination when recommendation arrives."/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. BD unrealized export audited — quantity source (1/2/3) recommended with cited evidence.
    2. `lib/sleeve_detect.py` exists with `is_sleeve_account` function; imports cleanly; Jones z0817905851 classifies as sleeve.
    3. Cohort sizing result: N_sleeve_accounts, aggregate_sleeve_AUA, delta_AUA documented. Delta in [$30M, $60M] range.
    4. ds-commit-gate.sh exit 0 on lib/sleeve_detect.py.
    5. Session log includes compiler tools section: comp-pipescript io B_01 + unrealized ingest audit + py_compile results.
    6. MCP COO with recommendation summary + commit hash + cohort numbers.
    7. Phase 1 does NOT begin until explicit COO GO after Andrew confirms quantity source path.
  </acceptance_criteria>

  <evidence>
    <!-- To be filled by DS on completion -->
  </evidence>
</task_order>
