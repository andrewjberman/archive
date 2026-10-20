# MDPF_DEMQUE round 9: L10 input, DRAFT (2.0.0_SA_COO~Q1, 2026-10-20)

STATUS: DRAFT. Round 9 is not finished: TO-DQ-t70 (AC2 dated to the 2026-10-24 14:00Z fire) is open; TO-DQ-t34 closed 2026-10-20 (see below). This file is the carry list the L10 slug will cite. It is not the slug and it sends nothing. `python .tools/round-close-check.py --project MDPF_DEMQUE --round 9` read MAY-CLOSE at 2026-10-20 ~21:4xZ (50 orders, 48 complete).

## Carry items for the round-10 enrichment list

| # | item | source | state |
|---|---|---|---|
| 1 | The drawer's budget-ledger double count: the untagged history figure adds the production budget ledger, which holds the drawer's own draws, surface draws included; a late-evening local draw can land under the next UTC day. | row `MDPF_DEMQUE-D1-W64-S2` (ARMED, disarm owner this seat), remediation `MDPF_DEMQUE-D1-C-S30` (OPEN, round v9); `standing_drawer.py` lines 185-193 at HEAD | STILL-PRESENT per `ARMED_ROWS_AUDIT_20261020.md` (@2931618b88) |
| 2 | `bbg_backfill.run` passes no `drawn_surface_today`, so a surface-tagged request it runs is capped by the wrong room. | row `MDPF_DEMQUE-D1-W64-S1` (ARMED) | STILL-PRESENT in code; reachable only by a direct `run()` call (main refuses every date but 2026-10-10) |
| 3 | 238 of 483 stored names carry a trade before their stored window and are appended with no identity check; how many also have no trade in the appended window was never measured. | row `MDPF_DEMQUE-D1-W50-S10` (ARMED); `daily_draw.py` lines 197-198, 213-214, 311-313 | STILL-PRESENT; a design residual of the ruled second rule (1029c04f3c); needs a count before a ruling |
| 4 | An ETFS_RIVALS landing cell, so a DEMQUE draw of a rival funds request reaches the page store. | decomposition amendment 34 (2026-10-17), "CARRIED TO ROUND 10" | not cut |
| 5 | The sweep stops on a sparse window: the 2026-10-20 16:00 ET sweep drew 1,911 cells, ended SPARSE-STOP on `MDPF_SECHIST-CARD-A-B1-OPTION-C` (21 empty windows) and left 2,479,598 of the daily total unspent. Andrew's ruling is that whatever is left of the daily total is drawn. | `REPORT_XB-20261020T184711Z-6e6e.md` @72874e7b8c (on `box/sitez`); rows `MDPF_DEMQUE-Z-S10`, `MDPF_DEMQUE-D1-W67-S1` | observed once; whether an empty window should cool and continue is the CTO's call |
| 6 | DQ-t-79 names no outcome for an empty-window trigger that arrives with no room left for one health-probe cell. | row `MDPF_DEMQUE-D1-W68-S1` (INERT) | open question |

## Already dispositioned this round

The CVO disarmed eight ARMED rows at 2026-10-20 13:24 ET (@13d2f5d992). Row `MDPF_DEMQUE-D1-W35-S3` (the commit-time client-data list absent on dell1) is the MSTR's.

## What the slug waits on

1. t34: DONE 2026-10-20 17:54 ET. The seat committed its proof instance and flipped the order `complete` (@983474921d, via cross-box call `XB-20261020T211229Z-0fb9`); the issuer re-ran `proof-of-spec-check.py` on the instance at 22:4xZ: VALID (rc=0). 49 of 50 orders complete.
2. t70: `dq_t70_fire.py` reads FIRE-OK on the 2026-10-24 14:00Z fire.
3. `round-close-check.py --round 9` reads MAY-CLOSE on the merged tree, and the four ARMED rows above carry a disposition.
