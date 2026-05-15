<task_order>
  <metadata>
    <id>ADVI_INFFIN.028</id>
    <slug>de-rd-max-window-anchor-2021-q1-combined</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform + 0.4.2_RD_AdvisorIntelligence (joint)</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>IMMEDIATE for DE 0.4 (bench-clear post FECACHE_COHERENCE Phase 2a Q2 ship). RD 0.4.2 propagation phase gated on DE shared-constant commit + RD H3 patch close. Andrew direct "push them along" override.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — cross-ADVI architectural constant; Andrew verbatim "MAX across ADVI should be 2021 Q1, anywhere that says max"</priority>
    <sla>~30-60min wall total (DE constant ~10min + RD propagation ~30min)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFFIN_UX_FIXES_BATCH.md §3.7 (CTO `23fdaac67`)</ref>
    <ref type="andrew_direct">Andrew 2026-05-14 ~23:0XZ: "I think MAX across ADVI should be 2021 Q1, and that goes for 49 and Inflection, anywhere that says max."</ref>
    <ref type="cto_lean">CTO PRD §3.7: shared constant for now (not TenantLayoutConfig per-partner); add per-partner override only if real partner needs later anchor</ref>
  </references>

  <context>
    Cross-ADVI system-wide constant change. Every MAX button currently anchors to "earliest available data" which varies per surface. Andrew wants hardcoded anchor at 2021 Q1 across ALL MAX selectors in AdvisorIntelligence (49F + Inflection).

    Affects: PartnerAnalytics Executive Summary Fees Window selector / Segment Analytics Snapshot Window selector / Books Cost Basis Window selector / Books Fee Summary Window selector / Continuous View Window selector.

    Combined TO routing per COO Q4 ratify: DE shared-constant emit + RD propagation as single deliverable (vs split per CTO suggested .028 + .029). Wall sub-1h artificially split would create 2x RAVC handshake overhead.
  </context>

  <objective>
    DE 0.4 emits shared constant `ADVI_MAX_WINDOW_ANCHOR = '2021-Q1'` (or equivalent ISO/quarterly format) in `_shared/constants/` location. RD 0.4.2 propagates across 5+ consumer sites in AdvisorIntelligence routing surfaces.
  </objective>

  <scope>
    <files>
      <file action="create" lane="DE">portal/src/_shared/constants/advi-window-anchors.ts (or per existing constants location) — emit ADVI_MAX_WINDOW_ANCHOR constant</file>
      <file action="modify" lane="RD">portal FE — PartnerAnalytics ExecutiveSummary Fees Window selector</file>
      <file action="modify" lane="RD">portal FE — Segment Analytics SnapshotWindow selector</file>
      <file action="modify" lane="RD">portal FE — Books CostBasisWindow selector</file>
      <file action="modify" lane="RD">portal FE — Books FeeSummaryWindow selector</file>
      <file action="modify" lane="RD">portal FE — Continuous View Window selector</file>
    </files>
  </scope>

  <phase id="1" when="DE shared constant emit">
    <step>
      <run>comp-transform schema-check (or grep) for existing constant location conventions in portal/_shared/</run>
      <expect>Existing constants pattern source identified.</expect>
    </step>
    <step>
      <run>DE authors: const ADVI_MAX_WINDOW_ANCHOR = '2021-Q1' (or Date('2021-01-01') equivalent per existing date format conventions); export from shared constants module</run>
      <expect>Single-source constant available for FE consumers.</expect>
    </step>
    <step>
      <run>DE safe-commit.sh per Rule 14a + Author identity DE 0.4</run>
      <expect>Constant committed; available for RD propagation phase.</expect>
    </step>
  </phase>

  <phase id="2" when="RD propagation">
    <step>
      <run>grep portal FE for MAX selector consumers: '\.\.\.MAX' OR 'maxWindow' OR 'earliestDate' OR similar patterns; surface 5+ consumer sites per PRD §3.7</run>
      <expect>All consumer sites enumerated.</expect>
    </step>
    <step>
      <run>Replace each consumer's dynamic-earliest-data MAX calculation with ADVI_MAX_WINDOW_ANCHOR import + use</run>
      <expect>5+ sites updated; uniform constant reference.</expect>
    </step>
    <step>
      <run>Verify backend implication: if any MAX-window-bound query computes earliest-date dynamically, that query should now use 2021-Q1 as lower bound. Investigation: any backend Lambda/script also reading MAX-window?</run>
      <expect>Backend MAX dependency surfaced OR ruled out. If backend dependency, cascade TO authored.</expect>
    </step>
    <step>
      <run>49F regression smoke: confirm no per-partner divergence; both 49F + Inflection MAX selectors anchor 2021 Q1 post-change</run>
      <expect>Cross-ADVI consistency verified.</expect>
    </step>
  </phase>

  <phase id="3" when="commit + RAVC">
    <step>
      <run>RD safe-commit.sh per Rule 14a + Author identity RD 0.4.2</run>
      <expect>Propagation commit clean.</expect>
    </step>
    <step>
      <run>Joint RAVC2 to COO + CC CTO + DT 0.4 (PROD promote candidate) — both DE + RD attestations</run>
      <expect>Evidence-bearing close with all 5+ consumer sites verified.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: ADVI_MAX_WINDOW_ANCHOR constant emitted at portal _shared/constants/ location
    AC2: Constant value = 2021-Q1 (or ISO equivalent matching existing date format)
    AC3: 5+ FE consumer sites updated to import + use the constant (PartnerAnalytics + Segment Analytics + Books CB + Books Fee + Continuous View)
    AC4: All MAX selectors in AdvisorIntelligence (49F + Inflection) anchor to 2021 Q1
    AC5: No "earlier than 2021 Q1" data displays when MAX selected (boundary filter applied)
    AC6: Backend MAX dependency surfaced + ruled out OR cascade TO authored
    AC7: 49F regression smoke PASS
    AC8: Cross-ADVI consistency verified (PartnerAnalytics + Distribution + Books same anchor)
    AC9: safe-commit.sh PASS (both DE + RD commits)
    AC10: No emoji per CLAUDE.md
    AC11: Joint RAVC2 to COO + CC CTO + DT 0.4
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 comp-transform schema-check reference; Phase 2 grep + edit + 49F smoke; Phase 3 safe-commit.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: DE Phase 1 constant commit gates RD Phase 2 propagation.
    PARALLEL-OK: INFFIN.019 + .021 (DS lane).
    GATED: RD Phase 2 dispatch_held until RD H3 patch close (current in-flight).
    POTENTIAL BACKEND CASCADE: if Phase 2 surfaces backend MAX-bound query, cascade TO INFFIN.028b for AE/DE.
    JOINT RAVC: single TO with both DE + RD attestations; no split into .028 + .029.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Pure FE constant propagation; no platinum re-emit needed. Backend MAX dependency (if any) handled via cascade.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. DE shared constant emit at _shared/constants/
    2. RD propagation across 5+ FE consumer sites
    3. Backend MAX dependency assessment
    4. 49F regression smoke evidence
    5. Joint RAVC2 with both attestations
  </deliverables>

  <ravc>DE 0.4 + RD 0.4.2 joint RAVC2 to COO + CC CTO + DT 0.4 on AC1-11 PASS.</ravc>

  <notes>
    **Author identity DE:** `--author="0.4.0_DE_ClientPlatform <0.4.0_DE_ClientPlatform@opal.agent>"`.
    **Author identity RD:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`.

    **Why combined TO:** sub-1h total wall artificially split into 2 TOs = 2x RAVC overhead per banked discipline. Single TO with DE Phase 1 → RD Phase 2 sequential within TO scope.

    **TenantLayoutConfig deferred:** per-partner override only if real partner needs later anchor. CTO lean shared constant first; flexibility added later when needed.

    **No emoji per CLAUDE.md.**
  </notes>
</task_order>
