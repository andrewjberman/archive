<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b8-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status><!-- GO sent 2026-04-14T21:30Z Wave A parallel dispatch -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 8: Fee Efficiency role-filter with rerank, N1)</ref>
  </references>

  <objective>
    Extend `FeeEfficiencyAdvisor` (`types.ts:1458-1476`) with per-role breakdown so the FE can
    rerank on a role slice (not just filter-hide):

    ```
    role_breakdown: Record<RoleKey, {
      aua: number
      nna: number
      commission: number
      fee_bps_weighted: number
      account_count: number
    }>
    ```

    RoleKey ∈ {architect, implementor, consultant, local_ops, additional_advisor}.
    Populated per window (QTD/YTD/1Y/3Y/Max) under `windows[win].advisors[]`.

    Synergy: B1 DS is adding `role_breakdown.{fee_paying,no_fee}` on D_00.leaderboard — same
    per-role accounting path, small incremental lift.
  </objective>

  <acceptance_criteria>
    1. fee_efficiency artifact has role_breakdown for all 5 role keys on every advisor row
    2. Populated per window (QTD/YTD/1Y/3Y/Max)
    3. Sum-reconciliation: with all 5 roles summed, metrics match existing top-level aggregates within $0.01 (aua/nna/commission) and exact for account_count
    4. MCP COMPLETE to COO with commit + S3 ETag + sample JSON showing role_breakdown on one advisor
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_00.leaderboard.py` (or whichever producer emits the fee_efficiency artifact); `comp-transform schema-check FeeEfficiencyPanel`; `comp-platinum reverse role_breakdown` within the fee_efficiency artifact (auto-rule: new platinum field); `comp-blast D_00.leaderboard` (new-field blast).
    Phase 2: `python -m py_compile`; `comp-validate` after rerun.
    Phase 3: Spot-check 3 advisors — role_breakdown populated, sum reconciliation holds.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>On COMPLETE: COO fires B8 FE TO.</next>
</task_order>
