# Task Order — Distribution Chart Nomenclature Fix: AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-02-distribution-nomenclature-advisor-intelligence</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-02</date>
    <status>pending</status>
    <priority>high</priority>
    <type>nomenclature-fix</type>
  </metadata>

  <objective>
    Fix all axis labels, tooltip labels, metrics tile labels, and footnotes in
    SnapshotDistributionChart and SnapshotDistributionMetrics to use accurate,
    mode-aware nomenclature.

    The chart operates in two fundamentally different data modes, each with its
    own correct unit of analysis:

    - AUA mode  (default, isNnaMode=false):
        Histogram bins individual Black Diamond *account* balances.
        Data source: gold/account_performance.parquet (account_id level).
        One observation = one funded account.
        Canonical unit: "account".

    - NNA mode  (isNnaMode=true):
        Histogram bins each *relationship's* period NNA.
        Data source: client_performance.parquet (relationship_id level).
        One observation = one relationship (relationship_id).
        Canonical unit: "relationship".

    Current labels ("Client AUA", "Client Count", "Number of Clients", "Total Clients")
    are wrong in both modes:
    - In AUA mode: data is account-level but labels imply relationship-level.
    - In NNA mode: "client" is informal and non-specific; "relationship" is the
      correct BD term that matches the underlying relationship_id key.

    ModelPortfolios (SmartX data) uses "Holdings" for the equivalent chart.
    AdvisorIntelligence (Black Diamond data) must NOT copy "holdings" — the correct
    BD term is "account". The formatting pattern (consistent label + tooltip + footnote)
    is the same; only the vocabulary differs.
  </objective>

  <data_context>
    Confirmed by reading data/black_diamond/scripts/gold/09_generate_partner_analytics.py:

    AUA distribution (lines 584, 621-623):
      acct_arch = acct_perf_day (gold/account_performance.parquet)
      arch_accts = acct_arch[acct_arch['architect'] == arch]
      adv_dist   = calculate_distribution_stats(arch_accts['total_aua'])
      One row = one Black Diamond account (account_id level).
      DistributionStats.count = number of funded accounts in that segment.

    NNA distribution (line 396-400, 508-509):
      rel_nna = _compute_rel_period_nna(cp_end, cp_start)
        returns DataFrame with columns: relationship_id, period_nna
      calculate_nna_distribution_stats(rel_nna['period_nna'])
      One row = one relationship (relationship_id level).
      DistributionStats.count = number of relationships.

    ModelPortfolios reference (AccountDistributionChart.tsx):
      Y-axis:       "Number of Holdings"    (SmartX-specific vocabulary)
      X-axis:       "Holding Size"          (SmartX-specific vocabulary)
      Tooltip row 1: "Holding Size"
      Tooltip row 2: "Account Count"        (note: row 2 already says "Account")
      Metrics tile: "Total Holdings"        (SmartX-specific vocabulary)
      Footnote:     "Excludes {N} newly opened holdings with $0 balance (unfunded)."

    AdvisorIntelligence must NOT use "Holdings" — that is SmartX terminology.
    The correct BD vocabulary is "account" (singular/plural) for AUA mode and
    "relationship" for NNA mode.
  </data_context>

  <nomenclature_standard>
    AUA mode (isNnaMode = false) — account-level data:
      Y-axis label:       "Number of Accounts"
      X-axis label:       "Account Size"
      Tooltip row 1 key:  "Account Size"
      Tooltip row 2 key:  "Account Count"
      Metrics tile label: "Total Accounts"
      Footnote amber:     "Excludes accounts with $0 balance (unfunded)."
      Footnote muted:     " Distribution reflects funded accounts only, log-spaced bins."

    NNA mode (isNnaMode = true) — relationship-level data:
      Y-axis label:       "Number of Relationships"
      X-axis label:       "Period NNA"
      Tooltip row 1 key:  "NNA Range"
      Tooltip row 2 key:  "Relationship Count"
      Metrics tile label: "Total Relationships"
      Footnote:           (keep existing NNA footnote — no change)
  </nomenclature_standard>

  <files_to_modify>

    <file path="portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx">
      <description>
        Eleven changes across four locations:
        (A) SnapshotDistributionChartProps interface + function signature (~lines 1696-1702)
        (B) SnapshotDistributionChart body — axis labels + tooltip (~lines 1759-1812)
        (C) SnapshotDistributionMetrics function signature + primary tile (~lines 1853-1877)
        (D) Call sites in SnapshotDistributionView + right-partition footnote (~lines 1444-1462)
      </description>

      <!-- ================================================================ -->
      <!-- A. SnapshotDistributionChartProps + function signature           -->
      <!-- ================================================================ -->

      <change id="1">
        <location>~Lines 1696-1700 — SnapshotDistributionChartProps interface</location>
        <current>
