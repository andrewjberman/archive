<task_order>
  <metadata>
    <id>ADVI_INFFIN.012</id>
    <slug>rd-surface-8-reactive-toggle</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-13</date>
    <status>pending</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>RD bandwidth opens next session; data side (per-period parallel fee-split fields) NOT a prerequisite per scope-reduced approach (FE-side toggle filter from per-account is_fee_paying + book totals)</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — completes Surface #8 reactive Fee/NoFee/All toggle wiring (largest .006 scope-split item); existing "Fee-split data unavailable" banner is acceptable temp state; not demo-blocking</priority>
    <sla>~1.5-2h wall post-unblock; substantive scope across Executive Summary + Flows + Fee + Lifetime Activity + ClientsTable</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md §Surface #8 (Fee-Paying / No-Fee / All toggle reactive across AdvisorPublicProfile)</ref>
    <ref type="cto_routing">CTO INFFIN.006 RAVC2 triage 22:55Z — SCOPE-SPLIT to INFFIN.012 (Surface #8 + banner removal)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="cross_link">Sibling: .006 RD Phase 2 wiring (10/12 items ACCEPTED) + .011 cross-firm consolidation (companion scope-split)</ref>
    <ref type="adjacent_ships">DS~C INFFIN.003 c5d98d41f (per-client is_fee_paying boolean + book block fee_earning_aua/non_fee_earning_aua totals — Surface #8 toggle source data) + .010 5e5f18edd (extension)</ref>
  </references>

  <context>
    Surface #8 (from DE INFFIN brief) — Fee-Paying / No-Fee / All toggle must reactively partition every metric on AdvisorPublicProfile:
    - Executive Summary cards (AUA + accounts + clients + new_clients)
    - Flows panel (inflows + outflows + nna)
    - Fee block (already populated; should toggle-aware)
    - Lifetime Activity chart (split bars)
    - "Fee-split data unavailable — showing aggregate" banner removal

    Per CTO scope-reduced plan (CTO Q1 ratify on INFFIN.003): FE-side toggle filter from per-account `is_fee_paying` + `book.fee_earning_aua/non_fee_earning_aua` totals. NO per-period parallel fee-split emit required (DS~B audit confirmed 49F doesn't emit those either; FE drives reactivity).

    Per CTO INFFIN.006 RAVC2 22:55Z scope-split reasoning:
    - RD in flight ~2h+ on INFFIN cleanup
    - Surface #8 is 1.5-2h substantive scope (5+ metric surfaces)
    - 10 shipped items = strong RAVC2 closure for partner-demo smoke
    - Surface #8 NOT demo-blocking (banner is acceptable temp state)
    - Partial-reactive metrics would be worse UX than explicit banner

    DS~C INFFIN.003 emit provides the data source:
    - `book.fee_earning_aua` + `book.non_fee_earning_aua` (toggle-aware AUA splits)
    - `book.fee_earning_account_count` + `book.non_fee_earning_account_count`
    - `clients[].is_fee_paying` boolean (per-HH for ClientsTable filter)
    - `fee_summary.by_account[]` (per-account fee data for detailed views)
  </context>

  <objective>
    Wire `feeView` state (`'all' | 'fee_paying' | 'no_fee'`) through every metric accessor on AdvisorPublicProfile + ClientsTable + Lifetime Activity. Remove "Fee-split data unavailable" banner. Apply null-elimination FE rendering rule (no `—` em-dashes; real values or sentinels only).

    Source of truth: DS~C INFFIN.003 emit fields. FE-side filtering on `is_fee_paying` boolean for per-HH/per-account; FE-side delta math on book totals for advisor-aggregate metrics.
  </objective>

  <scope>
    <surfaces>
      <surface id="8">Reactive Fee/NoFee/All toggle across AdvisorPublicProfile + Lifetime Activity + ClientsTable</surface>
    </surfaces>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/inflection/AdvisorPublicProfile.tsx (or similar) — wire feeView through every metric accessor</file>
      <file action="modify">Executive Summary cards (AUA + accounts + clients + new_clients) — toggle-aware rendering</file>
      <file action="modify">Flows panel (inflows + outflows + nna) — toggle-aware rendering</file>
      <file action="modify">Fee block — toggle-aware (already mostly there; verify)</file>
      <file action="modify">Lifetime Activity chart — split bars or toggle-aware aggregate</file>
      <file action="modify">ClientsTable — filter HHs by `is_fee_paying` on toggle</file>
      <file action="remove">"Fee-split data unavailable — showing aggregate" banner</file>
    </files>
  </scope>

  <phase id="1" when="pre-unblock-verify">
    <run>Verify DS~C INFFIN.003 c5d98d41f + .010 5e5f18edd shipped + chain materialized (book block + is_fee_paying boolean + fee_summary in advisor book.json + per-client detail.json)</run>
    <expect>Source data confirmed in platinum artifacts post-chain.</expect>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Wire `feeView` state through AdvisorPublicProfile metric accessors. Executive Summary cards consume `book.fee_earning_aua` / `book.non_fee_earning_aua` / `book.total_aua` per toggle state.</description>
      <expect>Executive Summary cards re-render on toggle change.</expect>
    </step>
    <step>
      <description>Flows panel: filter inflows + outflows + nna by `is_fee_paying` on per-HH basis (sum across HHs matching toggle). Or consume per-period parallel emits if DS~C added them later (currently null per scope-reduced plan).</description>
      <expect>Flows panel re-renders on toggle change.</expect>
    </step>
    <step>
      <description>Lifetime Activity chart: split bars OR toggle-aware aggregate (depending on DS~C emit shape). Remove "Fee-split data unavailable" banner.</description>
      <expect>Lifetime Activity chart respects toggle state; banner removed.</expect>
    </step>
    <step>
      <description>ClientsTable: filter HHs by `is_fee_paying` on toggle. All clients / fee-paying only / no-fee only views.</description>
      <expect>ClientsTable filter works correctly.</expect>
    </step>
    <step>
      <description>Null-elimination sweep: no `—` em-dashes on any metric in any toggle state. Real values or sentinels (`$0` / `0 bps` / explicit "N/A" with reason) only.</description>
      <expect>Zero em-dashes; partner-portal compliance with Andrew's null-elimination rule.</expect>
    </step>
  </phase>

  <phase id="3" when="empirical-test">
    <step>
      <description>Smoke against all 4 Inflection advisors (peter_lee / patrick_scanlan / joe_brandenburg / inflection_wealth_management) × 3 toggle states. Visual diff each.</description>
      <expect>All 4 × 3 combinations render correctly.</expect>
    </step>
    <step>
      <description>tsc 0 errors + bun run dev smoke.</description>
      <expect>PASS.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: feeView toggle wired through Executive Summary cards (AUA + accounts + clients + new_clients).
    AC2: feeView toggle wired through Flows panel (inflows + outflows + nna).
    AC3: feeView toggle wired through Fee block.
    AC4: feeView toggle wired through Lifetime Activity chart.
    AC5: feeView toggle wired through ClientsTable filter.
    AC6: "Fee-split data unavailable — showing aggregate" banner removed.
    AC7: No `—` em-dashes on any metric in any toggle state across all 4 advisors.
    AC8: tsc 0 errors + bun run dev smoke per advisor × toggle state.
    AC9: Session log captures evidence + visual diff.
    AC10: MCP RAVC2 to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>Verify DS~C source data via S3 platinum pull</phase_1>
    <phase_2>comp-transform schema-check on accessor sites; tsc + bun run dev</phase_2>
    <phase_3>Visual diff smoke per advisor × toggle state (Class-D production-empirical discipline)</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES:
    - DS~C INFFIN.003 + .010 + chain materialization (source data present in platinum)
    - RD bandwidth opens next session

    PARALLEL ACTIVITY:
    - .011 cross-firm consolidation (companion scope-split; may share FE work with this TO if accessor patterns align)
    - AE 0.7 v1.7.56 Lambda mirror (Lambda parity for DS~C fields)

    NO PORTAL CONFLICT during dispatch_held; once unblocked, normal portal DEV → CLOUD cycle.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure FE wiring. No data emit changes; no Lambda redeploys; no chain re-fires.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. AdvisorPublicProfile feeView wiring (all 5+ metric surfaces)
    2. ClientsTable filter
    3. Lifetime Activity chart toggle-aware rendering
    4. Banner removal
    5. Null-elimination FE sweep
    6. Single or multiple commits under 0.4.2_RD_AdvisorIntelligence author
    7. tsc + bun run dev smoke evidence (Class-D production-empirical discipline)
    8. MCP RAVC2 to COO
  </deliverables>

  <ravc>
    RD 0.4.2 RAVC2 to COO post-AC1-10 PASS. COO ratifies + relays Surface #8 partner-visible closure to Andrew. INFFIN v0.1 close gate (Surface #8 was the last partner-visible defect class).
  </ravc>

  <notes>
    **Dispatch hold:** dispatch_held=true until RD next-session bandwidth. COO unblocks via MCP "INFFIN.012 dispatch unblocked; proceed."

    **CTO scope-split reasoning (captured for COO ledger):**
    - 12 items shipped this session = strong RAVC2 closure for partner-demo smoke
    - Surface #8 is 1.5-2h substantive scope (largest remaining FE wiring item)
    - Banner is acceptable temp state; partial-reactive worse UX than explicit banner
    - Defers to next session for clean coherent ship vs piecemeal partial today

    **Cross-link with .011:** if cross-firm consolidation lands first (or in parallel), Surface #8 FE wiring may share shared accessor primitive. Otherwise, this TO ships Inflection-specific wiring; consolidation follows.

    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"` per protocol.
  </notes>
</task_order>
