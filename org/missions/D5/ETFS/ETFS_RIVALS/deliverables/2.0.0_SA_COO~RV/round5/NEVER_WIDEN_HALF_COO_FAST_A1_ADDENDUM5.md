# NEVER-WIDEN -- COO HALF, ADDENDUM 5: tb-1 handler reads the line-type columns (pin CLOUD c2b9023fc6) -- completes addendum 4

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~09:3xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-5 half (asked; its
condition, msg 28368: the served delta is measured THROUGH the deployed handler's own G1 read, never in-process over cached
inputs). **Extends:** the half @4df699fa92 and addenda 1-4. Every gate, key and condition stands.

**Why:** the addendum-4 post-act read (ledger `etfs-rivalfunds-fast-a1-r5`, held OPEN, leg E4 unproven) found the served
trend still carrying SCHY's index futures (1 index line, "Unclassified" -$1.046B lean) while the contribution and
`missing_reason` fields matched. Cause: `gold_buying_trend.handler_entry` read G1 without `provider_security_type` /
`position_type` / `asset_class`, so `_cash_keys` could not see a future in the Lambda; my addendum-4 delta was measured
in-process over cached G1 carrying those columns. Fix at CLOUD **c2b9023fc6** (commit f23c459ead): the handler reads the
four line-type columns; a test drives the handler path with a future and asserts it leaves the trend.

## VERDICT: SIGNED (at pin CLOUD c2b9023fc6)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** from `/c/tmp/rv-apply` at c2b9023fc6: the five Lambdas' `source_code_hash` +
`last_modified` only; no policy change. Package diff vs the deployed 3107eae49f: `gold_buying_trend.py` only (+4 lines).

## THE SERVED DELTA, MEASURED THROUGH THE HANDLER'S OWN READ

`gold_buying_trend.handler_entry({"date": "2026-10-01"})` run on an overlay sink (S3 reads, local writes) at the fix's
code, vs the served `buying_trend-20261002T092925Z-622f5765f524`:

| measure | served | new (handler path) |
|---|---|---|
| index lines in the trend | 1 | **0** |
| SCHY sector leaned away, rank 1 | Unclassified -$1,046,210,071 | **Energy -$27,194,033** |
| SCHY sector leaned away, rank 2 | Energy -$27,194,033 | Materials -$22,319,482 |
| trend rows changed | -- | **14 of 320, all SCHY** |

`holding_contribution`, `input_census`, the AI rows and every other fund's trend are unchanged.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| F1 | the five stage Lambdas' code | 3107eae49f (daily ITkxSe7y.., fetch 9o6C1Ggs.., canonical 8hOwhsij.., silver 1e/I++On.., publish zADQgpBF..) | in place to c2b9023fc6 | re-apply from a tree at 3107eae49f |
| F2 | gold `buying_trend` date=2026-10-01 | the 09:29Z object | ONE new content-sha object via `refresh_a1` (holding_contribution / input_census rebuilt to equal content write nothing) | prior objects stay |
| F3 | platinum page 2026-10-01 | batch fast-a1-publish-1001e | republished ONCE, batch fast-a1-publish-1001f | prior page kept under `revisions/<ts>/` |
| F4 | the 2026-10-02 scheduled runs and page | would run 3107eae49f | run c2b9023fc6 | F1's rollback |

## ACT-START GATES

1. Plan exactly 0/5/0. 2. Live base equals F1's CodeSha256. 3. NEVER-2 entry `etfs-rivalfunds-fast-a1-r6` opened AND
committed before the apply (`&&`). 4. Nothing in flight; window to 10:45Z, else after the 09:00 ET sweep.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 10:45Z:** the served trend reads 0 index lines and SCHY's rank-1 lean away is Energy; the post-act read
  prints both from the SERVED object. That read also proves r5's E4, and r5 then closes citing it.
- **Not applied by 10:45Z:** the 10-02 chain runs 3107eae49f (futures in SCHY's trend, as served now); the act follows the
  sweep and F3 also republishes 2026-10-02. Covered with the same keys and rollbacks.
