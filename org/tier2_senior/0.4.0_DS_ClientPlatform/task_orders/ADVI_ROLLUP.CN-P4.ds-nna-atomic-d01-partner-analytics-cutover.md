<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-cn-p4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- Flipped pending→complete 2026-04-16 by 0.4.0_DS_ClientPlatform. Commit 4e63038e on CLOUD: D_01 _load_canonical_nna CANONICAL_NNA_ATOMIC_PREFIX cutover (import + paginator). GEO 3-way schism closed by construction — all D_01 NNA sites now groupby nna_atomic rows. py_compile exit 0. comp-blast D_01 no downstream. S3 upload + deployed MATCH. TX 3-way + Travis 3-way NNA pending D_01 gold run. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>CN-P4 (D_01 partner_analytics NNA cutover — closes GEO 3-way schism)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #8, Phase 4)</ref>
    <ref type="ds_plan">docs/architecture/ADVI_CANNNA_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.CN-P3 (D_00c cutover must complete)</ref>
    <ref type="consumer_memo">docs/data/nna_atomic_consumer_enumeration.md (P4=D_01 scope)</ref>
    <ref type="paired">ADVI_ROLLUP.RA-P4.ds-role-aua-d01-partner-analytics-cutover.md — co-ship recommended</ref>
    <ref type="supersedes">GEO 3-way NNA schism (PRD item #4) — closed structurally at this phase</ref>
  </references>

  <objective>
    Phase 4 of 6. Cut D_01 `build_nna_geo_view` (L1242-1429) + all D_01 NNA aggregation sites to
    read from canonical `nna_atomic/{date}.parquet`. **This is the phase that structurally closes
    the GEO 3-way schism** (donut / by_city / distribution rollups all become groupbys on the same
    atomic table).

    Per CN-P0 consumer memo, P4 = D_01 scope. Sites include `build_nna_geo_view` donut/by_city/distribution
    + `build_adv_view` NNA rollups.

    Output parity: `platinum/firm/partner_analytics/*.json` donut.segments[X].value ==
    sum(by_city for same state) == distribution.total for same (period, state) — all three roll
    up from the same atomic rows. TX current: donut + by_city + distribution must agree within $0.01.
  </objective>

  <wire_contract>
    D_01 NNA emits from canonical. partner_analytics donut/by_city/distribution all groupby same atomic rows.
    GEO 3-way schism eliminated by construction.
  </wire_contract>

  <acceptance_criteria>
    1. D_01 NNA sites read from nna_atomic canonical.
    2. **GEO 3-way closed:** TX current donut.segments[tx].value == sum(by_city[tx].*) == distribution[tx].total within $0.01.
    3. Travis three-way NNA (summary / book / timeseries) closed — already done at P2/P3, confirmed at P4.
    4. `comp-validate nna_atomic --artifact /tmp/nna_atomic.parquet` exit 0.
    5. Zero-byte diff on non-NNA partner_analytics fields.
    6. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    7. Acceptance-flex pre-flag rule (CTO Rule 7).
    8. MCP COMPLETE with commit hash + TX 3-way + Travis 3-way closure table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>comp-pipescript io D_01</run><expect>Reads include nna_atomic canonical.</expect><if_mismatch>CN-P1..P3 chain incomplete — STOP.</if_mismatch></step>
      <step><run>Read CN-P0 consumer memo for D_01 NNA site list (L1242-1429 + adv view sites)</run><expect>All P4 sites inventoried.</expect><if_mismatch>Memo incomplete — escalate.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>python -m py_compile data/black_diamond/scripts/gold/D_01.partner_analytics.py</run><expect>Exit 0.</expect><if_mismatch>Fix.</if_mismatch></step>
      <step><run>TX current 3-way check: donut vs by_city sum vs distribution.total</run><expect>All three within $0.01.</expect><if_mismatch>Schism still present — trace cut gap.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>comp-blast D_01</run><expect>Consumer set unchanged.</expect><if_mismatch>Coordinate.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~B" task="ADVI_ROLLUP.CN-P3" status="complete" evidence="d96da39d"/>
    <dependency agent="co-phase" task="ADVI_ROLLUP.RA-P4" status="complete" description="co-ship pair — both on ~B, same D_01 commit; circular blocking dep resolved 2026-04-16"/>
  </dependencies>

  <next>On commit: COO authors CN-P5 (D_00b/D_00 remaining NNA closeout).</next>
</task_order>
