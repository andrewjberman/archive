<task_order>
  <metadata>
    <id>0.4.2_RD_AdvisorIntelligence-2026-04-14-advi-fntend-b0</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-14</date>
    <status>pending</status><!-- CONDITIONALLY COMPLETE — portal DEV 5ea017c diffs validated by CTO; acceptance #5 /frontend-dev closed-loop not yet satisfied (RD-triggered run requested 2026-04-14T21:31Z). Flip to complete when RD confirms clean run. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 0)</ref>
    <ref type="brief">org/tier2_senior/0.4.2_RD_AdvisorIntelligence/briefs/2026-04-14_advi_frontend_status.md</ref>
  </references>

  <objective>
    FE-trivial sweep — 5 items, one RD TO.

    B2: `ClientsTable.tsx:77` — `whitespace-nowrap` on No-Fee pill + widen cell.
    B4: `AdvisorBookClientDetail` → `CanonicalBookView` L3 — pass `readonlyAssetClass`.
    B10: `AdvisorBookAccountDetail` → `CanonicalBookView` L4 — pass `readonlyAssetClass`.
    G1: Audit Top Holdings render sites → `mixPieColor(asset_class)` via `chartColors.MIX_PIE`. Confirm MIX_PIE matches Assets Overview canonical (equity=blue, FI=green, alts=orange). One-line palette fix if mismatch.
    D5 (added 2026-04-14 per Andrew): `DistributionTab.tsx` `ContinuousChartView` when `cohort === 'adv' && isDrilled` — pseudonymize child category labels as `Client N` (stable ordinal per drill parent; `Other` preserved literally). New helper `pseudonymizeChildLabel(key, cohort, isDrilled, ordinalMap)` swapped in at DistributionTab.tsx lines 1295, 1308, 1445, 2022, 2180, 2249. Ordinal map keyed by drill-parent so color + search + tooltip + legend agree. Forced pseudonymization regardless of `canSeeCleartext()` — surface-specific, not role-gated. Click paths + drill data unchanged.
  </objective>

  <acceptance_criteria>
    1. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) shows No-Fee pill on single line
    2. Client/Account L1 drills show non-clickable Asset Mix (readonlyAssetClass propagated)
    3. Top Holdings palette matches Assets Overview (blue/green/orange) on every render site
    4. Continuous-ADV drilled view shows `Client N` labels across legend + search + tooltip + stacked bars + breadcrumb (forced, regardless of canSeeCleartext)
    5. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) closed-loop pass
    6. MCP COMPLETE to COO with commit hash
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check CanonicalBookView` (readonlyAssetClass trace); `comp-transform schema-check ConsolidatedOverviewPanel` (Top Holdings palette); **`comp-transform schema-check DistributionTab`** (D5 touches 6 call sites; without this the pseudonymize swap can miss a site).
    Phase 2: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) after commit.
    Phase 3: Post-PR visual QA.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>
</task_order>
