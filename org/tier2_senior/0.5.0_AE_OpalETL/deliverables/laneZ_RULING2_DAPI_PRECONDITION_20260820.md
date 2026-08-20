# Ruling-2 — DAPI-liveness PRECONDITION on the 07:00 ET Bloomberg pull (site Z)

**Seat:** `0.5.0_AE_OpalETL~Z` · **Date:** 2026-08-20 (design + build + exercise 12:2x–12:4xZ) ·
**archetype:** IMPLEMENT

## Authority, verbatim chain

| link | record |
|---|---|
| Andrew RULED YES | 2026-08-19 ~20:2xZ at the CTO~Z terminal, *"Your recs are accepted"* on the /open-calls card whose REC was "Yes" — `org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_ANDREW_DIRECT_20260819_OPENCALLS_RECS_PLUS_D8_FABRIC.md` @f45e5db124, ruling 2: *"07:00 ET pull DAPI-liveness precondition + BG's exercised signin-recovery runbook as the defined recovery path — RULED YES. A canonical-routes-and-schedules definition, explicitly NOT an alarm."* Discharges `OPAL_ANALYST_PRD.md` §9.9 item 1's park. |
| Owner routing | MSTR~Z 20260819T205716Z: *"YOU are the owner … formalize the DAPI-liveness precondition in the scheduled chain + wire the runbook … as the named recovery path — no alert machinery (moratorium; the schedule's exit contract stays the failure surface)."* Both hard bounds: (1) not before the 08-20 07:00 acceptance; (2) after my D6 rows. |
| Scope note | MSTR~Z 20260819T214255Z (from CTO~Z's first comp-adversary compose, note 214220Z / @15636c285e): the chain has TWO measured failure classes — **(1) DAPI-down (terminal logged out / bbcomm dead) = MINE**; (2) WDAC/env (policy-blocked binary, conda-meta resurrection, niche-wheel tail) = Andrew's deferred MSP-exemption frame, NOT mine. **Design bar: the limbs stay DISTINGUISHABLE in the exit path** — a DAPI-liveness PASS followed by a pull crash must not read as precondition failure, and the precondition must never absorb an env failure into "DAPI was fine". |
| Bounds cleared | (1) acceptance PASSED — MSTR~Z @91fe6afbca (BG 07:15 backstop, all four legs green), corroborated on-box by `%USERPROFILE%\opal_bbg_logs\bbg_tplus1_20260820_070001.log` (the fallback signed the Terminal in live at 11:00:41Z, `DAPI FALLBACK EXIT: 0`, pull + publish OK, served `data_as_of 2026-08-19`); (2) D6 TO-F authored+delivered+CTO~Z-prelim-validated, TO-G enum-certified (3 desks) — my 08-19 log. MSTR~Z 20260820T122512Z: *"NO re-sequencing, proceed"*; COO~Z 122501Z: *"ruling-2 proceed as you framed."* |

## What was there, and what the ruling adds

`scheduled_daily_pull.cmd` already ran the LD-0413 precheck + unattended sign-in fallback
(`bbg_credentials.py -- powershell … bbg_fallback.ps1`) before the pull — **but the pull ran
REGARDLESS of that exit** (`:71` logged it, `:74` pulled). The fallback's contract (`bbg_fallback.ps1:12-14`)
is `0` = DAPI up (was, or self-healed) · `2` = down and NOT self-healed (escalation record written).

The ruling makes the exit LOAD-BEARING: a **precondition** that gates the pull, names the recovery
path, and keeps the two limbs distinguishable in the task's exit contract.

## The design (as landed in `scheduled_daily_pull.cmd`)

```
fallback rc 0      -> PRECONDITION: PASS -- DAPI UP                     -> :pull
fallback rc 2      -> one dapi_check.py re-check (the transient the P0 gate itself names)
                       re-check 0  -> PRECONDITION: PASS on re-check   -> :pull
                       re-check !0 -> PRECONDITION: FAILED -- PULL NOT ATTEMPTED
                                      RECOVERY PATH: <BG runbook> + backstop Step-2 one-liner
                                      + the fallback's escalation record path
                                      set RC=50 -> :prune -> exit /b 50
fallback rc other  -> PRECONDITION: INSTRUMENT ERROR rc=N -- NOT a DAPI verdict -> :pull
                      (limb 2 territory; the pull proceeds and ITS rc is the evidence)
```

- **`50`** is the new, distinct task exit for *precondition FAILED, pull not attempted*. It collides
  with nothing in the chain's contract (`0` · `9` missing interpreter/runner · pull rc · publisher
  `1/20/30/40` · argparse `2`). BG's 07:15 backstop reads `LastTaskResult` (its Step 1 instrument,
  `STANDING_ORDER_0715_DAILY_BACKSTOP.md`); `50` routes it straight to its Step 2 = the runbook.
- **Label-based flow, no parenthesised blocks** — the cmd's own documented parsing hazard
  (`:117-120`).
