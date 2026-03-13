```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-13-p3-advisors-tab-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-13</date>
    <status>pending</status>
    <thread_serial>ADVI_MVPLVL-003</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-003-p3-advisors-tab-alignment/</thread_ref>
  </metadata>

  <objective>
    Implement 3 frontend fixes on the Advisors Tab (3b, 3c, 3d) per ADVI_MVPLVL PRD
    Part 3 and thread ADVI_MVPLVL-003 alignment. Items 3b and 3c are independent
    correctness fixes. Item 3d is a visual redesign of the leaderboard — implement
    as flat list default with grouping-ready architecture (group-by decision deferred
    pending DS 3a research).
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="3b">
      Fix Top 3 panel overwritten by stacked bar.

      Current bug: AdvisorsTab.tsx:272-276 conditionally renders EITHER TopTenStackedBar
      OR Top3Highlights in Panel 1. When flowsData loads, Top 3 disappears.

      Fix:
      - Panel 1 (Top Performers): ALWAYS render Top3Highlights (gold/silver/bronze cards).
        Remove the flowsData conditional from Panel 1.
      - Panel 2 (Rolling Flows): render TopTenStackedBar when flowsData?.stacked_bar
        exists, otherwise fall back to existing RollingFlowsDivergingBar.
      - Normalize Panel 2 heights (stacked bar h-[340px], diverging bar h-[380px]) to
        a shared height to prevent layout jump on data load.
    </requirement>

    <requirement id="3c">
      Fix stacked bar NNA sort order instability.

      Root cause (confirmed in thread): XAxis uses dataKey="name" where name is
      truncated to 12 chars. Two advisors can collide on the same truncated label,
      causing visual re-bucketing and unstable ordering.

      Fix:
      - Keep truncated advisor name for display only.
      - Use a unique category key for XAxis dataKey (advisor_id or a generated xKey).
      - Render the truncated label via XAxis tickFormatter.
      - Ensure bars are ordered left-to-right by NNA descending (highest NNA on left).
    </requirement>

    <requirement id="3d">
      Leaderboard visual polish — redesign the leaderboard table.

      Current state: very small text (text-xs / text-[10px]), minimal color, cramped rows.
      The table at AdvisorsTab.tsx:854-979 needs a complete visual upgrade.

      Design language references (read these for style guidance):
      - portal/src/pages/SecurityScanner/SecurityScanner.tsx — card-based layouts
      - portal/src/pages/FactorTilts/FactorTilts.tsx — rich data presentation
      - Keyword Intelligence modal in CausalityEngine/MarketUpdate — typography + color

      Required visual improvements:
      - Bigger text: at least text-sm for values, text-xs for labels
      - Color: NNA values colored green (positive) / red (negative), growth % with
        gradient backgrounds, rank badges with visual weight
      - Information hierarchy: name prominent, metrics well-spaced
      - Card-like rows or generous padding instead of compact table
      - Implement as FLAT LIST default (no group-by)
      - Structure the component to accept an optional groupKey prop for future
        grouped view (collapsible sections by portfolio_group or alternative dimension).
        Keep this disabled/hidden until DS delivers 3a research artifact.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Panel 1 always shows Top3Highlights regardless of flowsData state</criterion>
    <criterion id="2">Panel 2 shows TopTenStackedBar when available, else rolling flows</criterion>
    <criterion id="3">Stacked bar displays bars in NNA descending order with no visual instability on period/role toggle</criterion>
    <criterion id="4">Leaderboard rows have substantially more visual presence — bigger text, color coding, clear hierarchy</criterion>
    <criterion id="5">bunx tsc -b passes clean</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT implement group-by portfolio_group as default — data is raw/unnormalized per thread findings</constraint>
    <constraint>Do NOT modify backend data or publisher — all changes are frontend only</constraint>
    <constraint>Commit on portal DEV branch with --author="0.4.2_RD_AdvisorIntelligence"</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.003.p3-architect-investigation" status="pending">
      3d group-by extension only — flat leaderboard is independent
    </dependency>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_MVPLVL_PRD.md (Part 3)</ref>
    <ref type="thread">org/threads/ADVI_MVPLVL-003-p3-advisors-tab-alignment/</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Portal DEV commit with 3b + 3c + 3d changes in AdvisorsTab.tsx</deliverable>
  </deliverables>
</task_order>
```
