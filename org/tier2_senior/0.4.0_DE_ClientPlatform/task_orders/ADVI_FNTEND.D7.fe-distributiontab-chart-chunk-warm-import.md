<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-d7</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status><!-- GO 2026-04-14T22:08Z; DE flipped pending 2026-04-14T22:10Z; complete portal commit e200193 (2026-04-14); confirmed post-rerun regression 2026-04-15 distribution_tab_rapid_toggle PASS 10x3+10x2, 0 blanks -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A</wave>
    <type>FE regression fix (micro-TO)</type>
  </metadata>

  <references>
    <ref type="diagnosis">DE MCP 2026-04-14 — DistributionTab intermittent-blank on rapid toggle</ref>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (ADVI_FNTEND scope — additive regression fix)</ref>
  </references>

  <objective>
    Fix intermittent blank Snapshot / Continuous view on rapid cohort toggle in DistributionTab.

    Symptom: blank chart after fast toggling, no drilling involved, hard refresh unreliable.
    Root cause (DE-diagnosed, high confidence): ApexCharts + Recharts lazy-chunk race through
    React Suspense.
    Ruled out: D6 drillParentKey change; data shape; build errors.

    Fix — Option B (warm-import both chart chunks in DistributionTab's mount useEffect):
    Preloading both vendor chunks on DistributionTab mount prevents the Suspense race — whichever
    chart renders first already has the other's chunk resolved.
  </objective>

  <acceptance_criteria>
    1. 10x rapid cohort toggle across all cohorts (geo/adv/ofc/cla × snapshot/continuous) — zero blank-chart states observed
    2. Browser network tab confirms both ApexCharts + Recharts vendor chunks fetched early (on DistributionTab mount, not on first chart render)
    3. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) closed-loop pass on DistributionTab
    4. No regression on non-rapid toggle path
    5. MCP COMPLETE to COO with commit hash + /frontend-dev report path
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check DistributionTab` — confirm no prop/state drift from added useEffect.
    Phase 3: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) rapid-toggle scenario.
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <cross_domain_coordination>
    Isolated to DistributionTab.tsx — does NOT touch AdvisorBookView.tsx or types.ts. No serialization conflict with Wave C (B1/B3/B4/B5/B8 FE). Safe to run in parallel.
  </cross_domain_coordination>

  <frontend_dev_note>
    If no constitution exists at `portal/.frontend-dev/testing/` for the target component + scenario, author one first per the schema in that directory's README.md. Do not hand-roll Playwright scripts in repo root — the smoke-test.py/.mjs pattern is deprecated.
  </frontend_dev_note>
</task_order>
