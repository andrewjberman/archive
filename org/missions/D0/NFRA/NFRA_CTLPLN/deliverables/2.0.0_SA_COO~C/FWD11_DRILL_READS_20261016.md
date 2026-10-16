# NFRA_CTLPLN round 27 -- FWD-11's deliberate restart drill on dell1: the reads from git, before and after (issuer 2.0.0_SA_COO~C, 2026-10-16 ~05:5xZ)

Call `XB-20261016T045259Z-fbfa` (laptop to `1.0.0_SA_CTO~DELL1`); dell1's reply `org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_CTLPLN_R27_FWD11_RESTART_DRILL_DELL1_20261016.md` (commit `24b1e9d488` on `origin/box/dell1`). The CTO's ask (`ledger/ROUND_ANALYSIS.round26.md` section 3 item 3): a round in flight on one box, the process carrying it restarted at a time that box's CTO names, and the round then shown to finish. Not a whole-box reboot.

## The plan dell1's CTO stated (read from `24b1e9d488`)

Lane `2.0.0_SA_COO~C1` (ADVI_COTBKF); round 95 drained, cell `CB-cq-1` complete but NOT MEASURED (it waits on dell2 run data); restart by `0.0.0_AB_MSTR~DELL1` at 2026-10-16 05:15Z, after a push of `box/dell1` and with no worker in flight. dell1's CTO also states Andrew's 2026-10-14 hold covered a whole-box reboot and is spent; the issuer did not adjudicate that and read no record of the hold being lifted beyond that statement.

## BEFORE (read from git by this seat)

| what | value |
|---|---|
| `origin/box/dell1` tip, fetched 2026-10-16T05:01:34Z | `ea9d265e1b` |
| the lane's last drive log before | `9c4b527390` (2026-10-16T00:44:44-04:00 = 04:44:44Z), `drive-log(2.0.0_SA_COO~C1): ADVI_COTBKF ... round 95 issued and drained, route B ruled` |
| the lane's handoff just before the restart | `d0591b6961` (00:59:26-04:00 = 04:59:26Z), `handoff(2.0.0_SA_COO~C1): ADVI_COTBKF state, the dell2 block and the next acts, ahead of the 05:15Z restart drill`; file `org/tier1_exec/2.0.0_SA_COO~C1/handoff_20261016T0455Z_ADVI_COTBKF.md` |

## AFTER (read from git by this seat, fetched 2026-10-16T05:4xZ)

The lane's first commit after the handoff is `923f06e998` (01:24:40-04:00 = 05:24:40Z), author `2.0.0_SA_COO~C1`: `issuance(ADVI_COTBKF r96, 2.0.0_SA_COO~C1): CB-cr-1 measures the served move on the dell2 run data -- after the 05:16Z restart-drill respawn`. Its message states, verbatim: "State carried across the respawn (CTO msg 6507): round 95 drained @c2f2aff341; its one cell CB-cq-1 (worker ~185) is complete but NOT MEASURED (row ADVI_COTBKF-D1-W185-S1, BLOCKING, inert). Nothing was redone or lost. Resumed from the ledger and branch box/dell1 only." It cuts round 96 (decomposition `ADVI_COTBKF_DECOMP.round96.md`, order `ADVI_COTBKF.TO-CB-cr-1.measure-served-move-on-dell2-run-data.md`) because dell2's run data arrived by Taildrop (route B; zip sha256 `eea61674...2345`, 20,563 files).

## What these reads show, and what they do not

- **Shown (from committed files):** a lane's session ended and a new one resumed the same round from its ledger and the published branch, with the round's state (round 95 drained at `c2f2aff341`, cell `CB-cq-1` complete and unmeasured) carried unchanged into the next issuance; the new session's first commit is at 05:24:40Z, about 9 minutes after the planned 05:15Z. The cell `CB-cq-1` was not re-cut; its status row is the same one the handoff names. No commit between `d0591b6961` and `923f06e998` redoes round 95's cell (this seat read the lane's commit list for that window: two commits, the handoff and the issuance).
- **NOT shown:** that the round FINISHED. Round 95's cell is still unmeasured; its measurement is round 96's cell `CB-cr-1`, which was cut but is not yet complete. dell1's own plan names the finish as "round 95's measurement landing once the data arrives, then round 96 cut", and the result note it promised (`NFRA_CTLPLN_R27_FWD11_RESTART_DRILL_DELL1_RESULT.md`) is not on `origin/box/dell1`.
- **NOT read:** the restart act itself (who ended the session, at what minute): the only evidence of the minute is the lane's own commit subject ("05:16Z"), not an MSTR spawn record; and whether any work was lost inside the session that ended (the handoff is the lane's own account).
- DONE WHEN reads "one box restarted mid-round, and the round finished": the restart half is evidenced by the lane's own record; the finish half waits on `CB-cr-1`.
