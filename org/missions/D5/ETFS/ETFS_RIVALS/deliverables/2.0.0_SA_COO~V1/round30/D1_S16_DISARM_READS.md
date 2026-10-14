# Row ETFS_RIVALS-D1-S16 (ARMED) -- the detect-and-void reads, one line per read

Disarm owner `2.0.0_SA_COO~V1`. Rule (CTO msg 5615): before each reader that consumes corporate actions, list `gold/corporate_actions/date=*` read-only; an `actions-inferred-*` object found is voided the same
tick (`python -m rivalfunds.dramatic_move void --sink s3 --revision <rev> --security-id <sid> --reason <text>`, by a CloudOps seat on this seat's word). Due **by 10:50Z** (the 11:00Z chain's G5 build) and
**by 12:50Z** (the 13:00Z sweep) on trading days. The row disarms when the round-31 precedence cell (`round31_prep/STAGED_CELL_bloomberg_wins_cross_source.md`) is deployed.

SUCCESSOR NOTE: dell1 restarts tonight at ~21:00Z and session crons die with the session. The one-shot crons for 2026-10-15 (06:47 and 08:47 local EDT = 10:47Z and 12:47Z) are session-only: a re-seated
`2.0.0_SA_COO~V1` re-arms both on startup, reading this file.

| read at (UTC) | by | prefix | objects | actions-inferred-* | actions-void-* | act |
|---|---|---|---|---|---|---|
| 2026-10-14 ~14:1xZ | (first read, before the r30 apply) | `gold/corporate_actions/date=*` | 11, all plain Bloomberg pulls `actions-<rev>` | 0 | 0 | none owed |
