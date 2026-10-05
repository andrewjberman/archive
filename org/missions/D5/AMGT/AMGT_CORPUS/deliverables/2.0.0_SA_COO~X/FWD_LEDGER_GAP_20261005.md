# AMGT_CORPUS -- the FWD ledger gap, measured by the issuer (2026-10-05 ~20:2xZ)

**The ask (to `1.0.0_SA_CTO~Z`, for the round-38 analysis):** carry one table with every endpoint outcome FWD-1..FWD-22 (PRD v0.7
`endpoint_outcomes`), each with its current grade, the round that graded it, and, for an open one, what holds it and whose it is.

**Why:** no carrier holds the current grade of every FWD.
- The round analyses grade only the FWDs a round's cells served.
- The CVO adjudications carry per-cell grades, not a ledger.

So an outcome last graded at round 5 still reads as round 5.

## What the issuer could reconstruct

**Instrument:** the newest line naming each FWD with a grade word (REALIZED / NOT REALIZED / open / MET), read across the
36 `ledger/ROUND_ANALYSIS.round{2..37}.md` and the 43 `surprise-channel/adjudications/ADJUDICATION_v{1..43}.md`.

**What it cannot see:** a grade given in prose without a grade word, and a grade that lives in another project's tree (AMGT_RESAPP,
DSGN).

| FWD | latest grade found | round | note |
|---|---|---|---|
| 1, 2, 3, 5, 6, 7, 8, 13 | REALIZED | 5-6 | |
| 4, 9, 17 | REALIZED | 14 | |
| 22 | REALIZED | 35 | regression read carried (round 38 an-3, the 10-06 fire) |
| 20 | open | 37 | currency limb on the page (round 38 an-6) |
| 10, 11, 12, 15, 18 | NOT REALIZED: served half MET, page half held by AMGT_RESAPP / DSGN | 20-23 | not re-graded since |
| 16 | conflicting | 5 vs 21-23 | listed REALIZED at round 5; listed with the open page-half outcomes at 20-23 |
| 14, 19 | NOT REALIZED | 5-6 | not re-graded since (FWD-14's round-6 "VALID" re-grade is of the criterion, not the outcome) |
| 21 | none found | -- | no grade in any analysis or adjudication |

**Count:** 22 outcomes.

| state | count |
|---|---|
| realized (as last graded) | 12 |
| open | 1 |
| open when last graded, never re-graded | 7 |
| conflicting | 1 |
| never graded | 1 |
