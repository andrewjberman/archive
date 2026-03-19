# ADVI_BKSCMP PRD + ADVI_MVP318 Corrections — 1.0.0_SA_CTO

**Date:** 2026-03-19
**Start Time:** session start
**End Time:** ongoing

## Objective

Ground truth corrections for ADVI_MVP318 (WS1-WS5 complete, bd-v2.19.2), then research
and author full PRD for ADVI_BKSCMP — the Books tab per-class composition artifact system
that unblocks N1/L2 holdings rendering in the ConsolidatedOverviewPanel.

---

## Work Completed

### 1. Ground Truth Corrections (7 documents)

| Document | Correction |
|---|---|
| `ADVI_MVP318.json` | phase/blocking corrected to Phase 1 (first), then Phase 3 (WS1-WS5 complete, bd-v2.19.2, WS6 only remaining) |
| `REGISTRY.md` | ADVI_MVP318 row corrected to Phase 3 |
| `prompt.md` (session 5→6) | bd-v2.19.0→bd-v2.19.2, partners-api-v1.3.0→v1.4.0, ADVI_MVP318 status corrected, ADVI_MVPLVL MVPLVL.006 noted as deployed |
| `memory/MEMORY.md` | bd-v2.18.4→bd-v2.19.2, partners-api-v1.0.0→v1.4.0 |
| `ADVI_BKSCMP.json` | Created — project registered |
| `REGISTRY.md` | ADVI_BKSCMP row added |
| `prompt.md` (session 6→7) | ADVI_BKSCMP added to active projects |

### 2. Architecture Investigation — Books Tab Composition

Read `ClientsTab.tsx` (full component), `types.ts`, `opal-partners-data/lambda_function.py`,
`run_gold_layer.sh`, `06b_build_client_mix_timeseries.py`.

**Key findings:**
- `fetchComposition('firm', 'all', firmId)` and `fetchComposition('advisor', id, firmId)` already
  exist in ClientsTab.tsx (lines 308, 355). Both hit 404 today → synthesis fallback fires.
  The synthesis produces `concentration: { items: [], other: {...} }` — holdings panel renders empty.
- L3/L4 composition endpoints are deployed and working. Not touched.
- The `ConsolidatedOverviewPanel` holdings block reads `composition.concentration.items` and
  filters by `selectedAssetClass` client-side. For N1/L2 with 1000s of positions, this pattern
  cannot work — pre-aggregation is required.
- `run_gold_layer.sh` sequence: 08b at line 114, then 06b at 115. Script 12 slots after 08b.
- `06b` has `classify_series()` + `ETF_CLASSIFICATIONS` + `ASSET_NAME_TO_TICKER` — script 12
  must inline these (numeric prefix prevents clean imports).
- `cors_response()` hardcodes `max-age=300` — composition routes need `no-store`.

### 3. PRD: ADVI_BKSCMP

File: `docs/architecture/ADVI_BKSCMP_PRD.md`

Four workstreams:
- WS1 (DS + AE): Script `12_build_composition_artifacts.py` — EC2, pandas, reads
  holdings_lots + rel_architect_lookup, writes `gold/views/firm_composition.json` and
  `gold/advisors/{id}/composition.json`. Per-class top-9 + Other + global top-9 structure.
  Slots into run_gold_layer.sh after 08b.
- WS2 (DS): opal-partners-data v2.8 — `cors_response_nocache()`, `serve_s3_json_nocache()`,
  `handle_firm_composition()`, `handle_advisor_composition()`, routing for firm/advisor
  composition entity types.
- WS3 (RD): `types.ts` extends `MixItem` + `BooksCompositionResponse` with optional
  `top_holdings` and `other` fields. `ConsolidatedOverviewPanel` gets a schema-adaptive
  holdings resolver — detects N1/L2 (pre-aggregated) vs L3/L4 (flat list) by checking
  `mix[0].top_holdings` presence. Backward compat guaranteed.
- WS4 (DT + AE): DT deploys partners-api-v1.5.0. AE deploys script 12 + run_gold_layer.sh
  to EC2, runs gold layer, verifies artifacts.

**Schema:** per-class pct relative to class_market_value. Global pct relative to
total_market_value. `scope.advisor_id` presence is the L2 discriminator.

