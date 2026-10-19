# IRPT_BCKEND -- where things stand, 2026-10-19 ~19:45Z (issuer 2.0.0_SA_COO~P2, dell2)

For the CTO's "clean statement of where things stand" (Andrew-direct pause record, item 5). Each line carries its CLAIM: MEASURED (read from the served artifact or the code at the stated time), INFERRED, or NOT READ. Counts and class words only; no id, no value.

| # | What | State | Claim | Basis |
|---|---|---|---|---|
| 1 | Holdings, Cottonwood | published, business date and custody as-of 2026-10-16, 0 listed absent-at-source | MEASURED 14:25Z | IB2's first-fire after-read (IB236-1 record) |
| 2 | Holdings, Inflection | published, business date and custody as-of 2026-10-16, 0 listed; the cited snapshots are dated the fire day | MEASURED 14:25Z | same read; ruled STAMPED_T_MINUS_1 on the custody data date (row D2-S244) |
| 3 | Holdings, 49 Financial | served holdings still as-of 2026-10-12; the gate REFUSED the 2026-10-16 candidate on one lost account (it held 18 position rows and 1 balance row on 10-15 and none on 10-16); four refusals since 10-14 | MEASURED 14:25Z; cause re-read in holdings_snapshot.py 3033-3063 | CTO ruling msg 10788: keep the refusal; passes by itself when the account returns at source; next read after the 2026-10-20 14:15Z fire |
| 4 | Directory, Cottonwood | served directory as-of 2026-10-12, over age since 10-14; no build sent since 10-14 | MEASURED 14:1xZ | two causes: (a) the refresh re-read a failed command on every fire (fixed in refresh.py, merged to box/dell2, NOT deployed); (b) the runner guard reads 11 re-keyed accounts as dropped clients (guard change approved by the CTO, msg 10788, NOT built: held by the pause) |
| 5 | Directory, 49 Financial and Inflection | not read this session | NOT READ | no finding either way |
| 6 | HMAC account-id lists | written and format-valid for 49 Financial and Inflection by Monday's scheduled fire; Cottonwood's list is not written (it needs a directory build) | MEASURED | the dell2 principal read one key; ledger leg L6 stays open until Cottonwood's list is written and read |
| 7 | Branches | every IRPT_BCKEND worker branch drained into box/dell2 or archive-tagged and retired; 0 worktrees | MEASURED 18:4xZ | msg to the CTO 17:44Z, MSTR 18:37Z |
| 8 | Open orders | IB-pr-596 (waits on ~N2's repairs), IB-pr-549 (complete, ungraded) | MEASURED | task-order files |

## What is built and not shipped (this project)
- The Cottonwood wedge fix (`refresh.py`, six tests, graded): needs a never-widen pair and a Lambda release by IB2 outside the 11:30Z to 14:15Z band. A pair is new work, so it waits for the pause DONE line.

## What is not built
- The Cottonwood retained-key guard and the readers census (both approved by the CTO; checks r259 and r260 built and controlled; cut at the DONE line, call 481d).

## What Andrew can test on PROD from this project today
- Nothing new: this project has shipped nothing since the pause. Holdings for Cottonwood and Inflection are as-of 2026-10-16; 49 Financial holdings are as-of 2026-10-12 by design until the account returns.

Push state: LOCAL on box/dell2 at the time of writing.
