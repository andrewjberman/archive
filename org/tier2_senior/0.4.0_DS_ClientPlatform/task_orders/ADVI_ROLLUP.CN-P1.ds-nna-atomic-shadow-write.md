<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-cn-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-04-15 (~D). Code: bf9651b8 (paired with RA-P1 afd553d4). A→D rerun chain closed by AE 19:35Z. Shadow artifact gold/canonical/nna_atomic/2026-04-13.parquet (mtime 14:42 ET, 9,559 rows). validate_nna_atomic.py PASS: INV1 daily identity, INV2 cumulative identity, INV4 firm aggregates (daily_inflow=$4.01M, daily_outflow=$9.16M, nna_txn=-$5.15M consistent), INV5 fee partition. INV3 SKIPPED (no --prior-artifact). Unblocks CN-P2 (~D) consumer cutover. Scope deferrals preserved: billable/is_excluded/is_ghost populated at P2+. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>CN-P1 (shadow write in C_01, co-ships with RA-P1)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #8, Phase 1)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.CN-P0.ds-nna-canonical-schema.md (must complete first)</ref>
    <ref type="co_ship">ADVI_ROLLUP.RA-P1.ds-role-aua-shadow-write.md — MUST commit together in single DS commit</ref>
    <ref type="cto_directive">CTO 2026-04-15: RA-P1 + CN-P1 co-ship in one DS commit; both produce shadow artifacts in D_02 pre-pass; do not commit CN-P1 alone</ref>
    <ref type="supersedes">GEO 3-way NNA point fix (PRD item #4) — CANNNA eliminates the schism class structurally</ref>
  </references>

  <objective>
    Phase 1 of 6. Produce `gold/canonical/nna_atomic/{date}.parquet` as a SHADOW artifact written
    by C_01 — zero reader impact, rollback trivial (delete artifact).

    Scope (CN half of the co-ship):
    - Extend C_01 to produce `nna_atomic` parquet per the P0-ratified schema (no new columns without CN-P0a).
    - Run the P0 validator (`validate_nna_atomic.py`) inline; fail the pre-pass if any of the 5 invariants violate.
    - DO NOT cut any of the 12 consumer aggregation sites over yet (those are P2–P5 per plan).
    - DO NOT wire FE or ETL readers.

    Co-ship discipline: commit RA-P1 + CN-P1 together. Single DS commit on whichever ~ executes,
    commit message names both TOs.
  </objective>

  <wire_contract>
    New output: `gold/canonical/nna_atomic/{date}.parquet` (columns frozen at CN-P0).
    No existing outputs changed. Shadow only.
  </wire_contract>

  <acceptance_criteria>
    1. `gold/canonical/nna_atomic/{date}.parquet` written for the nightly run.
    2. `comp-validate nna_atomic --artifact /tmp/nna_atomic.parquet` exits 0 (all 5 invariants hold).
    3. Zero change in any existing consumer output (C_01/D_00/D_00b/D_00c/D_01/D_02): diff pre/post co-ship commit = 0 bytes.
    4. Co-ship: this TO's commit hash ALSO delivers RA-P1 artifact (`gold/canonical/role_aua/{date}.parquet`).
    5. Rollback test: deleting the artifact + re-running C_01 leaves everything green (validator skipped when parquet absent).
    6. Session log Compiler Tools section reproduces each `<run>` + observed + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. MCP COMPLETE to COO with commit hash + row count + RA and CN invariant pass summary.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io C_01</run>
        <expect>Confirm C_01 I/O manifest matches CN-P0 consumer memo; C_01 extension point identifiable for nna_atomic emit.</expect>
        <if_mismatch>Scope drifted — re-read P0 memo before touching C_01.</if_mismatch>
      </step>
      <step>
        <run>Read CN-P0 validator (validate_nna_atomic.py) and confirm 5 invariants wired</run>
        <expect>All 5 invariants implemented per plan doc (nna_txn = daily_inflow - daily_outflow, cum consistency, timeline consistency, cross-cohort additivity, fee-partition preservation).</expect>
        <if_mismatch>Validator incomplete — coordinate with CN-P0 author before shadow write.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate nna_atomic --artifact /tmp/nna_atomic.parquet</run>
        <expect>Exit 0, all 5 invariants hold on a sample day.</expect>
        <if_mismatch>Fix C_01 emit logic before commit.</if_mismatch>
      </step>
      <step>
        <run>Diff existing C_01 + downstream consumer outputs pre/post co-ship commit</run>
        <expect>Zero-byte diff. CN-P1 is shadow-only; no consumer change.</expect>
        <if_mismatch>STOP. Something leaked into an existing reader; trace + fix before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast nna_atomic</run>
        <expect>No consumers yet (shadow only).</expect>
        <if_mismatch>Rogue reader imported early — coordinate before P2 cutover.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~D" task="ADVI_ROLLUP.CN-P0" status="pending" description="schema + validator + consumer memo must be ratified before shadow emit"/>
    <dependency agent="co-ship" task="ADVI_ROLLUP.RA-P1" status="staged" description="RA-P1 MUST commit in the same DS commit as CN-P1"/>
  </dependencies>

  <cross_domain_coordination>
    RA-P1 + CN-P1 = single DS commit (CTO directive 2026-04-15). Whichever ~ executes picks up both
    TO scopes in one Edit→Commit cycle. Commit message names both TOs. Do NOT push CN-P1 shadow artifact
    without the paired RA-P1 shadow artifact in the same commit.
  </cross_domain_coordination>

  <next>
    On commit: COO flips CN-P1 + RA-P1 to complete, authors CN-P2 (first consumer cutover: D_02
    summary/book to read from nna_atomic, paired with RA-P2 D_02 cutover).
  </next>
</task_order>