**Cross-agent consistency requirement:** advisor_id sanitization in script 12 must match
`handleSelectAdvisor()` in ClientsTab.tsx:383 exactly.

---

## Decisions Made

| Decision | Rationale |
|---|---|
| pandas not DuckDB for script 12 | DuckDB not confirmed installed on EC2; pandas present everywhere; groupby + nlargest equivalent for this pattern. DuckDB noted as future optimization. |
| Inline classification logic in script 12 | 06b has numeric prefix — can't cleanly import. Inline with comment noting source. Avoids forcing a shared-module refactor as a gate for this PRD. |
| Schema extension (not replacement) | `concentration.items` kept in type for L3/L4 backward compat. New fields `top_holdings` and `other` are optional additions on both `MixItem` and `BooksCompositionResponse`. |
| `cors_response_nocache` new helper | Avoids adding params to `cors_response` which is used widely. Composition routes are the only sensitive ones needing no-store. |
| Script 12 runs before 06b (not after) | 12 only needs 08b output. Running before 06b doesn't affect 06b. Leaves room for future parallelization. |
| RD can work in parallel | Frontend adapter is backward compat — null/404 falls through to synthesis. RD doesn't need to wait for DS or AE. |
| partners-api-v1.5.0 as target tag | Minor bump (new routes, behavior change) from v1.4.0. |

---

## Files Modified

| File | Change | Committed |
|---|---|---|
| `docs/architecture/ADVI_BKSCMP_PRD.md` | Created | No — local |
| `org/projects/ADVI_BKSCMP.json` | Created | No — local |
| `org/projects/REGISTRY.md` | ADVI_BKSCMP row added | No — local |
| `org/projects/ADVI_MVP318.json` | Phase 3 correction | No — local |
| `org/tier1_exec/1.0.0_SA_CTO/prompt.md` | Dashboard updated session 6→7, ADVI_BKSCMP added | No — local |
| `memory/MEMORY.md` | Pipeline tags updated | No — local |

---

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

PRD for ADVI_BKSCMP written and registered. Project JSON and REGISTRY.md updated. All seven
stale documents corrected. Architecture is fully specced: script 12 (pandas, EC2) writes
composition artifacts, two new opal-partners-data routes serve them with no-store headers,
frontend adapter makes ConsolidatedOverviewPanel schema-polymorphic. RD can work independently.

---

### 4. GOLD_LAYER_RESTRUCTURE_PROPOSAL.md — CTO Review

DS submitted a full restructure proposal for the BD pipeline S3 layout.

**Approved with 4 conditions:**
1. BKSCMP paths coordinated — BKSCMP PRD updated to use new GLDRST paths (done this session)
2. `lib/classification.py` → Lambda layer relationship must be specified by DS before task orders
3. AE confirms S3 versioning on `opal-data-bd` before any Phase 1 work
4. CloudFront rewrite rule goes through AE_CloudOps, not DT

Registered as `ADVI_GLDRST`. REGISTRY.md and prompt dashboard updated.

---

## Next Steps

1. **[2.0.0_SA_COO] Receive PRD briefing** and decompose into task orders for DS, RD, DT, AE
2. **[0.4.0_DS_ClientPlatform]** WS1: write `12_build_composition_artifacts.py` + update
   `run_gold_layer.sh`; WS2: update `opal-partners-data/lambda_function.py` v2.8
3. **[0.4.2_RD_AdvisorIntelligence]** WS3: extend `types.ts` + update
   `ConsolidatedOverviewPanel` holdings block in `ClientsTab.tsx`
4. **[0.4.0_DT_ClientPlatform]** WS4: deploy opal-partners-data → `partners-api-v1.5.0`
5. **[0.6.0_AE_PartnerETL]** WS4: upload script 12 + run_gold_layer.sh to EC2, run gold layer,
   verify `gold/views/firm_composition.json` + `gold/advisors/*/composition.json`

**Files to touch next:**
- `docs/architecture/ADVI_BKSCMP_PRD.md` — COO reads as source for decomposition

**Do NOT:**
- Assign script 12 to AE alone — DS writes it, AE deploys it. The algorithm is DS work.
- Change L3/L4 composition endpoints or schema — not in scope
- Run gold layer before DS commits script 12 to CLOUD
