<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-3</id>
    <project>ADVI_INFTGT</project>
    <title>[P0] Reconcile AUA cut labels across panels — no two panels show conflicting AUA without explicit cut labels</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>P0 — partner-blocking</priority>
    <authorized_by>Andrew direct GO 2026-05-11; PRD ADVI_INFTGT v0.1 (1.0.0_SA_CTO)</authorized_by>
  </metadata>

  <context>
    Partner dashboard shows multiple AUA values that appear to conflict:
    - Firm Assets Overview: $201M (quarterly cut)
    - Snapshot Segment Analytics donut: $201M
    - Continuous Segment Analytics: $189M (state-tagged AUA, completeness gap)
    - Books Firm Overview radials: $203M (total_aua)
    Canonical total_aua = $202.96M. These are NOT bugs — they are different cuts
    (total_aua vs state_tagged_aua vs quarterly) but LOOK like bugs to a partner.
    Fix: label each panel with its cut name so partner reads them correctly.
    PRD §3.1 + §4 + TO-3 spec.
  </context>

  <scope>
    <step>Phase 1 — Compiler runs:
      `comp-transform schema-check PartnerAnalytics`
      `comp-transform schema-check DistributionTab`
      `comp-transform schema-check InflectionInsightsPanel`
      `comp-routes trace getFirmHeaderMetrics`
      `comp-cache collisions`
    </step>

    <step>Phase 2 — Panel-by-panel labeling (per PRD §4 + §3.1):
      - Firm Assets Overview ($201M Q2 '26 quarterly): label header as "(Quarterly cut)" or add chip
      - Snapshot Segment Analytics ($201M): either re-point to total_aua ($202.96M) OR label as quarterly
      - Continuous Segment Analytics ($189M): label header as "(State-tagged AUA, partial coverage)"
      - Books Firm Overview ($203M): confirm this reads from total_aua; no label change needed if correct
      - Add data_as_of chip to each panel header per PRD §3.1
    </step>

    <step>Portal: `bun install && bun run dev --port 5175` — visual verify no two panels
      show conflicting unlabeled values on the same page.</step>

    <step>Portal commit on submodule DEV branch + push.</step>

    <step>RAVC2 to COO with screenshots: before/after for each labeled panel.</step>
  </scope>

  <acceptance_criteria>
    1. No two panels show conflicting AUA values without explicit cut labels.
    2. Partner cannot read two contradicting headlines on the same page.
    3. data_as_of chips present on firm-level panels.
    4. Visual review: no layout breakage.
    5. Portal submodule commit on DEV.
    6. RAVC2 with before/after screenshots.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-transform schema-check PartnerAnalytics`
      `comp-transform schema-check DistributionTab`
      `comp-transform schema-check InflectionInsightsPanel`
      `comp-routes trace getFirmHeaderMetrics`
      `comp-cache collisions`
    </phase>
    <phase id="3" when="after commit">
      Visual diff against dashboard.json total_aua
    </phase>
  </compiler_tools_mandate>

  <notes>
    DS~A (label authority) is EOD — proceed with your best judgment on cut names per
    `docs/data/gold_runner_term_definitions.md`. Check the DDL doc for canonical terminology.
    If unsure on a specific cut, render "—" rather than wrong label.
  </notes>
</task_order>
