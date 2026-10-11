# L8 drain end -- IRPT_BCKEND round 122 (the ROLLBACK), workstream ~P -- and the CORRECTION of the rounds 119-121 packet and the COO half

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-11 ~10:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | **round-close:** round 122, workstream `~P`, reads MAY-CLOSE (`round-close-check.py --workstream ~P`:
orders=1, complete=1, proof_ok=1)

## CORRECTION -- read this before the rounds 119-121 packet (@a3cb79cdb6) and the COO half (@468df7baa4)

Both describe the vendor performance release (IB-pr-421, 422, 423) as the fix of DSGN_IRPTV1 FWD-1's Performance hop. **It was not a
fix. It was a departure from the ratified ENDPOINT, and it is rolled back.**

- ENDPOINT FWD-3 serves Inflection and Cottonwood "a performance figure computed by Opal from that account's own end-of-day holdings".
  PRD ADDENDUM v0.19, on Andrew-direct 2026-09-28: "FWD-3's vendor-calculation rule is RETIRED; a vendor figure is now only a
  comparison point (FWD-13)." `retained.py:53-62` (batch 66 item 2, row S247) states that a fresh vendor-path request is refused by
  design.
- This seat placed the refusal at `performance/authorization.py:90` as a stale per-use-word gate, recommended retiring it, and signed
  the COO half. It read the egress law and did not read the ENDPOINT. The egress law permits the vendor CALL; it does not change which
  figure FWD-3 serves. The CTO ordered the release on the same reading and has said so (msg 4624); msgs 4416 and 4616 are withdrawn.
- The miss was found by this seat while reading `retained.py` for the follow-on reopen cell, which was NOT cut. Escalation record:
  `deliverables/2.0.0_SA_COO~P2/ESCALATION_IB_pr_423_SERVES_COTTONWOOD_A_VENDOR_FIGURE_AGAINST_FWD_3_20261011.md` @a5f045cabf.
- **The COO half @468df7baa4 is VOID.** Its "Read by this seat" table is accurate as reads; its conclusion, GIVEN, rested on an
  unread ENDPOINT. The same holds for the round 119-121 packet's framing. Their measured facts stand; their word "fix" does not.

## What was served while the release was live (the part that cannot be undone)

Window 2026-10-11T09:19:10Z to 10:03:25Z, about 44 minutes. From `/aws/lambda/irpt-performance-adapter`, 31 events: **3 requests were
SERVED a vendor-calculated return** (09:45:40-42Z), 2 were refused NOT_AUTHORIZED, 1 was refused as a repeat. The firm is inferred to
be Cottonwood from the code path (only Cottonwood reaches the vendor branch); the caller is inferred to be the laptop's re-walk. **The
use records written in that window were NOT READ** (they are table items a log read does not reach; 0 log occurrences is not 0
records). The retained vendor reports and use records were deliberately not deleted: they are the record of what was shown.

## Round 122 (issuance @0246d74b53): 1 of 1 COMPLETE

- **IB-pr-424** (`0.7.0_AE_CloudOps~IB2`, WORLD): the release rolled back in one sitting under one ledger entry (CLOSED, 6 of 6 legs,
  @c267b71edb).
  - **Read by the issuer:** live adapter CodeSha256 `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` (modified 10:03:25Z); the live role
    holds 7 inline policies and neither session policy; `performance/` and `retained.tf` equal their content at `fb3bae3b99`; the
    adapter's source-map entry is its pre-release entry. AC1, AC2, AC3 PASS and proof VALID on the issuer run.
  - Per `~IB2`, not re-run here: the full-root plan reads "No changes"; a fresh request in the IB-pr-423 live-call shape is refused,
    with 0 `served` outcomes since the rollback. `~IB2` could not drive a caller the function ADMITS and says so; it also notes that
    this is why IB-pr-423's live-call arm could not have caught the defect.
  - The zip went back by content, not by version: the Terraform module reads the LATEST S3 version, so the pre-release entry was
    rebuilt (BUILD_ONLY printed `9kYLdR64...`) and uploaded as a new version of identical bytes.
  - Row D2-W282-S3's calendar test failure is now MEASURED pre-existing by `~IB2` on the restored tree.

## What the failure was, for the round-N analysis

1. **A pair that named the radius and never named the outcome.** Both halves listed what the act may touch and the rollback per
   key, correctly. Neither asked which ratified outcome the served change serves. The CTO has added that read to its next ruling
   (msg 4657); this seat carries it in every half from here: read the project's ENDPOINT against every served change before signing.
2. **A live-call arm that could not see the change.** The arm used an unauthenticated shape, refused before the vendor path, on
   purpose, so that the apply made no vendor call. It therefore read identical before and after. The only arm that exercised the
   change was a real user's request.
3. **An inherited sentence acted on.** "The gate enforces the law that order replaced" was true of one of the gate's two purposes.

## Rows

- D2-W282-S2 (a repeat of a vendor request is refused): with the release rolled back this is again the designed state, not a defect.
- Row filed with this packet: `round-close-check.py` without `--workstream` reads round 122 as REFUSED on `IRPT_BCKEND.TO-APPLY-Y77`
  (issued by `2.0.0_SA_COO~Y2`, complete, no proof instance at the name the checker expects). Thirteen seat-folder orders carry no
  `<round>` tag and are counted in every round.

## Carried

- IB-pr-413 L4 and IB-pr-404 L6: the Monday 2026-10-12 14:15Z 49F fire.
- Queued behind this close, by CTO ruling: a read-only read of what FWD-3 waits on for Cottonwood (rows S250, S252; msg 4704); the
  one-tree re-pin of `irpt-ycharts-generate` (msg 4657); the `_contracts` smoke-map pin with the two custody fixtures (`~D2` msg 4714).

**Push state:** LOCAL on box/dell2 (MSTR box-sync pushes); re-measured in the send.
