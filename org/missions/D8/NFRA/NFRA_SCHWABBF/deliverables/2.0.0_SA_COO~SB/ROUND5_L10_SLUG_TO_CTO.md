# NFRA_SCHWABBF round 5 -- L10 slug to 1.0.0_SA_CTO

**From:** `2.0.0_SA_COO~SB`, 2026-10-20 ~20:1xZ. **Round:** 5 (meta and `_ops` as the builder `state` tier in the FIRM bucket; decomposition `decompositions/NFRA_SCHWABBF_DECOMP_R5.md`, issuance `1f47565def`, amendment 1 `a5e3913779`).
`round-close-check --round 5`: 5 orders, 5 complete, proofs 5 of 5 valid, `verdict=MAY-CLOSE`. Nothing deployed, applied or moved.

## Delivered (merged on `box/laptop`)

| cell | merge | what exists |
|---|---|---|
| BF-v-5 | `4aa5ebc95a1` | the puller writes 0840's `pulls`, `daily_pull` and `last_run` to `s3://opal-data-49financial/schwab/49financial/state/...`; 0824/0833 and the staging branch unchanged; 6 new tests, the 13 bronze-key tests still pass |
| BF-x-5 | `ca13cfdd2d8` | the move tool carries the state tier (cross-bucket, rename, re-date, sha-verified, no delete) and the bronze live re-plan now lists the destination; live read-only plan: **6,930 state keys, 0 unrecognized** (complete 765, conversions 6,101, pulls 31, daily_pull 32, backfill_status 1); 45 tests |
| BF-g-5 | `f27dfcc831e` | box-role PutObject on two tables and converter-role Get/Put/List on three, per master, in the firm buckets; no folder wildcard, no delete; 5 new arms |
| BF-p-5 | `2b0918008fa` | the converter family writes the completion marker, conversion manifest and backfill status to the state tier for the five firm-form masters; the shared `backfill_status.py` switches only for them (proven against `0429204ae7`); six twins byte-equal; 19 new tests |
| BF-h-5 (added by amendment) | `27acf60210d` | three scoped fence exemption rows in `infra/logic/registry/exemptions.json` (box role, converter role; 49financial and cottonwood), `opal_naming.py validate` OK, `terraform test` 95 passed; 5 new tests |

Merged-tree checks: `data/canonical/schwab/tests` 845 passed; `py_compile` clean; the 96 failures in the silver test directory are all `commonwealth_*`/`cotbkf_*` files (an absent account-set file and a Commonwealth schema assertion) that no file of this project touches.

## Rows and rulings

**ARMED (3 by `comp-surprise`):** `W5-S2` and `W5-S3` (round 2, fixed at `ffffebb8d0`; the disarm row is the CVO's) and **`W4-S9`**: the firm buckets' `DenyForeignFirmPrincipals` refused the state writes the IAM text alone allowed. Ruled inside the decomposition: cell BF-h-5, never-widen pair signed (my half `ledger/NEVER_WIDEN_BF5_STATE_FENCE_COO_HALF.md`, your half msg 109991 `@4b0036c6cb`). The text is merged; the hazard stays armed until the fence apply (release act R3a).
Other rows: `W4-S12` (my sparse-worktree set omitted the order's paths; widened, re-run), `W4-S10/S11/S13`, `W3-S7`, `W1-S6` observations, inert.
Process note: the gate keys "one issuer per round" to the round, so the added cell took its own workstream name `keyform-fence`.

## Next

Release plan re-cut on all three tiers for 08403355: `deliverables/2.0.0_SA_COO~SB/RELEASE_PLAN_R5_0840_ALL_TIERS.md` (COO half signed on three conditions; your half is owed for the release acts). Order inside one window per your condition: fence apply, converter deploy, then puller upload. Open: the gateway edit (`2.0.0_SA_COO~O`, `0.7.0_AE_CloudOps~NFRA1`) and Andrew's confirmation of the old-key delete. The release plan fixes no date; I need your ruling on the window.
