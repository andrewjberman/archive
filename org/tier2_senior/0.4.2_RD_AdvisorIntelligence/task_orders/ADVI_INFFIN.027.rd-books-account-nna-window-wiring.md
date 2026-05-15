<task_order>
  <metadata>
    <id>ADVI_INFFIN.027</id>
    <slug>rd-books-account-nna-window-wiring</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-14</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>RD 0.4.2 bench-clear post H3 FE patch close. Wave 2 dispatch parallel with .025 + DS lane.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Books tab Account NNA window selector wiring; Andrew direct walkthrough</priority>
    <sla>~1-2h wall actual per Pod 4 velocity</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.6c (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ image #7: "we should be able to do account nna for the qtd ytd max views"</ref>
    <ref type="surface">Inflection portal → AdvisorIntelligence → Books tab → Accounts Summary table</ref>
    <ref type="sister_to">INFFIN.025 (fee containers/summary); INFFIN.028 (MAX 2021 Q1 anchor — affects MAX window value)</ref>
  </references>

  <context>
    Window selector (QTD / YTD / MAX) on Books tab currently only affects Cost Basis Tax Status panel. Per Andrew direct, should also drive Account NNA values in Accounts Summary table. Per-window NNA per account similar to PartnerAnalytics flows pattern.
  </context>

  <objective>
    Wire QTD/YTD/MAX window selector to Account NNA column in Books tab Accounts Summary table. Per-window NNA per account renders based on selection.
  </objective>

  <scope>
    <files>
      <file action="modify">portal FE Books tab Accounts Summary table component</file>
      <file action="modify">portal FE Books tab window selector handler</file>
      <file action="readonly_reference">PartnerAnalytics flows window pattern (sister-pattern reference)</file>
      <file action="readonly_reference">platinum Inflection books artifact — verify per-window NNA emit availability</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>S3 inspect platinum books artifact: verify per-window account NNA values exist (qtd_nna / ytd_nna / max_nna or equivalent shape) per account</run>
      <expect>Per-window NNA emit shape verified OR cascade DS for emit augment.</expect>
    </step>
    <step>
      <run>grep PartnerAnalytics flows window pattern as sister-reference</run>
      <expect>Window-driven value pattern identified.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Wire QTD/YTD/MAX window selector to Account NNA column data binding; window selection drives NNA value per account</run>
      <expect>NNA column responds to window selector.</expect>
    </step>
    <step>
      <run>Verify MAX window uses ADVI_MAX_WINDOW_ANCHOR (per INFFIN.028 shared constant if shipped); cross-coordination with .028</run>
      <expect>MAX = 2021 Q1 per INFFIN.028; pre-.028 fallback to existing earliest-date.</expect>
    </step>
    <step>
      <run>Per-window NNA per account validation: sample account, verify QTD vs YTD vs MAX values differ correctly</run>
      <expect>Per-window NNA correctly per account.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + RAVC">
    <step>
      <run>Visual smoke: Inflection Books tab Accounts Summary NNA column responds to QTD/YTD/MAX</run>
      <expect>Visual smoke PASS.</expect>
    </step>
    <step>
      <run>49F regression: same component shared; verify 49F Books tab Accounts Summary unchanged behavior</run>
      <expect>49F regression PASS.</expect>
    </step>
    <step>
      <run>safe-commit.sh per Rule 14a + Author identity RD 0.4.2</run>
      <expect>Commit clean.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + DT 0.4</run>
      <expect>Evidence-bearing close.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Window selector (QTD / YTD / MAX) drives Account NNA column on Inflection Books tab
    AC2: Per-window NNA correctly per account
    AC3: MAX window anchor uses ADVI_MAX_WINDOW_ANCHOR if INFFIN.028 shipped (cross-coordination)
    AC4: 49F regression PASS
    AC5: Inflection visual smoke PASS
    AC6: No emoji per CLAUDE.md
    AC7: RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 grep + S3 inspect; Phase 3 safe-commit.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: RD H3 FE patch close.
    PARALLEL-OK: All other INFFIN.019-028 sibs.
    CROSS-COORDINATION: .028 MAX anchor constant if shipped before this TO; otherwise fallback to existing earliest-date.
    POTENTIAL CASCADE: if per-window NNA emit gap surfaced Phase 1, cascade DS TO authored.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>FE-only assuming per-window NNA emit exists; cascade DS if gap.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Window selector → Account NNA wiring
    2. Per-window NNA verification
    3. .028 cross-coordination evidence
    4. 49F regression
    5. RAVC2
  </deliverables>

  <ravc>RD 0.4.2 RAVC2 to COO + CC CTO + DT 0.4 on AC1-7 PASS.</ravc>

  <notes>
    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.

    **Sister-pattern:** PartnerAnalytics flows window pattern is the canonical reference.

    **Cross-with-.028:** if .028 ships first, MAX anchors 2021 Q1 here too. If this ships first, MAX uses existing earliest-date and .028 propagation will catch this site.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
