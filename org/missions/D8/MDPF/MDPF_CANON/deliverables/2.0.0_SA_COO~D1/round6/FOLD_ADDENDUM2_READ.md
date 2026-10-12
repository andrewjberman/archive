# MDPF_CANON round 6 -- fe9b ADDENDUM 2 against the served history (2.0.0_SA_COO~D1, 2026-10-12 ~14:3xZ)

Read-only. Input: CTO msg 4414, ADDENDUM 2 of `RECORD_FE9B_RULED_BY_CLUSTER_LEAD_20261012.md`: if the folded other-models line is itself held at fewer
than 2 firms on a date, suppress it on that date in both series; the read-back asserts every emitted `by_model` line, the fold line included, is held at
2 or more firms. Context: `FOLD_DESIGN.md` @2f702bb7ff (the 11 model-class lines are the fold set; D1, D2 and D3 are asked and unanswered).

## What was measured

Source: the four scopes' latest served `aggregate-aua-timeseries` (as-of 2026-10-09, 494 global dates). The fold set is the 11 model-class lines of
`FOLD_DESIGN.md` section 1. "Held by a firm on a date" = that firm's own `model_value` for a member is greater than 0 on that date.

| measure | value |
|---|---|
| dates on which the other-models line would carry a positive total | 102 (the other 383 are zero or null) |
| of those, held by 2 or more firms (kept) | 47 |
| of those, held by exactly one firm (suppressed under ADDENDUM 2) | 55 |
| the 55 suppressed dates | 2026-05-15 .. 2026-09-09, every one held by inflection alone |
| dollars on the suppressed dates | 26,130,760.13 .. 58,576,784.27 |
| largest share of `opal_aggregate_aua` on a suppressed date | 2.79% |
| as-of 2026-10-09 | NOT suppressed (cottonwood and inflection both hold members) |

## Consequence the ruling's text does not state

"Headline sums unchanged" and "suppress the line on that date" cannot both leave the date's identity intact. On each of the 55 dates the other-models
dollars leave `by_model` while `model_aua` and `opal_aggregate_aua` stay. The sum of the global `by_model` model-class lines then falls short of
`model_aua` by that date's dollars (the shortfall equals the suppressed line's value, 26.1M to 58.6M). Before the fold that identity held on 479 of 485
valued dates (`FOLD_DESIGN.md` section 1). The W-7 `account_count_total` sums `by_model`, so it falls short of the headline count on the same 55 dates, or
the build holds the count by a second rule.

Under D1(a) the same date-set question returns for the fold line: its own multi-firm epoch is later than the core lines' (2026-09-10 on this read), so the
guard's date set is per line, not one global epoch.

## What this asks (one decision, not mine)

Whether the identity `sum(by_model model-class lines) == model_aua` is allowed to open on the 55 historical dates of the first folded object (and every
later one, since each served object carries its whole history), or the suppressed dollars are carried in a stated residual field. A new field adds a JSON
key, which the ruling forbids; so the options are (1) accept the gap and scope the build's identity assertion to dates where the fold line is emitted, or
(2) keep the individual one-firm lines on the 55 dates and fold only from the fold line's own multi-firm epoch, which leaves the one-firm disclosure
the ruling removes standing in the history arrays. REC: (1), stated in-band as the suppressed date set.

## After ADDENDUM 3 (msg 4418, arrived while this was written)

D1 is ruled (b): fold per date, so the core lines also leave `by_model` on the 383 dates 49financial held them alone (2024-11-01 .. 2026-05-14), and the
guard's flip count is zero by construction. Two effects on this read:
- The identity gap above is no longer 55 dates but 383 + 55 = 438 of 485 valued dates, and on the 383 the gap is the core lines' full dollars, not 2.79%
  of the headline. The ruling accepts "Global has no per-model lines before 2026-05-15"; the build's identity assertion is scoped to the dates a line is
  emitted, and the suppressed date set is stated in band.
- FOLD_DESIGN.md section 6 measured the Model Portfolios page on the as-of only. Its trend reads the global `by_model` history
  (`rollBlendsIntoArchetypeSeries`), so the per-model trend of a folded object starts 2026-05-15 on the core lines. That is a client-visible change beyond
  the -185 and -$43.16M the CTO accepted; it is put to him as a separate item, with the reader read he asked for (which readers open a pre-fold dated object).

Not done by this read: a build. The A4 conflict rule keeps the 135 served dated keys as they are in either case.
