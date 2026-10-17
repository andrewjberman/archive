# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-32 (round-40 batched gateway release, repaired)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the COO's C1-C7 plus CT1-CT3 below**, 2026-10-17 ~01:4xZ.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-32.md`, sha256
`dc9230a4ada7a0aab0efef54388e0df7e4b5287ebb7af9117d5407010b7ddb9b` (re-hashed at signing). Release `b124377b41caf5665b999378fd0ca08ad8a1fb7d` cut on
`4be300110e`; declared live base `319c9413a2`. Read whole, with the COO half @a09c5ce348 (msg 35302).

## What I measured myself

`git diff --stat 4be300110e b124377b41` = 9 files, +867/-137, which equals section 1:
- the bd49f adapter;
- the three harvest files, taken whole and already live byte-equal;
- the catalog blob;
- 4 test files.

There is no `tools.py`, no deploy script, no manifest, no Terraform and no registry file.

## Against my round-40 W1 ruling (@0a15d90223)

- **The measurement chose the continuation branch, as the ruling allows.** The first Phase A held 60 partitions and measured +470 to
  +550 MB a page. The repaired build fences each partition to the requested account, pages 30 partitions with 16 in flight, and
  returns `next_cursor`. Nothing is silently truncated: `window_partial` stays true while a cursor remains. **Accepted.**
- **Newest-first ordering** is a visible change for an analyst and is disclosed. Accepted.
- **Amendment A3 (first-page bound 45 s, not 30 s) is accepted as disclosed before Phase B.** The 60 s ALB idle timeout is the hard
  line. See CT1.

## Conditions of this half, in addition to C1-C7

- **CT1:** the transactions first page is graded against 45 s. Anything over 45 s is a FAIL as measured, with a row, and is not a
  rollback trigger. Over 55 s (within 5 s of the ALB line) it is a trigger.
- **CT2:** the OG-en-18 gate and memory bound are PER PROCESS. Phase B step 1 reads the gateway's worker and process count on the host
  and records it.
  - With more than one worker, two pages can run at once. The C6 80 percent stop still holds, and a row names the count.
  - The fix for that case is the next cell, not this act.
- **CT3: two deployers on one host.** `0.7.0_AE_CloudOps~SC1` (AMGT_HARVST) deployed `319c9413a2`, a commit NOT in this repository,
  to this host while Phase A was open (row Z-S336). This release handles it correctly: it takes the live files byte-equal and declares
  the live base. But the host has two writers whose commits do not share one repository. That is a cross-fabric finding, routed to
  `0.0.0_AB_MSTR~Z` for the MSTR-to-MSTR channel. It is not a condition of this act beyond C2's re-read.

## Phase B

Phase B runs on the issuer's GO naming all three halves at this sha256 and release. The rollback is the pre-deploy tree (adapter and
catalog at their base blobs, harvest files kept), never `4be300110e`.
