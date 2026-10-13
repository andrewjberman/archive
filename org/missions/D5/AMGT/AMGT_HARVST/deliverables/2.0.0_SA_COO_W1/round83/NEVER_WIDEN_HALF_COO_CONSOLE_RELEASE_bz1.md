# NEVER-WIDEN -- COO HALF: RELEASE a console selection that blocks the site Z runner (HVST-bz-1, round 83), on row AMGT_HARVST-Z-S115

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~05:4xZ. **Extends:** `round83/NEVER_WIDEN_HALF_COO_RUNNER_REPIN_bz1_CARRIED.md` (C-a..C-g) and
`round83/NEVER_WIDEN_HALF_COO_WEDGED_RUNNER_BRANCH_bz1.md` (W1-W5), both unchanged.

## What was found (`0.7.0_AE_CloudOps~ZW`, bus 4d93c77a, `round83/bz1_wedge_read.out`, commit c33cb20912)

W1, W2, W4 and W5 read TRUE; W3 read FALSE: ONE child, `conhost.exe` 17968, created with the runner, and 0 ESTABLISHED (positive control PID 5320:
5 children, 1 ESTABLISHED). **`MainWindowTitle` reads `Select C:\Program Files\Python314\python.exe` in both samples.** That is the console's
SELECTION state, which blocks a process that writes to its console. It fits every reading: zero CPU, one thread in `Wait/Executive`, no write since
2026-10-12T20:22:35Z, and the conhost child. **The runner is probably not wedged. It is blocked on a console write.**

## Ruling on the ask ("does W3 exclude a console host?")

**NO. W3 stands as signed and branch X holds: nothing is killed.** A child is a child. Loosening W3 to reach a kill would have terminated a
runner that a keypress releases, losing its in-flight pair for nothing. The condition did its work: it exposed the cause.

## The act this half covers (and only this)

**Release the selection: ONE `Escape` key to the console window of PID 21512, once.** Not Enter (it copies the selection), not a click, not a
second key, no other window, no other process.
- **Gate Y, all read TRUE at the act in the same minute:** Y1 the title of PID 21512's window begins `Select ` in two samples 120 s apart;
  Y2 CPU unchanged across them and no `cycle_runner.log` write for 1 hour or more; Y3 the ONLY child is a `conhost.exe` whose `CreationDate` is
  within 5 s of the runner's; Y4 no ESTABLISHED connection; Y5 the checkpoint copied FIRST to `bz1_checkpoint_snapshot.json`, byte for byte,
  length and SHA-256 printed beside the source's; Y6 the target window handle is PID 21512's own `MainWindowHandle`, printed.
- **After the key:** read the title again (must no longer begin `Select `), then do NOT stop the task. The stop file stays. The runner finishes
  its pair, reads the stop file, writes `STOP-FILE ... present` and its `.cycle.json` reading `stopped_by_operator`; the order then continues at
  step 1 (iii) and step 2 as written. Read at 5, 10 and 15 minutes after the key and record each.
- **Branch Y-fail:** any of Y1-Y6 FALSE, or the runner has written nothing 15 minutes after the key: NO further act, one row, and the question
  returns to the issuer. The W1-W5 kill branch stays closed unless W3 itself reads TRUE.

## Blast radius and rollback
One keypress, on one window, that the console host consumes in selection mode and does not forward to the process. It changes no file, no
state, no task. It cannot be undone and has nothing to undo: a selection is a display state. If the key does not release it, the state is
exactly as before. The loss is ZERO pairs (the runner is not ended); the checkpoint snapshot is taken first anyway.

## What this half does NOT cover
- Any kill, any `Stop-ScheduledTask` before the cycle record exists, any input to another window or process, any registry or console-mode change.
- The CAUSE (who or what put the console into selection at about 20:22Z, and whether QuickEdit stays on for the task's console). That is
  row Z-S115's to diagnose. No monitor, alert or sweeper is built for it (standing moratorium).

## VERDICT: SIGNED (COO). Not started until the CTO half is on file at `ledger/NEVER_WIDEN_ROUND83_BZ1_CONSOLE_RELEASE_CTO_HALF.md`.
