# IRPT_BCKEND round 4, workstream ~PO (the Orion pairs RE-CUT on the located writer) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~07:3xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @519b5ccbfb on the CTO's msg 8127: IB-pr-560 `complete` (merged @0ea9b3e1d2, flip @05b996a0eb). `python .tools/round-close-check.py --project IRPT_BCKEND --round 4 --workstream "~PO"` reads `MAY-CLOSE`. I re-ran IB203-1 AC1 to AC3 on the worker tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY: nothing was changed, pulled, started, stopped or written to AWS, and no Orion request was made.**

## What the CVO needs to know

- **The design and the packet V2 exist** (`deliverables/0.9.0_WK_IRPT_BCKEND~404/IB203-1_orion_recut_design.json`, `ORION_RECUT_PAIRS_PACKET_V2.md`, 12,881 characters, supersedes V1, both halves UNSIGNED): (b) re-times the existing chain into the 06:00 New York fold with no new function and no port; (a) re-runs the absent trading days through the chain's pull steps; the manual CLIs are retired with a message naming the chain.
- **Two findings stop the ACT (not the read), and both go to the CTO, who ruled on a design these facts contradict:**
  1. **(a) cannot run as ruled.** The catalog rows of `INF_API_PULL_POSITIONS_DAILY`, `INF_API_PULL_TXN` and `INF_API_PULL_PERF` carry no date token and `run_chain` refuses `--run-date` for date-agnostic steps, so a past day cannot be re-run through the chain's own steps (row W404-S3, BLOCKING). The day lists also differ from the calendar: of the seven positions days only four are trading days without a flat key (the other three hold a parquet key only); 13 transactions trading days hold no flat key, six of them 2026-05-04 to 2026-05-11, which my order did not list (W404-S1, S2). The 36-day denominator is mine and must be recomputed.
  2. **(b)'s timing is unmeasured.** Every flat write on record lands 11:39 to 11:56Z; a 06:00 New York fold starts the chain about 1 h 39 min before the earliest measured pull, and Orion's T-1 completeness at 06:00 was not measured (W404-S6, ARMED). The silver aggregator that fires the trigger has no source directory in the repository, so its change cannot be designed from source (W404-S5, BLOCKING).
- **Other rows:** W404-S4 ARMED (the dispatch script exists only as an S3 object, not versioned); W404-S9 ARMED (the pull branch logs WARN and returns success when a pull fails, so a day's key can stay absent while the chain reads complete); S7, S8, S10 stale comments (INERT).
- **Not cut and why:** the build slices wait on the CTO's answer to the two findings; the Scope-account addendum waits on B-IN's feed (CTO msgs 8110, 8112).
- **Carried ARMED (owner me):** D2-W403-S3, D2-S184, D2-W394-S2, D2-W392-S2, W349-S1, W361-S1, W348-S2, W368-S2, plus W404-S4, S6, S9; D2-S158 with the CTO. Scratch awaiting Andrew's word (recursive deletes): `_scratch403`, `_scratch404`, and the earlier directories (open call dell2-20261015T014138Z-53cb).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
