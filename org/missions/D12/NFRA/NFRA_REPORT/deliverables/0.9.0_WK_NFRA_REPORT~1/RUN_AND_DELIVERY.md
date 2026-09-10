# RUN AND DELIVERY -- the composer runs on trading days only, before Andrew's morning (cell RP-s-16, manifest row S3, outcome FWD-1)

Authority: `NFRA_REPORT_PRD.md@1aae9c43fe` manifest row S3 (`FWD-1`, verb `align`), decomposition
`NFRA_REPORT_DECOMP_R2.md` cell `RP-s-16`, `C-TRADING-DAYS`, and CLAUDE.md NEVER#4 verbatim:
*"NEVER call a pipeline stale or broken until you resolve the TRADING CALENDAR... Friday IS
Monday's answer. One frontier: `lib/trading_calendar.py`."* Dependency `RP-s-15` (the composer,
`compose_edition.py`) is observed complete in this worktree at
`org/missions/D12/NFRA/NFRA_REPORT/deliverables/0.9.0_WK_NFRA_REPORT~1/` and is used here
UNEDITED -- this cell does not touch the composer's own logic, only what decides WHEN it runs and
WHERE its output would need to go.

## 0. THE MEASURED STARTING STATE (inherited, not re-derived)

**Brief F2, carried verbatim from `NFRA_REPORT_PRD.md@1aae9c43fe` row S3:** the detectors are
weekday-aware and NOT trading-day-aware -- **it sent on Labor Day, 2026-09-07.** Labor Day 2026
falls on a Monday: a weekday by any Monday-Friday check, and not an NYSE trading day. This is the
exact and only failure mode `C-TRADING-DAYS` exists to close, and it is the same measured failure
round 1's own schedule cell (`RP-s-3`) recorded. **Round 1 produced twelve specification
documents and no engine** (`NFRA_REPORT_DECOMP_R2.md` sec.0); `RP-s-15` built the engine
(`compose_edition.py`); this cell is the one that makes the engine's OWN execution obey the same
law round 1 only wrote down.

## 1. THE FRONTIER -- inherited from round 1's schedule cell, not re-derived

`SCHEDULE.md@5ec7f6649b` (cell `RP-s-3`, round 1) already ran the resolved-path census this cell's
own BOUNDS repeats verbatim: **five files share the basename `trading_calendar.py`.** Three under
`infra/aws/lambda/*/trading_calendar.py` are byte-identical vendored deployment copies of one
canonical source; `lib/tests/test_trading_calendar.py` is a test module, excluded on role; **the
canonical source is `lib/trading_calendar.py`**, evidenced by CLAUDE.md's own explicit citation,
its location under the repo's general-purpose shared-library path, and its exposed API
(`is_trading_day(date) -> bool`, docstring *"True iff `date` is a NYSE trading day (weekday + not
a NYSE holiday)"*, `lib/trading_calendar.py@0cbb0ad174:81`).

**Naming the frontier by bare basename cannot discriminate between the five candidates.** Per
`SCHEDULE.md@5ec7f6649b` sec.3 and this cell's own BOUNDS, the frontier is named here the same way:
anchored at a DERIVED repo root, never a hardcoded literal and never a bare basename --
`toplevel/lib/trading_calendar.py`, where `toplevel` stands for `$(git rev-parse
--show-toplevel)`, resolved fresh by whatever process imports it (never this worker's own
ephemeral worktree path, which is worker-specific and not shared by any other consumer,
CLAUDE.md `LD-0405`). This document does not re-run the byte-for-byte diff across the three
vendored copies -- that census is `SCHEDULE.md@5ec7f6649b`'s and is inherited, per this cell's own
BOUNDS ("you inherit it rather than re-deriving it").

## 2. THE GATE -- built and RUN, for real, not only specified

Round 1's `SCHEDULE.md` was a LAW document: it named which frontier a compliant schedule must key
on and explicitly built no gate. This cell's ACT says *"the composer runs on TRADING DAYS ONLY"* --
so this cell builds the smallest possible gate around the unedited composer and RUNS it, three
ways, rather than only asserting in prose that such a gate would work.

