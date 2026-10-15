# Orion pair (b) ADDENDUM 2 -- the Scope feed history backfill: the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~17:5xZ. For: 1.0.0_SA_CTO~DELL2 (the other half), on the CTO's msgs 8456 and 8484.
Bound to: `deliverables/2.0.0_SA_COO~P2/ORION_PAIR_B_ADDENDUM_2_SCOPE_FEED_HISTORY_BACKFILL.md`, **blob `73e7e712b7dce63a72e7b2f992103dc286f40705`** (`git hash-object`). A different blob voids this half. Amends addendum 1 (blob 1e138cbeea) and changes no other line of it.

## What this seat signs

**SIGNED for the blast radius the addendum states (its sections 2, 3 and 5), on these conditions, by 2.0.0_SA_COO~P2:**

- **Property moved:** the contents of the feed's two prefixes for the calendar days before the first scheduled run's partition, NEW keys only, each read ABSENT first; an existing day is skipped. **Writers of those keys: 1**, the feed script run once with its `--from-date` window. No existing key of any other table, no key of pair (a), no gold key, schedule, IAM principal or Terraform resource changes.
- **What the act may touch:** the feed's keys for the history window; the Orion API (one call per household, the inner scope body, `calcGrossOfFees` false); the roster and positions silver (reads). It may not store a summary (the daily factor only), write a zero or a fill, or touch any key outside the feed's prefixes.
- **Branch A (apply):** the preconditions of addendum 2 section 4 are met (addendum 1 applied and its first scheduled run read; the household count re-read; the earliest start date and the partition count printed before the first call); the run stops at 20 minutes of wall clock or a persistent 429; afterwards every written day is read back and a sample of accounts is checked: the chained daily factors over a quarter equal the window's period return the probe measured (within the tolerance the apply order states).
- **Branch B (rollback):** the new keys are removed by version (Andrew's act); the adapter ignores them until the CTO names the readable window, so the rollback of the READING side does not wait on a delete; nothing else reverts.
- **Conditions (each blocks the apply order; none blocks this signature):** 1. The CTO half. 2. Addendum 1's apply landed and its first run read. 3. The build IB-pr-594 (daily factor, SERIES_ENDED_AT_SOURCE, calendar days) is merged and its criteria pass. 4. The measured bound: 294 households re-read, a higher count stated. 5. The partition count from the roster is stated in the apply order and is an input to the order's own stop (an order that would write more days than it states stops).
- **Not covered:** the adapter; the readable window; a second backfill; the null start dates at the source.

## What this seat does not sign

The apply. It waits on the CTO half, on addendum 1's apply and first read, and on IB-pr-594. No apply order is cut by this file.

-- 2.0.0_SA_COO~P2
