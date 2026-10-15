# TO-Z6-R8 report -- the submit waits the foreground transient out (0.7.0_AE_CloudOps~ZS, 2026-10-15)

**archetype:** DEPLOY

Order: `org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/OPAL_BBGTML.TO-Z6-R8.stable-foreground-settle-and-glyph-fixture.md` (issuer `2.0.0_SA_COO~ZB`, GO msg 34569,
CTO ruling @079108405c). **Result: AC1 PASS, AC2 PASS, AC3 PASS. Cell R8a landed. Cell R8b: NOT SEPARABLE, `bbg_verify.ps1` unchanged. Status flip is the issuer's.
The real-run read (the 2026-10-16 07:00 ET fire) is not done and is the issuer's.**

## Landing (measured)

- Branch `zs-bbgtml-z6-r8` @`08fb0ceb84`, merged to box/sitez as **`74f9b3b31b`** (1 file: `integrations/bloomberg/auth/bbg_signin.ps1`), landed **2026-10-15T20:48Z**:
  after the 20:00Z close, before 09:00Z on 10-16, outside 10:30Z-12:30Z. Blob `16ce99a00c57` at HEAD equals the branch blob.
- Ledger `opal-bbgtml-z6-r8-stable-fg-20261015` opened 20:45Z (entry and sentinel committed first), **CLOSED** (L1 merge, L2 AC3), sentinel removed.
  Worktree `C:/tmp/zs-z6-r8` (clean) and the branch removed.
- Push state: **LOCAL** (measured at the end of this report; see the last section).

## What changed (cell R8a)

