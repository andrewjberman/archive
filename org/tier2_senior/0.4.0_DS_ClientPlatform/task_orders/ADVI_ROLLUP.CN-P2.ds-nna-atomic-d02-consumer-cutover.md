<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-cn-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Flipped pending→complete 2026-04-16 by 0.4.0_DS_ClientPlatform. Commit ebd737e3 on CLOUD: D_02-2 + D_02-3 prefix flip (CANONICAL_NNA_PREFIX→CANONICAL_NNA_ATOMIC_PREFIX in _load_canonical_nna_per_advisor). Commit b3f6b1ee on CLOUD (DS~D 2026-04-16): D_02-1 canonical NNA for build_advisor_books summary site — canonical_lookup + canonical_adv_dates pre-computed in build_advisor_books, _nna_since now uses canonical period-diff with C_03 fallback. py_compile exit 0. comp-blast D_02 → no downstream. S3 upload complete. Travis NNA three-way validation pending D_02 gold run (schism closed by construction — all three D_02 NNA sites now source from nna_atomic canonical). -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>CN-P2 (D_02 consumer cutover — first of 4 cutover phases)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #8, Phase 2)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.CN-P1.ds-nna-atomic-shadow-write.md (must ship first)</ref>
    <ref type="consumer_memo">docs/data/nna_atomic_consumer_enumeration.md (P0 memo assigns P2=D_02 per CN-P0 93b70620)</ref>
    <ref type="paired">ADVI_ROLLUP.RA-P2.ds-role-aua-d02-consumer-cutover.md — paired D_02 cutover for role_aua</ref>
  </references>

  <objective>
    Phase 2 of 6. Cut over D_02's NNA aggregation sites (per CN-P0 consumer memo, P2=D_02 scope) to
    read from `gold/canonical/nna_atomic/{date}.parquet` (shipped as shadow artifact in CN-P1).

    D_02 NNA sites per CN-P0 enumeration memo (up to ~5 sites depending on the memo's exact count):
    the sites that drive `advisor_books` NNA aggregates + `advisor_timeseries` cumulative flow paths +
    the derived period_nna computations. Exact file:line list in the memo — agent reads + confirms.

    Output parity gate: `platinum/advisors/{*}/summary.json` NNA-related values + timeseries rfs
    decomposition fields must match CN-P1 shadow artifact within $0.01. RF01 (already shipped as
    `21c0637f`) corrected the window-decomposition math upstream; this cutover routes the NNA source
    through the canonical table instead of re-deriving from C_01 running totals per-site.

    Remaining 4+ sites (D_00c leaderboard NNA, D_01 partner_analytics geo/adv, D_00b adv_drill NNA,
    D_00 firm timeseries, etc.) are P3/P4/P5. DO NOT touch.
  </objective>

  <wire_contract>
    D_02 NNA reads from canonical. Downstream `platinum/advisors/{*}/*.json` shapes unchanged — same
    keys, same types. Only numeric values may shift where the old per-site filter stack produced
    different aggregates. Expected: Travis three-way NNA + TX three-way NNA resolve to single values
    across summary/book/timeseries.
  </wire_contract>

  <acceptance_criteria>
    1. All D_02 NNA sites per consumer memo read from nna_atomic canonical.
    2. Travis Cobb NNA across summary + book + timeseries matches within $0.01.
    3. `comp-validate nna_atomic --artifact /tmp/nna_atomic.parquet` exits 0.
    4. Zero-byte diff on all non-NNA D_02 outputs.
    5. NNA three-way schism at D_02 grain CLOSED (summary / book / timeseries consistent by construction).
    6. Session log Compiler Tools section reproduces each `<run>` + observed + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    7. Acceptance-flex pre-flag rule (CTO locked 2026-04-15) — any deviation = MCP to CTO before acceptance + closeout citation.
    8. MCP COMPLETE to COO with commit hash + Travis NNA spot-check table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>D_02 reads include `gold/canonical/nna_atomic/` (post CN-P1 shadow). Old per-site NNA inputs still present but only for non-NNA code paths.</expect>
        <if_mismatch>If nna_atomic not in reads, CN-P1 hasn't landed — STOP.</if_mismatch>
      </step>
      <step>
        <run>Read docs/data/nna_atomic_consumer_enumeration.md for P2=D_02 site list</run>
        <expect>Site list identifies each NNA aggregation path in D_02 with file:line precision.</expect>
        <if_mismatch>Memo missing P2 scope — escalate to CN-P0 author for clarification.</if_mismatch>
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
        <expect>Exit 0; D_02 NNA sites populated from canonical; non-NNA unchanged.</expect>
        <if_mismatch>Iterate until validator clean.</if_mismatch>
      </step>
      <step>
        <run>Diff platinum/advisors/{travis-penfield}/summary.json across summary + book + timeseries on NNA fields</run>
        <expect>All three equal within $0.01 (three-way schism closed).</expect>
        <if_mismatch>Schism persists — re-trace cut points; one is likely still on the old filter stack.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast D_02</run>
        <expect>Downstream consumer set unchanged.</expect>
        <if_mismatch>Coordinate with DE/DT before signaling complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <!-- Re-sequenced 2026-04-16 per CTO Path B (20260416T125816Z): CN-P1b historical backfill blocks D_02 consumer cutover because D_02 NNA paths are period/historical with no snapshot carve-out. -->
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.CN-P0" status="complete" evidence="93b70620" description="canonical schema ratified"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.CN-P1" status="complete" evidence="bf9651b8" description="daily shadow writer live"/>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_ROLLUP.RA-P1" status="complete" evidence="afd553d4" description="paired role_aua shadow writer live"/>
    <dependency agent="0.4.0_DS_ClientPlatform~D" task="ADVI_ROLLUP.CN-P1b" status="complete" description="historical backfill of nna_atomic partitions -- D_02 reads period/historical NNA, would collapse to $0 on ~2293 dates without CN-P1b close. COMPLETE dc4980c3 2026-04-16."/>
  </dependencies>

  <next>
    On commit: COO authors CN-P3 (D_00c leaderboard NNA cutover, paired with RA-P3). D_02 cutover
    is the first + broadest; subsequent phases narrow.
  </next>
</task_order>
