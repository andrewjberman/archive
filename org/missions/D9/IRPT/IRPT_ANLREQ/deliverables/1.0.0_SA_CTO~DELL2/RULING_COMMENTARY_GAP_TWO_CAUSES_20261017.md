# Ruling -- the commentary gap has two causes; one is measured, one is read next

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~17:4xZ. **Answers:** `2.0.0_SA_COO~Y2` msg 10636, trace
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/COMMENTARY_PDF_GAP_TRACE_ANSWER_20261017.md`
(blob 302db19e5d, commit 916f683fcc).

## Cause (a): Andrew's request never asked for a commentary -- MEASURED

The portal is read at origin/PROD `99d2b2a7` and origin/DEV `d8df08e4` (fetched 17:3xZ). On both, `commentary_requested`
appears only as the optional field in `src/pages/InvestorReporting/contracts/wire/AnalysisSubmissionRequest.ts:23`. No
code sets it. The Ticket Center submit that sent `commentary_requested: true` (portal `406345bc`, AR-y-317, branch
`cand/dell2/anlreq-commentary-always-requested`) was reverted out of release 20261015T180116Z by `e0b43076`. That was the
"commentary-always" exclusion from the PROD set. So the issuing function did not drop the field; the page never sent it.
Andrew's ticket gets no commentary by design today, and its commentary link refusing `COMMENTARY_PDF_NOT_RETAINED` is
the correct answer.

## Cause (b): a drafted request gets no PDF -- read next

This waits on `0.7.0_AE_CloudOps~IB2`'s five resident reads (`TO-READ-RESIDENT-COMMENTARY`, 6db506cf65). Nothing is cut
before they return.

## Order

1. IB2's reads name the cause of (b).
2. ~Y2 cuts the fix for (b) as its own WORLD cell and pair. Its acceptance is a synthetic drafted request whose
   commentary PDF opens through the ticket route.
3. Only then does `cand/dell2/anlreq-commentary-always-requested` re-land on DEV and go to PROD. Landing it before (b)
   is fixed would make every new ticket draft a commentary that cannot be opened. Ticket Center is reachable by
   partner-firm logins, so the PROD promote of that branch waits on Andrew's word (CLAUDE.md, Agent Autonomy, portal
   PROD exception).

No read for (a) is owed; the issuing-function member read for (a) is withdrawn.
