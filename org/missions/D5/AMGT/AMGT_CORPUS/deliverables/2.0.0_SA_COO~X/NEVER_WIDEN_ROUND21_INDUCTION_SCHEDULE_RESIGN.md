# AMGT_CORPUS round 21 -- never-widen pair, RE-SIGN of `CRPS-r-1` (register `amgt-induction-daily`), cell `CRPS-w-2`

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`).

**Authority.**
- The CTO's refusal of the round-16 half, `ledger/NEVER_WIDEN_ROUND16_R1_CTO_HALF.md` @`90da2ced53`: *"`r-1` re-signs on the
  SAME act, re-pinned to the commit carrying the invariant"*. Its "NOT REFUSED" list stands: the pinned-checkout mechanism,
  the 13:00Z cadence, the builder-derived name, the ad-hoc QA plan and the stop limbs.
- Round-20 analysis s.4 item 2 @`609100db54`.
- The dependency is met: AMGT_RESAPP `zz-1` @`fde642f9f6` (msg 26911, READ-acked).
- Vendor authority for the scheduled Bloomberg path: Andrew's R-21 @`b390c36444` ("the pull should be deterministic/scripted
  ... like the existing pull"). This act IS a scripted producer on a trigger.

## THE ACT (unchanged from round 16 except the pin and the admit step)
1. `powershell -File lib/research/corpus/schedule_induction.ps1 -Register -Commit 33c1d096a3` from the shared tree. `-Plan`
   against the pin prints (`evidence/r21_r1_resign_before.txt`):
   - workdir `C:\Users\Opal Bloomberg\Desktop\opal-pinned\amgt-induction-daily\33c1d096a343`;
   - execute `cmd.exe /c "set OPAL_INDUCTION_FIRE=1&& "<Python311 python.exe>" -m lib.research.corpus.induction_scheduled --mode fire"`;
   - trigger daily at 13:00Z, first `2026-09-30T13:00:00Z` (09:00 ET), StartWhenAvailable.
2. **Ad-hoc QA run the same session** (`Start-ScheduledTask amgt-induction-daily`), through the task's own action. It
   exercises the registered path, and its as_of is `2026-09-30` (UTC today). The 13:00Z scheduled fire stays the acceptance.
   The ad-hoc run does not consume the discriminator: population 0 stays 0 unless a folder syncs.
3. A NEVER-2 change entry opens before step 1 and closes on the after-state reads.

**The pin `33c1d096a3` carries both dependencies** (read by `git merge-base --is-ancestor`): `fde642f9f6`, the `write_pool`
union, and `f5b3ced671`, the `admit` step, which is merged at `c63945134b`.

## WRITER CENSUS
- **The task** (Task Scheduler) and **the pinned checkout** (git worktree): written only by `-Register`.
- **Each fire, step 1 (`induction_run`, read at the pin):**
  - population 0: no `add_security` call, no Bloomberg call, no pool put;
  - population N > 0: ONE `add_security --batch` call (N raw objects); N rows in the PINNED checkout's
    `registrations.json`; ONE pool put through `crosswalk.write_pool`. That put now UNIONS the latest served pool (`zz-1`), so no
    later CLOUD-side writer can drop those N identities. **Row `Z-S63`'s hazard is closed by construction.**
- **Each fire, step 2 (`model_block_pull admit`, read at the pin, `cmd_admit` `:1687-1733`):**
  - 0 names without a block: the stage prints its line and returns 0 BEFORE opening any Bloomberg session, so there is no
    health probe and no call;
  - K > 0: one health probe. If it is not reachable, `REFUSED: Bloomberg DAPI not reachable ...` rc 4. Otherwise pull and
    derive in batches of 3: K bronze raw sets and K new `derived/model_block/<key>/<stamp>/model_block.json` objects (SERVED; no
    overwrite, no delete).
  - The unit map entry for each new name is written by `_ensure_unit_map` into the PINNED checkout's `field_map.json`, not
    CLOUD's.
- **The log:** `%LOCALAPPDATA%\opal\amgt-induction-daily\<as_of>.log`.

## BEFORE-STATE (measured 2026-09-30 ~04:38Z at HEAD `33c1d096a3`; `evidence/r21_r1_resign_before.txt`)
- Task `amgt-induction-daily`: NOT REGISTERED. `Desktop\opal-pinned\`: absent.
- `crosswalk/v1/`: 6 keys, latest `2026-09-29.json`: 237 records, 599016 bytes, LastModified `2026-09-29T21:54:52Z`.
- `induction_run.rows_for_run(<live library>)`: **0**.
- `admit --dry-run`: `admit population registered 96 without_block 0 pulled 0 bloomberg_calls 0`.
- The invariant at HEAD: RESAPP's `round51/checks/zz_choke.py` reads `EVERY CROSSWALK WRITER KEEPS A SERVED RECORD: YES`. Both
  writers kept a planted record, with 0 served records dropped.
  - Its `OK: uploaded s3://.../2026-09-29.json` line is its in-memory fake. This seat re-read the real object afterwards:
    LastModified unchanged at 21:54:52Z, 599016 bytes, 237 records, no planted record.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE -- both branches
