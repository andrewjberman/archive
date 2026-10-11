# irpt-ycharts-generate: what IRPT_ANLREQ round 3 changed in it (cell AR-y-37) -- census line for IRPT_BCKEND's release

For `2.0.0_SA_COO~P2`, who releases the function by CTO ruling (`1.0.0_SA_CTO~DELL2` msg 4622). By `2.0.0_SA_COO~Y2`, 2026-10-11.
This seat cuts nothing on the function. Every line is this seat's own read of the shared tree at `d6d7bb5a84` unless it says otherwise.

## The two product files (commit `2f7cc7be42`, worker `0.9.0_WK_IRPT_ANLREQ~54`, merged `92af9db9b2`)

| file | change | served effect when it lands in irpt-ycharts-generate |
|---|---|---|
| `ycharts/generate/acceptance.py` | `DynamoAcceptance.accept(...)` takes a REQUIRED keyword `acting_principal_id`; a non-string or empty value refuses `ACTING_PRINCIPAL_REQUIRED`; a NEW acceptance record stores the field; a prior record is returned exactly as stored | CHANGES A WRITTEN RECORD: every newly accepted analysis request carries `acting_principal_id`. No existing record is rewritten |
| `ycharts/generate/submission_service.py` | the one call of `accept` passes `acting_principal_id=principal["principal_id"]` (line 148) | the verified submitter is what is recorded; it is never read from the browser body |

**The two must land together.** `acceptance.py` alone, with the old `submission_service.py`, raises a `TypeError` on every submission
(a required keyword is missing). A re-pin that moves one and not the other breaks acceptance.

**Callers of `.accept(` outside tests under `infra/aws/lambda/investor-reporting`: 2 lines in 2 files** (native search over every
non-test `.py` there). One is `submission_service.py:145`, above. The other is `export/entry.py:364`, which calls `_async.accept`, a
different function. `custody_submission.py` constructs `DynamoAcceptance` and has no `.accept(` call.

## Readers of the new field

- `intake/uploads.py:267` writes the same field name onto the upload's original record. That line is NOT this cell's (commit `2f7cc7be42` does not touch the file)
  and its owning commit was not read here; which function packages it was not read either.
- In irpt-status the new `acceptance.py` is INERT: 0 `.accept(` call sites in its 49 packaged modules (measured on the release 5 zip,
  build `Iw3FADFr`); its public projection returns identity and `accepted_at` only (worker `0.9.0_WK_IRPT_ANLREQ~53`'s reading, inferred).
- Reader census INHERITED from the cell's own report and not re-run here: 19 readers of the acceptance record, 0 with a closed key set.

## After-read this seat suggests for the generate pair

One fresh accepted request through the real submission path: its acceptance record carries `acting_principal_id` equal to the verified
submitter's principal id; one request accepted BEFORE the apply reads back byte-equal (no field added). Tests that pin both:
`ycharts/generate/tests/test_acceptance_actor.py` (in the generate folder's 497 passed at the merged state, two consecutive full runs).

## Not this cell's

Row `IRPT_ANLREQ-D2-S39`: the function's five disagreeing digests and its 23 of 88 pinned members older than HEAD. The base is not ruled.
