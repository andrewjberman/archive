<task_order>
  <metadata>
    <id>ADVI_INFFIN.019</id>
    <slug>dsc-cost-basis-tax-status-reconciliation-investigation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>IMMEDIATE — DS~C bench-clear post BPMVH D-max β + INFFIN.018 record-velocity ship. Andrew direct "decompose CTOs new PRD into TOs and get them pushed along" override of post-bundle-close staging.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Andrew empirical reconciliation gap; "many numbers don't make sense" verbatim</priority>
    <sla>~3-5h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.1 (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ image #2 walkthrough: "Some DS needs to look into all of these numbers and how they're calculated because many don't make sense, specifically capital gains, cost basis by year, and the aggregations."</ref>
    <ref type="sister_pattern">ADHC_BPMVH D-max β bronze+pmv reconciliation (`7be0dda7e`) — same DS lane sister-class pattern</ref>
    <ref type="surface">Inflection portal → AdvisorIntelligence → Books tab → COST BASIS & TAX STATUS panel</ref>
  </references>

  <context>
    Andrew 6-image walkthrough surfaced reconciliation gap on Inflection Books tab Cost Basis panel. Empirical anomalies:
    - AUA by Tax Status total: ~$165.6M ($42.6M Taxable + $109M Tax Deferred + $14M Tax Free) — matches firm AUA ~$203M minus excluded scope
    - Capital Gains (TTM): -$54.9M (large negative; reasonableness suspect)
    - Cost Basis By Year totals: $1.31B — 8x larger than AUA-by-Tax-Status; doesn't reconcile structurally
    - 2026 row (partial year) $291M cost basis — overstated vs 2025 $288M (implausible partial-year inversion)
    - Unrealized: $27.4M cost basis / +$8.05M gain
    - Realized: $37M cost basis / +$3.10M gain

    Five hypotheses from PRD §3.1 (DS investigates empirically):
    1. Lot-level vs account-level summation drift (multiple lots → cost basis duplication)
    2. Tax-status filter scope mismatch (top-tile filters to tax-aware accounts; CBBY may include all)
    3. Date-window scope mismatch (TTM realized vs all-time unrealized)
    4. Source artifact divergence (gold scripts emit incompatible cost-basis grain)
    5. Currency / units error ($1.31B could be cents-vs-dollars conversion)

    Per CLAUDE.md Rule 14+15: ds-commit-gate.sh + `from __future__ import annotations` first import for any new/modified DS scripts.
  </context>

  <objective>
    Empirical investigation of Inflection cost basis reconciliation gap. Root-cause identification per 5-hypothesis sweep OR new finding. Output: brief at `docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md` with empirical findings + recommended fix scope for INFFIN.020 cascade.
  </objective>

  <scope>
    <files>
      <file action="create">docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md — investigation brief output</file>
      <file action="readonly_reference">data/orion/scripts/gold/{cost-basis-emitting scripts} — empirical inspection</file>
      <file action="readonly_reference">platinum/inflection/firm/{cost-basis artifacts} — current emit shape</file>
      <file action="readonly_reference">portal FE Books tab cost basis components — read path</file>
    </files>
  </scope>

  <phase id="1" when="empirical surface">
    <step>
      <run>comp-pipescript io {gold scripts emitting cost basis fields} — surface current emit shape + consumers</run>
      <expect>Identify which gold scripts emit cost_basis fields; trace to platinum artifact paths; surface FE consumer wiring.</expect>
    </step>
    <step>
      <run>S3 inspect current Inflection platinum artifacts: aws s3 cp s3://opal-data-inf/platinum/firm/{cost_basis*} - | head; verify schema vs FE expectation</run>
      <expect>Empirical platinum shape vs PRD-cited screenshot values reconciled. If unit-scale ($1.31B implausible) immediately surfaces $1.31M vs $1.31B unit conversion issue, branch to Hyp #5.</expect>
    </step>
    <step>
      <run>Cross-check: aws s3 cp s3://opal-data-inf/platinum/firm/{aua_by_tax_status*} - and verify $165.6M total reconciles to Books tab top-tile</run>
      <expect>AUA-by-Tax-Status confirmed; baseline anchor for cost basis reconciliation expectation.</expect>
    </step>
  </phase>

  <phase id="2" when="hypothesis sweep">
    <step>
      <run>Hyp #1 lot-level vs account-level: SELECT distinct grain check — sum cost basis by account vs sum by (account, lot); divergence = duplication signal</run>
      <expect>Either: account-level grain confirmed AND CBBY $1.31B mismatch unexplained → continue. Or: lot-level grain detected → duplication root cause confirmed.</expect>
    </step>
    <step>
      <run>Hyp #2 filter scope: compare cohort filter on top-tile AUA-by-Tax-Status vs CBBY emit; check if CBBY includes excluded account types</run>
      <expect>Filter divergence quantified or ruled out.</expect>
    </step>
    <step>
      <run>Hyp #3 date-window: parse TTM-realized window vs all-time-unrealized window on Capital Gains panel; verify whether $-54.9M is realized OR realized+unrealized</run>
      <expect>Window scope clarified. Likely fix: separate TTM realized vs all-time unrealized presentation.</expect>
    </step>
    <step>
      <run>Hyp #4 source divergence: comp-pipescript io for each cost-basis-emitting script; verify cross-script schema consistency</run>
      <expect>Source divergence identified OR ruled out.</expect>
    </step>
    <step>
      <run>Hyp #5 units: spot-check sample value at lot level vs portal display; $1.31B / $1.31M? cents vs dollars?</run>
      <expect>Unit-scale confirmed. If cents-as-dollars detected ($1.31B should be $13.1M), root cause = units error (likely simplest fix).</expect>
    </step>
    <step>
      <run>Partial-year 2026 $291M vs 2025 $288M plausibility: check if 2026 row aggregates as YTD-only OR includes prior-year acquisitions still held</run>
      <expect>Year-row aggregation semantic clarified. Tooltip wording fix vs data fix decision.</expect>
    </step>
  </phase>

  <phase id="3" when="brief authoring">
    <step>
      <run>Author docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md:
        - Empirical findings per 5 hypotheses (PASS/FAIL each)
        - Root cause(s) identified
        - Recommended fix scope for INFFIN.020 cascade (gold-script update? FE tooltip wording? schema rename?)
        - Reconciliation table: AUA-by-Tax-Status vs CBBY vs Capital Gains TTM expected reconciliation
        - 49F regression risk assessment (does same fix apply to 49F? new partner scope?)
        - No emoji per CLAUDE.md</run>
      <expect>Brief 2-4 pages; investigation evidence-bearing; clear fix scope for cascade TO.</expect>
    </step>
    <step>
      <run>safe-commit.sh per Rule 14a; author DS~C identity; commit brief + any investigation scripts/queries</run>
      <expect>Brief committed; ds-commit-gate PASS for any .py scripts authored.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DS~C self-cascade-trigger for INFFIN.020 fix authoring</run>
      <expect>Evidence-bearing close with commit SHA + investigation findings summary.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md authored
    AC2: 5-hypothesis sweep evaluated (PASS/FAIL each with empirical evidence)
    AC3: Root cause(s) identified OR new finding documented if outside hypothesis space
    AC4: AUA-by-Tax-Status ($165.6M) vs CBBY ($1.31B) reconciliation explanation
    AC5: Capital Gains (TTM) -$54.9M plausibility check vs external Orion-side report
    AC6: 2026 partial-year vs 2025 plausibility resolved (tooltip vs data fix)
    AC7: Recommended INFFIN.020 fix scope (gold script? FE? schema?) clearly stated
    AC8: 49F regression risk assessment
    AC9: ds-commit-gate.sh PASS if any .py authored
    AC10: safe-commit.sh PASS
    AC11: RAVC2 to COO + CC CTO
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 comp-pipescript io reference; Phase 2 hypothesis sweep with empirical S3 / DB queries; Phase 3 ds-commit-gate + safe-commit.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: None (pure investigation).
    PARALLEL-OK: INFFIN.021 (DS~D Top Gain Positions); INFFIN.022-024 (RD Wave 1 staged post-H3); INFFIN.028 (DE MAX anchor immediate).
    OWNED-PATHS: docs/briefs/ is COO/CTO authoring lane; DS~C commit acceptable per author identity attribution.
    CASCADE: INFFIN.020 fix scope determined by this brief's recommendation.
    DS SUB-AGENT ROUTING: DS~C primary per record-velocity day + reconciliation-investigation expertise (BPMVH D-max sister-class).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Investigation only; no platinum re-emit until INFFIN.020 fix.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Investigation brief at docs/briefs/data-scientist-inflection-cost-basis-investigation-20260514.md
    2. Root cause(s) + recommended INFFIN.020 fix scope
    3. Reconciliation table (AUA-by-Tax-Status vs CBBY vs Capital Gains TTM)
    4. 49F regression risk assessment
    5. RAVC2 with empirical findings
  </deliverables>

  <ravc>DS~C RAVC2 to COO + CC CTO on AC1-11 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"`.

    **Investigation-first discipline:** per banked feedback `feedback_phantom_consumer_marker_pattern.md` + `feedback_to_scope_none_of_above_space.md` — leave none-of-the-above space; if 5-hypothesis sweep doesn't surface root cause, document new finding empirically rather than force-fit to options.

    **Sister-class BPMVH pattern:** D-max β bronze+pmv reconciliation (`7be0dda7e`) used decomposition-of-gap empirical approach. Same pattern likely applies here: decompose $1.31B - $165.6M = $1.14B into named categories (lot-duplication / unit-scale / scope-divergence).

    **No emoji per CLAUDE.md.** Plain ASCII log prefixes.

    **Brief output → INFFIN.020 cascade:** investigation scope only; fix scope cascades via dispatch_held=true INFFIN.020 unlocked by this RAVC2.
  </notes>
</task_order>