- **Nothing notification-shaped.** No alarm, no SNS, no monitor. The exit code + the log line are
  the surface (moratorium, Andrew-direct 2026-07-28; MSTR~Z's assignment restates it).
- **The WDAC/env limb is deliberately NOT absorbed**: an instrument error proceeds to the pull, so an
  env-class failure surfaces as the pull's own failure (limb 2), never as "DAPI down" (limb 1) and
  never as "DAPI fine".

### Taken in the same pass (COO~Z 122501Z + MSTR~Z 122512Z both routed it here)
The fire-once ledger `~/.bbg_signin_attempts.json` labelled today's **unattended** Task-Scheduler
submit `SUBMITTED-SUPERVISED-MSTRZ` — `bbg_signin.ps1:173` hardcoded that string on every row.
A misleading record in the exit contract's own evidence, not a guard defect (the fire-once guard
counts attempts regardless of label). Fix, 2 lines: `bbg_fallback.ps1` sets `BBG_SIGNIN_CALLER=bbg_fallback`
immediately before its submit; `bbg_signin.ps1` labels `SUBMITTED-UNATTENDED-FALLBACK` when that is
set, else `SUBMITTED-SUPERVISED`. Existing rows keep their historical label. No guard logic touched.

## Build-correctness — exercised BEFORE the port (run-and-read, nothing standing)

| # | exercise | result |
|---|---|---|
| 1 | anchored edit script: every replaced line asserted against what was read first | first attempt **refused** — the Bash heredoc collapsed one level of `\\` before Python saw it (`\\b` → backspace); **nothing was written**. Re-run from a Write-tool file: `cmd anchors OK (141 lines, CRLF=True)` · `fallback anchors OK` · `signin anchors OK`; written 141→188 / 102→103 / 185→189 lines. |
| 2 | PowerShell AST parse of both edited `.ps1` (`Parser::ParseFile`) | `bbg_signin.ps1 errors=0` · `bbg_fallback.ps1 errors=0` · **positive control** (a deliberately unbalanced copy) `errors=3` |
| 3 | ledger label expression evaluated both ways | caller-set → `SUBMITTED-UNATTENDED-FALLBACK`; unset → `SUBMITTED-SUPERVISED` |
| 4 | LIVE re-check instrument, pull interpreter: `C:\Anaconda\envs\cma\python.exe dapi_check.py` | `DAPI: UP (session + SPX Index/PX_LAST returned -- entitled session live)` rc=0 |
| 5 | LIVE precondition leg **exactly as the cmd invokes it** (line-70 form, credentials-injected) | `[fallback] DAPI UP -- proceed with pull, no sign-in needed.` rc=0 in 3s; ledger (2 newest rows) + escalation file (tail) **unchanged** — no side effect |
| 6 | cmd branch harness, 8 scratch variants, heavy legs stubbed to marker+rc, re-check REAL in B / stubbed DOWN in C+H | **8/8 PASS** (denominator 8): A pass→pull→publish rc0 · B rc2 + live re-check UP → "PASS on re-check", pull ran · **C rc2 + re-check DOWN → "PRECONDITION: FAILED", "PULL NOT ATTEMPTED", runbook path in log, no pull/publish marker, rc=50** · D rc7 → "INSTRUMENT ERROR rc=7 -- NOT a DAPI verdict", pull ran, rc0 · **E NEGATIVE CONTROL = HEAD cmd, rc2 → pull ran anyway, rc0 (the old code does not gate — the harness discriminates)** · F PASS + pull rc3 → "PULL FAILED rc=3", rc3, no "PRECONDITION: FAILED" (limbs distinguishable) · G PASS + publisher 20 → "PULL OK but PUBLISH rc=20", rc20 (existing label flow unchanged) · H rc2 + re-check rc9 → FAILED, rc50 |

Harness defect found + fixed in passing: the cmd's log stamp is per-SECOND, so two variants in one
second shared a filename and the second `>` overwrite read as "0 new logs" — per-variant log dirs.
(The production chain fires once a day; not a production concern.)

## Port + live exercise
- Direct port on my lane (no shadow, no comparator): the three files + this record + the README
  amendment, one commit. Commit hash in the session log.
- **Live exercise = the 08-21 07:00 ET fire + BG's 07:15 read.** Expected on a healthy morning: the
  new log carries `PRECONDITION: PASS -- DAPI UP …` (or the sign-in lines then PASS) and everything
  downstream reads exactly as today. The FAILED path is exercised only by a real down; it is NOT to be
  manufactured (fire-once, lockout risk — the spec's test-plan constraint stands).

## Not done / not mine (stated, not silent)
- BG's `STANDING_ORDER_0715_DAILY_BACKSTOP.md` Step 1 table + the runbook do not yet mention `50` —
  BG-owned deliverables (BG's G1 fence cannot take a repo edit from me either way); notified at landing.
- `OPAL_ANALYST_PRD.md` §9.9 item 1 annotation "LANDED @…" — CTO~Z holds the ruling record; notified
  at landing with the hash, per MSTR~Z's *"CTO~Z holds the ruling record; cite it at landing."*
- The WDAC/env limb (limb 2) — Andrew's MSP-exemption frame, untouched by design.
- `REPO=`/`PY=` are baked box paths in the cmd (pre-existing, MSTR~Z-authored); this is the one box
  with the Terminal and the Scheduled Task, i.e. device-AWARE by purpose — observed, not chased.

## Compiler tools
`comp-find scheduled_daily_pull` (15 hits / 26,589 files, bands printed) located the chain; `python .tools/comp-adversary compose <this file>` run before landing (declaration attached beside this file: `laneZ_RULING2_DAPI_PRECONDITION_20260820.adversary.md` -- 3/3 cited commits resolve at read-vintage, cited path stable, nothing bearing surfaced); the harness/parse/live-leg instruments above are this session's own, all denominator-printing. No comp-tool models a Windows Scheduled Task's exit contract — the instruments were the task record, the cmd's own log, and the live leg.
