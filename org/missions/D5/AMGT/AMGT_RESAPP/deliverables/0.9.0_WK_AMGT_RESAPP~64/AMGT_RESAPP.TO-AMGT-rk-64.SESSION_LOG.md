# AMGT_RESAPP.TO-AMGT-rk-64 -- session log -- `0.9.0_WK_AMGT_RESAPP~64`

Worktree: `C:/tmp/wk-amgt-15-64` (branch `wk-amgt-15-64`, based at `0777e942ff`).

## What was found (re-measured, not inherited)

Re-derived the analysis row's claim independently before touching anything:
- `integrations/bloomberg/research/pull_consumer.py:99` (HEAD, pre-fix) called
  `mbp.stage_pull(blp, s3, ticker, pull_log)` -- 4 positional arguments.
- `integrations/bloomberg/research/model_block_pull.py:371` declares
  `def stage_pull(blp, s3, security: str) -> dict:` -- 3 positional parameters.
- AST walk confirmed `call_args == 4`, `def_params == 3` at HEAD (pre-fix), independent of the
  CVO's own citation (a different instrument -- static AST inspection run fresh by this worker).

## What was built

1. `integrations/bloomberg/research/pull_consumer.py` lines 97-99: deleted the dead
   `pull_log: dict = {"securities": [], "requests": []}` line and changed the call to
   `mbp.stage_pull(blp, s3, ticker)` (3 args, matching the signature). Nothing else in
   `process_one` moved; `stage_derive`'s call was already correct and is untouched.
2. `integrations/bloomberg/research/tests/test_pull_consumer_arity.py` -- new, permanent,
   fully offline regression file: `test_ast_call_arity_matches_signature` (the same static AST
   check the CVO used) and `test_process_one_reaches_stage_pull_without_arity_typeerror`
   (dynamic, fully in-memory fake s3/sqs + monkeypatched blp/stage_pull/stage_derive).

## Criteria run

- AC1 (pytest, offline): 2 passed, 0 failed.
- AC2 (independent AST re-derivation on this worker's own branch HEAD): `call_positional_args 3
  def_positional_params 3 match True`.
- AC3 (the ONE live act -- real SQS round trip on `opal-research-pull-requests` +
  synthetic S3 key `packs/ZZZTEST_US_Equity/status.json` in `opal-data-harvest`, run exactly
  once): `pre_queue_visible 0`, `received 1 of 1 expected`, `state LANDED`,
  `status_state LANDED reason_has_positional_argument False`, `synthetic_key_cleaned True`
  (verified in the same invocation via a `head_object` that raised), `post_queue_visible 0`.
  No residue left behind.

## Controls

- Mutant: re-derived the AST check against the OLD pre-fix bytes at `HEAD` (`git show
  HEAD:integrations/bloomberg/research/pull_consumer.py`, still carrying `call_args=4` because
  the fix is uncommitted at measurement time) vs the NEW committed-this-cell bytes: OLD
  `match False`, NEW `match True` -- FIRED-AS-EXPECTED.
- Determinism: `test_pull_consumer_arity.py` run twice in succession, both `2 passed`; AC3's
  live act was run exactly once per the order's own instruction (a repeat would be a second
  live act, which the order does not authorize).

## Bounds honored

No deploy, no vendor call, no real Bloomberg call (blp monkeypatched in-process throughout).
No DLQ/retry/unconditional-delete structure change. No alarm/monitor/SNS/SES/notification. No
push (LOCAL only, per LD-0522). Synthetic S3 key deleted and confirmed absent in the same AC3
invocation. No surprises encountered -- the measured state matched the order's citations
exactly at every checked line; no row filed.
