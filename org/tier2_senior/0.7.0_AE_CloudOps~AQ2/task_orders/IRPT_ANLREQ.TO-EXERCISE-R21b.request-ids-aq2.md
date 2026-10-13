<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-EXERCISE-R21b.request-ids-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-13</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- read only: filter-log-events on one log group; nothing is written to AWS, no identity row, no token, no request is made.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE -- logs:FilterLogEvents, which you used in TO-EXERCISE-R21.
comp-adversary: RUN -- by reading the CTO's condition (msg 7039) against the run's counts; the lens: a RequestId assigned to a line by proximity. The order requires the RequestId to be read from the same log stream's START/END framing and the stream and event timestamps printed, and a line whose RequestId cannot be established is reported UNATTRIBUTED, never guessed. NOT seen: who made the second invocation.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R21B_Y.md</decomp_doc> round 21, workstream YR round 16: the request-id read of the exercise.
<owned_cells>AR-y-230</owned_cells>
</decomp_ref>

  <objective>
    Answer the CTO's condition on the exercise run (CTO half org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_R21_STATUS_RULE_DRIVEN_EXERCISE_CTO_HALF.md; ruling msg 7039): which Lambda RequestId carried each class line of the disabled sub-window, and how many tokens each identity got.
  </objective>

  <context>
    Your record: org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/ (EXERCISE_RESULT.txt, EXERCISE_PHASE2_COUNTS.txt, the two traces and the two scripts). The run's windows are [15:27:04Z, 15:28:45Z) norow, [15:28:45Z, 15:29:50Z) disabled, [15:29:50Z, 15:34:50Z) active, log group /aws/lambda/irpt-directory-search, 3 streams in the sitting window. No new request is made by this order.
  </context>

  <the_act>
    1. Read the events of the log group for the sitting window [15:27:04Z, 15:34:50Z] with filter-log-events (auto-paginated, counted client side; print the window, the stream names and the event count: the run read 30 events in 3 streams). Keep, per event: timestamp, logStreamName, and the message with no identity (class lines carry none; do not copy any other field of a message that holds a name or an account identifier).
    2. Establish the RequestId of every invocation in the window from the START RequestId / END RequestId / REPORT framing of each stream, and attach each INTERNAL-CALLER-CLASS line to the invocation whose START..END span contains its timestamp in its stream. Print a table: RequestId, stream, START time, END time, class lines (class and outcome). A line you cannot place inside one START..END span is UNATTRIBUTED.
    3. Say which RequestId carries the one row_non_active line (the disabled request) and whether its span matches the disabled request's start (15:28:45Z, 101 s after the norow request); state that the 3 row_present/admitted lines of that sub-window carry which RequestIds, and whether they differ from the disabled request's. Also give the RequestIds of the norow line and the active line.
    4. From your two trace files and scripts, count the tokens minted per identity over both phases (norow, disabled, active) and the signing-key reads; one token per identity is the expectation; any other count is a deviation to state, not to repair.
    5. Write the files named in the criteria and report once to 2.0.0_SA_COO~Y2 with the table in words (RequestIds shortened to 8 characters is fine in the report; the file holds them whole).
  </the_act>

  <bounds>
    Read only. No request to the function, no token, no write to DynamoDB or any AWS resource. No message body, name or account identifier in any file or message. A STOP at any step leaves the world as it is.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/IRPT_ANLREQ.TO-EXERCISE-R21b.request-ids-aq2.proof_of_spec.json`.
    <criterion id="R21B-AC1" cell_refs="AR-y-230">Every class line of the sitting window is placed on a RequestId, and none is unattributed.<invocation>grep -cE '^LINE .* request_id=[0-9a-f-]{36} ' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/EXERCISE_REQUEST_IDS.txt</invocation><expect>^[1-9][0-9]*$</expect></criterion>
    <criterion id="R21B-AC2" cell_refs="AR-y-230">The disabled request's row_non_active line is stated with its RequestId and the extra lines with theirs.<invocation>grep -cE '^(DISABLED_LINE|EXTRA_LINES) ' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/EXERCISE_REQUEST_IDS.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="R21B-AC3" cell_refs="AR-y-230">The tokens minted per identity are stated.<invocation>grep -cE '^TOKENS (norow|disabled|active) ' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r21/EXERCISE_REQUEST_IDS.txt</invocation><expect>^3$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a read-only follow-up order to a tier-2 applier on a signed pair's condition (not a worker cell); the cell AR-y-230 is the issuer's, as for TO-APPLY-R20.
