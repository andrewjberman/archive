# IB-yr-221 session log -- 0.9.0_WK_IRPT_BCKEND~73

Task order: `IRPT_BCKEND.TO-IB-yr-221.resolve-retry-bounded-below-the-dlq.md`, issued by `2.0.0_SA_COO~Y`,
CTO condition st4 @1576687ade (~P 102659). AMENDMENT 1 (2026-09-29, CTO ruling 102688 on CRO 102684): the
first form's GAVE_UP-delete-leave-row-RESOLVING bound was still unbounded via the client's 960 s redrive; the
bound must END the job. Branch already held steps 1-2 and the GAVE_UP delete (@c125c68396); merged CLOUD
(6a2a512c35, carrying the amended order) into `wk-IRPT_BCKEND-73` -- worktree arrived pre-merged at HEAD
e5a4be79d1, so no merge act was needed this session -- then replaced step 3 per the amendment.

## Build (`infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py` only)

1. `RESOLVE_MAX_RECEIVES = 4` (module constant, comment naming the live queue's `RedrivePolicy`
   `maxReceiveCount` 5) -- unchanged from @c125c68396.
2. `poll_once`'s `receive_message` call asks for `AttributeNames=["ApproximateReceiveCount"]`;
   `MaxNumberOfMessages`, `WaitTimeSeconds` and `VisibilityTimeout` unchanged -- unchanged from @c125c68396.
3. AMENDED: for a `resolve_upload` `RETRY` at `ApproximateReceiveCount >= RESOLVE_MAX_RECEIVES`, `poll_once`
   now calls `_end_exhausted_resolve(assembly, decoded)` before printing/deleting. That helper reads the row
   the way `ResidentAssembly.resolve_upload` does (`read_resolution_message`, `normalization_key`,
   `self.requests.artifacts.index.get`), and -- only while the row is still RESOLVING -- replaces it via
   `upload_resolution.NormalizationStates(index.table).replace(...)` (`expect_state=RESOLVING`, a conditional
   write; a `False` return is silently accepted as another writer's win) with `state=NEEDS_CORRECTION`,
   `reason="RESOLVE_RETRY_EXHAUSTED"`, `findings=[finding("RESOLVE_RETRY_EXHAUSTED")]` (`template_reader.finding`,
   default actions), `findings_total=1`, `resolved_at=int(assembly.clock())`. `poll_once` then prints exactly
   `IRPT_RESIDENT_RESOLVE state=ATTENTION code=RESOLVE_RETRY_EXHAUSTED` (flush=True) instead of the old GAVE_UP
   line, and deletes the message. The GAVE_UP line is removed. Below the bound: unchanged IB-yr-211 behaviour
   (the RETRY line, then the 60 s re-offer).
4. No new row state added: RESOLVING / NORMALIZED / NEEDS_CORRECTION is the existing contract; `intake/uploads.py`
   `_answer` already serves NEEDS_CORRECTION with its reason and findings (read-only, unmodified). Generation
   messages unchanged. `intake/uploads.py`, `intake/upload_resolution.py`, `intake/template_reader.py` read-only
   (imported, not edited).
5. `tests/test_resolve_upload.py` left unmodified (optional step skipped, as before): the read-only
   `R22_CHECKS/test_r22_y1_resolve_bounded.py` harness already exercises all three amended arms (fourth-retry-
   ends-attention-by-name, asks-for-the-count, early-retry control) via that file's own `Queue`/`case`/`assembly`
   fixtures subclassed as `CountedQueue`.

## Runs (amended criteria)

- `Y22-1-AC1` (`test_fourth_retry_ends_attention_by_name`): `1 passed in 1.49s`, rc 0.
- `Y22-1-AC2` (`test_asks_sqs_for_the_receive_count`): `1 passed in 1.47s`, rc 0.
- `Y22-1-AC3` (`test_early_retry_is_kept_and_reoffered`): `1 passed in 1.44s`, rc 0.
- Full check file together, twice for determinism: `3 passed in 1.35s` both runs, rc 0, identical.
- Full existing suite (`tests/test_resident_worker.py` + `tests/test_resolve_upload.py`, collected together so
  `test_resident_worker` sets up `sys.path` for `extract`/etc. first -- the collection-order dependency is
  pre-existing, confirmed by reproducing the same `ModuleNotFoundError: No module named 'extract'` when
  `test_resolve_upload.py` is invoked standalone, unrelated to this change): `46 passed, 8 skipped in 45.51s`,
  rc 0. No pre-existing test broken.

## Mutants

1. Boundary: changed `receives >= RESOLVE_MAX_RECEIVES` to `receives > RESOLVE_MAX_RECEIVES` (worktree-only,
   never committed). `test_fourth_retry_ends_attention_by_name` FAILED (`assert [] == ['rh-1']`, message kept
   instead of ended at receives==limit). Reverted before any commit.
2. Row write: made `_end_exhausted_resolve`'s `NormalizationStates(...).replace(...)` unreachable with an early
   `return` (worktree-only, never committed). `test_fourth_retry_ends_attention_by_name` FAILED on the row-state
   assertion (`'RESOLVING' == 'NEEDS_CORRECTION'`), confirming the test actually checks the amended row
   transition and not merely the print/delete. Reverted before any commit; re-ran all three criteria green,
   twice.

## Premise check

The cell's citations (`resident_worker.py` `RESOLVE_RETRY_VISIBILITY_S`, `poll_once`, `RESOLVE_MAX_RECEIVES`;
`intake/uploads.py` `_answer`'s `REDRIVE_SECONDS` redrive; `upload_resolution.NormalizationStates.replace`,
`normalization_key`, `read_resolution_message`; `template_reader.finding`) matched the world at HEAD e5a4be79d1
closely enough to act on directly; no surprise row filed for amendment 1.
