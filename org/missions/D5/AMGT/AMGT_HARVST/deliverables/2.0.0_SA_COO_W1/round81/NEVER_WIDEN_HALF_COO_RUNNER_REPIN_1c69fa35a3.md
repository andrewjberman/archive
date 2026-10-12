# NEVER-WIDEN -- COO HALF: re-pin site Z's FWD-18 cycle runner from b5a7a3a4b6 to 1c69fa35a3 (bx-3 merged), HVST-by-3, round 81

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-12 ~14:2xZ, on `1.0.0_SA_CTO~DELL1` msg 4394 ("the site Z runner re-pin as a crossbox ORDER
through MSTR"). **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (owed). **Actor:** `0.7.0_AE_CloudOps~ZW`, by order
`task-orders/AMGT_HARVST.TO-HVST-by-3.the-runner-repinned-to-the-bx3-merge.md`, delivered as a crossbox ORDER. The model is round
79's pair (`round78/NEVER_WIDEN_HALF_COO_RUNNER_REPIN_b5a7a3a4b6.md`), which `~ZW` executed.

## THE ACT (site Z box, once)

1. Wait for the current cycle to end by the runner's own stop file (C-f); delete the stop file before the restart (C-g).
2. `git worktree add --detach <new> 1c69fa35a3`; lock `<new>` and the rollback pin `<old>` (`git worktree lock`).
3. Stop the task, census (NONE), run the installer `-Plan`, read it, run it once with `-StateDir` and `-RuntimeRoot` as they are, start once.
4. A kill-maint DRY RUN lists the new runner `EXEMPT`.

## THE PIN

`1c69fa35a3` is the merge of `HVST-bx-3` on `box/dell1` (worker ~135 @4b549b166b, proof VALID rc 0, 11 and 63 passed) and holds
bx-1 (the enqueue fence) and bx-2's record as well, which the runner does not execute. It is on `box/dell1` only at the issuance;
the order's START CONDITION reads it on `origin/CLOUD` at the site Z box before anything is touched.

## THE STATE DIR (RULED, as in round 79)

One state dir across pins: it is the runner's own durable record, and re-queue of the previous cycle's failed pairs reads it. The
new pin runs with the task's current `--state-dir` and `--runtime-root`, unchanged.

## BLAST RADIUS

- The scheduled task's action and working directory move to the new pin. That is the only writer of the task.
- From the next cycle a failed pair's `detail` names its reason (class and vendor message, redacted, at most 303 characters).
  Nothing else in the record changes; a success row is byte-identical (bx-3's test).
- Publishers stay bbg, wsj and barrons. sa, the FT, gold, silver and `config.json` are not touched. Silver writers stay N = 1.
- The runner's cycle in progress is NOT killed; it ends by its stop file first.

## CONDITIONS (each checked at the act, not assumed)

- **C-a.** `git -C <new> rev-parse HEAD` reads 1c69fa35a3, with a positive control on `<old>`.
- **C-b.** The `-Plan` read shows `--publishers bbg wsj barrons`, WORKDIR `<new>`, and `--state-dir` unchanged.
- **C-c.** No other runner or `backfill_driver` process is alive after the stop (positive control printed).
- **C-d.** A ledger entry is opened before the stop and closed after the first cycle record under the new pin.
- **C-e.** `<new>` and `<old>` read `locked` in `git worktree list --porcelain` (row Z-S111: the GC removed unlocked pins under a live runner).
- **C-f.** The stop file ends the cycle; **C-g.** it is deleted before `Start-ScheduledTask`.

## ROLLBACK

Stop the task, re-run the installer with `-RepoRoot <old>` and the same state flags, start once. `<old>` stays, locked.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~DELL1`'s half
