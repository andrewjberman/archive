<task_order>
  <metadata>
    <id>ADVI_INFFIN.022</id>
    <slug>rd-executive-summary-aggregate-flag-removal</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RD 0.4.2 bench-clear post H3 FE patch close (Cottonwood (a) Track B Peter Lee chip-render). Wave 1 RD batch dispatch_held until H3 RAVC.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Andrew direct FE rewire; data already exists per Andrew</priority>
    <sla>~30-60min wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.3 (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ: "we shouldnt need that 'Aggregate' flag here, this should be a frontend edit, we alreayd have lifetime accurate NNA per advisor split by total/fee/no fee"</ref>
    <ref type="surface">Inflection portal → AdvisorIntelligence → Executive Summary FLOWS section</ref>
  </references>

  <context>
    Executive Summary FLOWS section currently displays Inflows / Outflows / NNA with "AGGREGATE QTD" pill indicator. Andrew wants pill removed; NNA values re-sourced from existing per-advisor lifetime-accurate NNA split (total/fee/no fee) data which is already emitted.

    FE-only rewire. No backend data change required per Andrew.
  </context>

  <objective>
    Remove "AGGREGATE" pill from FLOWS section header. Re-source Inflows / Outflows / NNA from existing per-advisor NNA split data (total/fee/no fee). Wire Fees toggle (All / Fee-Paying / No Fee) to drive split slice selection.
  </objective>

  <scope>
    <files>
      <file action="modify">portal FE — Executive Summary FLOWS section component (PartnerAnalytics or similar)</file>
      <file action="readonly_reference">existing per-advisor NNA split data source (total/fee/no fee)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-transform schema-check {FlowsSection component} — verify field availability + consumer wiring</run>
      <expect>Pill source identified; per-advisor NNA split source identified.</expect>
    </step>
    <step>
      <run>grep portal FE for AGGREGATE pill component reference</run>
      <expect>Pill location surfaced.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Remove "AGGREGATE" pill from FLOWS section header</run>
      <expect>Pill no longer rendered.</expect>
    </step>
    <step>
      <run>Re-source Inflows / Outflows / NNA to existing per-advisor lifetime-NNA split (total/fee/no fee) sum</run>
      <expect>FLOWS values now pull from per-advisor data; sum firm-wide.</expect>
    </step>
    <step>
      <run>Wire Fees toggle (All / Fee-Paying / No Fee) to drive split slice selection</run>
      <expect>Toggle correctly filters FLOWS values.</expect>
    </step>
    <step>
      <run>Verify QTD window selector behavior unchanged</run>
      <expect>No regression on QTD selector.</expect>
    </step>
  </phase>

  <phase id="3" when="visual smoke + commit">
    <step>
      <run>Visual smoke: Inflection + 49F Executive Summary FLOWS section render correctly with new wiring; QTD values match firm-wide sum of per-advisor data</run>
      <expect>Both partners visually clean.</expect>
    </step>
    <step>
      <run>safe-commit.sh per Rule 14a + Author identity RD 0.4.2</run>
      <expect>Commit clean.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4 (PROD promote candidate)</run>
      <expect>Evidence-bearing close + visual smoke evidence.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: "AGGREGATE" pill no longer visible in FLOWS section
    AC2: Inflows / Outflows / NNA values pull from existing per-advisor lifetime-NNA split data
    AC3: Fees toggle (All / Fee-Paying / No Fee) correctly filters FLOWS values
    AC4: QTD window selector unchanged behavior
    AC5: No backend data change required (data already exists)
    AC6: 49F regression smoke PASS
    AC7: Inflection visual smoke PASS
    AC8: No emoji per CLAUDE.md
    AC9: RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 comp-transform schema-check; Phase 3 safe-commit.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: RD 0.4.2 H3 FE patch close (current in-flight).
    PARALLEL-OK: All other INFFIN.019-028 sibs.
    NO BACKEND CHANGE.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE-only.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. AGGREGATE pill removed
    2. FLOWS re-sourced from per-advisor NNA split
    3. Fees toggle wired
    4. RAVC2 with visual smoke
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO + CC CTO + DT 0.4 on AC1-9 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
