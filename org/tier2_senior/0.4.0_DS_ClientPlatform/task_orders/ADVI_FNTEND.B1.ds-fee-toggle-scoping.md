<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b1-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>pending</status><!-- DS flipped 2026-04-14 after B2/B5 uploaded -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 1: A1+A2+A3)</ref>
  </references>

  <objective>
    Fee-toggle scoping contract on public profile.

    1. Extend `PlatinumLeaderboardEntry.fee_breakdown.{fee_paying, no_fee}` with `client_count`, `new_clients`, `account_count`.
    2. Extend `role_breakdown[role]` with `{fee_paying, no_fee}` sub-buckets of `{aua, nna, client_count, account_count}` (types.ts:1527 already anticipates).
    3. Reconcile Lifetime Activity timeseries: **PREFER option A — emit fee-bucketed `*_canonical` series** (option B pushes scaling onto FE and reintroduces drift risk per RD audit 2026-04-14). Option B (explicit reconciliation spec) only allowed if A infeasible.
  </objective>

  <acceptance_criteria>
    1. Platinum leaderboard artifact has all listed fields populated
    2. Role-breakdown subbucket sum reconciles to parent — **within $0.01 for aua/nna, exact for counts** (sharpened 2026-04-14 per CTO — matches reconciliation gate #4)
    3. Lifetime Activity series (option A preferred) OR reconciliation spec shipped
    4. **Reconciliation gate (added 2026-04-14 per RD audit):** at a given Window end, sum of Lifetime period diffs equals Summary.window values for the selected Fees bucket within $0.01 for each of NNA / Inflows / Outflows
    5. MCP COMPLETE to COO with commit + S3 ETag + sample JSON snippet
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_00.leaderboard.py` + `comp-pipescript consumers leaderboard`; `comp-blast D_00.leaderboard` (new-field blast); `comp-platinum reverse fee_breakdown` + `comp-platinum reverse role_breakdown` (new-platinum-field consumer enumeration).
    Phase 2: `python -m py_compile`; `comp-validate` after gold rerun.
    Phase 3: `comp-transform schema-check AdvisorPublicProfile` + `AdvisorBookView` — new fields typed + rendered.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>On COMPLETE: COO fires Bundle 1 FE TO.</next>
</task_order>