**The artifact:** `run_gate.py`, next to `compose_edition.py` in this same deliverables directory.
It resolves `toplevel/lib/trading_calendar.py` by deriving the repo root
(`git rev-parse --show-toplevel`, run from the gate script's own directory -- never a hardcoded
path), imports `is_trading_day()` from it, and:

- if the gating date is **not** an NYSE trading day: does **not** invoke the composer, prints why,
  and exits `0` -- no fallback to "run anyway, it's a weekday" and no calendar-day subtraction
  anywhere in the gate;
- if the gating date **is** an NYSE trading day: invokes `compose_edition.py` exactly as a human
  would (`python compose_edition.py`, subprocess, unedited), producing a real, freshly-timestamped
  `EDITION_SPECIMEN.md`.

**RUN 1 -- the exact failure this cell exists to close, re-created and shown fixed, this session:**

```
$ python run_gate.py --date 2026-09-07
OK: frontier = <toplevel>/lib/trading_calendar.py
OK: calendar_source = NYSE/hardcoded-fallback-2024-2027
OK: gating date = 2026-09-07
SKIP: 2026-09-07 is not an NYSE trading day (lib/trading_calendar.is_trading_day) -- the composer
is NOT run and NO edition is produced or delivered today. This is the exact case that a
weekday-only check got wrong on 2026-09-07 (Labor Day, a Monday).
rc=0
```

`--date` is a demonstration/test hook only (named as such in the script's own docstring); a real
trading-morning trigger calls `run_gate.py` with no `--date` and gates on the day it actually runs.
2026-09-07 is a Monday -- a weekday-only check (`date.weekday() < 5`) would have returned True and
run the composer; `is_trading_day()` returns False because `lib/trading_calendar.py@0cbb0ad174`
carries `2026-09-07` in its NYSE holiday table (Labor Day). **This is the trading-day check the old
detector did not have, exercised against the exact date it got wrong.**

**RUN 2 -- a weekend, for the same reason a weekday-only check is not sufficient either direction:**

```
$ python run_gate.py --date 2026-09-05
OK: gating date = 2026-09-05
SKIP: 2026-09-05 is not an NYSE trading day ...
rc=0
```

**RUN 3 -- a real trading day, no override, the composer ACTUALLY invoked:**

```
$ python run_gate.py
OK: frontier = <toplevel>/lib/trading_calendar.py
OK: calendar_source = NYSE/hardcoded-fallback-2024-2027
OK: gating date = 2026-09-10
OK: 2026-09-10 IS an NYSE trading day -- running the composer for real.
OK: wrote <toplevel>/org/missions/D12/NFRA/NFRA_REPORT/deliverables/0.9.0_WK_NFRA_REPORT~1/EDITION_SPECIMEN.md
OK: 25 rows composed; verdict=SOMETHING needs Andrew today
OK: delta counts -- {'unchanged': 10, 'better': 14, 'worse': 1}
rc=0
```

**This is not a dry run.** `EDITION_SPECIMEN.md` in this same directory carries the fresh
`Composed at (this run)` timestamp from RUN 3 -- diffed against its pre-RUN-3 state, exactly one
line changed (the timestamp), confirming `COMPOSER.md@5d808488f0`'s own claim ("re-running it
reproduces `EDITION_SPECIMEN.md` byte-identically apart from its composed-at timestamp") and
proving the gate calls the real, unedited composer rather than a stub.

**What the gate does not do, by construction:** create, modify or delete any CloudWatch alarm, SNS
topic, subscription or EventBridge rule. Every command it runs is either a local git read
(resolving the repo root), a local Python import, or a subprocess invocation of a script already
in this cell's own write surface. The standing alerting/monitor moratorium (`comp-schedule` C3,
carried into this decomposition sec.4) is unaffected -- nothing here mints an alert.

## 3. DELIVERY -- before Andrew's morning, and the declared limit on what this cell can do about it

**The ACT's second half -- "delivered before Andrew's morning" -- is a DIFFERENT question from the
gate above, and this cell's own write surface answers it only partway, named here rather than
silently assumed closed.**

