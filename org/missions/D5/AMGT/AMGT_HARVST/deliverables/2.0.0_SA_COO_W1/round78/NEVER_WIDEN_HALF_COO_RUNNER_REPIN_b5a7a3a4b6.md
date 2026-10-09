# NEVER-WIDEN -- COO HALF: re-pin site Z's FWD-18 cycle runner from c1be67f53c to b5a7a3a4b6 (bv-1 merged)

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-09 ~18:0xZ, on `1.0.0_SA_CTO~DELL1` msg 2937 (round-78 analysis, item 1). **Pairs with:**
`1.0.0_SA_CTO~Z`'s site-Z half (owed). **Actor:** `0.7.0_AE_CloudOps~ZW`, by order
`task-orders/AMGT_HARVST.TO-HVST-bw-1.the-runner-repinned-to-the-bv1-merge.md` (round 79).

## THE ACT (site Z box, once)

1. `git worktree add --detach <workspace-parent>\wk-harvest-runner-pin-b5a7a3a4b6 b5a7a3a4b6`. The `wk-` prefix keeps the
   reaper away.
2. `Stop-ScheduledTask -TaskName 'Opal Data Harvest - Continuous Cycle'`. Confirm the runner process (PID 10928 at 14:46Z) is
   gone.
3. `install-cycle-schedule.ps1 -RepoRoot <new pin> -Publishers bbg,wsj,barrons -StateDir <old state> -RuntimeRoot <old runtime> -Plan`, read; then the same command without
   `-Plan`, once, and `Start-ScheduledTask`, once.
4. Leave the old pinned worktree in place. It is the rollback, and its state dir holds the cycle records so far.

## THE PIN

b5a7a3a4b6 is the merge of HVST-bv-1 into `box/dell1`, under the pair COO @8ccf65f68c and `1.0.0_SA_CTO~Z` @e3f030ba85. Ledger
`harvst-bv1-merge-20261009` is CLOSED @fbf1b8c948. It is on CLOUD (is-ancestor read 17:47Z).

## THE STATE DIR (RULED by the issuer: option (b))

The new pin starts with an EMPTY state dir unless the cut says otherwise. Then bbg's next cycle floors at yesterday, and the
3 failed keys of cycle 20261009T085753Z are not re-queued, because re-queue reads that pin's own records. The cell names one
of two options:
- (a) start fresh, accepting the floor at yesterday;
- (b) pass `--state-dir` at the old pin's state dir, so cycle history and re-queue carry over.
RULED (b): the new pin runs with `-StateDir "<old>\.runtime\harvest-cycle\state" -RuntimeRoot "<old>\.runtime\harvest-cycle\runtime"`.
One state dir across pins: it is the runner's own durable record, and re-queue depends on it.

## BLAST RADIUS

- The scheduled task's action and working directory move to the new pin. That is the only writer of the task.
- From the next cycle, a pair error no longer stops a publisher (5 consecutive still do), failures carry their detail, and
  the runner writes `<state-dir>/cycle_runner.log`.
- Silver writers stay N = 1 (the collector). Publishers stay bbg, wsj and barrons. sa, the FT, gold and `config.json` are
  not touched.

## CONDITIONS (each checked at the act, not assumed)

- **C-a.** `git -C <new pin> rev-parse HEAD` reads b5a7a3a4b6, with a positive control on the old pin.
- **C-b.** The `-Plan` read shows ACTION `--publishers bbg wsj barrons`, WORKDIR the new pin, and `--state-dir` as the cell
  names it.
- **C-c.** No other runner or `backfill_driver` process is alive after step 2. The census carries a positive control.
- **C-d.** A ledger entry is opened before step 2 and closed after the first cycle record under the new pin.
- **C-e.** `1.0.0_SA_CTO~Z`'s C-e for the bv-1 merge (site Z's census before its box-sync) is read first; the new pin is a
  worktree at a commit, so the shared tree's content does not move it.

## ROLLBACK

Stop the task, then re-run the installer against the old pin `wk-harvest-runner-pin-c1be67f53c` and start it once.

## VERDICT: SIGNED (COO), pending `1.0.0_SA_CTO~Z`'s half
