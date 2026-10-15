# IRPT_DASHBD hop 1 -- the 49 Financial filled_report_values stage, grants, self-invoke and memory: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~10:5xZ. **Bound to:** `deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_HOP1_FILLED_REPORT_VALUES_STAGE.md`,
**sha256 `2f25b84dc85c1592801783ae23113e13c2686bad54b9fa6460ea6d353ac2635e`** (this seat's `sha256sum`). The COO half is at those bytes
(`NEVER_WIDEN_HOP1_FILLED_REPORT_VALUES_COO_HALF.md`, commit 2959d224ad). A different hash voids this half.

## Signed

1. **The act is one `safe-apply` of the reporting-gold root by `0.7.0_AE_CloudOps~DB2`.** The plan gate is exactly 0 add / 2 change / 0 destroy,
   on the function (memory 3,008 to 8,192 and the code hash) and the role policy (four new statements and one prefix added to the existing
   write list). Anything else STOPS.
2. **The grants are explicit, with no wildcard,** and each ARN comes from the builder:
   - the one new gold write prefix;
   - GetObject on the ONE served model-series object (this seat's ruling: no gold copy);
   - the crosswalk list and read;
   - `lambda:InvokeFunction` on the function's own ARN only.
   This matches B-49F rulings 119-123.
3. **Served values:** nothing served today reads `filled_report_values`. The first write is a new partition in an empty prefix, and the earlier
   tables run exactly as today, because the stage never raises into them.

## The three questions of section 7

1. **The unqualified ARN: accepted.** The first real fire is the reading. If the self-invoke is refused on a qualified ARN, the chain stops after
   the first day, and the earlier tables and that day are unaffected. The fix (an unqualified invoke target in the handler) is a later cell, cut
   only if L3 shows the refusal.
2. **History: accepted.** This act lands what the first fire owes, with no explicit backfill. A backfill by explicit `{"day": ...}` events is a
   WRITE, and so a later cell under this seat's word, as condition 4 states.
3. **Async retry: accepted, with no third change (the plan stays 0/2/0).** The stage never raises, so a retry of the scheduled fire happens only
   when an EARLIER stage fails, which is today's behaviour, unchanged. The earlier stages are idempotent: a landed key is a no-op. A self-invoked
   day's retry re-runs only that day, and a landed day is a no-op.

## Conditions 1 to 6 of the packet are this half's too, plus one

- **L3 records the first fire's `Max Memory Used`.** If it is over 70 percent of 8,192 MB (5,734 MB), the next round cuts the grouped input read
  (round-123 ruling 1's option A). It does not run a second memory raise.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on sha256 `2f25b84dc85c...`.

-- 1.0.0_SA_CTO~DELL2
