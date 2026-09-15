# IRPT_FNTEND.TO-FE-s-46 -- per-test timeouts sized to cost: result

- Worker: `0.9.0_WK_IRPT_FNTEND~1`
- Worktree pair: `C:/tmp/wk-irpt_fntend-8-1-fe-s-46`, and its `portal`. Both are on branch `wk-irpt_fntend-8-1-fe-s-46`.
- Workspace base: `3c35685158`, cut after the seat commit `716a9f4f6c`.
- Portal base: DEV `1f3ce9f0`.
- Portal commits, all LOCAL. The portal is frozen and nothing was pushed.
  - `01e5cf3d`: the first timeouts, plus fe-s-46/ (timeouts.test.ts, load-driver.mjs and ambient-shims.d.ts).
  - `904b6c4f`: re-sized from the first run's recorded costs, with 3 more tests added.
  - `a93275c8`: F41-AC5's control re-sized from the second run's recorded cost. The deciding runs are at this commit.
- `IRPT_FE_DEV_PORT=5261` was exported on every `bun test` run and measured closed first each time (ECONNREFUSED in 1-2 ms). No dev server was started.

## What changed in the two files

Only the third argument of `test(` calls changed. Against DEV `1f3ce9f0`, at portal `a93275c8` (`git diff -U0 1f3ce9f0 -- <the two files>`):

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

**It touches only `test(` calls.** Every test in both files spans several lines, and bun's third argument goes after the callback, on the line that closes the call. So each changed line is a closing `})`; no changed line carries `test(` itself (row **W1-S72**). The bound is shown by `fe-s-46/timeouts.test.ts`'s BOUNDS test instead. It parses both blobs with the TypeScript compiler, checks that each changed line closes a `test(` call, and cuts every third argument out of HEAD to compare it with DEV byte for byte. The deciding run at `a93275c8` printed:

```
fe-s-40/window.test.ts: DEV 1f3ce9f0 304 lines, HEAD 304 lines; 1 test( call(s) carry a third argument at HEAD
  :302  - "  })"  + "  }, 17625)"  closes the test( call at :253
  HEAD with every third argument removed equals the DEV blob byte for byte: yes
fe-s-41/one-writer.test.ts: DEV 1f3ce9f0 881 lines, HEAD 881 lines; 7 test( call(s) carry a third argument at HEAD
  :436 ... closes the test( call at :424     :452 ... at :438     :590 ... at :568     :626 ... at :592
  :764 ... closes the test( call at :751     :779 ... at :766     :869 ... at :791
  HEAD with every third argument removed equals the DEV blob byte for byte: yes
THE DIFF AGAINST DEV 1f3ce9f0 TOUCHES ONLY THE THIRD ARGUMENT OF test( CALLS: yes -- 8 of 8 changed lines close a test( call; 2 of 2 files equal DEV once the third arguments are removed
```

No assertion, printed line, helper or constant changed in either file.

## Each timeout and the recorded cost it is 3 times

"Can reach the default" (F46-AC3) means a named test, or any recorded cost of at least 2500 ms. Eight of the 16 tests are in that set. Each timeout is exactly 3 times that test's highest recorded cost. For a named test the timeout is also at least 17625 ms.

| test | line (closing line) | timeout ms | = 3 x | the recorded cost |
|---|---|---|---|---|
| F40-AC5 (named) | window.test.ts:253 (:302) | 17625 | 5875 | the named floor: F41-AC2's control in row W3-S33. Its own highest is 5735 (W3-S33), and 3 x 5735 = 17205 is below the floor |
| F41-AC2's control (named) | one-writer.test.ts:424 (:436) | 20952 | 6984 | first run at 01e5cf3d, AC5 BEFORE run 1 p3 |
| HISTORY (generators) | :438 (:452) | 11013 | 3671 | first run, AC5 BEFORE run 2 p4 |
| F41-AC4 | :568 (:590) | 20907 | 6969 | first run, AC5 AFTER run 3 p0 |
| CONTROL (comparison not a constant) | :592 (:626) | 15138 | 5046 | first run, AC5 AFTER run 3 p1 |
| F41-AC5 BOUND | :751 (:764) | 21000 | 7000 | first run, AC5 AFTER run 3 p3 |
| CONTROL (perf-9 in memory) | :766 (:779) | 19266 | 6422 | first run, the AC2 run of one-writer.test.ts. It FAILED there against bun's default |
| F41-AC5's control (named) | :791 (:869) | 56673 | 18891 | second run at 904b6c4f, AC5 BEFORE run 1 p4 |

These eight tests have no timeout argument; each test's highest recorded cost is below 2500 ms:

