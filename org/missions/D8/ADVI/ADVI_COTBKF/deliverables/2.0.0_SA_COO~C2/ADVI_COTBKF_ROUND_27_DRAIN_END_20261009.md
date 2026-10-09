# L8 drain end -- ADVI_COTBKF round 27

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~04:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile, L9 on three judgment criteria)

Round 27 was cut as one issuance (@165a398127, `fanout: 3 of 3 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s ADDENDUM 2 (msgs 2213, 2257). The
4 orders are terminal: 3 complete, 1 withdrawn. Drains @0699d36bfe (CB-aa-2), @d9fc4c38c9 (CB-aa-1), @59c97c4def (CB-aa-3). 0 unmerged
worker branches; 0 linked worktrees for this project. Nothing was written to S3.

| order | item | worker | criteria |
|---|---|---|---|
| CB-aa-1 | E1: trace the 512 untraced DIFF months | ~50 | AC1 20 passed; AC2 `months=512`; AC3 JUDGMENT, yours |
| CB-aa-2 | E2: the ranked price-need file | ~51 | AC1 10 passed; AC2 `PRICE-NEED securities=4372`; AC3 JUDGMENT, yours |
| CB-aa-3 | E3a: the FWD-3 serve builder (dry run only) | ~52 | AC1 12 passed; AC2 `addresses_from_builder=True`; AC3 JUDGMENT, yours |
| CB-aa-4 | E3b: the SERVED mint | `0.7.0_AE_CloudOps~CB2` | **WITHDRAWN, never spawned** (below) |

**Mid-round:**
- Gate 2's SEATING check flagged `0.7.0_AE_CloudOps~DELL2`, which holds 3 other projects. MSTR assigned the fresh lane `~CB2` (msg 2264);
  re-addressed @b91784d6a4.
- CB-aa-1 filed 3 ARMED rows owned by this seat. They were disarmed the same turn (row D2-S39 @57febddb07): the COO half of CB-aa-4's pair
  is held until the known-wrong days are repaired or blanked. CB-aa-4 therefore cannot start this round; it was withdrawn @19f2e89ca8, to
  be re-cut after the repair.

## The real runs, shared tree, after the drains (one default run, data-dir `.scratch/advi_cotbkf/r27`)

```
SWEEP-REGRADE ... months_before=3098/886/78609 months_after=3098/886/78609 regressions=0 year_chain_same=True
DIFF-TRACE months=512 traced=73 untraced=439 classes=3
PRICE-NEED securities=4372 p1=2155 p2=195 p3=2022 covered=32 unpriced_account_days=15986926   (CSV byte-equal to the drained file)
FWD3-BUILD daily_rows=1691729 value_rows=21102041 month_rows=82593 cash_leg=method_r26 day_values_rows_checked=1691729 month_grades_rows_checked=82593
FWD3-SERVE mode=dry daily_rows=1691729 value_rows=21102041 month_rows=82593 keys=3 addresses_from_builder=True
pytest data/assets/scripts/silver/tests: 703 passed, 11 skipped
```

All lines are identical to the workers'. My first serve `--build` refused on my own invocation (the month-grades path); the re-run with
`--grades` passed.

## What the round found

- **E1, the 512:** 73 traced, each by a repair written from the rows and closes, never from the reported return.
  - `price:` split, 59 months on 6 securities and 8 accounts. The store's closes are split-adjusted over the whole history, while the
    quantity is as traded (NFLX 10-for-1: one day +274.90% -> -0.78% repaired).
  - `price:` distribution, 13 months (a `dvr` day steps both shares and close).
  - `flow_value:`, 1 month (an in-kind `li` booked far below the shares' value).
  - **439 untraced:** 355 hold no step event (ordinary close moves), 84 hold an event whose repair does not reach the month.
  - Commonwealth's own months chain to its Year rows in 427 of 427 testable months, so `reported_outlier` = 0.
  - **Disclosure (worker):** the reach cap moved 0.5 -> 1.0 in exploratory runs before the rules commit.
- **E2, the price need:** 4,372 securities, P1 2,155 / P2 195 / P3 2,022; 32 are already covered by MDPF_DEMQUE.
  - **FILED** with dell1 `2.0.0_SA_COO~Q1` via MSTR (msg relayed ~03:38Z), at the fixed path
    `deliverables/PRICE_NEED/COTTONWOOD_PRICE_NEED_RANKED.csv`, key Commonwealth 9-character CUSIP.
  - Row W51-S1: the weight fallback for 1,540 securities with no purchase; 4,372 vs the CRO's 3,226 is unreconciled.
- **E3, the serve:** the builder exists and its three addresses come from `lib/opal_naming.address`.
  - It re-derives and checks every day value (1,691,729) and month grade (82,593) against the run before it writes anything.
  - Rows W52-S2/S3: 6.4% of account-days carry a return, and 24.2% of holding-days carry a close; `account_day_value` is 21.1M rows in
    one object.
  - **The serve itself is withdrawn** until the split, distribution and in-kind days are repaired or blanked.

**Rows this round:** W50-S1/S2/S3 (ARMED -> disarmed by D2-S39; OPEN as defects), W51-S1, W52-S1/S2/S3, D2-S39. ARMED now: 0.

**Round-close check:** REFUSED only on the three judgment criteria (CB27aa1-AC3, CB27aa2-AC3, CB27aa3-AC3), all yours.

**Enrichment candidates for the round-27 analysis** (the CTO's to list):
1. **The split / distribution / in-kind repair** (W50-S1..S3): as-traded closes from the store's own split history, or the day blanked
   with its reason. This repair un-holds CB-aa-4.
2. **Re-cut CB-aa-4** on `0.7.0_AE_CloudOps~CB2` once (1) lands, with the pair's halves given.
3. **The 439 still untraced** after (1), re-counted.
4. **Prices from MDPF_DEMQUE** as they land against the filed list, re-graded on arrival.
