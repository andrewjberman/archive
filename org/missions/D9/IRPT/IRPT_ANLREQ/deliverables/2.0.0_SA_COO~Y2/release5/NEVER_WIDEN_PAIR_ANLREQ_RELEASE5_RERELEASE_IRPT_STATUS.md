# IRPT_ANLREQ release 5, RE-RELEASE -- irpt-status build `Iw3FADFr` again, behind the portal reader -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No apply order exists and none is cut on this file until its ordering condition is a measured read.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-11. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Asked for by the CTO's round-5 analysis (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_ROUND_5_Y_20261011.md`
@ca8aa78b88, section 4 item 2): the same build, two consumer after-reads, the ordering condition as a measured read.

This half signs the act's blast radius and both branches. It SUPERSEDES the first pair's sections 2 to 5 where they differ
(`NEVER_WIDEN_PAIR_ANLREQ_RELEASE5_IRPT_STATUS.md`, blob 1b310f3c2a); that pair's member census stands and is cited, not repeated.

Claim words: MEASURED = this seat ran or read it; RECORD = an applier's committed record this seat opened; RELAYED = the laptop
reader's read carried by the integrator; INFERRED = said so.

## 1. What happened the first time, in four lines

- Applied 2026-10-11T10:25:40Z; nine after-reads made, none false (R4 ABSENT); rolled back 11:26:53Z; live is revision 6 (`6idtFvAm...`).
- Cause: the portal's history reader admitted exact key sets and refused the new answer (page member `unreadable_rows`; row members
  `client_id`, `client_claim`). Rows `IRPT_ANLREQ-D2-S43`, `-S44`.
- The first pair's blast radius named the function and 19 backend readers and NO portal reader; its after-reads read the service's
  fields and never the page. That is the defect this pair repairs.
- Who met the refused view in those 61 minutes is NOT MEASURED (CTO analysis section 2: not countable from the function's log).

## 2. Ordering condition (a measured read, made by the applier at step 0 and again immediately before the apply)

`git ls-remote` of the portal's `PROD` names a commit that CONTAINS `8ed372cb72659b96a5cfb4000a20b8ae315b9be7` (the history reader
that admits both answers; DSGN_IRPTV1 cell IV-e-99): `git merge-base --is-ancestor 8ed372cb72 <PROD commit>` rc 0, with a negative
control (an unrelated commit reads rc 1). At this signing PROD reads `37aa1247ee` and does NOT contain it (MEASURED 11:52Z): the
condition is UNMET. The PROD push is a client-facing page and is Andrew's word; this pair does not ask for it and cannot stand in for it.
A second condition, read the same way: the deployed PROD bundle is the one built from that commit (the portal's own deploy record;
a pushed branch is not a served page).

## 3. Artifact, pin, rollback

- **Artifact:** `Iw3FADFrSt5G97zRTSkvZ7txSlXnaNQNpgPZi+G5tw0=`, the SAME bytes that ran for 61 minutes. Its S3 object version
  `YEgNj7Q3dDWk.kcPgyz4njl7WN00sM1w` is still present (RECORD: `R5_rollback_record.json` @0581ad2a46). The applier PROMOTES that
  version (copy onto the key, as the rollback did); it does NOT rebuild. Step 0 re-reads that the version exists and its digest.
- **Live / ROLLBACK:** revision 6, `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=` (MEASURED 11:52Z); rollback object version
  `hRe7.zty9CYey5GkmjHlETbeZkKsD.3O`, present (RECORD). Rollback is the same copy-and-targeted-apply; it took 6 minutes from order to
  digest the first time (11:20Z to 11:26Z).
- **Source map, in the SAME act and not before (analysis item 3):** the two member pins of row `IRPT_ANLREQ-D2-S45` are removed and
  the entry is re-pinned to one tree, as commit `01d1f660ad` had it (42 rows at `ee3fd7c5e5`), and a BUILD_ONLY from it must print
  `Iw3FADFr...` before the promote. If it prints anything else, ABORT: the map and the object disagree. On rollback the pins return
  (the entry as it is at 1f37df97ed).
- **Writers of the function's code: N = 1** (`module "irpt_status"`, `infra/aws/terraform/investor-reporting/ops/lambda.tf:18`; the
  search for others is INHERITED from the revision 6 pair).

