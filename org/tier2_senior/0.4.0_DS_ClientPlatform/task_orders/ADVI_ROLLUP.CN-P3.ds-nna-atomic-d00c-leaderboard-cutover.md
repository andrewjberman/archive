<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-cn-p3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>staged</status><!-- ~B HELD 2026-04-15 21:50Z per CTO Path 1 APPROVED. Hard blocker: nna_atomic has 1 partition (2026-04-13) vs nna's 2294 partitions back to ~2018. D_00c multi-window aggregations (3M..MAX) would collapse to single-day sums. CTO assigned CN-P1b backfill TO authoring to COO for ~D dispatch. CN-P3 re-fires under same substituted parity (vs canonical SOURCE) once CN-P1b validator PASSES (partition count ≥ legacy nna/ + 90-day spot-check parity). Local D_00c CN-side edit reverted; not committed. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>CN-P3 (D_00c NNA consumer cutover — pairs with RA-P3)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #8, Phase 3)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.CN-P2.ds-nna-atomic-d02-consumer-cutover.md</ref>
    <ref type="consumer_memo">docs/data/nna_atomic_consumer_enumeration.md (P3 = D_00c scope per 93b70620)</ref>
    <ref type="paired">ADVI_ROLLUP.RA-P3.ds-role-aua-d00c-leaderboard-cutover.md — co-ship recommended</ref>
  </references>

  <objective>
    Phase 3 of 6. Cut D_00c's NNA aggregation sites to read from canonical `nna_atomic/{date}.parquet`.
    Per CN-P0 consumer memo, P3 = D_00c scope — exact sites in the memo. Leaderboard NNA aggregates
    + any cumulative-flow paths in D_00c.

    Output parity: `platinum/firm/leaderboard.json` NNA values match canonical within $0.01 and
    match CN-P2 D_02 values for the same (advisor) keys — cross-consumer NNA schism closed here at
    the leaderboard grain.

    Remaining sites (D_01, D_00b/D_00, rest) are P4/P5.
  </objective>

  <wire_contract>
    D_00c NNA emits from canonical. leaderboard.json shape unchanged. NNA values match CN-P2
    summary values within $0.01.
  </wire_contract>

  <acceptance_criteria>
    1. D_00c NNA sites (per consumer memo) read from nna_atomic canonical.
    2. Travis NNA: leaderboard.json matches D_02 summary.json within $0.01.
    3. `comp-validate nna_atomic --artifact /tmp/nna_atomic.parquet` exit 0.
    4. Zero-byte diff on non-NNA fields of leaderboard.json.
    5. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    6. Acceptance-flex pre-flag rule (CTO Rule 7).
    7. MCP COMPLETE to COO with commit hash + cross-consumer NNA match table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_00c</run>
        <expect>Reads include nna_atomic canonical post CN-P1+P2.</expect>
        <if_mismatch>CN-P1/P2 not landed — STOP.</if_mismatch>
      </step>
      <step>
        <run>Read P0 consumer memo for D_00c NNA site list</run>
        <expect>File:line inventory of D_00c NNA aggregation paths.</expect>
        <if_mismatch>Memo missing P3 scope — escalate.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_00c.advisor_summary.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>Diff leaderboard NNA vs D_02 summary NNA (Travis) pre/post cutover</run>
        <expect>Post: exact match within $0.01.</expect>
        <if_mismatch>Schism persists — trace.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast D_00c</run>
        <expect>Consumer set unchanged.</expect>
        <if_mismatch>Coordinate.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~D" task="ADVI_ROLLUP.CN-P1" status="pending"/>
    <dependency agent="0.4.0_DS_ClientPlatform~D" task="ADVI_ROLLUP.CN-P2" status="staged" description="D_02 NNA cutover must land first (cross-consumer parity target)"/>
    <dependency agent="co-phase" task="ADVI_ROLLUP.RA-P3" status="staged" description="paired D_00c role cutover; co-ship recommended"/>
  </dependencies>

  <next>
    On commit: COO authors CN-P4 (D_01 partner_analytics NNA cutover, paired RA-P4).
  </next>
</task_order>
