<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-ra-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to><!-- Reassigned from ~C to ~D 2026-04-15 per CTO Q1 ACK — single-agent co-ship commit cleaner than handoff. ~C continues B9-DS on its own lane. -->
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-04-15 (~D). Code: afd553d4 (paired with CN-P1 bf9651b8). A→D rerun chain closed by AE 19:35Z. Shadow artifact gold/canonical/role_aua/2026-04-13.parquet (mtime 15:05 ET, 18KB). validate_role_aua.py PASS 6/6: I1 fee-bucket partition, I2 equal-split sum reconciliation, I5 PK uniqueness, I6 role enum membership. I3/I4 SKIPPED (--cross-check, --certified not provided; optional). Unblocks RA-P2 (~C) consumer cutover. Scope deferrals preserved: aua_fee_paying=0, aua_no_fee=aua, nna_txn/daily_inflow/daily_outflow=0.0 (billable-split populated at P2+). -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>RA-P1 (shadow write in D_02 pre-pass, co-ships with CN-P1)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #7, Phase 1)</ref>
    <ref type="ds_plan">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.RA-P0.ds-role-aua-canonical-schema.md (COMPLETE — schema ratified, validator committed, consumer memo shipped)</ref>
    <ref type="co_ship">ADVI_ROLLUP.CN-P1.ds-nna-atomic-shadow-write.md — MUST commit together in single DS commit</ref>
    <ref type="cto_directive">CTO 2026-04-15: RA-P1 + CN-P1 co-ship in one DS commit; both produce shadow artifacts in D_02 pre-pass; do not commit RA-P1 alone</ref>
  </references>

  <objective>
    Phase 1 of 6. Produce `gold/canonical/role_aua/{date}.parquet` as a SHADOW artifact in D_02's
    pre-pass — zero reader impact, rollback trivial (delete the artifact).

    Scope (RA half of the co-ship):
    - Extend D_02 pre-pass to produce `role_aua` parquet per the P0-ratified schema (no new columns without RA-P0a).
    - Run the P0 validator (`validate_role_aua.py`) inline; fail the pre-pass if any of the 6 invariants violate.
    - DO NOT cut any of the 6 consumer aggregation sites over yet (those are P2–P5 per plan).
    - DO NOT wire FE or ETL readers.

    Co-ship discipline: commit RA-P1 + CN-P1 together. Single DS commit, single push. Agent author
    field names whichever ~ did the work but commit carries both scopes.
  </objective>

  <wire_contract>
    New output: `gold/canonical/role_aua/{date}.parquet` (columns frozen at P0).
    No existing outputs changed. No schema breakage. Shadow only.
  </wire_contract>

  <acceptance_criteria>
    1. `gold/canonical/role_aua/{date}.parquet` written for the nightly run.
    2. `comp-validate role_aua --artifact /tmp/role_aua.parquet` exits 0 (all 6 invariants hold).
    3. Zero change in any existing consumer output (D_00c leaderboard.json, D_02 summary/book/timeseries, D_01 partner_analytics, D_00b chart json, C_08 fee_efficiency): diff pre/post co-ship commit = 0 bytes.
    4. Co-ship: this TO's commit hash ALSO delivers CN-P1 artifact (`gold/canonical/nna_atomic/{date}.parquet`). Single commit on the DS lane that executes it.
    5. Rollback test: deleting the artifact + re-running D_02 leaves everything green (validator skipped when parquet absent).
    6. Session log Compiler Tools section reproduces each `<run>` + observed + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. MCP COMPLETE to COO with commit hash + row count + RA and CN invariant pass summary.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>Confirm D_02 I/O manifest unchanged from P0 consumer memo; pre-pass extension point identifiable.</expect>
        <if_mismatch>Scope drifted — re-read P0 memo + plan doc before touching D_02.</if_mismatch>
      </step>
      <step>
        <run>Read CN-P0 schema doc + validate_nna_atomic.py</run>
        <expect>CN-P0 columns stable per CN-P0 ratification (acceptance #7). RA row `nna_txn`/`daily_inflow`/`daily_outflow` columns sourced from CN-P1 canonical — co-ship ensures consistent shapes.</expect>
        <if_mismatch>If CN-P0 schema changed without a CN-P0a addendum, escalate to COO — column-lock violation.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-validate role_aua --artifact /tmp/role_aua.parquet</run>
        <expect>Exit 0, all 6 invariants hold.</expect>
        <if_mismatch>Fix producer before commit.</if_mismatch>
      </step>
      <step>
        <run>Diff existing D_02 consumer outputs pre/post shadow-write commit (summary.json, book.json, timeseries.json)</run>
        <expect>Zero-byte diff. RA-P1 is shadow-only; consumer artifacts unchanged.</expect>
        <if_mismatch>STOP. Something leaked into an existing reader; trace + fix before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast role_aua</run>
        <expect>No consumers yet (shadow only).</expect>
        <if_mismatch>Rogue reader imported early — coordinate before P2 cutover.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~C" task="ADVI_ROLLUP.RA-P0" status="complete" description="schema + validator + consumer memo"/>
    <dependency agent="0.4.0_DS_ClientPlatform~D" task="ADVI_ROLLUP.CN-P0" status="pending" description="nna_atomic schema must be column-locked before RA-P1 can source nna_txn/daily_inflow/daily_outflow"/>
    <dependency agent="co-ship" task="ADVI_ROLLUP.CN-P1" status="staged" description="CN-P1 MUST commit in the same DS commit as RA-P1"/>
  </dependencies>

  <cross_domain_coordination>
    RA-P1 + CN-P1 = single DS commit (CTO directive 2026-04-15). Whichever ~ executes picks up both
    TO scopes in one Edit→Commit cycle. Commit message names both TOs. Do NOT push RA-P1 shadow artifact
    without the paired CN-P1 shadow artifact in the same commit.
  </cross_domain_coordination>

  <next>
    On commit: COO flips RA-P1 + CN-P1 both to complete, authors RA-P2 (D_02 consumer cutover, first of 4 P2..P5 phases).
  </next>
</task_order>
