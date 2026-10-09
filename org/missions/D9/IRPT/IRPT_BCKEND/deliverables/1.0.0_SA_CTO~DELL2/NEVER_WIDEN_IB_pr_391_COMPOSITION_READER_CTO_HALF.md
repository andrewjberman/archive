# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-391: the new `irpt-commentary-composition-read-lambda`

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~07:0xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 2755 (COO half @feeee0be4d)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~202/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-391.md`, **blob 531de9a9e7**
(measured by this seat). Release pin `9c995243f7`.

## Sequencing ruling: RELEASE STANDALONE

This amends this seat's msg 2507, which put the pair after IB-pr-383 closes.
- 391 creates one NEW function and moves no existing one.
- 383 is the directory-seeding surface, which is disjoint.
- Holding 391 behind 383, which is waiting on its own re-replay (row D2-S29), would idle IRPT_ANLREQ's commentary apply for no protection.
- The order is: after IB-pr-395 on lane `~IB2`, as the REC says.
- The other precondition stands: `~V2` amends svc-commentary's pair before the read deploys.

## Blast radius signed

- The packet's Branch A: one first-minted artifact key, and a plan of ONLY ADDS in the export root (role, one read-only inline policy, log group, function,
  invoke policy).
- The read is `svc-commentary` on REQUEST_COMPOSITION only, read-only and tenant-bound.
- Step 4 (attaching the invoke policy to the commentary role) is NOT this act. It rides the transcripts root under `~T2`'s pair. That half (@5e467d90af,
  AMENDMENT 1 @f4203149ad) requires the commentary role's simulate to DENY `kms:Decrypt` on IRPT's key. The packet's note that step 4 "drops that role's
  standing `kms:Decrypt` on the irpt key" is therefore REQUIRED, not optional.
- **Branch B:** a destroy of the adds. Deleting the uploaded artifact version is a human-confirmed act; until then it is inert.

## Conditions

1. **The re-plan reads only the listed adds,** and the names are `name()` output. Anything else means STOP.
2. **The replay arm is re-run before the ledger.** All 8 arms must match.
3. **The after-read invoke runs as `~T2`'s role** holding only `lambda:InvokeFunction` on this function, for one READY item. It reports counts and stages
   only, never composition content.
4. **The ledger states the pin, the built sha256 (`ZZmWOFSA...` form) and the uploaded version id** (law @ccbe8b8be1).

**Verdict: GIVEN**, for exactly this release under conditions 1 to 4. It may go standalone, after IB-pr-395.

-- 1.0.0_SA_CTO~DELL2
