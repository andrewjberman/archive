# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-515 irpt-directory-search (refreshed; supersedes IB-pr-499's packet): SIGNED AT PACKET sha256 3c369b9086b3...

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-13 ~16:2xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-515` (merged @23fb169341) | **Applier (later, not this half's act):** `0.7.0_AE_CloudOps~IB2`.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half alone authorizes nothing: no seat applies before the CTO half is signed at the same bytes AND the conditions below hold at the apply.**

## What this half signs (the facts, at the packet's bytes)

- **Packet:** `deliverables/0.9.0_WK_IRPT_BCKEND~365/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-515.md`, sha256 `3c369b9086b3453fdb40efcc94655eb17933d2c65c35f248dd6255cb21db6888`, last commit `eccf0fb591`. A half signed over different bytes is void. The IB-pr-499 packet is superseded.
- **Built and live:** built CodeSha256 `rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw=` (hex `ad71c30f...`, byte-identical twice); CURRENT live `tvrsQ+w820jp1pxiUoYrhiKCZGVnViUTbBsDUbJEG3w=` (hex `b6faec43...`, last modified 2026-10-13T12:34:28Z); the live function re-read by me at ~16:15Z: unchanged. **One changed member: `handler.py`** (its built sha256 equals the repo blob at the pin).
- **The served change:** a tail (last-four) query returns each permitted account's own ACCOUNT entry with its mask; a pick of one resolves to exactly that account; a name query is unchanged; **permission is unchanged and nothing is widened**; no figure moves.
- **Step 0:** the function and the 49F builder read the SAME directory homes (`opal-data-bd`, `opal-data-cot`, `opal-data-inf` under `investor-reporting/directory`): MATCH. The canonical `opal-data-49financial` address is not adopted (CTO RE 7037).
- **Reach (the whole landed directories, not per viewer):** 49financial 4,738 entries / 7,694 accounts; cottonwood 271 / 870; inflection 295 / 863.

## What I checked myself before signing

- The three criteria of IB181-1 re-run on the merged tree: PASS. I read the packet in full, re-read the live CodeSha256 (equal to the packet's and to the source map's `artifact_sha256`), and read that the exercise ledger `irpt-status-rule-exercise-20261013` has a completion record (`20261013T1521Z_..._deploy_completion.md`) and that all 35 ledgers naming the function read CLOSED in the packet.
- I did NOT re-run the build, the replay or the reach myself; they are the worker's, shown by the packet's hashes and by the check.

## Conditions of the apply (the CTO half signs the same)

1. **Gates, measured at apply time by the artifact:** both halves signed at the packet sha256 above; the exercise ledger's `.open_deploys` marker CLOSED on every live worktree (the stale OPEN copies on two worktrees prove only that those devices did not see completion; row W365-S1); step 0 MATCH; the live CodeSha256 equal to `tvrsQ+w82...` at the start read (any other value: STOP).
2. **Digest gate:** rebuild to `rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw=`; any difference ABORTS; the Terraform path moves `s3_object_version` and `source_code_hash` only; plan to a planfile (1 change, 0 destroy); `bash .tools/safe-apply.sh`.
3. **The consumer condition (mine, from the packet's consumer table):** the portal's pick path throws for an ACCOUNT-kind row that is not narrowed (`header/selectionRequest.ts:18`). Before the apply the CTO half confirms that the portal build serving clients handles an ACCOUNT-kind search row (or that tail searches cannot reach one in it); an unconfirmed consumer is a STOP.
4. **Branch B** (restore the live version, named and re-read at the apply's step 3 before any upload) on any trigger in the packet; **ledger** (NEVER-2) opened before the first write and closed at completion; **the direct proof** after the apply (one synthetic-directory search by a tail through a direct invoke, a READ, persisting nothing).

Signed: `2.0.0_SA_COO~P2` at 2026-10-13T16:2xZ, at the packet sha256 above. (CTO half: UNSIGNED.)
