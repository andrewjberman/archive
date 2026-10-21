<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-EXERCISE-R21.status-rule-driven-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-13</date>
    <status>withdrawn -- the run executed and was recorded complete, but its criterion R21E-AC1 reads 2 of the 3 expected lines in EXERCISE_RESULT.txt (re-run 2026-10-21); it was never a pass as written, so the issuer 2.0.0_SA_COO~Y2 retires it from the round-43 verdict on 2026-10-21 (round hygiene) instead of grading it complete; the closed ledger and the receipts stand as history</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed pair (COO half section 5; CTO half "Conditions added").
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed; three GETs on the existing route. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; if a grant is missing at step 1 the order STOPS.
comp-adversary: RUN -- by reading the R2-cw-1 precedent (a row without email reads absent; a GSI read lags a delete) and the pair's section 4 against this cell; the lens: a refusal read as a pass when the row was never found, a class line read in the wrong sub-window, a row left behind. The order requires the email on the row, the GSI-and-ConsistentRead pre-read, the 60 s spacing with per-sub-window counts, and the removal read by both paths. NOT seen: the live token path and the edge's header rewrite.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R21A_Y.md</decomp_doc> round 21, workstream YR round 13: the applier acts of the round.
<owned_cells>AR-y-224</owned_cells>
</decomp_ref>

  <objective>
    Exercise the status rule through the live edge in ONE sitting: two synthetic internal identities (`norow`, `disabled`) each selecting cottonwood on irpt-directory-search must be REFUSED FIRM_BINDING with one class line each (`row_absent`, `row_non_active`); only if both refuse, a third (`active`) is ADMITTED with `row_present`. Then remove the rows and read all three addresses ABSENT. Nothing is kept of any response body.
  </objective>

  <context>
    Load /cloud-ops first. SIGNED PAIR: COO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release21/NEVER_WIDEN_PAIR_ANLREQ_STATUS_RULE_DRIVEN_EXERCISE.md (git hash-object d1d4296341, full id d1d4296341cbfb641595fddad558c2efdd2702fc; @4f8e80f124) and CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_R21_STATUS_RULE_DRIVEN_EXERCISE_CTO_HALF.md (@decdd94c48, CTO msg 7011, choice (A)). A different COO blob voids both halves: STOP. The pair IS the plan; read it whole: section 2 (route, request, firm), section 3 (the identities and rows; THE ROW MUST CARRY email), section 4 (steps 0-6), section 5 (blast radius), section 7 (both branches), and the CTO half's four added conditions. The design record with the offline predictions and the precedent mint steps is org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~69/r21/EXERCISE_DESIGN.json; the R2-cw-1 pair (org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_CW1_CRAWL_PAIR.md) shows how a sitting token was minted and held. Re-derive everything you run.
    The addresses: irpt-r21-status-norow@opal.invalid, irpt-r21-status-disabled@opal.invalid, irpt-r21-status-active@opal.invalid. The selection is `selected_tenant=cottonwood`, no other query member, no body.
  </context>

  <the_act>
    1. Step 0 of the pair: read your own grants as met (DynamoDB conditional write, delete and read on the three keys, the signing-key read, logs:FilterLogEvents). A grant missing: STOP, file a surprise row naming it, report; never an order to another box. Open the NEVER-2 ledger irpt-status-rule-exercise-20261013 and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: an open entry naming opal-users-v2 or irpt-directory-search is a STOP.
    2. Pair step 1: ConsistentRead the three USER# keys: all ABSENT; the email-index query for the three addresses returns nothing. Any other state: STOP, nothing written.
    3. Pair step 2: write the `disabled` row and the `active` row (attribute_not_exists(PK); each with email, firmId opal-capital, userType test-filer, allowedFirmIds ["cottonwood"], status as named); read each back with ConsistentRead. `norow` writes nothing.
    4. Pair steps 3-4 with the CTO half's conditions: mint ONE token per identity (current signing slot, exp at most 20 minutes after iat and long enough for the sitting; held in your process only, never written). Requests in this order: `norow`, then `disabled`, then `active` ONLY IF both refused; at least 60 s between requests; record each request's UTC start, status, refusal code and the sha256 of the body; keep no body.
    5. Pair step 5, per sub-window: count the INTERNAL-CALLER-CLASS class lines of /aws/lambda/irpt-directory-search for each request's own sub-window (its start to the next request's start, the last to +5 minutes), auto-paginated, counted client side; print the window, the distinct logStreamName count and the total per sub-window. Zero streams searched is VOID. Expected: exactly one line per sub-window with the class named; a line in another sub-window or a wrong class is a FAIL, not a reassignment.
    6. Pair step 6: after the LATER exp has passed, delete the written rows (condition attribute_exists(PK)); then read ALL THREE addresses by the GSI AND a ConsistentRead GetItem until ABSENT (repeat a lagging GSI read in a printed bounded window). A PRESENT read after the delete is a STOP. Write the files named in the criteria, close the ledger, send the counts to 1.0.0_SA_CTO~DELL2 and report once to 2.0.0_SA_COO~Y2. The signing-key read is reported through 0.0.0_AB_MSTR~DELL2 as in R2.
  </the_act>

  <bounds>
    As the pair's section 5 and the CTO half "Not covered": two opal-users-v2 items for one sitting, three GETs of the one route with selected_tenant=cottonwood, no write through the route, no other firm or route, no second token, no holdings read, no row that outlives the sitting, no response body, account identifier or name in any file, log, trace or message. A refusal arm that ADMITS: do not run `active`, remove the rows (step 6), close the ledger FAILED, file a BLOCKING row, tell 1.0.0_SA_CTO~DELL2 and 2.0.0_SA_COO~Y2 the same hour. A write fails or a token is refused at the edge: remove what was written, record the status and reason, no retry with a second token. Rollback per key: delete the item, read GSI and ConsistentRead ABSENT.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/IRPT_ANLREQ.TO-EXERCISE-R21.status-rule-driven-aq2.proof_of_spec.json`.
    <criterion id="R21E-AC1" cell_refs="AR-y-224">Each arm's outcome and its own sub-window's class line are recorded.<invocation>grep -cE '^(norow REFUSED FIRM_BINDING class=row_absent lines=1|disabled REFUSED FIRM_BINDING class=row_non_active lines=1|active ADMITTED status=200 class=row_present lines=1)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/EXERCISE_RESULT.txt</invocation><expect>^3$</expect></criterion>
    <criterion id="R21E-AC2" cell_refs="AR-y-224">All three addresses read ABSENT by the GSI and by a ConsistentRead after the removal.<invocation>grep -cE '^ABSENT (GSI|CONSISTENT) irpt-r21-status-(norow|disabled|active)@opal.invalid$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/EXERCISE_REMOVAL.txt</invocation><expect>^6$</expect></criterion>
    <criterion id="R21E-AC3" cell_refs="AR-y-224">The ledger irpt-status-rule-exercise-20261013 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-status-rule-exercise-20261013_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair (not a worker cell); the cell AR-y-224 is the issuer's, as for TO-APPLY-R20.
<!-- ISSUER NOTE 2026-10-13 (2.0.0_SA_COO~Y2): status flipped to complete: every step ran, ledger CLOSED, proof instance VALID. R21E-AC1 is recorded FAIL (2 of 3): the disabled sub-window holds 4 class lines (1 row_non_active plus 3 row_present/admitted from a second invocation not made by the applier; row D2-S74). The CTO ruled (msg 7039) PASS with no re-run on the condition answered by TO-EXERCISE-R21b (RequestIds, tokens per identity). The run was in two phases on the same rows because refusals travel as HTTP 200 envelopes. -->