The submit phase's 3 x 300 ms re-assert loop is replaced by a SETTLE loop: poll every 250 ms for at most 90 s; on every poll where the login window is not in front, re-assert it and
reset the stable Stopwatch; proceed only after 2000 ms of real elapsed time with the login window in front. One line per state change (`settle: lost fg to <proc>(<pid>), re-asserting` /
`settle: login window regained foreground ...` / `settle: login window foreground, stable clock 2000/2000 ms after <n> ms`). Never settling keeps today's abort exactly (`ABORT: focus lost before
submit.`, R7's TRACE line, exit 4, zero attempts). The LAST foreground check immediately before the ledger write and the click is untouched; R3's re-fill, R7's trace and `bbg_fallback.ps1` are untouched.

## AC1 and AC2 -- against a FAKE login window; nothing real was touched

Harness: `deliverables/r8_thief_harness.ps1`. It refuses (exit 7) if any real `BLOOMBERG: Login` window exists (none did), creates a fake window with that title and a thief window, both owned by
the harness, runs `bbg_signin.ps1 -Phase submit -DryRun` as a hidden child, and destroys both windows at exit (0 left open). No fill, no `-Fresh`, no Bloomberg process touched.

| arm | log | exit | key lines |
|---|---|---|---|
| **AC1 release** | `z6_r8_arm_release.log` | **0** | `settle: lost fg to powershell(57532), re-asserting` (+1.0 s) -> `thief released at +4.1s` -> `regained foreground after 3459 ms` -> `settle: login window foreground, stable clock 2000/2000 ms after 5530 ms` -> `DRY-RUN: focus held at the click point -- no ledger write, no click.` |
| **AC2 hold** | `z6_r8_arm_hold.log` | **4** | `settle: lost fg ...` (+1.3 s) -> **`ABORT: focus lost before submit.`** (+91.3 s) -> one `TRACE fgproc=powershell(19888) fgtitle='r8-harness-thief' ...`; DRY-RUN lines: 0; thief re-grabbed 945 times |

Four before/after numbers (identical in both arms): sign-in attempts **35 before, 35 after**; wintrv start **2026-10-15T11:00:25.765Z before, same after**.

- **AC2 timing, stated plainly:** launch-to-exit on the harness clock was **92.0 s** (inside 85-95). The whole shell invocation was **94-95 s** by two clocks (harness start-up and teardown add ~3 s), which sits at the very top of
  the order's band. The 90 s loop budget is the design; the margin on a wall-clock reading is thin by construction.
- **Difference control (not in the order):** the same release arm against the OLD code in the shared tree (R3+R7 bytes, `z6_r8_negative_control_old_code.log`) FAILS exactly as signature B reads: `focus re-assert 1/3,
  2/3, 3/3 did not take`, `ABORT: focus lost before submit.`, TRACE naming the thief, exit 4 in 3.9 s. So the harness reproduces the failure and the new loop is what changes the outcome.
- **After landing,** the release arm re-run against the shared-tree copy: exit 0, settled, DRY-RUN line, attempts and wintrv unchanged (`z6_r8_arm_release_shared_tree.log`).

## AC3 (shared tree, 2026-10-15T20:49:37Z, 8194 listeners = 1)

`P0 gate: 8194 listening (3/3) but dapi_check failed -> listener up, not entitled -> sign-in warranted`, `STUB: would now fill`, **`R2: PASS`, exit=0**; attempts 35 -> 35; the landed file parses with 0 errors.

## Cell R8b -- glyph calibration (evidence first; band NOT widened)

Instrument: `deliverables/r8b_glyph_census.py` over the 37 pull logs plus my 05:44Z exercise log (output `z6_r8b_glyph_census.txt`; it prints run counts and OCR similarity only, never the OCR text). **18 VERIFY renders** of the correct login, all with password dots 9/9 and OCR similarity 100%:

| period | logs | glyph runs | verdict |
|---|---|---|---|
| 09-20 .. 10-04 (before the 10-06 Terminal update) | 8 | 11 | PASS x8 |
| 10-06 (3 fills) and 10-08 (2 fills) | 2 | **10** | FAIL x5 (`outside 11..12`) |
| 10-11, 10-13, 10-15 07:00 ET and my 10-15 05:44Z exercise (2 renders) | 4 | 11 | PASS x5 |

**Retained images on the current build: none.** `C:\opal-elev` holds only 08-14/08-18 images (`bbg_login_shot_NEG.png`, `bbg_user_crop.png`, `bbg_pw_zoom.png`, `state_check.png`, `monitor2.png`), all from the old build, and each fill scrubs the prior `bbg_login_shot.png`. So the glyph counter could not be re-run
over a 10-run render: the only record of one is the logged count. No screenshot was opened.

**Verdict: NOT SEPARABLE by run count alone.** A legitimate render measured 10 on 10-06 and 10-08 and 11 on every render since 10-11, on the SAME Terminal build (replaced 10-06 04:04Z), so the count is not a function of the build; and the border-artifact mutant is defined by also measuring 10
(the comment above `$uLo`), so no run-count threshold admits the legitimate 10 and rejects the mutant. OCR read 100% on the 10-run renders, but OCR is observation-only by Andrew-direct 08-20 and no mutant OCR figure is retained to compare. **Per the order, `bbg_verify.ps1` is unchanged**; the band
stays `[len-1, len]` and the password-dot check stays exact. This corrects one claim in the 10-15 investigation: it reads the 10 as a build-wide shift of the count by one, but the build did not change between the 10-run and 11-run renders. The 10-09 reboot lies between them and is a confound candidate; I tested nothing about it.
Signature A has been quiet since 10-11 because the count has read 11 and passes; why it read 10 on 10-06 and 10-08 is not established here. Re-deriving a fixture needs an image of a 10-run render, which exists only if the next such fill is captured before it is scrubbed.

## Not exercised -- say so plainly

- **A thief from a DIFFERENT process under the Windows foreground lock.** In the harness the thief and the child share a parent, so the child's `SetForegroundWindow` is permitted. In the 07:00 ET task the re-assert may be refused outright, and the loop then succeeds only if the transient ends and the
  login window regains the foreground on its own. The release arm shows the loop settles once the foreground is stable; it does not show that a foreign process's transient ends. The 10-16 fire is the real test.
- The scheduled task was not run. The settle loop can add up to 90 s per submit (about 180 s with R3's one re-fill) to a fallback step; the task's `ExecutionTimeLimit` is 30 min and a normal pull is ~8 min.
- Real clicks, a real Login window and the real ledger were never touched (every submit was `-DryRun`).

## Push state

Measured after the commit of this report: see the message to the issuer.
