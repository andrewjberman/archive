# LGIC_NAMING.TO-LN-t-1 -- result (0.9.0_WK_LGIC_NAMING~2)

Cell `LN-t-1`: the costed ranking (PRD candidate N7; FWD-6).

## What was produced

`org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md`, commit `3497a41c31` on branch
`wk-lgic-naming-1-2`: the ten rows of Part IV.7 of `docs/briefs/d14-naming-schema-brief-20260913.md` at `1b42dbe758`,
in the brief's order and with its ranks. Each row states what it costs today (what breaks, what someone has to do by
hand, or what it blocks), with the figure beside it from the brief or `infra/logic/09_NAMING_CENSUS.md`, section
cited. The file ends with one fenced json block, `{"rows": [...]}`, ranks 1..10. No row is re-ranked and no
remediation is minted.

Two rows have no figure in the named sources, and each says so: row 3 (key grammar; the census defers to
`01_CENSUS.md`) and row 10 (Terraform labels and tags; unmeasured by census section 5). Row 5 states that the census
table breaks down 145 of the 339 `LIVE-no-DECLARED` nodes by type and not the other 194.

## Criteria

| id | invocation | deciding output | denominator | verdict |
|---|---|---|---|---|
| T1-AC1 | `check_ln.py t1-ten` | `VERDICT: PASS-TEN-COSTED` | 10 of 10 rows ranked 1..10; 0 without surface or cost | PASS-by-output |
| T1-J1 | read of TENSION_RANKING.md @3497a41c31 | recorded, no verdict | 10 of 10 rows costed; 8 carry a figure, 2 state none exists | RECORDED (judgment; 3.0.0_SA_CVO at L9) |

## Surprises

None filed.
