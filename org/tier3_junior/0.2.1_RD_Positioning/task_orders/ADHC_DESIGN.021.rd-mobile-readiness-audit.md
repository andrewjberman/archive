# Task Order: Positioning Mobile Readiness Audit

<task_order>
  <metadata>
    <id>ADHC_DESIGN-021</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.1_RD_Positioning</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <project>ADHC_DESIGN</project>
    <phase>3</phase>
  </metadata>

  <objective>
    Produce a structured audit of everything in the Positioning page that would
    break, degrade, or be unusable on a small screen (375px-428px). Read-only
    audit -- no code changes. Deliverable feeds CTO's ADHC_MOBILE PRD.
    Also identify design flaws and holistic enhancement opportunities.
  </objective>

  <references>
    <ref type="prd">docs/architecture/PORTAL_DESIGN_NORMALIZATION_AND_COMPILER_TOOLS.md</ref>
    <ref type="design-qa">org/ref/design/PORTAL_DESIGN_QA.md</ref>
  </references>

  <scope>
    <pages>
      <page>portal/src/pages/Positioning/</page>
    </pages>
  </scope>

  <requirements>
    <requirement id="1">**Fixed-width audit**: Every hardcoded width. File:line and current value.</requirement>
    <requirement id="2">**Hardcoded height audit**: Every fixed height constraining chart/panel sizing.</requirement>
    <requirement id="3">**Non-responsive grid audit**: Grid/flex without breakpoint variants. What happens at 375px?</requirement>
    <requirement id="4">**Touch target audit**: Every clickable element. Flag under 44px.</requirement>
    <requirement id="5">**Chart audit**: Container sizing, ResponsiveContainer, axis labels at 375px, legend overlap.</requirement>
    <requirement id="6">**Table audit**: Column count, width, scroll wrapper, truncation, sticky columns.</requirement>
    <requirement id="7">**Text/content audit**: Long text, tooltips, font sizes below 12px.</requirement>
    <requirement id="8">**Design flaws**: Layout anti-patterns, inconsistent spacing, unnecessary nesting.</requirement>
    <requirement id="9">**Enhancement opportunities**: Collapsible sections, progressive disclosure, swipeable areas.</requirement>
  </requirements>

  <deliverable>
    Write to: `org/tier3_junior/0.2.1_RD_Positioning/deliverables/mobile_readiness_audit.md`

    Use same structure: Summary, Critical Issues, Warnings, Touch Targets, Charts, Tables, Design Flaws, Enhancements. All with file:line refs.
  </deliverable>

  <acceptance_criteria>
    <criterion id="1">Every .tsx/.ts file covered</criterion>
    <criterion id="2">File:line references for every finding</criterion>
    <criterion id="3">No code changes</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read-only audit. No code modifications.</constraint>
  </constraints>

  <commit_pattern>audit(Positioning): mobile readiness assessment for ADHC_MOBILE</commit_pattern>
</task_order>
