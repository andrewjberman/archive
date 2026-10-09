# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-133-r78` (`HVST-bv-1`) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~16:4xZ.
**Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed). Under `1.0.0_SA_CTO~DELL1` msg 1267, a merge that lands in
`lib/opal_data_harvest` is a site-Z deploy under a never-widen pair, and `1.0.0_SA_CTO~Z`'s half is signed before the merge.
`1.0.0_SA_CTO~DELL1` msg 2724 rules the change itself.

## THE ACT

One merge of branch `wk-AMGT_HARVST-133-r78` @4b0475b646 (on origin) into `box/dell1` through `.tools/safe-merge.sh`, and
nothing else. CLOUD takes it at the integrator's box-sync, and site Z takes it at its own box-sync.

## WHAT THE BRANCH CHANGES (read at signing, `git diff 878f9466df 4b0475b646`: 5 files, +567 -27; the lib files are the three below)

- `lib/opal_data_harvest/backfill_driver.py`: `--continue-on-pair-error [0|1]`, default 0. Under 1, a pair job returning
  `error` is a failed pair and the leg goes on. `MAX_CONSECUTIVE_PAIR_ERRORS = 5` errors in a row stop the publisher with
  `stopped: "error: <detail>"`. Retry and gave-up entries keep the job's `detail`. `drive`'s `out` resolves at call time.
  Without the flag, behaviour is unchanged (`test_ae4`, `test_ba1` and `test_br2` pass unchanged: 53 passed).
- `lib/opal_data_harvest/cycle_runner.py`: passes the flag as `1`. The cycle record gains `failures` and (AMENDMENT 1)
  `requeued`. A cycle is `completed` when every pair was reached and nothing stopped it. Failed pairs are re-asked next
  cycle with their failed window: `requeue_floors` reads the newest cycle record's failures and passes `--pair-floors <file>`
  to the driver, which runs each such key with its own `--floor`. The runner appends its output to `<state-dir>/cycle_runner.log`.
- `lib/opal_data_harvest/test_bv1_cycle_continues_past_pair_errors.py` (10 tests, 2 mutants), plus the proof and rows
  D1-W133-S1/S2.
- Re-run by this issuer on the branch: AC1 `10 passed`, AC2 `53 passed`, proof-of-spec-check VALID rc 0. Full suite per the
  worker: 4 failed (the same 4 as the base), 781 passed.
- Residual stated in row D1-W133-S2: re-queue reads only the newest cycle record, so a pair owed from cycle N that a
  STOPPED cycle N+1 never reached is asked in N+2 with the unmoved floor rather than its own. This goes to the round-78
  analysis.

## BLAST RADIUS

- **Writers of the cycle records and checkpoints, N = 1:** `cycle_runner` through `backfill_driver`.
- **Running processes:** site Z's runner (PID 10928 at 14:46Z) runs from the PINNED worktree
  `wk-harvest-runner-pin-c1be67f53c`, not from the shared tree. This merge does not change it. Its change of behaviour waits
  for a re-pin, which is a separate act under its own pair. The r47 driver had exited (JOB-EXIT rc=0, CLEARED).
- **Shared-tree imports at site Z:** any `backfill_driver` leg run from site Z's shared tree after its box-sync would see the
  new code. Without `--continue-on-pair-error` its behaviour is unchanged except that `detail` is kept and output resolves
  at call time.
- **Not touched:** silver, bronze, gold, S3, `config.json`, the collector pointer, any scheduled task.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** The branch head is the one named above; a newer head is a new pair.
- **C-b.** On the merged tree, before the close: AC1 and AC2 of the order pass, and the full `lib/opal_data_harvest` suite
  shows the same 4 base failures and no new ones.
- **C-c.** A ledger entry is opened before the merge and closed after C-b (NEVER-2).
- **C-d.** No `backfill_driver` leg is running from site Z's shared tree at the merge. This is read through
  `0.0.0_AB_MSTR~Z` or `0.7.0_AE_CloudOps~ZW` as a process census with a positive control.

## BOTH BRANCHES

- **C-b holds:** bv-1 closes. The re-pin of site Z's runner to the merge commit is cut as its own act and pair.
- **C-b fails or the merge conflicts:** the merge is reverted the same session with a new commit (never a rebase), and the
  revert is read back by AC2.

## ROLLBACK

`git revert -m 1 <merge>` on `box/dell1`. The integrator carries it to CLOUD and site Z as it carried the merge. No pinned
process runs the merged code until the re-pin.

## EXCLUDED

No runner re-pin, task change, collector or backfill run, or S3 write.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~Z`'s half
