<task_order>
  <metadata>
    <id>ADVI_INFDEMO.001</id>
    <slug>rd-modelportfolios-benchmark-and-books-lookback</slug>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-05-28</date>
    <status>in_progress</status>
    <dispatch_held>false</dispatch_held>
    <progress note="F1+F2+F3 committed portal DEV f61cb40b; F3b committed 4bdb844e. bun run build PASS (all 4); comp-transform schema-check ConsolidatedOverviewPanel clean. CODE COMPLETE + build/schema/code-trace verified. OUTSTANDING: browser visual-confirm (CTO-required) — no browser-automation tool in this agent env; requesting Andrew (live dev server :5173) or CVO (F3 per CC) to visual-confirm to close. RAVC2 sent to COO 2026-05-28."/>
    <project_code>ADVI_INFDEMO</project_code>
    <priority>P0 — Inflection Wealth Management demo TODAY (Andrew direct 2026-05-28). Top priority. 2-4h runway.</priority>
    <sla>Fast — F1/F2 are one-liners; F3 is a focused adapter mapping. Bundle one portal DEV cycle.</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFDEMO.md (CTO 368e16b75) — F1, F2, F3, F3b</ref>
    <ref type="andrew_direct">Andrew 2026-05-28 ~1333Z: Model Portfolios default ETF benchmark + hide toggle; Books-tab missing lookback AUA (screenshot Peter Lee); active-since/role header gaps. Workers 0.4.2_RD + 0.4.0_DS named for this work.</ref>
    <ref type="surface">portal → AdvisorIntelligence → Model Portfolios page; portal → AdvisorIntelligence → advisor Book / Book Overview</ref>
  </references>

  <context>
    Demo-prep cleanup for the IWM presentation today. Portal is on DEV (Rule 19 — stays on DEV; do NOT promote to PROD as part of this TO). All four items are frontend; file paths + line numbers below are CTO-verified this session against current DEV. Read `comp-transform schema-check ConsolidatedOverviewPanel` before the F3 edit per CLAUDE.md.
  </context>

  <objective>
    Land four demo-prep frontend fixes on portal DEV: (F1) default Model Portfolios benchmark to ETF; (F2) hide the ETF/Index toggle reversibly; (F3) fix the missing snapshot-lookback AUA under the Book Overview radial; (F3b) investigate + address the "ACTIVE SINCE Unknown" / "PRIMARY TYPE NO ROLE DATA" header gaps.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/ModelPortfolios.tsx (F1 line 172; F2 lines 1337-1367)</file>
      <file action="modify">portal/src/api/endpoints/advisor-intelligence.ts (F3 line 1180; F3b lines 1196/1199)</file>
      <file action="readonly_reference">portal/src/pages/AdvisorIntelligence/_shared/panels/ConsolidatedOverviewPanel.tsx (F3 consumer — QuarterlyMetricsBar L80-176, getClassAua L68-73)</file>
      <file action="readonly_reference">portal/src/pages/AdvisorIntelligence/_shared/types.ts:1601 (FirmMixPeriodPoint target shape)</file>
      <file action="readonly_reference">portal/src/api/endpoints/advisor-intelligence.ts ~1410-1490 (getPlatinumClientDetailStatic — working mix_periods mapping pattern to mirror)</file>
      <file action="readonly_reference">portal/src/pages/AdvisorIntelligence/_shared/AdvisorPublicProfile.tsx (~1238-1261 role derive; ~1270/1293 active_since reader) — F3b</file>
    </files>
  </scope>

  <fix id="F1" priority="P0-trivial">
    <what>Model Portfolios must default to the ETF benchmark, not Index.</what>
    <where>portal/src/pages/ModelPortfolios.tsx:172</where>
    <current>const [benchmarkType, setBenchmarkType] = useState&lt;'index' | 'etf'&gt;('index')</current>
    <do>Change the useState default from 'index' to 'etf'. Downstream transform (~L335-348) already keys off benchmarkType — no other change.</do>
    <ac>Fresh load of Model Portfolios renders the ETF benchmark comparison populated (not empty), no console errors.</ac>
  </fix>

  <fix id="F2" priority="P0-trivial">
    <what>Temporarily HIDE the ETF/Index toggle — do NOT delete. Reversible.</what>
    <where>portal/src/pages/ModelPortfolios.tsx:1337-1367 — the "Benchmark:" label + Index/ETF button group inside the Benchmark Comparison PanelHeader actions. The sibling "Returns: Gross/Net" toggle (L1369-1400) MUST stay visible.</where>
    <do>Hide the Benchmark-toggle div without removing code. Prefer a named reversible guard: add `const SHOW_BENCHMARK_TOGGLE = false` and wrap the div in `{SHOW_BENCHMARK_TOGGLE &amp;&amp; ( ... )}`. Leave benchmarkType state (172), click handlers, and transform logic (335-348) fully intact — with F1 the page always shows ETF.</do>
    <ac>Index/ETF toggle not visible; Returns toggle still visible + functional; re-enable is a one-line flip; PanelHeader actions row layout does not break (gap-6 container collapses cleanly).</ac>
  </fix>

  <fix id="F3" priority="P0">
    <what>Book Overview: the three snapshot-lookback AUA slots beside "Current AUA" under the donut render "—" for Inflection advisors (screenshot: Peter Lee). Root cause = mapping bug; the data EXISTS in the payload but is never mapped.</what>
    <where>portal/src/api/endpoints/advisor-intelligence.ts:1180 — `mix_periods: raw.mix_periods ?? [],`</where>
    <root_cause>`raw.mix_periods` is undefined for Inflection so it falls back to []. The lookback data is present as `raw.historical_quarters` (interface L994: {period, label, end_date, total_aua, nna_canonical}), preserved via the 3-envelope merge, but never mapped into mix_periods. The consumer QuarterlyMetricsBar reads quarterlyMix=FirmMixPeriodPoint[] and getClassAua(pt, null) returns pt.total_aua for the default (no-class-selected) view — which is exactly the screenshot.</root_cause>
    <do>Replace the empty fallback with a mapping of raw.historical_quarters -&gt; FirmMixPeriodPoint[]: populate period, label, end_date, total_aua from each historical quarter; default the per-class FirmMixClassValue fields (equity/fixed_income/alternatives/cash) to zero/empty (historical_quarters has no per-class breakdown). Preserve precedence: `raw.mix_periods ?? &lt;mapped historical_quarters&gt;` so existing populated firms don't regress. Mirror the shape used by getPlatinumClientDetailStatic (~L1410-1490).</do>
    <ac>AC3.1: Peter Lee + other Inflection advisors with historical_quarters render real lookback AUA + QoQ in the 3 slots, not "—". AC3.2: Current-AUA QoQ vs most-recent completed quarter computes. AC3.3: no regression for firms/advisors that already populate mix_periods.</ac>
    <known_limitation>When a donut asset-class slice is selected, class-level lookback will show 0/"—" (historical_quarters carries only total_aua). That is OUT OF SCOPE for this TO — the default no-class view is the demo target. Do not block on it; note it for the post-demo per-class-emit follow-on.</known_limitation>
  </fix>

  <fix id="F3b" priority="P1">
    <what>Peter Lee header shows "ACTIVE SINCE Unknown" and "PRIMARY TYPE NO ROLE DATA". Likely shares F3's mapping-vs-emit pathology.</what>
    <where>active_since: adapter advisor-intelligence.ts:1199 (raw.active_since ?? activeSince); reader AdvisorPublicProfile.tsx ~1270/1293 (drilldownSummary?.active_since). role: adapter :1196 (role_breakdown ?? {}); reader AdvisorPublicProfile.tsx ~1238-1261 (primaryRole from role_breakdown, falls back roles[0], else "No role data").</where>
    <do>PHASE 1 — DETERMINE FIRST: does the Inflection book.json / leaderboard actually emit active_since + a role for these advisors? Inspect the live artifact. If emitted -&gt; wire the reader to the populated path (mapping fix). If NOT emitted -&gt; this is a DS data-emit gap OR legitimately absent for Inflection's single-role model; cascade 0.4.0_DS for confirm and flag CTO for the F3b posture decision (Q3 in PRD §4 — what the header should show instead). Do NOT fabricate values.</do>
    <ac>AC3b.1: source emit status determined. AC3b.2: if emitted, header shows real active-since + primary type. AC3b.3: if not emitted, escalate posture decision (don't guess).</ac>
  </fix>

  <phase id="verify" when="after write">
    <step>
      <run>bun run dev on portal DEV; open Model Portfolios (confirm F1 ETF default + F2 toggle hidden, Returns toggle present) and the Peter Lee Book Overview (confirm F3 lookback slots populated).</run>
      <expect>All ACs visually confirmed in the running app — this is a demo; visual confirmation is required, not just typecheck-green.</expect>
    </step>
    <step>
      <run>bun typecheck / lint per portal convention.</run>
      <expect>Clean. Inflection-adapter-only changes for F3/F3b — confirm no 49F / non-Inflection regression.</expect>
    </step>
  </phase>

  <acceptance>
    Commit to portal DEV (NOT PROD — Rule 19). RAVC2-Request to COO + CC CTO on completion. CVO /verify-channel will independently confirm F3 against the live artifact. Report F3b PHASE-1 emit-status finding explicitly so the posture decision can resolve.
  </acceptance>

  <notes>
    Demo TODAY, 2-4h runway. F1+F2 first (instant demo win), then F3, then F3b investigate. If anything is larger than it looks, flag CTO immediately rather than expanding scope silently.
  </notes>
</task_order>
