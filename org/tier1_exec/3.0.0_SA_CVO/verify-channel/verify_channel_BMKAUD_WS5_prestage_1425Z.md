# BMKAUD WS-5 — pre-stage readiness (NOT a verdict) — 2026-06-01T1425Z

**Mode:** pre-execution prep (read-only). CTO GO `[BMKAUD WS-5] GO pre-stage` 1423Z. **No verdict rendered** — harness-readiness + chain-mapping only. Full WS-5 verify HOLDS for WS-0 quarantine snapshot + WS-2/WS-4 evidence.
**Discipline (CTO put on audit record):** do NOT recompute against live S3 pre-WS-0-freeze; the frozen consumer-resolved snapshot is the verification surface (same partition-vs-serving lesson).

## Component-1 (number validity) — harness READY
- **Canonical source CONFIRMED:** `benchmarks/LATEST.json` → `data_20260531_v1.pkl` (gen 2026-05-31T22:03:42Z) + sibling `model_20260531_v1.pkl`. The Benchmark generator reads **`data_*.pkl` → `return_daily`** (derives `data_` from `model_` trigger key). Brief's `data_YYYYMMDD_v1.pkl` path = CORRECT (my first-pass `model_*.pkl` was the sibling). **WS-1 coordination:** point my recompute + DS-CP at `data_20260531_v1.pkl`, don't fork.
- **Independent recompute logic captured** (from post-revert `yang-model-portfolio-benchmarks/lambda_function.py`; I will build my OWN path, not reuse DS-CP WS-2 code):
  - `get_term_returns`: `return_daily` filter `index_name contains "Term"` → datetime → **drop weekends (weekday<5)** → pivot date×index_name=return → **drop holiday all-zero rows** (`(fillna(0)!=0).any(axis=1)`).
  - Period windows (calendar-day arithmetic): 1D=tail(1); WTD=≥monday; MTD=≥month-1st; **1M=(idx>end−30d)&(≤end)**; QTD=≥quarter-1st; **1Q=(idx>end−91d)**; YTD=≥year-1st; 1Y=(idx>end−365d); SI=≥2024-04-30 annualized `(1+r)^(365/days)−1`.
  - `compound_returns`=∏(1+r/100)−1 ×100 round2; `volatility`=std(ddof=1)·√252 ×100 (min 5 pts, 20-pt window for 1D); `index_spread`=round(model−index,2).
  - `INDEX_NAME_MAP`: LTC/LTA SHARE 'Long Term Benchmark'+'Long Term ETF'; LTA model='Long Term Agressive' (source typo preserved).
- **Post-revert state in source:** `model_source='yang_design'` on every period; SmartX B1 monthly + B3 daily sidecar fully removed; model/benchmark/spread/vol all yang-computed from the same `return_daily` over consistent windows. Deployed `artifact_sha256=IYrvZ0zN...` == source-map entry (deploy-parity, post-revert).
- **Targets at fire:** 1M + 1Q × {UST,ST,INT,LTC,LTA} + UST Peers 1M, recomputed by me vs lambda output (`json/benchmarks/model_portfolio_benchmarks.json`) vs FE.

## Peers (UST 1M gap) — source characterized
Peers comes from uploaded `uploads/Models Performance vs Peers YYYYMM.xlsx` via `yang-generate-peer-performance` (fixed cell-offset parse of "Peer Table" sheet; `period_cols` 1M=(1,2)), → `json/peers/peer_performance.json`. **NOT Yang PKL.** PERIODS includes 1M, so UST-no-1M is either (a) xlsx UST 1M cell = `--`/empty (legit source gap) or (b) parse-offset miss. At fire: read frozen xlsx + output JSON, classify gap-vs-parse. (WS-2/WS-3 own the upstream classification; I verify the output faithfully reflects the xlsx.)

## Component-2 (change completeness) — 1 candidate examined + CLEARED
- `infra/aws/lambda/ycharts-market-data-pull/ws2_mp_benchmark_pull.py` = **YALP_MDSRC.C2 (0.2.0_DS) FROZEN benchmark-leg input-resourcing module.** Re-sources only the index/ETF BENCHMARK leg from public data per generator weights; Opal computation UNCHANGED; **no live call at import, no write to `json/benchmarks/*`** (generator owns the write). NOT a residual SmartX writer. Its docstring confirms the model-leg=SmartX/TO-B1 lineage (useful WS-4 ledger corroboration). Benign for live Benchmark output.
- Full residual-swap sweep (orphaned writers / un-TF paths / unmanaged portal-v2 bucket policy) is WS-4-gated; this is one pre-cleared candidate, not the sweep.

## Component-3 (FE source-of-truth) — chain located
- Benchmark: `portal/src/api/endpoints/benchmarks.ts` → `getBenchmarkReturns()` in `../portal-proxy` (S3-key resolution lives in portal-proxy — read at fire to confirm it resolves ONLY `json/benchmarks/*` pure-yang, no SmartX path).
- Peers: `portal/src/pages/ModelPortfolios/tabs/PeersTab.tsx` → `json/peers/peer_performance.json`.

## HOLD
Pre-stage complete; harness ready. HOLD for: (1) WS-0 quarantine snapshot to evidence prefix (pending Andrew greenlight on prod schedule-freeze), (2) WS-2 DS-CP number-validation evidence, (3) WS-4 AE change-forensics ledger. Fire full WS-5 on ping; verdict → verify_channel log + §5.6 input0 emit; report CTO, CC COO.
