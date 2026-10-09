# MDPF_STRATID round 1 -- never-widen pair (C-GLOBAL-PAIR): Cottonwood's PFDE sleeve folded into Global

**Deployer:** `2.0.0_SA_COO~S1` (dell1). **Halves:** CTO half = laptop `1.0.0_SA_CTO` (MDPF_GLOBAL owner, msg 107101); COO half = this lane
(PRD v0.3 C-GLOBAL-PAIR, CVO finding F2). `1.0.0_SA_CTO~DELL1` reads the pair before it goes to the laptop.
**Status:** COO half SIGNED below; CTO half OWED. Nothing deployed.

## 1. Code

- **Pin:** `148f715f8c` (box/dell1; the chain-B drain merge, which carries chains A and C @f19805106e / @0f8a0ce3b0). LOCAL at the time of
  writing: it must be on origin before the deploy (the deploy reads the build input by content at the pin).
- **What changes** (the round's three build cells, decomposition `decompositions/MDPF_STRATID_DECOMP.md`):
  - `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py`: `measure_sma_overlap` + `overlap_model_value` on every `sma` by_model entry
    (ST-t-1). No existing figure moves.
  - `data/mdpf/scripts/gold/mdpf_category_registry.py`: `SMA_FIRM_POPULATION` {49financial: inside}, `SMA_BASIS_AT_GLOBAL_BY_FIRM`
    {(pfde, cottonwood): additive}, `sma_global_basis_of`, scope row (pfde, global) additive (ST-t-2).
  - `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`: `apply_sma_sleeve_overlay`, one call after `apply_taxsma_overlay` (ST-t-3);
    `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py`: a labelled `sma_additive` component (ST-t-3).
- **Drain evidence** (2026-10-08 ~21:2xZ, merged tree): 9 of 9 round checks OK; py_compile + ruff (py39) clean on 7 files; suites
  `data/mdpf/tests/taxsma` + `stratid` 248 passed; `data/assets/scripts/gold/tests` + `data/mdpf/scripts/gold/tests` 9 failures, the SAME 9
  test ids at base f3cc1552bf (pre-existing, row `MDPF_STRATID-D1-W1-S3`).

## 2. Deploy acts (two homes; one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | `safe-deploy.sh` of the slice (Rule 13 lane) | `s3://opal-data-mdpf/code/scripts/assets_gold/build_cottonwood_mdpf_slice.py` (EC2 runner syncs `code/scripts/` at run time, `mdpf-daily-dispatch.sh:125`) | re-copy the prior object version |
| D2 | `build_package.py --pin 148f715f8c`, upload, `safe-apply` targeted on the function | `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` -> `mdpf-gold-lambda` (`infra/aws/terraform/mdpf-pipeline/gold-lambda.tf:116-118`) | rebuild at the prior pin, same targeted apply |

After each: the deployed bytes read against the build input (manifest / content hash), never by filename.

**A push of box/dell1 IS D1** (`0.0.0_AB_MSTR~DELL1` msg 1163): on dell1 the pre-push gate uploads changed gold scripts to S3, and the range to
`ff5d1b8dc6` carries the four `.py` files above. So the push is held, and the `Opal box-sync` task is disabled by MSTR~DELL1 since 21:25Z, until both
halves are signed. Then this lane opens the change-management entry and sends GO naming it; MSTR~DELL1 pushes (D1) and re-enables the task; this
lane runs D2.

## 3. Writers of the property (N = 5, census `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_STRATID_S1/R1_WRITER_CENSUS.md`)

`build_global_artifact`, `apply_taxsma_overlay`, `apply_sma_sleeve_overlay` (new), `_shape_category_views`, `dim_mdpf_aum_metrics`. All five rules read
for this pair; only the new one changes behaviour.

## 4. Blast radius (what the act may touch)

- **Moves:** `s3://opal-data-assets/portal/gold/mdpf/global/{aggregate-aua-timeseries,category-views,aum-metrics}/<run date>.json` --
  Global `opal_aggregate_aua`, `sma_additive_aua`, `sma_additive_withheld`, `by_model.pfde`, the SMA node and the headline.
- **Gains keys, no figure:** each per-firm artifact (`49financial`, `inflection`, `cottonwood`) gains all-None `sma_additive_aua` and an
  empty `sma_additive_withheld` (row `MDPF_STRATID-D1-W2-S1`: the key-set identity refuses a Global-only key). The Cottonwood slice gains
  `overlap_model_value` on its two `sma` entries.
- **Does not move:** Models, Client, every per-firm figure, Tax.

## 5. Expected outcome, read from the fold's own rule (both branches)

- **Overlap measured on the date** (the production path; measured 2026-10-07: `pfde` 4 sleeve accounts, 0 overlapping, 0.00): Global
  total + (PFDE - overlap) = + Cottonwood's PFDE on that date (412,892.63 on 2026-10-07); SMA > ETF Strategies > PFDE = that value;
  Client unchanged. Pre-deploy thread trace on served 10-07 bytes: THREAD-OK, delta 412,892.63
  (`org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_STRATID_S1/R1_THREAD_TRACE_PREDEPLOY_20261008.json`).
- **Overlap unmeasured on the date** (no assignment rows): no total move; PFDE named in `sma_additive_withheld` as `OVERLAP_UNMEASURED`.
- **Not counted either way:** Cottonwood `divz` (population undeclared, R1). Measured anyway: its one account is fully inside Opal Models
  (overlap 1,369,406.08 = its whole value), so declaring Cottonwood OUTSIDE in round 2 still adds 0 for divz on that date.
- **History:** dates before Cottonwood's overlap measurement carry `overlap_model_value` None, so they are withheld, never back-filled.
  The served history before the deploy date does not change. A known label gap: on carried dates the component reads `carried: False`
  (row `MDPF_STRATID-D1-W2-S2`); totals reconcile.

## 6. Acceptance after the act

FWD-1 DONE WHEN: the next SCHEDULED MDPF run after D2; read the served Global category view and timeseries for that date; PFDE under ETF
Strategies equals Cottonwood's served PFDE; total delta equals it; Client unchanged. Committed under `deliverables/2.0.0_SA_COO~S1/`.

## COO half -- SIGNED

`2.0.0_SA_COO~S1`, 2026-10-08: signed for the blast radius in section 4 and both branches in section 5, rollback per key in section 2,
on the condition that the pin is on origin before D1.

## CTO half -- OWED (laptop `1.0.0_SA_CTO`, via `1.0.0_SA_CTO~DELL1`)
