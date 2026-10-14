# HANDOFF -- 2.0.0_SA_COO~V1 (dell1, ETFS_RIVALS), 2026-10-14 ~19:58Z, written ahead of dell1's ~21:00Z restart

A fresh session of this seat resumes here. Session crons and watchers die with the restart; re-arm them (below). Identity: `2.0.0_SA_COO~V1`, project ETFS_RIVALS (D5/ETFS), lease FULL.

## Where it stands (all MEASURED this session)

- **Andrew-direct ~18:5xZ (CTO msg 5712): ETFS_RIVALS is DONE; there is no new round, ever.** Task: drain round 30, write `ledger/COMPLETION_REPORT.round30.json` (the CTO grades; CLOSED flips on R6),
  file missing backfill ranges as DEMQUE rows (DONE: `round30/BACKFILL_GAPS_FOR_DEMQUE.md` @c9e98081a6, corrected to 70 securities @df1130de54; Q1 cut DQ-t-63, msg 5733). Stand-down position for the next seat: write it at the drain.
- **Round 30 is built, merged and deployed.** Cells xa-2 @dff53957e5, xc-2 @8475f46512, xe-1 @47530f3817, xf-1 @03dbf4b128, xe-3 @fb61d59cf4. Deploy `TO-APPLY-R30` complete (@38300e3a5d): five packages live at pin `ea0e5025ac` since 2026-10-14 14:53Z.
  The L8 packet is at CVO~RV1 (@7d58db9f71). `round-close-check --round 30` reads REFUSED on the CVO's two ungraded J1s only. RIV-xe-2 is NOT cut and never will be (no new round).
- Open items: (1) CVO J1 xa-2 and xc-2 on the 2026-10-15 13:00Z sweep page; (2) deploy ledger `etfs-rivalfunds-r30-dell1-20261014` leg L2 (MINE: read the 2026-10-15 11:00Z chain and 13:00Z sweep; close with `python .tools/deploy_ledger.py close-leg --slug etfs-rivalfunds-r30-dell1-20261014 --leg-id L2 --proof "<measured>"`, then `close`);
  (3) row **ETFS_RIVALS-D1-S16 (ARMED, disarm owner this seat)**: the detect-and-void reads before each reader consumes actions (CTO msg 5615): list `gold/corporate_actions/date=*` read-only BY 10:50Z and BY 12:50Z on trading days,
  void any `actions-inferred-*` object found the same tick (`python -m rivalfunds.dramatic_move void --sink s3 --revision <rev> --security-id <sid> --reason <text>` via a CloudOps seat on this seat's word), record each read in `round30/D1_S16_DISARM_READS.md`
  (last read 2026-10-14 15:55Z: 11 plain objects, 0 inferred, 0 void). The row disarms only when the round-31 precedence cell is deployed, and it will not be issued: at the drain, tell the CTO the row needs a named owner or an off-plan stop (see the stand-down).

## Re-arm on startup

1. `/watcher` once (inbox). 2. Hourly `/canonical-drive ETFS_RIVALS` at `:49` (authority: `org/ref/LIVE_ARMS.md` COO row; ETFS_RIVALS is DONE but r30 has not drained). 3. One-shots for 2026-10-15 in LOCAL time (EDT = UTC-4):
the D1-S16 reads at 06:47 and 08:47 local (10:47Z and 12:47Z); an L2/drain tick after 09:30 local (13:30Z).

## The drain, in order (after the 13:00Z sweep on 2026-10-15)

1. D1-S16 reads (above) and record them. 2. Read the first chain and sweep on the pin: `python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/round28/l2_read.py 2026-10-15` (set `PYTHONIOENCODING=utf-8`), the audit page's
sentence beside BIDD, CGIC and SCHY, the verdict openings, and the G5 stage's output; close ledger L2 and the ledger. 3. When the CVO has graded J1 xa-2 and xc-2 (`round-close-check --project ETFS_RIVALS --round 30` MAY-CLOSE), send the L10 slug to
`1.0.0_SA_CTO` (the CTO flips `dep_stage` to ROUND_CLOSE on receipt) (one message, with the CVO watermark and the armed D1-S16 row's owner gap). 4. Write `ledger/COMPLETION_REPORT.round30.json` per `org/standards/COMPLETION_REPORT.schema.json`: 24 FWD rows (the PRD header), `done_when_text` verbatim from the PRD ENDPOINT cards, cells and each task order's
`proof_of_spec_ref` (path@commit; instances under `deliverables/0.9.0_WK_*/` and `0.7.0_AE_*/`), both denominators printed. NOTE: the cell-to-FWD mapping is not recorded as data (146 cells in 12 decomposition files; 115 name no FWD in their own section); derive it mechanically
(paragraph association over decompositions and orders), say so in each note; `FWD-24`'s final act (the switch-on) has no closing-pass order, claim it with a note; FWD-8, 11, 12 are unmapped by text. 5. Remove the kept trees after L2 closes: `git worktree remove C:/tmp/rv-r30-dell1` and `C:/tmp/rv-r30-rollback`.

## Facts a successor would otherwise re-derive

- Gates: the `coo-drive-tick-gate` Stop hook needs `/next-calls ETFS_RIVALS --drive` plus `unblock.py tick` on any turn that fires no act. Commit only through `.tools/safe-commit.sh --author "2.0.0_SA_COO~V1 <2.0.0_SA_COO~V1@opal.agent>" -F <msgfile>`; keep `safe-merge` and `safe-commit` in separate Bash calls (a hook misreads a call carrying both).
- This seat does not push; push state is read with `git ls-remote origin box/dell1` (last read f22c3956f5, 2026-10-14 ~15:00Z).
- `D1_S16`'s disarm needs a CloudOps seat (`0.7.0_AE_CloudOps~DELL1` applied R30) and the `dramatic_move void` CLI. The lookup is live (since 2026-10-09) and has never found a split (0 inferred objects).
- Andrew's four priorities (relay msg 5666) name TCKT, IRPT, ADVI, OPLGTW/MCPINDEX; ETFS_RIVALS is not among them and is DONE.