interface SnapshotDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number
}
        </current>
        <new>
interface SnapshotDistributionChartProps {
  data: DistributionStats
  accentColor?: string
  globalMaxCount?: number
  isNnaMode?: boolean
}
        </new>
        <rationale>Adds the mode flag so the chart can render mode-aware labels.</rationale>
      </change>

      <change id="2">
        <location>~Line 1702 — SnapshotDistributionChart function signature</location>
        <current>
function SnapshotDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount }: SnapshotDistributionChartProps) {
        </current>
        <new>
function SnapshotDistributionChart({ data, accentColor = '#5e72e4', globalMaxCount, isNnaMode = false }: SnapshotDistributionChartProps) {
        </new>
        <rationale>Destructures the new prop with a safe default of false (AUA mode).</rationale>
      </change>

      <!-- ================================================================ -->
      <!-- B. SnapshotDistributionChart body — axis labels + tooltip        -->
      <!-- ================================================================ -->

      <change id="3">
        <location>
          ~Line 1760 — Y-axis label text inside SnapshotDistributionChart
          (the span inside the absolute-positioned vertical div,
           search context: writingMode vertical-rl, text "Number of Clients")
        </location>
        <current>
          Number of Clients
        </current>
        <new>
          {isNnaMode ? 'Number of Relationships' : 'Number of Accounts'}
        </new>
        <rationale>
          AUA mode: counts individual Black Diamond accounts.
          NNA mode: counts relationships (relationship_id level).
          "Clients" was wrong for both.
        </rationale>
      </change>

      <change id="4">
        <location>
          ~Line 1767 — X-axis label span inside SnapshotDistributionChart
          (absolute-positioned div at bottom, search: "Client AUA")
        </location>
        <current>
          &lt;span className="text-[11px] text-white/50"&gt;Client AUA&lt;/span&gt;
        </current>
        <new>
          &lt;span className="text-[11px] text-white/50"&gt;{isNnaMode ? 'Period NNA' : 'Account Size'}&lt;/span&gt;
        </new>
        <rationale>
          AUA mode: x-axis is the size of an individual account ("Account Size").
          NNA mode: x-axis is the relationship's period NNA ("Period NNA").
        </rationale>
      </change>

      <change id="5">
        <location>
          ~Line 1807 — Tooltip row 1 label inside RechartsTooltip
          (search: the span with text "Client AUA" — first row in tooltip content)
        </location>
        <current>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;Client AUA&lt;/span&gt;
        </current>
        <new>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;{isNnaMode ? 'NNA Range' : 'Account Size'}&lt;/span&gt;
        </new>
        <rationale>Tooltip row 1 names the x-axis bin. Must match x-axis label.</rationale>
      </change>

      <change id="6">
        <location>
          ~Line 1811 — Tooltip row 2 label inside RechartsTooltip
          (search: the span with text "Client Count" — second row in tooltip content)
        </location>
        <current>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;Client Count&lt;/span&gt;
        </current>
        <new>
                      &lt;span className="text-[hsl(var(--semantic-text-chartTooltip))]/70 text-sm"&gt;{isNnaMode ? 'Relationship Count' : 'Account Count'}&lt;/span&gt;
        </new>
        <rationale>
          AUA mode: the bar height is a count of accounts in that size bin.
          "Account Count" matches ModelPortfolios tooltip row 2 exactly.
          NNA mode: count is relationships.
        </rationale>
      </change>

      <!-- ================================================================ -->
      <!-- C. SnapshotDistributionMetrics — function signature + tile label -->
      <!-- ================================================================ -->

      <change id="7">
        <location>
          ~Line 1853 — SnapshotDistributionMetrics function signature
          (search: "function SnapshotDistributionMetrics({ data, currentData }")
        </location>
        <current>
function SnapshotDistributionMetrics({ data, currentData }: { data: DistributionStats; currentData?: DistributionStats | null }) {
        </current>
        <new>
function SnapshotDistributionMetrics({ data, currentData, isNnaMode = false }: { data: DistributionStats; currentData?: DistributionStats | null; isNnaMode?: boolean }) {
        </new>
        <rationale>Adds mode flag so the primary tile label can be mode-aware.</rationale>
      </change>

      <change id="8">
        <location>
          ~Lines 1874-1878 — Primary tile inside SnapshotDistributionMetrics
          (search: comment "Total Clients" and the div containing it)
        </location>
        <current>
        {/* Total Clients */}
        &lt;div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85%)]/40 min-w-[100px]"&gt;
          &lt;div className="text-xs text-white/90 font-semibold mb-1"&gt;Total Clients&lt;/div&gt;
          &lt;div className="text-lg font-bold text-white"&gt;{data.count.toLocaleString()}&lt;/div&gt;
        &lt;/div&gt;
        </current>
        <new>
        {/* Total Accounts / Total Relationships */}
        &lt;div className="flex flex-col items-center px-4 py-1.5 rounded bg-[hsl(253,74%,85%)]/15 border border-[hsl(253,74%,85())]/40 min-w-[100px]"&gt;
          &lt;div className="text-xs text-white/90 font-semibold mb-1"&gt;{isNnaMode ? 'Total Relationships' : 'Total Accounts'}&lt;/div&gt;
          &lt;div className="text-lg font-bold text-white"&gt;{data.count.toLocaleString()}&lt;/div&gt;
        &lt;/div&gt;
        </new>
        <rationale>
          AUA mode: count is funded Black Diamond accounts → "Total Accounts".
          NNA mode: count is relationships → "Total Relationships".
          data.count is correct for both — only the label text changes.
        </rationale>
      </change>

      <!-- ================================================================ -->
      <!-- D. Call sites + right-partition footnote                         -->
      <!-- ================================================================ -->

      <change id="9">
        <location>
          ~Line 1444 — SnapshotDistributionChart JSX element inside SnapshotDistributionView
          (search: "&lt;SnapshotDistributionChart" — the component usage, not its definition)
        </location>
        <current>
              &lt;SnapshotDistributionChart
                data={distributionData}
                accentColor={selectedSegment?.color || parentSegment?.color || 'hsl(var(--primary))'}
                globalMaxCount={globalMaxCount}
              /&gt;
        </current>
        <new>
              &lt;SnapshotDistributionChart
                data={distributionData}
                accentColor={selectedSegment?.color || parentSegment?.color || 'hsl(var(--primary))'}
                globalMaxCount={globalMaxCount}
                isNnaMode={isNnaMode}
              /&gt;
        </new>
        <rationale>
          isNnaMode is already a const in SnapshotDistributionView scope
          (derived from: const isNnaMode = metric === 'nna').
          Threading it into the chart component so it can render mode-aware labels.
        </rationale>
      </change>

      <change id="10">
        <location>
          ~Line 1451 — SnapshotDistributionMetrics JSX element inside SnapshotDistributionView
          (search: "&lt;SnapshotDistributionMetrics data={distributionData}")
        </location>
        <current>
              &lt;SnapshotDistributionMetrics data={distributionData} currentData={currentDistributionData} /&gt;
        </current>
        <new>
              &lt;SnapshotDistributionMetrics data={distributionData} currentData={currentDistributionData} isNnaMode={isNnaMode} /&gt;
        </new>
        <rationale>Threads the mode flag into the metrics component for the tile label.</rationale>
      </change>

      <change id="11">
        <location>
          ~Lines 1457-1461 — AUA branch of the right-partition footnote
          (search: amber span "Excludes accounts with $0 balance (unfunded)."
           and the muted span " Distribution uses log-spaced bins across funded accounts only.")
        </location>
        <current>
                    &lt;span className="text-amber-400 font-bold"&gt;Excludes accounts with $0 balance (unfunded).&lt;/span&gt;
                    &lt;span className="text-white/40"&gt; Distribution uses log-spaced bins across funded accounts only.&lt;/span&gt;
        </current>
        <new>
                    &lt;span className="text-amber-400 font-bold"&gt;Excludes accounts with $0 balance (unfunded).&lt;/span&gt;
                    &lt;span className="text-white/40"&gt; Distribution reflects funded accounts only, log-spaced bins.&lt;/span&gt;
        </new>
        <rationale>
          The amber span is already correct — "accounts" is right.
          Only the muted span changes: shorter phrasing, consistent with ModelPortfolios
          footnote structure ("reflects funded accounts only" instead of the more wordy
          "uses log-spaced bins across funded accounts only").
        </rationale>
      </change>
    </file>

  </files_to_modify>

  <requirements>
    <requirement id="1">
      Read DistributionTab.tsx before editing. Use offset reads:
      - ~line 1696 for Changes 1-2 (interface + function signature)
      - ~line 1755 for Changes 3-6 (axis labels + tooltip body)
      - ~line 1853 for Changes 7-8 (metrics component)
      - ~line 1440 for Changes 9-11 (call sites + footnote)
      Use the Edit tool — never sed or heredoc.
    </requirement>
    <requirement id="2">
      Apply all 11 changes. Do not apply a subset.
      Changes 3-6 and 8 are the most visible to users. Changes 1-2 and 7 are
      the prerequisite interface wiring. Changes 9-11 are the connective tissue.
    </requirement>
    <requirement id="3">
      isNnaMode is already declared in SnapshotDistributionView scope as:
        const isNnaMode = metric === 'nna'
      You are NOT introducing a new variable. You are only threading it as a prop
      into SnapshotDistributionChart (Change 9) and SnapshotDistributionMetrics
      (Change 10), then consuming it inside those functions (Changes 3-8).
    </requirement>
    <requirement id="4">
      Do not change the NNA footnote text (the isNnaMode=true branch, ~line 1454).
      Only the AUA branch text is updated (Change 11 — muted span wording only).
    </requirement>
    <requirement id="5">
      Do not change the right-partition section header (distributionLabel h4),
      the help tooltip on that header, or the donut legend client_count labels.
      Those are in separate scope and are not part of this task.
    </requirement>
    <requirement id="6">
      Do not change any percentile tile (P10/P25/Median/P75/P90) in
      SnapshotDistributionMetrics. Only the primary "Total" tile (Change 8) changes.
    </requirement>
    <requirement id="7">
      ModelPortfolios uses data.account_count; DistributionTab uses data.count.
      These are different TypeScript interface shapes (aum endpoint vs AI types).
      Do NOT attempt to change data.count to data.account_count. Display label
      changes only — field access is untouched.
    </requirement>
    <requirement id="8">
      Commit with tag:
      "0.4.0_DE_ClientPlatform: fix distribution chart nomenclature — accounts/relationships"
      Do not git push — DT is the QA gate.
    </requirement>
    <requirement id="9">
      Write a session log at:
      logs/sessions/2026-03-02/react_designer/distribution_nomenclature_fix.md
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      SnapshotDistributionChartProps has isNnaMode?: boolean field.
    </criterion>
    <criterion id="2">
      In AUA mode (isNnaMode=false):
      Y-axis = "Number of Accounts"
      X-axis = "Account Size"
      Tooltip row 1 = "Account Size"
      Tooltip row 2 = "Account Count"
    </criterion>
    <criterion id="3">
      In NNA mode (isNnaMode=true):
      Y-axis = "Number of Relationships"
      X-axis = "Period NNA"
      Tooltip row 1 = "NNA Range"
      Tooltip row 2 = "Relationship Count"
    </criterion>
    <criterion id="4">
      SnapshotDistributionMetrics primary tile:
      AUA mode = "Total Accounts", NNA mode = "Total Relationships".
    </criterion>
    <criterion id="5">
      Right-partition AUA footnote muted span reads:
      " Distribution reflects funded accounts only, log-spaced bins."
    </criterion>
    <criterion id="6">
      isNnaMode={isNnaMode} is present on both
      &lt;SnapshotDistributionChart&gt; and &lt;SnapshotDistributionMetrics&gt; call sites.
    </criterion>
    <criterion id="7">
      No other labels, data fields, percentile tiles, section headers,
      or donut legend text changed.
    </criterion>
    <criterion id="8">
      Changes committed. Session log written.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not use "Holdings" anywhere — that is SmartX/ModelPortfolios vocabulary.
      AdvisorIntelligence data is Black Diamond. The correct terms are
      "account" (AUA mode) and "relationship" (NNA mode).
    </constraint>
    <constraint>
      Change 8 edits the JSX comment and the tile label text only.
      The className strings on the surrounding divs are identical — match them
      exactly when constructing the old_string for the Edit tool.
    </constraint>
    <constraint>Do not push to remote — DT deploys.</constraint>
    <constraint>
      Changes 3-6 use JSX expressions ({isNnaMode ? '...' : '...'}) inside
      text nodes. Verify JSX is syntactically valid after each edit.
    </constraint>
  </constraints>

  <deliverables>
    <deliverable type="code-commit">
      Changes to portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx
      (11 changes: SnapshotDistributionChartProps, SnapshotDistributionChart body,
      SnapshotDistributionMetrics, call sites, AUA footnote)
    </deliverable>
    <deliverable type="session-log">
      logs/sessions/2026-03-02/react_designer/distribution_nomenclature_fix.md
    </deliverable>
  </deliverables>
</task_order>
```
