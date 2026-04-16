<task_order>
  <metadata>
    <id>ADVI_ROLLUP.RA-P1c</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>staged</status><!-- Authored by 2.0.0_SA_COO per CTO directive 2026-04-16T18:03Z. Non-blocking deferred TO — does not hold Wave 4 close. Gates on tonight CN-P1b PROD nightly confirmation. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>RA-P1c (role_aua flow column repopulation — nna_txn deferred fix)</phase_label>
    <priority>P3 (non-blocking; Wave 4 closed; deferred to post-nightly confirmation)</priority>
  </metadata>

  <references>
    <ref type="trigger">W4-CG Rule 7 flag: role_aua.nna_txn = 0.00 across all canonical partitions. CTO disposition: ACCEPT INFO for Wave 4 close; RA-P1c staged as deferred cleanup.</ref>
    <ref type="ds_plan">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.RA-P1b — historical backfill complete (c962ddb3, 2,294 partitions)</ref>
  </references>

  <objective>
    Repopulate nna_txn in role_aua canonical partitions. Currently 0.00 across all partitions
    because the RA-P1b backfill producer did not populate flow columns (only AUA snapshot fields).

    Technical basis from CTO: role_aua is a per-date AUA snapshot; NNA is a flow metric requiring
    a time window. nna_txn in role_aua should carry the role-attributed NNA for that date window,
    derived from a join of role_aua × nna_atomic, not from a single-date AUA snapshot. The field
    exists in the schema for structural consistency; populating it correctly requires a separate
    computation pass, not a fix to the AUA snapshot producer.

    Scope: update the role_aua backfill/producer logic to populate nna_txn from nna_atomic join
    for each date partition. Re-run partitions or add incremental per-date computation.

    Gate: tonight's PROD nightly must confirm CN-P1b nna_atomic partitions are being written
    correctly before this TO can execute (RA-P1c depends on nna_atomic PROD confirm).
  </objective>

  <wire_contract>
    role_aua canonical partitions emit non-zero nna_txn where role-attributed NNA is non-zero.
    Computed as a join of role_aua × nna_atomic per date, not inferred from AUA snapshot.
  </wire_contract>

  <acceptance_criteria>
    1. role_aua producer or backfill script updated to populate nna_txn via nna_atomic join.
    2. At least 5 sample dates spot-checked: nna_txn non-zero for advisors with known NNA activity.
    3. py_compile exit 0.
    4. comp-validate role_aua --artifact /tmp/role_aua.parquet exit 0 with nna_txn non-zero check.
    5. Session log with compiler tools section.
    6. MCP COMPLETE to COO + CTO with commit hash + spot-check table.
  </acceptance_criteria>

  <dependencies>
    <dependency to="ADVI_ROLLUP.RA-P1b" status="complete" evidence="c962ddb3"/>
    <dependency description="Tonight CN-P1b PROD nightly confirmation — nna_atomic partitions writing correctly" status="pending"/>
  </dependencies>

  <next>On complete: role_aua partitions fully populated. RA convergence numerically sealed.</next>
</task_order>
