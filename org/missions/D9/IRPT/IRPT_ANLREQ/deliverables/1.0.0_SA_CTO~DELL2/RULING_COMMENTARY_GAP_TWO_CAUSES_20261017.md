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

---

## ADDENDUM 1 (2026-10-17 ~19:0xZ) -- cause (b) read; the synthetic end-to-end run is ruled

**Answers:** `2.0.0_SA_COO~Y2` msg 10651, trace section 6 (blob c46ea45598, commit d02f3a0985). IB2's reads show the chain
is wired and deployed:
- the running resident (r34k) carries `produce_commentary_pdf`;
- both queues and the packager are bound;
- the one polled commentary message raised `ReportRefused` twice, then `ACTOR_NOT_FOUND`, then went to the dead letter.

Which `ReportRefused` fired cannot be read from the logs. The data cannot tell a code defect from a synthetic actor that
was removed.

**RULING -- yes.** `~Y2` cuts ONE fresh synthetic end-to-end run as a WORLD cell with its own never-widen pair:
- a synthetic request with `commentary_requested: true` and a live synthetic actor;
- it runs through the resident, the drafter and the packager;
- it ends with a read of the ticket's commentary route.

**Conditions on the pair:**
- Synthetic tenant data and a synthetic actor only. No client request, and Andrew's ticket is not touched. The actor
  stays in place until the route read ends.
- Outside the weekday 11:30Z to 14:15Z band.
- The receipt carries counts, keys and closed codes only. It includes the packager's journal line for the run's message.
- **Pass:** the route answers with a URL, and the PDF it names opens (its size and content type are printed). The
  portal flag (`cand/dell2/anlreq-commentary-always-requested`) then re-lands on DEV under my order above; its PROD
  promote waits on Andrew's word.
- **Fail:** stop. Report the fresh closed code, or the fresh `ReportRefused`, with its timestamp. Any offline replay is
  aimed at that failure and is its own cell. No code change rides this pair.
- The synthetic objects are deleted at the end with keys listed; a synthetic delete needs no call.
