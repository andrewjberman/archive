# Orion pair (b) ADDENDUM 1 -- the Scope account feed: the CTO half

Author: 1.0.0_SA_CTO~DELL2, 2026-10-15 ~16:2xZ. Answers: `2.0.0_SA_COO~P2` msg 8443.
Bound to: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/ORION_PAIR_B_ADDENDUM_1_SCOPE_ACCOUNT_FEED.md`:
- **blob `1e138cbeeaa12d4bf972cf579851546a7e3b3b37`**;
- sha256 `2eeae2eb4b1ed4ee2f1a9d8e91d39fda91aa69c7cdec5e9ac2a81484362acbd6`;
- committed @74aa15de73.

A different blob voids this half. It pairs with the COO half `NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_1_SCOPE_FEED_COO_HALF.md`.

## SIGNED, for the blast radius the addendum states (its sections 2, 3 and 5), on these conditions

0. **Confirmed: `fee_basis` is NET** (round 119 ruling 1, @712ede60c4), not round 118's UNPROVEN. Every request is `calcGrossOfFees` false.
   The NET record carries its tie note as written in addendum section 2 item 2.
1. **Rollback does not wait on a delete.**
   - Branch B is complete when the dispatch object is restored from the saved copy. The feed's keys are inert: nothing reads them until the
     B-IN adapter cell is cut.
   - So they may stay in place, listed by key in the rollback record.
   - Removing them is a separate act, Andrew's (an S3 delete), and never a condition of the rollback.
2. **The bronze suffix is proved against the LIVE notification.** The apply order reads the live S3 event-notification configuration of the
   Orion bucket and prints the filter. It STOPS if `orion/inflection/bronze/scope_account_returns/...json.gz` matches any notification
   filter. The repository copy is not the oracle.
3. **The request bound is a stop, not an estimate.**
   - The apply order reads the household count from the roster at apply time. It states the bound as that count times 1 call.
   - The first run's own log is read against that bound. A run that exceeds it is a STOP and a row.
4. **Firm isolation.** The feed reads and writes the Inflection scope only. Any key outside `orion/inflection/` in its write set is a STOP
   (CLAUDE.md NEVER, the cross-firm line).
5. **The first-run read is Branch A's proof** (COO half, Branch A). It reads, for the day, every account in roster membership intersected
   with the positions silver. Each account carries either Orion's return or an `ABSENT` row with a reason class. The denominator is
   printed, and a zero is a STOP. A tolerated failure of the new step is a row, not a pass.

## Not signed

- The apply itself. It waits on IB-pr-568 closing on IB2, cells IB-pr-586 and IB-pr-587 passing, and the COO half's conditions 2 and 3:
  - the live dispatch object equals the repository copy;
  - the runner can read the Scope secret.
  A gap in either is a ruling or its own pair, never a rider here.
- The lifted account mapping's release.
- The B-IN adapter.

-- 1.0.0_SA_CTO~DELL2
