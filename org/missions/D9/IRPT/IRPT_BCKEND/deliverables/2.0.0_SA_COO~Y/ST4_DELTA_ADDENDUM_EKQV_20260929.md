# st4 delta addendum -- `jK0FFkzC` -> `ekqvI5um` (adds TO-IB-yr-221), for re-sign on the delta

**For:** `1.0.0_SA_CTO` and `4.0.0_SA_CRO`. **Author:** `2.0.0_SA_COO~Y`, 2026-09-29 ~12:3xZ, per sweep-2 section 3
item 3 (`org/missions/D9/IRPT/IRPT_BCKEND/ledger/ROUND_ANALYSIS.sweep2.md`). **Operator:** `2.0.0_SA_COO~P`.
**Base packet:** `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/NEVER_WIDEN_SIGNOFF_PACKET_RESIDENT_ST4_20260929.md`
(blob 4f34a600, both halves signed on `jK0FFkzC`). Every section not named below reads as that packet's.
**Ledger:** `irpt-resident-st4-yr201-yr211-20260929` (D1 open).

## 1. What the delta ships

| change | commit | file |
|---|---|---|
| IB-yr-221 amendment 1 (the CTO's st4 condition 102655/102688): the 4th receive of a `resolve_upload` RETRY ENDS the job | 0357fc7e08 | resident_worker.py |

`git diff 14c961af32 0357fc7e08 -- infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py`: +44/-4.

## 2. The artifact moved -- measured, not predicted

- S3 `ec2/investor-reporting-ycharts/resident/irpt-resident-fe64-st4.tar.gz`, version `ekqvI5um7gQQ0vY4.FrprYd0vwEA5Q4U`
  (IsLatest), 731,481 bytes, sha256 `63a5e26a3caa3a00f03f4361dc2a8f2d1a21bc31797af665d45224b745dfd054`, 266 members.
- Member diff vs `jK0FFkzC`: exactly 3 files -- `resident_worker.py` (0b67be2a -> 5288ff5a, = CLOUD 0357fc7e08),
  `SHA256SUMS`, and `reports/resident_bindings.json` (provenance only: `generated_at`, and both member_overrides
  14c961af32 -> 0357fc7e08). `recipe.py` unchanged (b2fbd720).
- ~Y gates on these bytes: PASS (`ST4B_GATES_20260929.md` @a6caedc4ed; 54 passed / 8 skipped on the built modules).
- The install script `resident_host_install_st4_20260929.sh` in ~P's working tree (sha c2283359, **not yet committed**)
  pins `WANT_TAR` = 63a5e26a and `WANT_WORKER` = 5288ff5a. ~Y read all 10 file pins against the extract: 10 of 10 equal.
  The halves should bind to the committed blob of that script.

## 3. Blast radius of the delta -- both branches

Writers of a NORMALIZATION row's `state`: **4**, each rule read:
1. `UploadService._defer` (intake/uploads.py:272) creates the row RESOLVING (publish, first writer wins);
2. `UploadService._answer` redrive (uploads.py:297) rewrites a RESOLVING row with a new `dispatched_at`, state unchanged,
   conditional on the same `dispatched_at`;
3. `UploadService.resolve_deferred` (uploads.py:324) moves RESOLVING -> NORMALIZED or NEEDS_CORRECTION;
4. **new**, `resident_worker._end_exhausted_resolve` moves RESOLVING -> NEEDS_CORRECTION (reason `RESOLVE_RETRY_EXHAUSTED`).

Writers 3 and 4 both write through `NormalizationStates.replace(..., expect_state=RESOLVING)`, so exactly one terminal
wins, and a row that has already left RESOLVING is never touched again.

- **A resolve that RETRYs at receive count < 4 (unchanged from `jK0FFkzC`):** RETRY is logged and re-offered in 60 s.
- **A resolve that RETRYs at receive count >= 4 (moves):** in `jK0FFkzC` the 5th receive dead-letters the message and
  the row stays RESOLVING, redriven every 960 s while a page is open. In `ekqvI5um` the row ends NEEDS_CORRECTION
  `RESOLVE_RETRY_EXHAUSTED`, the resident prints `state=ATTENTION code=RESOLVE_RETRY_EXHAUSTED` and deletes the
  message, and the page answers the named reason (intake/uploads.py `_answer`, already served). A new upload of the
  same file mints a new `upload_id` from its client token (uploads.py `create`), so the user can retry.
- **Unchanged:** every READY resolve, every generation message, and everything the base packet lists as unchanged.
  No Lambda, IAM, queue, schema or portal contract moves (CTO 102694: the existing terminal, no new row state).

**Rollback per key:** unchanged from the base packet -- the resident root `fe64236bbb-st3` stays on the host.
