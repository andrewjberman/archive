<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-13-hdrspl-003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>pending</status>
    <project_code>ADVI_HDRSPL</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_HEADER_SPLIT_PRIMITIVES.md</ref>
    <ref type="project">org/projects/ADVI_HDRSPL.json</ref>
  </references>

  <dependencies>
    <dependency task="ADVI_HDRSPL.002" status="staged"/>
  </dependencies>

  <objective>
    Wave 3 of 3. Give Segment Analytics (DistributionTab) its own local `timeWindow` + `granularity` state and its own in-panel toggle strip. Toggle order in panel header (left-to-right, EXACT): **Mode -> Interval -> Window -> View**. Panel fetches its own data with its own (window, interval, firm) triple. Firm remains shared (from Wave 2 page-level picker). Assets Overview and Segment Analytics are fully decoupled afterwards — changing one's window/interval does not affect the other.
  </objective>

  <context>
    State ownership after Wave 3:

    | State | Owner |
    |-------|-------|
    | `selectedFirmId` | AdvisorIntelligence.tsx root (render in page header per Wave 2) |
    | `timeWindow` (Assets Overview) | PartnerAnalytics local (per Wave 2) |
    | `granularity` (Assets Overview) | PartnerAnalytics local (per Wave 2) |
    | `timeWindow` (Segment Analytics) | DistributionTab local (NEW) |
    | `granularity` (Segment Analytics) | DistributionTab local (NEW) |
    | `mode (AUA/NNA)` | DistributionTab (existing) |
    | `view (Snapshot/Continuous)` | DistributionTab (existing) |

    DE may bundle Wave 3 with Wave 2 in a single commit per CTO discretion (cross-domain `<none/>`); if split, ship Wave 2 first then Wave 3. ADVI_OTHDED.001 also touches DistributionTab.tsx (different region: `enforceTop9Other`) — OTHDED should land first (already pending).

    Toggle values per PRD:
    - Mode: `AUA` / `NNA`
    - Interval: `Month` / `Quarter` / `Year`
    - Window: `1Y` / `3Y` / `Max`
    - View: `Snapshot` / `Continuous`
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-blast DistributionTab.tsx` — COO pre-check: 3 endpoints, 1 Lambda, 6 downstream.
    - `comp-transform schema-check DistributionTab` — COO pre-check PASS, all rendered fields typed.

    Phase 2 (before committing):
    - Re-run `comp-blast DistributionTab.tsx` — should be unchanged or narrower.
    - tsc + lint clean.

    Phase 3 (after committing):
    - `/frontend-dev` closed-loop pass: toggle order visible (Mode/Interval/Window/View), independence verified by flipping one panel's window and confirming the other does NOT change, firm propagation unchanged.

    Log runs to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- Frontend only. Sequencing with ADVI_OTHDED.001 (different region of same file): OTHDED first, then HDRSPL.003. DE manages the rebase if in parallel. -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Segment Analytics panel header renders toggles in EXACT order Mode -> Interval -> Window -> View (left-to-right).
    2. `timeWindow` and `granularity` are local state inside DistributionTab (new `useState`).
    3. Changing Assets Overview Window from 1Y to 3Y does NOT change Segment Analytics chart data.
    4. Changing Segment Analytics Window from 1Y to 3Y does NOT change Assets Overview chart data.
    5. Firm picker change still propagates to both panels.
    6. Segment Analytics fetches with its own (window, interval, firm) triple.
    7. No TypeScript errors, no ESLint errors, no new console warnings.
    8. `/frontend-dev` visual test confirms toggle order + panel independence.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
    </files>
  </scope>

  <requirements>
    - Toggle order is NOT negotiable: Mode -> Interval -> Window -> View. Verified visually in Phase 3.
    - Use existing panel-internal control styling (these toggles live inside the dark panel, NOT on silver bg — do NOT use `<PageSurfaceControl>` here).
    - No endpoint or response-shape changes.
  </requirements>

  <deliverables>
    - Commit (or part of Wave 2 bundle) to portal DEV with agent author.
    - Session log with Compiler Tools section + independence validation.
    - `org/compiler-tools-log.md` entries.
    - Flip `<status>` staged -> pending on GO (or on Wave 2 completion if bundled), then -> complete after acceptance criteria 1-8.
  </deliverables>

  <do_not>
    - Do NOT alter Assets Overview behavior.
    - Do NOT use `<PageSurfaceControl>` here — that primitive is for page-background surfaces, not in-panel toggles.
    - Do NOT change Mode/View behavior — they already exist; only add Interval/Window controls next to them in the specified order.
  </do_not>
</task_order>
