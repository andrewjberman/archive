<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <id>2.0.0_SA_COO-2026-04-24-cannna-p2-d02-nna-reader-migration</id>
  <project>ADVI_CANNNA</project>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_to>0.4.0_DS_ClientPlatform</issued_to>
  <issued_date>2026-04-24</issued_date>
  <status>cancelled</status><!-- CANCELLED 2026-04-24 by 2.0.0_SA_COO. Work already complete at ebd737e3/b3f6b1ee (D_02 CN-P2 reader migration all 3 NNA sites on nna_atomic — done 2026-04-16 as part of CN WAVE TERMINAL). COO issued this TO without verifying actual D_02 implementation state; compiler graph showed old CANONICAL_NNA_PREFIX read (stale graph). DS confirmed all phases terminal before execution began. No DS cleanup required. -->

  <title>CANNNA Phase 2 — D_02 NNA reader migration to nna_atomic</title>

  <references>
    <ref type="prd">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
    <ref type="prd">docs/architecture/ADVI_ROLLUP_MASTER_WAVE.md</ref>
  </references>

  <context>
    Phase 0+1 complete: C_01 writes gold/canonical/nna_atomic/{date}.parquet (CN-P1
    shadow writer + CN-P1b bulk backfill in production since 2026-04-15). comp-validate
    nna_atomic rule in gold_validate_config.yaml. Five invariants enforced. Phase 2 is
    the first consumer-side migration: switch D_02 advisor_client_detail.py's three NNA
    aggregation sites from reading CANONICAL_NNA_PREFIX (gold/canonical/nna/) and
    account_performance to reading from canonical_nna_atomic_key. This closes the
    Travis three-panel NNA schism (summary vs timeseries vs role_breakdown).

    COO pre-TO compiler study (2026-04-24):
    - comp-pipescript io D_02: D_02 currently READs CANONICAL_NNA_PREFIX (old nna/ path)
      + ACCOUNT_PERFORMANCE. Does NOT read canonical_nna_atomic_key. Phase 2 adds this read.
    - comp-blast D_02: downstream consumers = IMPLEMENTOR_LEADERBOARD (terminal),
      advisor_mix_timeseries (terminal), canonical_role_aua (-> D_01), client_detail (-> D_04).
      No new consumers introduced by this TO.
    - D_02 ROLLING-WINDOW on canonical_role_aua_key: confirmed prior-run self-read pattern
      (Phase 1 shadow writer already in D_02). This TO does not touch the role_aua write path.
  </context>

  <scope>
    Switch three NNA aggregation sites in D_02.advisor_client_detail.py from their current
    read paths (CANONICAL_NNA_PREFIX + account_performance) to canonical_nna_atomic groupby:

    1. L576 — book-grain NNA per advisor/window:
       Current: reads from CANONICAL_NNA_PREFIX, groups by (advisor, window), computes
       cum_inflows - cum_outflows period diff.
       Target: groupby on nna_atomic where architect/implementor/etc == advisor, period window.
       Field: nna_atomic.nna_txn (daily) or cum_nna (cumulative).

    2. L1517 — timeseries NNA per (date, advisor):
       Current: reads account_performance cumulative columns, date-slices per advisor.
       Target: groupby nna_atomic on (date, architect==advisor) summing daily_inflow/
       daily_outflow/nna_txn. Cumulative = running sum over sorted date index.

    3. L1764 — role-scoped NNA per advisor/role/window:
       Current: mixed source (nna_txn from canonical_nna + role slot from account_team SCD).
       Target: groupby nna_atomic on (architect|implementor|consultant|local_ops|
       additional_advisor == advisor), per-role, window period. Full-credit convention:
       each role slot gets the full nna_txn of the account (per CANNNA PRD §integration
       with ADVI_ROLEAUA — no fractional split on flows).

    Do NOT touch the role_aua write path (canonical_role_aua_key — rolling-window shadow
    writer from Phase 1). Only the NNA read paths change. No changes to WRITES.
  </scope>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="CANNNA Phase 1"
                status="complete" required="C_01 nna_atomic shadow writer in production (CN-P1)"/>
  </dependencies>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>READS list includes canonical_nna_atomic_key (gold/canonical/nna_atomic/) after adding the import. No COLUMN GAPS on nna_atomic columns (date, account_id, daily_inflow, daily_outflow, nna_txn, cum_inflows, cum_outflows, cum_nna, architect, implementor, consultant, local_ops, additional_advisor, office, state, city, billable, is_excluded, is_ghost). WRITES unchanged from pre-edit baseline.</expect>
        <if_mismatch>STOP. If COLUMN GAPS listed for nna_atomic columns, the canonical schema in lib/s3_layout.py or the nna_atomic parquet does not expose the column — surface to COO before writing consumer code.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_02</run>
        <expect>Downstream: IMPLEMENTOR_LEADERBOARD (terminal), advisor_mix_timeseries (terminal), canonical_role_aua (-> D_01), client_detail (-> D_04). No new downstream nodes vs pre-edit baseline.</expect>
        <if_mismatch>STOP. New consumer appeared mid-flight — message its owning agent before committing.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse 'gold/entities/advisors/*/book.json'</run>
        <expect>Consumer list surfaces the advisor intelligence portal component. Document which FE component(s) render advisor book NNA — this confirms the schism-fix reaches the portal.</expect>
        <if_mismatch>NOTE only (not a blocker). Log consumer list in session log Compiler Tools section.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile D_02.advisor_client_detail.py</run>
        <expect>Exit 0. No syntax errors.</expect>
        <if_mismatch>STOP. Fix syntax before committing.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>Exit 0. py_compile + AST scan + ruff check all pass.</expect>
        <if_mismatch>STOP. Fix all gate failures before committing.</if_mismatch>
      </step>
      <step>
        <run>comp-validate nna_atomic --artifact /tmp/nna_atomic_{latest_date}.parquet</run>
        <expect>Exit 0. All 5 invariants pass: daily identity, cumulative identity, timeline consistency, cross-cohort additivity, fee partition. WARN count documented in session log.</expect>
        <if_mismatch>STOP. Do not commit until all ERROR checks pass. Surface invariant failures to COO.</if_mismatch>
      </step>
      <step>
        <run>Per-advisor NNA reconciliation spot-check (at least 3 advisors from latest D_02 output): summary.nna vs timeseries.period_nna(window) vs sum(role_breakdown[*].nna)</run>
        <expect>All three agree within $0.01 per advisor per window. Document spot-check advisor IDs + values in session log.</expect>
        <if_mismatch>STOP. The three-panel schism is NOT closed. Surface disagreement details to COO with advisor ID + delta.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast D_02</run>
        <expect>Same consumer set as Phase 1 check. No new downstream nodes appeared during write.</expect>
        <if_mismatch>Surface to COO. Another agent may have committed a new consumer mid-flight.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed D_02</run>
        <expect>MATCH — runner has your committed code before triggering gold run.</expect>
        <if_mismatch>STOP. Upload to S3 before triggering. Stale runner = wrong results.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>
      D_02 reads from gold-tier artifacts (nna_atomic, account_performance, role_aua) —
      not silver or bronze. No silver/bronze reprocess required. D_02's output artifacts
      (advisor book.json, timeseries.json, client_detail.json) will update on the next
      gold run automatically. D_01 reads canonical_role_aua from D_02 — the role_aua
      write path is unchanged by this TO, so D_01 is unaffected.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    <coordination agent="0.4.0_DS_ClientPlatform~A" note="ADVI_INFLEC lanes use D_02 (I_D02). Coordinate commit timing — do not merge during active INFLEC W4.13b gold chain run. MCP DS~A when committing to confirm no in-flight INFLEC chain conflict."/>
    <coordination agent="2.0.0_SA_COO" note="MCP COO on Phase 2 commit with acceptance evidence before signaling DE for portal validation. COO relays to DE 0.4.0 for AdvisorsTab frontend-dev check on NNA panel convergence."/>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. D_02 NNA aggregation at L576 (book), L1517 (timeseries), L1764 (role) reads from
       canonical_nna_atomic instead of CANONICAL_NNA_PREFIX / account_performance.
    2. comp-pipescript io D_02 Phase 1 run logged in session Compiler Tools section with
       READS including canonical_nna_atomic_key — PASS confirmed.
    3. comp-blast D_02 pre- and post-commit logged — consumer set unchanged.
    4. comp-validate nna_atomic exit 0 — all 5 invariants PASS — logged in session Compiler
       Tools section with WARN count.
    5. Per-advisor spot-check: at least 3 advisors verified: summary.nna == timeseries.nna
       == sum(role_breakdown.nna) within $0.01 per window. Advisor IDs + values documented.
    6. Session log includes Compiler Tools section reproducing every run from
       compiler_tools_mandate with observed output and explicit pass/fail vs expect.
       Missing rows = REWORK.
    7. ds-commit-gate.sh exit 0 on D_02 file before commit.
    8. comp-pipescript deployed D_02 shows MATCH before any gold run trigger.
    9. MCP COO on completion with commit hash + spot-check evidence.
  </acceptance_criteria>

  <evidence>
    <!-- To be filled by DS on completion -->
  </evidence>
</task_order>
