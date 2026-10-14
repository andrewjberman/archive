<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-EXERCISE-R28b.door-d1d4-internal-viewer-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-14</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed Addendum 1 (section 5): one users row for one sitting, four door requests, two synthetic stored inputs that stay.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; the sitting calls the upload door's route, once per case, as the addendum says.
comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; step 1 reads your own grants as met (the same as TO-EXERCISE-R28) and stops if one is missing.
comp-adversary: RUN -- by reading TO-EXERCISE-R28's result (SITTING_RESULT.txt: D1 to D4 refused NOT_AUTHORIZED, C1 parsed three REFUSAL envelopes and proved nothing) against this cell; the lens: a C1 that passes on a refusal envelope, a door case read as passed because the status was 200, a row that outlives the sitting. The order requires every arm to be an answer body (NEEDS_CORRECTION or NORMALIZED) and C1 to parse answer bodies only, keeps only status, finding code and sha256, and removes the row after exp with a bounded GSI read. NOT seen: the live users rows (0 read before the sitting), the live edge's header handling for an internal class beyond what the code shows.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R37A_Y.md</decomp_doc> round 37, workstream ZB: the door steps D1-D4 and C1 as one synthetic Opal-internal viewer.
<owned_cells>AR-y-307</owned_cells>
</decomp_ref>

  <objective>
    Prove the upload door's NEW answers live, ONCE, as ONE synthetic Opal-internal viewer with synthetic files only: D1 (a two-account file is turned back), D2 (a one-account file is accepted), D3 (a Shares file with no price date is accepted and priced at the previous trading day), D4 (the stored input of D2 re-opens), and C1 (the answer bodies parse in the portal's reader). Then remove the minted row. You change no code and apply nothing. Then STOP and report.
  </objective>

  <context>
    Load /cloud-ops first. Signed: Addendum 1 COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release28/NEVER_WIDEN_PAIR_ANLREQ_RELEASE28_ADDENDUM_1_D1D4_INTERNAL_VIEWER.md (git hash-object must print a blob that starts 909ca2c466) and its CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE28_ADDENDUM_1_D1D4_INTERNAL_VIEWER_CTO_HALF.md (@daf0a6043e, CTO msg 7507). A different COO blob voids both halves: STOP. The method and the thirteen-line result format are those of org/tier2_senior/0.7.0_AE_CloudOps~AQ2/task_orders/IRPT_ANLREQ.TO-EXERCISE-R28.release-28-sitting-aq2.md (read its AMENDMENTS 1 and 2, and your script and offline run in deliverables/irpt_anlreq_r28/): REUSE your script's mint, request and removal functions; only the identity and the arms change. The release-28 pair's section 5 steps D1 to D4 and C1 define the cases.
    **THE IDENTITY (Addendum 1, section 3):** ONE users PROFILE row `irpt-r28-iv-<YYYYMMDD>@opal.invalid` (lowercase; the date of the sitting) in opal-users-v2, written with attribute_not_exists(PK), status the exact string active, the user class the authorizer reads as an INTERNAL human (read how the door's InteractiveAccess.current() decides `verified_internal_subject`, _scope/interactive_access.py :78-99, and mint the claims it needs, nothing more), allowedFirmIds ["49financial"] and nothing else (the on-behalf door refuses an absent, empty or ALL value). NO partner row. ONE RS256 token for it (the current signing slot; exp at most 20 minutes after iat; held in your process only, never written, never logged). If the door sends mail to this address, STOP.
    **Not exercised, not to be:** the ticket service, any other route, any firm other than 49financial (selected_tenant=49financial), any real client file, a second token, a partner-firm caller (the door refuses it until the authorizer cell AR-y-306 is released: that is a later pair).
  </context>

  <the_act>
    GO: both halves of Addendum 1 are signed; start at step 1.
    1. Read the addendum's COO half and CTO half at HEAD. Read the four legs as closed, read-only (irpt-status MIVrDbv+/w8ioVB24xS97gnETVbNRCroDiY+Ne5osbA=; opal-ticket-api C/Rt/FnSqOj7SnZC1GeoEilj8jbCKdvAUHnxYrnNZNM=; irpt-ycharts-generate reAjAQOVVfD4Wui2u0UfZRt7cr9o6ioFKIwXa+8EVgc=); anything else: STOP, report. Read your own grants as met (DynamoDB read, conditional put and conditional delete on the one key; the signing-key read; the intake store read of the two inputs you will name). Open the NEVER-2 ledger irpt-r28-door-20261014 (legs M mint, D door, X removal) and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: an open entry naming opal-users-v2 or irpt-ycharts-generate is a STOP.
    2. ConsistentRead the IV key and the email-index (GSI) for the address: ABSENT. Any other state: STOP, nothing written. Write the row (conditions as above); read it back ConsistentRead. Mint the token.
    3. Create three small SYNTHETIC CSV files in your .scratch (outside the repository; round numbers, tickers SYNTHA SYNTHB SYNTHC style, no client data): D1 a two-account file whose account column is headed Accnt (two identifier-like values); D2 a one-account file with the column headed Acct Market Value; D3 a file with a Shares column and NO price date. Requests, each ONCE, at least 15 s apart, to the door's route as the internal viewer with selected_tenant=49financial (the route and the body shape are in the AR-y-276 design record and the portal's investor-reporting.ts; read them): D1, D2, D3, then D4 (re-open of D2's stored input). Keep only status, the finding code or state and the sha256 of the body.
    4. EXPECTED (any other outcome is a FAIL of that arm, not a reassignment): D1 NEEDS_CORRECTION with ACCOUNT_COLUMN_SEVERAL_VALUES; D2 NORMALIZED; D3 NORMALIZED and the answer carries the previous trading day's price date (compute lib/trading_calendar.py prev_trading_day for today and print both); D4 the stored input re-opens and is accepted. A door arm that answers NOT_AUTHORIZED: STOP at once, go to step 6, report the classifier code (do NOT try another identity). A wrong D1 (a two-account file ACCEPTED) is a BLOCKING row; tell 1.0.0_SA_CTO~DELL2 and 2.0.0_SA_COO~Y2 in the same hour.
    5. C1: the bodies of D1, D2 and D3, in process, through parseIrEnvelope loaded from the portal at origin/PROD (git show of src/pages/InvestorReporting/contracts/envelope.ts and its imports into a scratch folder; a bun one-liner reading the body from a file you delete at once). Each body must be an ANSWER (NEEDS_CORRECTION or NORMALIZED), not a refusal envelope, and each must parse without a throw. A refusal envelope parsed is `C1 NOT RUN`, not a pass. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/DOOR_RESULT.txt with, ONE line exactly each: `D1 NEEDS_CORRECTION ACCOUNT_COLUMN_SEVERAL_VALUES`, `D2 NORMALIZED`, `D3 NORMALIZED price_date=<YYYY-MM-DD>`, `D4 ACCEPTED`, `C1 PARSED 3 of 3 answers`; a line for an arm that did not pass reads `<arm> FAIL <status> <code>`.
    6. After the token's exp has passed: delete the row (attribute_exists), then read the address by the GSI AND a ConsistentRead GetItem until ABSENT, repeating a lagging GSI read in a printed bounded window of 5 minutes. A PRESENT read after the window is a STOP. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/DOOR_REMOVAL.txt with `ABSENT GSI <address>` and `ABSENT CONSISTENT <address>`. Name, in the report, the two synthetic stored inputs (D2 and D3) by input id and tenant: they are NOT deleted by you (an S3 delete is Andrew's word; the CTO asks for the ids). Close the ledger and report ONCE to 2.0.0_SA_COO~Y2 and 1.0.0_SA_CTO~DELL2. The signing-key read is reported through 0.0.0_AB_MSTR~DELL2 as in R2.
  </the_act>

  <bounds>
    One opal-users-v2 item for one sitting; the door's route, four requests; the intake store's two synthetic inputs (they stay, named); no partner row; no write through any other route; no other firm; no second token; no holdings read; no row that outlives the sitting; no response body, account identifier or name in any file, log, trace or message (status, code and sha256 only); no real client file. Rollback: delete the item, read the GSI and a ConsistentRead ABSENT. A write fails or the token is refused at the edge: remove what was written, record the status and reason, no retry.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/IRPT_ANLREQ.TO-EXERCISE-R28b.door-d1d4-internal-viewer-aq2.proof_of_spec.json`.
    <criterion id="R28F-AC1" cell_refs="AR-y-307">Each door arm answered as expected and C1 parsed answers.<invocation>grep -cE '^(D1 NEEDS_CORRECTION ACCOUNT_COLUMN_SEVERAL_VALUES|D2 NORMALIZED|D3 NORMALIZED price_date=[0-9]{4}-[0-9]{2}-[0-9]{2}|D4 ACCEPTED|C1 PARSED 3 of 3 answers)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/DOOR_RESULT.txt</invocation><expect>^5$</expect></criterion>
    <criterion id="R28F-AC2" cell_refs="AR-y-307">The address reads ABSENT by the GSI and by a ConsistentRead after the removal.<invocation>grep -cE '^ABSENT (GSI|CONSISTENT) irpt-r28-iv-[0-9]{8}@opal.invalid$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r28/DOOR_REMOVAL.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="R28F-AC3" cell_refs="AR-y-307">The ledger irpt-r28-door-20261014 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-r28-door-20261014_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an exercise order to a tier-2 applier under a signed addendum (not a worker cell); the cell AR-y-307 is the issuer's, as for TO-EXERCISE-R28.
