<to_id>YANG_SITTW.TO-2</to_id>
<project>YANG_SITTW</project>
<title>WS-2a Trailing-Two-Weeks: add 2W to Market Overview — the 4 tab heatmaps + Top/Bottom Performers</title>
<assigned_to>0.1.0_DE_MarketIntelligence</assigned_to>
<co_assignees>0.1.1_RD_MarketPerformance (components) + 0.1.0_DS_MarketIntelligence (ONLY if Phase-0 = data-side)</co_assignees>
<issued_by>2.0.0_SA_COO (PRD §7 decomposition, 2026-06-16; CTO handoff YANG_SITTW v0.2 42f6d414a + TTW-def 172336Z)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>complete</status>
<!-- COMPLETE 2026-06-16T1921Z (COO-accepted): FE leg verified DEV 27299745 — MECHANISM read from deployed Lambda (time_series[-10:]=10 sessions, §5 trap avoided by construction) + VALUES (served TTW == independent 10-session calc; non-div exact, div-payers differ by coherent total-return basis); additive/never-widen 71/71. Pending the YANG BATCH DT promote (TO-1+TO-2+TO-3 together) + Andrew promote/polish decision. Cross-pod total-return-basis gate reinforced to TO-3. -->>
<priority>Yang-ad-hoc, NOT urgent — slot behind live OPLMCP/GCONTR. **EXECUTION-GATED ON SPAWN**: Pod 1 DE 0.1.0 + RD 0.1.1 (+ DS 0.1.0 if data-side) are OFFLINE (allocation surfaced to MSTR/Andrew 2026-06-16). Pairs with TO-3 (same TTW computation).</priority>

<references>
  <ref type="prd">docs/architecture/YANG_SITTW.md (v0.2, 42f6d414a) — §4 WS-2 surfaces, §5 TTW-def RESOLVED, §7 TO-2, §8 acceptance</ref>
  <ref type="surfaces">portal/src/pages/MarketPerformance/ + components/market-performance/ExecutiveSummary.tsx — tabbed heatmaps (TabType = multi-asset|equities|fixed-income|commodities) + Top/Bottom Performers; period set 1D/1M/YTD... (NO 2W today)</ref>
</references>

<scope>
Add a `2W` (trailing-two-weeks) period to Market Overview, two surfaces:
1. **Top/Bottom Performers** — add TTW as a selectable period.
2. **The 4 tab-group performance heatmaps** (multi-asset / equities / fixed-income / commodities) — add a NEW `2W` column.

**Per-surface Phase-0 (the FE-vs-data fork) — classify BEFORE building each:** is the 2W return (a) DATA-PROVIDED (the market-returns producer emits per-period returns -> DS adds a 2W key) or (b) FE-COMPUTABLE from an available daily index/return series (-> RD computes in-component)? The period model is fixed-period-keyed (return-per-key), so determine the source per surface first.

FE work (both surfaces): add `'2W'` to the relevant period set(s) + render the column / selectable period.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-transform schema-check [the heatmap component] + comp-transform schema-check ExecutiveSummary</run>
      <expect>The period-keyed data contract for the heatmaps + Top/Bottom; confirm adding a '2W' key does not orphan a union/type. MISSING = runtime undefined.</expect>
      <if_mismatch>Reconcile the type/union to include '2W' before rendering; run comp-transform ternary-audit if 2W is a new mode/cohort in a switch.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io [the market-returns producer] — ONLY if Phase-0 = data-side</run>
      <expect>If data-side: the producer's WRITES include the per-period returns artifact the heatmaps read; enumerate its consumers before adding a 2W key (never-widen: 2W is an ADDITIVE period key — new field, not a moved one).</expect>
      <if_mismatch>If FE-computable instead, skip the producer touch entirely (RD computes from the daily series); document the Phase-0 classification in the log.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after change">
    <step>
      <run>2W values vs an INDEPENDENT trailing-10-trading-day calc (the acceptance check)</run>
      <expect>Every 2W cell = return over the most recent 10 trading sessions (P_latest / P_{10 sessions ago} - 1), matching the §5 definition + identical to TO-3's computation. comp-transform schema-check clean on every touched component.</expect>
      <if_mismatch>If 2W != the independent 10-session calc, or differs from TO-3's surfaces, the computation diverged — reconcile to the ONE shared definition before RAVC.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
**BINDING LABEL (Andrew-direct 2026-06-16): the user-facing label + the internal period key = `TTW`, NOT `2W`, across ALL 4 WS-2 surfaces (TO-2 + TO-3).** A split label (one page "TTW", one "2W") is the same silent-disagreement failure as a split definition. Definition UNCHANGED (the label change carries no math change).

**BINDING cross-pod shared computation (§5, Andrew-direct 2026-06-16) — IDENTICAL in TO-2 + TO-3:** Trailing-two-weeks (`TTW`) = **the trailing 10 TRADING days** (NOT 14 calendar). Return = `P_latest / P_{10 trading sessions ago} - 1`, trading-day-counted (a holiday week spans more calendar days but stays 10 sessions). Slot `2W` next to each surface's existing trading-day periods (e.g. if 1W = 5 sessions, 2W = 10). ALL FOUR WS-2 surfaces (this TO's Top/Bottom + 4 heatmaps, AND TO-3's return-vs-vol + BenchmarkHeatmap) MUST use this same trading-day-count logic — a split definition makes the surfaces silently disagree. If your Phase-0 finds the 2W must be DATA-emitted, coordinate the period-return definition with TO-3's producer touch so both pods' data agrees. MCP TO-3's lane (Pod 4) before committing a shared producer/util change.
</cross_domain_coordination>

<acceptance_criteria>
- A `2W` column appears in all 4 Market-Overview heatmaps + `2W` is a selectable period in Top/Bottom Performers.
- 2W values = an independent trailing-10-trading-day calc (§5 definition), consistent with TO-3's surfaces (cross-page agreement).
- comp-transform schema-check clean on every touched component (no runtime-undefined).
- Phase-0 (data-vs-FE-compute) classification documented per surface in the session log.
- Session log Compiler Tools section reproduces every `<run>` with observed output + pass/fail vs `<expect>`.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>If Phase-0 = FE-computed: no data change at all (RD computes 2W from the existing daily series). If Phase-0 = data-side: a 2W period-return key is ADDITIVE (new field, never-widen-safe — no existing series moves); a targeted re-emit of the returns artifact with the new key, verified additive. Classify + note per surface.</no_reprocess_needed></data_reprocess_scope>
