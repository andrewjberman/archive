<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-office-w6</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>staged</status>
    <project_code>ADVI_OFFICE</project_code>
  </metadata>

  <references>
    <ref type="prd_addendum">docs/architecture/ADVI_OFFICE_ADDENDUM.md</ref>
    <ref type="source">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</ref>
    <ref type="prior_work">ADVI_OFFICE.W3 (DE — OFC toggle, donut, L1 advisor drill)</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform"
                task="ADVI_OFFICE.W5.ds-d00b-fix3-ofc-timeseries"
                status="staged"
                description="Fixes 1-9 below are all independent of W5 data. Fix 9 (bell curve verification) and Fix 10 (canonical advisor format) should be verified AFTER W7 AE gold run confirms data is present. Start Fixes 1-8 immediately on GO."/>
  </dependencies>

  <objective>
    Fix 10 specific OFC parity gaps in DistributionTab.tsx identified by compiler analysis
    of the W3-shipped implementation. OFC must behave identically to GEO and ADV for all
    Snapshot and Continuous modes. Every bug has an exact line number — no guesswork required.

    Fixes 1-8 have no data dependency and can begin immediately.
    Fixes 9-10 require W7 AE gold run to have confirmed ofc data in platinum before verifying.
  </objective>

  <context>
    CTO ran comp-transform schema-check, comp-transform fields, comp-platinum page, and
    comp-pipescript io against D_01 and D_00b. All 10 bugs were identified with exact
    line numbers. The root cause of most visual gaps is a single missing OFC branch in
    drillParentKey (L663) that cascades through time machine, bell curve, and drill state.

    comp-validate context: set before starting work:
    printf "SERIAL=0.4.0_DE_ClientPlatform\nTO_ID=ADVI_OFFICE.W6\n" > .comp-graph/.agent_context

    TARGET FILE: portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx

    ALL 10 FIXES WITH EXACT LINE NUMBERS:

    FIX 1 — drillParentKey CASCADE FIX (Lines 663-665)
    This is the highest-priority fix — it cascades to time machine, NNA strip,
    and drill state for OFC.
    Current:
      const drillParentKey = cohort === 'geo' ? selectedStateKey
        : selectedArchitectKey
    Fix:
      const drillParentKey = cohort === 'geo' ? selectedStateKey
        : cohort === 'ofc' ? selectedOfficeKey
        : selectedArchitectKey

    FIX 2 — Time machine parentSegmentKey (TWO SITES: Lines 2925 and 2928)
    Current (both): parentSegmentKey={cohort === 'geo' ? selectedStateKey : selectedArchitectKey}
    Fix (both): parentSegmentKey={cohort === 'geo' ? selectedStateKey : cohort === 'ofc' ? selectedOfficeKey : selectedArchitectKey}
    Note: Line 2925 is inside NnaQuarterlyStrip props, line 2928 is inside DistributionQuarterlyStrip props.
    Both must be updated.

    FIX 3 — Continuous chart title (Line 2032)
    Current: ${cohort === 'geo' ? 'Geography' : 'Advisor'}
    Fix:     ${cohort === 'geo' ? 'Geography' : cohort === 'ofc' ? 'Office' : 'Advisor'}

    FIX 4 — NNA continuous series view (Line 1956)
    Current: const nnaSeriesView = cohort === 'geo' ? data?.nna_geo : data?.nna_adv
    Fix:     const nnaSeriesView = cohort === 'geo' ? data?.nna_geo : cohort === 'ofc' ? data?.nna_ofc : data?.nna_adv

    FIX 5 — Search placeholder (Line 2089)
    Current: placeholder={cohort === 'geo' ? 'Search all states...' : 'Search all architects...'}
    Fix:     placeholder={cohort === 'geo' ? 'Search all states...' : cohort === 'ofc' ? 'Search all offices...' : 'Search all architects...'}

    FIX 6 — Search drill keys (Lines 2102-2104)
    Current:
      const drillKeys = cohort === 'geo'
        ? (viewData?.categories ?? [])
        : Object.keys(data?.adv_drill ?? {})
    Fix:
      const drillKeys = cohort === 'geo'
        ? (viewData?.categories ?? [])
        : cohort === 'ofc'
        ? (viewData?.categories ?? [])
        : Object.keys(data?.adv_drill ?? {})

    FIX 7 — NNA breakout (Line 1195)
    Current: const breakout = cohort === 'geo' ? p.by_geo : p.by_adv
    Fix:     const breakout = cohort === 'geo' ? p.by_geo : cohort === 'ofc' ? (p as any).by_ofc : p.by_adv
    Note: 'by_ofc' may not be in the TimeseriesNnaPeriod type. If not, check if
    timeseries_overview.json actually emits it. If the type is missing but data exists,
    add by_ofc?: Record<string, NnaCohortEntry> to the type. If data doesn't exist
    (timeseries_overview doesn't emit by_ofc), leave this fix as a comment and note in session log.

    FIX 8 — Footnote text (Lines 2944-2957)
    Multiple ternaries use `cohort === 'geo' ? 'State/City/Geographic' : 'Architect/Client/Advisor'`.
    Each must add an OFC branch. Pattern for each:
      cohort === 'geo' ? 'State-level' : cohort === 'ofc' ? 'Office-level' : 'Architect-level'
      cohort === 'geo' ? 'City' : cohort === 'ofc' ? 'Advisor' : 'Relationship'
      (drill footnote) cohort === 'geo' ? 'state' : cohort === 'ofc' ? 'office' : 'architect'
    Read each ternary in context and choose the semantically correct OFC equivalent.

    FIX 9 — Bell curve L0 (no office selected): VERIFY AFTER W7 DATA
    After W7 gold run, check that analyticsData.views?.ofc.current.distribution.total is
    non-null. If present, the existing code path at line 2572 (return dist?.total || null)
    should render the bell curve automatically. No code change needed if data exists.
    If distribution.total is null/empty → flag to CTO for DS investigation.

    FIX 10 — Advisor list canonical format (L1 drill): VERIFY AFTER W7 DATA
    After W7, click Austin in OFC donut. Verify right panel shows advisor list with same
    format as GEO city drill: name, AUA ($), account count. If format differs, normalize
    to match. D_01's _build_ofc_advisors function populates each segment's advisors array
    — verify it emits name, aua, account_count fields matching the frontend type.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing any code:
      <run>comp-transform schema-check DistributionTab</run>
      <expect>0 MISSING fields. chartData/analyticsData as NOTE (runtime aliases). nna_ofc UNUSED on PlatinumCumulativeChartResponse (this will change after Fix 4).</expect>
      <if_mismatch>If new MISSING fields appear beyond known aliases, flag to CTO before writing</if_mismatch>

      <run>comp-blast DistributionTab</run>
      <expect>8 downstream nodes via opal-partners-data Lambda — unchanged from W3 baseline</expect>
      <if_mismatch>If node count changed, flag to COO — unexpected dependency may exist</if_mismatch>

    Phase 2 — before committing:
      <run>comp-transform schema-check DistributionTab</run>
      <expect>nna_ofc now RENDERED (not UNUSED) on PlatinumCumulativeChartResponse after Fix 4. 0 MISSING fields. ofc types in rendered set.</expect>
      <if_mismatch>If nna_ofc still UNUSED, Fix 4 was not applied correctly — check line 1956</if_mismatch>

      bun run build — zero TypeScript errors
      bun run lint — zero new warnings

    Phase 3 — after committing:
      <run>comp-blast DistributionTab</run>
      <expect>Still 8 downstream nodes — blast radius unchanged</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</shared_resource>
    <shared_resource>portal/src/pages/AdvisorIntelligence/types.ts</shared_resource>
    <also_in_to>No other active TOs currently touching DistributionTab</also_in_to>
    <required_action>
      Pull latest CLOUD before starting — DT W4 portal deploy may have updated portal submodule.
      Check git log --oneline portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx -5
      before editing to confirm you're on the latest W3 base.
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. OFC Continuous AUA: stacked area chart renders with 5+ office series (after W7 data confirmed)
    2. OFC Continuous NNA: diverging bar chart renders with 5+ office series (not "No NNA advisor data")
    3. OFC Continuous: title reads "Cumulative AUA by Office" / "Net New Assets by Office" — not "by Advisor"
    4. OFC Snapshot + office selected → time machine strip shows historical AUA for that office, not $0/N/A
    5. OFC Snapshot → search box reads "Search all offices..." — not "architects"
    6. OFC Snapshot + no office selected → if D_01 emits distribution.total, bell curve renders; if not, placeholder explains why
    7. comp-transform schema-check DistributionTab: 0 MISSING fields; nna_ofc in rendered set
    8. bun run build exits 0 (zero TypeScript errors)
    9. comp-blast DistributionTab: 8 downstream nodes (unchanged)
    10. Session log: all 10 fixes documented with before/after, Fixes 9-10 noted as verified or deferred with reason
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify" optional="true">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
    <out_of_scope>
      Gold scripts (DS W5). AE gold run (W7). Portal deploy (W8 DT).
      Any changes outside the 10 fixes listed above.
    </out_of_scope>
  </scope>

  <deliverables>
    - Commit to portal DEV with DE author
    - Session log: each fix confirmed, comp-transform schema-check before+after, Fixes 9-10 verified or deferred
    - MCP message to 2.0.0_SA_COO: "W6 complete — 10 OFC parity fixes on portal DEV. Fixes 9-10: {status}."
  </deliverables>
</task_order>
