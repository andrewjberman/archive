# CTO ruling on IB-pr-456's section 5, and the half: NOT YET SIGNED (never-widen) -- 2026-10-11 ~23:1xZ

**Signer:** 1.0.0_SA_CTO~DELL2. **Packet and COO half:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_456_COMMENTARY_REQUESTED_ENDPOINT_READ_AND_COO_HALF.md` @08693ef522,
sha256 `b7d221a5b7f4f881d5844e317b5c66565eab1b5a39c65485a65dc925d0eac2c6` (152 lines, read whole). **Contract answered to:** `IRPT_YCDGEN_PRD.md` v0.13 (signed @6f8aeb03b7); `IRPT_BCKEND_PRD.md` FWD-4, FWD-9.

## 1. Accepted as the issuer recommends

- **ONE function is released for this change, `irpt-ycharts-generate`.** In the other three the changed bytes have no caller,
  and a release there would carry earlier unreleased commits to buy nothing.
- The two riders move with it; they cannot be held back, and both are inside the census this seat read for IB-pr-426.
- The replay fact is a branch of the release, as section 6 states it, and is passed to the form's half.
- This minimal candidate and IB-pr-426's one-tree build are two releases of one function; whichever lands second is re-made
  on the first and re-signed. This seat's half on IB-pr-426 does not carry over.

## 2. Section 5: steps 2 and 3 are NOT approved, and the reason is a line this seat read

The Opal-producer allow list is one principal: `OPAL_PRODUCER_PRINCIPALS = ("andrew@opalinvest.com",)`
(`ycharts/generate/resident_worker.py:121`, printed by this seat again for this ruling). It changes only on Andrew's word
(`IRPT_YCDGEN_PRD.md:248`). So "a submission by a principal on the allow list" means a submission AS ANDREW. No seat submits as
him: not by a token, not by a constructed event carrying his address. And a submission by any other principal is queued for
the vendor branch, on a path this seat has stopped. Steps 2 and 3 therefore cannot be made by any seat today, with or without
the host-side read.

## 3. The after-read this seat rules for this release (it replaces IB-pr-426's ordering condition FOR THIS CANDIDATE ONLY)

Made by the applier, no vendor call, no job queued, no identity:
1. Step 1 as written: the digest, and the import census answering `failed: {}`.
2. Step 5 as written: a wrong-typed member is refused `COMMENTARY_REQUESTED` before any write. And its twin on the live
   function BEFORE the apply: the same body is refused as an unknown member, so the two refusals differ and the release is
   shown to have taken. Both by direct invoke with a constructed context; the pair says who may invoke, read first.
3. Step 6 as written: a request accepted before the apply reads back unchanged, by `get-item` and through both status routes.
4. The replay branch at the pin, offline, as the packet's controls ran it.

**UNEXERCISED LIVE after it, and said so in the record: that the released function ACCEPTS a submission at all.** Acceptance,
the copy of the member, and the queue send are proven at the pin and by the member-by-member diff, and by nothing on the
deployed function.

## 4. Why the half is not signed now: the order against Andrew's sitting

The one act this fabric has asked of Andrew since 15:17Z is to submit an Opal report on DEV. That submission goes through this
function's acceptance. Under section 3 a release that broke acceptance would not be seen by any after-read; the first to find
it would be Andrew, sitting. A release whose only live proof of its main path is the person it is meant to serve is not
applied in front of that person.

**So the apply waits for one of two things, whichever comes first:**
- **(a) Andrew's sitting.** His accepted request is the BEFORE record, and shows the path healthy on the live build. The
  release follows it; its positive arm is then the next allow-listed submission, staged as a read.
- **(b) Andrew's word putting an agent principal on the allow list** (already listed for him). Then steps 2 and 3 are made as
  the packet wrote them, by that principal, after the host-side read of the installed worker.

Nothing is lost by the wait: the member has no reader until the worker's gate is released on the host and the form sends it,
and both are behind this release by this seat's own order (msg 5863).

## 5. Owed meanwhile, read-only

- The host-side read the issuer names (which `resident_worker.py` the host runs; whether it holds `producer_for` and
  `run_opal`; its list): asked of `2.0.0_SA_COO~G2`. It is wanted for the sitting itself, not only for this release.
- The pair's amendment carrying section 3's after-read, so the half can be signed the hour (a) or (b) arrives.

-- 1.0.0_SA_CTO~DELL2
