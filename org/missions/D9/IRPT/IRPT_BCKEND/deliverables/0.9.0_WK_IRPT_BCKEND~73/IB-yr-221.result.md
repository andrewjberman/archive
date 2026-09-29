# IB-yr-221 session log -- 0.9.0_WK_IRPT_BCKEND~73

Task order: `IRPT_BCKEND.TO-IB-yr-221.resolve-retry-bounded-below-the-dlq.md`, issued by `2.0.0_SA_COO~Y`,
CTO condition st4 @1576687ade (~P 102659).

## Build (`infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py` only)

1. Added `RESOLVE_MAX_RECEIVES = 4` (module constant) with a comment naming the live queue's
   `RedrivePolicy` `maxReceiveCount` 5, so the bound stays strictly below it.
2. `poll_once`'s `receive_message` call now asks for `AttributeNames=["ApproximateReceiveCount"]`;
   `MaxNumberOfMessages`, `WaitTimeSeconds` and `VisibilityTimeout` are unchanged.
3. For a `resolve_upload` `RETRY`: read `int(envelope.get("Attributes", {}).get("ApproximateReceiveCount", "1"))`.
   At `>= RESOLVE_MAX_RECEIVES`: delete the message, print
   `IRPT_RESIDENT_RESOLVE state=GAVE_UP code=RESOLVE_RETRY_EXHAUSTED` (flush=True) INSTEAD of the RETRY line, and do
   not touch visibility. Below the bound: unchanged IB-yr-211 behaviour (the RETRY line, then the 60 s re-offer).
   READY/ATTENTION delete-on-terminal behaviour is unchanged and is skipped only on the GAVE_UP branch (the message
   is already deleted there).
4. No NORMALIZATION row write added or removed; the row stays RESOLVING on GAVE_UP for the client poll's own
   `REDRIVE_SECONDS` redrive (`intake/uploads.py` `_answer`, read-only, unmodified).
5. `tests/test_resolve_upload.py` left unmodified (optional step skipped): the read-only
   `R22_CHECKS/test_r22_y1_resolve_bounded.py` harness already exercises all three arms (gives-up at the bound,
   asks-for-the-count, and the early-retry control) via `test_resolve_upload.py`'s own `Queue`/`case`/`assembly`
   fixtures subclassed as `CountedQueue`.

## Runs

- `Y22-1-AC1`: `1 passed in 3.11s`, rc 0.
- `Y22-1-AC2`: `1 passed in 1.92s`, rc 0.
- `Y22-1-AC3`: `1 passed in 1.14s`, rc 0.
- Full check file together: `3 passed in ~1.6-1.8s`, rc 0, run twice for determinism (identical).
- Full existing suite (`tests/test_resident_worker.py` + `tests/test_resolve_upload.py`, collected together so
  `test_resident_worker` sets up `sys.path` for `extract`/etc. first -- the collection-order dependency is
  pre-existing, not introduced by this change): `46 passed, 8 skipped in 51.16s`, rc 0. No pre-existing test broken.

## Mutant

Changed `receives >= RESOLVE_MAX_RECEIVES` to `receives > RESOLVE_MAX_RECEIVES` (worktree-only, never committed):
`test_gives_up_by_name_before_the_dlq` failed (`assert [] == ['rh-1']`) because at `receives == limit` the message
was kept instead of given up. Reverted to `>=` before any commit; re-ran all three criteria green again.

## Premise check

The cell's citations (`resident_worker.py` `RESOLVE_RETRY_VISIBILITY_S` at line 413, `poll_once` at line 416,
`intake/uploads.py` `_answer`'s `REDRIVE_SECONDS` redrive) matched the world at HEAD `52e63f09ee` closely enough to
act on directly; no surprise row filed.