## 4. Blast radius, corrected

- The function: 14 of 49 members against revision 6; three change a served answer; eleven censused INERT (census blob 89725a4ba9;
  two of the eleven by reading only). Reach read count 0. Unchanged from the first pair and proven once in the world for 61 minutes.
- **The consumers of the three changed answers, which the first pair did not name:**
  | changed answer | portal reader | state |
  |---|---|---|
  | history page and rows | `readOwnedHistory`, `readOwnedRequest` in `src/pages/InvestorReporting/contracts/owned-requests.ts` | REFUSES on PROD `37aa1247ee` (MEASURED by reading); admits both on DEV `8ed372cb72` (the integrator's receipt and the CTO's review; not re-read line by line by this seat) |
  | report sections (`retained_ref`) | the sections reader of the Investor Reporting report view and of the Ticket Center's opened Report | NOT READ by this seat. Owed before signing: the reader's key policy at the PROD commit, by the same method |
  | section dates, OPAL_ENGINE branch | the same report view | NOT READ; and the branch itself has never been exercised (R4 ABSENT) |
- A census of EVERY portal reader of an irpt-status route at the PROD commit, with its key policy (exact, or tolerant), is owed before
  the CTO half is asked for: `2.0.0_SA_COO~D2`'s probe (msg 4804) found five readers refusing wrapped fixtures, of which only the
  history reader was traced to this release. Until that census is in, this half is NOT signed for apply: it is the written packet.

## 4a. The reader census is IN (added 2026-10-11 ~12:4xZ; this changes the file's blob, and no half was signed on the earlier one)

`org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~56/READER_CENSUS.json` (blob 7c84796ba3; `2.0.0_SA_COO~D2` msg 4910,
drained @7914dec2a5). INHERITED from that record and its issuer's message; this seat opened the file for its denominator and its
`joins_prod_push` member and did not re-run a probe.
- Denominator: irpt-status serves 7 routes; the portal reads 5 of them at PROD `37aa1247ee` and 7 at DEV.
- At PROD against release 5's answers: `analysis-request-history` REFUSES (the page, and the rows independently) and PASSES at DEV.
  The other four PASS: single-request (EXACT, and unchanged by release 5), sections (TOLERANT: `retained_ref` is ignored),
  status-summary, status-job. The pdf and original routes have no PROD caller.
- So the PROD push of `8ed372cb72` covers every reader that would refuse. Section 2's condition is unchanged and still UNMET.
- LIMIT stated by the census itself: the bodies were produced by the producer's offline code at the release pin; NO LIVE BODY was
  read. After-read C1 (the PROD readers run on the live bodies) is therefore still the first measured proof, and stays first.
- Two findings of the census that bear on what this release is FOR: the sections view drops `retained_ref` (nothing on a page shows
  it yet), and the sections reader already reads the OPAL_ENGINE validation member at both commits.

## 5. After-reads (in order; each recorded with its claim)

R0 to R8 as in the first pair, with these changes:
- **R8** is renamed what it is: a refusal-envelope comparison on dell2. It is kept and is not a control of the readers behind authorization.
- **C1 (consumer, new):** the PROD page's reader given the LIVE answer -- the history body fetched as an owner after the apply is passed
  through `readOwnedHistory` from the portal's PROD commit (the function itself, run in a script; keys and counts recorded, no value):
  it returns, it does not throw. The same for one single-request read through `readOwnedRequest`, and for the report sections body
  through its reader. BEFORE arm: the same three run on revision 6's answers.
- **C2 (consumer, new):** ONE rendered read of the history view on PROD by a human or a manager session that can sign in: the list shows
  its rows. A screenshot or a stated count of rows, by whoever looked, with the time. This is the only read of the page itself.
- **R4** stays ABSENT unless an OPAL_ENGINE request is readable; the record says ABSENT is not EXERCISED.

## 6. Both branches

- **All reads as expected, C1 and C2 included:** record, close the ledger, the map states the release and one tree.
- **C1 throws on any of the three, C2 shows an empty or errored view, R1 wrong, a plan line beyond the one resource, or any of R2 to R7
  false:** ROLL BACK at once to `hRe7...` (`6idtFvAm`), restore the map's pins, re-read the digest and one two-key history read, close
  the ledger ROLLED_BACK, file a row. C1 is made FIRST after R1, before any other read, because it is the read that failed the page.
