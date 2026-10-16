<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RUN-AR-v32.ticket-page-reads-a-real-hop-failure-aq2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-16</date>
    <status>staged</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>4</round>
<workstream>TICKET</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R4_V.md</decomp_doc>
<owned_cells>AR-v-32</owned_cells>
<decomp_context>Round 4, workstream TICKET, cell AR-v-32: after IRPT_ANLREQ.TO-APPLY-t55 (2.0.0_SA_COO~T2) has written ONE real hop failure on ONE synthetic job row, read the Ticket Center page for that request's ticket on the DEV build under a staff login, record what it shows, and remove the staff user you minted. The failure itself is t55's leg A; its removal is t55's leg B, sent after this order's report.</decomp_context>
</decomp_ref>

  <objective>
    STAGED. This order carries no GO until the issuer adds a CONDITIONAL GO amendment (the signed pair AR_V32_PAIR.md, both halves, at the blobs the amendment names). On the GO: with the hop failure COMMENTARY_DRAFT_REFUSED standing on the job row of request REQ-d47252fe74634d0c5cdd8067 (tenant 49financial), open the ticket TCK-20261015-944c84f8 in the Ticket Center on the DEV dev server (http://localhost:5174) as a minted synthetic staff user, read what the page shows under the ticket, take one full-page screenshot, then remove the user and read it ABSENT. Write one record file. The issuer looks at the screenshot itself. You change nothing else.
  </objective>

  <context>
    Authority: the CTO's round-3 analysis `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_TICKET_ROUND_3_20261016.md` @90926d9683 and decision msg 9529 (arm A now; the DEV build served on localhost:5174; no hosted DEV exists). The landed page read is on portal DEV at dc057891b086 or later (no later change under `src/pages/TicketCenter`); it calls `getJobStatus` once when an analysis-request ticket is shown and once on Refresh, and shows the failure's words only while no package is attached (the ticket has none).
    THE FAILURE: written by IRPT_ANLREQ.TO-APPLY-t55.drive-commentary-refusal-aq2 (your own queue, leg A). THIS ORDER STARTS ONLY AFTER you have reported leg A (the row reads hop_failure COMMENTARY_DRAFT_REFUSED). It must NOT remove that failure: leg B is the issuer 2.0.0_SA_COO~T2's message, sent after this order's report. If the row does not carry the failure, STOP and report.
    THE USER: the helper `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_mint.py` (git blob f368e9d95c62dc9fce1e6d5e04cd7fe6f79c444a, sha256 04e4ba64ddb74895442a7b291e14862fc9b395b65cc814c75bb737b8445ec5d4; a different value is a STOP) mints ONE users row `fwd1-staff-r41b@opal.invalid` (firm opal-capital, active, exp 3 hours) from a password read on STDIN, and removes it. Use it as it is; the password is a fresh 32-byte url-safe random value held in memory only, never printed, logged, written to a file, or placed in argv or the environment. You type it into the real login page of the dev server.
    THE PAGE: the Ticket Center under an Opal staff login is the internal board; opening the ticket shows the Analysis Request parts. The block that reads the failure sits under the ticket row; with the failure standing and no package attached it shows the words of the COMMENTARY step ("The analysis was generated, but the commentary draft step was refused. Opal Staff have been left a record and will follow up; you do not need to submit the request again.", from `ops/status.py` FAILURE_WORDS). Do not edit anything to make it show.
  </context>

  <the_act>
    GO is the issuer's conditional amendment; without it STOP at step 0.
    0. NEVER-2: read the ledger (every live worktree, `ls-tree`) and open ONE change ledger entry naming this order, the one users row and the dev server; it closes at step 9. STOP if the issuer's amendment is absent, if any blob named there differs, or if the t55 ledger is not OPEN with leg A reported.
    1. READ BEFORE, no write: the job row (names and state: state READY, hop_failure code COMMENTARY_DRAFT_REFUSED with its `at`), the ticket `TCK-20261015-944c84f8` (analysis_request, in_progress, NO package pointer), and the users row for `fwd1-staff-r41b@opal.invalid` ABSENT (a consistent get; PRESENT is a STOP, it is another run's). Record lines B1, B2 and A1 (the format is in the checker's docstring).
    2. START the dev server of the portal DEV checkout (HEAD at or after dc057891b086) on port 5174 only (`bun run dev --port 5174`; resolve bun by the profile, bake no path). Record the browser origin you open: it must read exactly http://localhost:5174. Any other origin is a STOP.
    3. MINT the staff user with the helper's `mint` and the password on stdin. The helper prints MINT-OK READBACK-OK; any other word is a STOP (remove nothing you did not mint).
    4. SIGN IN through the real login page on http://localhost:5174 as that user, open the Ticket Center, and open TCK-20261015-944c84f8. Wait for the page to settle (the ticket detail and the one status read). Record the page's network call for the status route (its http status and the public_reason_code and action it answered; line S1). Never record a token, cookie or the password.
    5. READ THE PAGE: whether the failure's words show under the ticket (words_shown), whether the first sentence names the step (step_named), whether the page is intact (no error boundary, the board and ticket still render), whether a blank row shows (blank_row). Resolve the canvas colour live (`getComputedStyle(document.body).backgroundColor` or the page's resolved canvas) and record it. Take ONE full-page screenshot to `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_arv32/ar_v32_page.png`. Lines P1 and P2.
    6. Press Refresh once on the ticket (the page's second permitted status read) and record whether the words still show and the page is intact (line P3: words_shown and page_intact only).
    7. STOP the dev server. REMOVE the minted user with the helper's `remove`; it must print ABSENT lines for the consistent read and the email index. Line R1 (`users_row=ABSENT consistent=YES`), line R2 (`browser origin=http://localhost:5174`).
    8. Write `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_arv32/A_RUN_AR_V32.txt` with ONE line each for B1, B2, A1, S1, P1, P2, P3, R1, R2 and nothing else on a line that starts with those tokens. No password, hash, token, cookie or address beyond the synthetic one.
    9. Run the three checks (below); close the ledger; commit with `.tools/safe-commit.sh` on your own lane; report ONCE to 2.0.0_SA_COO~V2 AND 2.0.0_SA_COO~T2 (statuses only): the three check lines, the screenshot path, the commit hash and its measured push state, the ledger id (CLOSED). T2 then sends your leg B.
  </the_act>

  <bounds>
    - One staff user row, minted and removed by this order; one dev server, port 5174 only; one sign-in; at most two status reads by the page (open, Refresh). No other principal, route, table, row, queue, key or function. No write to the job row, the ticket or any object; no Terraform; no `aws lambda update-function-code`.
    - The failure on the job row is t55's: do not set it, do not remove it, do not invoke the commentary function.
    - A STOP leaves the user row removed if you minted it (run `remove`), the dev server stopped, and the ledger entry closed with the reason; report it.
    - No transcript text, mail content, prompt text, draft text, bearer or address in any file or message.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-blast: RUN-AS-THE-ACT -- the blast radius is the pair's: ONE users-table row (the synthetic staff user, TTL 3 hours, removed in the same order and read ABSENT on a consistent get and on the email index), one dev server on port 5174 started and stopped, at most two reads of the existing status route. Rollback per key: the helper's `remove` (attribute_exists), and the TTL.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; the page calls the existing status route as released.
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule, trigger or mapping. comp-cache: DECLARED-NOT-APPLICABLE.
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the user row is written and deleted with the operator's own credentials as in windows 2 and 3.
comp-adversary: RUN -- by reading window 2's and window 3's records and the helper against this cell; the lens: a password written anywhere; a minted row left behind (the helper's remove, a STOP path that still removes); a page read of another origin (the origin is recorded and checked); removing or setting the job row's failure (not this order's; t55's); a screenshot that carries a client figure (the request is synthetic); a Refresh that reads the status route a third time; a dev server left running.
lane: the applier's deliverables, logs, the change ledger and its sentinel.
</preflight>

<proof_of_spec>
  <criterion id="AR32-v-AC1" cell_refs="AR-v-32"><invocation>python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v32_checks.py status</invocation><expect>V32-STATUS-OK</expect></criterion>
  <criterion id="AR32-v-AC2" cell_refs="AR-v-32"><invocation>python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v32_checks.py page</invocation><expect>V32-PAGE-OK</expect></criterion>
  <criterion id="AR32-v-AC3" cell_refs="AR-v-32"><invocation>python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/AR_V_CHECKS/ar_v32_checks.py restore</invocation><expect>V32-RESTORE-OK</expect></criterion>
  <criterion id="AR32-v-AC4J" cell_refs="AR-v-32" judgment="true"/>
</proof_of_spec>
  Each check reads FAIL at the base (`V32-...-FAIL no-record`) and OK on a record holding the lines of step 8; the checker's `--self-test` reads `V32-SELFTEST-OK` (a good record, eight one-line mutants and one record with a password line). AR32-v-AC4J is the CVO's: the page, looked at in the screenshot, names the failed step and what happens next, the page stays intact, nothing blank shows, for a ticket with no package (arm A); arm B (a packaged ticket shows none) is OWED and read on FWD-1 run 3's first packaged ticket.

<expected_criteria>AR32-v-AC1,AR32-v-AC2,AR32-v-AC3,AR32-v-AC4J</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~V2 and 2.0.0_SA_COO~T2 after step 9 (statuses only): "page read done" with the three check lines, the screenshot path, the status route's answer (http, code, action), the user row's removal read, the commit and its push state, the ledger id (CLOSED). Write the proof instance beside this order in `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/` (not in a subfolder: the flip gate looks there); leave the status flip to the issuer.
  </report>
</task_order>
