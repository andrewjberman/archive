# BMKAUD WS-5 INDEPENDENT VERIFY — FINAL VERDICT — 2026-06-01T1507Z

**VERDICT: PASS — un-quarantine GO for the yang benchmark/peers data-writers.** (Sign-off gate cleared. Conditions + non-blocking residuals below.)
**Scope:** the DATA-WRITER pipeline (benchmark + peers correctness, revert-completeness, FE source-of-truth). NOT gating on the RD FE falsy-zero fix (parallel portal-DEV fast-follow) per COO.
**Verification surface:** WS-0 FROZEN snapshot `s3://opal-data-mdpf/bmkaud-evidence/20260601T1445Z/` + LIVE AWS cross-checks + repo forensics. Verifier≠fixer satisfied (DS-CP/AE/RD did the work; CVO independently verified). Sole verify-state writer.

## Three-component result — all PASS

### Component-1 NUMBER VALIDITY = PASS
Independent recompute (`.runtmp/bmkaud_ws5/recompute_ws5.py`, my own path) from raw frozen `data_20260531_v1.pkl` → **40/40 cells match** `model_portfolio_benchmarks.json` ≤0.01 (1M+1Q × 5 models × {model,index,etf,spread}), zero mismatches, `data_as_of` 2026-05-29. INT 1M=2.95 independently confirmed = correct trailing-30d → methodology-of-record per Andrew KEEP ruling. Disjoint cross-check of DS-CP HALF-A 360/360 consistent. PKL canonical = `data_20260531_v1.pkl` (resolved).

### Component-2 CHANGE COMPLETENESS = PASS
Independently corroborated AE WS-4 ledger (`4fd0f447b`, not rubber-stamped):
- **Revert PROVEN complete:** triple-corroboration — source-map `last_deployed_commit=80224d674` (revert) + `artifact_sha256=IYrvZ0zN` == LIVE CodeSha256 == revert artifact; deployed-bytes grep pure-yang (SmartX comments only); my own pre-stage read of post-revert lambda concurs (`model_source='yang_design'`). (This independently RESOLVES AE's A.5 flag — the source-map DOES carry the sha + deployed-commit.)
- **Change-set exhaustive:** SmartX work was contained to the benchmark producer (B1-B4: `84128c245`+`9f6357634`) + the smartx producer + ONE TF file (`smartx-pipeline/model-perf-pull.tf`); yang `lambdas.tf` untouched. No other swap.
- **Orphan `smartx-model-monthly-pull` (Finding #1):** schedule DISABLED + **consumers NONE** — directly corroborated by my Component-3 (portal-proxy zero `_smartx_*` references). MUST STAY DISABLED — recommend full retirement post-sign-off (do NOT un-quarantine the orphan).
- **No undocumented/console deploys**; ONE deploy today (yang-v2.4.9; ET-vs-UTC two-deploy artifact reconciled).

### Component-3 FE SOURCE-OF-TRUTH = PASS (Benchmark tab)
FE resolves only pure-yang `/api/general/benchmarks/*`; zero portal references to `_smartx_*` sidecars (orphan, frozen, dead). The 7 `smartx` refs in ModelPortfolios.tsx are the legitimate AUM panel (different surface). UST-1M Peers data present in feed (`model=0.3017, bench=0.1639, p95=-0.0`) → FE falsy-zero display guard (RD-owned fast-follow), not a data-writer defect.

## Un-quarantine ruling
- **GO: re-enable the yang benchmark + peers data-writers** (upload-gated; pure-yang verified, revert complete, numbers reproduce).
- **HOLD-DISABLED: `smartx-model-monthly-pull` orphan** — keep frozen; retire (Finding #1). It is NOT part of the un-quarantine.
- **Finding #2 (portal-v2 bucket policy unmanaged-by-TF):** folds into the WS-4 managed-import pass (CTO import ruling) — deploy-ops hygiene, non-blocking for data-writer un-quarantine.

## Non-blocking residuals (teed, do not gate this sign-off)
1. **Andrew design-residual:** LTC/LTA share one 'Long Term Benchmark' in the PKL (faithful-to-source, not mis-mapping) — Andrew design question.
2. **Andrew design-residual:** Peers external-xlsx provenance + refresh-cadence recommendation.
3. **RD fast-follow:** Peers UST-1M FE falsy-zero guard fix (portal-DEV) — distinct from data-writer un-quarantine.

## Honest-limit
Peers SOURCE xlsx was NOT in the frozen snapshot prefix — I could not independently re-parse xlsx→JSON. I confirmed JSON-data-presence + faithfulness-of-structure; the parse-faithfulness leg rests on DS-CP WS-2's xlsx exact-trace. Peers UST-1M is FE-display (not a data-writer issue), so this does not gate the data-writer un-quarantine. To close independently, add the frozen xlsx to the evidence prefix.

## Routing
PASS → COO (consolidates) + CTO (single RAVC2 to Andrew). §5.6 input0 verdict emitted (CLEAN, mechanical/intent/decision-useful all GREEN).
