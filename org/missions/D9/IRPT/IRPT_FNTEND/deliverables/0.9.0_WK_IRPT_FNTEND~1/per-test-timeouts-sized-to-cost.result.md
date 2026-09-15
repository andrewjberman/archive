# IRPT_FNTEND.TO-FE-s-46 -- per-test timeouts sized to cost: result (AMENDMENT 1)

- Worker: `0.9.0_WK_IRPT_FNTEND~1`
- Worktree pair: `C:/tmp/wk-irpt_fntend-8-1-fe-s-46`, and its `portal`. Both are on branch `wk-irpt_fntend-8-1-fe-s-46`.
- Workspace base for this run: `70315e1079` (the amendment commit).
- Portal base for this run: `b3c80698`. That is the first run's `a93275c8` plus portal DEV `ad732941` (FE-s-48 drained), synced in by the issuer.
- Portal commits for amendment 1, all LOCAL. The portal is frozen and nothing was pushed.
  - `09e9431a`: the census run reads only committed blobs; the load and measurement arms are opt-in. The two named files are unchanged.
  - `953afc32`: the committed cost ledger `fe-s-46/recorded-costs.json`, from the first load run.
  - `f66ebad1`: the ledger with the deciding F46-AC5 load run appended. Every census criterion's deciding run is at this commit, on a clean tree.
- The first run's portal commits stand: `01e5cf3d`, `904b6c4f` and `a93275c8`.
- `IRPT_FE_DEV_PORT=5261` was exported on every `bun test` run and measured closed first each time (ECONNREFUSED in 2-4 ms). No dev server was started.

## What amendment 1 changed (row W1-S74)

`fe-s-46/timeouts.test.ts` now has two runs:

- **The census run** is the default, with `IRPT_FE_TIMEOUT_LOAD` unset. Every whole-suite census is this run.
  - It reads only committed blobs, each with `git cat-file blob HEAD:<path>`: the two files, and the committed ledger `fe-s-46/recorded-costs.json`.
  - It spawns no load, records no cost, and runs no test of the two files.
  - F46-AC6 prints every process it started and its own wall time.
  - It runs in about 2 s. The first run's version took 74 to 228 s, because it ran its load every time.
- **The load run** is `IRPT_FE_TIMEOUT_LOAD=1`. It runs the census tests, then three arms that the census run skips:
  - **MEASURE**: one junit run of each file.
  - **F46-AC5**: 3 AFTER runs, plus 1 BEFORE run on the DEV `1f3ce9f0` blobs, 5 processes at once each time.
  - **LEDGER**: appends every cost those runs recorded, each with its run (date, load, source, portal), to the working-tree ledger. The ledger is then committed by hand.
- **How the census run skips.** Each of the three arms is skipped with bun's `test.skipIf`, so the census counts them as skips. Each also prints `SKIPPED -- <arm>: <reason>` by name. The suite's skip count therefore rises by 3.
- **F46-AC4** is now a seeded scratch test of this file's own. It is written under `<WS>/.scratch/fe-s-46-*/ac4/` and removed afterwards.
  - Its body is about 50 ms: `await` a 50 ms timer, then expect at least 45 ms elapsed.
  - `seeded-1ms.test.ts` and `seeded-5000ms.test.ts` differ only in the third argument. The test checks that before running either.
- **F46-AC3** reads the committed ledger only.
  - It prints each set member's headroom under the 60000 ms cap, and under the 20000 ms residual line.
  - A ledger cost above 20000 ms makes its test a **named residual for the next cut**, printed by name. It is not counted red. There are none now.
- **Files.**
  - The blob census, the TypeScript-compiler parser and the junit reader moved to `fe-s-46/census-lib.mjs`. The test imports it in process, so every process the census starts goes through its logged spawner.
  - `load-driver.mjs` keeps only its `run` mode. Its `enumerate`, `diffcheck` and `control` modes are gone.
  - `ambient-shims.d.ts` adds a type-only `test.skipIf` overload.

## The ledger

`fe-s-46/recorded-costs.json` holds 24 runs and 707 costs, covering 16 of 16 tests. It is LF, with one line per run and one line per cost, so its diff lists what a run added.

