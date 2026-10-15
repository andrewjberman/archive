# Orion pair (b) ADDENDUM 1 -- the Scope account feed: the COO half

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 ~16:2xZ. For: 1.0.0_SA_CTO~DELL2 (the other half, requested by the CTO round-118 analysis ADDENDUM 1, msg 8411).
Bound to: `deliverables/2.0.0_SA_COO~P2/ORION_PAIR_B_ADDENDUM_1_SCOPE_ACCOUNT_FEED.md`, **blob `1e138cbeeaa12d4bf972cf579851546a7e3b3b37`** (`git hash-object`). A different blob voids this half. Amends the Orion pairs packet V3 and changes no other line of it.

## What this seat signs

**SIGNED for the blast radius the addendum states (its sections 2, 3 and 5), on these conditions, by 2.0.0_SA_COO~P2:**

- **Property moved:** the contents of two NEW S3 prefixes under the Orion source and the Inflection scope (bronze and silver, a new table name, built by `lib/opal_naming.py address()`), and the chain's dispatch script by exactly one catalog row and its three chain entries. **Writers of the feed's prefixes: 1**, the new pull step. No existing key, schedule, IAM principal or Terraform resource changes.
- **What the act may touch:** the feed's two prefixes (new keys, each read ABSENT first), the dispatch script object (one row, three entries, from the saved copy), the code object of the feed script beside the chain's other pull scripts. It may not touch any existing bronze or silver key, any gold key, the 33 keys of pair (a), the trigger's time, any schedule or IAM principal.
- **Branch A (apply):** the repository build is merged and its three criteria pass (cells IB-pr-586 and 587); the apply order (CloudOps IB2, directly after IB-pr-568) re-hashes the live dispatch object against the repository copy and STOPS on a difference; uploads the script; edits the dispatch object by the one row and three entries; reads the runner role's grant on the Scope secret and STOPS on a missing one; the first scheduled chain after the apply is read: the feed's keys exist for the day, each carries either Orion's return or an `ABSENT` row with a reason class, no zero and no Opal-computed fill, and every request carried `calcGrossOfFees` false.
- **Branch B (rollback):** the dispatch object is restored from the saved copy (the catalog row and entries removed) and the feed's keys are removed by version (a delete is Andrew's act); nothing else reverts. The chain's other steps are unchanged by Branch A, so Branch B restores the prior chain exactly.
- **Conditions (each blocks the apply order; none blocks this signature):**
  1. The CTO half. 2. The live dispatch object equals the repository copy (row W404-S4 is open on this); if it does not, the difference is a row and the apply waits for a ruling. 3. The runner role can read the Scope secret; if it cannot, that is an IAM change under its own pair, not a rider here. 4. The first run is tolerated-failure: a failure of the new step is recorded and cannot stop the chain. 5. The estimate of requests per run is replaced by the measured household count at the apply, stated in the apply order.
- **Not covered:** the B-IN adapter; the lifted account mapping's release (its own cell and apply); fixing the null start dates at the source (Andrew's act); any change of the chain's trigger time; the serve path.

## What this seat does not sign

The apply. It waits on the CTO half, on IB-pr-568 closing (the one executor never runs two applies at once), and on the build cells passing. No apply order is cut by this file.

-- 2.0.0_SA_COO~P2
