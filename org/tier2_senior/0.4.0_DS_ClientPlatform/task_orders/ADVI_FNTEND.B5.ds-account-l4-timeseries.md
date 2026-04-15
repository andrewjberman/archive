<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b5-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to><!-- re-dialed 2026-04-15 PM by COO from base lane to ~B for post-rerun validator pass -->
    <date>2026-04-14</date>
    <status>complete</status><!-- VALIDATED 2026-04-15 22:11Z by ~B against post-19:35Z artifacts. Acceptance #1+#2 PASS: account summary z0812152081 has timeseries[] length=844, inception 2023-12-22 → 2026-04-13. Fields exact-match TO: {date, aua_canonical, nna_canonical, inflows_canonical, outflows_canonical}. Code shipped 2026-04-14 commit f17e8366. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 5: B9)</ref>
  </references>

  <objective>
    Add account-level inception-to-date timeseries under `PlatinumAccountSummary`
    (AUA + flows, same `*_canonical` convention as advisor lifetime activity).
  </objective>

  <acceptance_criteria>
    1. Account summary artifacts have timeseries array
    2. Fields mirror advisor Lifetime Activity (aua_canonical, nna_canonical, inflows_canonical, outflows_canonical, date)
    3. MCP COMPLETE to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io` on account-summary writer; `comp-platinum reverse` on the new PlatinumAccountSummary timeseries field (confirm no other consumer blast).
    Phase 2: `python -m py_compile`.
    Phase 3: `comp-validate`.
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B2 DS" status="staged" description="B5 rides B2's gold rerun per CTO ruling 2026-04-14 — separate commit but shares rerun window"/>
  </dependencies>
</task_order>
