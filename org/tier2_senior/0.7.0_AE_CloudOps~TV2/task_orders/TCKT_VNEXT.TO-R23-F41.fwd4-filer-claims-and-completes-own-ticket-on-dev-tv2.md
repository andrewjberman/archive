<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R23-F41.fwd4-filer-claims-and-completes-own-ticket-on-dev-tv2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-21</date>
    <status>cancelled</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>23</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R23.md</decomp_doc> (round 23): FWD-4 exercised once on DEV, cell `R23-f4-1` (the CTO's PRD v0.7 ADDENDUM 6 and msg 11766).
<owned_cells>R23-f4-1</owned_cells>
</decomp_ref>

  <objective>
    GO under the start gate below. Prove FWD-4 on DEV, ONCE: one synthetic internal sign-in FILES a ticket of a non-analysis type (Service Request), CLAIMS it, and COMPLETES it, through the DEV page; then the saved ticket reads the claimer and the completer equal to the filer; then, after the token `exp`, the ticket (saved whole first) and the filer row are deleted by key and both read ABSENT. The PRD's FWD-4 ACCEPT: "the person who filed a request claims and completes that same request, on any type of ticket; nothing stops them because they filed it".
  </objective>

  <context>
    Why: the CTO (msg 11766) ruled that unit tests cannot meet FWD-4's EXERCISED bar and told the issuer to cut this arm now. The rule is in code (`infra/aws/lambda/ticket_center/lambda_function.py`: `_sod_block` keeps only "a claimed ticket is completed by its assignee"; `claim_ticket` and `complete_ticket` take the requester) and unit-tested; no run in the record has a filer do all three. DEV means what it meant in `TO-R18-RUN`: the portal DEV branch served by `bun run dev --port 5174` on this box, the ONE browser origin `http://localhost:5174` (the laptop CORS list already admits it), against the live ticket service and tables. Model: your `TO-R21-RB1` (mint the synthetic row and token, removal after `exp`) and `TO-R18-RUN` (the DEV origin). The claim fires the isolated pickup notice to the requester address; the filer address is `.invalid`, so no mailbox exists; a failure of that notice never costs a claim.
  </context>

  <go>
    THE START GATE (all printed; a failed item is a STOP before any write):
    1. `check-inbox`. Open the NEVER-2 ledger `tckt-vnext-r23-f41-20261021` FIRST and send its SLUG to `2.0.0_SA_COO~V2`. Census of live open entries naming `opal-ticket-api`, `opal-tickets` or `opal-users-v2` across every live worktree (`git worktree list --porcelain`, then `ls-tree` of `org/critical_paths/.open_deploys/` per tree; print the denominator): 0 open, or STOP.
    2. The portal DEV checkout at the box: print its `git rev-parse HEAD` and that the Service Request type is in the New Ticket type list on `http://localhost:5174` (read, no write). Tell `0.7.0_AE_CloudOps~IB2` once what you are about to do (a DEV ticket filed, claimed, completed and deleted by key, one `opal-users-v2` row); the CTO ruled that IB2's run 7H shares no write with this one, so do not wait for IB2 unless it names a ticket-service act in flight. Weekday: not between 11:30Z and 14:15Z.
    3. The filer row and the ticket ABSENT; the protected tickets `TCK-20261017-da2a1987` and `TCK-20261017-5af976ff` present (read only).
    THE RUN: (a) mint ONE synthetic filer `tckt-r23-filer-20261021@opal.invalid` (`opal-users-v2` `PK USER#<address>`, `SK PROFILE`, `firmId opal-capital`, `status active`, `userType "test-filer"`, `allowedFirmIds` the LIST `["cottonwood"]`, written with `attribute_not_exists(PK)` and read back PRESENT with ConsistentRead; one RS256 token of at most 20 minutes as in `TO-R21-RB1`, held in memory and the one browser context only, never written, logged or traced); (b) in the browser at `http://localhost:5174` as the filer: New Ticket, record the type list, select Service Request and firm `cottonwood`, a title and a description that say `synthetic FWD-4 arm`, shot `r23_form_filled` BEFORE the press, Submit, shot `r23_filed` (the ticket id read from the page); (c) the filer presses Claim on that ticket, shot `r23_claimed`; (d) the filer presses Complete with a one-line resolution `synthetic FWD-4 arm`, shot `r23_completed`; (e) READ the ticket (`aws dynamodb get-item --consistent-read`) and save the whole output UNCHANGED to `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r23_fwd4_dev/R23_FWD4_TICKET_ITEM.json`; (f) wait until the token `exp` has passed, delete the ticket item by its key and the filer row by key, read each ABSENT with ConsistentRead; (g) write `R23_FWD4_RESULT.json` in the same folder with exactly the keys the check reads: `browser_origin`, `filer`, `firm`, `ticket`, `ticket_type`, `claim_via`, `complete_via`, `shots` (each role -> `{path, bytes, origin, viewer}`, saved in that folder), `token_exp`, `row_deleted_at`, `ticket_deleted_at`, `ticket_absent_after`, `row_absent_after`, `no_engine_call`, `token_printed`. Close the ledger. Report ONCE to `2.0.0_SA_COO~V2` and `1.0.0_SA_CTO~DELL2`.
    IF THE PAGE OFFERS THE FILER NO CLAIM OR NO COMPLETE CONTROL on its own ticket: shot it, then make that one call by HTTPS (`POST /api/scoped/tickets/{ticket}/claim`, then `/complete`) with the same token and an empty body (complete: `{"resolution": "synthetic FWD-4 arm"}`), record `claim_via` or `complete_via` as `direct`, and file a surprise row for the missing control. IF THE SERVER REFUSES either call on the filer's own ticket (403, 409 or any non-200): that is FWD-4 failing, not a thing to work around: STOP, record the status and body, save the item as it stands, remove what the run created, report.
    STOPS: any write other than the three ticket acts and the two removals; any call to the engine submit; a second ticket; any use of another identity; a ticket id in the protected set; the origin differing from `http://localhost:5174`. On a STOP: remove what the run created by its printed keys, report the world as left, file a surprise row.
  </go>

  <bounds>
    Blast radius (the CTO's ruling msg 11766, nothing wider): one `opal-tickets` item created, claimed, completed then deleted by key; one `opal-users-v2` row created then deleted; no S3 write (a Service Request carries no attachment); no policy, role, routing or Lambda change; no PROD origin. The dev server is stopped when the run ends.
  </bounds>

<close_note>
  CANCELLED (issuer 2.0.0_SA_COO~V2, 2026-10-21 ~02:5xZ; gate limb: none graded, a status flip on my own order). Withdrawn before TV2 was told of it and before any run: the CVO's ADJUDICATION_v21 graded FWD-4 REALIZED from the R20 DEV run (`tckt-r20-filer` filed, claimed and completed `TCK-20261017-da2a1987`), and the CTO's msg 11772 supersedes his msg 11766. The FWD-5 arm is `TO-R23-F51`. No ledger was opened, nothing was written.
</close_note>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R23F41-AC1" cell_refs="R23-f4-1"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r23_fwd4_check.py</invocation><expect>^RUN-OK \(fwd4\)</expect></criterion>
  <criterion id="R23F41-AC2J" cell_refs="R23-f4-1" judgment="true"/>
</proof_of_spec>
`R23F41-AC1` at the issuance: FAIL as expected (`RUN-BAD cannot read the result file or the saved ticket record`: no result file; its self-test reads `R23-FWD4-SELFTEST-OK`, 17 mutants caught). The check holds the record's side: one address as requester, assignee and the actor of the created, claimed and completed events, status completed, the ticket and the filer row ABSENT, the shots PNGs of the recorded size taken at the DEV origin as the filer, the protected tickets present. `R23F41-AC2J` is the CVO's: the four shots show the filer filing, claiming and completing its own ticket on the page.

<preflight>
comp-schedule: RUN-AS-A-READ -- the weekday band at step 2 and the IB2 notice. comp-iam: DECLARED-NOT-APPLICABLE -- the filer row is written and deleted with the operator's credentials as in `TO-R21-RB1`; no IAM change. comp-adversary: the lens: a second identity or a second ticket (forbidden), a claim or complete by the engine path (forbidden), a refusal of the filer's own claim worked around (forbidden: reported as FWD-4 failing), a token or key printed.
</preflight>

# pipeline-override: a RUN order to the dell2 applier for an issuer cell (R23-f4-1, FWD-4 on DEV): a live run under the CTO's PRD v0.7 ADDENDUM 6 and msg 11766; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
