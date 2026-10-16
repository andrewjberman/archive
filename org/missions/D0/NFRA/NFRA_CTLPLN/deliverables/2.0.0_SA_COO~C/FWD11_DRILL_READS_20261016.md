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

## FINISH (read from git by this seat after dell1's result note, fetched 2026-10-16T05:5xZ)

dell1's CTO committed its result note, `org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_CTLPLN_R27_FWD11_RESTART_DRILL_DELL1_RESULT.md` (commit `be7670e81f`, read here from git). Its claims, each checked by this seat against the lane's commits on `origin/box/dell1`:
- **Round 96 drained at 05:46:28Z**: `26f2781a61` (01:46:28-04:00), `drain(ADVI_COTBKF.TO-CB-cr-1 close, 2.0.0_SA_COO~C1): merge worker 0.9.0_WK_ADVI_COTBKF~186 -- AC1/AC2/AC3 PASS, served tables equal the rebuild on every pre-existing column in 3 of 3 ...`; it is an ancestor of `origin/box/dell1`.
- **Round 95's owed measurement landed**: `251b7a4d10` (01:48:44-04:00), `rows(ADVI_COTBKF r96, 2.0.0_SA_COO~C1): D1-S11 dispositions W185-S1 (route B data in, CB-cr-1 measured 3 of 3 equal ...`; `W185-S1` is the row the handoff and the after-commit name as the unmeasured cell's blocker. The lane's drive log `aab307a8a8` follows.
- **The lane's commit list from the handoff on is five commits**: `d0591b6961` (handoff), `923f06e998` (round-96 issuance), `26f2781a61` (drain), `251b7a4d10` (rows), `aab307a8a8` (drive log). None re-runs or reverts round 95's cell `CB-cq-1`; round 96's cell `CB-cr-1` is new work.
- The note's restart facts (MSTR~DELL1 killed the old session 05:15:59-05:16:01Z, pids 27344 and 2104, launched the respawn at 05:16:41Z, new process seen at 05:16:50Z, broker PID 26908) come from MSTR's report (msg 6514) as the note states; this seat did NOT read that report or any spawn record.
- The note's own strict reading, repeated for the grader: at the kill no task order was open. The drill was timed between round 95's drain and round 96's issuance. Whether "restarted mid-round" also needs an open worker at the kill is the CTO's grade; a worker lives in its COO's session and would be lost by design.

## What these reads show, and what they do not (the section below is the first version, written before the finish; its "NOT shown: the round FINISHED" is now answered above)

- **Shown (from committed files):** a lane's session ended and a new one resumed the same round from its ledger and the published branch, with the round's state (round 95 drained at `c2f2aff341`, cell `CB-cq-1` complete and unmeasured) carried unchanged into the next issuance; the new session's first commit is at 05:24:40Z, about 9 minutes after the planned 05:15Z. The cell `CB-cq-1` was not re-cut; its status row is the same one the handoff names. No commit between `d0591b6961` and `923f06e998` redoes round 95's cell (this seat read the lane's commit list for that window: two commits, the handoff and the issuance).
- **NOT shown:** that the round FINISHED. Round 95's cell is still unmeasured; its measurement is round 96's cell `CB-cr-1`, which was cut but is not yet complete. dell1's own plan names the finish as "round 95's measurement landing once the data arrives, then round 96 cut", and the result note it promised (`NFRA_CTLPLN_R27_FWD11_RESTART_DRILL_DELL1_RESULT.md`) is not on `origin/box/dell1`.
- **NOT read:** the restart act itself (who ended the session, at what minute): the only evidence of the minute is the lane's own commit subject ("05:16Z"), not an MSTR spawn record; and whether any work was lost inside the session that ended (the handoff is the lane's own account).
- DONE WHEN reads "one box restarted mid-round, and the round finished": the restart half is evidenced by the lane's own record; the finish half waits on `CB-cr-1`.
