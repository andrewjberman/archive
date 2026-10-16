<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-AR-v34.ticket-page-reads-window4-real-link-and-packaged-failed-ib2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-16</date>
    <status>staged</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>5</round>
<workstream>TICKET</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R5_V.md</decomp_doc>
<owned_cells>AR-v-34</owned_cells>
<decomp_context>Round 5, workstream TICKET, cell AR-v-34: on FWD-1 window 4's request (a REAL filing whose step 4 recorded a REAL report_ref), read the Ticket Center page with a failure standing before the package lands (phase 1, the real link) and again after the package lands with a failure standing (phase 2, packaged AND failed). Round 4's sittings (TO-RUN-AR-v32 and TO-RUN-AR-v33) proved arm A on a hand-written link and arm B partial.</decomp_context>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer adds a CONDITIONAL GO amendment on the signed pair `AR_V34_PAIR.md` (both halves) that NAMES window 4's ticket id and request id. On the GO, in TWO phases, on that one request: PHASE 1 (the ticket has the filing's real `report_ref` and NO package; a failure standing on the job row, driven by `2.0.0_SA_COO~T2`'s order or natural): mint ONE staff-only synthetic user, read the page on the DEV dev server (http://localhost:5174), screenshot, remove the user. PHASE 2 (the package attached; a failure driven again by `~T2` after its leg B of phase 1): the same with a second mint. Write one record file. The issuer looks at the screenshots itself. You write nothing else.
  </objective>

  <context>
    Authority: the CTO's round-4 analysis `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_TICKET_ROUND_4_20261016.md` @d891371278 (msg 9722; both owed halves, ONE sitting, ONE pair, applier IB2); the staff-only user condition of XA-20261016T160537Z-f98b; the CTO's msg 9670 (after the combined release a synthetic staff user carries `allowedFirmIds` = [the one firm], never `scope_all_firms`). Model: `IRPT_ANLREQ.TO-RUN-AR-v33...` (your own sitting 2: its script `ar_v33_run.mjs` and `ar_v33b_run.mjs` are the model for the sign-in, the sidebar and the Open or In Progress tab click, the screenshot and the status-read count). THE LESSON OF SITTING 2: click the tab that lists the ticket and CONFIRM the ticket is listed before reading.
    THE REQUEST: FWD-1 window 4's own filing (a staff filing through the Ticket Center under `~AQ2`'s run, `~Y2`'s order). Its ticket and request ids are named in the GO amendment. Its job row is the run's evidence: set and remove a failure only in the gap `~T2` and the issuers agree, and only when the row reads state READY (a row still moving is a STOP for that phase).
    THE FAILURES are `~T2`'s (`IRPT_ANLREQ.TO-APPLY-t57...`, your queue, legs A and B per phase). You must NOT set, remove or invoke anything on a job row. Phase 2's failure is set only after phase 1's is removed (the value is set-once).
    THE USER: the helper `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py` at the blob the GO names (the combined release may have landed: then the helper carries the allowedFirmIds amendment, and an old blob is a STOP). The password is a fresh random value in memory only; never printed, logged, written, in argv or the environment; your report says so in words.
  </context>

  <the_act>
    GO is the issuer's conditional amendment; without it STOP at step 0. THE TWO PHASES ARE INDEPENDENT: a phase whose precondition is false is UNREACHED (recorded, no user minted for it), never forced; the other phase may still run.
    0. NEVER-2: read the ledger (every live worktree, `ls-tree`) and open ONE change-ledger entry naming this order, the two users rows (one at a time) and the dev server; it closes at the last step. Measure the blobs the amendment names; verify `python .tools/xadj.py show --id XA-20261016T160537Z-f98b` prints `State: RULED`. Record line L0: `L0 window4 ticket=<TCK-...> request_id=<REQ-...>` (the ids the GO names; every later line carries the same two).
    PHASE 1 (before the package)
    1. READ, no write: the ticket (`report_ref` PRESENT, `recorded_by` NOT beginning `fixture:` and equal to the filing user's address, the request id equal to L0's; NO package; line L1 `L1 ticket=<..> request_id=<..> report_ref=PRESENT recorded_by=<address>` and line B2 `B2 ticket=<..> status=<s> package=ABSENT`); the job row of the request (state READY; line B1 `B1 job_row request_id=<..> state=READY hop_failure=ABSENT|PRESENT`, a natural failure already standing is allowed and recorded in A1). If any is false: phase 1 is UNREACHED (record a NOTE line `NOTE phase1 UNREACHED <the false item>`), skip to PHASE 2.
    2. FAILURE: if the row carries no failure, tell the issuer (a message) and wait for `~T2`'s leg A report; a natural failure needs no leg A. Read the row: line A1 `A1 job_row request_id=<..> hop_failure=PRESENT code=<CODE> at=<UTC>`.
    3. The dev server of the portal DEV checkout (HEAD contains dc057891b086) on port 5174 only: reuse one already listening there (leave it running) else start `bun run dev --port 5174` (stop it at the end of the phase). Origin must read exactly http://localhost:5174.
    4. MINT (the helper's `mint`: `MINT-OK READBACK-OK`); print U1 before the removal: `U1 users_row role=<role> userType=<userType> firmId=<firmId> allowedFirmIds=<the list or NONE> scope_all_firms=<present or ABSENT> entitlement_rows=<count of other rows under that PK> status=<status>`; role user, userType test-filer, firmId opal-capital, 0 entitlement rows, scope_all_firms ABSENT required; a combined-release world also requires allowedFirmIds = [the one firm]. Anything else is a STOP (remove the user, report, grade nothing).
    5. Sign in by the real form; open the Ticket Center by the SIDEBAR link; click the tab that lists the ticket (In Progress or Open) and CONFIRM the ticket is listed; read the page: the words shown under the ticket (words_shown), the first sentence names the step (step_named), the page intact (page_intact), no blank row (blank_row). Record the status-route reads (each: http, public_reason_code, action) for the request: line S1 `S1 status_route request_id=<..> http=<n> public_reason_code=<CODE> action=<NONE|...>`. Screenshot `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_arv34/ar_v34_p1_page.png`. Lines P1 (`P1 page ticket=<..> words_shown=YES|NO step_named=YES|NO page_intact=YES|NO blank_row=NO|YES`), P2 (`P2 canvas=<resolved canvas colour> screenshot=<path>`), R3 (`R3 browser origin=http://localhost:5174`). THEN re-read the ticket: record in a NOTE line whether a package landed during the read (a landed package voids the phase-1 grade: record `NOTE phase1 package landed during the read` and the page is not graded as the pre-package read).
    6. Remove the user (helper `remove`: ABSENT consistent and index). Line R1. Report phase 1 to the issuer AND `~T2` (statuses only) so that `~T2` sends leg B for phase 1.
    PHASE 2 (after the package)
    7. READ, no write: the ticket carries the package (line B3 `B3 ticket=<..> status=<s> package=PRESENT`), the job row READY with NO failure standing (phase 1's removed and read ABSENT: `~T2`'s leg B). If the package is not attached yet, WAIT (read again every few minutes for up to the ledger's window); if it never lands, phase 2 is UNREACHED. If a failure still stands from phase 1, STOP for this phase.
    8. FAILURE: wait for `~T2`'s phase-2 leg A report (a driven failure on the packaged request). Line A2 `A2 job_row request_id=<..> hop_failure=PRESENT code=<CODE> at=<UTC>`.
    9. Dev server, MINT (U2 in a NOTE line, same required values), sign in, sidebar, click the listing tab and CONFIRM the ticket listed. Read the page: the package block shows and NO failure words show (`P3 page ticket=<..> words_shown=NO package_block=YES page_intact=YES screenshot=<path>`, screenshot `.../ar_v34_p2_page.png`) and COUNT the status-route reads the page makes for the request (`S3 status_reads request_id=<..> count=<n>`, 0 expected: a ticket with a package is never asked for).
    10. Remove the user (R2: `R2 users_row=ABSENT consistent=YES`). Report phase 2 to the issuer AND `~T2` so `~T2` sends leg B for phase 2.
    11. AFTER both legs B are reported by `~T2`: read the job row (failure ABSENT and the item hash equal to PRE): lines X1 (after phase 1's removal, `X1 job_row request_id=<..> hop_failure=ABSENT item_hash_equals_pre=YES`) and X2 (after phase 2's, the same shape). Write `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_arv34/A_RUN_AR_V34.txt` with ONE line each for L0, L1, B1, B2, A1, S1, P1, P2, R3, B3, A2, S3, P3, R1, R2, X1, X2 (and U1, NOTE lines) and nothing else on a line that starts with those tokens. No password, hash, token or cookie. Run the three checks; close the ledger; commit with `.tools/safe-commit.sh`; report ONCE to the issuer AND `~T2` (statuses only): the three check lines (a phase UNREACHED reads FAIL on its check and says so), the screenshot paths, the commit and its measured push state, the ledger id (CLOSED), "the password lived in memory only".
  </the_act>

  <bounds>
    - ONE users row at a time (a mint per phase, two at most); no job-row write; no ticket write; one dev server, port 5174 only; no other principal, route, table, row, queue, key or function; no Terraform; no `aws lambda update-function-code`; no Retry press and no other button on the ticket.
    - The failures are `~T2`'s. A STOP leaves any minted user removed, the dev server stopped if started, and the ledger closed with the reason; report it.
    - If phase 1 reads NO words with the real link and the failure both standing, or phase 2 shows failure words beside a package, that is a RESULT: record it as read, adjust nothing. Branch 2 (a precondition false) grades nothing.
    - The request is FWD-1 window 4's run evidence: touch nothing of its chain.
    - No transcript text, mail content, prompt text, draft text, bearer or address in any file or message.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-blast: RUN-AS-THE-ACT -- the pair's blast radius: ONE users-table row at a time (the synthetic staff user, TTL 3 hours, removed in the same phase), one dev server on 5174, the page's own reads of the status route; NO write to a job row or a ticket by this order (the failures are the other order's). Rollback per key: the helper's `remove`; stop the process.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; the page calls the existing status route as released.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule, trigger or mapping. comp-cache: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the user rows are written and removed with the operator's own credentials as in windows 2 and 3 and round 4's sittings.
comp-adversary: RUN -- by reading round 4's records and scripts, the helper and the service route against this cell; the lens: the package landing between the precondition read and the page read (re-read after), a fixture mistaken for the real link (`recorded_by`), a failure left on the run's row (T2's leg B each phase), a second user present at once, a password written anywhere, a screenshot that carries a client figure (the request is synthetic), the Open or In Progress tab not clicked (confirm listed), a combined-release world where the old helper blob gets 403, window 4's chain disturbed.
lane: the applier's deliverables, logs, the change ledger and its sentinel.
</preflight>

<proof_of_spec>
  <criterion id="AR34-v-AC1" cell_refs="AR-v-34"><invocation>python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v34_checks.py phase1</invocation><expect>V34-PHASE1-OK</expect></criterion>
  <criterion id="AR34-v-AC2" cell_refs="AR-v-34"><invocation>python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v34_checks.py phase2</invocation><expect>V34-PHASE2-OK</expect></criterion>
  <criterion id="AR34-v-AC3" cell_refs="AR-v-34"><invocation>python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v34_checks.py restore</invocation><expect>V34-RESTORE-OK</expect></criterion>
  <criterion id="AR34-v-AC4J" cell_refs="AR-v-34" judgment="true"/>
</proof_of_spec>
  Each check reads FAIL at the base (`V34-...-FAIL no-record`) and OK on a record holding the lines of step 11; the checker's `--self-test` reads `V34-SELFTEST-OK` (a good record, nine one-line mutants and one record with a password line). The ids are read from the record's own line L0, so the check names none. AR34-v-AC4J is the CVO's: phase 1, the page, looked at in the screenshot, names the failed step on the REAL link and stays intact; phase 2, the packaged request shows its package and no failure words although its row carries a failure.

<expected_criteria>AR34-v-AC1,AR34-v-AC2,AR34-v-AC3,AR34-v-AC4J</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~V2 and 2.0.0_SA_COO~T2 after step 11 (statuses only), and to the issuer alone after each phase (steps 6 and 10). Write the proof instance beside this order in `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/` (not in a subfolder: the flip gate looks there); leave the status flip to the issuer.
  </report>
</task_order>
