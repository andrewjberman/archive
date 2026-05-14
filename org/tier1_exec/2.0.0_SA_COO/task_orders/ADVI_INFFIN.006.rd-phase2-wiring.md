<task_order>
  <metadata>
    <id>ADVI_INFFIN.006</id>
    <slug>rd-phase2-wiring</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-13</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO. Original conditions met: .003 DS~C c5d98d41f + .010 5e5f18edd shipped + chain #28 mode=gold-d materialized fields + v1.7.56 Lambda passthrough verified via direct-invoke smoke. **Effective remaining scope = Surface #2 stacked HH render only** (11/12 items already shipped via portal-302992c6 / portal-v2.1.85). Surfaces #6 + #8 split out to .011 + .012. Final dev-smoke for Surface #2 gates on chain #30 mode=full completion (in flight 13:01Z; ETA terminal 14:11-14:21Z) — RD can code against expected schema in parallel.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P0 — completes Phase 2 of INFFIN; Surface #6 FeeSummary top half presentation + Surface #8 reactive toggle wiring close Andrew's #1 priority items (per-account null elimination + cross-firm parity)</priority>
    <sla>~2-3h wall post-unblock; ships standalone (no further dep after unblock)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief §Surface #2 + #6 + #8 FE-wiring portions)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough 2026-05-13</ref>
    <ref type="cross_link">Gated on: .003 DS~C INF emit batch ship + .007 AE 0.6.1 chain fire. Sibling: .001 RD UI parity (already landed Phase 1) + .002 RD advisor-context wiring (already landed Phase 1; Surface #3 NNA chart wiring should be complete by this TO's start) + .004 DS~A directory artifact (Surface #4 backend, available) + .005 DS~B 49F audit (schema normalization spec)</ref>
  </references>

  <context>
    Phase 2 RD wiring lands the FE consumers of DS~C's new gold emits (.003) once chain (.007) fires to materialize the new fields in platinum.

    **Surface #2 wiring (stacked HH render):** RD-A's .001 NNA chart primitive + .002 advisor-selection wiring are foundational. This TO completes Surface #2 by:
    - Consuming `relationship_stacked_periods[]` block from advisor book.json (emit by .003)
    - Replacing 4 static "Client 1 / Client 2 / Client 3 / Client 4" stub entries with real top-N HH legend
    - Rendering stacked timeseries (bar or area) per period using `enforceTop9Other` helper pattern
    - PII-pseudonymized display_name in stacks
    - Optional polish: clicking an HH bar segment navigates to L3 client detail

    **Surface #6 wiring (FeeSummary top half presentation):** Once .003 emits per-account fee fields without null:
    - Render FeeSummary top half canonical with 49F: "Client Fee" headline + per-role row breakdown
    - Match 49F's `FeeSummaryPanel.tsx` layout
    - Drop the inert empty top half placeholder
    - Render per-account FEE / TOTAL (BPS) / SPLIT (BPS) values (no more `—` em-dashes)
    - Render red-flag accounts (166, 477) with warning icon + tooltip from `fee_structure_reason` sentinel field

    **Surface #8 wiring (reactive Fee/NoFee/All toggle):** Once .003 emits per-period parallel fee-split fields:
    - Wire `feeView` state through every metric accessor in `_partners/inflection/AdvisorPublicProfile.tsx`
    - Executive Summary cards (AUA + accounts + clients) re-render on toggle
    - Flows panel re-renders on toggle
    - Fee block stays + reflects toggle
    - Lifetime Activity chart re-renders with split bars (consuming Lifetime Activity portion of .003)
    - Remove "Fee-split data unavailable — showing aggregate" banner
    - Drop `—` em-dashes from `AUA Growth`, `Fee-Earning AUA`, `Non-Fee AUA` rows
    - If .005 DS~B audit + .003 schema-normalize landed, FE accessor becomes shared between 49F + Inflection (single canonical accessor)
  </context>

  <objective>
    Land 3 Phase 2 FE wiring surfaces consuming DS~C's new gold emits:

    1. **Surface #2 stacked HH render** — replace static stubs with real top-N HH stacked timeseries
    2. **Surface #6 FeeSummary top half + per-account fees** — render canonical with 49F + drop em-dashes + surface red-flag tooltips
    3. **Surface #8 reactive Fee/NoFee/All toggle** — wire toggle through every metric on AdvisorPublicProfile + Lifetime Activity split bars + remove banner

    Single coherent FE authoring pass; ships post-chain-fire (.007).
  </objective>

  <scope>
    <surfaces>
      <surface id="2">Stacked HH render (Continuous-ADV-L1 right partition)</surface>
      <surface id="6">FeeSummary top half presentation + per-account fee rendering + red-flag tooltip</surface>
      <surface id="8">Reactive Fee/NoFee/All toggle across AdvisorPublicProfile + Lifetime Activity</surface>
    </surfaces>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/components/DistributionTab/ContinuousView/ (or similar) — Surface #2 stacked HH render consuming `relationship_stacked_periods[]`</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/inflection/L3/FeeSummaryPanel.tsx (or _shared/) — Surface #6 top half canonical with 49F + per-account FEE/TOTAL/SPLIT rendering</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/inflection/AdvisorPublicProfile.tsx (or similar) — Surface #8 reactive toggle wiring through every metric</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_shared/charts/ — Lifetime Activity split bars consuming .003 Lifetime Activity portion</file>
      <file action="potentially_consolidate">portal/src/pages/AdvisorIntelligence/_shared/accessors/feeView.ts (or similar) — shared accessor consumed by both 49F + Inflection if .005 + .003 normalize aligned</file>
    </files>
  </scope>

  <phase id="1" when="pre-unblock-verify">
    <run>Verify .003 DS~C ship signal received (RAVC2 PASS from COO)</run>
    <expect>.003 commit hash + gold emit confirmed in chain fire output</expect>
    <if_mismatch>Do not start; surface to COO. dispatch_held=true.</if_mismatch>

    <run>Verify .007 AE 0.6.1 chain fire complete (RAVC2 PASS from COO)</run>
    <expect>Chain exit 0 + new fields visible in platinum artifacts</expect>
    <if_mismatch>Wait for AE chain; dispatch_held=true.</if_mismatch>

    <run>Empirical S3 inspect — does platinum/advisors/{id}/book.json contain new fields per-account fee + fee-paying split + relationship_stacked_periods? Spot-check 1 advisor.</run>
    <expect>New fields present.</expect>
    <if_mismatch>Surface to COO; .003 + .007 RAVC2 may be premature.</if_mismatch>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Surface #2 stacked HH render: consume `relationship_stacked_periods[]` from advisor book.json. Replace 4 static stub entries with real top-N HHs (`enforceTop9Other` helper) + "Other" aggregate. Stacked bars or area per period (Quarter × 1Y default). PII-pseudonymized display_name only.</description>
      <expect>Continuous-ADV-L1 right partition renders real data; left rail legend matches stacks.</expect>
    </step>
    <step>
      <description>Surface #2 optional polish: click HH bar segment → navigates to L3 client detail. RD discretion at implementation.</description>
      <expect>Click handler wired if RD chooses to ship; otherwise document as follow-up.</expect>
    </step>
    <step>
      <description>Surface #6 FeeSummary top half: render canonical with 49F. "Client Fee" headline + per-role row breakdown. Match 49F FeeSummaryPanel layout. Drop empty top half placeholder.</description>
      <expect>Top half visually matches 49F FeeSummary.</expect>
    </step>
    <step>
      <description>Surface #6 per-account fee rendering: consume new fee_* fields from `clients[].accounts[]`. Render FEE / TOTAL (BPS) / SPLIT (BPS) columns. Apply null-elimination FE rendering rule:
- Real `0` / `0.0` → display as `$0` / `0 bps`
- Real value → display as `$X.XX` / `Y.Y bps`
- Sentinel `fee_structure: "no_structure"` (or similar) → display warning icon + tooltip from `fee_structure_reason` field</description>
      <expect>No `—` em-dashes; red-flag accounts (166, 477) surface tooltip.</expect>
    </step>
    <step>
      <description>Surface #8 reactive toggle: wire `feeView` state through every metric accessor in AdvisorPublicProfile. Affected:
- Executive Summary cards (AUA + accounts + clients + new_clients)
- Flows panel (inflows + outflows + nna)
- Fee block (already populated; should toggle-aware)
- Lifetime Activity chart (split bars via .003 emit)
Apply: All / Fee-Paying / No-Fee → consume corresponding parallel field.</description>
      <expect>Every number on AdvisorPublicProfile re-renders on toggle change.</expect>
    </step>
    <step>
      <description>Surface #8 Lifetime Activity: consume split-bars data from .003 Lifetime Activity portion. Render stacked bars (fee-paying + no-fee). Remove "Fee-split data unavailable — showing aggregate" banner.</description>
      <expect>Lifetime Activity chart renders with split bars; banner gone.</expect>
    </step>
    <step>
      <description>Surface #8 cross-firm parity (if .005 + .003 normalize aligned): consolidate FE accessor into shared component consumed by both 49F + Inflection. Single source of truth for fee-split rendering.</description>
      <expect>One shared accessor; both partners consume.</expect>
      <if_mismatch>If .005/.003 surfaced divergent semantics requiring fork, document the adapter requirement; ship without consolidation.</if_mismatch>
    </step>
    <step>
      <description>Null-elimination rule sweep: audit every metric on AdvisorPublicProfile for any remaining `—` em-dashes. If found, surface to COO — likely upstream `null` from .003 emit (bug; route back to DS~C for fix).</description>
      <expect>Zero `—` em-dashes; every metric has real value or sentinel-with-tooltip.</expect>
    </step>
  </phase>

  <phase id="3" when="visual-validation">
    <step>
      <description>Visual diff: AdvisorPublicProfile Lifetime Activity tooltip + chart consume canonical primitive from .001 (NNA mode + AUA mode). Confirm no regressions vs .001 ship state.</description>
      <expect>Tooltip parity preserved.</expect>
    </step>
    <step>
      <description>Cross-firm visual diff: 49F + Inflection AdvisorPublicProfile fee-split renderings visually consistent (modulo partner-specific cosmetic differences). Confirm shared schema flowing correctly.</description>
      <expect>Cross-firm parity visible.</expect>
    </step>
    <step>
      <description>Smoke against all 4 Inflection advisors (peter_lee + patrick_scanlan + joe_brandenburg + IWM). Toggle each fee-view state. Confirm zero `—` em-dashes anywhere.</description>
      <expect>All 4 advisors + 3 toggle states clean.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1 (Surface #2): Continuous-ADV-L1 right partition renders stacked timeseries over selected window; top-N HHs + "Other"; PII-pseudonymized; left rail legend matches stacks.
    AC2 (Surface #6 top half): FeeSummary top half renders canonical with 49F ("Client Fee" headline + per-role row breakdown).
    AC3 (Surface #6 per-account): No `—` em-dashes in FEE/TOTAL(BPS)/SPLIT(BPS) columns for any Inflection account at any HH.
    AC4 (Surface #6 red-flag): Red-flag accounts (166, 477) surface warning icon + tooltip explaining structural condition from `fee_structure_reason` sentinel.
    AC5 (Surface #8 toggle): Click Fee-Paying / No-Fee / All re-renders every number in Executive Summary + Flows + Fee + Lifetime Activity chart.
    AC6 (Surface #8 banner): "Fee-split data unavailable — showing aggregate" banner removed from Lifetime Activity.
    AC7 (Surface #8 em-dashes): No `—` em-dashes for AUA Growth / Fee-Earning AUA / Non-Fee AUA on any toggle state.
    AC8 (Cross-firm parity): 49F + Inflection share FE accessor where .005 + .003 normalized; documented adapter requirement if divergent.
    AC9: tsc 0 errors on portal build.
    AC10: bun run dev + manual smoke across all 4 advisors + 3 toggle states.
    AC11: MCP RAVC2 to COO post-AC1-10 PASS with per-surface evidence (screenshots preferred for visual surfaces).
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>Verify .003 DS~C RAVC2 + .007 AE chain RAVC2; empirical S3 inspect new fields</phase_1>
    <phase_2>comp-transform schema-check on AdvisorPublicProfile + FeeSummaryPanel + DistributionTab post-edit; tsc + bun run dev smoke</phase_2>
    <phase_3>visual diff per surface; cross-firm parity check; null-elimination FE sweep</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES:
    - .003 DS~C INF emit batch RAVC2 PASS
    - .007 AE 0.6.1 chain fire RAVC2 PASS
    - Both required for dispatch unblock

    SOFT DEPENDENCIES:
    - .005 DS~B 49F audit normalization recommendations (informs cross-firm parity FE accessor consolidation; not blocking — RD ships without consolidation if normalization landed late)
    - .001 RD UI parity batch canonical NNA primitive (Lifetime Activity AUA-mode tooltip from .009)
    - .002 RD advisor-context wiring (Surface #3 already landed; this TO doesn't touch Surface #3)
    - .004 DS~A directory artifact (Surface #4 already landed if .002 picked this path)

    PORTAL SUBMODULE: DT 0.4 owns portal submodule push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      FE-only wiring. No data emit changes; no Lambda redeploys; no chain re-fires. .007's chain fire is the prerequisite (NOT triggered by this TO).
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Surface #2: stacked HH render
    2. Surface #6: FeeSummary top half + per-account fee rendering + red-flag tooltip
    3. Surface #8: reactive toggle wiring + Lifetime Activity split bars + banner removal
    4. Cross-firm FE accessor consolidation (where .005 + .003 normalized)
    5. Single or multiple commits under 0.4.2_RD_AdvisorIntelligence author per RD discipline
    6. tsc 0 errors + visual diff smoke on dev
    7. MCP RAVC2 to COO post-AC1-11 PASS with per-surface evidence
  </deliverables>

  <ravc>
    RD 0.4.2 RAVC2 to COO post-AC1-11 PASS. Final Phase 2 close on INFFIN project. COO ratifies + relays to Andrew for partner-visible acceptance on the 9 surfaces.
  </ravc>

  <notes>
    **Dispatch hold:** dispatch_held=true until .003 + .007 RAVC2 both PASS. COO unblocks via MCP "INFFIN.006 dispatch unblocked; proceed."

    **Cross-firm FE accessor consolidation timing:** if .005 + .003 normalization aligned, consolidate FE accessor in this TO. If normalization is incomplete (e.g., .005 lands after .003 with rename requirements), ship .006 without consolidation; follow-on cleanup TO authors the consolidation.

    **Null-elimination FE responsibility:** if any `null` slips through to FE rendering despite .003's gold-side null-elimination, .006 surfaces it back as upstream bug (route to DS~C for fix). FE should NOT silently render `—` for what should be a real value.

    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"` per agent commit identity protocol.

    **Open question #4 (red-flag accounts):** AC4 surfaces the `fee_structure_reason` tooltip — every red flag explains itself. This is the FE half of the deliverable; DS~C's .003 emit provides the sentinel content.
  </notes>
</task_order>
