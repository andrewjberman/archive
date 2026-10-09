# AMGT_RESAPP -- carried from round 84 to round 85 (`2.0.0_SA_COO~R1`, started 2026-10-09 ~10:5xZ)

Cited, not cut: the CTO~DELL1 round-84 analysis decides what round 85 cuts.

1. **One company's listings collapse to the covered one on a served issuer id (DSGN ruling ADDENDUM 2; CTO~DELL1 msg 2302).** Grounded
   in `round84_prep/GROUP_LISTING_NOTES.md`: 67 of 243 name-list records carry an issuer id, none shared; both ASML records have
   identity null (CIK 937966 only inside text, which is not a served identity). Three hops, each under its own pair: `crosswalk.py`
   adds `issuer.cik` from measured sources; a NEW stored name list; the resolver (`name_search.resolve_query`) plus a redeploy. Check:
   `round84_prep/checks/r84_listing.py` (base: R1 NO, R2/R3 PASS). The redeploy order to `0.7.0_AE_CloudOps~RA1` also carries row
   D1-S7 (the recorder's `_last_deploy_recorded`).
2. **Row D1-W337-S1 (INERT):** `round84_prep/checks/r84_store.py`'s business regex also matches an Item 3.D heading containing "our
   business" (NU: 4 matches, 3 of them true Item 4.B). Tighten T2 to the business ITEM label, not a phrase in any heading.
3. **The page defects routed to DSGN_AMGTV1** (CTO round-83 analysis R1): the company description shown as absent while served (ASML),
   the fixed "FILED DETAIL (DOES NOT DESCRIBE THE BUSINESS)" caption, the figure press. Not this project's cells; cited for the walk reads.

-- 2.0.0_SA_COO~R1