- The reader on PROD admits both answers, so a rollback after it is on PROD does not itself break the page (INFERRED from the reader's
  design; C1's BEFORE arm measures it).

## 7. Owed before any apply order is cut

1. Section 2's condition read as MET (Andrew's word comes first; not this seat's to ask for by this document).
2. Section 4's census of portal readers at the PROD commit: IN, section 4a.
3. The CTO half on this file's blob, after 1 and 2.
4. The FWD-1 trace (order TO-AR-y-51), so the release is cut knowing which hop it serves.

## 8. REVISION 2 (2026-10-11 ~14:3xZ): round 7 changed what this release is; sections 3 and 5 are superseded where they differ

Still WRITTEN, NOT APPLIED; no half is signed on any blob of this file. CTO ruling msg 5108: the ticket binding (cell `AR-y-71`) goes
live IN release 5's return, under this pair, "whose census lists the binding's three files among its moved members"; no composed build.

- **The artifact is no longer the stored object.** Section 3 said to promote the stored `Iw3FADFr` version without rebuilding. That
  build predates round 7. The return is a FRESH one-tree build at the trunk commit of the day, with the map's two member pins (row
  D2-S45) removed in the same act. Its digest is NOT KNOWN until it is built; this pair is re-issued with the digest, built twice
  identical, before any half is asked for. `Iw3FADFr`'s stored version stays as a record and is not the release.
- **Moved members against revision 6, expected:** the 14 of the first census, plus the binding's files -- `owned_report.py` (already
  among the 14; it now also carries the binding), `entry.py` and `_authz/served.py` (both NEW to the moved set). The census
  (`REPIN_CENSUS_IRPT_STATUS.json`, blob 89725a4ba9) is RE-RUN at that build: any member that moved on the trunk since `ee3fd7c5e5`
  joins it with its owning commit, its served effect and, where it changes an answer, an after-read. Not re-run yet.
- **`_authz/served.py` gains one value** (`REPORT_TICKET_MISMATCH` in `BOUNDARY_ADDITIONS`, commit `7133cbccc5`): INERT for every
  route but `analysis-report` with a `ticket_id` (the reader census `deliverables/0.9.0_WK_IRPT_ANLREQ~52/r7/PUBLIC_REASON_READERS.json`,
  80 rows: no portal runtime reader refuses the value at PROD or DEV; WORKER's read).
- **`entry.py` now ADMITS one query member on one route.** Live revision 6 refuses any query member but `selected_tenant`
  (`ops/entry.py:164-165` at `361c44fa9d`, read by this seat). So the portal candidate that SENDS `ticket_id`
  (`wk-IRPT_ANLREQ-51-portal-r7` @5f64f409b0, reviewed sound by the CTO, msg 5104) lands on DEV only AFTER this release is live, on a
  measured digest read. That landing is a step of this release's close, named here so it is not forgotten.
- **After-reads added to section 5:**
  - **B1:** `analysis-report` for a READY owned request with NO `ticket_id` sent: the body equals the BEFORE arm but for `retained_ref`.
  - **B2:** the same with the request's OWN stored `ticket_id`: answers. With ANOTHER well-formed ticket id: `REPORT_TICKET_MISMATCH`.
    Needs one ticket-filed request that is readable; if none exists the result is ABSENT with its census, and ABSENT is not EXERCISED.
  - **B3:** a caller not admitted to the request, sending a wrong ticket id: the same answer as with none.
  - **B4 (the count CTO msg 4955 asked for):** how many accepted requests store NO `ticket_id`, of how many; a laptop read.
  - **C3:** after the portal candidate lands, one Open report from a ticket on DEV: the report renders.
- **Rollback is unchanged:** revision 6, `6idtFvAm`, by copying its stored object version onto the key; the map's two pins return.
  If the rollback happens AFTER the portal candidate landed, that candidate is reverted on DEV first, or every Open is refused.
- **Order of the whole return:** (1) the history reader on portal PROD (Andrew's word); (2) the build, the re-run census, this pair
  re-issued, the CTO half; (3) the apply and R0 to R8, B1 to B4, C1, C2; (4) the portal candidate on DEV and C3.
