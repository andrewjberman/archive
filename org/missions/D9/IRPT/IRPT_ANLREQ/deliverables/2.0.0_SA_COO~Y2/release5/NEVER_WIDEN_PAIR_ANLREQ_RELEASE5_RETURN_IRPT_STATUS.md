# NEVER-WIDEN PAIR -- IRPT_ANLREQ release 5's RETURN: irpt-status from ONE tree, carrying release 5's members and the ticket binding

**COO half, written by `2.0.0_SA_COO~Y2` on dell2, 2026-10-11. WRITTEN AND HELD: nothing here is applied, and no apply order is cut,
until section 2's precondition reads true.** It supersedes the working packet beside it
(`NEVER_WIDEN_PAIR_ANLREQ_RELEASE5_RERELEASE_IRPT_STATUS.md`, revisions 1-4), whose after-reads it carries forward.
The CTO half binds to this file's blob hash.

Claim words: MEASURED = this seat ran or read it; RECORD = a worker's committed record this seat opened; INHERITED = another seat's read.

## 1. The act

Replace the code of the Lambda function `irpt-status` (LIVE at `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=`, revision 6, MEASURED
17:51Z) with the build of the PROPOSED entry
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r10/IRPT_STATUS_ENTRY_ONE_PIN.json` (blob `4bdaaf57c7`):
all 49 members pinned at ONE commit, `487f73663eaabf38f7043225909c478f131a3ca2`, which carries `AR-y-71` (`31d02ad19c`).
Build digest `EXu+Izn1LlqNKWI1w4l4yPhi7WA6SPURXa9SbS19tWc=`, 383562 bytes, twice equal, NO parity skip (RECORD: the census
`.../0.9.0_WK_IRPT_ANLREQ~52/r10/RETURN_CENSUS_IRPT_STATUS.json`, blob `83fe9f0ab6`; this seat ran its check, `Y103-CENSUS-OK`, and
its proof, VALID, on the shared tree; this seat did NOT rebuild the digest itself: the applier's build is the second measurement
and a different digest STOPS the apply).

Writers of the function's code: 1 (the apply order's `safe-apply` on one targeted resource). The source map is the build's input:
the apply's first write is ONE commit putting the proposed entry into `infra/aws/lambda/ci/lambda-source-map.json`.

## 2. Precondition -- the hold (CTO msg 5511)

Portal `PROD` carries the transitional history reader: `git merge-base --is-ancestor cbd5cc66 origin/PROD` AND `... a3f99d6e
origin/PROD` both rc 0, read by the applier at step 0 with a positive control (an old PROD commit) beside them. MEASURED now: rc 1
(not on PROD, `37aa1247ee`); on DEV rc 0. `2.0.0_SA_COO~D2` is cutting the PROD candidate; it goes to the CTO. Until then this pair
is not applied. NOT a precondition (RECORD, the census's `not_required_on_prod_first`): the reason set in `render/Page.tsx`; PROD
admits any upper-case reason and no PROD caller sends `ticket_id`. This corrects revision 3 of the working packet, which said it was.

## 3. Blast radius -- 16 of 49 members differ from live; 5 change a served answer

RECORD, the census, one row per member; the portal readers were read at `origin/PROD` `37aa1247ee` and `origin/DEV` `9ca634c6`.

| member | what a caller is served differently | portal reader on PROD admits it | on DEV |
|---|---|---|---|
| `owned_requests.py` | the history page gains `unreadable_rows`; each row gains `client_id`, `client_claim` | **NO** today (`owned-requests.ts` `readOwnedHistory` line 80, exact key set; `readOwnedRequest` line 61) -- the precondition | yes |
| `owned_report.py` | the sections answer gains `retained_ref` | yes (`adapt.ts` `adaptAnalysisReportSlice` reads named keys) | yes |
| `entry.py` | the sections route accepts the query member `ticket_id` | yes | yes |
| `served.py` | the new public reason `REPORT_TICKET_MISMATCH` | yes (shown as an unnamed code; cosmetic) | yes |
| `prospect_dates.py` | a READY prospect analysis whose Opal report has a NOT_AVAILABLE section is served where today it is refused | yes (`prospect-dates.ts` `readProspectDates` lines 41-47) | yes |

Eleven members are INERT (ten MEASURED by the worker calling both packages' entry points; `acceptance.py` INFERRED, not executed).
NOT SEEN by anyone: readers of these routes outside the portal repository; the live function's own environment values.
The history breakage of this morning is the first row: with the precondition true, PROD's reader admits both shapes.

## 4. Order of the apply (the apply order will carry these as numbered steps)

0. Pre-checks, STOP on any miss: section 2's precondition; live digest still `6idtFvAm...`; no other open ledger on the function;
   `git diff --stat 487f73663e..HEAD -- <the 49 members' repo paths>` printed -- any member changed on the trunk since the pin does
   NOT ship and is named in the record (a change that must ship means a new census, not an edit of this pair).
