# L8 drain end -- IRPT_BCKEND rounds 88-90, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~23:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD by path
floor; round 88 is a packet only, and rounds 89-90 are apply orders issued to `0.7.0_AE_CloudOps~DELL2` and still open |
**Judgment criteria:** 0

## Round 88 -- IB-pr-376, slot ~184 (complete; drained @acae8acb73): the release packet for IB-pr-375

- **Pin P 49bc13131d.** `custody_write.py`'s staged row is repinned d34a46f37d -> 6a0226dc02 (IB-pr-375), because a HEAD build does not
  carry a staged row's change. `custody_persist.py` ships from the source dir.
- **Census:** 2 members, owned. BUILD_ONLY from a clean tree, rc 0, built `7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns=`. The replay is
  identical; custody tests: 54.
- **Graded by the issuer:** IB88-1-AC1 PASS, IB88-1-AC2 PASS.
- **Halves:** COO @66c617a5c7, CTO @b97fa248b2. The CTO ruled the sequencing: this function first, the route only after live reads
  7T29wPhz.

## Round 89 -- IB-pr-377 (OPEN, applier 0.7.0_AE_CloudOps~DELL2; ledger opened @6519c4989e): the r61 directory release

- The release was signed 2026-10-07. It was blocked because dell2 had no terraform (row S364); row D2-S11 cleared that.
- Live still equals the packet's "before" on both functions, so it is unapplied (re-read ~23:1xZ).
- The census at 4710b8007b equals the signed lists. `entry.py` differs from the packet pin only by IB-pr-341's P1 fix.
- The directory root's "NOT INITIALISED" header is stale: the state object exists, 2026-10-06.

## Round 90 -- IB-pr-378 (OPEN, applier 0.7.0_AE_CloudOps~DELL2): IB-pr-376's function, then the Performance client statement route

- **The IAM leg is applied** (2026-10-08T22:47:14Z, laptop CloudOps, CloudTrail 717f3ed8, 11/11 simulations; pair @77440a907b; CTO half
  @5f65b4f40e).
- The route follows Part A's live read. The real persist and the owner/other-firm reads follow IRPT_CUSTDY E2a.

## Open finding (not a block)

- `to-decomp-ref-lint` (gate2, ANNOUNCE) flags SEATING on IB-pr-377/378. `0.7.0_AE_CloudOps~DELL2` also holds TCKT_VNEXT.TO-APPLY-F10,
  which breaks rule 27's one project per Tier-2 seat. Andrew-direct msg 1756 routes all dell2 applies to that seat.
- MSTR~DELL2 has put this to Andrew (msg 1869). The hand-offs stand.

## Also this hour (records, no cell)

- **IAM-leg pair** for row D2-W181-S1, written by the issuer (@77440a907b). It grants PutItem only: the code never calls UpdateItem.
- **H1 (C-TRIGGER) READY-event contract v1** (~T2 @98ca40fd4c) AGREED. The producer facts are @6061d0e274. H1 is cut once
  `outlook-global-commentary-draft-lambda` exists.

**Push state:** LOCAL on box/dell2 (MSTR pushes :18/:48).
