# NEVER-WIDEN PAIR -- IRPT_BCKEND: the 49 Financial split-adjusted holdings price return -- the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~16:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO ruling @9913bf3ed4 (the 2026-04-21 6-for-1 rows are a stock split, non-flow, and the price-only return must be split-adjusted) and the CTO round analysis @57266eeb77 (msg 8435: the split correction ships under its own pair, apart from the exemption).
**Status: DESIGN, nothing applied.** Evidence: the READ `IB211-1_split_adjust_read.json` (IB-pr-572), the served DELTA `IB218-2_split_delta.json` (IB-pr-581, merged @2f69e24932), the builds IB-pr-578 (@07f60f52f3) and IB-pr-583 (@18812065e6) and the release candidate `IB221-1_perf_candidate.json` (IB-pr-585, merged @5bdf4f810a). The packet's sha256 is LEFT for the signer.

## 1. What moves, in two acts

**Act 1: the release.** `irpt-holdings-performance-lambda` (49 Financial's performance function) moves from live CodeSha256 `o9UugRAVhYmF3Q2ULtU6eaaNiLFRAFWW4tjjQPyj2Ok=` to the minimal candidate `fvmE5j1hkNA16csMEtB3/WydmovkAucF/AmBxLCIqEg=` (two builds byte-identical). **2 of 14 members move: `holdings_performance.py` and `sources.json`**, both from pin `de3d423dce` to the base `c5c0646241`; no other member moves. The candidate is built with a candidate source map that re-pins ONLY those two rows of this function. The sibling functions that also stage these members (`irpt-inf-holdings-performance-lambda`, `irpt-cot-holdings-performance-lambda`) are NOT released: the declaration carries `split_adjust` for the 49 Financial entry only, so Inflection and Cottonwood would gain only a manifest block and no served value.

**Act 2: the restatement of the 47 split days.** After Act 1 and its first scheduled run are read, the producer re-runs the 47 dated partitions of the READ (2024-07-09 to 2026-09-03) so the stored returns of the split days are the adjusted ones. This is the act that changes served history: **1,291 of the 266,455 account-days run over those days change** (0.48 percent; 1,293 hold a split security at t-1). Without Act 2 only a FUTURE split day is adjusted.

## 2. The measured effect (counts only, IB-pr-581)

266,455 account-days run; 1,291 changed; 63 security-days adjusted; **13 security-days ratio-absent: not graded, they leave the basket as unpriced** (counted in `excluded_count` and `excluded_value`; row S203); returns at or below -50 percent 3 before and 2 after; no status moves; 2026-04-21: 985 changed (the CTO's ruling states 920; the READ and this run both read 985; row S203, armed, mine); `unkeyed_split_rows` is counted per day since IB-pr-583 and grading is unchanged by it. Cottonwood and Inflection channels change by nothing.

## 3. Blast radius

- **Property moved by Act 1:** the code of Lambda `irpt-holdings-performance-lambda` (object version and `source_code_hash`). **Writers of that property: 1**, `module.irpt_holdings_performance.aws_lambda_function.this` in `infra/aws/terraform/investor-reporting/holdings-performance`, through `safe-apply`. No other writer is admitted.
- **Property moved by Act 2:** the 47 dated gold keys of the 49 Financial `holdings_performance_daily` (one per split day; the key addresses are the builder's `address()` output, read by the applier from the producer's own write path, never typed). **Writers of those keys: 1**, the producer itself (`holdings_performance.py`), run for a stated date. Only the rows of accounts holding a split security at t-1 change within each key (1,291 in all); the applier compares the new key with the prior version row by row and STOPS if any other row differs.
- **Not touched:** the role, layers, environment, schedule, any other function, any Cottonwood or Inflection key, any holdings snapshot, any served page's code.

## 4. Branch A and Branch B

- **Branch A, Act 1:** the candidate map's two rows land in the real map first; the build from the REAL map prints `fvmE5j1h...` or the apply stops; the saved plan reads 1 to change, 0 to add or destroy on the one function and only `s3_object_version` and `source_code_hash`; one safe-apply; re-plan 0; the deployed zip differs from the pre-apply zip in exactly the two members; the health proof reads Invocations and Errors for at least 10 minutes with 0 errors. The first scheduled run after the apply is read: its manifest carries `split_adjust.declared` true and counts.
- **Branch B, Act 1:** the prior S3 version of the artifact key (named by the applier BEFORE any upload, its content sha256 equal to the live CodeSha256) is redeployed by the same Terraform path; the map rows are reverted; CodeSha256 reads `o9UugRAV...` and the re-plan 0. Keys the new code wrote stay and are read by the old code as before (the frame's columns do not change).
- **Branch A, Act 2:** for each of the 47 dates the prior version id of the key is RECORDED, the producer re-runs that date, the key is read back, and the row-level comparison holds (only split-holding accounts change; the changed count per day equals the READ's per-day count). The act is done day by day in ascending order and stops at the first day that disagrees.
- **Branch B, Act 2, per key:** the recorded prior version of each key is restored (the bucket is versioned); a delete of a version is Andrew's act; no other key is touched.

## 5. The manual path

Act 2 runs the producer for a stated date off its own clock. **That manual path is covered by this half for the 47 named dates only, through the producer's existing date parameter.** If the producer has no such parameter, Act 2 is NOT covered and a separate pair is needed (the `--month`-style override class). The applier reads the producer's arguments first and STOPS on a missing one.

## 6. Stop rule and conditions (each blocks the apply order; none blocks this signature)

1. The CTO half. 2. The live CodeSha256 at the apply equals `o9UugRAV...` (another release landed first: STOP). 3. One change at a time on the function (no open ledger or marker naming it). 4. The candidate rebuilt from the real map prints the signed digest. 5. For Act 2: the per-key prior version recorded before each write, the comparison per day, the first disagreement stops the run. 6. The 21 test failures that are identical at the pre-round base are listed, not new. 7. A 429 or Errors above 0 in the health window is Branch B for Act 1.

## 7. Not covered

Cottonwood's and Inflection's split correction (no split key declared for them: their own cells); the 13 ratio-absent security-days' remedy (a ruling on whether to grade them another way); the CTO's 920 versus 985 on 2026-04-21 (to be read with the CTO); a restatement of any date outside the 47; any change to the served pages.

## 8. Signatures

**COO half:** 2.0.0_SA_COO~P2 -- SIGNED for the blast radius of sections 3 and 4, on the conditions of section 6, bound to the sha256 of this file (LEFT for the signer). **CTO half:** 1.0.0_SA_CTO~DELL2 -- UNSIGNED at these bytes. No apply order is cut on this file.

-- 2.0.0_SA_COO~P2
