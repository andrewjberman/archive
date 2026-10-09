# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ release 1: `irpt-status` + the `/original` route

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~08:5xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 2937
**Signed against:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_IRPT_STATUS.md`, **blob ae6a278722**
(commit d88c78917a). Pin `3a6d021e4a`.

## Measured by this seat

- Live `irpt-status` is `E7VKvhg3...`, which equals the packet's live and rollback (IB-pr-390's release on this host).
- `served.py` at the pin is `87d9ecc49747...`, equal to `74a62fb46c`. This release reverts neither ALL-never-admits nor the narrowing (the D2-S31 class).
- The pin is an ancestor of `origin/box/dell2`, so it is on origin.

## Blast radius signed

- One code update (5 changed members: AR-y-11 and AR-y-22).
- One ADDED GET route under the existing authorizer and integration.
- The signer admits `ORIGINAL_HOLDINGS` and `ORIGINAL_CSV` bound to `reporting_destination`, for the caller's OWN request, re-authorized per request.
- No IAM change: the family list already holds both, at `ops/iam.tf:85`.
- **Two plans:** ops (the function only) and api (1 add). Any other line in either means STOP (the shared-root rule @29a9a2c684).
- **Branch B:** as the packet states. Re-promote the step-0 version, revert the route, then a BLOCKING row.

## Conditions

1. **After-reads 0-5 run in the packet's fixed order.** Read 1 gates the apply.
2. **Read 3 has three arms, and all three must pass:**
   - the owner receives the link, with sha256 equal;
   - another firm is refused;
   - custody refuses `ANALYSIS_ORIGINAL_NOT_APPLICABLE`.
   The signed link is never written to a log or report; only its sha256 match is recorded.
3. **Read 6's S3 deletes wait on Andrew's word,** listed by key and version.
4. **The ledger states the pin, `WTGCJPiS`, and the uploaded version id** (law @ccbe8b8be1). The applier is `0.7.0_AE_CloudOps~DELL2`.
5. **The census row for the new route reads ONE for the test filer** after the apply, so FWD-1's seat run stays unblocked.

**Verdict: GIVEN**, for release 1 exactly, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (~10:3xZ, row IRPT_BCKEND-D2-S43, `~P2` msg 3139): the new route must be declared to `_authz` before apply

`_authz test_unguarded_census` fails at box/dell2 HEAD: `GET .../analysis/requests/{requestId}/original` (AR-y-22) is declared by no entry. A route the guard
census cannot see is unguarded as far as the estate's own check knows, even though it is re-authorized in code.

**Added condition 6:** `~Y2` adds the route's `_authz` entry in a one-cell fix. `test_unguarded_census` passes at the release pin, and is printed in the ledger,
BEFORE the apply. No apply happens while the census fails. The only excuse permitted is `~P2`'s, by name and inside IB-pr-405's own check.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 2 (~10:4xZ, `~Y2` msg 3162): re-signed on REVISION 2, blob 0bb9a5a803 (commit ba918317c3)

**Measured by this seat:**
- the diff over the signed blob is the re-pin (`f23639ea21`), the new build (`BjUZjt2o...`), one added member (`status_installed.py`, which declares `/original`), and the census
  row `9 passed, 22 of 22 guarded`;
- `served.py` at `f23639ea21` is `87d9ecc49747...`, which equals `74a62fb46c`, so there is no 390 revert;
- `f23639ea21` is NOT yet an ancestor of `origin/box/dell2`, read at 10:4xZ.

**Verdict: GIVEN on REVISION 2,** with conditions 1 to 6 unchanged. Condition 6 (the census) is now met at the pin.
- **The pin must be on origin before the apply,** as the packet itself says, and the applier re-reads it.
- The ledger names `BjUZjt2o` and the uploaded version id.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 3 (~12:2xZ, `~Y2` msg 3259): re-signed on REVISION 3, blob ac59c753eb (commit 1d9154f3ce)

**Measured by this seat:**
- live `irpt-status` is `BjUZjt2o...` (11:20:57Z), so REVISION 2 is LIVE and is REVISION 3's rollback.
- At the new pin `5240156380`, the TREE's `served.py` hashes to `ada9bf5bcfd1...`, NOT `87d9ecc49747...`. The tree has moved (IB-pr-403 and 405 work).
- The build stages members from their own pins, so **the BUILT bytes, not the tree, are what ship.** The packet's census of the built zip against live reads exactly
  ONE changed member: `reporting_policies.json`, research firms 1 to 3. `entry.py` and `owned_report.py` are held at `~Y` commits so IB-pr-405 does not ride.

**Verdict: GIVEN on REVISION 3,** for exactly the one-member change, built `t6OJTCcm`.

**Conditions added:**
- **The applier prints the sha256 of EVERY member inside the uploaded zip against the live zip's,** and exactly one may differ. That is the census, re-run on the
  uploaded bytes.
- **Any second differing member means STOP.** That would be the D2-S31 class: a tree change riding a narrow release.
- Its after-read: REQ-5e4149d2 (the YCDGEN Opal Overview) is no longer RetentionRefused.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 4 (~15:3xZ, `~Y2` msg 3567): REVISION 4 -- `irpt-status` registers the writer's research revision

**Signed against:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV4_IRPT_STATUS.md`, **blob 142e1e6d2d**
(@86685d4180). Ruling it executes: `CTO_RULING_IRPT_YCDGEN_FWD1_RETENTION_REF_SKEW_20261009.md` AMENDMENTS 2-3.

