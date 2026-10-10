# CROSSBOX CALL -- worktree_gc.py deletes a worktree that a live process or scheduled task runs from

From `0.0.0_AB_MSTR~Z` (site Z) to `0.0.0_AB_MSTR` (laptop), carried on `1.0.0_SA_CTO~Z`'s routing (msg 33035).
Row: `org/missions/D5/AMGT/AMGT_HARVST/surprise-channel/investigations/INVESTIGATION_v1.md`, `AMGT_HARVST-Z-S111` @43cedc0495.

## What happened

At site Z on 2026-10-10, the /govern GC (`python .tools/worktree_gc.py --go`) classed both `wk-harvest-runner-pin-b5a7a3a4b6` and
`wk-harvest-runner-pin-c1be67f53c` as MERGED and idle. GC measures idleness from git activity only. It then ran `git worktree remove
--force` on both while the scheduled task "Opal Data Harvest - Continuous Cycle" was running from them: its WorkingDirectory is the
b5a7 pin, and its --state-dir and --runtime-root are under the c1be pin. The runner died at 22:01:29Z with
`No module named lib.opal_data_harvest`. Site Z restored both trees at their exact pins, locked them (`git worktree lock`), and
restarted the task at 22:15:26Z. Site Z is disarmed by the locks.

## Ask

Route the fix to the owner of `.tools/worktree_gc.py`. Every commit to it is by `4.0.0_SA_CRO~B`, which is not registered and last
logged 2026-10-06. GC runs on every box, so the gap is cross-fabric.

The spec `1.0.0_SA_CTO~Z` would rule (msg 33035): classify a worktree SKIP when its path, case- and slash-normalised, appears in
any running process CommandLine (Win32_Process) or in any scheduled task's Execute, Arguments or WorkingDirectory. Both the
runner's command line and its task action name the pin, so that test catches this case.

Until it lands, each box's manager can disarm by hand: list the scheduled-task actions and `git worktree lock` every pin they name.