| test | highest recorded ms |
|---|---|
| window :163 | 141 |
| window :181 | 188 |
| window :198 | 78 |
| window :216 | 32 |
| one-writer :397 | 844 |
| one-writer :545 | 265 |
| one-writer :560 | 46 |
| one-writer :871 | 2250 |

Every cost is a junit per-test time from bun's `--reporter=junit`. The full table, with each cost's source, is `RECORDED` in `fe-s-46/timeouts.test.ts`. That test also adds every cost the invocation records to it.

### How the sizes were reached, measured each time

1. **Unloaded**, one run per file on the DEV blobs:
   - F40-AC5 1250 ms, F41-AC2's control 625 ms, F41-AC5's control 3391 ms, BOUND 1141 ms.
   - Everything else was under 750 ms.
   - The whole suite at DEV took 77 s: 560 pass, 18 skip, 0 fail across 578 tests.
2. **Sizing**, on the DEV blobs, with `.scratch/loadrun.mjs`. That is 43 processes, each running both files with junit, started K at once. The table shows each K's fails, the peak cost of F41-AC5's control, and what else that K showed.

   | K at once | runs | processes failed | F41-AC5's control peak | also |
   |---|---|---|---|---|
   | 3 | 2 | 0 of 6 | 4000 ms | |
   | 5 | 1 | 5 of 5 (timed out) | 6531 ms | |
   | 8 | 1 | 8 of 8 (timed out) | 6625 ms | F41-AC4 2531 ms |
   | 12 | 2 | 24 of 24 (timed out) | 8375 ms | F41-AC4 3078, BOUND 3828, F40-AC5 3860, F41-AC2's control 1766 ms |

   First sizes, at `01e5cf3d`:
   - F40-AC5 17625
   - F41-AC2's control 17625
   - F41-AC4 9234 (3 x 3078)
   - BOUND 11484 (3 x 3828)
   - F41-AC5's control 25125 (3 x 8375)
3. **The first run of `timeouts.test.ts`**, at `01e5cf3d`, rc=1 in 228 s. The box was loaded by more than this file: between runs there were 23 python, 16 node and 7 claude processes that were not its own.
   - It recorded costs above the sizing's:
     - F41-AC5's control 15234 ms
     - BOUND 7000 ms
     - F41-AC4 6969 ms
     - F41-AC2's control 6984 ms
     - the CONTROL at :766 6422 ms (FAILED at 5000 ms)
     - the CONTROL at :592 5046 ms
     - HISTORY :438 3671 ms
   - Two AFTER load processes failed at the default on tests that had no timeout.
   - F46-AC3 read 1 of 8 and F46-AC5 read 2 of 3.
   - Result: re-sized at `904b6c4f`, with :438, :592 and :766 added.
4. **The second run**, at `904b6c4f`, rc=1 in 141 s.
   - F46-AC5 read 3 of 3 and F46-AC3 read 7 of 8.
   - Its BEFORE run recorded 18891 ms for F41-AC5's control, so that test needed at least 56673 ms against the 45702 committed.
   - Result: re-sized at `a93275c8`.
5. **The deciding run**, at `a93275c8`, rc=0 in 74 s. Every graded line reads as the criteria require (below). The same file inside the whole-suite census gives the same verdicts.

F41-AC5's control has recorded 8375, then 15234, then 18891 ms. The 60000 ms cap leaves 3327 ms: a recorded cost above 20000 ms has no timeout that meets F46-AC3's bar. Row **W1-S74** (ARMED) covers this.

## The load (F46-AC5)

The graded process and **4 more** `bun test` processes over the same two files, **5 at once**. The order's example is 2 more (3 at once). Sizing measured 3 at once reading **0 fails in 6 processes** on the DEV blobs, and 5 at once timing out F41-AC5's control in 5 of 5. A load that cannot fail the BEFORE arm could not show the timeouts doing anything.

A run counts as `0 FAIL` only when all 5 processes ran all 16 tests with 0 fail, not just the graded one.

The BEFORE arm runs the same load on scratch copies of the DEV `1f3ce9f0` blobs. It is recorded, not graded:

| invocation | BEFORE result |
|---|---|
| first run (3 BEFORE runs) | 15 of 15 processes failed |
| second run | 5 of 5 |
| deciding run (quieter box) | 0 of 5 |
| inside the whole-suite census | 5 of 5 |

A load timeout is probabilistic, so the deciding run's 0 proves nothing by itself.

## Scratch copies (F46-AC4, and the BEFORE arm)

The copies live under `<WS>/.scratch/fe-s-46-*/`, never under `__tests__/`, and are removed after the run. The tests locate their roots from `import.meta.url` and import by relative path. So in a copy:
- every `import.meta.url` becomes the ORIGINAL file's URL: 7 in one-writer, 4 in window;
- every non-builtin import specifier becomes the path bun resolves from the original directory: 1 in one-writer, 6 in window.

