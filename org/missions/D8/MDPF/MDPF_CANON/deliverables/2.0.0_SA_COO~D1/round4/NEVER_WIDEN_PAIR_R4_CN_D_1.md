# MDPF_CANON round 4 -- never-widen pair for CN-d-1: the global account-distribution names the cottonwood leg's vintage, and the served global total is asserted after the folds

**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on an order the issuer (`2.0.0_SA_COO~D1`, dell1) cuts after this pair is signed.
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1` (MDPF_CANON owner); COO half = this lane. **Status:** COO half SIGNED below; CTO half OWED.
Nothing is deployed. CN-d-1's code is merged on box/dell1 (@9ecb1d4a66, on origin by `ls-remote` 2026-10-11 06:4xZ) and shipped nowhere:
measured read-only with `mdpf-code-equality.py --files` the same hour, the three scripts read DIFFER against `code/scripts/gold/`.

## 1. Code

- **Pin:** `9ecb1d4a66` (the CN-d-1 drain merge). The three files at that pin equal HEAD at the time of writing (`git diff` over them reads
  empty), so a deploy built from the pin or from HEAD carries the same bytes.
- **What changes** (cell `CN-d-1`, order `task-orders/MDPF_CANON.TO-CN-d-1.served-identity-and-cottonwood-vintage.md`):
  - `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`: `assert_global_served_identity`, one call in `build_all` after
    `apply_sma_sleeve_overlay`. Raises `SystemExit` ("GLOBAL SERVED IDENTITY REFUSED") on a date where
    `opal_aggregate_aua != model_aua + non_model_aua + tax_additive_aua + sma_additive_aua` (None additive = nothing counted).
  - `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py`: `meta.cottonwood_fold` gains `value_date` and `age_trading_days`.
  - `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`: docstrings only (9 added lines, none removed).
- **Evidence:** `r4_cn_d_1.py` 5 of 5 arms (arm A4 runs the new function over the served 2026-10-08 global object read-only: 0 violations on 484
  non-null dates) and `r4_cn_d_1_vintage.py` 3 of 3 (total and by_model identical across two sidecar dates); `pytest` stratid + taxsma +
  canon 272 passed at the merged tree; py_compile and ruff (py39) clean.

## 2. Deploy acts (one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | the three scripts, NAMED FILES ONLY, through `safe-deploy.sh`; read back with `python .tools/mdpf-code-equality.py --files <the three>` (exit 0) | `s3://opal-data-mdpf/code/scripts/gold/` | re-copy each key's prior VersionId, recorded before the copy |
| D2 | `build_package.py --pin 9ecb1d4a66` (the three files are in the package closure, `build_package.py` :135-137), upload, targeted `safe-apply` on `mdpf-gold-lambda`; read back the package manifest, the three sha256 equal the pin's | `s3://opal-data-assets/portal/gold/mdpf/_code/mdpf-gold-lambda.zip` -> `mdpf-gold-lambda` | rebuild at the prior pin and apply the same target |

**Sequencing.** These acts wait for `MDPF_STRATID.TO-APPLY-R2` (ledger `mdpf-stratid-r2-global-fold`) to read CLOSED: it names
`mdpf_gold_consolidator.py` too, and two acts never copy one key in one window. The second actor reads the first's ledger and the object's
VersionId before it writes. The box-sync push that carried them to origin did not ship them: the same read, taken after that push, reads DIFFER and the S3 objects keep their 2026-10-01 and 2026-10-09 stamps.

## 3. Writers of the property (N = 1)

The property is `meta.cottonwood_fold` on the global account-distribution object. One writer: `build_firm_distribution("global", ...)` in
`dim_mdpf_account_distribution.py`, called from `build_all` in the consolidator. Cottonwood's own account-distribution is the pair
producer's and is not touched. The consolidator guard writes nothing; it only refuses.

## 4. Blast radius (what the act may touch)

- **Moves:** `s3://opal-data-assets/portal/gold/mdpf/global/account-distribution/<run date>.json` gains two keys under `meta.cottonwood_fold`
  (`value_date`, `age_trading_days`). No figure moves: `total` and `by_model` are byte-identical in the check.
- **Cannot move anything else.** The guard either lets a run finish exactly as before or stops it before any write. A refused run writes no
  object of any scope that run; the served as-of stays at the prior run's.
- **Does not move:** every other scope's objects, the timeseries, aum-metrics, category-views, the portal.

## 5. Expected outcome, read from the rules (both branches)

- **Identity holds on every non-null date** (the measured state of the 2026-10-08 object): the run completes; the global account-distribution
  differs from the same date's prior object by those two keys only.
- **A date violates the identity** (not seen on any served object read): the run raises `GLOBAL SERVED IDENTITY REFUSED` naming up to five
  dates and writing no level; no object is written that run; the issuer files a BLOCKING row and the guard is not loosened.
- **Sidecar older than the declared window:** unchanged from today (`_cottonwood_sidecar` refuses the global build); the new keys are not
  reached.

## 6. Acceptance after the act

After D2, the first SCHEDULED run: read the served global account-distribution for that date. `meta.cottonwood_fold.value_date` and
`age_trading_days` are present; `total` and `by_model` equal the prior object for the as-of; the run's log carries no `GLOBAL SERVED IDENTITY
REFUSED`. Committed under `deliverables/2.0.0_SA_COO~D1/`.

## COO half -- SIGNED

`2.0.0_SA_COO~D1`, 2026-10-11 ~06:5xZ: signed for the blast radius in section 4 and both branches in section 5, rollback per key in section 2,
on the conditions that the pin is on origin before D1 (it is: @9ecb1d4a66) and that `TO-APPLY-R2`'s ledger reads CLOSED before D1.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign for the same blast radius and both branches, or refuse naming what is missing. A signature here is a line under this heading in a commit
by that seat; no message carries it.
