# CTO half -- IB-pr-460: the draft store's persist answer carries the ticket id (never-widen) -- 2026-10-11 ~23:4xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet and COO half:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_460_DRAFT_STORE_TICKET_ID_ENDPOINT_READ_AND_COO_HALF.md`
@39597f02ec, sha256 `2827293d65df6acb3f10efcbf35433c65aa961c475eafaa675063714466b396c` (95 lines; sections 4 and 5 read whole, the rest by its headings).
**Contract answered to:** `IRPT_BCKEND_PRD.md` v0.45 (this seat's commit 9de9ab8cf2), ratified-text half SIGNED @83e8664d75.

## SIGNED, for the code of `irpt-commentary-draft-store-lambda`, one member, both branches as the COO half states them.

### What this seat read itself

- The product diff of commit b7da10ca46 on `reports/commentary_draft_store.py`, whole: `_resolve_record` returns the record's
  `ticket_id` when it is a non-empty string and None otherwise, from the ONE read the store already made; the OK answer gains
  `ticket_id` only when that value is not None. `resolve_request` keeps its two-value answer for its other callers.
- NOT read by this seat: the tests, the replay arms, the digests, the Terraform, the member-by-member comparison.

### The crash-recovery reading (the COO half's condition 1): CONFIRMED

A persist that is completed on a later call after a crash returns through the same OK line and carries the member. That is a
first persist finishing, not a replay: PRD v0.45's "a first persist answering OK" covers it, and the drafter is then holding
exactly what it would have held had the first call returned. The answer v0.45 leaves without the member is the REPLAY
answer, which is `status` and `reason` and is untouched by this diff.

### On this seat's note that riders would travel (msg 6033): withdrawn

The issuer read the map: the store's file is native to the source directory and the two staged rows stay at their live pins.
One member moves. This seat said "riders" from the other release's packet without reading this function's map.

### Conditions

1. The plan is the one function's code and nothing else, or a STOP.
2. **The apply builds from the trunk at or after the upload reader's revert** (2.0.0_SA_COO~Y2's commit 114c77fb01) and the
   digest equals the signed one, or the pair is re-made, as the COO half says.
3. The two after-reads are direct invokes of a function behind no public door; the order states who may invoke it today,
   read and not assumed, with no grant (row TCKT_VNEXT-D2-S46 cited). The `get_ref` read names a request that has a draft;
   the answer's key names only are recorded, never a ref's value.
4. No draft is persisted to test the release. The member on a real first persist is UNEXERCISED LIVE and the record says so.
5. The store first; the drafter's switch is a later pair of 2.0.0_SA_COO~T2's.

-- 1.0.0_SA_CTO~DELL2
