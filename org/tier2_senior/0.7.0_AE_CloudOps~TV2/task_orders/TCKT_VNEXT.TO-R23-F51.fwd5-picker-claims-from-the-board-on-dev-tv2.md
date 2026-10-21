<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R23-F51.fwd5-picker-claims-from-the-board-on-dev-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-21</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>23</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R23.md</decomp_doc> (round 23): FWD-5 exercised once on DEV, cell `R23-f5-1` (the CVO's `ADJUDICATION_v21`, relayed by the CTO's msg 11772).
<owned_cells>R23-f5-1</owned_cells>
</decomp_ref>

  <objective>
    GO under the start gate below. Prove FWD-5 on DEV, ONCE: two open tickets of DIFFERENT types stand on the board together; a second synthetic internal identity (the picker) reads the board unclipped, with both rows' type and age visible; chooses one by what it reads; and claims it from the board without opening either ticket; the full-board shots are saved, the choice and what was read are recorded, the two tickets are saved whole, and then the tickets and the identity rows are deleted by key after the tokens' `exp` and read ABSENT. The PRD's FWD-5 ACCEPT: "an Opal person reads each request's type and how long it has waited from the queue itself, and opens only the ones that are theirs".
  </objective>

  <context>
    Why: the CVO (`org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/adjudications/ADJUDICATION_v21.md`) read type and age on the row from the R20 shots and found no run that picks from a queue: every R18 to R21 shot is clipped to one ticket's rows and every run finds its ticket by id. The CTO (msg 11772) told the issuer to cut this one arm exactly as the adjudication specifies. DEV means what it meant in `TO-R18-RUN` and `TO-R20-RV`: the portal DEV branch served by `bun run dev --port 5174` on this box, the ONE browser origin `http://localhost:5174`, against the live ticket service and tables, so the board also lists whatever else is open. Model: your `TO-R21-RB1` (mint the synthetic row and token, removal after `exp`) and `TO-R18-RUN`. The picker is a second identity on purpose: the claim must be the queue's act, not the self-claim FWD-4 already proves. The synthetic-delete is under Andrew's standing synthetic-delete word, as in `TO-R21-RB1`.
  </context>

  <go>
    THE START GATE (all printed; a failed item is a STOP before any write):
    1. `check-inbox`. Open the NEVER-2 ledger `tckt-vnext-r23-f51-20261021` FIRST and send its SLUG to `2.0.0_SA_COO~V2`. Census of live open entries naming `opal-ticket-api`, `opal-tickets` or `opal-users-v2` across every live worktree (`git worktree list --porcelain`, then `ls-tree` of `org/critical_paths/.open_deploys/` per tree; print the denominator): 0 open, or STOP.
    2. The portal DEV checkout at the box: print its `git rev-parse HEAD`; on `http://localhost:5174` the New Ticket type list carries Service Request and Other (read, no write); the board lists tickets (read, no write). Tell `0.7.0_AE_CloudOps~IB2` once what you are about to do (two DEV tickets filed, one claimed, both deleted by key, two `opal-users-v2` rows); the CTO ruled that IB2's run 7H shares no write with a DEV ticket arm, so do not wait for IB2 unless it names a ticket-service act in flight. Weekday: not between 11:30Z and 14:15Z.
    3. Both identity rows ABSENT; the protected tickets `TCK-20261017-da2a1987` and `TCK-20261017-5af976ff` present (read only); print the count of open tickets already on the board (they will appear in the shot).
    THE RUN: (a) mint TWO synthetic identities, `tckt-r23-filer-20261021@opal.invalid` and `tckt-r23-picker-20261021@opal.invalid` (each an `opal-users-v2` row, `PK USER#<address>`, `SK PROFILE`, `firmId opal-capital`, `status active`, `userType "test-filer"`, `allowedFirmIds` the LIST `["cottonwood"]`, written with `attribute_not_exists(PK)` and read back PRESENT with ConsistentRead; one RS256 token each of at most 20 minutes as in `TO-R21-RB1`, held in memory and the one browser context only, never written, logged or traced); (b) as the filer in the browser at `http://localhost:5174`: file ONE Service Request and ONE Other ticket, each for firm `cottonwood`, title and description `synthetic FWD-5 arm`; note both ticket ids; (c) as the picker, in a separate browser context: open the board; do NOT open either ticket; take the FULL-PAGE shot `r23_board_full` (the whole board as rendered, not clipped to a ticket; both new rows must be visible with type and age); read from the board rows, as text, each of the two rows' type label and age text and record them; choose one and record in one sentence what you read that made you choose it; (d) press Claim on the chosen row IN THE BOARD, take the full-page shot `r23_board_claimed`; (e) READ both tickets (`aws dynamodb get-item --consistent-read`) and save the two outputs UNCHANGED, as `{"chosen": <output>, "other": <output>}`, to `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r23_fwd5_dev/R23_FWD5_TICKET_ITEMS.json`; (f) REVIEW the two shots for any client account id or client name beyond ticket id, type, title, requester and age: if one is visible, STOP, delete the shots, report which column, do not commit them; (g) wait until BOTH tokens' `exp` have passed, delete both ticket items and both identity rows by key, read each ABSENT with ConsistentRead; (h) write `R23_FWD5_RESULT.json` in the same folder with exactly the keys the check reads: `browser_origin`, `filer`, `picker`, `chosen_ticket`, `other_ticket`, `board_read` (ticket id -> `{type_label, age_text}` as read from the board row), `chosen_basis`, `claim_via` (`board`), `opened_before_claim` (`false`), `shots` (each role -> `{path, bytes, origin, viewer, full_page, rows_visible}`, the viewer the picker, saved in that folder), `token_exp` (the later of the two), `rows_deleted_at`, `tickets_deleted_at`, `tickets_absent_after`, `rows_absent_after`, `no_engine_call`, `token_printed`, `shot_data_reviewed`. Close the ledger. Report ONCE to `2.0.0_SA_COO~V2` and `1.0.0_SA_CTO~DELL2`.
    IF THE BOARD'S ROWS CARRY NO CLAIM CONTROL, or the board does not show a row's type or its age: shot it, STOP, and report it as FWD-5 failing; do NOT claim from inside a ticket. IF THE SERVER REFUSES the picker's claim (403, 409 or any non-200): STOP, record the status and body, save the items as they stand, remove what the run created, report.
    STOPS: any write other than the two ticket creates, the one claim and the removals; any call to the engine submit; a third ticket; any use of an identity other than the two; a ticket id in the protected set; the origin differing from `http://localhost:5174`; a client account id visible in a shot. On a STOP: remove what the run created by its printed keys, report the world as left, file a surprise row.
  </go>

  <bounds>
    Blast radius (the CVO's `ADJUDICATION_v21` as relayed in the CTO's msg 11772, nothing wider): two `opal-tickets` items created, one claimed, both deleted by key; two `opal-users-v2` rows created then deleted; no S3 write (neither type carries an attachment); no policy, role, routing or Lambda change; no PROD origin. The dev server is stopped when the run ends.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R23F51-AC1" cell_refs="R23-f5-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r23_fwd5_check.py</invocation><expect>^RUN-OK \(fwd5\)</expect></criterion>
  <criterion id="R23F51-AC2J" cell_refs="R23-f5-1" judgment="true"/>
</proof_of_spec>
`R23F51-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file or the saved ticket records`: no result file; its self-test reads `R23-FWD5-SELFTEST-OK`, 25 mutants caught). The check holds the record's side: two tickets of different types by one filer, the chosen one in_progress under the picker with events created then claimed, the other open and unassigned, the board labels equal to the types, the claim made from the board without opening a ticket, the shots full-page PNGs of the recorded size taken as the picker at the DEV origin, both tickets and both rows ABSENT, the protected tickets present. `R23F51-AC2J` is the CVO's: the full-board shot shows several open requests of more than one type together, with each row's type and age readable, and the claim was made from the board.

<preflight>
comp-schedule: RUN-AS-A-READ -- the weekday band at step 2 and the IB2 notice. comp-iam: DECLARED-NOT-APPLICABLE -- the identity rows are written and deleted with the operator's credentials as in `TO-R21-RB1`; no IAM change. comp-adversary: the lens: a claim made from inside a ticket (forbidden: FWD-5 failing is reported), an identity beyond the two or a third ticket (forbidden), a client account id committed in a shot (forbidden: reviewed at step (f)), a token or key printed.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R23-f5-1, FWD-5 on DEV): a live run under the CVO's ADJUDICATION_v21 and the CTO's msg 11772; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
