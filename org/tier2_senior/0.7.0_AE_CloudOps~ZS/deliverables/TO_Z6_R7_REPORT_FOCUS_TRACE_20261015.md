# TO-Z6-R7 report -- foreground trace at every focus abort (0.7.0_AE_CloudOps~ZS, 2026-10-15)

**archetype:** DEPLOY

Order: `org/tier2_senior/0.7.0_AE_CloudOps~ZS/task_orders/OPAL_BBGTML.TO-Z6-R7.focus-abort-foreground-trace.md` (issuer `2.0.0_SA_COO~ZB`, GO msg 34431,
CTO ruling @701a4c705a). **Result: AC1 PASS, AC2 PASS, AC3 PASS; merged and closed. Status flip is the issuer's. The real-run read is not done and is the issuer's.**

## What changed (2 files, both landed together)

- `bbg_signin.ps1`: `Get-FgTrace` builds ONE ASCII line `TRACE fgproc=<name>(<pid>) fgtitle='<=60 ASCII, no quotes>' loginhwnd=<hwnd|none> sess=<n> console=<n>
  state=<Active|Disconnected|other> locked=<y|n>`, printed at the three focus aborts just before `exit 4` (fill "focus did not take", submit re-assert
  exhaustion, submit last check). Read-only: no click, no focus change, no ledger. A field that cannot be read prints `unreadable`; no foreground window prints `fgproc=none(0)`.
  `-TraceOnly` (test-only) prints the line and exits 0.
- `bbg_fallback.ps1`: `Cap` keeps the last `TRACE ` line from the sign-in output it already pipes through `Say`; the `Escalate` calls on the fill-not-verified,
  rc=4 re-fill-not-verified and submit-aborted-rc=4 paths append it. `-TraceTest` and the env var `BBG_ESCALATION_PATH` are test-only. No new file, process or task.
- Untouched: R3's re-assert and re-fill logic, the P0 gate, the fire-once ledger guard, the verify logic, the scheduled task.

## Criteria

- **AC1** (run from the worktree at 14:26:11Z, exit=0, grep count **1**). Matched line, which holds no credential or login name:
  `TRACE fgproc=cmd(3512) fgtitle='C:\windows\system32\cmd.exe' loginhwnd=none sess=1 console=1 state=Active locked=n`. Copy: `deliverables/z6_r7_trace_test_escalation.txt` (1 line).
- **AC2**: attempts count **35 before, 35 after**; `C:\opal-elev\bbg_fallback_ESCALATION.txt` **17 lines before, 17 after**. No attempt spent, no fake entry.
- **AC3** (shared tree, 14:38:00Z, 8194 listeners = 1): `P0 gate: 8194 listening (3/3) but dapi_check failed -> listener up, not entitled -> sign-in warranted`, then
  `STUB: would now fill`, **no `transport sustained-down` line**, `R2: PASS`, **exit=0**; attempts 35 -> 35. This is the listener-up arm R3's L2 could not reach
  (R3's ledger stays closed as NOT-EXERCISED per ruling 34431; this read now covers that arm on the merged R3+R7 bytes).

## Landing, ledger, disposal, push

Merge **`3aaf87a486`** on box/sitez (2 files), landed 14:37Z, outside 10:30Z-12:30Z. A manual pull for vintage 20261014 was mid-run (started 14:24:57Z); I waited until its
pull and publish legs had finished (`PUBLISH EXIT CODE: 0`, `END-TO-END OK`) and landed while only its later legs ran, none of which call these scripts.
Ledger `opal-bbgtml-z6-r7-focus-trace-20261015` CLOSED (L1 merge hash, L2 AC3), sentinel removed. Worktree `C:/tmp/zs-z6-r7` (clean) and branch `zs-bbgtml-z6-r7` removed.
Push state: **LOCAL** (origin `box/sitez` does not contain it).

## Not exercised -- say so plainly

- **The three abort sites and the escalation-line append were NOT run.** AC1 exercises the trace function and `Escalate`; reaching a real abort needs a Login window and
  a lost foreground, which the order forbids touching. Verified by parse (0 errors), a byte-exact edit (each file kept its own line ending, 0 non-ASCII), and a read of the diff.
  The issuer's real-run read of the next failed fire is the test of that wiring.
- `state=` reads `other` for every state but Active (0) and Disconnected (4), as the order specifies; `locked=y` is a `LogonUI.exe` process in the session and was
  never seen true here (only `n` was observed).
- The title field can carry whatever the foreground window shows (capped at 60 ASCII chars, quotes removed). Today's was a console title; a browser tab title would also be written
  to the escalation file under `C:\opal-elev` (not committed).

## Interpreter facts for grading (CTO FYI 34457, python 3.14 outage since 14:02Z)

`scheduled_daily_pull.cmd` pins explicit interpreters: `PY` = `C:\Anaconda\envs\cma\python.exe` (:38), `PY_AWS` and `PRICE_PY` = `...\Python311\python.exe` (:143, :354); `bbg_fallback.ps1` calls
`$CMA` = the cma python for `dapi_check.py`. None resolves `python` from PATH, and the 14:25Z manual pull ran end to end after the 14:02Z break. So a failed fire would not be
the outage's doing unless some other caller changed. That is read from the scripts and one run, not from the next scheduled fire.

## Open for the issuer

Flip the status; read the next failed fire's escalation line (the `| TRACE ...` suffix). Today's 07:00 ET fire is the only real-world evidence so far: it logged
`fg=32116010 != 266432` and no trace, because R7 was not landed yet.
