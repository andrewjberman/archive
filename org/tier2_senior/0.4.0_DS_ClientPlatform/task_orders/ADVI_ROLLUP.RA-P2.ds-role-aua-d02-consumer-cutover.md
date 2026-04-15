<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-ra-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-15</date>
    <status>pending</status><!-- RA-P1 landed afd553d4 (shadow artifact live 2026-04-13 parquet, validator 6/6 PASS per ~D). CN-P1 landed bf9651b8. COO GO 20:06Z. Rule 7 pre-flag on Option 1 (narrow P2 scope, respect P1 billable-split deferrals) APPROVED by COO 20:12Z + acknowledged by CTO 20:18Z. Coord with ~D on D_02 simultaneous edit locked at 20:08Z. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>RA-P2 (D_02 consumer cutover — first of 4 cutover phases)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #7, Phase 2)</ref>
    <ref type="ds_plan">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.RA-P1.ds-role-aua-shadow-write.md (must ship first — shadow artifact must be producing)</ref>
    <ref type="consumer_memo">docs/data/role_aua_consumer_enumeration.md (P0 memo identifies 2 of 6 D_02 aggregation sites)</ref>
    <ref type="paired">ADVI_ROLLUP.CN-P2.ds-nna-atomic-d02-consumer-cutover.md — paired D_02 cutover for nna_atomic; ships serially or together per CTO direction at P1 review</ref>
  </references>

  <objective>
    Phase 2 of 6. Cut over D_02's two role-AUA aggregation sites to read from `gold/canonical/role_aua/{date}.parquet`
    (shipped as shadow artifact in RA-P1).

    Cutover targets (from P0 consumer memo):
    1. `D_02.build_advisor_books` role_breakdown at L1269 → replace filter+groupby logic with `SELECT advisor, role, aua FROM role_aua WHERE date=...` pattern.
    2. `D_02.build_advisor_timeseries` role_ts_lookup at L1619 → same pattern, per-date iteration.

    Output parity gate: `platinum/advisors/{*}/summary.json` role_breakdown + `platinum/advisors/{*}/timeseries.json` role_ts values must match RA-P1 shadow artifact within $0.01. If the old (filter-stack-diverged) output and the new (canonical) output disagree beyond $0.01, the canonical is correct per P0 ratification — document the delta.

    Remaining 4 sites (D_00c leaderboard, D_01 adv view, D_00b adv_drill, C_08 scorecard) are P3/P4/P5.
    DO NOT touch them in this TO.
  </objective>

  <wire_contract>
    D_02 role-breakdown + role-ts emit from canonical. Downstream `platinum/advisors/{*}/*.json`
    shapes unchanged — same keys, same types. Only numeric values may shift where the old filter
    stack produced a different aggregate. Expected: Travis architect row matches canonical across
    summary + timeseries (no more ~0.5% drift).
  </wire_contract>

  <acceptance_criteria>
    1. L1269 role_breakdown reads from role_aua canonical, not re-computed from account_team + advisor_fee_detail.
    2. L1619 role_ts_lookup reads from role_aua canonical.
    3. Dry-run spot-check: Travis Cobb architect AUA matches across `summary.json` + `timeseries.json` + `leaderboard.json` within $0.01 (NOTE: leaderboard not yet cut over at P2, so initial delta is expected — record magnitude).
    4. `comp-validate role_aua --artifact /tmp/role_aua.parquet` exits 0 on the nightly run feeding this cutover.
    5. Zero-byte diff on ALL non-role D_02 outputs (books, summary non-role-breakdown fields, etc.) — the cutover is scope-limited to role aggregation paths only.
    6. Session log Compiler Tools section reproduces each `<run>` + observed + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. **Acceptance-flex pre-flag rule (CTO locked 2026-04-15):** any deviation from acceptance criteria requires MCP heads-up to CTO BEFORE accepting + closeout citation of original `<expect>` vs. substituted observation.
    8. MCP COMPLETE to COO with commit hash + Travis spot-check table + magnitude of any non-role artifact delta (should be 0).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>D_02 reads include `gold/canonical/role_aua/` (post RA-P1 shadow write); old filter-stack inputs (account_team, advisor_fee_detail) still present but only for non-role code paths.</expect>
        <if_mismatch>If role_aua not in reads, RA-P1 shadow write hasn't landed yet — STOP and coordinate.</if_mismatch>
      </step>
      <step>
        <run>grep -n 'role_breakdown\|role_ts_lookup' data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>Two callsites identified at approximately L1269 + L1619 (exact line numbers may shift from consumer memo; confirm both still present).</expect>
        <if_mismatch>Scope drifted since P0 memo; re-read D_02 and update cutover targets before write.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_02 --artifact /tmp/platinum_sample.json</run>
        <expect>Exit 0; role-breakdown + role-ts populated from canonical; non-role fields unchanged.</expect>
        <if_mismatch>Iterate until validator clean.</if_mismatch>
      </step>
      <step>
        <run>Diff platinum/advisors/{travis-penfield}/summary.json pre/post cutover — non-role fields only</run>
        <expect>Zero-byte diff on non-role fields (books, aua, fees, etc.).</expect>
        <if_mismatch>Scope bled into non-role paths; STOP and trace.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast D_02</run>
        <expect>Downstream consumer set unchanged; no new reader introduced.</expect>
        <if_mismatch>Coordinate with DE/DT before signaling complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.RA-P1" status="staged" description="shadow artifact must be producing before consumer cutover"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.CN-P1" status="staged" description="nna_txn / daily_inflow / daily_outflow columns in role_aua sourced from nna_atomic; both shadows must be live"/>
  </dependencies>

  <next>
    On commit: COO authors RA-P3 (D_00c leaderboard cutover, paired with CN-P3). D_02 cutover is the
    highest-risk blast radius — P3/P4/P5 are incrementally narrower.
  </next>
</task_order>
