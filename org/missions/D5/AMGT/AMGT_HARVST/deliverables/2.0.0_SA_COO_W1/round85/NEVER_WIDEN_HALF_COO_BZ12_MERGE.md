# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-140-r85` (`HVST-bz-12`, the refresh is limited to wsj and barrons) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~23:0xZ. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s addendum to his bz-9 producer half (owed), at `ledger/NEVER_WIDEN_ROUND85_BZ9_MERGE_CTO_HALF.md` ADDENDUM 1.
**Relation to the bz-9 pair** (COO `a3eba883d4`, CTO `9eef371300`): this change only NARROWS what that pair signed. It adds no capability, no writer and no behaviour in the default (flag OFF) state.
**Why it exists:** row `AMGT_HARVST-D1-S16` (mine): the merged `--refresh-once` decided on the refusal class only, so a `bbg` job refused as expired would have spent its one refresh through the non-Dow-Jones branch of `SessionManager._refresh`, whose credential is `google/andrew-goldengate/credentials`.
Nothing fired: the flag is off and nothing is registered. Ruling (A) closes on `wsj` and `barrons`.

## THE ACT

ONE merge of branch `wk-AMGT_HARVST-140-r85` @e9b759200e (the worker's proof commit; the build is `cb4cdc7ad1`, on the local worktree `C:/dev/wk-harvst-140`) into `box/dell1` through `.tools/safe-merge.sh`, and nothing else. No scheduled task is registered, stopped or started, no sign-in is made.

## WHAT THE BRANCH CHANGES (read at signing, `git diff d1439782c7 e9b759200e`: 5 files, +228 -34)

- `lib/opal_data_harvest/backfill_driver.py` (+6 -2): one constant `REFRESH_PUBLISHERS = frozenset({"wsj", "barrons"})`, and `refresh_wanted()` also requires `pub in REFRESH_PUBLISHERS`. Nothing else in the driver changes: the class table, `note_refusal`, `spend_refresh`, the `drive()` loop and the CLI flag are untouched.
- `lib/opal_data_harvest/test_bz9_refresh_once.py` (+32 -32): the publisher name in the refresh arms moves from `sa` to `wsj` (the shared `drive_once()` default too, which also renamed it in two non-refresh arms; their assertions are unchanged). Read in the diff: only names and the strings that quote them changed.
- `lib/opal_data_harvest/test_bz9b_refresh_publishers.py` (3 tests): a loop over EVERY publisher of `credentials.PUBLISHERS` proves `wsj` and `barrons` make exactly one refresh and replay, and `sa`, `ft`, `bbg` make zero, print one `REFUSAL` line, do not replay, and stop the leg with the SAME lines as with the flag off; the constant equals exactly the two; a MUTANT with the constant widened to every publisher fails the loop for exactly `sa`, `ft`, `bbg`.
- **Re-run by this issuer in the worker's worktree:** AC1 `3 passed in 0.65s`; proof-of-spec-check VALID rc 0 with `--governing-order`. The worker reports AC2 `100 passed` and the full suite `4 failed / 826 passed / 3 skipped` against `4 failed / 823 passed / 3 skipped` before (the same four known failures). AC2 and the clean-checkout suite are re-run on the merged tree at the act (C-b).

## BLAST RADIUS

- **Writers, N = 1 per property.** `backfill_driver.py` and `test_bz9_refresh_once.py` are written by this branch only (of the local `wk-*` branches, this one differs from `HEAD` in them; counted at the act as C-e). No new writer of any checkpoint or record.
- **Running processes:** site Z's runner executes from the pinned worktree `wk-harvest-runner-pin-995adcaeaa`, which does not contain `--refresh-once`. Unchanged.
- **Default (flag OFF) behaviour:** identical to the bz-9 merge. **Flag ON (reached only by `HVST-bz-10`):** strictly narrower than the bz-9 merge: the refresh path is reachable for `wsj` and `barrons` only.
- **Not touched:** the installer, `cycle_runner`, `worker.py`, `transport.py`, Secrets Manager, any publisher, any scheduled task, silver, bronze, gold, S3.

## BOTH BRANCHES (the half is signed for BOTH or for neither)

- **Branch O (flag OFF):** no change from the bz-9 merge. **Branch R (flag ON):** NOT activated by this act; it is `HVST-bz-10`'s own pair, and it will name the account's readers (CloudTrail, 42 events, 29 `GetSecretValue`, all by IAM principal `Andrew_Berman`, `deliverables/2.0.0_SA_COO_W1/round85/DOWJONES_SECRET_TOUCHES_20261013.txt` @dd6c8e07ac).

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** The branch head is `e9b759200e`; a newer head is a new pair. **C-b.** On the merged tree: AC1 and AC2 of the order pass, and the full suite on a CLEAN checkout of the merge shows the same four failures as the base and no new one. **C-c.** The merge lands through `safe-merge.sh` with its guards on; a conflict is a stop.
- **C-d.** The order's proof instance reads VALID with `--governing-order` at the merged tree before the flip (it does, in the worktree, as of signing). **C-e.** Denominator printed at the act: how many local `wk-*` branches differ from `HEAD` in the two lib files.

## ROLLBACK

Revert the merge commit on `box/dell1` (a new commit, no rebase). Nothing served has moved. A revert restores the bz-9 behaviour, which is why `bz-10` is NOT sent until this merge has landed.

## VERDICT: SIGNED (COO). Not started until the CTO's addendum is on file.
