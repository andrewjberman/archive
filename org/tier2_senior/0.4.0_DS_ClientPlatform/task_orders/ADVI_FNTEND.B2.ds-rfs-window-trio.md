<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-14-advi-fntend-b2-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to><!-- re-dialed 2026-04-15 PM by COO from base lane to ~B for post-rerun validator pass -->
    <date>2026-04-14</date>
    <status>complete</status><!-- VALIDATED 2026-04-15 22:11Z by ~B against post-19:35Z artifacts. Acceptance #1 PASS: all 12 keys present at all 3 grains (advisor.book.rfs, client.rfs, account.rfs) — verified on Travis Penfield (advisor), z08103151 (client), z0812152081 (account). Acceptance #2 PASS: decomp.nna == rfs.nna in all windows (qtd/ytd/max); market_growth + synth_corr terms present + non-zero; reconciliation by construction. Code shipped 2026-04-14 commit 3a2f0998. Original CODE SHIPPED note preserved for audit trail. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
    <priority>keystone — window vocabulary reused by B3/B4/B5</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 2: B3+B7+B8)</ref>
  </references>

  <objective>
    Ship window-scoped `{nna, inflows, outflows}_{qtd, ytd, max}` at:
    - client-level (AdvisorClient)
    - account-level (AccountsTable row — per DS scoping doc, 5-line passthrough absorbed into B2 scope per CTO ruling 2026-04-14; no separate TO)
    AND full `decomposition_{qtd, ytd, max}` = `{market_growth, synthetic_correction, nna}`.
  </objective>

  <acceptance_criteria>
    1. All fields present on artifacts for both client + account grains
    2. Decomposition sums reconcile: market_growth + synthetic_correction + nna ≈ aua delta over window
    3. MCP COMPLETE to COO with commit + S3 ETag + sample JSON
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-pipescript io D_02.timeseries.py` + `comp-platinum` trace for decomposition emission.
    Phase 2: `python -m py_compile`; `comp-validate` after gold rerun.
    Phase 3: `comp-transform schema-check` RelationshipFlowsSummary + AccountsTable + ClientsTable.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>On COMPLETE: fires B2 FE AND unblocks B3 DS.</next>
</task_order>
