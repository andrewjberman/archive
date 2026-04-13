<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-13-hdrspl-002</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>staged</status>
    <project_code>ADVI_HDRSPL</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_HEADER_SPLIT_PRIMITIVES.md</ref>
    <ref type="project">org/projects/ADVI_HDRSPL.json</ref>
  </references>

  <dependencies>
    <dependency task="ADVI_HDRSPL.001" status="pending"/>
  </dependencies>

  <objective>
    Wave 2 of 3. Move the firm picker out of the Assets Overview (PartnerAnalytics) panel header to the ADVI page top-right (above the tab strip). Render it using `<PageSurfaceControl variant="solid-indigo" as="dropdown" />` from Wave 1. Internalize `timeWindow` + `granularity` inside `PartnerAnalytics` — remove these from page-root state. Assets Overview retains its existing in-panel toggles unchanged from its own POV; it is no longer the source of truth for Segment Analytics (Wave 3 will give Segment Analytics its own state).
  </objective>

  <context>
    State ownership change table (from PRD):

    | State | Before | After |
    |-------|--------|-------|
    | `selectedFirmId` | AdvisorIntelligence.tsx root | AdvisorIntelligence.tsx root (unchanged; render moves to page header) |
    | `timeWindow` (Assets Overview) | AdvisorIntelligence.tsx shared | PartnerAnalytics local |
    | `granularity` (Assets Overview) | AdvisorIntelligence.tsx shared | PartnerAnalytics local |

    Page-root refs to verify when internalizing: `AdvisorIntelligence.tsx:144,156` per CTO grep. Firm picker goes top-right, ABOVE the tab strip, rendered on silver bg (page surface).

    This TO does NOT yet add Segment Analytics toggles — Distribution tab will temporarily have no window/interval controls between Wave 2 ship and Wave 3 ship. Coordinate sequencing with Wave 3.

    NOTE: Wave 2 and Wave 3 may be bundled into a single commit at DE discretion per CTO — cross-domain is `<none/>` and both touch `portal/src/` only. If bundled, flip both TOs to complete in the same session; if split, ship Wave 2 first.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-blast components/PartnerAnalytics.tsx` — confirm no external consumer depends on lifted state (COO pre-check: 1 endpoint getTimeseriesOverview, 1 Lambda opal-partners-data, 2 downstream nodes).
    - `comp-blast pages/AdvisorIntelligence/AdvisorIntelligence.tsx` — full page impact (COO pre-check: 2 endpoints getPlatinumPartnerAnalytics + getFirmLeaderboard, 1 Lambda, 3 downstream).
    - `comp-transform schema-check PartnerAnalytics` — confirm prop-shape change is safe (COO pre-check: 4/7 rendered, no waste).
    - Grep `timeWindow`, `granularity`, `selectedFirmId` across the page directory to find every reference.

    Phase 2 (before committing):
    - Re-run `comp-blast` on both files — no new downstream edges expected.
    - tsc --noEmit + bun run lint clean.

    Phase 3 (after committing):
    - `/frontend-dev` pass verifying: firm picker is outside every `<Panel>`, sits top-right above tabs, renders via `<PageSurfaceControl>`, WCAG AA >= 4.5:1 numeric ratio recorded.
    - Functional check: changing firm propagates to all tabs + both panels (no regression).

    Log all runs to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- Frontend only. ADVI_OTHDED.001 also touches DistributionTab.tsx but different region (enforceTop9Other, not panel header). Recommend OTHDED lands first (trivial, already pending). -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Firm picker rendered OUTSIDE any `<Panel>` in the ADVI page (React DevTools / grep confirms).
    2. Firm picker positioned top-right, above the tab strip, visible on silver page bg.
    3. Firm picker uses `<PageSurfaceControl variant="solid-indigo" as="dropdown" />`.
    4. `timeWindow` and `granularity` are local state inside `PartnerAnalytics` — removed from `AdvisorIntelligence.tsx` root.
    5. Firm change propagates to all tabs + both panels (no regression from current behavior).
    6. No TypeScript errors, no ESLint errors, no new console warnings.
    7. Compiler log shows Phase 1 + Phase 2 + Phase 3 runs with results.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/AdvisorIntelligence.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx</file>
    </files>
  </scope>

  <requirements>
    - Do NOT change any endpoint or response-shape contract.
    - Preserve all existing ADVI tab behavior other than the firm-picker render location and the `timeWindow`/`granularity` prop split.
    - If Wave 3 is bundled, include Segment Analytics toggles per `ADVI_HDRSPL.003` requirements; otherwise leave Distribution tab unchanged pending Wave 3.
  </requirements>

  <deliverables>
    - Commit to portal DEV with `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.
    - Session log with Compiler Tools section.
    - `org/compiler-tools-log.md` entries.
    - Flip `<status>` staged -> pending on GO, then -> complete after validation.
  </deliverables>

  <do_not>
    - Do NOT add Segment Analytics local toggles here — Wave 3 scope.
    - Do NOT remove the Assets Overview in-panel Window/Interval toggles.
    - Do NOT change the `selectedFirmId` ownership — only its render location.
  </do_not>
</task_order>
