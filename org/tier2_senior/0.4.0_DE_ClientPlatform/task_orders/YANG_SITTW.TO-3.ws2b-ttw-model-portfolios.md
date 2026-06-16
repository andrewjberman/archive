<to_id>YANG_SITTW.TO-3</to_id>
<project>YANG_SITTW</project>
<title>WS-2b Trailing-Two-Weeks: add TTW toggle to Model Portfolios return-vs-vol panel + 2W to BenchmarkHeatmap</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<co_assignees>0.4.1_RD_ModelPortfolios (components) + 0.4.0_DS_ClientPlatform (ONLY if Phase-0 = data-side)</co_assignees>
<issued_by>2.0.0_SA_COO (PRD §7 decomposition, 2026-06-16; CTO handoff YANG_SITTW v0.2 42f6d414a + TTW-def 172336Z)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>staged</status>
<priority>Yang-ad-hoc, NOT urgent — slot behind live OPLMCP/GCONTR. **EXECUTION-GATED ON SPAWN**: Pod 4 DE 0.4.0 + RD 0.4.1 (+ DS 0.4.0 if data-side) are OFFLINE (allocation surfaced to MSTR/Andrew 2026-06-16). Pairs with TO-2 (same TTW computation).</priority>

<references>
  <ref type="prd">docs/architecture/YANG_SITTW.md (v0.2, 42f6d414a) — §4 WS-2 surfaces, §5 TTW-def RESOLVED, §7 TO-3, §8 acceptance</ref>
  <ref type="surfaces">portal/src/components/BenchmarkHeatmap.tsx — ALL_PERIODS = ['1D','WTD','MTD','1M','QTD','1Q','YTD','1Y','SI'] + PERIOD_LABELS (model/benchmark/spread rows; NO 2W) ; Model Portfolios "Performance" tab return-vs-volatility panel (existing period toggles, no 2W)</ref>
</references>

<scope>
Add `2W` (trailing-two-weeks) to the Model Portfolios "Performance" tab, two surfaces:
1. **Return-vs-volatility panel** — add the **TTW toggle** alongside the existing period toggles.
2. **BenchmarkHeatmap** — add `2W` to `ALL_PERIODS` + the `PERIOD_LABELS` map + the return data (model / benchmark / spread rows).

**Per-surface Phase-0 (the FE-vs-data fork) — classify BEFORE building each:** is the 2W return (a) DATA-PROVIDED (the model/benchmark returns producer emits per-period returns -> DS adds a 2W key) or (b) FE-COMPUTABLE from an available daily series (-> RD computes in-component)? Determine the source per surface first.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-transform schema-check BenchmarkHeatmap + comp-transform schema-check [the return-vs-vol panel]</run>
      <expect>The period-keyed contracts; confirm adding '2W' to ALL_PERIODS + PERIOD_LABELS + the return data does not orphan a union/type. MISSING = runtime undefined.</expect>
      <if_mismatch>Reconcile the type/union to include '2W'; comp-transform ternary-audit BenchmarkHeatmap if 2W is a new branch in a period switch.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io [the model/benchmark returns producer] — ONLY if Phase-0 = data-side</run>
      <expect>If data-side: the producer WRITES the per-period model/benchmark/spread returns the heatmap reads; enumerate consumers before adding a 2W key (additive period key — never-widen-safe).</expect>
      <if_mismatch>If FE-computable, skip the producer touch (RD computes from the daily series); document the Phase-0 classification.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after change">
    <step>
      <run>2W correct on model / benchmark / spread rows vs an INDEPENDENT trailing-10-trading-day calc</run>
      <expect>Every 2W cell (model, benchmark, AND spread) = return over the most recent 10 trading sessions (§5), identical to TO-2's computation. The return-vs-vol TTW toggle plots the 10-session return. comp-transform schema-check clean.</expect>
      <if_mismatch>If 2W != the independent 10-session calc, or the spread != model-benchmark under the same window, or it differs from TO-2's surfaces — reconcile to the ONE shared definition before RAVC.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
**BINDING cross-pod shared computation (§5, Andrew-direct 2026-06-16) — IDENTICAL in TO-2 + TO-3:** Trailing-two-weeks = **the trailing 10 TRADING days** (NOT 14 calendar). Return = `P_latest / P_{10 trading sessions ago} - 1`, trading-day-counted. Slot `2W` next to each surface's existing trading-day periods (e.g. if 1W = 5 sessions, 2W = 10). ALL FOUR WS-2 surfaces (TO-2's Top/Bottom + 4 heatmaps, AND this TO's return-vs-vol + BenchmarkHeatmap) MUST use this same trading-day-count logic — a split definition makes the surfaces silently disagree. The model/benchmark/spread rows must all compute the spread under the SAME 2W window (spread = model_2W - benchmark_2W). If Phase-0 finds 2W must be DATA-emitted, coordinate the period-return definition with TO-2's producer touch so both pods' data agrees — MCP TO-2's lane (Pod 1) before committing a shared producer/util change.
</cross_domain_coordination>

<acceptance_criteria>
- The return-vs-vol panel has a working TTW toggle; BenchmarkHeatmap shows `2W` in ALL_PERIODS + PERIOD_LABELS + the return data (model/benchmark/spread).
- 2W values = an independent trailing-10-trading-day calc (§5), spread = model_2W - benchmark_2W under the same window, consistent with TO-2's surfaces (cross-page agreement).
- comp-transform schema-check clean on BenchmarkHeatmap + the return-vs-vol panel (no runtime-undefined).
- Phase-0 (data-vs-FE-compute) classification documented per surface.
- Session log Compiler Tools section reproduces every `<run>` with observed output + pass/fail vs `<expect>`.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>If Phase-0 = FE-computed: no data change (RD computes 2W from the existing daily series). If data-side: an additive 2W period-return key (never-widen-safe — no existing return moves); targeted additive re-emit, verified. Classify + note per surface.</no_reprocess_needed></data_reprocess_scope>
