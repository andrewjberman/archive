# L8 drain end -- IRPT_BCKEND rounds 90-92, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~00:2xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0

## Round 90 -- IB-pr-378 (COMPLETE, applier 0.7.0_AE_CloudOps~DELL2, proof @3e470562c6): the Performance client statement function, then its route

- **Part A:** irpt-export-render live == built `7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns=`. Re-plan clean, census 0. The replay ran
  before the ledger (@b9fccdccaa): identical through both zips, and the negative control was refused by both.
- **Part B:** planned only after Part A's live read. Route `POST /api/scoped/investor-reporting/custody-report` is live as RouteId
  jtwlf6l under the CUSTOM authorizer naqxlm; re-plan 0. The ledger is CLOSED 4 of 4.
- **Graded by the issuer** at box/dell2 HEAD: IB90-1-AC1 PASS, IB90-1-AC2 PASS. `round-close-check --round 90`: MAY-CLOSE.
- **Row D2-S14** (an unpaginated route read answered [] for a live route on page 2 of 116) is resolved by D2-S15. The applier re-read
  all pages, found 1 match of 116, and fired no Branch B.
- **Still owed** after IRPT_CUSTDY E2a retains a real submission: the real persist, the owner read by reference, and the other-firm
  OBJECT_NOT_COVERED read.

## Round 91 -- IB-pr-379 (COMPLETE under AMENDMENT 1): why the inflection and cottonwood builds drop entries

- **Both drops are SOURCE_REMOVAL**, one entry at each firm, absent from the source since 2026-10-06:
  - inflection: a household the vendor merged away;
  - cottonwood: a zero-value account no longer emitted.
- The build is right. Row D2-W187-S1 is BLOCKING and ARMED: cottonwood goes OVER_AGE 2026-10-12, inflection 2026-10-13.
- The CTO ruled the rule (msg 1959). AMENDMENT 1 closes the cell on its diagnosis, IB91-1-AC1 PASS.
- The worker's proof instance is being updated to the amended criteria, so round-close reads REFUSED until it lands.

## Round 92 -- IB-pr-380 (OPEN, worker ~188, issued @cea36aeb49): carry source-removed entries forward as TERMINATED

- The rule is as ruled: an entry absent from both the build and the source is carried forward as TERMINATED + source_removed_on, and
  the build goes READY. An entry in the source but missing from the build stays REFRESH_FAILED; that is the negative arm, run on both
  firms' real inputs. Each refresh prints its TERMINATED count.
- The release goes under its own pair and is due live by Friday 2026-10-09's close.

**Push state:** LOCAL on box/dell2 (MSTR pushes :18/:48).
