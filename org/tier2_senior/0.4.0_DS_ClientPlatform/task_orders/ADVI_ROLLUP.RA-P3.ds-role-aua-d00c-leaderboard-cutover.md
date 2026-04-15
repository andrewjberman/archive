<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-ra-p3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>pending</status><!-- ~B flipped 2026-04-15 21:43Z. CTO Rule 7 substitution APPROVED 21:43Z: parity vs canonical SOURCE (gold/canonical/role_aua/{latest}.parquet) instead of vs in-flight D_02 consumer. RA-P2 narrowed to snapshot L1277 only (RA-P2b deferred); cross-consumer convergence retargeted to Wave 4 closeout gate per CTO. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>RA-P3 (D_00c leaderboard consumer cutover)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #7, Phase 3)</ref>
    <ref type="ds_plan">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.RA-P2.ds-role-aua-d02-consumer-cutover.md (D_02 must be on canonical first — RA-P2 artifact provides the source)</ref>
    <ref type="consumer_memo">docs/data/role_aua_consumer_enumeration.md (P0 memo: D_00c `_build_at_role_slice` + `tagged_aua_counts` → leaderboard.json)</ref>
    <ref type="paired">ADVI_ROLLUP.CN-P3.ds-nna-atomic-d00c-leaderboard-cutover.md — paired D_00c cutover for nna_atomic</ref>
  </references>

  <objective>
    Phase 3 of 6. Cut over D_00c leaderboard's role-AUA aggregation to read from canonical
    `role_aua/{date}.parquet` instead of `_build_at_role_slice` + `tagged_aua_counts` filter+groupby
    logic.

    Cutover target (from P0 memo):
    - `D_00c._build_at_role_slice` + `tagged_aua_counts` → replace with `SELECT advisor, role, aua FROM role_aua WHERE date=...` pattern feeding `leaderboard.json`.

    Output parity: `platinum/firm/leaderboard.json` role-AUA values match RA canonical within $0.01,
    matches RA-P2 D_02 `summary.json` values for the same (advisor, role) keys.

    Remaining 3 sites (D_01, D_00b, C_08) are P4/P5.
  </objective>

  <wire_contract>
    D_00c leaderboard emits role-AUA from canonical. `platinum/firm/leaderboard.json` shape
    unchanged. Values match RA-P2 summary/book/timeseries within $0.01 by construction.
  </wire_contract>

  <acceptance_criteria>
    1. `_build_at_role_slice` + `tagged_aua_counts` call sites rewritten to read from role_aua canonical.
    2. `platinum/firm/leaderboard.json` Travis architect AUA matches `platinum/advisors/travis-penfield/summary.json` role_breakdown.architect within $0.01 (post RA-P2).
    3. `comp-validate role_aua --artifact /tmp/role_aua.parquet` exit 0.
    4. Zero-byte diff on all non-role fields of leaderboard.json.
    5. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    6. Acceptance-flex pre-flag rule (CTO Rule 7 locked 2026-04-15).
    7. MCP COMPLETE to COO with commit hash + Travis cross-consumer table (D_02 summary + D_00c leaderboard match).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_00c</run>
        <expect>Reads include `gold/canonical/role_aua/` post RA-P1+RA-P2 landing. Old inputs (account_team, advisor_fee_detail) still present for non-role code paths.</expect>
        <if_mismatch>If role_aua not in reads, RA-P1 shadow write hasn't landed — STOP.</if_mismatch>
      </step>
      <step>
        <run>grep -n '_build_at_role_slice\|tagged_aua_counts' data/black_diamond/scripts/gold/D_00c.advisor_summary.py</run>
        <expect>Both sites identified with file:line.</expect>
        <if_mismatch>Function rename since P0 memo — escalate.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_00c.advisor_summary.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>Diff leaderboard.json Travis architect AUA vs D_02 summary.json Travis architect AUA pre/post</run>
        <expect>Post-cutover: exact match within $0.01 across both consumers (cross-consumer schism closed).</expect>
        <if_mismatch>Schism persists — trace cutover gap before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast D_00c</run>
        <expect>Consumer set unchanged.</expect>
        <if_mismatch>Coordinate with DE/DT.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~D" task="ADVI_ROLLUP.RA-P1" status="pending" description="shadow must be producing"/>
    <dependency agent="0.4.0_DS_ClientPlatform~C" task="ADVI_ROLLUP.RA-P2" status="staged" description="D_02 must be on canonical first (cross-consumer parity target)"/>
    <dependency agent="co-phase" task="ADVI_ROLLUP.CN-P3" status="staged" description="paired D_00c NNA cutover; co-ship recommended"/>
  </dependencies>

  <next>
    On commit: COO authors RA-P4 (D_01 partner_analytics cutover, paired CN-P4).
  </next>
</task_order>
