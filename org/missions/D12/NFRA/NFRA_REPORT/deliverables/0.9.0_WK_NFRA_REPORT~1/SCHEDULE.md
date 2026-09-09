# SCHEDULE AND DELIVERY — trading days only, before Andrew's morning (cell RP-s-3, outcome FWD-1)

Authority: `NFRA_REPORT_PRD.md` manifest row S3 (`FWD-1`), `C-TRADING-DAYS`, and CLAUDE.md NEVER#4
verbatim: *"NEVER call a pipeline stale or broken until you resolve the TRADING CALENDAR... Friday IS
Monday's answer. One frontier: `lib/trading_calendar.py`."* This cell **specifies which frontier the
schedule must key on and why** — it does not edit any scheduler, detector, or calendar source; none of
those is in this cell's write surface, deliberately (bound, verbatim).

## 0. THE MEASURED FAILURE THIS LAW MUST NOT REPEAT

**Brief F2, carried verbatim into this cell:** the current detectors are **weekday-aware, not
trading-day-aware** — Monday–Friday is not the same set as NYSE trading days, because a market holiday
that falls on a weekday (Labor Day, Thanksgiving, etc.) is a weekday but not a trading day. **The report
sent on Labor Day, 2026-09-07.** Labor Day 2026 falls on a Monday — a weekday by every calendar-day or
weekday-only rule, and NOT an NYSE trading day. **This is the exact and only failure mode `C-TRADING-DAYS`
exists to close: a weekday check will pass on a market holiday every time; a trading-day check will not.**

## 1. THE LAW

**The report lands ONLY on trading days, before Andrew's morning. NEVER a calendar-day subtraction.**
A schedule keyed on weekdays, or on a fixed cron with no calendar check at all, is out of compliance
regardless of how it is otherwise timed. The check that decides whether today's edition sends is a
single boolean question — *is today an NYSE trading day* — answered by the ONE frontier this document
names in §3, never re-derived locally by any consuming schedule.

## 2. THE BASENAME TRAP — five files, one frontier, and the defect that reintroduces itself one layer down

**A resolved-path census, not a name census:** `comp-find --name 'trading_calendar.py'` returns
**5 hits** across the repo (denominator: 5 of 5, re-confirmed at `--corpus raw`, the maximal scope, same
count):

1. `lib/trading_calendar.py`
2. `lib/tests/test_trading_calendar.py`
3. `infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm/trading_calendar.py`
4. `infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py`
5. `infra/aws/lambda/opal-assets-absence-check/trading_calendar.py`

**Naming the frontier by BARE basename (`trading_calendar.py`) cannot distinguish any of these five from
one another — a cell, or a scheduler, that resolves the wrong one PASSES its own "I checked the trading
calendar" self-report and still sends on a market holiday, which is exactly the defect this cell exists
to fix, one layer down (battery finding, verbatim).** This is why `C-TRADING-DAYS`'s frontier must be
named by its full, resolved, repo-root-relative path: **`lib/trading_calendar.py`**, never a bare
`trading_calendar.py`.

## 3. WHICH OF THE FIVE IS THE FRONTIER, ON EVIDENCE — not the plausible pick

A pattern match on the basename cannot discriminate between the five; all five satisfy it equally. The
determination below is made on CONTENT, not on the name:

- **`lib/tests/test_trading_calendar.py`** is a test module (`lib/tests/`), not a calendar
  implementation — it asserts behavior of another module rather than defining a calendar. Excluded on
  its own directory and role, not merely its name.
- **The three `infra/aws/lambda/*/trading_calendar.py` copies were diffed, byte-for-byte, against
  `lib/trading_calendar.py`:**

  ```
  diff lib/trading_calendar.py infra/aws/lambda/bd-pipeline/bd-served-vintage-alarm/trading_calendar.py       -> 0 lines of difference
  diff lib/trading_calendar.py infra/aws/lambda/inf-pipeline/inf-etf-ownership-daily/trading_calendar.py      -> 0 lines of difference
  diff lib/trading_calendar.py infra/aws/lambda/opal-assets-absence-check/trading_calendar.py                 -> 0 lines of difference
  ```

  **All three are byte-identical to `lib/trading_calendar.py` at this vintage.** This is the evidence
  that they are VENDORED DEPLOYMENT COPIES of one canonical source — each Lambda's own zip package must
  bundle its own dependencies, so the same module is physically duplicated into three deploy trees — and
  not three independent, competing implementations of trading-day logic.
