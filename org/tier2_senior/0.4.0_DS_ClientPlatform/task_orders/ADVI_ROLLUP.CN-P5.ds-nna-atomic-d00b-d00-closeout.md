<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-cn-p5</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- auto-dispatch 20260416T170353Z operator.py --dispatch. COMPLETE 2026-04-16 by 0.4.0_DS_ClientPlatform~D. Commit 49eac17d on CLOUD: D_00b/D_00/D_04/C_08 CANONICAL_NNA_PREFIX -> CANONICAL_NNA_ATOMIC_PREFIX. All 4 scripts py_compile OK. CN WAVE TERMINAL -- all consumer scripts on nna_atomic. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>CN-P5 (D_00b / D_00 remaining NNA — terminal cutover)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #8, Phase 5 — terminal)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.CN-P4 (D_01 cutover must complete)</ref>
    <ref type="consumer_memo">docs/data/nna_atomic_consumer_enumeration.md (P5 = remaining sites)</ref>
  </references>

  <objective>
    Phase 5 of 6 (terminal). Cut all remaining NNA consumer sites per CN-P0 consumer memo — D_00b
    adv_drill (timeseries_chart.json + cumulative_chart.json) + D_00 firm timeseries + any straggler
    NNA aggregates in C_02/C_03/C_08.

    On ship: ALL ~25 NNA aggregation sites across 10 scripts consume canonical nna_atomic. All
    latent NNA schismata structurally eliminated. CN wave terminal.

    Acceptance includes wave-level closure check: Travis NNA across ALL consumer surfaces within
    $0.01 + firm-level NNA additivity invariant (Invariant #4 from CN-P0 validator) passes on
    the complete consumer cutover.
  </objective>

  <wire_contract>
    All NNA consumer sites cut over. CN wave terminal. nna_atomic is the single source of NNA truth
    for every downstream consumer.
  </wire_contract>

  <acceptance_criteria>
    1. All remaining P5 sites (D_00b + D_00 + stragglers per memo) read from nna_atomic canonical.
    2. Travis NNA consistent across ALL consumer surfaces (D_02 summary, D_00c leaderboard, D_01 partner_analytics, D_00b chart, D_00 firm timeseries, C_*) within $0.01.
    3. Firm-level NNA additivity invariant #4 passes on complete cutover (sum_{account} daily_inflow at date = firm daily_inflow).
    4. `comp-validate nna_atomic --artifact /tmp/nna_atomic.parquet` exit 0.
    5. Reconciliation matrix in commit message: all consumer sites cross-check.
    6. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    7. Acceptance-flex pre-flag rule (CTO Rule 7).
    8. MCP COMPLETE with commit hash + full consumer reconciliation. **CN wave TERMINAL.**
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>comp-pipescript io D_00b; comp-pipescript io D_00</run><expect>Both read from nna_atomic canonical.</expect><if_mismatch>CN-P1..P4 chain incomplete — STOP.</if_mismatch></step>
      <step><run>Read CN-P0 memo for P5 straggler site list</run><expect>Every remaining site inventoried with file:line.</expect><if_mismatch>Memo incomplete — escalate.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>python -m py_compile D_00b.*.py D_00.*.py</run><expect>Exit 0.</expect><if_mismatch>Fix.</if_mismatch></step>
      <step><run>Firm-level additivity check: sum_{account} daily_inflow at 2026-04-15 == firm daily_inflow within $0.01</run><expect>Invariant #4 PASS on complete cutover.</expect><if_mismatch>Invariant broken — trace.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>comp-blast nna_atomic</run><expect>All ~25 sites cut over; CN wave terminal.</expect><if_mismatch>Rogue reader — coordinate.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~B" task="ADVI_ROLLUP.CN-P4" status="complete" evidence="4e63038e"/>
  </dependencies>

  <next>On commit: CN wave COMPLETE. COO marks ADVI_CANNNA structural-convergence goal met. GEO 3-way, Travis 3-way, architect 3-way — ALL schismata eliminated by construction.</next>
</task_order>