- **B01-B12**: the 30 costs recorded before amendment 1, from the RECORDED table at `a93275c8`. The LEDGER arm carries them in from its BOOTSTRAP table, and only when no ledger exists in the working tree or at HEAD (row **W1-S75**).
  - B01 and B02 (row W3-S33's runs) are dated 2026-09-14, before 23:08:10Z.
  - B03 and B04 (the issuer's probes) have a day-only date.
  - B05 to B12 carry the time of the scratch output that recorded them.
- **R001-R006**: the first load run, at `09e9431a`. It recorded 336 costs. F41-AC5's control peaked at 8313 ms. The BEFORE arm failed 5 of 5 processes, each `timed out after 5000ms` on F41-AC5's control (5219-5468 ms).
- **R007-R012**: the deciding load run, at `953afc32`. It recorded 336 costs. F41-AC5's control peaked at 5187 ms. The BEFORE arm failed 0 of 5.
- The second append changed 17 existing lines, and each one only gained its joining comma (checked line by line).

Neither load run moved any test's highest cost. No untimed test reached 2500 ms, so **the eight committed timeouts stand**, each 3 times a ledger cost.

## What changed in the two files

Nothing in amendment 1. Only the third argument of `test(` calls ever changed. Against DEV `1f3ce9f0`, at portal `f66ebad1` (`git diff -U0 1f3ce9f0 -- <the two files>`, the same as at `a93275c8`):

```
--- a/src/pages/InvestorReporting/__tests__/fe-s-40/window.test.ts
+++ b/src/pages/InvestorReporting/__tests__/fe-s-40/window.test.ts
@@ -302 +302 @@ describe('F40-AC5 -- the portal calendar agrees with lib/trading_calendar.py, da
-  })
+  }, 17625)
--- a/src/pages/InvestorReporting/__tests__/fe-s-41/one-writer.test.ts
+++ b/src/pages/InvestorReporting/__tests__/fe-s-41/one-writer.test.ts
@@ -436 +436 @@ describe('F41-AC2 -- the Global map has one writer', () => {
-  })
+  }, 20952)
@@ -452 +452 @@ describe('F41-AC2 -- the Global map has one writer', () => {
-  })
+  }, 11013)
@@ -590 +590 @@ describe('F41-AC3 / F41-AC4 -- the one writer, run into a scratch directory', ()
-  })
+  }, 20907)
@@ -626 +626 @@ describe('F41-AC3 / F41-AC4 -- the one writer, run into a scratch directory', ()
-  })
+  }, 15138)
@@ -764 +764 @@ describe('F41-AC5 -- the frozen narrative speaks for the frozen report', () => {
-  })
+  }, 21000)
@@ -779 +779 @@ describe('F41-AC5 -- the frozen narrative speaks for the frozen report', () => {
-  })
+  }, 19266)
@@ -869 +869 @@ describe('F41-AC5 -- the frozen narrative speaks for the frozen report', () => {
-  })
+  }, 56673)
```

**It touches only `test(` calls.** The third argument goes on each multi-line call's closing line, so each changed line is a closing `})` (row **W1-S72**). The BOUNDS test at `f66ebad1` printed:

```
fe-s-40/window.test.ts: DEV 1f3ce9f0 304 lines, HEAD 304 lines; 1 test( call(s) carry a third argument at HEAD
  :302  - "  })"  + "  }, 17625)"  closes the test( call at :253
  HEAD with every third argument removed equals the DEV blob byte for byte: yes
fe-s-41/one-writer.test.ts: DEV 1f3ce9f0 881 lines, HEAD 881 lines; 7 test( call(s) carry a third argument at HEAD
  :436 ... at :424   :452 ... at :438   :590 ... at :568   :626 ... at :592
  :764 ... at :751   :779 ... at :766   :869 ... at :791
  HEAD with every third argument removed equals the DEV blob byte for byte: yes
THE DIFF AGAINST DEV 1f3ce9f0 TOUCHES ONLY THE THIRD ARGUMENT OF test( CALLS: yes -- 8 of 8 changed lines close a test( call; 2 of 2 files equal DEV once the third arguments are removed
```

No assertion, printed line, helper or constant changed in either file.

## Each timeout and the ledger cost it is 3 times

"Can reach the default" (F46-AC3) means a named test, or any ledger cost of at least 2500 ms. Eight of the 16 tests are in that set. Each timeout is exactly 3 times that test's highest ledger cost, except F40-AC5's: 3 x 5735 = 17205 is below the named floor of 17625 ms (3 x 5875), so F40-AC5 carries the floor.

| test | line (closing line) | timeout ms | = 3 x | the ledger cost (run) | headroom under the cap |
|---|---|---|---|---|---|
| F40-AC5 (named) | window.test.ts:253 (:302) | 17625 | 5875 | the named floor: F41-AC2's control in row W3-S33 (B01). Its own highest is 5735 (B02) | 42375 |
| F41-AC2's control (named) | one-writer.test.ts:424 (:436) | 20952 | 6984 | B09 p3, the first run's AC5 BEFORE run 1 | 39048 |
| HISTORY (generators) | :438 (:452) | 11013 | 3671 | B10 p4, the first run's AC5 BEFORE run 2 | 48987 |
| F41-AC4 | :568 (:590) | 20907 | 6969 | B08 p0, the first run's AC5 AFTER run 3 | 39093 |
| CONTROL (the comparison is not a constant) | :592 (:626) | 15138 | 5046 | B08 p1 | 44862 |
| F41-AC5 BOUND | :751 (:764) | 21000 | 7000 | B08 p3 | 39000 |
| CONTROL (perf-9 in memory) | :766 (:779) | 19266 | 6422 | B11 p0, the first run's F46-AC2 run of one-writer.test.ts | 40734 |
| F41-AC5's control (named) | :791 (:869) | 56673 | 18891 | B12 p4, the second run's AC5 BEFORE run 1 | 3327; its cost is 1109 ms under the 20000 ms residual line |

These eight tests have no timeout argument. Each test's highest ledger cost is below 2500 ms:

| test | highest ledger ms (run) |
|---|---|
| window :163 | 141 (B07) |
| window :181 | 188 (B06) |
| window :198 | 78 (B06) |
| window :216 | 32 (B05) |
| one-writer :397 | 844 (B08) |
| one-writer :545 | 265 (B09) |
| one-writer :560 | 46 (B09) |
| one-writer :871 | 2250 (B08) |

The measurement history behind B01 to B12, with the unloaded runs, the 43 sizing processes and the three runs of the first version, is in this file's first-run version at workspace `cb6b753407`.

## The load (F46-AC5)

The graded process plus 4 more `bun test` processes over the same two files, 5 at once. The order's example is 2 more. Sizing measured 3 at once reading 0 fails in 6 processes on the DEV blobs, and 5 at once timing out F41-AC5's control in 5 of 5.

A run counts as `0 FAIL` only when all 5 processes ran all 16 tests with 0 fail.

The BEFORE arm is recorded, not graded:

| invocation | BEFORE result |
|---|---|
| first-run invocations (three in all, plus the in-suite run) | 25 of 30 processes failed |
| amendment 1, first load run (`09e9431a`) | 5 of 5 failed, each `timed out after 5000ms` |
| amendment 1, the deciding load run (`953afc32`) | 0 of 5 (quieter box) |

A load timeout is probabilistic, so the deciding run's 0 proves nothing by itself.

## Criteria -- the deciding runs

- **F46-AC1**: at `f66ebad1`, 0 status lines, `$ tsc -b --noEmit` gives `rc=0`.
- **F46-AC2** (`timeout 300`, census run at `f66ebad1`, rc=0, 5 pass / 3 skip / 0 fail, 1.94 s):
  - It printed `ENUMERATED 16 MINUS NO LEDGER COST 0 = MEASURED 16`, then `EVERY TEST IN THE TWO FILES MEASURED: 16 of 16`.
  - The committed ledger read 36822 chars and 24 runs.
  - Each test's line gives its ledger cost count (43-47) and its highest cost, with the run's date, load, source, process and portal.
- **F46-AC3**: the same run printed `EXPLICIT TIMEOUT ON EVERY TEST THAT CAN REACH THE DEFAULT: 8 of 8`. It also printed:
  - `LEDGER COSTS CONSIDERED: 707`
  - `NAMED TESTS FOUND BY NAME IN THE COMMITTED BLOBS: 3 of 3`
  - `TIMEOUTS OUTSIDE THE SET: 0, sized 0`
  - `NAMED RESIDUALS FOR THE NEXT CUT (a ledger cost above 20000 ms): 0`
- **F46-AC4**: the same run printed `A SEEDED 1 MS TIMEOUT FAILS THE SAME TEST: yes`.
  - `ARM 1 MS: ... rc=1; junit tests 1 fail 1; the test FAILED in 15 ms (TimeoutError); timed out after 1ms`
  - `ARM 5000 MS: ... rc=0; junit tests 1 fail 0; the test passed in 63 ms; no timeout line`
- **F46-AC5** (`IRPT_FE_TIMEOUT_LOAD=1 timeout 900`, at `953afc32`, rc=0, 7 pass / 1 skip / 0 fail, 55 s): `THE TWO FILES UNDER LOAD: 3 of 3 RUNS 0 FAIL`. All 15 AFTER processes read 16 tests, 0 fail. Named costs in the AFTER runs:
  - F40-AC5 1891-2266 ms
  - F41-AC2's control 719-875 ms
  - F41-AC5's control 2172-5187 ms
  - The same run's census read 16 of 16 and 8 of 8.
- **F46-AC6** (`timeout 120`, census run at `f66ebad1`, rc=0, 1.69 s): `THE CENSUS RUN SPAWNS NO LOAD AND MEASURES NO COST: yes`.
  - It spawned 10 processes: 8 git reads (`cat-file blob` of the two files, the ledger and the DEV blobs, plus `rev-parse`) and 2 `bun test` runs of the seeded scratch test.
  - `LOAD OR MEASUREMENT PROCESSES AMONG THEM: 0`; `PROCESSES OF NO KNOWN KIND: 0`; `COSTS RECORDED BY THIS RUN: 0; LEDGER WRITTEN: no`; `WALL TIME OF THIS FILE TO HERE: 1595 ms`.
  - All 3 arms were skipped by name.
  - The classifier's control reads a seeded `load-driver.mjs` run and a seeded `bun test` of one-writer.test.ts as LOAD OR MEASUREMENT: `yes`.
- **F46-AC7** (`timeout 600`, the whole suite at `f66ebad1`, 0 status lines, port 5261 ECONNREFUSED in 3 ms):
  - `569 pass`, `21 skip`, `0 fail`, `2460 expect() calls`, `Ran 590 tests across 104 files. [74.34s]`, rc=0.
  - The first run's census at `a93275c8` read 583 tests across 103 files in 127.87 s. The DEV baseline read 578 across 102 files in 77 s.
  - `timeouts.test.ts` gives 8 of the 590: 5 pass and 3 skip, the three arms skipped by name. The remaining difference arrives with portal DEV `ad732941` (FE-s-48) and was not measured separately.
  - Inside the suite, the census run read `16 of 16`, `8 of 8`, `yes` (seeded control), `yes` (bounds) and `THE CENSUS RUN SPAWNS NO LOAD AND MEASURES NO COST: yes`, in 1916 ms.
  - F41-AC2's census reads `WRITERS OF fe-s-14-global.json: 1 of 154 source files ... -- fe-s-14/gen-maps.ts`. So `census-lib.mjs` and the ledger are scanned, and neither is a writer.
  - No test read red, so no BLOCKING list is owed.
- **F46-AC8**: recorded below, with no verdict.

## F46-AC8 -- RECORDED, NOT GRADED

- **Timeouts.** Eight tests in the two files carry a timeout, each 3 times a ledger cost cited above. The other eight each have a highest ledger cost under 2500 ms.
- **The census is deterministic.** The census run reads only the committed blobs and the committed ledger. Its verdicts move only when a committed file moves: a load cannot turn F46-AC3 red inside a later census, because no cost is measured there. The F46-AC6 line and its process list show this on each run.
- **The discriminating arms.**
  - The DEV blobs under the same load failed 30 of 40 BEFORE processes across six invocations.
  - The committed files read 0 fail in every AFTER process of both amendment-1 load runs.
  - A 1 ms seeded timeout fails a 50 ms body that passes on 5000 ms.
- **What remains.**
  - F41-AC5's control has 3327 ms of headroom under the cap. A future ledger cost above 20000 ms would now print it as a named residual, not a red, and only after that ledger is committed.
  - A new cost counts only once the ledger is committed. So the sizing is as fresh as the last committed load run: here `f66ebad1`, with 24 runs.

## Rows filed

Both amendment-1 rows are in `INVESTIGATION_v2.md` with `disposition` UNDER_INVESTIGATION. W1-S71 to W1-S74 are the first run's rows. W1-S74 is not edited: its resolution record is the issuer's.

| row | class, standing | finding |
|---|---|---|
| IRPT_FNTEND-W1-S75 | OBSERVATION, INERT | The ledger is "produced only by" the load path, yet seven of the committed timeouts rest on pre-amendment costs. The LEDGER arm carries those in from a BOOTSTRAP table (B01-B12), and two of those runs have a day-only date |

## Not done, and why

- **`fe-s-46/timeouts.test.ts`'s own test timeouts are not 3 x a cost.**
  - The census tests each carry 30000 ms. Measured: 1.1 to 1.9 s for the whole file in five census runs, and the AC4 arm spawns two bun processes of about 0.1 s each.
  - The load arms carry 300000 (MEASURE), 620000 (F46-AC5) and 30000 (LEDGER) ms, inside the load invocation's `timeout 900`. F46-AC5 measured 55 and 65 s here, and 186890 ms in the first run's version (three BEFORE runs).
  - The 3 x rule binds the two files named in the grant.
- **The whole-suite skip count rises by 3**: the three load arms, skipped by name in every census. This is by design (amendment 1: "skipped BY NAME").
- **`package.json`, `bunfig.toml`, and every other file under `fe-s-40/` and `fe-s-41/`**: out of bounds, not touched.
