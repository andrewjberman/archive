# NON_POSITIVE_BASE re-grade (CB-r-1)

Rule (CTO ruling, row D2-W35-S2): a day whose prior-day value is zero OR negative reads BLANK with reason NON_POSITIVE_BASE; a month holding one is UNGRADABLE (the monthly grade's rule for any blank day); never interpolated. BEFORE = a zero prior-day value blanks (ZERO_BASE), a negative one is computed. AFTER = prior-day value <= 0 blanks.

## Blank days by reason

| reason | before | after |
|---|---|---|
| FIRST_DAY | 1533 | 1533 |
| FLOW_UNVALUED | 5 | 5 |
| NON_POSITIVE_BASE | 0 | 29603 |
| UNPRICED | 1560217 | 1560217 |
| ZERO_BASE | 2578 | 0 |
| (all blank) | 1564333 | 1591358 |

Days with a negative prior-day value (previously computed): 27044

## Graded months

| grade | before | after |
|---|---|---|
| MATCH | 1973 | 1685 |
| DIFF | 2264 | 1931 |
| UNGRADABLE | 78356 | 78977 |
| (all) | 82593 | 82593 |

NON-POSITIVE-BASE days_blanked=29603 months_before=1973/2264/78356 months_after=1685/1931/78977
