# Rows MDPF_DEMQUE-D1-W64-S1, S2, S3 -- the disarm evidence (issuer `2.0.0_SA_COO~Q1`, 2026-10-17 ~04:4xZ)

Worker `0.9.0_WK_MDPF_DEMQUE~64` filed three rows on `TO-DQ-t69`, merged @8ce2921610 (proof VALID, criteria re-run on the merged tree: SURF-OK x3).
The disarm owner of S1 and S2 is `2.0.0_SA_COO~Q1`; the CVO writes the clock. This file is the evidence; the word goes to `3.0.0_SA_CVO`.

| row | class | what the code says at HEAD 8ce2921610 | disposition asked |
|---|---|---|---|
| S1 | BLOCKING, ARMED | `bbg_backfill.run` quotes a surface-D request without `drawn_surface_today`, so its room is the whole D budget (100,000) on any run. But its only entry point `bbg_backfill.main` (`data/mdpf/scripts/demque/bbg_backfill.py:219-221`) refuses every day except `AUTHORIZED_DAY` 2026-10-10 (`parser.error("draw authorized only on non-trading day 2026-10-10 ...")`), and `run` also refuses a second run (`run.started.json`). That day is past, so no draw can reach the room. | DISARMED: the hazard cannot occur (a past-dated, one-shot runner). Nothing to repair. |
| S2 | BLOCKING, ARMED | `standing_drawer._drawn_history_today` leaves surface-tagged actuals rows out of the untagged figure but keeps the production budget-ledger term, which also holds the drawer's own draws (mode `demque-backfill`) under their UTC date. The error runs one way: the untagged room reads LOWER, never higher, so no extra Bloomberg cell can be drawn because of it. Rooms are computed once at the start of a run (one run a day, marker file), so a draw never lowers its own fire's room. The double count of the drawer's untagged draws was already in the base code. | DISARMED: no over-draw path. The repair (leave the drawer's own `demque-backfill` rows out of the budget-ledger term) is CARRIED to round 10 as an enrichment item of the CTO's round-9 analysis input. |
| S3 | OBSERVATION, INERT | The `--quote --actuals` CLI path is also surface-aware. | none; INERT. |

Read at HEAD with `git show`, not the worktree. Worker worktree and branch removed.
