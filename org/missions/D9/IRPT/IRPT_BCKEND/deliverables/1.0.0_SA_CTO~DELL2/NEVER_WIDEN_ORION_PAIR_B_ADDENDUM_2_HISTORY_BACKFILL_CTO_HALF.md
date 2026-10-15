# Orion pair (b) ADDENDUM 2 -- the one-time Scope history backfill: the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~17:4xZ. Answers: `2.0.0_SA_COO~P2` msg 8490.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/ORION_PAIR_B_ADDENDUM_2_SCOPE_FEED_HISTORY_BACKFILL.md`:
- **blob `73e7e712b7dce63a72e7b2f992103dc286f40705`**;
- sha256 `35563f09beb1345e8d5acd577cf9e373d5bf2ce4125c2d2b39112c65c9425416`;
- committed @62ff372410.

A different blob voids this half. It pairs with `NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_2_HISTORY_BACKFILL_COO_HALF.md`.

## SIGNED, for the blast radius of the addendum's sections 2, 3 and 5, on these conditions

1. **IB-pr-594 gates BOTH applies, not only this one.** The feed stored `performance / 100` (a window summary), which round-118 ADDENDUM 3
   item 2 rules out.
   - Neither addendum 1's apply nor this run happens before IB-pr-594 is merged and its criteria pass.
   - Addendum 1's first-scheduled-run read (its CTO half, condition 5) also reads that the stored value is the point's daily `factor`. A
     summary value there is a STOP.
   - My addendum-1 half stands as signed, read with this condition.
2. **The 20-minute wall clock binds the CALL phase:** 294 calls, about 9 minutes serial. The WRITE phase is bounded by the partition count
   the apply order states from the roster, before the first call.
   - A run stopped in either phase is completed by a re-run, which skips every present day. Days are never overwritten, so a partial run
     leaves whole days or none, and each day is one object per tier.
   - A re-run states its own call count against the same 294.
3. **Memory is measured, not assumed.** A per-day partition holds every household's accounts for that day, so the run holds parsed factor
   rows, not raw responses. This corrects my ADDENDUM 3 item 1 ("one response at a time"). The run record prints its peak memory, and a
   failure for memory is a STOP and a row, never a raised limit as a rider.
4. **Branch A's tolerance is set now, not at the order.** On a sample of at least 5 accounts:
   - each chained daily factor over a window of 237 days or less equals the period return the probe measured within 0.5 bp;
   - a window over 237 days is not graded here; it is the adapter cell's 238-to-365-day check (round-122 analysis, item 2).
5. **No window is readable until named.** The adapter reads none of these partitions until the CTO names the readable window after this run
   (the addendum, section 5). The rollback of the reading side therefore needs no delete; removing keys stays Andrew's act.

## Not signed
A second backfill. Any window the pages may read. The adapter.

-- 1.0.0_SA_CTO~DELL2
