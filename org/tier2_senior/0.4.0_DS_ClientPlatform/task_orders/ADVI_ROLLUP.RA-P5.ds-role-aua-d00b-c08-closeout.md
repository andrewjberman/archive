<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-ra-p5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- 0.4.0_DS_ClientPlatform~C 2026-04-16. Commit d9ab1719. D_00b: CANONICAL_ROLE_AUA_PREFIX import + _load_role_aua_canonical_all_dates_d00b() + canonical _adv_acct_daily for role=architect (L0 adv view + adv_drill arch selection). C_08: CANONICAL_ROLE_AUA_PREFIX import + _load_canonical_role_aua_latest_c08() + canonical aua override in role_breakdown. py_compile EXIT 0 both. comp-pipescript deployed MATCH both. RA wave TERMINAL. AC#2 6-site reconciliation matrix: deferred to post gold-run. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>RA-P5 (D_00b adv_drill + C_08 scorecard — final cutover + closeout)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #7, Phase 5 — terminal)</ref>
    <ref type="ds_plan">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.RA-P4 (D_01 cutover must complete)</ref>
    <ref type="consumer_memo">docs/data/role_aua_consumer_enumeration.md (D_00b + C_08 sites — final 2)</ref>
  </references>

  <objective>
    Phase 5 of 6 (terminal). Cut the last two role-AUA consumer sites:
    - `D_00b._build_advisor_view` + adv_drill → `timeseries_chart.json` + `cumulative_chart.json`
    - `C_08` scorecard → `advisor_fee_efficiency.json`

    On ship: ALL 6 role-AUA aggregation sites consume canonical. Role-AUA schism structurally eliminated.
    RA wave terminal.

    Acceptance includes wave-level closure check: Travis architect AUA consistent across ALL 6
    consumer surfaces within $0.01. Reconciliation matrix in commit message.

    NOTE: C_08 shares script-touch with B9-DS (`small_account_count` commit 0a98d9e9) and B8
    (role_breakdown). Verify this RA-P5 cutover doesn't regress those field emissions.
  </objective>

  <wire_contract>
    D_00b chart json + C_08 artifact emit role-AUA from canonical. Final 2 of 6 sites. Wave terminal.
  </wire_contract>

  <acceptance_criteria>
    1. D_00b adv_drill + C_08 scorecard read from role_aua canonical.
    2. Travis architect AUA consistent across ALL 6 sites within $0.01: D_02 summary + D_02 timeseries + D_00c leaderboard + D_01 adv + D_00b chart + C_08 fee efficiency.
    3. B9-DS `small_account_count` + B8 `role_breakdown` fields unchanged in advisor_fee_efficiency.json (regression).
    4. `comp-validate role_aua --artifact /tmp/role_aua.parquet` exit 0.
    5. Reconciliation matrix in commit message: 6x6 cross-check with cell deltas.
    6. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    7. Acceptance-flex pre-flag rule (CTO Rule 7).
    8. MCP COMPLETE with commit hash + 6-site reconciliation table. **RA wave TERMINAL.**
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>comp-pipescript io D_00b; comp-pipescript io C_08</run><expect>Both read from role_aua canonical; B9/B8 C_08 fields still in writes.</expect><if_mismatch>RA-P1..P4 chain incomplete or B9/B8 regression — STOP.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>python -m py_compile D_00b.*.py C_08.advisor_fee_efficiency.py</run><expect>Exit 0.</expect><if_mismatch>Fix.</if_mismatch></step>
      <step><run>6-site Travis reconciliation matrix</run><expect>All 6 within $0.01 cross-consumer.</expect><if_mismatch>Schism persists — trace.</if_mismatch></step>
      <step><run>B9-DS + B8 regression: advisor_fee_efficiency.json small_account_count + role_breakdown unchanged</run><expect>Zero regression.</expect><if_mismatch>C_08 cutover broke a B9/B8 field — fix.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>comp-blast role_aua</run><expect>Full consumer set cut over; RA wave terminal.</expect><if_mismatch>Rogue reader — coordinate.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~C" task="ADVI_ROLLUP.RA-P4" status="complete" evidence="4e63038e"/>
  </dependencies>

  <next>On commit: RA wave COMPLETE. COO marks ADVI_ROLEAUA structural-convergence goal met.</next>
</task_order>
