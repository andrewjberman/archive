# TO-DQ-t18: incompatible row-count requirements

**Seat:** 0.7.0_AE_CloudOps~ZQ. **Order pin:** 73cae9cfe68cbc45a358da63a026eb431920da60. **State:** pending; refusal clause exercised before implementation or activation.

Build item 2 requires one `bbgtml-unmetered` row for a day without `bbgtml-*` lines. Build item 3 requires `test_demque_bbg_ledger_upload.py` to keep passing. The write grant excludes that test file and explicitly says everything else is read-only.

The existing test fixtures all lack `bbgtml-*` lines. Three tests assert exact output cardinality:

| Existing test | Assertion | With required extra row |
|---|---|---|
| `test_reads_record_lines_and_converts_rows_to_cells_per_mode` | cells exactly `[48,64,5,14,2]`, and all claims held | extra `None` cell and absent claim |
| `test_unknown_mode_is_written_with_claim_absent_not_defaulted` | four uploaded rows | five uploaded rows |
| `test_rerun_of_a_day_is_idempotent` | two lines after changed-source overwrite | three lines |

## Measured preflight

An uncommitted scratch probe, `.scratch/demque-zq-t18-compatibility.py`, wraps `rows_for_day` **in process memory only**, adding the mandated row to nonempty days without meter lines, then runs the five existing tests with their S3 stub and temporary ledger fixtures. No production file, AWS object, task or notebook is changed or run.

Output: `3 failed, 2 passed in 0.55s`, exit 1. Deciding failures: extra `None` in the cells list; `assert 5 == 4`; `assert 3 == 2`.

Unmodified baseline immediately afterward: `5 passed in 0.67s`, `UPL-OK`, exit 0. The mutation existed only in the completed probe process.

This cannot be solved by adding the row only in CLI: the old tests also assert the uploaded object's row counts. Silencing the sentinel under pytest, only for fixtures, or for library callers would hide the new contract from the tests. No such exception is specified.

## Issuer action needed

Amend the grant to include `data/mdpf/scripts/demque/test_demque_bbg_ledger_upload.py` and allow its cardinality expectations to include exactly one absent sentinel while preserving all original conversion, dry-run and idempotence assertions. Alternatively, amend item 2 to specify a different interface/condition for the sentinel. The assignee has not amended the order or tests.

Surprise row: `MDPF_DEMQUE-Z-W1-S3`, BLOCKING, in the named investigation file. The row uses the issuer-required coordinate; the same documented audited override used for S1/S2 is needed because this named seat is not a numeric worker.

## Current state and next steps

No meter implementation or production `.cmd` change has begun. The 07:00 task, notebooks, uploader source and IAM remain unchanged by this order. The next scheduled run's metering requirement is unfulfilled; the order stays open. Resume after issuer amendment, then implement and test, obtain the named site-Z CTO half, activate within the change-management entry, and read the scheduled run's real ledger lines before completing.

## Compiler Tools

`comp-which` routed exact file reads to native Read/comp-read. Read the current AGENTS mission-tree authorization, exact order, acceptance helpers, runner and old test assertions. No dependency change or production execution was attempted. Local records only; no push.
