# TO MDPF_REVAMP.S5-ROLLOVER -- Frontend Alignment to the revamp model-focused schema

**Project:** MDPF_REVAMP | **Assignee:** 0.4.0_DE_ClientPlatform | **Author/Gate:** 1.0.0_SA_CTO | **Coordinator:** 2.0.0_SA_COO | **Tandem:** 0.7.0_AE_CloudOps (cutover mechanics)
**Date:** 2026-07-21 | **Status:** pending (GO via MSTR spawn ~18:23Z + FE-alignment re-brief @182618/182727Z)

## Context (Andrew-direct 2026-07-21, real-time)
The S5 cutover of the MDPF revamp (aggregate_aua_timeseries + account_distribution + non_model_assets, all 3 firms) was blocked at the publish gate. AE grounded the FE serving path (opal-data-portal-v2 via the public-data-router, NOT opal-data-assets) and found the revamp global aggregate (165K/427d) has a divergent SCHEMA from the served (443K/429d). GROUNDED: the divergence is INTENDED -- the revamp is MODELS-ONLY by design and correctly sheds the legacy `nested-aggregate` + `partners{49financial,inflection}` + `etf_decomposition{DIVZ,IDVZ,PFDE,PFOE}` + `methodology_version`. Andrew-direct verbatim: "this is focused solely on models, if we want to incorporate ETFs we can expand on the schema as needed to do so"; "our structure is correct on the data side... the issue is more a factor of making sure that we are clear on the frontend side with the 0.4.0_DE_ClientPlatform." DATA IS CORRECT; day-depth matches (427~429). Why parity missed it: DT/CVO date-joined parity compared VALUES at mapped paths, not the served SCHEMA/field-completeness.

## Scope -- FRONTEND ALIGNMENT ONLY (NO producer/data-side changes)
1. **FE-consumption audit** for all 7 revamp keys: every field each component / endpoint-transform / queryFn reads TODAY (the legacy shape off opal-data-portal-v2).
2. **The exact FE changes** to consume the revamp MODEL-FOCUSED FLAT schema (`opal_aggregate_aua`/`model_aua`/`non_model_aua`/`by_model`) off opal-data-assets.
3. **Confirm no legacy-only field** (`partners`/`etf_decomposition`/`nested-aggregate`) is LOAD-BEARING for a MODELS view. If one genuinely is (Andrew hedged "from what I can tell"), **SURFACE to CTO** -- it is a deliberate models-scope drop OR the sole case producer-side comes up -> CTO/Andrew ruling, NOT defaulted. Do NOT re-add producer fields by default.

## Guardrails
- NO producer/data changes -- data is Andrew-confirmed-correct. ETFs = FUTURE schema expansion, not now.
- Ground on the served + revamp artifacts + the FE queryFns -- NEVER assume.
- Cutover MECHANICS (publish + origin/router-repoint + tested rollback + version manifest) = 0.7.0_AE_CloudOps (CloudOps lane).

## Compiler-tools mandate
- `comp-routes trace` the AUM-Daily / model-portfolio endpoints (the ACTUAL FE-read path). `comp-transform schema-check` on every touched component. `comp-cache collisions` for any new query keys.

## Gate / cutover (S5 push STAYS HELD until all clear)
- FE aligned + `/frontend-dev` render-check: AUM-Daily + account-dist + non-model render FULL-DEPTH clean off the revamp artifacts, BEFORE live.
- CTO independent S3 re-verify of DS's count-wired artifacts (@82c4d1ec6) at the final gate.
- AE mechanism-A rollback (router revert-to-legacy, legacy opal-data-portal-v2 UNTOUCHED) TESTED-armed BEFORE publish (COO cond 1).
- COO re-co-sign against the aligned FE + render-check + mechanism A (@bfadb4f39 re-opened).
- **Mechanism A** = origin-repoint (publisher -> opal-data-assets/portal/*, repoint the router origin to opal-data-assets; rollback = repoint back, legacy untouched + shadow).

Report to CTO (CC MSTR); build in tandem with 0.7.0_AE_CloudOps.