Nothing else in the text changes.

The F46-AC4 control copy is one-writer.test.ts at HEAD, run with `-t "<F41-AC2's control name>"`:
- Seeded with a third argument of 1: FAILED (TimeoutError), `timed out after 1ms`, junit 1 fail / 10 skip.
- The same copy with the committed 20952: passed, 0 fail.

## Criteria -- the deciding runs

- **F46-AC1**: at `a93275c8`, git status clean, `$ tsc -b --noEmit` gives `rc=0`.
- **F46-AC2**: `ENUMERATED 16 MINUS UNMEASURED 0 = MEASURED 16`, then `EVERY TEST IN THE TWO FILES MEASURED: 16 of 16`. The committed blobs hold 5 and 11 `test(` calls. Each file's own junit run read 5/0 and 11/0.
- **F46-AC3**: `EXPLICIT TIMEOUT ON EVERY TEST THAT CAN REACH THE DEFAULT: 8 of 8`. The check weighed 373 recorded costs, found `NAMED TESTS FOUND BY NAME IN THE COMMITTED BLOBS: 3 of 3`, and reported `TIMEOUTS OUTSIDE THE SET: 0`.
- **F46-AC4**: `A SEEDED 1 MS TIMEOUT FAILS THE SAME TEST: yes`.
- **F46-AC5**: `THE TWO FILES UNDER LOAD: 3 of 3 RUNS 0 FAIL`. Every process read 16 tests / 0 fail. Named costs:
  - F40-AC5 1703-1938 ms
  - F41-AC2's control 843-953 ms
  - F41-AC5's control 3516-5203 ms
- **F46-AC6**: `565 pass`, `18 skip`, `0 fail`, `Ran 583 tests across 103 files. [127.87s]`, rc=0. That is the DEV baseline of 578 across 102 files, plus this file's 5 tests. F41-AC2's census inside the run reads `WRITERS OF fe-s-14-global.json: 1 of 152 source files ... -- fe-s-14/gen-maps.ts`, so the three new fe-s-46 files are scanned and are not writers.
- **F46-AC7**: recorded below, with no verdict.

## F46-AC7 -- RECORDED, NOT GRADED

- **Timeouts.** Eight tests in the two files carry a timeout, each 3 times a recorded cost cited above. The remaining eight tests each recorded a highest cost under 2500 ms.
- **The discriminating arms.**
  - The DEV blobs under the same load failed in 25 of 30 BEFORE processes across four invocations.
  - The committed files under that load read 0 fail in every AFTER process of the deciding run and of the in-suite run.
  - A 1 ms seeded timeout fails the same test, so bun honours the argument.
- **Against the bar, W1-S74.** The bar's 60000 ms cap is 3327 ms above F41-AC5's control's sized timeout. `fe-s-46/timeouts.test.ts` sits in every later census and counts that census's own load runs as recorded costs, so under a heavier load its F46-AC3 can read red with no file changed. It also adds its load runs to every later census: here 128 s against 77 s for the whole suite.

## Rows filed

All four are in `INVESTIGATION_v2.md`, with `disposition` UNDER_INVESTIGATION.

| row | class, standing | finding |
|---|---|---|
| IRPT_FNTEND-W1-S71 | OBSERVATION, INERT | fe-s-1's `bun:test` shim declares `test(label, fn)` only. A type-only overload with the third parameter was added as `fe-s-46/ambient-shims.d.ts` |
| IRPT_FNTEND-W1-S72 | OBSERVATION, INERT | The third argument sits on the closing line, not on the `test(` line |
| IRPT_FNTEND-W1-S73 | OBSERVATION, INERT | The cell names 3 tests. On this box 8 of 16 recorded at least 2500 ms, and one unnamed test failed at the default |
| IRPT_FNTEND-W1-S74 | OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO~F` | F46-AC3's bar can be met only up to a 20000 ms recorded cost, and the fe-s-46 file carries a load-dependent verdict into every later census |

## Not done, and why

- **`fe-s-46/timeouts.test.ts`'s own test timeouts are not 3 x a cost.** They are 90000, 90000, 280000 and 30000 ms, set inside the order's `timeout 300` bound on the invocation. Their measured costs: the AC5 test took 186890 ms in the first run (three BEFORE runs), and the whole file took 228, 141 and 74 s. 3 x 186890 is past the 300 s bound. The rule that each timeout is 3 times a recorded cost binds the two files named in the grant.
- **`package.json`, `bunfig.toml` and every other file under `fe-s-40/` and `fe-s-41/`**: out of bounds, not touched.
- **No other file in the suite read red**, so no BLOCKING list is owed.
