# Task Order: Macroeconomics Mobile Readiness Audit

<task_order>
  <metadata>
    <id>ADHC_DESIGN-019</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.5_RD_Macroeconomics</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project>ADHC_DESIGN</project>
    <phase>3</phase>
  </metadata>

  <objective>
    Produce a structured audit of everything in the Macroeconomics page that would
    break, degrade, or be unusable on a small screen (375px-428px). This is NOT a
    code change task. The deliverable is a report that feeds into the CTO's
    ADHC_MOBILE PRD for the Capacitor mobile app.

    Additionally, identify any design flaws, layout anti-patterns, or enhancement
    opportunities you see -- things that could be improved holistically regardless
    of mobile, with mobile readiness in mind.
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/Macroeconomics/</page>
    </pages>
  </scope>

  <requirements>
    <requirement id="1">**Fixed-width audit**: Find every hardcoded width (w-[Npx], w-[Nrem], min-w-[N], max-w-[N], gridTemplateColumns with px values). Report each with file:line and current value.</requirement>
    <requirement id="2">**Hardcoded height audit**: Find every fixed height that constrains chart/panel sizing (h-[Npx]). Note which are chart containers (may need responsive scaling) vs decorative (fine to keep).</requirement>
    <requirement id="3">**Non-responsive grid audit**: Find every grid/flex layout that uses fixed column counts without breakpoint variants (e.g., `grid-cols-3` without `sm:grid-cols-1`). Report what would happen at 375px.</requirement>
    <requirement id="4">**Touch target audit**: Find every clickable element (button, link, dropdown, tab, checkbox, toggle). Measure or estimate its tap area. Flag anything under 44px height.</requirement>
    <requirement id="5">**Chart audit**: For each chart (Recharts, ApexCharts, SVG), report: current container sizing, whether it uses ResponsiveContainer, axis label density (would labels overlap at 375px?), legend position (would it overlap the chart on mobile?).</requirement>
    <requirement id="6">**Table audit**: For each table, report: column count, total estimated width, whether it has horizontal scroll wrapper, whether any column has truncation, sticky columns.</requirement>
    <requirement id="7">**Text/content audit**: Find long text blocks, tooltips, or data labels that might overflow or become unreadable at small widths. Note any font sizes below 12px.</requirement>
    <requirement id="8">**Design flaw identification**: Beyond mobile, note any layout anti-patterns, inconsistent spacing, misaligned elements, unnecessary nesting, or patterns that could be simplified or improved holistically.</requirement>
    <requirement id="9">**Enhancement opportunities**: Identify places where the layout could be improved with a mobile-first mindset -- collapsible sections, progressive disclosure, swipeable areas, simplified views for small screens.</requirement>
  </requirements>

  <deliverable>
    Write the audit report to: `org/tier3_junior/0.2.5_RD_Macroeconomics/deliverables/mobile_readiness_audit.md`

    Structure:
    ```
    # Mobile Readiness Audit: Macroeconomics

    ## Summary
    (2-3 sentences: overall assessment of mobile readiness)

    ## Critical Issues (would break on mobile)
    | File:Line | Issue | Current Value | Impact at 375px |
    |-----------|-------|---------------|-----------------|

    ## Warnings (would degrade on mobile)
    | File:Line | Issue | Current Value | Recommendation |
    |-----------|-------|---------------|----------------|

    ## Touch Target Violations
    | File:Line | Element | Estimated Size | Minimum Required |
    |-----------|---------|----------------|------------------|

    ## Chart Responsiveness
    | Chart | Container | ResponsiveContainer? | Mobile Concern |
    |-------|-----------|---------------------|----------------|

    ## Table Responsiveness
    | Table | Columns | Est. Width | Scroll Wrapper? | Mobile Strategy |
    |-------|---------|------------|-----------------|-----------------|

    ## Design Flaws (not mobile-specific)
    (bulleted list)

    ## Enhancement Opportunities
    (bulleted list with rationale)
    ```
  </deliverable>

  <acceptance_criteria>
    <criterion id="1">Every .tsx/.ts file in the page directory is covered by the audit</criterion>
    <criterion id="2">Report includes file:line references for every finding</criterion>
    <criterion id="3">No code changes made -- this is audit only</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DO NOT modify any code. This is a read-only audit.</constraint>
    <constraint>Commit only the audit report file to parent CLOUD branch.</constraint>
  </constraints>

  <commit_pattern>audit(Macroeconomics): mobile readiness assessment for ADHC_MOBILE</commit_pattern>
</task_order>
