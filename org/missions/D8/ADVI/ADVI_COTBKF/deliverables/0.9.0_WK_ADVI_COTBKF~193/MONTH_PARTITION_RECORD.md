# MONTH_PARTITION_RECORD -- ADVI_COTBKF TO-CB-cy-2 (round 103), worker 0.9.0_WK_ADVI_COTBKF~193

Read-only. Counts only; no account id, name or dollar value. Served objects at the pinned VersionIds:
`daily_returns` lNzQMjfx6uX2zdFdWKsDANboShtDUz2N, `month_grades` nkTE.F82uFSboXr9PEamIENCwFL9cwcC.
Machine record: `MONTH_PARTITION_RECORD.json` (this folder). Own reproduction: `cy2_own_partition.py`, output in `OWN_REPRODUCTION_OUTPUT.txt`.

## Partition of the 78,622 UNGRADABLE months (disjoint, assigned in the issuer's order)

| category | months |
|---|---:|
| no_daily (no daily_returns row) | 116 |
| blank_only_unpriced (blank days, all UNPRICED, no reported-side clause) | 72,184 |
| blank_only_other (blank days, one not UNPRICED, no reported-side clause) | 1,563 |
| blank_and_reported (blank days and a reported-side clause) | 3,818 |
| reported_only (no blank day, a reported-side clause) | 941 |
| other | 0 |
| **sum** | **78,622** |

The issuer's script (`cy2_month_partition.py`) gives the same six counts; `MONTH-CROSS partition_equal=True fill_bound_equal=True`.

## Overlap matrix (UNGRADABLE months)

| has blank day | has reported-side clause | has no daily row | months |
|---|---|---|---:|
| no | no | no | 0 |
| no | no | yes | 86 |
| no | yes | no | 941 |
| no | yes | yes | 30 |
| yes | no | no | 73,747 |
| yes | no | yes | 0 |
| yes | yes | no | 3,818 |
| yes | yes | yes | 0 |

Blank-day months: 73,747 + 3,818 = 77,565. No-daily months: 86 + 30 = 116.

## Blank-reason sets (the 77,565 blank-day UNGRADABLE months, from the daily rows)

- only UNPRICED: 73,093
- UNPRICED with at least one other reason: 2,856
- only other reasons: 1,616

The month reason text names only the first blank reason in date order, so these sets are taken from `daily_returns`, not from the text.

## Fill bound

`fill_upper_bound` = 72,184 (the blank_only_unpriced category): the most months that could grade if every UNPRICED blank day received a price and nothing else changed. Every other category keeps a blocking reason (no daily row, a non-UNPRICED blank, or a reported-side clause).

The bound is not a promise that any of those months would match, and it is not conditional on whether a vendor covers the securities (round 103's other cell measures that). The earlier UNPRICED-first count of 74,791 in row D1-S18 is above this exact bound because it includes the 3,818 blank-and-reported months and the 1,563 months with a non-UNPRICED blank.

## Checks

- Sensitivity: 0 UNGRADABLE months carry the clause `reported value is null` (module line 118, not in the partition's four fragments); 0 reason clauses fall outside the module's emitted texts. Row filed: `ADVI_COTBKF-D1-W193-S1` (OBSERVATION, INERT).
- Blank-day months in `daily_returns` total 77,570; 77,565 of them are UNGRADABLE months, so 5 sit outside this census (their verdict was not read).
- Blank_reason null rows: 0 of 1,584,413 blank days.
