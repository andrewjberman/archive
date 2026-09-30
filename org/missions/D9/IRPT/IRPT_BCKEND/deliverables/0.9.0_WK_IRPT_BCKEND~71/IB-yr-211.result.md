# IB-yr-211 result -- resolve_upload RETRY logged and re-offered soon

Worker: 0.9.0_WK_IRPT_BCKEND~71. TO: `IRPT_BCKEND.TO-IB-yr-211.resolve-retry-logged-and-reoffered-soon`.

## Build

In `infra/aws/lambda/investor-reporting/ycharts/generate/resident_worker.py`:

1. Added module constant `RESOLVE_RETRY_VISIBILITY_S = 60` immediately before `poll_once`.
2. In `poll_once`, the decoded message body is now held in `decoded` (previously inlined into the
   `assembly.execute(...)` call). After `result = assembly.execute(decoded, heartbeat)`, when
   `decoded.get("kind") == "resolve_upload"`, prints exactly one line
   `IRPT_RESIDENT_RESOLVE state=<state> code=<code>` (flush=True), and when `result["state"] == "RETRY"`
   calls `sqs.change_message_visibility(QueueUrl=queue_url, ReceiptHandle=envelope["ReceiptHandle"],
   VisibilityTimeout=RESOLVE_RETRY_VISIBILITY_S)` as the last visibility change made for that message
   (no heartbeat/900s change follows it in this code path).
3. `analysis_generate` messages (`decoded.get("kind") != "resolve_upload"`) print no new line and receive
   no new visibility change -- the guard is an `if`, not a branch that alters the existing delete logic.
4. No existing test file was changed. No test was added to `test_resolve_upload.py` (see
   `declared_exclusions` in the proof-of-spec instance) -- the read-only R20_CHECKS harness already
   exercises both new behaviours end to end.

## Acceptance runs

- `Y21-1-AC1`: `python -m pytest -q -p no:cacheprovider org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/R20_CHECKS/test_r20_y2_resolve_retry.py::test_retry_is_logged_and_reoffered_soon` -> `1 passed in 2.00s`.
- `Y21-1-AC2`: `python -m pytest -q -p no:cacheprovider org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/R20_CHECKS/test_r20_y2_resolve_retry.py::test_ready_still_deletes_and_is_logged` -> `1 passed in 1.64s`.

## Regression

Full `infra/aws/lambda/investor-reporting/ycharts/generate/tests/` directory run: `290 passed, 30 skipped,
32 subtests passed in 80.63s` -- identical pass/skip counts to the pre-existing baseline shape (matches the
prior IB-yr-201 result's own full-directory run), no regression from this change.

## Controls

Mutant: temporarily reverted the `if result["state"] == "RETRY":` visibility-change call to a no-op (commented
it out) and reran AC1 -- it failed on `assert queue.visibility and queue.visibility[-1] == short` because
`queue.visibility` stayed empty. Restored the exact original bytes afterward (`git hash-object` reproduced the
same blob hash as the delivered artifact).

Determinism: ran the full `test_r20_y2_resolve_retry.py` file twice in succession at the final bytes -- both
runs `2 passed` with identical timing shape and identical pass/fail outcome.
