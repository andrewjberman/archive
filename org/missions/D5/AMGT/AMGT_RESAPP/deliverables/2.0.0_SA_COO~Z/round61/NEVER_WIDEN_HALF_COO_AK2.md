# AMGT_RESAPP round 61 -- `AMGT-ak-2` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~07:2xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names: the round-61 issuance tip, or a descendant whose
CONTENT-DIFF equals the list below. Build + upload ONE artifact; ONE code-only `safe-apply`. Executor `0.7.0_AE_CloudOps~A`; order
`task-orders/AMGT_RESAPP.TO-AMGT-ak-2.the-company-name-redeploy.md`; decomposition s.69. DSGN round-21 analysis section 3B cell B1
(@e14de1769c), before the 07:13 ET generation if it can.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `UnSqZgCDkSxM3J3roY8d+iVGZp+8JB1XnM/phfZrmeo=` |
| function LastModified | `2026-10-01T13:59:33.000+0000` (aj-2) |
| artifact S3 VersionId | `1DFcRU3xDzUsi84yZnWv985DDF1MymMn` (LastModified 2026-10-01T13:54:17Z, 41,116,975 B) |

## WRITERS OF THE PROPERTY: 2 seats, 1 path

`build-and-upload-scoped-amgt.sh` + a code-only `safe-apply`; AMGT_RESAPP (this act) and AMGT_HARVST (no redeploy of this function in
flight at signing).

## THE FILE LIST (`--build-only` at the issuance tree, rc=0: VERIFY missing [], isolated runtime 3 of 3 arms)

`CONTENT-DIFF SUMMARY: files 350, IDENTICAL 347, CHANGED 3, ADDED 0, REMOVED 0` against `UnSqZgCD...`:

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | ak-1 | a ranked row the classifications table and the crosswalk leave unnamed takes its model block's header `NAME` (`name_source` `model_block_header`); `/security/{key}/overlay` takes the same step before its ticker fallback. A row already named keeps its name and source. No figure, rank, key or identity block changes. |
| `lib/research/api/monthly_chatter.py` | CHANGED | ak-1 | the chatter set's `display_name` takes the same step before the ticker fallback (`name_source` `model_block_header`) |
| `org/standards/NAMING_SCHEMA.json` | CHANGED | rider `aa2b5a42ff` (`4.0.0_SA_CRO`) | `cadence.values` gains `1min`; no served route reads it |

Any other changed file at build time is a STOP.

## READERS

The price rankings (TRENDING/PRICE, BREAKOUT/PRICE), the chatter set and the per-name overlay, on DEV and PROD. No other route changes.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId above |
| code-only `safe-apply` | the function's code (source hash) only | a code-only `safe-apply` with `1DFcRU3xDzUsi84yZnWv985DDF1MymMn`, restoring `UnSqZgCD...` |

## EXPECTED OUTCOME -- both branches, read from the code's own rule

- **The model-block reads succeed (expected):** 0 of 94 rows unnamed on both price rankings (24 gain `model_block_header` names; 35
  etf-classifications and 35 crosswalk unchanged); 0 of 95 chatter rows by ticker; the RMS overlay equals its row. Measured locally on
  the issuance tree against the live stores: exactly this.
- **A model-block read fails or is absent at serve time:** that row keeps today's ticker label (`_model_block_name` answers None; nothing
  is guessed). b1_names C1 or C3 then FAILS for that row, which is the rollback trigger. The round-60 overlay-equals-row property holds
  in both branches, because the ranking and the overlay take the same step on the same read (AC2).
- **Latency:** at most 24 extra reads per ranking call, 8 in parallel. Deployed base 7.6 s against a 29 s timeout; locally the ak-1
  tree is no slower than the base tree (15.4 s vs 17.5 s).
- **AC1 or AC2 fails after the act -> ROLLBACK** per the table.

## WHAT THIS HALF DOES NOT COVER

No producer change, no store write, no S3 delete, no vendor call, no registration. No IAM, route or gateway change: any of these in the
plan is a STOP.
