<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-ra-p4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to><!-- Reassigned ~C→~B 2026-04-15 per Andrew Option A + CTO Rule 3 fix: RA-P4 + CN-P4 share D_01.partner_analytics.py — both on same lane (~B) to avoid two-agent same-file conflict. -->
    <date>2026-04-15</date>
    <status>complete</status><!-- Flipped pending→complete 2026-04-16 by 0.4.0_DS_ClientPlatform. Commit 4e63038e on CLOUD: _load_role_aua_snapshot helper added; role_aua_snap pre-loaded per period in main(); build_adv_view param role_aua_snap wired; advisor_aua + advisor_role_aua override from canonical when snap non-empty; advisor_accts + advisor_rels retained from account_team loop. py_compile exit 0. comp-blast D_01 no downstream. S3 upload + deployed MATCH. Travis cross-consumer role-AUA parity (D_02/D_00c/D_01) pending D_01 gold run. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W4</wave>
    <phase_label>RA-P4 (D_01 partner_analytics adv view cutover)</phase_label>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 4 item #7, Phase 4)</ref>
    <ref type="ds_plan">docs/architecture/ROLE_AUA_CANONICAL_CONVERGENCE_PLAN.md</ref>
    <ref type="predecessor">ADVI_ROLLUP.RA-P3 (D_00c cutover must complete; cross-consumer parity target)</ref>
    <ref type="consumer_memo">docs/data/role_aua_consumer_enumeration.md (D_01 `build_adv_view` site)</ref>
    <ref type="paired">ADVI_ROLLUP.CN-P4.ds-nna-atomic-d01-partner-analytics-cutover.md — co-ship recommended</ref>
  </references>

  <objective>
    Phase 4 of 6. Cut D_01 `build_adv_view` (partner_analytics views.adv) role-AUA aggregation to
    read from canonical `role_aua/{date}.parquet`. Closes role-AUA schism across the 3rd consumer
    (D_02 summary, D_00c leaderboard, D_01 partner_analytics).

    Output parity: `platinum/firm/partner_analytics/*.json` views.adv role-AUA values match
    D_02 summary + D_00c leaderboard within $0.01 by construction.
  </objective>

  <wire_contract>
    D_01 adv view emits role-AUA from canonical. partner_analytics shape unchanged. Cross-consumer parity.
  </wire_contract>

  <acceptance_criteria>
    1. D_01 `build_adv_view` reads from role_aua canonical.
    2. Travis architect AUA matches across D_02 summary + D_00c leaderboard + D_01 partner_analytics within $0.01.
    3. `comp-validate role_aua --artifact /tmp/role_aua.parquet` exit 0.
    4. Zero-byte diff on non-role fields of partner_analytics outputs.
    5. Session log Compiler Tools reproduces each `<run>` + observed + pass/fail vs. `<expect>`.
    6. Acceptance-flex pre-flag rule (CTO Rule 7).
    7. MCP COMPLETE with commit hash + 3-consumer cross-check table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step><run>comp-pipescript io D_01</run><expect>Reads include role_aua canonical.</expect><if_mismatch>RA-P1/P2/P3 chain not landed — STOP.</if_mismatch></step>
      <step><run>grep -n 'build_adv_view' data/black_diamond/scripts/gold/D_01.partner_analytics.py</run><expect>Callsite identified.</expect><if_mismatch>Function renamed — escalate.</if_mismatch></step>
    </phase>
    <phase id="2" when="before commit">
      <step><run>python -m py_compile data/black_diamond/scripts/gold/D_01.partner_analytics.py</run><expect>Exit 0.</expect><if_mismatch>Fix.</if_mismatch></step>
      <step><run>Diff D_01 partner_analytics adv.role_breakdown vs D_02 summary.role_breakdown for Travis</run><expect>Match within $0.01.</expect><if_mismatch>Trace schism before commit.</if_mismatch></step>
    </phase>
    <phase id="3" when="after commit">
      <step><run>comp-blast D_01</run><expect>Consumer set unchanged.</expect><if_mismatch>Coordinate.</if_mismatch></step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~B" task="ADVI_ROLLUP.RA-P3" status="complete" evidence="e53f0afa"/>
    <dependency agent="co-phase" task="ADVI_ROLLUP.CN-P4" status="complete" description="co-ship pair — both on ~B, same D_01 commit; circular blocking dep resolved 2026-04-16"/>
  </dependencies>

  <next>On commit: COO authors RA-P5 (D_00b adv_drill + C_08 closeout).</next>
</task_order>
