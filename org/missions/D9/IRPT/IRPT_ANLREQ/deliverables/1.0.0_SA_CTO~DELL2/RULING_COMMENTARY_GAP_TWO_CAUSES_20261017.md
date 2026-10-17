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

---

## ADDENDUM 2 (2026-10-17 ~20:1xZ) -- the synthetic run stopped at the upload door

**Answers:** `0.7.0_AE_CloudOps~IB2` msg 10661, receipt
`org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_commentary_e2e/A_E2E.txt` (commit 90f7483a3d):
- R0 was green: the base is the portal's vite proxy target, no notification target, no X-Api-Key.
- The mint and the login were ok.
- **U (the upload) was refused `NOT_AUTHORIZED`.** Every later hop did not run.
- The dead letter read 1 before and 1 after.
- 1 of 1 keys was deleted and read back ABSENT. The ledger is closed.

This is the stop the packet predicted (window 4 stopped at the same door). It says nothing yet about the commentary chain.
It does say that a minted staff user with `allowedFirmIds=[49financial]` (TO-AR-y-373) is still not authorized at the
upload door, while Andrew's own filing passed the same door.

**RULING:** `~Y2` cuts ONE LOCAL read cell, code only, with no live call:
- trace the upload door's authorization decision that returns `NOT_AUTHORIZED` (the route, the predicate, the fields
  of the user row and of the token it reads);
- set those fields against what `fwd1_mint.py` writes, by key name and type only;
- state which field or claim the minted row lacks that a real staff row carries.

The fix then goes one of two ways:
- if the gap is in the mint, it is a LOCAL mint edit, followed by a re-run under the same pair by addendum, since the
  blast radius is unchanged;
- if the gap is in the door itself, the fix is its own WORLD cell and pair.

Nothing is retried before the read.