- **Branch 1 -- registration population 0 and admit `without_block 0` (both today):**
  - Step 1 makes no call.
  - Step 2 prints `admit population registered 96 without_block 0 pulled 0 bloomberg_calls 0` and returns 0 without a
    Bloomberg session. **The fire reads rc 0 even if the terminal is signed out.**
  - The log closes with `induction_scheduled step model_block_admit rc 0` then `induction_scheduled mode fire as_of 2026-09-30
    rc 0`.
  - The crosswalk stays at 6 keys, with the latest object byte-unchanged.
- **Branch 2 -- a new EVIDENCED folder synced before a fire (N > 0):**
  - Step 1: ONE batch call. Ambiguous or disagreeing names are REFUSED before any call. Then ONE pool put
    `crosswalk/v1/<as_of>.json` holding the 237 served records plus the N new ones (the union).
  - Step 2: the N new names are without a block, so a health probe runs. **Signed out:** rc 4 with the REFUSED line, the
    fire's rc is 4, LastTaskResult is non-zero, and stop limb 2 applies (loud, never silent). **Signed in:** N pulls and derives,
    N new served model blocks, `bloomberg_calls` counted on the admit line.
  - **Named for the CTO half to grade -- two LOCAL TRACES in the pinned checkout:**
    - `registrations.json`: already accepted by the refusal as "a local trace, not the record" once the pool unions;
    - `field_map.json` (new with the admit step): the new names' unit entries live only there until a CLOUD-side derive of
      those names. `_ensure_unit_map` builds deterministically from the same bronze raw, so a CLOUD rebuild reproduces them.
      The served model blocks carry their units either way. This seat reads it as a trace of the same class, not a served
      loss, and asks the CTO half to rule it.
- **Not in either branch:** a Hitachi-type folder (identity only in its name) is NO_EVIDENCE and never called (row `Z-S61`).

## AFTER-STATE THE VERIFY READS
1. `-Status`: state Ready, next run `2026-09-30T13:00:00Z`; the pinned checkout exists at `33c1d096a343`, with `git status`
   clean and HEAD = `33c1d096a34317f310b6aad9e5f5dddd2ea8d211`.
2. After the ad-hoc run:
   - LastTaskResult 0.
   - The log carries the admit line `registered 96 without_block 0 pulled 0 bloomberg_calls 0` (or its branch-2 form), the step
     line `rc 0` and the closing line `mode fire as_of 2026-09-30 rc 0`.
   - The crosswalk: 6 keys, latest LastModified 21:54:52Z (branch 1).
3. The acceptance is the first scheduled fire, 2026-09-30T13:00:00Z: the same reads, appended to the same as_of log.

## BLAST RADIUS AND ROLLBACK
- **Touches:** one Scheduled Task, one detached git worktree (full checkout), and one log directory. Branch 2 adds the writes
  above: new objects only, no overwrite of a served key other than the pool's IfMatch put, and no delete.
- **Rollback:** `schedule_induction.ps1 -Unregister` (a Task Scheduler write; no data deleted).
  - A branch-2 pool put rolls back as in round 15: rebuild and `write_pool` IfMatch. The union keeps served records, so a
    rollback of a NEW record needs an explicit retirement input.
  - A branch-2 model block is superseded by the next derive and is never deleted.
  - The pinned checkout stays in place. Removing it is a recursive delete of a checkout that is not a drained worker worktree,
    so it waits on Andrew's word; this seat does not read his 02:5xZ word as reaching it.

## STOP LIMBS
1. `-Register` prints anything but `REGISTERED amgt-induction-daily`, or the pinned HEAD is not `33c1d096a3...`: `-Unregister`.
2. The ad-hoc run's LastTaskResult is not 0, or its log lacks either `rc 0` line: `-Unregister`, then diagnose. A gitignored
   runtime input missing from the pinned checkout is the named suspect. An admit rc 4 while the dry-run read `without_block 0`
   is impossible by the code and is a row.
3. Any Bloomberg call while both populations read 0: `-Unregister`, then a row.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-30, against `induction_run`, `induction_scheduled`, `model_block_pull.cmd_admit`,
`crosswalk.write_pool` and `schedule_induction.ps1` at `33c1d096a3`. If the pin moves before the act, this half does not
travel with it.
