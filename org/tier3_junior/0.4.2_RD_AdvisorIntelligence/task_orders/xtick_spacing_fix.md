# Task Order — X-Tick Spacing Fix: AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-xtick-spacing-advisor-intelligence</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
    <priority>high</priority>
    <type>bug-fix</type>
  </metadata>

  <objective>
    Make the DistributionTab split layout in AdvisorIntelligence visually canonical
    with the equivalent split layout in ModelPortfolios. This means:
    (a) the donut (left partition) and bell curve (right partition) containers are
        the same height, and
    (b) the metrics rows below each chart partition sit at the same vertical level.
    Root cause is four structural mismatches vs ModelPortfolios, not purely a tick
    spacing issue.
  </objective>

  <problem>
    Four differences vs ModelPortfolios cause the visual disparity:

    1. DONUT CONTAINER HEIGHT (primary cause of layout misalignment):
       DistributionTab wraps the ApexCharts donut (left partition) in h-[380px].
       ModelPortfolios wraps its donut in h-[450px].
       This 70px mismatch means the left partition is shorter than the right, so
       the SnapshotDistributionMetrics row starts at a different Y position than
       the donut-side content — the two partitions are not level.

    2. BELL CURVE CONTAINER HEIGHT (mirrors problem 1):
       DistributionTab wraps SnapshotDistributionChart (right partition) in h-[380px].
       ModelPortfolios wraps AccountDistributionChart in h-[450px].
       The 70px deficit directly shrinks the plot area and makes the chart cramped.

    3. XAXIS HEIGHT (cause of gap between tick labels and metrics):
       SnapshotDistributionChart uses XAxis height={72}.
       AccountDistributionChart uses XAxis height={50}.
       The extra 22px allocates a dead strip of space below the axis line — the tick
       labels at negative angle extend upward (not downward) so that strip is visually
       empty, creating the perceived gap between the chart and the metrics row below.

    4. TICK MARGIN (secondary — same as other charts):
       No tickMargin set, so labels are flush against the axis line.
  </problem>

  <fix_standard>
    Four changes required to make DistributionTab canonical with ModelPortfolios:
    1. Donut container height: h-[380px] → h-[450px]   (DistributionTab.tsx ~line 1266)
    2. Bell curve container height: h-[380px] → h-[450px]  (DistributionTab.tsx ~line 1443)
    3. XAxis height: 72 → 50                            (SnapshotDistributionChart XAxis)
    4. tickMargin={16}                                  (SnapshotDistributionChart XAxis)
    The bottom margin change (15 → 50) also stands — with the container now at 450px,
    bottom=50 gives a plot area of 320px (identical to ModelPortfolios after its own fix:
    450 - 30 - 50 - 50 = 320).
    With both partitions at h-[450px], the SnapshotDistributionMetrics row and the
    donut-side quarter strip sit at identical vertical positions — matching ModelPortfolios.
  </fix_standard>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Four locations to edit:
        (1) the donut container div ~line 1266 (LEFT partition),
        (2) the bell curve container div ~line 1443 (RIGHT partition),
        (3) SnapshotDistributionChart AreaChart margin ~line 1764, and
        (4) SnapshotDistributionChart XAxis ~lines 1772-1780.
        All four are inside DistributionTab.tsx.
      </description>

      <change id="1">
        <location>
          ~Line 1266 — donut container div in the LEFT partition
          (search context: directly inside
           "&lt;div className="w-full max-w-[700px] flex flex-col gap-6 items-center"&gt;"
           in the LEFT PARTITION section, wrapping the ApexCharts donut + legend row)
        </location>
        <current>&lt;div className="h-[380px] flex items-center justify-center relative"&gt;</current>
        <new>&lt;div className="h-[450px] flex items-center justify-center relative"&gt;</new>
        <rationale>
          ModelPortfolios wraps its donut in h-[450px]. With the left partition at
          h-[380px] and the right at h-[450px] (after Change 2), the two partitions
          are mismatched in height — the SnapshotDistributionMetrics row starts 70px
          higher than the donut-side content. Setting both to h-[450px] levels them.
        </rationale>
      </change>

      <change id="2">
        <location>
          ~Line 1443 — chart container div wrapping SnapshotDistributionChart
          (search context: directly inside
           "&lt;div className="w-full max-w-[700px] flex flex-col gap-6 items-center"&gt;"
           in the RIGHT PARTITION section)
        </location>
        <current>&lt;div className="h-[380px] w-full min-w-0"&gt;</current>
        <new>&lt;div className="h-[450px] w-full min-w-0"&gt;</new>
        <rationale>
          ModelPortfolios uses h-[450px]. The 70px deficit is the primary cause of
          the cramped plot area. This is the most important change for the bell curve.
        </rationale>
      </change>

      <change id="3">
        <location>
          ~Line 1764 — AreaChart margin prop inside SnapshotDistributionChart
          (search context: the AreaChart directly under
           "&lt;ResponsiveContainer width="100%" height="100%"&gt;" inside
           SnapshotDistributionChart)
        </location>
        <current>margin={{ top: 30, right: 10, left: 0, bottom: 15 }}</current>
        <new>margin={{ top: 30, right: 10, left: 0, bottom: 50 }}</new>
        <rationale>
          With h-[450px] container, bottom=50 yields plot area of 320px
          (450 - 30 - 50 - 50 = 320) — identical to ModelPortfolios after its fix.
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Lines 1772-1780 — XAxis inside SnapshotDistributionChart AreaChart
        </location>
        <current>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-55}
            textAnchor="end"
            height={72}
            interval={0}
          /&gt;
        </current>
        <new>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-55}
            textAnchor="end"
            height={50}
            interval={0}
            tickMargin={16}
          /&gt;
        </new>
        <rationale>
          height: 72 → 50 — matches AccountDistributionChart. The 22px reduction
          eliminates the dead strip below the axis line (tick labels at negative angle
          extend upward, not downward, so that strip was visually empty whitespace).
          tickMargin={16} — adds gap between axis tick line and label text.
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. The file is very large.
      Read ~line 1260 for the donut container div (Change 1).
      Read ~line 1440 for the bell curve container div (Change 2).
      Read ~line 1690 onward for SnapshotDistributionChart (Changes 3 and 4).
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 4 changes. Changes 1 and 2 (both container heights) are the most
      important — they are what levels the two partitions. Do not apply a subset.
    </requirement>
    <requirement id="3">
      The two h-[380px] → h-[450px] changes are on different divs with different
      className strings:
      - Change 1 (donut): "h-[380px] flex items-center justify-center relative"
      - Change 2 (bell curve): "h-[380px] w-full min-w-0"
      Do not confuse them. Match on the full className string for each Edit call.
    </requirement>
    <requirement id="4">
      Do not touch any other container divs, chart components, or XAxis elements
      in DistributionTab.tsx. The only div heights being changed are the two at
      ~line 1266 and ~line 1443. No other heights, no other charts.
    </requirement>
    <requirement id="5">
      Do NOT touch the other XAxis elements in DistributionTab.tsx:
      - ComposedChart XAxis at ~line 546 (continuous view) — not in scope
      - AreaChart XAxis at ~line 862 (daily NNA chart) — not in scope
      - ClaSnapshotView XAxis at ~line 2067 (CLA diverging bar) — not in scope
    </requirement>
    <requirement id="6">
      Commit with tag: "0.4.0_DE_ClientPlatform: canonicalize AdvisorIntelligence distribution layout"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="7">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/xtick_spacing_advisor_intelligence.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      Donut container div (LEFT partition, ~line 1266) is h-[450px] (was h-[380px]).
    </criterion>
    <criterion id="2">
      Bell curve container div (RIGHT partition, ~line 1443) is h-[450px] (was h-[380px]).
    </criterion>
    <criterion id="3">
      SnapshotDistributionChart AreaChart bottom margin = 50.
    </criterion>
    <criterion id="4">
      SnapshotDistributionChart XAxis height = 50 (was 72). tickMargin={16}.
    </criterion>
    <criterion id="5">
      Resulting plot area = 450 - 30 - 50 - 50 = 320px. Matches ModelPortfolios.
    </criterion>
    <criterion id="6">
      Both partitions at h-[450px]: SnapshotDistributionMetrics and donut-side
      quarter strip sit at identical vertical positions — layout mirrors ModelPortfolios.
    </criterion>
    <criterion id="7">
      No other container heights or XAxis elements in DistributionTab.tsx modified.
    </criterion>
    <criterion id="8">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Change 1 must target the div at ~line 1266 (className contains "flex items-center justify-center relative"). Change 2 must target the div at ~line 1443 (className contains "w-full min-w-0"). Do not swap them.</constraint>
    <constraint>Do not change angle, textAnchor, fontSize, or interval on the XAxis.</constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
    <constraint>
      This fix is being applied in parallel with task order
      0.4.0_DE_ClientPlatform-2026-03-02-xtick-spacing-model-portfolios (issued to 0.4.1_RD_ModelPortfolios).
      Both fixes must use identical tickMargin={16} standard for cross-page uniformity.
    </constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx (4 changes:
      donut container height, bell curve container height, AreaChart bottom margin,
      XAxis height + tickMargin)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/xtick_spacing_advisor_intelligence.md
    </deliverable>
  </deliverables>
</task_order>
```
