<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-046-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~D</issued_to>
    <date>2026-04-09</date>
    <status>complete -- fix_1 DONE (16f0552), fix_2 DONE (16f0552), commission tooltip DONE (20ccb6f), fix_3 DONE (DS .045 Option A confirmed: ratio=commission/NNA, Efficiency label correct, tooltip updated)</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>11</wave>
    <phase>Books tab UI fixes</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Three UI fixes for the Books tab fee efficiency panel, plus a note on the
    blocked advisor/client drilldown. fix_1 (ordinal) and fix_2 (table UX) are
    unblocked and can be shipped immediately.
  </objective>

  <fix_1 label="Fix ordinal formatting throughout ADVI -- 83th → 83rd">
    <description>
      "83th percentile" is grammatically wrong. Correct ordinals:
        1st, 2nd, 3rd, 4th ... 11th, 12th, 13th ... 21st, 22nd, 23rd, 24th ...
        83rd (not 83th), 91st (not 91th), 92nd (not 92th), 93rd (not 93rd)

      Add a shared ordinal utility in portal/src/lib/ (e.g. formatOrdinal.ts):

        const _rules = new Intl.PluralRules('en-US', { type: 'ordinal' })
        const _suffixes: Record<string, string> = {
          one: 'st', two: 'nd', few: 'rd', other: 'th'
        }
        export function formatOrdinal(n: number): string {
          return `${n}${_suffixes[_rules.select(n)]}`
        }

      Handles all edge cases correctly including 11th, 12th, 13th (not 11st/12nd/13rd).

      Search ALL ADVI components for any hardcoded ordinal suffixes or naive
      "${n}th" / "${n}st" patterns. Replace every occurrence with formatOrdinal(n).

      Known location: Fee Efficiency panel (FeeEfficiencyPanel.tsx) efficiency_pctile display.
      Also check: AdvisorsTab (if any rank display), tooltip renders, any other pctile display.
    </description>
  </fix_1>

  <fix_2 label="Fee efficiency table: column sorting + rounded edges">
    <description>
      TABLE SORTING:
      The fee efficiency table currently has no sort interaction on column headers.
      Add click-to-sort behavior on every column header.

      Sort state cycle per column: Neutral → DESC → ASC → Neutral (3-state toggle).
      Only one column can be sorted at a time. Clicking a new column resets others to Neutral.

      Visual indicators in the column header:
        Neutral:  no icon (default state)
        DESC:     ↓ icon (ChevronDown from lucide-react), dimmed slightly (opacity 70%)
        ASC:      ↑ icon (ChevronUp from lucide-react), white

      Sortable columns (sort by):
        Name         -- alphabetical (string)
        AUA          -- numeric desc default
        Commission   -- numeric desc default
        Fee Rate     -- numeric desc default (bps)
        NNA          -- numeric, sort by absolute value or signed value (use signed)
        Efficiency   -- numeric desc default (pctile)
        [RANK if added from .043]

      Default sort: Efficiency DESC (highest percentile first) -- same as current.

      Implementation: add a useMemo that sorts the advisors array based on
      (sortColumn, sortDirection) state. Reset to default on period window change.

      ROUNDED TABLE EDGES:
      Apply rounded-lg (or rounded-xl to match other ADVI cards) to the outer table
      container. Ensure the first-row top corners and last-row bottom corners clip correctly.
      Use overflow-hidden on the container to enforce the border radius on cells.
    </description>
  </fix_2>

  <fix_3 label="Efficiency ratio label clarification (blocked on DS .045)">
    <description>
      After DS .045 investigation_2 confirms what the "ratio" column actually represents,
      DE must ensure the column label matches the actual field being displayed.

      Possible outcomes from DS .045:
        A. "ratio" = commission/nna (correct label: "Fee/NNA Ratio" or "Cost per NNA $")
        B. "ratio" = fee_bps_weighted displayed as % (mislabeled -- rename to "Fee Rate")
        C. "ratio" = regression_residual_ratio (relabel accordingly)

      Wait for DS .045 findings before relabeling. Do not rename blindly.

      Also: add a tooltip (HelpCircle icon) on the Efficiency column header explaining:
        "Percentile rank based on fee cost relative to net new assets. Higher = more
        efficient. Advisors with negative NNA are ranked separately below positive-NNA peers."
      This tooltip prevents future confusion about what efficiency means.
    </description>
  </fix_3>

  <drilldown_note label="Books tab advisor/client drilldown -- blocked">
    <description>
      Andrew confirmed: clicking into an advisor from the Books tab does not work.
      Client-level drilldown (L3) is also unavailable for assessment.

      This is BLOCKED pending investigation of the platinum data structure at advisor
      and client drill levels. The following is NOT in scope for this TO:
        - Fix the L2 advisor drilldown from Books tab
        - Spec the L3 client view

      Future TO (unnumbered, pending): once Andrew can access the advisor drill view,
      a separate DE TO will spec the Books tab advisor page and client page layouts.
      The platinum data for these levels exists (platinum/advisors/{id}/summary.json,
      platinum/clients/{id}/summary.json) -- the issue is likely a frontend routing or
      fetch error that needs diagnosis first.

      For now: note the breakage, do not attempt to fix it in this TO.
      DE should add a console.error with enough context to diagnose the failure mode
      (silent null? 401? 404? wrong path?) so the next TO can be properly specced.
    </description>
  </drilldown_note>

  <acceptance_criteria>
    1. formatOrdinal utility exists in lib/, all pctile displays use it (83rd not 83th)
    2. Fee efficiency table columns are clickable for sort; 3-state cycle works
    3. Sort default is Efficiency DESC; resets on period change
    4. Table container has rounded corners, overflow-hidden applied
    5. fix_3 column label deferred pending DS .045 (do not rename without findings)
    6. HelpCircle tooltip added to Efficiency column header
    7. Console.error added to drilldown failure path for diagnosis
    8. Build clean, no TypeScript errors
  </acceptance_criteria>


  <compiler_tools>
    comp-transform schema-check FeeEfficiencyPanel
      -- Run before fix_3 (ratio label). Shows which platinum fields are currently
         being rendered by FeeEfficiencyPanel and which are UNUSED. Tells you
         immediately which field = 0.53% without reading through the component.
         This is the fastest way to answer the "what is the ratio column displaying"
         question from DS .045 investigation_2.

    comp-pii scan ClientsTab
      -- Run as part of the drilldown diagnostic (drilldown_note). When the Books tab
         advisor drilldown is attempted, a PII scan on ClientsTab will reveal whether
         any relationship names are being fetched but failing silently (vs a routing
         error). Useful context for speccing the next TO.
  </compiler_tools>

</task_order>
