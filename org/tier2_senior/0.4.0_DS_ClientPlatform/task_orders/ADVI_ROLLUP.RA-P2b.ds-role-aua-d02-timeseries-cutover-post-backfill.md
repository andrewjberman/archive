<task_order>
  <metadata>
    <id>ADVI_ROLLUP.RA-P2b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- 0.4.0_DS_ClientPlatform~C 2026-04-16. Commit 94600ff6. Added CANONICAL_ROLE_AUA_PREFIX import + _load_role_aua_canonical_all_dates() + replaced role_ts_lookup/fee/nofee builder (L1740-1775) with canonical all-dates load + local-compute fallback. py_compile EXIT 0. comp-blast terminal. comp-pipescript deployed MATCH. S3: opal-data-bd/code/gold/D_02.advisor_client_detail.py. AC#3-5 Travis + 5-date spot-check: deferred to post gold-run (same run as CN-P3 AC#2). -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>4 (Structural convergence)</wave>
    <priority>P1 (closes RA-P2 deferred scope; gates Wave 4 convergence gate)</priority>
  </metadata>

  <references>
    <ref type="trigger">CTO ACCEPTANCE FLEX 2026-04-15 21:39Z + ~C completion of RA-P2 snapshot-only (commit 0c06d423)</ref>
    <ref type="prereq">ADVI_ROLLUP.RA-P1b — historical backfill of canonical role_aua per-date</ref>
    <ref type="parent">ADVI_ROLLUP.RA-P2 — snapshot-only D_02 cutover (L1289 only) (commit 0c06d423)</ref>
    <ref type="prd">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
  </references>

  <objective>
    Complete the deferred D_02 timeseries cutover at L1632-1655 (`build_advisor_timeseries.role_ts_lookup`). Per-date canonical read of `gold/canonical/role_aua/{YYYY-MM-DD}.parquet` replacing legacy local-compute path.

    Note: line refs may have shifted post-RA-P2 commit (0c06d423). Re-locate via `grep -n role_ts_lookup` before editing.

    Single-lane on D_02.advisor_client_detail.py — coordinate with ~D's CN-P2 follow-on if any in flight. ~C natural fit (lane match — owns RA-P2 snapshot work, knows the L1289 helper inserted there).
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</file>
    </files>
  </scope>

  <wire_contract>
    `summary.timeseries.role_breakdown.architect.aua` data array now sourced from per-date canonical role_aua parquet read instead of legacy local-compute. Expected behavior: equal-split semantics applied per-date; closes the three-way schism on Travis Penfield (snapshot ✓ via RA-P2, leaderboard ✓ via RA-P3, timeseries ✓ via this TO).
  </wire_contract>

  <acceptance_criteria>
    1. L1632-1655 region (or its post-shift equivalent) reads from `gold/canonical/role_aua/` per-date instead of local compute.
    2. `_load_canonical_role_aua_per_date` (or analogous helper) added if not already present from RA-P2.
    3. `git commit --only --` scoped to D_02.advisor_client_detail.py.
    4. Travis Penfield three-way convergence verified post-nightly D_02 run: summary.role_breakdown.architect.aua == timeseries.architect_aua data[-1] == leaderboard architect.aua, all within $0.01.
    5. Spot-check parity: `timeseries.architect_aua` historical data points (5 sample dates) match canonical role_aua per-date sums within $0.01 OR documented divergence.
    6. Rule 7 pre-flag if any acceptance flex.
    7. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    8. MCP COMPLETE to COO + CTO with commit hash + Travis convergence table + spot-check parity table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>grep -n 'role_ts_lookup\|build_advisor_timeseries' data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>Function visible; line refs identified post-RA-P2 shift.</expect>
        <if_mismatch>If function renamed or removed, surface to COO before proceeding.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/canonical/role_aua/ | wc -l</run>
        <expect>Partition count from RA-P1b backfill (≥ window-required count).</expect>
        <if_mismatch>RA-P1b not closed — STOP. Cannot proceed without backfill.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>READS includes `gold/canonical/role_aua/` post-RA-P2; this TO extends per-date read pattern.</expect>
        <if_mismatch>If READS missing canonical, RA-P2 may not have shipped — verify.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>{D_02 dry-run for Travis Penfield, output role_ts_lookup result for last 5 dates}</run>
        <expect>Per-date values populated, non-zero, equal-split semantics applied.</expect>
        <if_mismatch>Investigate per-date read.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit + nightly D_02 run">
      <step>
        <run>{compare Travis Penfield three-way: summary vs timeseries[-1] vs leaderboard}</run>
        <expect>All three within $0.01.</expect>
        <if_mismatch>Three-way schism unresolved — surface to CTO+COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency to="ADVI_ROLLUP.RA-P1b" description="Historical backfill must complete + validator PASS" status="complete" evidence="c962ddb3"/>
  </dependencies>

  <next>
    RA-P2b close + RA-P3 close + CN-P3 close (post-CN-P1b backfill) + CN-P4 close → unblocks Wave 4 convergence gate (W4-CG).
  </next>
</task_order>
