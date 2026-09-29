# IB-mr-221 -- amendment 3 (Holdings labels + four-step release order), 0.9.0_WK_IRPT_BCKEND~78

Reopened slot for TO IRPT_BCKEND.TO-IB-m22-221 amendments 1-2. The first build
(0.9.0_WK_IRPT_BCKEND~75, branch `wk-IRPT_BCKEND-75` @4ecbaca410) is already merged into this
worktree (drain `38061b8839`); its directory-runner `account_masks` field, schema edit, 9 tests,
per-firm summary and half are unchanged here except where amendment 3 names an edit.

## What this slot did (amendment 3 steps 1-3)

1. **Holdings labels** (amendment 2 step 6): `data/assets/scripts/gold/investor_reporting/holdings_snapshot.py`
   `_directory_account_labels` (~:714-744) now reads each entry's `account_masks` array when present
   (`account_id` -> its own `masked_discriminator`) and falls back to the entry's one
   `masked_discriminator` for every account under it when `account_masks` is absent -- so a build
   against today's served directory (no `account_masks` field yet) is byte-for-byte unchanged.
   Docstring corrected to state the per-account read and the fallback, replacing the old "its
   accounts share its discriminator" claim (that claim is now only the FALLBACK, not the rule).
   Two new tests added to `tests/test_directory_account_masks.py`
   (`test_directory_account_labels_gives_each_account_its_own_mask_when_entry_carries_account_masks`,
   `test_directory_account_labels_falls_back_to_the_entry_mask_when_account_masks_is_absent`), each
   exercising `_directory_account_labels` directly against a stub S3 client (`_FakeDirectoryS3`,
   `_FakeDirectoryBody`) carrying a constructed directory document -- no AWS call. 9 tests -> 11.

2. **Half's release order rewritten to four steps** (amendment 3 step 2), replacing the earlier
   three-step order superseded by amendments 1-2:
   (1) handlers' `_contracts` copy (2.0.0_SA_COO~P cutting it now);
   (2) portal reader on PROD (`directory-browse.ts` accepting `account_masks`; already true on
   portal DEV `27eae57a`, carried in the pending PROD hotfix -- PROD itself unmoved);
   (3) directory bundle re-mint;
   (4) Holdings re-mint AFTER the directory re-mint, so `_directory_account_labels` finds
   `account_masks` in the landed directory.
   Readers census gained two rows: `holdings_snapshot.py` `_directory_account_labels` (landed this
   slot) and portal `IdentityCard.tsx:176-185` `accountListFromSnapshot` (no code change needed --
   it already reads `display.label`; inherits the per-account mask once fed a re-minted snapshot).
   The `directory-browse.ts` row updated to state the DEV/PROD split instead of a flat REJECT.

3. Re-ran AC1-AC3 (all PASS, see proof instance), re-ran the full
   `data/assets/scripts/gold/investor_reporting/tests` suite: 313 passed, 1 known-red
   (`test_inf_entries_validate_against_the_contract`, row `IRPT_BCKEND-W75-S1`, disarm owner
   `2.0.0_SA_COO~P` -- not re-filed, as instructed).

## Not touched

`directory_runner.py`, `DirectoryEntry.schema.json`, the per-firm summary JSON, and
`INVESTIGATION_v1.md` are byte-identical to ~75's build (git hash-object matches: `36cc82cf...`,
`27d9a8f7...`, `c0730c45...`, `5fed15e1...` respectively) -- amendment 3 named no edit to them.

## Commands run (verbatim, see proof instance `compiler_tools` for the full list)

- `python -m pytest data/assets/scripts/gold/investor_reporting/tests/test_directory_account_masks.py -q -p no:cacheprovider` -> `11 passed`
- `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R22_CHECKS/r22_ad10_masks.py` -> `AD10-MASKED 49financial=7598 inflection=884 cottonwood=953`
- `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R20_CHECKS/r20_half_ready.py org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/NEVER_WIDEN_HALF_REQUEST_DIRECTORY_AD10_20260929.md` -> `HALF-READY NEVER_WIDEN_HALF_REQUEST_DIRECTORY_AD10_20260929.md`
- `python -m pytest data/assets/scripts/gold/investor_reporting/tests -q -p no:cacheprovider` -> `1 failed, 313 passed`
