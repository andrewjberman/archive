# IB-mr-221 (round 22, ~M) -- AD-10: every DirectoryEntry carries each account's own mask

TO `IRPT_BCKEND.TO-IB-m22-221`, worker `0.9.0_WK_IRPT_BCKEND~75`, worktree `wk_irpt_bckend_75`, branch
`wk-IRPT_BCKEND-75` on `CLOUD@70b36eec24`.

## What was built

1. `docs/contracts/investor-reporting/v1/DirectoryEntry.schema.json` gains an ADDITIVE, OPTIONAL property
   `account_masks`: an array of `{"account_id", "masked_discriminator"}`, one per account in
   `ids.account_ids` and in the same order. `masked_discriminator` (the entry-level field, head row) is
   UNCHANGED.
2. `data/assets/scripts/gold/investor_reporting/directory_runner.py`'s `_entry()` now builds `account_masks`
   from EVERY account row with the existing `masked_discriminator()` function, deduped the same way
   `ids.account_ids` is (one item per unique opaque account id, first row wins, order preserved).
3. New pure-fixture tests: `data/assets/scripts/gold/investor_reporting/tests/test_directory_account_masks.py`
   (9 tests) -- multi-account entries get one mask per account in order, the masks are distinct and carry
   each account's own tail (the CRO's exact measured shape: `****9079/IRA` + `****3302/JOINT` instead of one
   repeated), the head `masked_discriminator` is unchanged, the account-only path (a different code branch in
   `build_inf`) also carries `account_masks`, no mask exceeds 4 digits, the property validates against the
   edited schema, and a document with no `account_masks` at all still validates (additive).
4. Real local builds, no upload, all three firms, at each firm's own latest complete business date
   (`directory_runner.py --firms all --dry-run --local-out`): 49F (7,598 accounts across 4,642 entries,
   1,945 multi-account), INF (884 accounts / 298 entries, 205 multi-account), COT (953 accounts / 263
   entries, 180 multi-account). Summarized in
   `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R22_AD10_ACCOUNT_MASKS_SUMMARY_20260929.json`.
5. `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/NEVER_WIDEN_HALF_REQUEST_DIRECTORY_AD10_20260929.md` --
   the readers census (`directory_runner.py`'s own pre-flight validator, the Lambda's `entry.py`/`handler.py`,
   the portal's `directory-browse.ts`/wire types/adapt.ts/picker+identity components) and the release order
   (handlers' contract copy first, then the directory bundle re-mint, then the portal reading the field).

## The real conflict found and recorded, not fixed here

`directory_runner.py`'s own `validate_entries()`/`main()` validate every built entry against the DEPLOYED
Lambda's packaged contract copy (`infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json`,
`CONTRACT_PATH`), which is out of this order's `<paths>` grant to edit. The moment `_entry()` emits
`account_masks` (required by Build step 2), that copy's `additionalProperties: false` rejects every entry:
the pre-existing test `test_inf_entries_validate_against_the_contract`
(`data/assets/scripts/gold/investor_reporting/tests/test_directory_runner.py:159-162`) goes red, and a real
`python directory_runner.py` run returns rc=1 with a schema ERROR line per entry -- measured on this session's
real local build (`valid=0 of <entry_count>` at all three firms). Filed as
`IRPT_BCKEND-W75-S1` (ARMED, disarm owner `2.0.0_SA_COO~P`, the release order's first step). Not remediated
here: the Lambda contract copy is explicitly named as not this order's to edit, and widening the grant to fix
it would be the widening the order forbids.

## Acceptance

- **AC1**: `python -m pytest data/assets/scripts/gold/investor_reporting/tests/test_directory_account_masks.py -q -p no:cacheprovider` -> `9 passed`.
- **AC2**: `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R22_CHECKS/r22_ad10_masks.py` -> `AD10-MASKED 49financial=7598 inflection=884 cottonwood=953`, rc=0.
- **AC3**: `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R20_CHECKS/r20_half_ready.py org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/NEVER_WIDEN_HALF_REQUEST_DIRECTORY_AD10_20260929.md` -> `HALF-READY NEVER_WIDEN_HALF_REQUEST_DIRECTORY_AD10_20260929.md`, rc=0.

## Controls

- **Mutant** (worktree-only, reverted before commit, never landed): the `account_masks` loop's row-level
  `masked_discriminator(row.get(...), row.get(...))` call changed to `head.get(...)`, reproducing the ORIGINAL
  defect (every account in a multi-account entry reads the head row's mask). Fired as expected:
  `test_multi_account_entry_masks_are_distinct_and_carry_each_accounts_own_tail` FAILED
  (`'****9079 / IRA' == '****3302 / JOINT'`), the other 8 tests stayed green. Reverted; `diff` against the
  pre-mutation copy showed zero difference; the suite re-ran `9 passed` after revert.
- **Determinism**: the 9-test file run twice at final bytes -- `9 passed in 1.65s` then `9 passed in 1.33s`
  (and a third confirmatory `9 passed in 1.61s`) -- identical pass/fail shape each time.
- **Regression**: full `data/assets/scripts/gold/investor_reporting/tests` directory run: `1 failed, 311
  passed` -- the ONE failure is the documented, out-of-lane Lambda-contract-copy conflict above (row
  `IRPT_BCKEND-W75-S1`); no other test moved.

## Surprises

- `IRPT_BCKEND-W75-S1` (OBSERVATION, ARMED) -- the Lambda contract copy conflict above.
