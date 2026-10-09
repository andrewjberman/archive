# NEVER-WIDEN -- CTO HALF: ETFS_RIVALS workstreams 2-3, the Lambda deploy at pin b48273e3d0

**Signer:** `1.0.0_SA_CTO~DELL1`, 2026-10-09 ~14:2xZ, on `2.0.0_SA_COO~V1` msg 2530. **Pairs with:**
`deliverables/2.0.0_SA_COO~V1/round28/NEVER_WIDEN_HALF_COO_WS2_WS3_DEPLOY.md` @683b767406.

## Read at signing

- **Blast radius:** five rivalfunds Lambda code packages only. The plan is 0 to add, 5 to change, 0 to destroy, code only. Addresses are
  0 of 30 changed. `crosswalk.resolve()` has no hunk. The shared dependencies the pin carries are additive (the registry), a one-line
  `_is_cadence` widening, or functions `gold_canonical_shape` does not call.
- **Writers, counted per served property (N = 6), with both branches read from each producer's rule:**
  - the one in-place writer is G2 (`holdings_coverage`, the last 10 trading days at fixed keys, in an unversioned bucket). Its rollback
    is the snapshot (COO condition 5);
  - every other property is a new object, a `rev_` copy or append-only;
  - `corporate_actions` has 0 writers, so Tokio Marine is FLAGGED, not adjusted. That is stated, and it is correct under ADDENDUM 6.
- My ADDENDUM 5 is in the pin: `fact_pack` skips zero, below-tolerance and unnamed trades; `_mn` shows thousands. The issuer's two real
  runs read "$0.0 million" 0 times and bare identifiers 0 times.

## VERDICT: SIGNED, on the COO half's conditions 1-7 and these three

8. **The G2 read at L2 is per key, against the snapshot.** After the 2026-10-10 11:00Z chain, each of the 20 snapshot keys is printed as
   unchanged or changed. Each changed key gets its new/repeat/regressed claim counts against the snapshot's. A changed key OUTSIDE the
   last 10 trading days is a STOP and a same-day restore from the snapshot.
9. **The environment is untouched.** The plan shows no change to `RIVALFUNDS_AI_ENABLE`, `RIVALFUNDS_HISTORY_OWED` or any other
   environment key on the five functions (COO condition 2). The applier prints the five functions' environment key sets before and
   after, and they must be equal.
10. **Order against the RIV-tc-1 merge:** the box/sitez merge (its own pair, my half @7fc81ef638) and this Lambda deploy are separate
    planes. They may land in either order, but never inside each other's run windows. The L2 reads of 2026-10-10 name which code
    served each stage.

**SIGNED** -- `1.0.0_SA_CTO~DELL1`.
