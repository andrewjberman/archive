<task_order>
  <metadata>
    <id>ADVI_INFFIN.001</id>
    <slug>rd-ui-parity-batch</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-13</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — bundles 4 visible-state defects (3 P1 + 1 P2) into single RD authoring pass; no upstream deps; ships first wave of Phase 1 parallel</priority>
    <sla>~3-4h wall; ships standalone (no dependency on DS~A/~B/~C)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief, commit e7965874b)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct evening walkthrough 2026-05-13 via DE 0.4 brief — 9 surfaces from screenshots; routing directive: "write a document covering every single thing that needs to get done, issue it to COO, and have COO distribute the TOs across the relevant parties"</ref>
    <ref type="cross_link">Sibling TOs in same project: .002 RD advisor-context wiring (parallel) + .003 DS~C INF emit (parallel) + .004 DS~A directory artifact (parallel) + .005 DS~B 49F audit (parallel) + .006 RD Phase 2 dispatch_held + .007 AE 0.6.1 dispatch_held</ref>
  </references>

  <context>
    Andrew evening walkthrough surfaced 4 UI parity defects on Inflection AdvisorIntelligence page that share lane (FE-only, RD 0.4.2) and have no DS data dependencies. Batch into single authoring pass for maximum RD context efficiency.

    **Surface #1 — ADV-L0 right partition missing global account-size bell curve.** Page: AdvisorIntelligence → Distribution → Segment Analytics. View: ADV/Snapshot/AUA/Quarter at L0 (no advisor selected). Right partition shows placeholder "Select a advisor to view account size distribution"; expected = global account-size bell curve identical to GEO-L0's "Account Sizes by State" panel (firm-wide aggregate regardless of ADV vs GEO cohort axis).

    **Surface #5 — BusinessIntelligence table columns must all support 3-state click-to-sort.** Page: BusinessIntelligence — any table view. Current: inconsistent column sortability. Expected: every column header clickable with 3-state cycle (default → DESC first click → ASC second click → default third click); chevron indicator on hover; persistent + highlighted on active sort.

    **Surface #7 — Universal canonical NNA chart design directive.** Andrew rule: "All NNA should have same tooltips and canonical color/design as is displayed in 'Assets Overview'... this is not acceptable, this should be a universal design." Canonical reference: Assets Overview (PartnerAnalytics) NNA chart — blue bars (Inflows) + red bars (Outflows) + orange Net Flow line + tooltip card with colored bullet markers + structured rows + YoY/QoQ Change delta. Violator: AdvisorPublicProfile → Lifetime Activity NNA chart (indigo/purple line, compact black tooltip, no colored markers, no YoY/QoQ delta).

    **Surface #9 — Lifetime Activity AUA-mode tooltip parity.** Page: AdvisorIntelligence → AdvisorPublicProfile → Lifetime Activity, AUA mode. AUA value renders in indigo highlight color in tooltip — hard to read, non-canonical. Andrew quote: "We show AUA in the tooltip as highlighted in indigo out of pattern, it's hard to read and not canonical, should be white text and look similar to how we design all the other tooltips in Assets Overview."

    Surfaces #7 + #9 bundle naturally — both require extracting canonical chart primitive from Assets Overview into shared `_shared/charts/` components. Once extracted, the shared `<NnaBarLineChart>` + `<ChartTooltip>` cover both NNA-mode and AUA-mode variants. Surface #3 (in .002) inherits this primitive once advisor-selection wiring lands.
  </context>

  <objective>
    Land 4 UI parity surfaces on Inflection AdvisorIntelligence in single RD authoring pass:

    1. Render global account-size bell curve at ADV-L0 right partition (mirror GEO-L0's "Account Sizes by State")
    2. Wire 3-state click-to-sort on every column header in every BusinessIntelligence table view
    3. Extract canonical NNA chart primitive (`<NnaBarLineChart>` + `<ChartTooltip>`) from Assets Overview into shared `_shared/charts/`; migrate AdvisorPublicProfile Lifetime Activity NNA chart to use shared primitive
    4. AUA-mode tooltip parity via same shared primitive (white text, structured rows, no indigo highlight)

    No DS data dependencies; ships standalone. Single commit if natural; multiple commits acceptable per RD discipline.
  </objective>

  <scope>
    <surfaces>
      <surface id="1">ADV-L0 right partition global account-size bell curve render</surface>
      <surface id="5">3-state click-to-sort on BusinessIntelligence table columns</surface>
      <surface id="7">Canonical NNA chart primitive extraction + AdvisorPublicProfile Lifetime Activity migration</surface>
      <surface id="9">AUA-mode tooltip parity via shared ChartTooltip primitive</surface>
    </surfaces>
    <files>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_shared/components/DistributionTab/ (or similar) — cohort-routing ternary for right-partition render at L0</file>
      <file action="investigate">portal/src/pages/AdvisorIntelligence/_partners/49financial/PartnerAnalytics/ (or similar) — locate canonical NNA chart primitive currently used by Assets Overview</file>
      <file action="extract">portal/src/pages/AdvisorIntelligence/_shared/charts/NnaBarLineChart.tsx (or similar — new shared primitive)</file>
      <file action="extract">portal/src/pages/AdvisorIntelligence/_shared/charts/ChartTooltip.tsx (or similar — new shared primitive)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/_partners/inflection/AdvisorPublicProfile.tsx (or similar) — Lifetime Activity NNA chart migration to shared primitive</file>
      <file action="extract_or_extend">portal/src/pages/AdvisorIntelligence/_shared/components/SortableTableHeader.tsx (or similar — 3-state sort primitive)</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/BusinessIntelligence/ table view components — apply SortableTableHeader across all columns</file>
    </files>
  </scope>

  <phase id="1" when="investigation">
    <step>
      <description>Surface #1 investigation: `comp-transform ternary-audit DistributionTab` (or similar component) to locate cohort-routing ternary in right-partition render. Identify missing `cohort === 'ADV'` branch at L0 that should render the same global-bell-curve component GEO-L0 already renders.</description>
      <expect>Ternary located + missing branch identified.</expect>
      <if_mismatch>If no ternary exists yet, the cohort-routing pattern is elsewhere — investigate via component tree walk.</if_mismatch>
    </step>
    <step>
      <description>Surface #7 investigation: locate canonical NNA chart primitive in Assets Overview (PartnerAnalytics NNA chart). Verify if it's already shared or page-local. `grep -rn "Net New Assets|netFlow|NNA|net_flow" portal/src/pages/AdvisorIntelligence/ --include="*.tsx"` to enumerate all NNA visualizations.</description>
      <expect>Canonical primitive identified; non-canonical violators enumerated.</expect>
      <if_mismatch>If multiple NNA chart implementations exist (Assets Overview + Lifetime Activity + DistributionTab Continuous-NNA + BookView), prioritize Assets Overview as canonical reference.</if_mismatch>
    </step>
    <step>
      <description>Surface #5 investigation: identify existing SortableTableHeader primitive (if any) or pick the cleanest target table view to extract from.</description>
      <expect>Existing primitive identified OR clean target located.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Surface #1: add missing `cohort === 'ADV'` branch at L0 to render global account-size bell curve. Mirror GEO-L0's "Account Sizes by State" panel data shape (P10/P25/Median/P75/P90 + Total Accounts + percentile stats).</description>
      <expect>ADV-L0 right partition renders bell curve; GEO-L0 unchanged.</expect>
    </step>
    <step>
      <description>Surface #7 step 1: extract canonical NNA chart primitive from Assets Overview into `_shared/charts/NnaBarLineChart.tsx` + `ChartTooltip.tsx`. Preserve blue bars (Inflows) + red bars (Outflows) + orange Net Flow line + colored bullet markers in tooltip + YoY/QoQ delta row.</description>
      <expect>Shared primitives created; Assets Overview consumes from new location with no visual diff.</expect>
      <if_mismatch>If primitive extraction surfaces deeper coupling (e.g., NNA chart hard-bound to Assets Overview data accessor), surface to COO before extending scope.</if_mismatch>
    </step>
    <step>
      <description>Surface #7 step 2: migrate AdvisorPublicProfile Lifetime Activity NNA chart to consume shared primitive. Remove indigo/purple line color; remove compact black tooltip; replace with shared primitive (blue/red/orange + tooltip card).</description>
      <expect>Lifetime Activity NNA chart visually identical to Assets Overview NNA chart in NNA mode.</expect>
    </step>
    <step>
      <description>Surface #9: extend shared `ChartTooltip` primitive to also cover AUA mode (white text, structured rows, AUA + QoQ delta only). Apply to AdvisorPublicProfile Lifetime Activity AUA mode.</description>
      <expect>AUA tooltip matches Assets Overview AUA tooltip visually (white text, no indigo highlight).</expect>
    </step>
    <step>
      <description>Surface #5: implement (or extend) `<SortableTableHeader>` primitive with 3-state cycle (default → DESC → ASC → default). Single sort-state hook drives row ordering. Visual affordance: chevron up/down on hover; persistent + highlighted on active sort column.</description>
      <expect>SortableTableHeader primitive landed.</expect>
    </step>
    <step>
      <description>Surface #5 cascade: apply SortableTableHeader to every column header across every BusinessIntelligence table view (Activity scan + others). Preserve default sort on initial render.</description>
      <expect>All BI table columns sortable; 3-cycle returns to original row order on third click.</expect>
    </step>
  </phase>

  <phase id="3" when="audit">
    <step>
      <description>Audit all OTHER NNA visualizations in the portal (DistributionTab Continuous-NNA, BookView Inflows/Outflows panels, anywhere else NNA is rendered). Migrate any other violators to the shared `<NnaBarLineChart>` + `<ChartTooltip>` primitives.</description>
      <expect>Universal NNA chart design system holds across the portal.</expect>
      <if_mismatch>If a violator has unique data shape that doesn't match shared primitive, surface to COO before fork or per-page bespoke variant.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1 (Surface #1): ADV-L0 right partition renders global Account Sizes bell curve with P10/P25/Median/P75/P90 + Total Accounts + percentile stats. GEO-L0 unchanged. Visual diff: ADV-L0 right panel === GEO-L0 right panel at L0.
    AC2 (Surface #5): Every column header in every BI table view clickable; 3-state cycle (default → DESC → ASC → default); sort indicator visible on active column; default sort preserved on initial render.
    AC3 (Surface #7): Canonical `<NnaBarLineChart>` + `<ChartTooltip>` primitives extracted to `_shared/charts/`. AdvisorPublicProfile Lifetime Activity NNA chart visually identical to Assets Overview NNA chart in NNA mode. All other NNA visualizations migrated to shared primitive.
    AC4 (Surface #9): AdvisorPublicProfile Lifetime Activity tooltip in AUA mode matches Assets Overview AUA tooltip visually (white text, structured rows, no indigo highlight).
    AC5 (Universal): Every NNA + AUA chart in the portal consumes shared primitive. No per-page bespoke variants remaining.
    AC6: No regression on existing Assets Overview chart rendering.
    AC7: tsc 0 errors on portal build.
    AC8: bun run dev + manual smoke against ADV-L0 + Lifetime Activity + BI tables in dev environment.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-transform ternary-audit DistributionTab; grep -rn "Net New Assets|netFlow|NNA|net_flow" portal/src/pages/AdvisorIntelligence/ --include="*.tsx"; comp-transform fields on each NNA-chart candidate to verify shape</phase_1>
    <phase_2>tsc + bun run dev smoke; visual diff each shipped surface</phase_2>
    <phase_3>portal lint check (no new react-refresh warnings introduced)</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    NO DS DEPS: surfaces #1 / #5 / #7 / #9 all FE-only. Ships standalone.

    PARALLEL ACTIVITY:
    - .002 RD advisor-context wiring (Surface #3 inherits canonical NNA chart from #7 once that primitive lands; .001 ships first, .002 then consumes)
    - .003 DS~C INF emit batch (independent surfaces; no FE-side conflict)
    - .004 DS~A directory artifact (Surface #4 backend, independent)
    - .005 DS~B 49F audit (parallel investigation)

    PORTAL SUBMODULE: ships through normal DEV → PROD cycle. DT 0.4 owns portal submodule push.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure frontend change. No data emit changes; no Lambda redeploys; no chain re-fires.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Surface #1: ADV-L0 right partition cohort-routing branch addition + global bell curve render
    2. Surface #5: SortableTableHeader 3-state primitive + applied across all BI table views
    3. Surface #7: Shared `<NnaBarLineChart>` + `<ChartTooltip>` primitives extracted + Lifetime Activity migration + portal-wide NNA chart audit + migration
    4. Surface #9: AUA-mode tooltip parity via shared primitive
    5. Single or multiple commits under 0.4.2_RD_AdvisorIntelligence author per RD discipline
    6. tsc 0 errors + visual diff smoke on dev
    7. MCP RAVC2 to COO post-AC1-8 PASS with per-surface evidence (screenshots or commit hashes)
  </deliverables>

  <ravc>
    RD 0.4.2 RAVC2 to COO post-AC1-8 PASS with per-surface evidence (screenshots preferred for visual surfaces #1/#7/#9; commit hashes for #5). COO relays acceptance to Andrew. .006 Phase 2 wiring dispatches post .003 DS~C ship signal.
  </ravc>

  <notes>
    **Per DE brief recommendations:** this TO batches Phase 1 RD UI parity surfaces. Ships first wave alongside .002 (RD advisor-context wiring), .003 (DS~C emit), .004 (DS~A directory), .005 (DS~B 49F audit).

    **Cross-link with Surface #3 (in .002):** once canonical `<NnaBarLineChart>` primitive lands here, Surface #3 (Continuous-ADV-NNA L1 chart in .002) inherits it on advisor-selection wiring. No explicit handoff needed; primitive consumption is via import.

    **Author identity:** `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"` per agent commit identity protocol.

    **Open question #4 (red-flag accounts):** Surface #6 FeeSummary panel has red-flag accounts (166, 477) with warning icons + reduced AUA cells. The tooltip explanation is in DE brief §Open Questions for .003 (DS~C) to surface what structural condition triggers. .001 RD work does NOT touch FeeSummary panel — that's .006 Phase 2 scope post DS~C emit.
  </notes>
</task_order>
