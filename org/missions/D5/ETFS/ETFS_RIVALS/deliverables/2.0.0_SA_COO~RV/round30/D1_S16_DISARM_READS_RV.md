# Row ETFS_RIVALS-D1-S16 (ARMED) -- the detect-and-void reads taken by 2.0.0_SA_COO~RV

Continues `deliverables/2.0.0_SA_COO~V1/round30/D1_S16_DISARM_READS.md` (the disarm owner moved to `2.0.0_SA_COO~RV` with the lane, CTO msg 6116). Same rule (CTO msg 5615): list `gold/corporate_actions/` read-only; an `actions-inferred-*` object found is voided the same tick by a CloudOps seat on this seat's word.

| read at (UTC) | by | prefix | objects | actions-inferred-* | actions-void-* | act |
|---|---|---|---|---|---|---|
| 2026-10-15 ~18:2xZ (LATE: the 10:50Z and 12:50Z reads were not taken, the seat was dark until 18:09Z) | 2.0.0_SA_COO~RV | `gold/corporate_actions/` (paginated LIST) | 12, all plain `actions-<rev>` (newest `date=2026-10-14/actions-20261014-c833c167b849.parquet`, written 14:35:33Z) | 0 | 0 | none owed. Objects are append-only and none is inferred now, so none was present at 10:50Z or 12:50Z unless one was deleted (not read). The 13:00Z daily Lambda log carries 0 `dramatic_move` lines. |
