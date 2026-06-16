<to_id>YANG_SITTW.TO-4</to_id>
<project>YANG_SITTW</project>
<title>WS-2 data-side producer leg: emit an ADDITIVE `TTW` period (10 TRADING days) into BOTH the Market-Overview tiered producer AND the Model-Portfolio benchmark producer — trading-day-counted, never-widen-safe</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_assignees>none (AE-lane producer touch; FE legs are TO-2 0.1.0_DE + TO-3 0.4.0_DE, gated on this)</co_assignees>
<issued_by>2.0.0_SA_COO (YANG_SITTW Phase-0 outcome 2026-06-16; both DE leads classified DATA-SIDE + identified the producers as AE-lane Lambdas, correcting the original TO "DS if data-side" co-assignee)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>pending</status>
<priority>**UP-FIRST — Andrew-direct 2026-06-16 "YANG macro project up first."** This is the WS-2 critical path: both FE legs (TO-2 + TO-3) render the TTW column N/A until this producer key lands. Deploy-sequencing: the producer TTW key must land BEFORE/WITH each FE promote (no all-N/A column ships). Additive + never-widen-safe (no existing return moves) -> no CTO+COO never-widen co-sign required (distinct from TO-1).</priority>

<references>
  <ref type="prd">docs/architecture/YANG_SITTW.md (v0.2) §4 WS-2 surfaces, §5 TTW-def RESOLVED = 10 trading days</ref>
  <ref type="phase0-to2">0.1.0_DE_MarketIntelligence Phase-0 (181913Z): both Market-Overview surfaces DATA-PROVIDED off all-returns.json periodReturns; no in-payload daily series -> TTW must be an additive producer key.</ref>
  <ref type="phase0-to3">0.4.0_DE_ClientPlatform Phase-0 (181938Z): both Model-Portfolio surfaces DATA-SIDE off model_portfolio_benchmarks.json (need index AND ETF TTW; scatter vol producer-computed); ~2-line additive change.</ref>
</references>

<scope>
Two producer Lambdas, same additive-`TTW` pattern, both trading-day-counted (NOT calendar). `TTW` = §5 trailing 10 TRADING sessions: return = P_latest / P_{10 sessions ago} - 1; volatility through the producer's existing per-period vol path so methodology matches every other period.

**(A) Market-Overview tiered producer — `opal-market-overview-tiered-generator`**
- File: `infra/aws/lambda/v2_portal/01_market_overview/lambdas/market-overview-tiered-generator/lambda_function.py` (python3.11; reads DynamoDB `opal-portal-market-data`, emits `s3://opal-data-portal-v2/json-tiered/market-overview/summary/all-returns.json`).
- **§5 METHODOLOGY TRAP (the DE-flagged correctness gate):** this Lambda computes ALL period returns by CALENDAR-day arithmetic — `PERIOD_CALENDAR_DAYS = {1W:7, 1M:30, 1Q:91, 1Y:365,...}` + `calculate_period_return()` compounds over a calendar date window (L97-132, L135-189). **Do NOT add `TTW:14` to PERIOD_CALENDAR_DAYS** — that emits 14-calendar-day, violating §5. Add a TRADING-DAY-COUNTED path: the last 10 trading-day rows (`latest / price_10_rows_back - 1`). For market-overview INDICES the series is trading-days-only, so "last 10 rows" == 10 sessions (clean). Emit key = `TTW`.
- Touches: `calculate_all_returns` (L135-189) + `calculate_period_return` (L97-132).

**(B) Model-Portfolio benchmark producer — `yang-model-portfolio-benchmarks`**
- File: `infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py` (TF `module.model_portfolio_benchmarks`; ProcessBothPKLs branch of the YangDataPipeline Step Functions; emits `model_portfolio_benchmarks.json` + `benchmark_returns.json`).
- Change (DE-scoped, ~2 lines, additive): (1) periods list ~L191 append `'TTW'`; (2) in `calculate_period_returns()` add `elif period == 'TTW': period_data = series.tail(10)` among the window-setting branches (NOT the 1D early-return path). `series` is trading-day-indexed so `tail(10)` == §5 exactly; return=compound_returns + vol=calculate_volatility flow the existing generic path -> identical methodology to all periods; min_points=5 satisfied (10 pts). Emits model + index + ETF TTW (return/vol/spread) into BOTH artifacts. `etf_returns.json` / `yang-generate-etf-returns` does NOT need a touch (ETF mode reads etf_benchmark from the comprehensive file).