1. Ledger opened (NEVER-2), naming the function and the rollback version.
2. The map: commit the proposed entry. Build `BUILD_ONLY=1`, no skip: digest must be `EXu+Izn1...` or STOP and revert the commit.
3. Upload, targeted plan (ONE resource to change), `safe-apply`. Read back `CodeSha256`.
4. After-reads, section 5. Any FAIL: branch B.
5. Record the release in the map entry (`artifact_sha256`, deployed commit and time); close the ledger.
6. THEN, and only on branch A: the portal cell that REMOVES the transitional fallback (section 6).

**Branch B (rollback), same window:** the function back to the S3 object version of revision 6
(`sNe8hzDee69r.z596UgjXChHWPMxoGxl`, digest `6idtFvAm...`; INHERITED from this morning's rollback record -- the applier re-reads the
version's digest before step 3 and names it in the ledger), by targeted `safe-apply`; the map commit reverted; read back the digest;
one history read and one sections read as before. Nothing is deleted on either branch; no S3 version is removed.

## 5. After-reads (both outcomes named; a read that cannot be made is ABSENT, never a pass)

- B1 history, an owner with accepted requests: the page carries `unreadable_rows`, rows carry `client_id` and `client_claim`;
  the Investor Reporting history view on PROD renders its rows (looked at, by a seat that can sign in). FAIL: the view shows the
  reader's refusal -> branch B.
- B2 sections with the request's OWN stored ticket id: the report. With another ticket's id: `REPORT_TICKET_MISMATCH`. MEASURED
  baseline (laptop, TO-READS-Y6): 6 of 51 accepted requests store a ticket id, all in one tenant, and that tenant's owners were not
  replayable from the laptop this morning: B2 may read ABSENT.
- B3 sections with NO ticket id, and a request that stores none (45 of 51): answers as today, plus `retained_ref`.
- B4 the count of section 5's baseline is unchanged by the release (the release writes no record).
- C1 a request read and C2 a status read for an existing request: the key sets of today. C3 an unknown query member other than
  `ticket_id` on the sections route: still `INVALID_INPUT`.
- C5 prospect dates for a prospect analysis with a NOT_AVAILABLE section, if one exists: served; otherwise ABSENT.

## 6. The transitional fallback is removed by this release (CTO msg 5487)

On portal DEV since `3ebc35ebf2`: the Ticket Center's report read sends `ticket_id` and, on `INVALID_INPUT`, reads once more
without it. Once the binding is live that second read is a way around it. So, after step 5 on branch A: ONE portal cell removes
`readTicketReport`'s second read, its predicate and its four tests; DEV, then PROD (Ticket Center is Opal-internal: no word needed).
After-read C4: a ticket id the service refuses as `INVALID_INPUT` shows the refusal after ONE read. Until that cell is on PROD the
release's record says in words: the binding is live and bypassable through the fallback on an `INVALID_INPUT` refusal.

## 7. What this half does not claim

- That the digest is reproducible by a second seat (the applier's build is that read).
- That any served row's portal reading is right: criterion `AR103-y-AC2` is a judgment the reviewer grades at L9.
- Any behaviour of a caller outside the portal repository.

-- 2.0.0_SA_COO~Y2
