# aw-1 AMENDMENT 1 condition (a) names five functions, but the 11:00Z chain invokes four

**Seat:** `0.7.0_AE_CloudOps~DELL1` -- **2026-10-09 ~09:0xZ** -- read-only, APPLIED NOTHING
**Order:** `ETFS_RIVALS.TO-APPLY-R28-aw1.rivalfunds-lambda-deploy-sitez` (steps 4-6 wait on the 11:15Z-12:50Z window)

## The condition, verbatim

> (a) the five rivalfunds Lambdas' runs of the 11:00Z chain have each logged a REPORT line in CloudWatch Logs
> (all five functions the chain invokes that day; print each REPORT line whole);

## What the trigger graph actually is

The five functions have **exactly two entry points**, and they are EventBridge **Scheduler** schedules, not Rules
(`events list-rules` returns 153 rules, 5 of them `rival*`, and **none** carries a `ScheduleExpression` -- the
schedules live in the separate `scheduler` API, which is why a rules-only read would have found no 11:00Z trigger
at all):

| entry | expression | timezone | target |
|---|---|---|---|
| `etfs-rivalfunds-daily` | `cron(0 7 ? * MON-FRI *)` | America/New_York = **11:00Z** today | `etfs-rivalfunds-fetch-holdings-lambda` |
| `etfs-rivalfunds-sweep-daily` | `cron(0 9 ? * MON-FRI *)` | America/New_York = **13:00Z** today | `etfs-rivalfunds-daily-lambda` |

The five marker rules chain the rest, and **not one of them targets `etfs-rivalfunds-daily-lambda`**
(`list-targets-by-rule` on all five, printed per rule):

- `rivalfunds-build-silver-on-marker-created` and its `-bloomberg-` twin -> `rivalfunds-build-silver-lambda`
- `rivalfunds-build-canonical-shape-on-marker-created` and its `-bloomberg-` twin -> `rivalfunds-build-canonical-shape-lambda`
- `rivalfunds-publish-page-on-marker-created` -> `rivalfunds-publish-page-lambda`

So the 11:00Z fire reaches **four** functions: fetch-holdings, build-silver, build-canonical-shape, publish-page.

## The measurement that settles it

Yesterday, Thu 2026-10-08, REPORT timestamps in UTC:

- `etfs-rivalfunds-fetch-holdings-lambda` -- **1** REPORT, `11:00:33Z`. The chain fire.
- `etfs-rivalfunds-daily-lambda` -- **4** REPORTs: `00:12:06Z`, `01:43:49Z`, **`13:08:18Z`**, `15:09:39Z`.
  **None inside 11:00Z-12:50Z.** The 13:08Z one is the 09:00 ET sweep; the other three are off-schedule invocations.

`etfs-rivalfunds-daily-lambda` therefore does not run as part of the 11:00Z chain, and its scheduled fire is
**13:00Z -- after the 12:50Z apply window closes**. Read literally, condition (a) is unsatisfiable inside the
window on any normal day: the fifth REPORT cannot exist yet when the apply must already be done.

## The reading I recommend, and why it is probably the intended one

The order's own step 4 already assigns the 13:00Z sweep elsewhere:

> L2 is the verify, the 13:00Z sweep of 2026-10-09; the issuer reads it and closes it.

That is `etfs-rivalfunds-daily-lambda`'s run. So the order already treats that function's fire as the **post-apply
verify leg owned by the issuer**, not as a pre-apply condition. Condition (a)'s "five" looks like it folded the
post-apply sweep into the pre-apply health check.

**Recommended:** (a) is met by the **four** functions the 11:00Z fire invokes, each with a clean REPORT and no
failure marker; `etfs-rivalfunds-daily-lambda` stays where step 4 already puts it, in the issuer's L2 read of the
13:00Z sweep. I will not adopt that reading on my own -- the issuer rules.

## Non-application

This says nothing about whether the apply should happen. Conditions (b), (c) and (d) are untouched and I read them
in the window as written.

## The instrument, committed so the window is one invocation

`org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/aw1_window_conditions_ab.py` reads (a) and (b) together:
auto-paginates `filter-log-events` to exhaustion, prints each REPORT line whole, parses Duration against the
720,000 ms cap, sweeps for `Task timed out` / `Status: timeout` / `errorType` / `Unhandled`, prints its denominator,
and keeps **"could not read the group"** separate from **"read it, found none"**. Exercised on yesterday's window
BEFORE being relied on, where it correctly returned a STOP naming `etfs-rivalfunds-daily-lambda` as the function
with no REPORT -- which is how this finding surfaced.

Two traps it cost to find, both named in the file so the next reader does not pay them again:

1. `.tools/aws` is an MSYS shell script, so a bare `subprocess.run` of it dies `FileNotFoundError [WinError 2]`.
   CLAUDE.md's remedy (`.tools/msys_argv_guard.py msys_safe_run()`) is what the file uses.
2. The schedules are in **America/New_York**, so "11:00Z" and "13:00Z" are DST-dependent renderings of 07:00 and
   09:00 ET -- they become 12:00Z and 14:00Z in EST. Today is EDT, so the order's arithmetic holds; the script takes
   its window as an argument rather than assuming it.

Confirmed before relying on any of it: 2026-10-09 is a **Friday** and `trading_calendar.is_trading_day` reads
**True**, so the MON-FRI schedule does fire today.
