# TO-Z6-R3 report -- sign-in focus re-assert + one bounded re-fill (0.7.0_AE_CloudOps~ZS, 2026-10-15)

**archetype:** DEPLOY

Order: `org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/OPAL_BBGTML.TO-Z6-R3.signin-focus-reassert-and-bounded-refill.md`
(issuer `2.0.0_SA_COO~ZB`, GO msg 34346). **Result: AC1 PASS, AC2 PASS, merge landed, AC3 NOT-EXERCISED (exit 2), ledger L2 OPEN and HELD.**

## Step-2 preconditions (read at the moment of starting)

| read | value |
|---|---|
| `dapi_check` earlier (TO-Z6-R3 un-park read) | 2026-10-14T12:58:15Z `DAPI: UP` (stayed parked) |
| `dapi_check` for this GO | 2026-10-15T05:42:00Z `DAPI: DOWN (session.start() failed -- no listener/transport on 8194)`, exit 1 |
| window | 05:44Z-05:50Z, outside 10:30Z-12:30Z |
| `BLOOMBERG: Login` window open | none (0 windows with a BLOOMBERG title) |
| `wintrv.exe` before | **not running**. Bloomberg processes before: `bbcomm` only (PID 11100) |
| 8194 listeners before | 0 |

## AC2 (attempts ledger `%USERPROFILE%\.bbg_signin_attempts.json`)

Before AC1: **35**. After AC1: **35**. Equal: the exercise spent no Bloomberg attempt. Still 35 after the later stub run.

## AC1 (`org/tier2_senior/0.7.0_AE_CloudOps~ZS/deliverables/z6_r3_exercise.log`, exit=0)

Run from the worktree copy `C:/tmp/zs-z6-r3` (branch `zs-bbgtml-z6-r3` @`7ab72b201a`), 05:44:23Z-05:48:14Z. Key lines, in order:

1. `fill attempt 1/3 (bbg_signin.ps1 -Phase fill -Fresh)` ... `focus VERIFIED` ... `VERIFY: PASS` (password dots 9 of 9)
2. `DRY-RUN: focus held at the click point -- no ledger write, no click.`
3. `TEST: -ForceRc4Once -- first submit rc forced to 4`
4. `rc=4 -- one bounded re-fill (1/1), no attempt spent`
5. second fill, `wintrv already running (re-targeting its login window)` (no `-Fresh`), `VERIFY: PASS`
6. `DRY-RUN: focus held at the click point -- no ledger write, no click.`
7. `DRY-SUBMIT: stopped before Login`

Forbidden lines (`Clicking Login`, `ledger recorded`): 0. One note on order: the first dry-run line prints before the `TEST` line, an extra line in the sequence the order lists; the required lines are all present in the required order.

**Redaction:** the verify step prints an OCR read of the login NAME. I replaced that value in my copy before committing (grep for it: 0 hits). Row `OPAL_BBGTML-Z-S21` records that this is routine (16 hits across 13 local pull logs) and asks the issuer's reading.

## Box left as found

After AC1 I closed the Bloomberg UI tree because `wintrv` was not running before: 6 processes (`wintrv`, `blpsmarthost`, 4 `blpwtk2_subprocess`), 2 survived the first pass and went on the second; final count 0. `bbcomm` untouched (PID 11100). 8194 listeners: 0, as before. Done by 05:50Z, before 10:30Z.

## Landing and AC3

- Ledger `opal-bbgtml-z6-r3-signin-20261013` opened 05:52Z (entry and sentinel committed by the tool).
- Merge **`3dad54c56f`** on box/sitez via `safe-merge.sh`, 05:53Z, exactly the two files `bbg_signin.ps1` and `bbg_fallback.ps1`. Trunk had no commit on `integrations/bloomberg/auth/` since the branch base.
- **AC3** (`r2_p0_listener_check.sh`) at 05:54:02Z: `8194 listeners before run: 0`, `R2: NOT-EXERCISED (no 8194 listener -- the check cannot discriminate)`, **exit=2**. By its own header this is never a PASS and not a FAIL, so the order's revert condition did not trigger and I did not revert. I did not stand up a listener myself.
- What I could read instead (NOT a substitute for AC3): both landed files parse with 0 errors (PowerShell AST, nothing executed). The check's own safe command (`-ForceDown -StubSubmit`) with no listener took the `$absent -eq 3` arm: `P0 gate: transport sustained-down, network OK -> sign-in warranted.` printed, then `STUB: would now fill`, rc 0, attempts 35 -> 35, no UI started (`deliverables/z6_r3_ac3_partial_absent3_arm.log`). The arm AC3 grades, `$absent -eq 0` (listener up, no `sustained-down` line), was **not** exercised.
- R3 changed one P0-area line (Amendment 1: the `sustained-down` line is now `if ($absent -eq 3)`, `bbg_fallback.ps1:69`). So the unexercised arm is the one this merge touched.

## Ledger, disposal, push

- L1 CLOSED (merge hash). **L2 OPEN**, entry put on `hold --gate-type external` (reread event: 8194 has a listener). It reads KNOWN-HELD, not RED, and goes HELD-STALE after 4 days.
- Worktree `C:/tmp/zs-z6-r3` and branch `zs-bbgtml-z6-r3` are **kept, locked**: the order removes them after the ledger closes, and it has not.
- Push state: **LOCAL** (HEAD measured at commit time; origin `box/sitez` does not contain it).

## Decision needed from the issuer

Keep the landing (my action) or revert before the 11:00Z scheduled pull. Evidence for keeping: the same bytes passed AC1 end to end, parse clean, and the changed `$absent -eq 3` arm printed correctly. Evidence against: the `$absent -eq 0` arm is unverified on the shared tree. I will re-run AC3 and close L2 as soon as 8194 has a listener, if this seat is still live.