This cell's paths are five documentation surfaces (deliverables, the decomposition, the PRD, a
round-N-analysis doc, and this project's own investigation file) plus this cell's own task-order
file. **None of them is an infra, scheduler or messaging path.** No EventBridge rule, Lambda
trigger, cron entry, SNS topic or subscription can be created, edited or repaired from inside this
cell's write surface, whatever the BOUNDS permit in principle -- the same declared limit round 1's
`SCHEDULE.md@5ec7f6649b` sec.6 stated for itself ("does not build a new scheduler ... this is a LAW
cell, not a wiring cell"), restated here because it still applies to a cell whose verb is also
`align`.

**What was checked, so the BOUNDS clause ("repairing an existing non-delivering egress is
permitted") is answered on evidence rather than left untested:** this project's own
`ALERT_DELIVERY.md@3919310a37` (cell `RP-s-6`) already swept every SNS-backed alarm target in the
account for exactly this question -- alarm to topic to CONFIRMED human-reaching subscriber -- and
found that **of the seven alarm-backed SNS topics in the estate, zero are affirmatively shown, end
to end, to reach a human today**: three have zero confirmed subscribers, one (`opal-infrastructure-
alerts`) has a confirmed subscription whose only leg is an SMS endpoint stuck in `Pending` sandbox
verification, and three route through a Lambda or SQS consumer whose own downstream notification
behavior was not traced. There is no existing egress in this estate, reachable from this cell's
paths or otherwise evidenced here, that is currently known to deliver a message to a human at all
-- so "repair an existing non-delivering egress" cannot be exercised as a concrete repair by this
cell: there is no verified-working destination to point the composer's output at, and no path in
this cell's write surface to fix the ones that are broken even if there were.

**What this cell asserts as LAW instead, for whoever does hold the infra/scheduler write surface
next:**

- The recurring trigger that invokes the composer every morning **must** gate on
  `toplevel/lib/trading_calendar.py`'s `is_trading_day()` (via `run_gate.py` or an equivalent that
  imports the same canonical module) -- never a bare weekday cron, never a calendar-day
  subtraction, and never one of the three vendored Lambda copies of the frontier module.
  `SCHEDULE.md@5ec7f6649b` sec.4 already named the risk of a vendored copy drifting from the
  canonical source if only the canonical source is patched; this cell's gate imports
  `lib.trading_calendar` directly rather than embedding its own copy, for that reason.
- Delivery must land **before** Andrew's morning on a trading day, and must not land at all on a
  non-trading day -- the gate in section 2 already enforces the second half; the first half (a
  concrete clock time) is a scheduling parameter this document does not fix, consistent with
  `SCHEDULE.md@5ec7f6649b` sec.5's own statement that a LAW-lane cell fixes WHICH CALENDAR decides
  a sending day, not the clock time within it.
- **No new alert, alarm, topic, subscription or notification may be created to carry this
  delivery.** If an existing SNS topic is ever repaired to a genuinely CONFIRMED, human-reaching
  state (for example, completing SMS sandbox destination verification, or adding a working
  non-SMS subscriber to one of the three zero-subscriber topics), that repaired, already-existing
  topic is a legal delivery target under this cell's BOUNDS; minting a new one is not, regardless
  of how convenient a fresh topic would be.

## 4. What this document does NOT do

- Does not edit `lib/trading_calendar.py`, any of its three vendored copies, its test, or
  `compose_edition.py` itself -- none is in this cell's write surface, and none was touched.
- Does not create, modify, subscribe to, or repair any SNS topic, CloudWatch alarm or EventBridge
  rule -- no infra/messaging path is in this cell's write surface, and the standing moratorium
  forbids minting any of them from anywhere.
- Does not wire the recurring, unattended trigger that would call `run_gate.py` every trading
  morning without a human running it by hand -- that is a scheduler-plane act outside every path
  this cell owns, named as law in section 3 rather than built.
- **Does not close the `EXERCISED` bar `FWD-1` needs.** `NFRA_REPORT_DECOMP_R2.md` sec.5 point 6
  states this precisely: *"A cell can produce the edition; it cannot produce the reading."* This
  cell produces a real, gated, trading-day-aware edition (section 2) and states the law an
  unattended trigger and a repaired egress must both satisfy (section 3) -- it does not, and by
  its own write surface cannot, put that edition in front of Andrew on a real trading morning
  going forward. That gap is not hidden by the gate having run cleanly three times above.
