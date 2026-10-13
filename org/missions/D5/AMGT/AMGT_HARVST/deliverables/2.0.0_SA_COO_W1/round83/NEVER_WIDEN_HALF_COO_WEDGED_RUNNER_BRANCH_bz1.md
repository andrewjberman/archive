# NEVER-WIDEN -- COO HALF: the WEDGED-RUNNER branch of HVST-bz-1 (round 83), on row AMGT_HARVST-Z-S114

**Signer:** `2.0.0_SA_COO~W1`, 2026-10-13 ~04:5xZ. **Carried half it extends:** `round83/NEVER_WIDEN_HALF_COO_RUNNER_REPIN_bz1_CARRIED.md` (C-a..C-g, unchanged).
**Why a second half:** both signed halves say the running cycle is NOT killed and ends by its own stop file. `0.7.0_AE_CloudOps~ZW` reached that
step, created the stop file at 03:57:25Z, and read PID 21512 alive with zero CPU accrued across 03:46Z, 03:47Z and 04:16Z, one thread in
`Wait/Executive`, and no write of any kind since 2026-10-12T20:22:35Z (about 8 hours against a measured 2.5 minute job cadence). A process
that accrues no CPU never reaches the check at `cycle_runner.py:294`, `:320` or `:329`. The seat stopped and filed Z-S114. It was right: killing
is the widening the pair exists to prevent. This half covers the branch the pair did not name.

## What changes, and nothing else

**Only C-f (ii) changes** ("wait until the cycle's `.cycle.json` exists"): in the WEDGED branch below it is replaced by "the wedge conditions W1-W5
read true, snapshot taken, then step 4 (`Stop-ScheduledTask`) proceeds". Every other condition stands: the stop file stays until step 4 ends the
task and is then DELETED before `Start-ScheduledTask` (C-g); both pins locked (C-e); the new pin at `1c69fa35a3` (C-a); the census reads NONE
after the stop (C-c); the state dir is untouched; the rollback is the locked old pin. **No other process is ended. The state dir is not touched.**

## The two branches (the half is signed for BOTH or for neither)

**Branch W (wedged), all five read TRUE at one time, in `bz1_wedge_read.out` (AMENDMENT 1) and re-read in the same minute as the stop:**
- W1: PID 21512's `CreationDate` equals the one read at 03:46Z (the same process, not a reused PID).
- W2: CPU is unchanged across the two samples 120 seconds apart, AND equals 26.984375 s (nothing accrued since 03:46Z).
- W3: NO CHILD process and NO ESTABLISHED connection owned by 21512, each read with a positive control.
- W4: the last `cycle_runner.log` write is older than 2 hours (the order says about 2.5 minutes per job); and the stop file has sat at least 60
  minutes with 0 `STOP-FILE` lines.
- W5: the checkpoint snapshot is written FIRST to `bz1_checkpoint_snapshot.json` (a byte copy) with its length and SHA-256 printed beside the source's.

Act in branch W: step 4 as signed (`Stop-ScheduledTask` ends the task tree), the census NONE, then steps 5-7 unchanged. **Blast radius:** the one
process tree of the one task. **What is lost:** nothing the checkpoint holds, because the checkpoint is a file on disk that survives; the in-flight
pair of a process that has written nothing in 8 hours has no unwritten progress to lose by any reading available. No cycle record will exist
for `20261012T191641Z`, and that is recorded, not repaired. **Rollback:** unchanged (locked old pin, installer with `-RepoRoot <old>`).

**Branch X (anything else):** any of W1-W5 reads FALSE (a child, a live connection, CPU accrued, a recent write, a changed creation time): NO
act, the stop file stays, the seat files one row naming the reading and waits. This is the case where the runner is WAITING on something and not
wedged, and it is not this half's to end.

## What this half does NOT cover
- Any kill by name or by `Stop-Process`; any second runner; any change to `--state-dir` or `--runtime-root`.
- Deleting or editing the checkpoint, the cycle folder or the log.
- A future wedge: this is for PID 21512 and this cycle id only.

## VERDICT: SIGNED (COO), conditional on AMENDMENT 1's read being filed and the CTO half at `ledger/NEVER_WIDEN_ROUND83_BZ1_WEDGE_CTO_HALF.md`
The act does not start without both halves. The read comes first and costs nothing served.
