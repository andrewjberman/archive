# ETFS_POSITIONING L1-3 -- ISOLATION, EXERCISED

**Seat:** `0.0.0_AB_MSTR~Z` · **2026-08-21 ~1058Z** · **Work order:** `1.0.0_SA_CTO`, ETFS_POSITIONING L1
**Criterion:** *"isolation EXERCISED once (forced ETF-leg failure, models leg green, reverted)"*
**Subject:** `integrations/bloomberg/pipeline/scheduled_daily_pull.cmd` @`49501d1e55`

## VERDICT: EXERCISED, with a negative control that fires.

| case | chain exit | expected |
|---|---|---|
| instrument control (`rc37.cmd`) | **37** | 37 |
| **NEGATIVE CONTROL** -- models publish 20, ETF ok | **20** | 20 |
| baseline -- ETF rc 0 | **0** | 0 |
| **MUTANT** -- ETF rc 62 | **0** | 0 (isolated) |
| **MUTANT** -- ETF rc 63 | **0** | 0 (isolated) |
| both -- publish 20 + ETF 62 | **20** | 20 (ETF must not displace) |

Harness log files written at 10:58:45/46/47 -- **positive evidence the chain executed**, not an
absence of errors. Production untouched: the harness is a copy with the three models-leg
invocations stubbed and the ETF invocation repointed at a controllable rc.

## HOW THE HARNESS WAS KEPT FAITHFUL

Anchor assertions before any edit (`PRECOND`/`PULL`/`PUBLISH`/`ETF` each asserted to exist at
**exactly one** site; a multi-site or zero-site match REFUSES). Structure re-asserted after the
edit, code-anchored: `^:etf_leg` x1, `^goto :etf_leg` x1, `^set RC_ETF=` x1, `^set RC=` x3
(unchanged from live).

## THE FIRST FOUR RESULTS WERE FABRICATED, AND ONLY THE NEGATIVE CONTROL SAID SO

**`cmd.exe /c` from Git Bash: MSYS converted the `/c` FLAG into a path.** cmd opened an
interactive shell, printed its banner, and returned **0**. Baseline and both mutants "passed."
The chain had never executed.

> **THREE PASSES LOOK IDENTICAL WHETHER THE HARNESS WORKS OR NEVER RUNS.** The negative control
> refusing to produce a 20 is what exposed it; the confirmation was that **no new log file
> existed**. A pass set with no failing member is not evidence -- it is an untested instrument.

**Then I broke it a second way:** applied `MSYS_NO_PATHCONV=1` **and** `//c` together. Each works
alone; the combination does not. **Two fixes at once masked which one was needed.** Measured:

    MSYS_NO_PATHCONV=1 + //c  -> 0   (broken)
    MSYS_NO_PATHCONV=1 + /c   -> 42  (works)
    bare //c                  -> 42  (works)

**Third failure:** `\"$W\"` inside a double-quoted bash string reached cmd as literal `\"` --
`'\"C:\...\iso.cmd\"' is not recognized`. Fixed by passing env vars through bash (which cmd
inherits) instead of a `set X=..&&` chain.

## THREE OF MY OWN GUARDS FIRED, AND EACH WAS RIGHT

1. **Anchor assertion refused** -- an unquoted heredoc had turned `\b`/`\a` into backspace/bell
   inside the anchor strings (`\x08loomberg`, `\x07uth`). Authoring moved to the Write tool.
2. **Structural assertion refused** -- my own unmeasured `== 2` for `:etf_leg`. The true count is
   **3**: `goto` at :170, **prose mention inside my own REM block** at :195, label at :210. The
   assertion was re-anchored to code so a comment cannot satisfy it.
3. **Instrument control** -- `rc37.cmd` returning 37 is what licensed reading any other number.

## SIDE EFFECT, NAMED

The harness wrote three log files into the production log directory
(`%USERPROFILE%\opal_bbg_logs`, 10:58:45-47). Harmless and rotation-bounded at 30, but real, and
recorded here so nobody later finds unexplained logs between the 07:00 fires.

## WHAT THIS DOES NOT CLOSE

**L1-2** (three consecutive scheduled fires) is inherently three days; first fire 2026-08-22 07:00.
**L1-4** (manifest window continuity) needs two consecutive runs. This record closes **L1-3 only.**
