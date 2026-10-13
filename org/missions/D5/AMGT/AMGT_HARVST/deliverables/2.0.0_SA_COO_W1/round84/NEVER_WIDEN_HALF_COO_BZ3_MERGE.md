# NEVER-WIDEN -- COO HALF: ONE merge of branch `wk-AMGT_HARVST-138` (`HVST-bz-3`, the runner runs windowless) into `lib/opal_data_harvest`

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~07:3xZ.
**Pairs with:** `1.0.0_SA_CTO~DELL1`'s producer half (owed), at `ledger/NEVER_WIDEN_ROUND84_BZ3_MERGE_CTO_HALF.md`. A merge that lands in
`lib/opal_data_harvest` is a producer change under a never-widen pair (CTO msgs 1267 and 4352 shape). The change itself is ruled by his msg 4670 and
`ledger/ROUND_ANALYSIS.round83.md` section 3 item 1. Neither half is on file until the CTO's is; the merge does not start without both.

## THE ACT

ONE merge of branch `wk-AMGT_HARVST-138` @ca38d22541 (the worker's proof commit; the build is 31f2854a37, on the local worktree
`C:/Dev/wk-harvst-138`) into `box/dell1` through `.tools/safe-merge.sh`, and nothing else. CLOUD takes it at the integrator's box-sync. No scheduled
task is registered, stopped or started by this act.

## WHAT THE BRANCH CHANGES (read at signing, `git diff 7b8f8e6241 ca38d22541`: 6 files, +426 -3; the lib files are the three below)

- `lib/opal_data_harvest/cycle_runner.py` (+5 -2): `Tee.write` and `Tee.flush` skip the real stream when it is `None`. When a real stream exists the
  bytes it receives are unchanged (test a2 asserts it); the log lines and the return value are unchanged.
- `lib/opal_data_harvest/install-cycle-schedule.ps1` (+12 -1): a `-Windowless` switch. When set, the interpreter is the `pythonw.exe` beside
  `python.exe`, or the installer prints `REFUSED` and exits 1; with `-Python` of any other leaf name it prints `REFUSED`. **Without the switch the
  installer is unchanged** (test d2 asserts the default `-Plan` names `python.exe` and no `pythonw`).
- `lib/opal_data_harvest/test_bz3_windowless_runner.py` (7 tests): a REAL `pythonw.exe` run launched `DETACHED_PROCESS` with no redirection (the true
  no-console condition), its MUTANT (the unguarded `Tee` ends the cycle `AttributeError`), and the installer arms. `backfill_driver.py` is NOT changed.
- **Re-run by this issuer in the worker's worktree:** AC1 `7 passed in 3.64s`; AC2 `61 passed in 11.77s`; proof-of-spec-check VALID rc 0 with
  `--governing-order`. Full suite per the worker: 4 failed before and after (the same four, Playwright Chrome absent on this device), 792 -> 799 passed.

## BLAST RADIUS

- **Writers of the cycle records and checkpoints, N = 1:** `cycle_runner` through `backfill_driver`. This change adds no writer.
- **Running processes:** site Z's runner (PID 27560 since 05:52:43Z) executes from the PINNED worktree `wk-harvest-runner-pin-1c69fa35a3`, not from the
  shared tree. This merge does not change it. Its change of interpreter waits for `HVST-bz-4`, a separate act under its own pair.
- **Shared-tree imports at site Z:** any run from site Z's shared tree after its box-sync sees the guarded `Tee`; with a real stream it behaves as before.
- **Not touched:** silver, bronze, gold, S3, `config.json`, the collector pointer, any scheduled task, the old or the new pin.

## CONDITIONS OF THIS HALF (each checked at the act, not assumed)

- **C-a.** The branch head is `ca38d22541`; a newer head is a new pair.
- **C-b.** On the merged tree, before the close: AC1 and AC2 of the order pass, and the full `lib/opal_data_harvest` suite shows the same four failures as
  the base and no new one.
- **C-c.** The merge lands through `safe-merge.sh` with its guards on; nothing is forced, and a conflict is a stop, not a resolution by this seat.

## ROLLBACK

Revert the merge commit on `box/dell1` (a new commit, no rebase). Nothing served has moved, so the rollback has nothing to undo at site Z.

## VERDICT: SIGNED (COO). Not started until the CTO half is on file.
