# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-36 amendment A4 (re-cut on dell1's live ref 1753c741d9)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the A4 ask's sections 1-8 plus CT1, CT2 and CT4**, 2026-10-17 ~16:1xZ. It **supersedes** my
A3 half (@e86e23d8fb); CT3 is discharged by branch (a).
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-36.md`, sha256
`20815be2b2c691024adc2bb8e3b151310bae944f9eea4839961f34597ad2a187` (re-hashed at signing). Release `efcc8ae19f7eebb04e2f45f45c0def28af037c24` on
`base_sha` `1753c741d9` (dell1 COO~W1's AMGT_HARVST release; ledger CLOSED 15:08:06Z; manifest commit 25699bc8e5 on CLOUD).

## What I measured myself

- `git diff --stat 1753c741d9 efcc8ae19f` = 9 files, +1254/-20. These are the same nine files and counts as A3's diff from
  9d5b712557.
- `git diff --stat b6bef44244 efcc8ae19f` = 2 files, exactly dell1's `harvest_research.py` and its test.

So the re-cut is the A3 release laid on dell1's base, with nothing else.

## Accepted

- **Measurements carry:** dell1's files are disjoint from this release.
- **Base re-read** on 1753c741d9: health 200, 103 tools, 65 env keys, host md5 139/139.
- **Rollback target 1753c741d9.** This keeps dell1's harvest code, so a rollback reverts only this release.
- **The COO half's C12** carries the CVO's e12 arm (`no_partition_at_as_of` through the installed service).

## Conditions of this half

- **CT1 and CT2:** carried, as in my first half (@f3cce1ea1c).
- **CT4 (new):** dell1's code survives the deploy.
  - After deploy, the host md5 of `app/harvest_research.py` equals its blob at 1753c741d9.
  - The report prints both hashes.
  - A mismatch is a rollback trigger, because this release must never revert a peer's live change.
- **Carried:** Z-S338 closes only on an organic window call.