- **`lib/trading_calendar.py` is the canonical source**, evidenced three ways: (a) it is the one CLAUDE.md
  NEVER#4 names explicitly, by this exact resolved path; (b) it is the one under `lib/`, the repo's
  general-purpose shared-library location, rather than under any single Lambda's private deploy tree;
  (c) it exposes the actual API a scheduler needs — `is_trading_day(date) -> bool`, docstring *"True iff
  `date` is a NYSE trading day (weekday + not a NYSE holiday)"* — read directly from the module, not
  assumed.

**THE FRONTIER, RESOLVED — and resolved is not the same word as bare.** A repo-relative fragment like
`lib/trading_calendar.py` is only a correct pointer FROM the repo root; read from anywhere else, or
handed to a consumer that resolves paths against its own working directory, it can silently miss or
(worse) hit a different file. **The fully resolved path is anchored at the repo root, derived, never
hardcoded** — CLAUDE.md's own rule on device-specific paths (`LD-0405`) is explicit that the workspace
root is obtained via `git rev-parse --show-toplevel`, never written as a literal absolute path, because
this worktree's own top-level folder name (`wk-NFRA_REPORT-1f`) is this worker's ephemeral identity, not
a stable one any other consumer shares. **Written here as `toplevel/lib/trading_calendar.py`** — `toplevel`
standing for `$(git rev-parse --show-toplevel)`, exactly the way a `~`-prefixed path stands for
`$HOME` without hardcoding it — this is the resolved frontier: not a bare basename, not a plausible
guess among five identically-named candidates, and not a device-specific literal either.

## 4. A DECLARED LIMIT ON THAT DETERMINATION — named, not hidden

**Byte-identical TODAY is a measured snapshot, not a structural guarantee.** Nothing observed here
enforces that the three vendored Lambda copies stay in sync with `lib/trading_calendar.py` if the
canonical source is ever patched (a new NYSE holiday added, a leap-year fix, etc.) without each Lambda's
deploy bundle being re-vendored. **This cell's law binds the REPORT's OWN schedule to import or read the
canonical `lib/trading_calendar.py` directly — never one of the three vendored copies, and never a
locally re-implemented weekday check** — precisely because a fix to the canonical source is otherwise
not guaranteed to reach every consumer, and the report's schedule must not be one of the consumers a
future drift silently strands.

## 5. What a compliant schedule does, stated as law (no scheduler is built or edited here)

- Before sending, call the canonical frontier's `is_trading_day(today)` (or the equivalent
  trading-day-aware helper it exposes) — **never** a weekday check (`date.weekday() < 5`), and **never**
  a calendar-day subtraction (`today - N days`) to find "yesterday's" edition or window.
- If today is not a trading day, the report does not send today, full stop — no fallback to "send
  anyway on a weekday."
- Delivery lands **before Andrew's morning**, on trading days only — this document does not fix a clock
  time (that is a scheduling/infra parameter, not a law this cell owns); it fixes WHICH CALENDAR decides
  whether today is a sending day at all.

## 6. What this document does NOT do

- Does not edit `lib/trading_calendar.py`, any of its three vendored copies, its test, or any scheduler
  or detector source — none is in this cell's write surface (bound, verbatim), and none was touched.
- Does not build a new scheduler, EventBridge rule, or cron expression — this is a LAW cell (`align`
  lane per the PRD manifest), not a wiring cell.
- Does not claim the three vendored copies will always match the canonical source going forward — §4
  states that limit explicitly rather than presenting a one-time diff as a permanent guarantee.
