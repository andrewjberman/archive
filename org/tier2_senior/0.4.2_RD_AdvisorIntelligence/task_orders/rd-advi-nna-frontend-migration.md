<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-advi-nna-frontend-migration</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-10</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code>ad-hoc</project_code>
    <related_to>companion ds-advi-nna-canonical-source.md (backend schema extension)</related_to>
  </metadata>

  <objective>
    Migrate `ContinuousNnaDivergingView` Level 0 bars in `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` to read NNA per-category breakouts from `platinum/firm/timeseries_overview.json.nna[granularity][i].by_geo` / `.by_adv` via a new optional prop, with a legacy fallback that keeps the current cumulative-chart pairwise-diff path alive for drilled views AND for the DS rollout window.

    Types add `NnaPerCategoryBreakout`, extend `TimeseriesOverviewNnaPeriod` with optional `by_geo` / `by_adv` fields, and add a new helper `extractNnaCategoryKeys`. React Query cache dedup against the existing `['advisor-intelligence', 'timeseries-overview', firmOverride]` key eliminates any extra network cost.

    **This TO can ship BEFORE the companion DS task (`ds-advi-nna-canonical-source.md`).** The fallback path renders identically to today's production build when `by_geo`/`by_adv` are absent. Once DS ships and the next gold runner cycle writes the extended `timeseries_overview.json`, the canonical path auto-activates on the next React Query cache refresh — no frontend redeploy required. Zero coordination between RD and DS commit timing.
  </objective>

  <context>
    **Authoritative brief:** `docs/briefs/rd-brief-advi-nna-canonical-source-frontend.md` — READ IN FULL before starting. This task order wraps the brief with org protocol; it does not restate the brief.

    **Companion brief (reference only):** `docs/briefs/ds-brief-advi-nna-canonical-source.md` — explains the data-layer fix and the sum-invariance contract the RD frontend relies on.

    **Cross-panel drift this closes:** Assets Overview Q2 2026 bar = $5.3M vs Segment Analytics Continuous GEO-NNA Q2 2026 tooltip = $10.3M (observed on 2026-04-10 at 3Y + Quarter + NNA). Root cause is the cumulative weekly-downsampled pairwise-diff path drifting from the pre-aggregated per-period path. After RD + DS both ship, both panels read the same `timeseries_overview.json` file and drift becomes structurally impossible.

    **COO compiler-verified cross-layer state (2026-04-10 pre-TO runs, logged in org/compiler-tools-log.md):**
    - `comp-platinum reverse platinum/firm/timeseries_overview.json` — Producer D_04, served via S3-direct `/api/scoped/advisor-intelligence/*.json` through `shared-advisor-router` edge auth, current consumer is `PartnerAnalytics` only. This TO adds `DistributionTab` as the second consumer.
    - `comp-transform fields DistributionTab` — confirms DistributionTab currently reads only `chartData.adv?.categories` and `chartData.geo?.categories` at the field-tracker's visible surface. `nna_geo`, `nna_geo_drill`, `nna_adv`, `nna_adv_drill` are in the type but flagged as unused at top level in `schema-check` output — reflecting the pairwise-diff internal usage rather than direct render.
    - `comp-transform schema-check DistributionTab` — all rendered fields match their response types. 12 unused fields on `PlatinumCumulativeChartResponse` expected. Clean baseline.
    - `comp-transform fields PartnerAnalytics` — current consumer pattern is `timeseriesData?.nna?.[auaGranularity]`. The new `by_geo`/`by_adv` fields nest inside each period entry, so the access pattern extends naturally for both PartnerAnalytics and the new DistributionTab consumer.
    - `comp-cache collisions` — no existing collision on `['advisor-intelligence', 'timeseries-overview', firmOverride]`. Only intentional shared key today is `['firm-leaderboard', firmOverride]` from ADVI_PROFIL.001. RD's plan to add a second `useQuery` with the same queryKey creates a dedup pattern — same file fetches once, two component consumers.

    **Critical: fallback path is mandatory.** Per the brief Appendix B, shipping without the fallback risks a blank Segment Analytics NNA view if `timeseries_overview.json` still has the old schema at deploy time. The component must render identically to today's production build when `by_geo`/`by_adv` are absent on every period.

    **Scope discipline reminder from comp-transform:** the schema-check output lists 12 unused fields on `PlatinumCumulativeChartResponse` including `nna_geo`, `nna_geo_drill`, `nna_adv`, `nna_adv_drill`. Per the brief §4, drilled views (`drillParent !== null`) continue to use these legacy fields from `cumulative_chart.json`. Do NOT remove them from type or fetch. Only Level 0 bars migrate.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - Read the RD brief in full. Note the dependency model (Part 2), the fallback path (Part 5), and the failure modes (Appendix C).
    - Read the DS brief §"Schema" and §"Invariants" so you know exactly what shape to expect and which invariants are enforced on the DS side. This drives your frontend type definitions.
    - `comp-transform schema-check DistributionTab` — baseline before edits. Save the output. You will re-run after edits to prove no new drift.
    - `comp-transform fields DistributionTab` — baseline for the rendered field set.
    - `comp-transform fields PartnerAnalytics` — confirm the `timeseriesData?.nna?.[auaGranularity]` pattern still holds. Your new consumer must match this shape.
    - `comp-cache collisions` — confirm the `['advisor-intelligence', 'timeseries-overview', firmOverride]` queryKey is what PartnerAnalytics uses, and that your new `useQuery` will dedupe correctly. If PartnerAnalytics' key has drifted (e.g., a version bump, a new suffix), fix the reconciliation BEFORE shipping — two same-file fetches with different keys is a pure waste, and the brief acceptance criterion 6 explicitly checks for it.
    - `comp-blast ContinuousNnaDivergingView` — capture baseline so Phase 3's re-run can confirm the only new consumer relationship is `DistributionTab` → `ContinuousNnaDivergingView` with a new optional prop (no public-API expansion).
    - Read the companion DS task order (`ds-advi-nna-canonical-source.md`) so you know which DS deliverables are in flight. This TO does NOT block on the DS TO, but the acceptance criterion 4 (cross-panel parity on live data) requires DS to have shipped first.

    Phase 2 (during implementation):
    - Follow the brief Parts 1-5 verbatim for type additions, data fetch strategy, component refactor, drill-path preservation, and fallback behavior. The brief has exact code snippets — they are authoritative unless you discover a type mismatch that forces a change.
    - Mock test BEFORE running the dev server: write a quick unit test (or in-file mock object) with the OLD schema (no `by_geo`/`by_adv`) and verify `hasCanonicalBreakout === false` and `barData` takes the legacy path. Write another mock with the NEW schema and verify `hasCanonicalBreakout === true` and the canonical path activates. The brief §Part 5.2 lists the exact check matrix.
    - Follow the cursor-affordance cleanup that was flagged by DT 0.4.0 during ADVI_PROFIL.002 verification: the non-admin blocked click surfaces in `AdvisorsTab.tsx` show a hand cursor on surfaces that are no-ops for non-admins. This is a tiny CSS/conditional fix adjacent to the Level 0 NNA rendering surface and can be bundled into this TO (no extra commit required). If scope grows beyond ~10 lines, split into a follow-up instead — do not let scope creep push this TO.

    Phase 3 (before committing):
    - `bun run tsc -b` exit 0 — mandatory.
    - `bun run eslint src/pages/AdvisorIntelligence/` — 0 errors. Any new warnings must be explicitly called out in the session log.
    - `comp-transform fields DistributionTab` — re-run. Confirm the new additions are picked up: `timeseriesNna`, `nnaPeriods`, `hasCanonicalBreakout`, `barData` (new branching). No previously-rendered fields dropped.
    - `comp-transform schema-check DistributionTab` — re-run. Must still pass. No type contract regressions.
    - `comp-transform fields PartnerAnalytics` — re-run. MUST be unchanged. This TO does NOT touch PartnerAnalytics per brief Part 7 scope constraint #2.
    - `comp-blast ContinuousNnaDivergingView` — re-run. The new public-API change (adding an optional `timeseriesNna` prop) should not expand blast radius. Only `DistributionTab` should appear as a consumer.
    - `comp-cache` re-run — confirm the new queryKey is picked up and dedupes cleanly against PartnerAnalytics' existing key.
    - Manual fallback test in the browser: load the page with the current production `timeseries_overview.json` (which lacks `by_geo`/`by_adv`). Verify the Level 0 Segment Analytics Continuous NNA bars render identically to the pre-migration build. Spot-check one Q2 2026 bar value against Assets Overview's Q2 2026 bar — the drift should still be there (cross-panel parity only lands after DS ships) BUT the view must be functional.

    Log every tool run with result to `org/compiler-tools-log.md` using the standard format.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `platinum/firm/timeseries_overview.json` schema — DS extends (companion TO `ds-advi-nna-canonical-source.md`), RD consumes (this TO). Schema frozen at the shape defined in the DS brief §"Schema". Any future change requires coordinated DS + RD pass.
    shared_resource: React Query cache key `['advisor-intelligence', 'timeseries-overview', firmOverride]` — PartnerAnalytics has it today at `PartnerAnalytics.tsx:163` (per comp-cache). DistributionTab adds a second `useQuery` with the SAME key — React Query dedupes automatically. Verify byte-for-byte key match at `bun run tsc -b` time.
    shared_resource: `portal/src/pages/AdvisorIntelligence/types.ts` — RD extends with `NnaPerCategoryBreakout` + optional fields on `TimeseriesOverviewNnaPeriod` + `extractNnaCategoryKeys`. No other agent touches types.ts in this window.
    shared_resource: `portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx` — RD owns for this TO. Other open work touching DistributionTab: none currently. ADVI_PROFIL.005 will touch `ClientsTab.tsx` (sibling file) but that's a different component path.
    shared_resource: `portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx` — REFERENCE ONLY. Do NOT modify. Brief Part 7 scope constraint #2 is explicit.
    shared_resource: `portal/src/api/endpoints/advisor-intelligence.ts` — already exports `getPlatinumTimeseriesOverview` (confirmed in RD brief §Part 2). No change needed to the API client; just add an import in DistributionTab.
    last_write_owner: 0.4.2_RD_AdvisorIntelligence for all code. DT ships separately.
    required_action: "RD ships the frontend with the mandatory fallback path BEFORE DS ships the backend. This order is intentional: the frontend fallback renders identically to today's build when the old schema is still live, and auto-activates the canonical path on the first cache refresh after DS's gold run. Hand off to 0.4.0_DT_ClientPlatform for commit + push (same pattern as ADVI_PROFIL.001 / .005). Do NOT commit or push yourself."
  </cross_domain_coordination>

  <acceptance_criteria>
    All 12 criteria from the RD brief §Part 6 apply verbatim. Summarizing and layering COO additions:

    1. Type additions compile cleanly. `tsc --noEmit` passes.
    2. Fallback path preserves current behavior when `by_geo`/`by_adv` are absent. Tested via mock + browser load against current production schema.
    3. Canonical path activates on new schema. Tested via mock with populated breakouts; bar values match sum-of-categories per period; hero sums to bar totals within $0.01.
    4. Cross-panel parity on live data — verified AFTER DS ships and the next gold runner cycle writes the extended file. Segment Analytics Q2 2026 NNA bar and PartnerAnalytics Assets Overview Q2 2026 NNA bar show identical values at `3Y + Quarter + NNA + GEO` and `3Y + Quarter + NNA + ADV`. This criterion closes on Andrew's verification — it is the final user-facing win condition.
    5. Drilled views unchanged. `drillParent !== null` continues to use legacy cumulative source.
    6. React Query cache dedup verified. Network tab shows exactly one fetch to `timeseries_overview.json` on page load even with both components subscribing.
    7. `comp-transform schema-check DistributionTab` passes with zero new drift.
    8. `comp-blast ContinuousNnaDivergingView` shows zero unintended downstream impact. Only new consumer is the new optional prop in DistributionTab.
    9. Max window works — all periods render.
    10. 1Y window works — correct period count for each granularity.
    11. Cohort toggle works — GEO vs ADV swaps `by_geo` vs `by_adv` from same `nnaPeriods`.
    12. Granularity toggle works — Quarterly / Monthly / Annual swaps `timeseriesNna[granularity]`.

    **COO-layer additions:**

    13. **Compiler Tools section in the session log.** Every compiler tool run from §compiler_tools_mandate Phases 1-3 logged with command + result + one-line note, and appended to `org/compiler-tools-log.md`. Mandatory per feedback memory.

    14. **Cursor-affordance cleanup (bundled from DT 0.4.0 ADVI_PROFIL.002 findings).** Hand cursor on blocked click surfaces in AdvisorsTab (non-admin leaderboard entries) removed. Small scope (~10 lines). If the fix grows beyond 10 lines, split into a follow-up TO instead of expanding this one.

    15. **RD hands off to DT for commit+push.** RD does NOT commit or push directly. Broker message to 0.4.0_DT_ClientPlatform with the working tree list, tsc/eslint results, manual-fallback-test screenshot or DOM snippet, and compiler tools log. Same pattern as ADVI_PROFIL.001 / .005.

    16. **Session log format.** `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-{NN}/advi_nna_frontend_migration.md` with the file list, type additions summary, component refactor diff summary, fallback test results (screenshot or output), compiler tools log, and Next Steps block naming DT for commit+push and (after DS lands) Andrew for cross-panel verification.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts (add NnaPerCategoryBreakout, extend TimeseriesOverviewNnaPeriod, add extractNnaCategoryKeys)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx (ContinuousNnaDivergingView props + barData branching + useQuery add + computeLegacyBarData extract)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx (cursor-affordance cleanup on blocked non-admin click surfaces, ~10 lines, bundled)</file>
      <file action="reference">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx — REFERENCE ONLY (queryKey at line 163, do NOT modify)</file>
      <file action="reference">portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx — REFERENCE ONLY (prop plumbing line 219)</file>
      <file action="reference">portal/src/api/endpoints/advisor-intelligence.ts — REFERENCE ONLY (getPlatinumTimeseriesOverview already exists at line 438)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read the RD brief in full before starting. It is authoritative on type shape, component refactor structure, fallback behavior, and failure modes.</requirement>
    <requirement id="2">Fallback path is MANDATORY. The component must render identically to today's production build when `by_geo`/`by_adv` are absent. No blank chart. No zero-bar state. See brief Appendix B.</requirement>
    <requirement id="3">Do NOT kill the `getPlatinumCumulativeChart` fetch. Still needed for AUA continuous view, drilled NNA views, and legacy fallback. Brief scope constraint #1.</requirement>
    <requirement id="4">Do NOT modify `PartnerAnalytics.tsx`. Brief scope constraint #2.</requirement>
    <requirement id="5">Do NOT lift `getPlatinumTimeseriesOverview` to a parent component. Component-level fetch with React Query dedup is the right scope. Brief scope constraint #3.</requirement>
    <requirement id="6">Do NOT migrate drilled views to the canonical source. `by_geo`/`by_adv` are aggregate-only. Brief scope constraint #4.</requirement>
    <requirement id="7">Do NOT remove `ContinuousNnaChartView` legacy component. Brief scope constraint #5.</requirement>
    <requirement id="8">Do NOT change window/interval/cohort selector semantics. Only the data source under the hood switches. Brief scope constraint #6.</requirement>
    <requirement id="9">Do NOT assume `timeseriesNna` is always defined. Handle `undefined`, empty arrays, missing granularity keys, missing periods, missing breakouts, empty breakout objects — all gracefully. Brief scope constraint #9.</requirement>
    <requirement id="10">Verify React Query cache dedup at tsc time by byte-for-byte matching the queryKey in PartnerAnalytics (`['advisor-intelligence', 'timeseries-overview', firmOverride]`). Reconcile any drift.</requirement>
    <requirement id="11">Manual fallback test in the browser is mandatory before handing off to DT. Brief scope constraint #10.</requirement>
    <requirement id="12">Hand off to DT for commit+push. Do NOT commit or push yourself.</requirement>
    <requirement id="13">Log every compiler tool run to `org/compiler-tools-log.md`.</requirement>
    <requirement id="14">Bundle the cursor-affordance cleanup (AdvisorsTab hand cursor on blocked non-admin click surfaces) only if scope stays under ~10 lines. If it grows, split.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="code">2-3 files modified in the portal DEV working tree, staged for DT commit+push under RD author attribution.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-{NN}/advi_nna_frontend_migration.md` with file list, type additions, component refactor diff summary, fallback test output, compiler tools log, and Next Steps.</deliverable>
    <deliverable type="message">Broker message to 0.4.0_DT_ClientPlatform for commit+push handoff (same pattern as ADVI_PROFIL.001/.005).</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT ship without the fallback path. Blank-chart regression is unacceptable.</rule>
    <rule>Do NOT modify PartnerAnalytics.tsx.</rule>
    <rule>Do NOT kill the getPlatinumCumulativeChart fetch.</rule>
    <rule>Do NOT migrate drilled views. Level 0 only.</rule>
    <rule>Do NOT commit or push. Hand off to DT.</rule>
    <rule>Do NOT let the cursor-affordance cleanup expand beyond ~10 lines; split if it grows.</rule>
    <rule>Do NOT skip the manual browser fallback test.</rule>
    <rule>Do NOT wait on DS. This TO can ship independently.</rule>
  </do_not>
</task_order>