**Read:**
- Built `VC/r14ka...`; live and rollback `t6OJTCcm...` (rev 3).
- Census against live: ONE member, `status_installed.py`. `resident_installed.py` stays at 80a79a7462.
- Symbol closure: missing=0. `_authz`: 22/22. Revision tests: 6 passed, including the fail-closed arms.
- Plan: `-target=module.irpt_status`, code only, no API change.

**Conditions:** the pair's R0-R3, with the release 1 half's rules unchanged:
1. **R0:** live reads `t6OJTCcm` before the upload. The per-member diff of the UPLOADED zip against live is exactly `status_installed.py`, or STOP.
2. **The shared-root rule (@29a9a2c684):** any plan line outside `module.irpt_status`'s code means STOP.
3. **R3 is `~G2`'s owner read, in a NEW sr1 window under that half** (the 30-minute bound from W1). It returns codes and section names only.
   - Answering 200 is FWD-1's served-half evidence.
   - A refusal is recorded with its code, and Branch B is NOT taken for a refusal alone: rev 4 does not regress rev 3, and only an R2 failure rolls back.
4. **The ledger states the pin `287b105600` and the built sha256** (law @ccbe8b8be1).

**Verdict: GIVEN**, for exactly this one-member update.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 5 (~16:2xZ, `~G2` msg 3676, LIVE OUTAGE): REVISION 4 crashes every caller -- Branch B ORDERED

**Measured:** rev 4 (live 15:43:11Z) raises `TypeError: build_retained_repositories() got an unexpected keyword argument 'additional_policy_revisions'` at
`status_installed.py`:137 on every request. CloudWatch shows 52 events between 16:17 and 16:22Z, and HTTP 500 to every caller.

**Cause:** a split ship. The packaged `composition.py` lacks the new keyword, so the one-member census was the fault. The symbol-closure check reads names, not
call signatures, so `missing=0` could not see it.

**RULING:**
1. **Branch B now:** re-promote rev 3's S3 version `t6OJTCcm` through the same path (msg to `~Y2` ~16:2xZ).
   - AMENDMENT 4's line "only an R2 failure rolls back" is WITHDRAWN: a regression to every caller is Branch B, whatever R2 read.
   - This seat's wording was the gap.
2. **The after-read of the rollback:**
   - live reads `t6OJTCcm`;
   - ONE real GET through CloudFront answers 200 for a caller outside the 49F case;
   - the CloudWatch error count goes flat after the promote.
3. **Re-cut rev 4:**
   - `composition.py` is co-staged with `status_installed.py`; the census shows exactly those two members;
   - a call-signature closure read covers every changed call site;
   - **a LIVE-CALL arm sits before the ledger closes:** one GET answering 200 on a non-49F request within a minute of the promote. A 500 means immediate Branch B.
   - **This live-call arm is now standard in this seat's halves for every served Lambda release.**
4. **The outage window is recorded in the ledger:** 15:43:11Z to the promote time.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 6 (~17:1xZ, `~Y2` msg 3774): REVISION 5 (the rev 4 re-cut) -- GIVEN

**Signed against:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV5_IRPT_STATUS.md`, **blob 5e8b14bf46**
(@778f5097f0). Pin 54ed3aa8f6, built `DZOdwUOG`, rollback rev 3 `t6OJTCcm`.

**Read:**
- **3 members change vs live:** `status_installed.py`, plus `composition.py` and `repository.py` re-pinned to `2aa217ec58`.
  - That pin is the bytes `irpt-export-render` already serves (IB-pr-369: families retained under their own policy revisions).
  - The three commits that ride the re-pins are therefore already-served code, not new behavior on any host. This is the D2-S31 class answered by measurement.
- **Signature closure:** 121 calls, 1 mismatch (`served:1006 InteractiveAccess(profile_reader=)`). It is ALSO in live rev 3 and owned by `~P2` (D2-S60), so it is
  tolerated by name. The rev 4 mismatch is gone.

**Conditions:** the pair's R0-R4 and Branch B, plus three:
1. **The S60 tolerance holds only while IB-pr-419 (verdict about 17:50Z) does not read irpt-status's `profile_reader` route FAILING.**
   - If it reads FAILING, this release does not promote until IB-pr-416's one-tree rebuild carries the fix.
   - Rev 3 serves meanwhile; it carries the same latent mismatch, so waiting is not worse.
2. **R3's traffic read prints the 5xx count beside the TypeError count,** both 0 over 5 minutes with START lines shown, plus `~G2`'s authorized 200. Either one
   failing means immediate Branch B.
3. **R4 failing alone does not roll back.** It is recorded with its code, as the pair states.

**Verdict: GIVEN** for this three-member update under the pair's R0-R4, Branch B, and conditions 1 to 3.

-- 1.0.0_SA_CTO~DELL2
