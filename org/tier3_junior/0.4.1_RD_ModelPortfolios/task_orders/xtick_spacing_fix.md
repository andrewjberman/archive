# Task Order — X-Tick Spacing Fix: ModelPortfolios

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-xtick-spacing-model-portfolios</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.1_RD_ModelPortfolios</issued_to>
    <date>2026-03-02</date>
    <status>complete</status>
    <priority>high</priority>
    <type>bug-fix</type>
  </metadata>

  <objective>
    Fix x-axis tick spacing on three chart elements in the ModelPortfolios page.
    The x-ticks are currently cramping against and overlapping the graph body on
    all three charts. The fix is uniform: increase the bottom margin on each
    chart container and add tickMargin to each XAxis to create consistent, clean
    separation between tick labels and the chart area. Apply the standard below
    uniformly — do not deviate per chart.
  </objective>

  <problem>
    All three charts share the same root cause: angled x-tick labels (-45° to -65°)
    with an insufficient bottom margin (currently 5px on two charts, which is far too
    small for rotated tick text that needs to clear the chart container edge). The
    result is tick labels that sit on top of or inside the chart plot area.

    Additionally, no chart currently sets tickMargin on XAxis, meaning tick labels
    are flush against the axis line itself with no gap.
  </problem>

  <fix_standard>
    Apply these two changes uniformly to every XAxis in scope:
    1. tickMargin={16}        — adds 16px gap between the axis tick line and the label text
    2. bottom margin increase  — gives rotated labels room to clear the container edge
       - For -45° angle: bottom from 5 → 40
       - For -65° angle: bottom from 5 → 50
  </fix_standard>

  <files_to_modify>

    <file path="portal/src/components/AccountDistributionChart.tsx">
      <description>
        Shared bell curve component. Used in ModelPortfolios Growth tab
        (Account Distribution panel, right partition).
      </description>
      <change id="1">
        <location>Line 119-122 — AreaChart margin prop</location>
        <current>margin={{ top: 30, right: 10, left: 0, bottom: 5 }}</current>
        <new>margin={{ top: 30, right: 10, left: 0, bottom: 50 }}</new>
        <rationale>-65° angle requires substantial bottom clearance.</rationale>
      </change>
      <change id="2">
        <location>Lines 130-138 — XAxis element</location>
        <current>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-65}
            textAnchor="end"
            height={50}
            interval={0}
          /&gt;
        </current>
        <new>
          &lt;XAxis
            dataKey="bin"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 7, fill: 'rgba(255,255,255,0.7)' }}
            angle={-65}
            textAnchor="end"
            height={50}
            interval={0}
            tickMargin={16}
          /&gt;
        </new>
        <rationale>tickMargin pushes labels away from the axis line.</rationale>
      </change>
    </file>

    <file path="portal/src/pages/ModelPortfolios.tsx">
      <description>
        Main page component. Contains two inline chart elements that need fixing:
        (1) Period End Summary BarChart and (2) Daily AUA Analysis AreaChart.
        Both are rendered inside the Growth tab (Portfolio Analytics panel).
      </description>

      <change id="3">
        <location>
          Lines ~1019-1031 — BarChart for "Period End Summary"
          (search context: "AUA Growth Trends - Stacked Bar Chart" comment above,
           panel section labeled "Period End Summary")
        </location>
        <current>margin={{ top: 5, right: 30, left: 0, bottom: 5 }}</current>
        <new>margin={{ top: 5, right: 30, left: 0, bottom: 40 }}</new>
        <rationale>-45° angle requires substantial bottom clearance.</rationale>
      </change>
      <change id="4">
        <location>
          Lines ~1024-1031 — XAxis inside the Period End Summary BarChart
        </location>
        <current>
          &lt;XAxis
            dataKey="period"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 11 }}
            angle={-45}
            textAnchor="end"
            height={60}
          /&gt;
        </current>
        <new>
          &lt;XAxis
            dataKey="period"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 11 }}
            angle={-45}
            textAnchor="end"
            height={60}
            tickMargin={16}
          /&gt;
        </new>
      </change>

      <change id="5">
        <location>
          Lines ~1204-1207 — AreaChart for "Daily AUA Analysis"
          (search context: "Daily AUA Analysis" h4 label immediately above)
        </location>
        <current>margin={{ top: 5, right: 30, left: 0, bottom: 5 }}</current>
        <new>margin={{ top: 5, right: 30, left: 0, bottom: 50 }}</new>
        <rationale>
          Matches AccountDistributionChart bell curve (bottom=50). See Change 6 for the
          root cause — margin alone is not sufficient; the tickFormatter and tickMargin
          override are also required.
        </rationale>
      </change>
      <change id="6">
        <location>
          Lines ~1231-1240 — XAxis inside the Daily AUA Analysis AreaChart
        </location>

        <root_cause_analysis>
          Three externalities distinguish Daily AUA Analysis from Period End Summary
          and the bell curve, explaining why spacing fixes alone have not resolved the overlap:

          1. tickMargin={0} is HARDCODED explicitly on this XAxis (line ~1239). It is not merely
             absent — it is actively zeroed. Any spacing fix must override this to a non-zero value.

          2. No tickFormatter. The period dataKey contains raw ISO date strings ("2025-01-15",
             10 characters). Period End Summary renders pre-formatted short strings from the API
             (e.g. "Jan 2025"). At -45° rotation a 10-char string sweeps a significantly larger
             arc into the chart body than a short formatted string, causing overlap that margin
             alone cannot fix.

          3. ticks={weeklyTicks} forces all filtered ticks to render — recharts cannot auto-thin
             them. The tickFormatter shortens each label, which is the correct lever here.
        </root_cause_analysis>

        <current>
          &lt;XAxis
            dataKey="period"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 11 }}
            angle={-45}
            textAnchor="end"
            height={80}
            ticks={weeklyTicks}
            tickMargin={0}
          /&gt;
        </current>
        <new>
          &lt;XAxis
            dataKey="period"
            stroke="rgba(255,255,255,0.5)"
            tick={{ fontSize: 11 }}
            angle={-45}
            textAnchor="end"
            height={80}
            ticks={weeklyTicks}
            tickMargin={16}
            tickFormatter={(value: string) =&gt; {
              const d = new Date(value + 'T12:00:00')
              return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
            }}
          /&gt;
        </new>
        <rationale>
          tickMargin: 0 → 16 — overrides the hardcoded zero.
          tickFormatter: formats "2025-01-15" → "Jan 15", matching the short-label style
          of Period End Summary and eliminating long-string overlap at the chart edge.
          The T12:00:00 suffix on the Date constructor prevents timezone offset from
          rolling the date back one day on negative-offset machines.
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read each file before editing. Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 6 changes. Do not apply a subset. Uniformity across all three
      charts is the acceptance criterion.
    </requirement>
    <requirement id="3">
      For the Period End Summary and AccountDistributionChart: scope is strictly
      bottom margin and tickMargin only — do not change any other properties.
      For Daily AUA Analysis: also add tickFormatter (see Change 6). The tickFormatter
      is required to fix the root cause (raw ISO string length); it is not optional.
    </requirement>
    <requirement id="4">
      Commit with tag: "0.4.0_DE_ClientPlatform: fix x-tick spacing on ModelPortfolios charts"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="5">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/xtick_spacing_model_portfolios.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      All 3 charts have tickMargin={16} on their XAxis.
    </criterion>
    <criterion id="2">
      AccountDistributionChart bottom margin = 50.
    </criterion>
    <criterion id="3">
      Period End Summary BarChart bottom margin = 40.
    </criterion>
    <criterion id="4">
      Daily AUA Analysis AreaChart bottom margin = 50. tickMargin overridden from 0 to 16.
      tickFormatter present, formatting ISO dates as "Mon D" (e.g. "Jan 15").
    </criterion>
    <criterion id="5">
      No other chart properties changed.
    </criterion>
    <criterion id="6">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not modify any chart besides the three explicitly listed.</constraint>
    <constraint>Do not change angle, height, textAnchor, fontSize, or any visual property other than bottom margin and tickMargin.</constraint>
    <constraint>AccountDistributionChart.tsx is a shared component — verify it is only used in ModelPortfolios before confirming this fix does not affect other pages.</constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/components/AccountDistributionChart.tsx (2 changes)
      and portal/src/pages/ModelPortfolios.tsx (4 changes)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/xtick_spacing_model_portfolios.md
    </deliverable>
  </deliverables>
</task_order>
```
