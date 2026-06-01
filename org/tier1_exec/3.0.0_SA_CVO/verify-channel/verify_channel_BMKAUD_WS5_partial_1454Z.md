# BMKAUD WS-5 INDEPENDENT VERIFY — PARTIAL (components 1+3 PASS; 2 pending WS-4) — 2026-06-01T1454Z

**Verdict:** PARTIAL — **Component-1 (number validity) PASS + Component-3 (FE source-of-truth) PASS (Benchmark tab); Component-2 (change-completeness) HELD for WS-4 ledger.** NOT yet the final un-quarantine sign-off (gated on component-2).
**Verification surface:** WS-0 FROZEN evidence snapshot `s3://opal-data-mdpf/bmkaud-evidence/20260601T1445Z/` (MANIFEST attests freeze: smartx schedule DISABLED live-verified, yang upload-held; snapshot == live S3 @14:45Z, won't move). Verified the frozen consumer-resolved state per discipline, not a live mid-write target.
**Verifier≠fixer:** DS-CP/AE/RD did the work; CVO independently recomputes. Satisfied.

## Component-1 — NUMBER VALIDITY = PASS (independent recompute, my own harness)
Built an INDEPENDENT recompute (`.runtmp/bmkaud_ws5/recompute_ws5.py`, NOT DS-CP WS-2 code) from raw frozen `data_20260531_v1.pkl` → `return_daily`, replicating the documented post-revert transform (weekday+holiday filter, calendar-day windows 1M=end−30d / 1Q=end−91d, geometric compound, spread=model−index), compared to frozen `model_portfolio_benchmarks.json`:
- **40/40 cells MATCH to ≤0.01** — 1M + 1Q × {UST,ST,INT,LTC,LTA} × {model, index_benchmark, etf_benchmark, index_spread}. **ZERO mismatches.**
- `data_as_of` 2026-05-29 confirmed (my PKL read == JSON).
- **INT 1M = 2.95 independently confirmed** (the number flagged "broken" vs 4.62 last-complete-month): 2.95 is the correct trailing-30d value from the PKL. Per Andrew's KEEP-trailing ruling (WS-3 631d8d0d9) it is methodology-of-record-correct. **Benchmark vindicated by independent reproduction**, not just self-report.
- **PKL ambiguity (MANIFEST flag) RESOLVED:** lambda reads `data_*.pkl`→`return_daily` (derives `data_` from `model_` trigger key, `load_pkl(data_pkl_key)`); `model_*.pkl` is the sibling. Canonical = `data_20260531_v1.pkl`. (Confirms to WS-1/DS-CP.)

## Component-3 — FE SOURCE-OF-TRUTH INTEGRITY (Benchmark tab) = PASS
- Benchmark consumers (`portal-proxy.ts`) resolve ONLY `/api/general/benchmarks/{benchmark_returns, model_portfolio_benchmarks, model_portfolio_timeseries}.json` = the audited pure-yang outputs.
- `portal-proxy.ts` has **ZERO** references to `_smartx_model_monthly/_daily.json` — the FE never resolves the reverted SmartX benchmark sidecars. They are frozen + **orphan/unconsumed** (dead).
- The 7 `smartx` refs in `ModelPortfolios.tsx` are the **legitimate AUM panel** ("SmartX Model AUM" / "Source: SMArtX Advisory Solutions") — a real custody/AUM data source on a DIFFERENT surface, unrelated to the Benchmark-returns revert. Not a source-of-truth violation.
- **UST-1M Peers = FE-display falsy-zero guard, NOT data** (corroborates RD~B 8d3252f15): frozen `peer_performance.json` UST 1M block IS PRESENT — `model=0.3017, benchmark=0.1639`, percentiles p5=0.3126..p95=-0.0. The data exists in the feed; a JS falsy guard on small/`-0.0` values suppresses display. **RD owns the FE fix**; my component confirms it's display-not-source. (Peers source xlsx is NOT in the frozen prefix — independent re-parse of the xlsx deferred; DS-CP WS-2 reported UST-1M exact-trace from xlsx.)

## Component-2 — CHANGE COMPLETENESS = HELD for WS-4 ledger
Pre-confirmed inputs (not the full sweep): deployed `yang-model-portfolio-benchmarks` CodeSha256 `IYrvZ0zN...` == revert commit `80224d674` artifact (source-map + MANIFEST + AE grep-confirmed pure-yang, `model_source='yang_design'` only, one deploy today). Orphan `_smartx_*` benchmark sidecars frozen + FE-unconsumed (consistent with revert-complete + quarantine). **The exhaustive "no other swap / no orphaned writer / no un-TF path" sweep is AE's WS-4 deliverable** (landing shortly: smartx-model-monthly-pull orphan = finding #1, portal-v2 policy unmanaged-by-TF flagged). I verify the ledger is exhaustive + revert COMPLETE when it lands.

## Final sign-off gate (un-quarantine)
HELD pending: (1) WS-4 minute-ledger (AE, imminent) — verify exhaustive + revert-complete; (2) confirm the UST-1M FE falsy-zero guard fix is in/out of un-quarantine scope (RD-owned). On WS-4 ledger receipt I render the final WS-5 verdict + §5.6 input0 emit. Components 1+3 PASS de-risk the data + FE-source axes now.
