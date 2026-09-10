# THE VERDICT, RENDERED IN A REAL EDITION -- checkable against that edition's own rows (cell `RP-s-17`, manifest row `S4`, outcome `FWD-1`, acceptance property 1)

Authority: `NFRA_REPORT_PRD.md` manifest row `S4` (*"The VERDICT rule -- the does-anything-need-Andrew
determination, derived from the rows"*, `FWD-1` ACCEPT property 1: *"On a trading morning the report
states plainly whether anything needs Andrew, and that statement can be checked against the rows"*),
`C-AI` part 3, and Andrew's clause (a). Depends on `RP-s-15`'s composer (drained at `1443d20f78`) and
renders strictly against the edition it produces -- this document mints no new rule, no new vocabulary,
and no new edition of its own.

## 0. WHAT ROUND 1 LEFT UNDONE, AND WHAT THIS CELL ADDS

`RP-s-4`'s `VERDICT.md` (round 1) specified the rule and demonstrated it twice: once against a single
real row cited by hand (`ALERT_DELIVERY.md` sec.4, before any edition existed), and once against a
table explicitly labelled a **hypothetical**, because *"no live daily edition of this report exists yet
to draw a real 'nothing' morning from."* Both demonstrations were honest about that limit.

An edition exists now. `RP-s-15`'s `compose_edition.py` composed `EDITION_SPECIMEN.md` -- **25 rows (24
real + 1 explicitly-labelled illustrative)**, deterministic, re-runnable. This cell's ACT is narrower
than building that edition (that is `S2`, already `RP-s-15`'s): it is to render the verdict THAT real
edition's rows actually produce, and to show -- not merely assert -- that the rendering is CHECKABLE
against the rows beneath it in the same document. `COMPOSER.md` sec.6 says so itself: composing an
edition "does not render the VERDICT rule's own rendering of it (`S4`/`RP-s-17`, also downstream)" --
that is this document.

**Grounding this session, before rendering anything:** `compose_edition.py` was re-run in this worktree
against the same twelve-plus round-1 source deliverables already on disk. The output differed from the
committed `EDITION_SPECIMEN.md` in exactly one line -- the `Composed at (this run)` timestamp (line 1)
-- and nowhere else; the verdict line, the row table, every delta, and both summary counts (`{'unchanged':
10, 'better': 14, 'worse': 1}`) reproduced byte-for-byte. The re-run's working copy was then restored to
the committed version (`git checkout --`) so this cell does not carry an incidental re-composition as
part of its own diff. This is the same reproducibility `COMPOSER.md`'s own charter claims; it was
exercised, not merely quoted, before anything below relied on it.

## 1. THE VERDICT -- COMPUTED, never generated

`EDITION_SPECIMEN.md` sec.1, verbatim:

> **SOMETHING needs Andrew today.**

This is **COMPUTED**, not generated: it is the direct output of `compute_verdict()`, which implements
`VERDICT.md` sec.1's rule verbatim over already-`QUOTED`/`COMPUTED` per-row fields --

```
NEEDS-ANDREW today  IFF  (a row exists with Axis 1 = CHECKED AND Axis 2 = BREACH)
                     OR   (a real row's delta = worse)
```

-- a deterministic function with no step that asks a model to judge, weigh, or interpret anything
(`C-AI` part 3: *"A VERDICT IS COMPUTED, NEVER GENERATED. A model may render it in better English; it
may not decide it."*). This document renders that sentence in readable prose around the computed facts;
it does not choose between `SOMETHING` and `NOTHING` -- `compute_verdict()` already did, deterministically,
before this document existed.

## 2. CHECKABLE -- traceable to the specific rows beneath it, in the same edition

`EDITION_SPECIMEN.md` sec.1 states its own **COMPUTED basis**, and every row it names is a row a reader
can turn to directly, two sections lower, in the identical document:

- **Clause 1 (a live `CHECKED`+`BREACH` row exists): 3 of 24 real rows** --
  - `opal-infrastructure-alerts` (SNS topic) -- sec.2 row, `CHECKED` / `BREACH`, cited to `ALERT_DELIVERY.md`
    sec.4 (the confirmed subscriber's SMS endpoint sits in sandbox status `Pending`, not `Verified` --
    the topic reaches nobody).
  - Cost segment: `inf` (Pipeline tag) -- sec.2 row, `CHECKED` / `BREACH`, cited to `COST_ANOMALY.md`
    sec.1 (+639.6% over the trailing-30d baseline, over the $0.50/day floor).
  - Cost segment: `bd` (Pipeline tag) -- sec.2 row, `CHECKED` / `BREACH`, cited to `COST_ANOMALY.md`
    sec.1 (+37.3% over baseline, over the floor).
- **Clause 2 (a real row's delta is `worse`): 0 of 24 real rows.** The one `worse` delta in the whole
  edition belongs to the row explicitly marked `(ILLUSTRATIVE ONLY -- NOT A LIVE ROW)`, `compute_verdict()`
  excludes it from both clauses BY CONSTRUCTION (it is filtered out before either clause is evaluated,
  per `EDITION_SPECIMEN.md` sec.1's own `GENERATED` note) -- a demonstration fixture can never trip a
  real verdict.

**Why this is checkable, not merely narrated:** a reader does not need to trust this document's account
of the rule. They can open `EDITION_SPECIMEN.md` sec.2's row table directly, find the three named rows
by name, read their `Axis 1`/`Axis 2` cells, confirm each reads `CHECKED`/`BREACH`, confirm no other real
row's delta cell reads `worse`, and re-derive `SOMETHING needs Andrew today` themselves -- because the
verdict is a deterministic function of exactly those cells, stated as such, not a separate claim layered
on top of them. This is the same test `C-AI` part 2 applies to the edition's `GENERATED` prose (strip it
and the table beneath still carries every fact): here it is applied to the verdict sentence itself --
strip this document's prose and `EDITION_SPECIMEN.md` sec.1's own citations plus sec.2's table still
carry the whole basis for `SOMETHING`, unabridged, because that is what this document quotes rather than
re-derives.

## 3. PURELY DECLARATIVE -- no acknowledgement, no escalation, no required response

The rendered verdict above is a statement of fact, never a request. Per Andrew's clause (a) (*"I can
elect to remediate issues or not at my discretion, separate from the greater flow"*) and the bound this
cell was issued under (*"the morning read is PURELY DECLARATIVE. No acknowledgement, no escalation, no
required response, no SLA"*), this rendering:

- Names no deadline, no SLA, no "must be resolved by" date, and opens no ticket or case of any kind.
- Does not require any reader -- Andrew or anyone else -- to acknowledge, reply to, or act on it today
  or any day; the statement stands whether or not it is ever read.
- Would render `NOTHING needs Andrew today` on a future edition where none of the three `CHECKED`/`BREACH`
  rows still hold and no real row's delta is `worse` -- not because the report is granting relief, but
  because the same deterministic rule, run against different `QUOTED` inputs, produces a different
  output. `VERDICT.md` sec.4 states this mechanism and it is unedited here.
- Builds, proposes, or implies no alert, alarm, SNS-send, notification, or escalation mechanism of any
  kind -- the standing moratorium is unaffected and unaddressed by this document.

**A verdict that quietly expected a reply would make Andrew the acceptance instrument for this report --
exactly the defect `FWD-1`'s declarative re-cut exists to remove**, and nothing above asks him to be one.

## 4. WHY THIS RENDERING CANNOT BE "NOTHING" TODAY, AND WHY IT IS NOT MANUFACTURED

`FWD-1`'s own DONE-WHEN bar needs, eventually, at least one real morning where the verdict is correctly
`NOTHING` -- but this cell's bound is explicit that this cannot be manufactured: *"Render the verdict the
real edition's rows actually produce, and if that is SOMETHING, say SOMETHING."* The one composed
edition that exists trips clause 1 on three real rows (sec.2 above); rendering `NOTHING` against those
same facts would be a decision this document is forbidden to make (`C-AI` part 3). So this rendering is
`SOMETHING`, stated plainly, because that is what today's real rows compute -- not because a negative
outcome is unwanted or hard to produce.

The rule's structural capacity for `NOTHING` is not unproven: `VERDICT.md` sec.3 and `EDITION_SPECIMEN.md`
sec.4 already carry a labelled hypothetical table (five rows, none `CHECKED`+`BREACH`, none `worse`) on
which the identical `compute_verdict()` function returns `NOTHING needs Andrew today`. That table is
quoted, not re-derived, here: it is not today's real state, and this document does not present it as
one. `RP-s-16`'s live trading-morning runs are what will eventually supply the real negative FWD-1 asks
for; this cell's job is to render what the one real edition that exists says today, correctly, and that
is `SOMETHING`.

## 5. What this document does NOT do

- Does not compose a new edition, alter `EDITION_SPECIMEN.md`, or re-derive `compute_verdict()` --
  it quotes the one already-composed edition and its already-verbatim rule, per the build ladder.
- Does not add a third clause, a severity weighting, or a model-judged urgency score to the rule --
  `C-AI` part 3 forbids a model from deciding the verdict.
- Does not manufacture, imply, or narrate toward a `NOTHING` verdict against rows that do not support
  one -- see sec.4.
- Does not build, propose, or imply an acknowledgement/escalation/notification mechanism of any kind
  (sec.3) -- the standing moratorium on alerts/alarms/notifications is unaffected.
- Does not claim to satisfy `FWD-1`'s full `EXERCISED` bar on its own -- that bar also needs `RP-s-16`'s
  live trading-morning runs and a real future `NOTHING` morning; this cell renders acceptance property 1
  (the verdict, checkable against the rows) against the one real edition that exists.
