# DRAFT -- NOT APPENDED, AND BLOCKED. Companion to `DECOMP_V6_DRAFT.md`: the v6 table row for cell `CN-g-1` if the CTO rules it cuttable.

## Row (same columns as DECOMP_V6_DRAFT.md)

| cell | serves (cell_refs) | candidate | owned files | depends on | actor |
|---|---|---|---|---|---|
| `CN-g-1` the non-model-assets builder reads the gold-tier aggregates: `load_global_aggregate` and `load_inflection_nm` default to the newest `aggregate_aua_timeseries` partitions at the builder's address (global: `date`, `base_excluding_tax_aua`, `model_aua`; inflection: `non_model_aua`); the staging WRITE and the frozen pre-cutover READ stay (SERVED on deployment: the file runs in the dispatch chain at stage 6c) | FWD-5 | M4 / non-model assets | `data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py`, `data/mdpf/tests/canon/test_non_model_assets_gold_tier.py` (new), `deliverables/0.9.0_WK_MDPF_CANON~4/READER_CENSUS.md` (two rows) | -- (no data edge; a deploy-order edge: its `code/` sync follows `build_portal_gold_accrual.py`'s, which DIFFERS on the runner) | ~17 (worker-light) |

**Fan-out:** 2 of 2 chains with `CN-f-1`, cap 8. Disjoint write sets (`CN-f-1` owns the consolidator, the distribution and aum-metrics builders and the
crosswalk; `CN-g-1` owns one builder and the census). Touches none of the six R2 files.

**Checks (drafts at `round6/draft/checks/`; at base, HEAD of box/dell1):** `r6_cn_g_1.py reader` 1 of 5 (DERIVE-UNCHANGED is a control),
`seam` 2 of 3 (the two controls pass; SEAM-DELTA0 fails: the base cannot read the gold tier), `r6_cn_g_1_census.py` 1 of 4 (C4 control). A scratch
reference copy (never in a product path) reads 5 of 5, 3 of 3 and 4 of 4. A planted wrong column (`opal_aggregate_aua` for
`base_excluding_tax_aua`) turns reader and seam red (25 unequal rows of 497).

## BLOCKER carried with the row (the cell is NOT cuttable as specified)

Stage 6c runs inside the daily dispatch, before the gold lambda's 13:30Z fire; the gold-tier partition for as-of D is written by that fire
(`date=2026-10-09` LastModified 2026-10-12T13:31Z, after the 12:54:22Z dispatch). A repoint therefore reads the previous fire's partition at the
moment it runs: one trading day behind the staged aggregate it reads today. See `TO-CN-g-1.DRAFT.md` record face. Put to the CTO as options
(a) leave stage 6 on the staged aggregate until the dispatch chain retires, (b) move the non-model build into the gold lambda after the parquet
emit, (c) accept the lag. REC (a).

## Not in this cell

- `dim_mdpf_aum_metrics.py` and `build_mdpf_spine.py`: both run in the same dispatch stage ahead of the fire (the same ordering fact) and feed the
  staged trio the verifier and the accrual bridge read; a chain, not one reader.
- `build_portal_gold_accrual.py`: DIFFERS on the runner (executed by the accrual SSM fire); its own `code/` sync comes first.
- `opal-assets-mdpf-portal-publisher/lambda_function.py` (M5): switched last (PRD :367; FWD-4 text).
- `verify_mdpf_revamp_conditions.py`: stays on staging until M12 (CTO ruling); four of its cells are not wide-parquet columns.
