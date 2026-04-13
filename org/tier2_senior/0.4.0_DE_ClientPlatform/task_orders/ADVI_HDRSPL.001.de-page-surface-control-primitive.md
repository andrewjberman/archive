<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-13-hdrspl-001</id>
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

  <objective>
    Wave 1 of 3. Introduce the reusable `<PageSurfaceControl>` primitive: high-contrast (indigo solid, WCAG AA >= 4.5:1 against silver page background), shape-polymorphic (button / dropdown / toggle-group), sized to match existing panel-internal controls. First concrete variant: `solid-indigo`. No integration into ADVI yet — that is Wave 2/3.
  </objective>

  <context>
    The ADVI page background is silver; existing panel-internal controls are dark-surface-tuned. PRD Wave 2 moves the firm picker out to the page level, which requires a primitive readable on silver. Wave 1 delivers only the primitive + its visual/contrast validation so Wave 2 has a stable dependency.

    Component path is DE's call based on existing conventions (likely `portal/src/components/ui/` or `portal/src/lib/ui/`). Shape contract per PRD:
    ```tsx
    <PageSurfaceControl variant="solid-indigo" as="dropdown"
      label="Firm" value={selectedFirmId} options={firmOptions} onChange={...} />
    <PageSurfaceControl variant="solid-indigo" as="toggle-group"
      label="Window" value={w} options={['1Y','3Y','Max']} onChange={...} />
    ```

    Visual spec: indigo 600/700 bg, white fg, hover/active one step darker, border radius + padding matching existing in-panel controls. Pass WCAG AA against silver page bg.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - Grep `portal/src/components/` and `portal/src/lib/` for existing control primitives to choose the canonical location.
    - `comp-transform schema-check` any existing component you plan to pattern after (optional; primitive has no endpoint dep).

    Phase 2 (before committing):
    - `comp-blast` on the new primitive file — should have zero consumers at Wave 1 ship (primitive only; Wave 2 wires it).
    - tsc + lint clean.

    Phase 3 (after committing):
    - `/frontend-dev` visual-test pass against a demo/storybook page (or an ad-hoc test route) rendering each shape with `variant="solid-indigo"` on silver bg.
    - Measured and reported WCAG AA contrast ratio numerically.

    Log every run to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- Primitive only. No integration into ADVI in this TO. -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `<PageSurfaceControl>` exported from the chosen component-library path.
    2. Supports `as="button" | "dropdown" | "toggle-group"` with consistent sizing.
    3. `variant="solid-indigo"` renders white-on-indigo with hover/active states one step darker.
    4. `/frontend-dev` reports WCAG AA contrast ratio >= 4.5:1 against silver page bg. Numeric ratio recorded in session log.
    5. No TypeScript errors, no ESLint errors, no new console warnings.
    6. Primitive has a demo/test route exercising all three shapes.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">portal/src/components/ui/PageSurfaceControl.tsx (or DE-chosen canonical path)</file>
      <file action="create">portal/src/components/ui/__tests__/PageSurfaceControl.demo.tsx (or analogous test/demo route)</file>
    </files>
  </scope>

  <requirements>
    - Primitive is self-contained and reusable — no ADVI-specific coupling.
    - Variant system is open for future variants (not hardcoded to solid-indigo only).
    - Sizing matches existing in-panel control metrics so Wave 2 drop-in looks visually balanced.
  </requirements>

  <deliverables>
    - Commit to portal DEV with `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.
    - Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-13/hdrspl_001_page_surface_control.md` with Compiler Tools section (including measured contrast ratio).
    - Append compiler runs to `org/compiler-tools-log.md`.
    - Flip `<status>pending</status>` -> `complete` after acceptance criteria 1-6 validated.
  </deliverables>

  <do_not>
    - Do NOT integrate into ADVI in this TO (Wave 2 work).
    - Do NOT hardcode indigo shade; use a variant token so other shades can be added later.
    - Do NOT skip `/frontend-dev` — contrast ratio is a gating criterion.
  </do_not>
</task_order>
