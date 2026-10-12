# FAMILY_SPLIT -- the date convention by fund family (round 74, CB-bv-1)

Measurement only. Nothing was fetched. No pricing rule or correction is proposed: the convention belongs to validation only.

Rule written first at 2026-10-11T20:32:11Z (full text in FAMILY_SPLIT.json `rule`).

## Headline

Under the rule written first (2026-10-11T20:32:11Z) the date convention is not established by family. The reviewer row reproduces: 12 of the 15 day-before funds and 1 of the 17 same-day funds are American Funds (30 of the 101 funds; 13 of them decided: 12 before, 1 same). American Funds is the only family of the first-two-words reading with 5 decided funds; it reads `before` (12 of 13 decided, 0.92; pooled informative cells 102 before-only to 18 same-only on 25 funds, 0.85). Every other family has fewer than 5 funds, so none is read; reading = not_established (only one family has a convention; the fund sitting against it: CMLAX). Held out, on the 17 undecided American Funds funds alone, 15 before-only to 10 same-only informative cells (0.60): `not_confirmed` under the rule, neither a refutation nor a confirmation; post hoc, the 529 plan funds are 10 same-only to 0 before-only and the A and F funds 15 before-only to 0 same-only. Rival splits: the share class read from the description, the sponsor (first word) and large-against-rest each classify 0.875 of the decided funds correctly (leave-one-out), the same as the family; the share class cannot be told from the family on these funds. The sponsor reading reads `by_family` under the same rules (American before, Fidelity same, DFA same, one fund against). Kind, substituted, period and the ticker letter separate less. Why a family's rows would be dated a day later is not established.

## Reviewer row reproduced

12 of 15 day-before funds and 1 of 17 same-day funds are American Funds (first two words of the custodian description). Reading under the rule: **not_established**. Funds against their family: CMLAX.

## Families (first two words; families under 5 funds folded)

| family | funds | decided same | decided before | undecided | pooled same-only | pooled before-only | both equal | funds with informative cells | convention |
|---|---|---|---|---|---|---|---|---|---|
| AMERICAN FUNDS | 30 | 1 | 12 | 17 | 18 | 102 | 94 | 25 | before |
| other (60 families) | 71 | 16 | 3 | 52 | 178 | 44 | 504 | - | not_established |

## Held-out test inside American Funds (17 undecided funds)

Under the rule the held-out test is `not_confirmed`: 25 informative cells on 12 of the 17 undecided funds, 15 before-only against 10 same-only (0.60 before-only; the line is 0.75). By fund 7 lean before and 5 lean same. The decided funds of the family give 87 before-only against 8 same-only.

| share class (post hoc) | funds | funds with informative cells | same-only | before-only |
|---|---|---|---|---|
| 529 | 6 | 5 | 10 | 0 |
| A | 9 | 5 | 0 | 12 |
| F | 2 | 2 | 0 | 3 |

## Other splits (leave-one-out accuracy on 32 decided funds; no split 0.531; family 0.875)

- R1: share class letter of the ticker: accuracy 0.688 against 0.875, does not separate as well as family.
- R2: share class from the description: accuracy 0.875, equal to the family; confounded with family (every A/F/C/529 decided fund is in the large family).
- R3: open or closed end: accuracy 0.531, no better than no split (one closed-end fund among the 32).
- R4: substituted or left on the store: accuracy 0.688 (substituted 10 same / 3 before; left 7 same / 12 before): a partial separation, below the family.
- R5: period: by fund accuracy 0.625; by cell no period separates (the large family holds before-only and the rest same-only in every period).
- R6: sponsor (first word): accuracy 0.875, equal to the family; reads by_family under the rule (Fidelity and DFA same, American before).
- R7: large family against all others: accuracy 0.875, equal to the family (built from the lead, so not independent).

## Not established

- The convention is not established by family under the rule: only American Funds has 5 decided funds under the first-two-words reading; the other 71 funds sit in 60 families of 1 to 3 funds each, so every other family is `not_established` for too few funds, not because it was tested and found mixed.
- That the convention is a property of the family is not established. The 13 decided American Funds funds are the whole of the decided funds with an A, F, C or 529 share class, so family and share class cannot be told apart; and inside the family the 529 plan funds (1 decided same, 5 more with informative cells, all same-only) lean the other way from the A and F funds. This is a post hoc lead.
- Why a family's rows would be dated a day later is not established: no ex-date, record-date or pay-date field is read, and no transfer-agent or processing-path field is read.
- The family is read from a description string (the first two words, or the first word), not from a sponsor field; one CUSIP carries one first-two-words value (0 of 101 carry more than one), but the string is a proxy.
- The cache window starts 2020-06-29; most reinvestment dates of the older funds fall before it and are not compared (round 73: 944 compared cells of 1740), which is why 69 of 101 funds stay undecided (the held-out American Funds funds have 38 compared cells in all).
- The sponsor reading by_family is a rival result under a coarser name; it classifies the decided funds as well as the first-two-words family and no better. Fidelity and DFA read `same` on 6 and 5 decided funds, the largest fund supplying 0.23 and 0.22 of the pooled cells.
- No pricing rule and no correction is proposed; the convention belongs to validation only. Nothing was fetched.