**Deploy:** Terraform (per Rule 1 — TF is the only Lambda deploy mechanism; safe-apply) + the YangDataPipeline re-run / market-overview pipeline re-run to regenerate the JSON (AE owns the re-run mechanism). NO console, no direct code push.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-iam service market-overview-tiered-generator + comp-iam service yang-model-portfolio-benchmarks</run>
      <expect>No NEW boto3 call introduced (the TTW key is pure compute on already-read data — DynamoDB read / PKL read unchanged). No new IAM permission needed.</expect>
      <if_mismatch>If a new permission surfaces, STOP — this should be pure-compute additive; a new perm means scope drifted. Surface to COO.</if_mismatch>
    </step>
    <step>
      <run>comp-blast all-returns.json + comp-blast model_portfolio_benchmarks.json</run>
      <expect>Enumerate consumers of each artifact before re-emit. Confirm the only period-keyed consumers are the WS-2 FE surfaces (PerformanceHeatMap/ExecutiveSummary for A; BenchmarkHeatmap/ReturnVolatilityScatter for B). An additive key breaks no consumer (additive = never-widen-safe).</expect>
      <if_mismatch>If a consumer hard-iterates period keys in a way an extra key breaks, document + coordinate before deploy.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy (additive-safe verify, NOT the never-widen co-sign)">
    <step>
      <run>Re-derive locally + diff served-before vs regenerated artifact for BOTH files</run>
      <expect>EVERY existing period key (1D/1W/1M/1Q/1Y/WTD/MTD/QTD/YTD/... and the model/index/etf/spread values) BYTE-UNCHANGED; the ONLY delta = the new `TTW` key added. Purely additive.</expect>
      <if_mismatch>STOP — if any existing period value moves, the change is not purely additive (a regression in the producer path). Fix before deploy; if a served value genuinely must move, that escalates to the CTO+COO never-widen gate (not expected here).</if_mismatch>
    </step>
    <step>
      <run>comp-iam gaps — ONLY if iam.tf changed</run>
      <expect>No new gaps. (iam.tf should NOT change for a pure-compute additive key.)</expect>
      <if_mismatch>Resolve gaps before apply.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>aws s3 cp the regenerated all-returns.json + model_portfolio_benchmarks.json + benchmark_returns.json; verify TTW key present + value correctness</run>
      <expect>`TTW` key present in all three served artifacts (mtime > deploy-commit-time). TTW value == an INDEPENDENT trailing-10-trading-session calc (latest / 10-rows-back - 1) per model/index/etf; spread = model_TTW - benchmark_TTW under the same window. All existing periods unchanged on the live artifact.</expect>
      <if_mismatch>STALE/wrong -> re-run the pipeline or revert; surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **GATES BOTH FE LEGS:** TO-2 (0.1.0_DE, all-returns.json) + TO-3 (0.4.0_DE, model_portfolio_benchmarks.json) author additive FE TTW that renders N/A until this producer key lands. DEPLOY-SEQUENCING: each producer artifact's TTW key must be live BEFORE/WITH the corresponding FE promote so no all-N/A column ever ships. On each artifact deploy, MCP the owning DE lane (+ CC COO) so they land + Phase-3-verify same-turn; flag DT for promote ordering.
- **§5 BINDING (Andrew-direct): TTW = 10 TRADING days, key+label = `TTW` (NOT `2W`, NOT 14 calendar).** IDENTICAL across all 4 WS-2 surfaces. Producer (A) MUST NOT reuse the calendar-day path; producer (B)'s `tail(10)` is correct by construction. Both DEs already aligned on the label/def.
- Additive + never-widen-safe -> NO CTO+COO never-widen co-sign (distinct from TO-1's MDPF re-derive which moves the band). The Phase-2 additive-diff IS the safety evidence.
</cross_domain_coordination>

<acceptance_criteria>
- Both producer Lambdas emit an additive `TTW` period (10 trading days, trading-day-counted) into all three served artifacts (all-returns.json; model_portfolio_benchmarks.json + benchmark_returns.json) — model + index + ETF where applicable.
- Producer (A) computes TTW via a TRADING-DAY-counted path (last 10 rows), NOT a `PERIOD_CALENDAR_DAYS` entry.
- Phase-2 additive-diff proves every existing period/value byte-unchanged (only TTW added).
- Phase-3 live-artifact verify: TTW value == independent trailing-10-session calc; spread = model_TTW - benchmark_TTW.
- Deployed via Terraform (safe-apply) + pipeline re-run; lambda-source-map current; tag if a pipeline tag applies.
- Each artifact deploy MCP'd to its FE-leg DE + CC COO for deploy-sequencing.
- Session-log Compiler Tools section reproduces every `<run>` with observed output + pass/fail vs `<expect>`.
</acceptance_criteria>

<data_reprocess_scope><reprocess_required>The producer change re-emits all-returns.json + model_portfolio_benchmarks.json + benchmark_returns.json with the new TTW key (additive). Phase-2 additive-diff (existing values byte-unchanged) is the safety gate; Phase-3 verifies the deployed artifacts' mtime > deploy-commit-time + TTW correctness. Additive period key = never-widen-safe (no existing series moves).</reprocess_required></data_reprocess_scope>
