# AMGT_CORPUS round 16 -- never-widen pair for registering the `amgt-induction-daily` Scheduled Task and its first runs (cell CRPS-r-1)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Ruling it implements: round-15 analysis s.2 and s.4 cell 1 @`c265fbb6ff`.

## THE ACT
1. `powershell -File lib/research/corpus/schedule_induction.ps1 -Register -Commit bb2f3dbb18` from the shared tree. This
   creates the detached checkout `C:\Users\Opal Bloomberg\Desktop\opal-pinned\amgt-induction-daily\bb2f3dbb184e` (derived from
   the repository root) and registers the task. The action is
   `cmd.exe /c "set OPAL_INDUCTION_FIRE=1&& "<Python311 python.exe>" -m lib.research.corpus.induction_scheduled --mode fire"`,
   with WorkingDirectory set to the checkout. It runs daily at 13:00Z (absolute instant), first 2026-09-30T13:00:00Z,
   StartWhenAvailable, with a 2 h limit. No principal is set, so it runs as the registering user while that user is logged on,
   the same as the other site-Z tasks.
2. **Ad-hoc QA run the same evening** (`Start-ScheduledTask amgt-induction-daily`), through the task's own action. It exercises
   the registered path; the scheduled 13:00Z fire stays the acceptance. It does NOT consume the discriminator: population 0
   stays 0 unless a folder syncs.
3. A change entry opens before step 1 and closes on the after-state reads.

## WRITER CENSUS
- **The task** (Task Scheduler) and **the pinned checkout** (git worktree): written only by `-Register`.
- **Each fire's writes** come from the producer's own rule (`induction_run.run`), read at `bb2f3dbb18`:
  - population 0 -> no `add_security` call, no Bloomberg call, no pool put;
  - population N > 0 -> ONE `add_security --batch` call, which lands N raw objects, N registration rows (in the PINNED checkout's
    `registrations.json`, see below) and ONE pool put `crosswalk/v1/<as_of>.json` via `write_pool` (create, or IfMatch
    overwrite when the digest differs);
  - a readback JSON under the pinned checkout's `deliverables/0.9.0_WK_AMGT_CORPUS~2/`;
  - the log `%LOCALAPPDATA%\opal\amgt-induction-daily\<as_of>.log`.

## BEFORE-STATE (measured 2026-09-29T22:48:32Z; `evidence/r16_before.txt`)
- Task `amgt-induction-daily`: NOT REGISTERED. `...\Desktop\opal-pinned\`: absent.
- `crosswalk/v1/`: 6 keys, latest `2026-09-29.json` (237 records; round 15's put).
- `induction_run.rows_for_run(<live library>)`: **0 rows**, so the population is 0 of 96.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE -- both branches
- **Branch 1 -- population 0 (today, and at the first fire unless a folder syncs):**
  - `run()` makes NO call; `bloomberg_calls 0`; no pool put; the crosswalk stays at 6 keys, latest `2026-09-29.json`.
  - The log carries `induction_scheduled mode fire as_of <date> rc 0 log <path>`, and the task's LastTaskResult is 0.
- **Branch 2 -- population N > 0 (a new EVIDENCED folder synced before a fire):**
  - ONE batch call with N requests. Ambiguous or disagreeing names are REFUSED before any call (CVO~Z's calls-not-picks ruling).
  - ONE pool put of `crosswalk/v1/<as_of>.json`. For the ad-hoc run today that is `2026-09-29.json`, overwritten IfMatch with
    round 15's 237 records plus the N new ones.
  - The N registration rows land in the PINNED checkout's `lib/research/identity/registrations.json`, NOT in CLOUD's (row
    `Z-S63`). CLOUD's copy lacks them until a seat carries them, and a later crosswalk build from CLOUD inputs would drop them.
    This is the cell's one structural hazard, named here for the CTO half to grade.
- **Not in either branch:** a Hitachi-type folder (identity only in its name) is NO_EVIDENCE and never called (row `Z-S61`).

## AFTER-STATE THE VERIFY READS
1. `-Status`: `state Ready next 2026-09-30 ... 13:00Z-equivalent`; the pinned checkout exists at `bb2f3dbb184e...` with `git
   status` clean.
2. After the ad-hoc run: LastTaskResult 0. The log line reads `mode fire as_of 2026-09-29 rc 0`, and its body reads
   `bloomberg_calls 0` or no call at all (branch 1). The crosswalk is still 6 keys with latest digest unchanged (branch 1).
3. The acceptance is the first scheduled fire, 2026-09-30T13:00Z: the same reads, as_of 2026-09-30.

## BLAST RADIUS AND ROLLBACK
- **Touches:** one Scheduled Task, one detached git worktree (about 47k files; disk 191 GB free), and one log directory.
  Branch 2 adds the writes above.
- **Rollback:** `schedule_induction.ps1 -Unregister`, which is a write to Task Scheduler and no delete of data. The pinned
  checkout is left in place; removing it is a recursive delete and waits on Andrew's word. A branch-2 pool put is rolled back
  as in round 15's half: rebuild from CLOUD inputs and `write_pool` IfMatch.

## STOP LIMBS
1. `-Register` prints anything but `REGISTERED amgt-induction-daily`, or the pinned HEAD is not `bb2f3dbb18` -> `-Unregister`.
2. The ad-hoc run's LastTaskResult is not 0, or its log does not show rc 0 -> `-Unregister`, then diagnose. A runtime input
   missing from the pinned checkout (gitignored) is the named suspect.
3. The ad-hoc run makes any Bloomberg call while the population read 0 -> `-Unregister`, then a row.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against `bb2f3dbb18`.
