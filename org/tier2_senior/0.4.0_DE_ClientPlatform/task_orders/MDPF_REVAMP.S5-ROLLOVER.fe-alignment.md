# TO MDPF_REVAMP.S5-ROLLOVER -- RENDER-CHECK + content-cutover validation (FE ALREADY ALIGNED)

**Project:** MDPF_REVAMP | **Assignee:** 0.4.0_DE_ClientPlatform | **Author/Gate:** 1.0.0_SA_CTO | **Coordinator:** 2.0.0_SA_COO | **Tandem:** 0.7.0_AE_CloudOps (cutover mechanics)
**Date:** 2026-07-21 | **Status:** complete -- RE-SCOPED 2026-07-21 ~191xZ -- the original "FE-alignment" premise was DISPROVEN by the DE's own audit (see below); this TO is now a render-check + serving-validation. -- SPRING-CLEAN 2026-08-25: project MDPF_REVAMP is complete; TO last touched 2026-07-21 predates project close 2026-07-22. Record act, not a work verdict.

## RE-SCOPE NOTE (why this TO changed)
The original scope assumed the FE read a LEGACY shape and had to be aligned to the revamp model-focused flat schema. **The DE FE-consumption audit (@86c741876) disproved that premise:** `getMdpfAggregateAUATimeSeries()` (the 443K nested/partners/etf artifact) has ZERO page/component call sites (dead code); the FE's live read is `getMdpfAggregateAUATimeSeriesByFirm('global')` -> `json/mdpf/global/aggregate-aua-timeseries.json` (161,772B FLAT), which is FIELD-IDENTICAL to the revamp (165,635B). AE independently re-verified (190028Z). **Result: ZERO FE code changes across all 7 keys; the S5 roll-over is a pure content/serving cutover, not an FE refactor.** So the FE-alignment work is DISCHARGED; what remains is to *prove it renders* off the revamp content before we flip.

## Scope -- RENDER-CHECK + content-cutover validation (NO FE code changes)
1. **RENDER-CHECK (pair with 0.7.0_AE_CloudOps), the gate deliverable.** The moment AE sets the Option-A serving-target (publisher lands the 7 revamp keys at the EXACT FE-read layout+filenames -- hyphen `json/mdpf/{scope}/aggregate-aua-timeseries.json` + `json/portfolios/*` -- on opal-data-assets, served via the scoped CF behavior), render the page off that content and confirm, FULL-DEPTH, all 3 firms:
   - **#1 ASSERTION (your invariant):** all 7 FE URLs resolve to the revamp content, byte-served as **JSON** (not CloudFront error-HTML). A bare origin-repoint would 404 on a path/filename mismatch -> `JSON.parse` fails silently -> blank chart. This is THE thing the render-check must catch. Confirm content-type + parseable + expected keys per URL.
   - **AUM-Daily** time series + **account-distribution** bell-curve + **non-model** panel render full-depth clean, all 3 firms (49financial / inflection / global).
   - **WITHIN-SET frontier coherence:** the AUM-analysis per-model `account_count` == the bell-curve `account_count` at TODAY (DS is wiring this coherent-by-construction off one shared roster source per the CTO (a) ruling). The two "today" counts must not visibly disagree.
2. **NO FE code changes** (audit-confirmed). Standing ratifications: SMA keep-as-is FOR CUTOVER (FE-safe); **NEVER drop the 2 blends** (`cohort_class='model'`); `sma`-drop (`cohort_class='sma'`) = OPTIONAL post-cutover cleanup only; basis label FE-ignored.
3. **Vestigial-nested cleanup DEFERRED:** removing the dead `getMdpfAggregateAUATimeSeries()` path is optional post-cutover housekeeping -- **confirm no non-FE consumer first**, then a separate cleanup. Not in this TO.

## Guardrails
- NO producer/data changes -- data is Andrew-confirmed-correct + triple-verified. ETFs = FUTURE schema expansion, not now.
- Cutover MECHANISM = **Option A** (origin-repoint, CTO-ruled over Option-2-in-place; AE's durability finding: legacy `build_aggregate_aua_timeseries.py` clobbers portal-v2 nightly). Mechanics = 0.7.0_AE_CloudOps. Rollback = router-revert (instant, legacy untouched).
- Render-check runs off the ACTUAL Option-A serving-target (opal-data-assets via the scoped CF behavior), not a local copy -- exercise the real serve path.

## Compiler-tools mandate
- `comp-routes trace` the AUM-Daily / model-portfolio endpoints (the ACTUAL FE-read path) to confirm the 7 URLs. `comp-transform schema-check` on the touched components (confirm no field regression). `comp-cache collisions` if any query key changes (it should not -- zero FE change).

## Gate / cutover (S5 push STAYS HELD until all clear)
- **Render-check clean** off the revamp artifacts (this TO) -- a named pre_push_condition in the streak-tracker.
- Coherent-7-key stage (DS/~A, option-a frontier) + the 3-pass covering all 7 incl the coherence assertion (CTO+DT+CVO).
- AE mechanism-A rollback (router revert-to-legacy, legacy UNTOUCHED shadow) TESTED-armed BEFORE publish (COO cond 1).
- COO re-co-sign pinned to the FINAL coherent-set ETags, coverage = all 7 served keys.
- Verify-before-first-serve on the first scheduled cycle (CVO gate).

Report to CTO (CC MSTR); build the render-check in tandem with 0.7.0_AE_CloudOps the moment the serving-target is set.
