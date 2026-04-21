# Task Order: Attribution Mobile Readiness Audit

<task_order>
  <metadata>
    <id>ADHC_DESIGN-024</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.2_RD_Attribution</issued_to>
    <date>2026-04-07</date>
    <status>complete</status><!-- CANCELLED 2026-04-21 — surface not under active investment; see org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md §4. ADHC_DESIGN closed at 28/32 effective; Attribution + Valuation sub-pages deferred per Andrew directive (no product driver). 0.2.2_RD_Attribution agent not spawned; no code shipped. -->
    <project>ADHC_DESIGN</project>
    <phase>3</phase>
  </metadata>

  <objective>
    Produce a structured audit of everything in the Attribution page that would
    break, degrade, or be unusable on a small screen (375px-428px). Read-only
    audit -- no code changes. Deliverable feeds CTO's ADHC_MOBILE PRD.
    Also identify design flaws and holistic enhancement opportunities.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/Attribution/</page>
    </pages>
  </scope>

  <requirements>
    <requirement id="1">Fixed-width, hardcoded height, non-responsive grid, touch target, chart, table, text/content audits — all with file:line refs</requirement>
    <requirement id="2">Design flaws and enhancement opportunities</requirement>
  </requirements>

  <deliverable>
    Write to: `org/tier3_junior/0.2.2_RD_Attribution/deliverables/mobile_readiness_audit.md`
    Same structure as other Phase 3 audits.
  </deliverable>

  <acceptance_criteria>
    <criterion id="1">Every .tsx/.ts file covered</criterion>
    <criterion id="2">File:line references for every finding</criterion>
    <criterion id="3">No code changes</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Read-only audit. No code modifications.</constraint>
  </constraints>

  <commit_pattern>audit(Attribution): mobile readiness assessment for ADHC_MOBILE</commit_pattern>
</task_order>
