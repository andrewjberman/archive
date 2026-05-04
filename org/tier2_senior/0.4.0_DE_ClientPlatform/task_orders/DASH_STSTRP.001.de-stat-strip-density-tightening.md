<task_order>
  <metadata>
    <id>DASH_STSTRP.001</id>
    <project>DASH_STSTRP</project>
    <title>Stat-Strip Density Tightening — 4-file CSS class diff (Option A)</title>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>pending</status>
    <priority>P2 — visual consistency cleanup; not blocking any current pipeline work</priority>
    <estimated_effort>0.5d (3h CSS edit + Surface Laptop validation; CSS-only diff, no logic changes)</estimated_effort>
  </metadata>

  <context>
    Andrew chose Option A 2026-05-04 from a 7-option set (A-G) over alternatives. Tighten existing
    single-row stat-strip density across 4 portal sites so the 6-element bell-curve variants stop
    wrapping on Surface Laptop and the 4-element variants align to the same density.

    PRD: `docs/architecture/PORTAL_STAT_STRIP_DENSITY.md` (CTO commit `01de2e5b5`).
    Project JSON: `org/projects/DASH_STSTRP.json`.

    DASH_STSTRP_V2 — shared `<MetricStrip>` primitive extraction — is DEFERRED until Option A
    bakes one nightly cycle. Do NOT extract a shared component in this TO; keep the 4 files in
    lockstep with verbatim diffs and rely on reviewer discipline meanwhile.

    Compiler evidence (PRD §5): `comp-transform schema-check ConsolidatedOverviewPanel` clean;
    AccountDistributionMetrics + AUMGrowthMetrics not in graph (props-only presentational); no
    API contract or data-path risk; CSS-only diff is type-safe.
  </context>

  <objective>
    Apply the §3 class diff verbatim to all 4 files in PRD §2 in a single commit. No logic changes,
    no font-size reductions on labels/values, no semantic changes. Validate on Surface Laptop
    emulation via `/frontend-dev` and on actual hardware (RD sign-off).
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>4-file class diff applied verbatim</title>
      <detail>
        All 4 files carry the PRD §3 class diff exactly:
        - `portal/src/components/AccountDistributionMetrics.tsx` (Model Portfolios — Client Holdings bell curve, 6-element)
        - `portal/src/pages/AdvisorIntelligence/_shared/tabs/DistributionTab.tsx` lines 3895–3990 (`SnapshotDistributionMetrics` inline, 6-element with vs-current deltas)
        - `portal/src/components/AUMGrowthMetrics.tsx` (AUA by Model radial sibling, 4-element)
        - `portal/src/pages/AdvisorIntelligence/_shared/panels/ConsolidatedOverviewPanel.tsx` lines 126+ (Firm/Advisor/Relationship Overview header strip, 4-element)

        Per-element diffs (PRD §3 table):
        - Inner flex row: `gap-x-4 gap-y-3` → `gap-x-2 gap-y-2`
        - Anchor pill: `px-4 py-1.5 ... min-w-[100px]` → `px-3 py-1 ... min-w-[88px]`
        - Anchor value text: `text-lg` → `text-base`
        - Standard pills: `min-w-[80px]` → `min-w-[64px]`
        - Median pill: `px-3 py-1.5 ... min-w-[100px]` → `px-2 py-1 ... min-w-[88px]`
        - Pill labels (`text-xs`), pill values (`text-sm font-semibold`), median value (`text-base font-bold`), delta annotation (`text-[9px]`): UNCHANGED

        Outer shell unchanged: `w-full px-6 py-3 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center`.
      </detail>
    </ac>
    <ac id="2">
      <title>Surface Laptop single-row render (1366×912 emulation)</title>
      <detail>
        On Surface Laptop emulation in Chrome devtools (1366×912, default Opal sidebar):
        - Client Holdings bell-curve strip (AccountDistributionMetrics) renders on a single row, zero element wrapping
        - 49F Segment Analytics snapshot strip (SnapshotDistributionMetrics) renders on a single row, zero element wrapping
        Verified via `/frontend-dev` Playwright screenshots saved to `.frontend-dev-results/`.
      </detail>
    </ac>
    <ac id="3">
      <title>Cross-strip visual consistency</title>
      <detail>
        All 4 strips visually match each other in pill height, padding, gap on Surface Laptop +
        on a 1920×1080 desktop reference. Side-by-side screenshot comparison saved with the
        session log.
      </detail>
    </ac>
    <ac id="4">
      <title>Behavior unchanged</title>
      <detail>
        Element semantics (labels, currency formatting, color anchors, delta annotations) unchanged.
        Visual regression diff against pre-change screenshots: only spacing/padding/gap delta;
        no semantic / color / count / label changes.
      </detail>
    </ac>
    <ac id="5">
      <title>TypeScript + schema-check clean</title>
      <detail>
        - `bun run typecheck` (or `cd portal && bun run typecheck`) exits 0
        - `comp-transform schema-check ConsolidatedOverviewPanel` shows no NEW WARNs vs the PRD §5 baseline ("All rendered fields match their response types.")
        - AccountDistributionMetrics / AUMGrowthMetrics not in graph — schema-check N/A (expected; per PRD §5)
      </detail>
    </ac>
    <ac id="6">
      <title>RD Surface Laptop hardware sign-off (PRE-PROD gate)</title>
      <detail>
        Devtools emulation is necessary but not sufficient. Before PROD ship:
        - Hand off to RD (0.4.2_RD_AdvisorIntelligence) OR validate on Andrew's actual Surface
          Laptop hardware
        - RD captures real-hardware screenshots of all 4 strips on Surface Laptop default zoom +
          tab to next bell-curve page
        - RD signs off in TO completion comment OR you self-validate if you have hardware access

        Decision delegate: if you have Surface Laptop access, self-validate is fine. If not, fork
        to RD via brief MCP after your typecheck/schema-check gates pass — RD scope is read-only
        screenshot capture, no code edits.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_edit">
      <step>
        <run>comp-transform schema-check ConsolidatedOverviewPanel</run>
        <expect>"All rendered fields match their response types." (matches PRD §5 baseline)</expect>
        <if_mismatch>Capture diff from baseline; if NEW WARN appears, investigate before applying CSS diff (could indicate concurrent type drift)</if_mismatch>
      </step>
      <step>
        <run>comp-blast AccountDistributionMetrics</run>
        <expect>"No nodes matching" or empty downstream (props-only component, no graph nodes)</expect>
        <if_mismatch>If new graph nodes appeared since PRD authoring, surface to COO before proceeding</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>cd portal &amp;&amp; bun run typecheck</run>
        <expect>Exit 0; no new TypeScript errors</expect>
        <if_mismatch>Fix typecheck before commit; CSS class string changes shouldn't break types unless a class was deleted that something else referenced</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check ConsolidatedOverviewPanel</run>
        <expect>Same clean output as Phase 1</expect>
        <if_mismatch>Investigate any drift</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after_commit">
      <step>
        <run>/frontend-dev</run>
        <expect>Closed-loop Playwright run hits Model Portfolios + Advisor Intelligence Segment Analytics (Distribution tab) + 49F Firm Overview pages on Surface Laptop emulation; AC#2 + AC#3 visual gates PASS; results saved to `.frontend-dev-results/`</expect>
        <if_mismatch>Per /frontend-dev convention, the harness self-iterates fixes; if it can't resolve, surface to COO with screenshot evidence</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: pure portal frontend CSS-only diff. No Lambda, no Terraform, no EC2, no data
      pipeline. No data semantics change.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>Single commit applying §3 class diff to all 4 files (DE 0.4.0 author; portal submodule lane)</item>
    <item>`/frontend-dev` results captured under `.frontend-dev-results/` with Surface Laptop screenshots</item>
    <item>Side-by-side cross-strip consistency screenshot</item>
    <item>RD Surface Laptop hardware sign-off (or self-validation if you have hardware access)</item>
    <item>Session log with Compiler Tools section + AC matrix + screenshot paths</item>
    <item>RAVC4 MCP to COO with commit hash + screenshot evidence + AC matrix PASS</item>
  </deliverables>
</task_order>
